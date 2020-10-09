from pathlib import Path
import shutil

import yaml

from cumulusci.tasks.bulkdata.generate_from_yaml import GenerateDataFromYaml
from snowfakery.output_streams import SqlOutputStream
from snowfakery.data_generator import generate, StoppingCriteria
from snowfakery.generate_mapping_from_recipe import mapping_from_recipe_templates

'''
The purpose of this custom generator is to remove the __ from "hidden" objects in the mapping.yml. This allows us to create dummy objects to manually set an Id for references in Snowfakery templates.

Example:

- object: Analytic__c
  count:
    random_number:
      min: 1
      max: 3
  fields:
    Legislation__c:
      object: __Legislation__c
      fields:
        id:
          random_number:
            min: 1
            max: 10
'''


class CustomGenerateDataFromYaml(GenerateDataFromYaml):
    def postProcessMapping(self, mapping):
        for table in mapping.values():
            if "lookups" in table:
                for reference in table["lookups"].values():
                    if reference["table"].startswith("__"):
                        self.logger.info(
                            f'Replacing {reference["table"]} with {reference["table"][2:]}')
                        reference["table"] = reference["table"][2:]

    def generate_data(self, db_url, num_records, current_batch_num):
        output_stream = SqlOutputStream.from_url(db_url, self.mapping)
        old_continuation_file = self.get_old_continuation_file()
        if old_continuation_file:
            # reopen to ensure file pointer is at starting point
            old_continuation_file = open(old_continuation_file, "r")
        with self.open_new_continuation_file() as new_continuation_file:
            try:
                with open(self.yaml_file) as open_yaml_file:
                    summary = generate(
                        open_yaml_file=open_yaml_file,
                        user_options=self.vars,
                        output_stream=output_stream,
                        stopping_criteria=self.stopping_criteria,
                        continuation_file=old_continuation_file,
                        generate_continuation_file=new_continuation_file,
                    )
            finally:
                output_stream.close()

            if (
                new_continuation_file
                and Path(new_continuation_file.name).exists()
                and self.working_directory
            ):
                shutil.copyfile(
                    new_continuation_file.name, self.default_continuation_file_path()
                )

        mapping = mapping_from_recipe_templates(summary)
        self.postProcessMapping(mapping)

        if self.generate_mapping_file:
            with open(self.generate_mapping_file, "w+") as f:
                yaml.safe_dump(
                    mapping, f, sort_keys=False
                )
