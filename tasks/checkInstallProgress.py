import time

from cumulusci.core.tasks import BaseTask
from cumulusci.tasks.sfdx import SFDXOrgTask

class ProgressCommand(SFDXOrgTask):
    result = False

    def _get_command(self):
        return super()._get_command()
    
    def _process_output(self, line):
        if not ("sfdx" in str(line)):
          print(str(line).replace("b'","").replace("\\n'", ""))
          self.result = not ("InProgress" in str(line))

class CheckProgressList(BaseTask):
    def _run_task(self):
        file = open(".packageInstallList")
        lines = file.readlines()
        file.close()

        for line in lines:
            if len(line.strip()) == 18:
                self.task_config.options = {
                  "command": "force:package:install:report -i",
                  "extra": line.strip()
                }

                progressCommand = ProgressCommand(
                    project_config = self.project_config,
                    task_config = self.task_config,
                    org_config = self.org_config
                )

                sleepTime = 30

                while not progressCommand.result:
                  progressCommand._run_task()
                  if not progressCommand.result:
                    sleepMessage = "waiting {sleepTime} seconds...".format(sleepTime=sleepTime)
                    print(sleepMessage)
                    time.sleep(sleepTime)
        
        f = open(".packageInstallList", "w")
        f.write("")
        f.close()
