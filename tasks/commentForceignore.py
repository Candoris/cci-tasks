from cumulusci.core.tasks import BaseTask


class CommentForceIgnore(BaseTask):

    task_options = {
        "commented": {
            "description": "Boolean describing if the specified lines should be commented",
            "required": True,
        },
        "items": {
            "description": "Comma separated list of items to be changed in the forceignore file",
            "required": True,
        }
    }

    def process_bool_arg(self, arg):
        """Determine True/False from argument."""
        if isinstance(arg, (int, bool)):
            return bool(arg)
        elif isinstance(arg, str):
            if arg.lower() in ["yes", "y", "true", "on", "1"]:
                return True
            elif arg.lower() in ["no", "n", "false", "off", "0"]:
                return False
        raise TypeError(f"Cannot interpret as boolean: `{arg}`")

    def _run_task(self):

        should_be_commented = CommentForceIgnore.process_bool_arg(
            self, self.options["commented"])

        item_list = self.options["items"].split(",")

        file = open(".forceignore")
        text = file.read()
        file.close()

        if should_be_commented:
            print("Commenting specified lines")
            for item in item_list:
                text = text.replace("\n" + item, "\n# " + item)
        elif not should_be_commented:
            print("Uncommenting specified lines")
            for item in item_list:
                text = text.replace("# " + item, item)
        else:
            # throw error
            raise Exception(
                "'commented' parameter must be either 'True' or 'False'")

        f = open(".forceignore", "w")
        f.write(text)
        f.close()
