from cumulusci.tasks.salesforce import BaseSalesforceApiTask
import yaml


class PullSettings(BaseSalesforceApiTask):

    def _run_task(self):
        self.logger.info("Beginning to pull custom settings...")
        unwantedFields = ["CreatedById", "CreatedDate", "Id", "IsDeleted", "LastModifiedById", "LastModifiedDate", "Name", "SetupOwnerId", "SystemModstamp"]

        # Gather all settings from Salesforce
        res = self.sf.describe()

        masterList = {}
        
        # Filter the entries to result in only custom settings
        customSettings = []
        for x in res["sobjects"]:
            if x["customSetting"]:
                customSettings.append(x)

        # for every custom setting
        for setting in customSettings:
            settingName = setting["name"]
            fields = getattr(self.sf, settingName).describe()["fields"]
            # build the query for this setting
            first = True
            query = "SELECT"
            for field in fields:
                if first:
                    query += " " + field["name"]
                    first = False
                else:
                    query += ", " + field["name"]
            query += " FROM " + settingName

            # execute the query
            queryResult = self.sf.query(query)

            # if query is non-empty, add fields/values to masterList
            if queryResult["totalSize"] > 0:
                settingProperties = { "location": "org" }
                settingFields = {}
                for field in fields:
                    if field["name"] not in unwantedFields:
                        name = field["name"]
                        value = queryResult["records"][0][name]

                        settingFields[name] = value
                
                settingProperties["data"] = settingFields
                masterList[settingName] = [ settingProperties ]

        self.logger.info("MasterList:")
        self.logger.info(masterList)
            
        # write the results to a yaml file
        yamlContents = yaml.safe_dump(masterList)
        f = open("orgCustomSettings.yml", "w")
        f.write(yamlContents)
        f.close()

        self.logger.info("Pulling custom settings has completed")
