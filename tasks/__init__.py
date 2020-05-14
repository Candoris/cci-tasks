import json

from cumulusci.salesforce_api.metadata import ApiRetrieveInstalledPackages
from cumulusci.tasks.salesforce import BaseSalesforceTask
from cumulusci.tasks.salesforce import BaseSalesforceMetadataApiTask

class ResolveDependencies(BaseSalesforceMetadataApiTask):
    api_class = ApiRetrieveInstalledPackages
    name = "GetInstalledPackages"

    def _add_dependency(self, packageDirectory):
        packageDirectory["dependencies"] = self.dependencies
        return packageDirectory

    def _package_to_dependency(self, item):
        return { 'package': f'{item[0]}@{item[1]}' }

    def _run_task(self):
        result = super()._run_task()
        with open("sfdx-project.json", "r") as f:
            data = json.load(f)

        # result = {
        #     "npe01": "3.14",
        #     "npe4": "3.10",
        #     "npe03": "3.19",
        #     "npo02": "3.12",
        #     "npsp": "3.176",
        #     "npe5": "3.8"
        # }
        #
        # Converts above to managed package dependency format. See https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev2gp_config_file.htm
        self.dependencies = list(map(self._package_to_dependency, result.items()))

        # For each package directory, add dependencies.
        data["packageDirectories"] = list(map(self._add_dependency, data["packageDirectories"]))

        with open("sfdx-project.json", "w") as f:
            f.write(json.dumps(data, indent=2))

class SetDefault(BaseSalesforceTask):
    task_options = {
        "dir": {
            "description": "Directory to set as default",
            "required": True,
        }
    }

    def _set_default(self, dir):
        dir["default"] = dir["path"] == self.default_dir
        return dir

    def _run_task(self):
        self.default_dir = self.options.get("dir")

        with open("sfdx-project.json", "r") as f:
            data = json.load(f)

        data["packageDirectories"] = list(map(self._set_default, data["packageDirectories"]))

        with open("sfdx-project.json", "w") as f:
            f.write(json.dumps(data, indent=2))
