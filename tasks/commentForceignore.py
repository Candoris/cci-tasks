from cumulusci.core.tasks import BaseTask

class CommentProfile(BaseTask):

    task_options = {
        "comment_profile": {
            "description": "Boolean describing if the profile line should be commented",
            "required": True,
        }
    }

    def _run_task(self):

        commentProfile = self.options["comment_profile"]

        file = open(".forceignore")
        text = file.read()
        file.close()

        if commentProfile.lower() == "true":
            print("Commenting profile line")
            output = text.replace("**profile", "# **profile")
        elif commentProfile.lower() == "false":
            print("Uncommenting profile line")
            output = text.replace("# **profile", "**profile")
        else:
            # throw error
            raise Exception("comment_line must be either 'true' or 'false'")

        f = open(".forceignore", "w")
        f.write(output)
        f.close()
        