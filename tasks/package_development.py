import json

from cumulusci.salesforce_api.metadata import ApiRetrieveInstalledPackages
from cumulusci.tasks.salesforce import BaseSalesforceTask
from cumulusci.tasks.salesforce import BaseSalesforceApiTask
from cumulusci.tasks.salesforce import UpdateDependencies


class ListDependencies(UpdateDependencies):
    """
    This class overrides a few key methods of the standard UpdateDependencies to resolve dependencies in manner defined by CumulusCI, while not actually installing the dependencies. Results in a List of dependencies.
    """

    def _run_task(self):
        self.results = []
        super()._run_task()
        return self.results

    def _process_dependencies(self, dependencies):
        for dependency in dependencies:
            subdependencies = dependency.get("dependencies")
            if subdependencies:
                self._process_dependencies(subdependencies)

            if ("namespace" in dependency):
                self.results.append(dependency)

    def _uninstall_dependencies(self):
        None

    def _uninstall_dependencies(self):
        None

    def _install_dependencies(self):
        None


class ResolveDependencies(ListDependencies, BaseSalesforceApiTask):
    """
    Adds package aliases to sfdx-project.json for each packageDirectory dependencies list. Also adds subscriber package version ids to list of packageAliases.
    """

    def _add_dependency(self, packageDirectory):
        """
        Helper function used in map() to add packages to each packageDirectories in sfdx-project.json
        """
        packageDirectory["dependencies"] = self.packages
        return packageDirectory

    def _run_task(self):
        self.dependencies = []
        with open("sfdx-project.json", "r") as f:
            data = json.load(f)

        # super() refers to ListDependencies
        self.dependencies = super()._run_task()

        # Get installed packages
        self.installed_packages = self.tooling.query(
            'SELECT SubscriberPackage.NamespacePrefix, SubscriberPackageVersionId FROM InstalledSubscriberPackage')

        self.packages = []
        for dependency in self.dependencies:
            self.packages.append({'package': dependency["namespace"]})
            # Add subscriber package version ids to packageAliases. For each namespace (e.g., packageAliases.npe01), lookup the installed package record and grab the SubscriberPackageVersionId.
            data["packageAliases"][dependency["namespace"]] = next(
                filter(
                    lambda record: record["SubscriberPackage"]["NamespacePrefix"] == dependency[
                        "namespace"], self.installed_packages["records"]
                ), None
            )["SubscriberPackageVersionId"]

        # For each package directory, add dependencies.
        data["packageDirectories"] = list(
            map(self._add_dependency, data["packageDirectories"]))

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

        data["packageDirectories"] = list(
            map(self._set_default, data["packageDirectories"]))

        with open("sfdx-project.json", "w") as f:
            f.write(json.dumps(data, indent=2))
