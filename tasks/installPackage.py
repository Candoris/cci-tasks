from cumulusci.core.config import ScratchOrgConfig
from cumulusci.tasks.command import Command
from cumulusci.tasks.sfdx import SFDXBaseTask
from cumulusci.tasks.sfdx import SFDXOrgTask

class Install(SFDXOrgTask):
    command = "force:package:install -p "
    extra = "-r"

    task_options = {
        "packageVersionId": {
          "description": "The Version Id of the Package to install.",
          "required": True,
        },
        "installationKey": {
          "description": "The installation key required to install the package."
        },
        "clearPackageFile": {
          "description": "Initialize the package install list file."
        }
    }

    def _get_command(self):
        self.options["command"] = self.command + self.options["packageVersionId"]
        self.options["extra"] = self.extra

        installKey = self.options.get("installationKey")
        clearPackageFile = self.options.get("clearPackageFile")
        
        if installKey is not None:
          self.options["command"] += " -k " + installKey

        if clearPackageFile is not None:
          f = open(".packageInstallList", "w")
          f.write("")
          f.close()

        return super()._get_command()

    def _process_output(self, line):
        if "sfdx" in str(line):
          statusCommand = str(line).replace("b'","").replace("\\n'", "")
          idStartPosition = statusCommand.find("-i") + 3
          idEndPosition = idStartPosition + 18
          requestId = statusCommand[idStartPosition:idEndPosition]
          
          f = open(".packageInstallList", "a")
          f.write(requestId + "\n")
          f.close()