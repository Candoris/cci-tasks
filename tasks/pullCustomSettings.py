from cumulusci.tasks.salesforce import BaseSalesforceApiTask
import yaml


class PullSettings(BaseSalesforceApiTask):

    def _run_task(self):
        self.logger.info("Beginning to pull custom settings...")
        unwantedFields = ["CreatedById", "CreatedDate", "Id", "IsDeleted",
                          "LastModifiedById", "LastModifiedDate", "SetupOwnerId", "SystemModstamp"]

        # Gather all settings from Salesforce
        res = self.sf.describe()

        masterList = {}

        # Filter the entries to result in only custom settings
        customSettings = []
        for x in res["sobjects"]:
            if x["customSetting"]:
                customSettings.append(x)

        # For every custom setting
        for setting in customSettings:
            settingName = setting["name"]
            fields = getattr(self.sf, settingName).describe()["fields"]

            isHierarchy = False

            # build the query for this setting
            first = True
            query = "SELECT"
            for field in fields:
                if field["name"] == "Name":
                    isHierarchy = field["nillable"]
                if first:
                    query += " " + field["name"]
                    first = False
                else:
                    query += ", " + field["name"]
            query += " FROM " + settingName

            # execute the query
            queryResult = self.sf.query(query)

            # If query is non-empty, add fields/values to masterList using the appropriate format
            if queryResult["totalSize"] > 0:
                if isHierarchy:
                    # HIERARCHY
                    settingProperties = {"location": "org"}
                    settingFields = {}
                    for field in fields:
                        if field["name"] not in unwantedFields:
                            name = field["name"]
                            value = queryResult["records"][0][name]

                            settingFields[name] = value

                    settingProperties["data"] = settingFields
                    masterList[settingName] = [settingProperties]
                else:
                    # LIST
                    settingRecords = {}
                    for i in range(queryResult["totalSize"]):
                        recordDict = {}
                        recordName = queryResult["records"][i]["Name"]
                        for field in fields:
                            if field["name"] not in unwantedFields and field["name"] != "Name":
                                name = field["name"]
                                value = queryResult["records"][i][name]

                                recordDict[name] = value

                        settingRecords[recordName] = recordDict

                    masterList[settingName] = settingRecords

        self.logger.info("MasterList:")
        self.logger.info(masterList)

        # Write the results to a yaml file
        yamlContents = yaml.safe_dump(masterList)
        f = open("orgCustomSettings.yml", "w")
        f.write(yamlContents)
        f.close()

        self.logger.info("Pulling custom settings has completed")
