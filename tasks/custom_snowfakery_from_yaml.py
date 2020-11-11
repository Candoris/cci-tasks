from cumulusci.tasks.bulkdata import GenerateAndLoadData
from tasks.custom_generate_data_from_yaml import CustomGenerateDataFromYaml


bulkgen_task = "tasks.custom_generate_data_from_yaml.CustomGenerateDataFromYaml"

# This is an entrypoint for CustomGenerateAndLoadData. See GenerateAndLoadData for more info.


class CustomSnowfakeryFromYaml(GenerateAndLoadData):
    """Generate and load data from Snowfakery in as many batches as necessary"""

    task_options = {
        **GenerateAndLoadData.task_options,
        **CustomGenerateDataFromYaml.task_options,
    }

    def _init_options(self, kwargs):
        args = {"data_generation_task": bulkgen_task, **kwargs}
        super()._init_options(args)
