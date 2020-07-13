from faker import Faker
from cumulusci.salesforce_api.metadata import ApiRetrieveInstalledPackages
from cumulusci.tasks.salesforce import BaseSalesforceTask
from cumulusci.tasks.salesforce import BaseSalesforceApiTask
from cumulusci.tasks.salesforce import UpdateDependencies
import datetime

class CreateTestData(BaseSalesforceApiTask):
  task_options = {
    "sql_path": {
      "description": "The path to the metadata source to be deployed",
      "required": True,
    },
    "num_records": {
      "description": "The number of records to create",
      "required": False,
    }
  }

  def _run_task(self):
    fake = Faker()

    if("num_number" in self.options):
      num_records = self.options["num_records"] 
    else:
      num_records = 100

    script_lines = ['BEGIN TRANSACTION;']

    # Accounts
    # TODO: Have an array that tracks Names to check for duplicates and then regenerate
    script_lines.append('CREATE TABLE "Account" (')
    script_lines.append('id INTEGER NOT NULL,')
    script_lines.append('"Name" VARCHAR(255),')
    script_lines.append('"Type" VARCHAR(255),')
    script_lines.append('"BillingStreet" VARCHAR(255),')
    script_lines.append('"BillingCity" VARCHAR(255),')
    script_lines.append('"BillingState" VARCHAR(255),')
    script_lines.append('"BillingPostalCode" VARCHAR(255),')
    script_lines.append('"BillingCountry" VARCHAR(255),')
    script_lines.append('"ShippingStreet" VARCHAR(255),')
    script_lines.append('"ShippingCity" VARCHAR(255),')
    script_lines.append('"ShippingState" VARCHAR(255),')
    script_lines.append('"ShippingPostalCode" VARCHAR(255),')
    script_lines.append('"ShippingCountry" VARCHAR(255),')
    script_lines.append('"Phone" VARCHAR(255),')
    script_lines.append('"HouseholdPhone" VARCHAR(255),')
    script_lines.append('"AccountType" VARCHAR(255),')
    script_lines.append('PRIMARY KEY (id)')
    script_lines.append(');')

    for index in range(num_records):
      account_address = fake.street_address()

      # Organization or Household specific values
      if (index % 2) == 0:
        account_name = account_address
        account_type = ''
        record_type = 'Household Account'
      else:
        account_name = fake.company()
        account_type = fake.word(ext_word_list=['Corporate', 'Nonprofit', 'Government', 'Foundation'])
        record_type = 'Organization'

      account_line = 'INSERT INTO "Account" VALUES('
      account_line += str(index) + ','

      account_line += '\'' + account_name + '\','
      
      account_line += '\'' + account_address + '\','
      account_line += '\'' + fake.city() + '\','

      state_code = fake.state_abbr()

      account_line += '\'' + state_code + '\','
      account_line += '\'' + fake.zipcode_in_state(state_abbr=state_code) + '\','
      account_line += '\'United States\','
      account_line += '\'\','
      account_line += '\'\','
      account_line += '\'\','
      account_line += '\'\','
      account_line += '\'\','
      account_line += '\'' + fake.phone_number() + '\','
      account_line += '\'' + fake.phone_number() + '\','
      account_line += '\'' + account_type + '\','
      account_line += '\'' + record_type + '\''

      
      account_line += ');'
      script_lines.append(account_line)

    # Contacts
    # TODO: AccountId should only be Household accounts
    # TODO: Primary affiliations should only be Organization accounts
    script_lines.append('CREATE TABLE "Contact" (')
    script_lines.append('id INTEGER NOT NULL,')
    script_lines.append('"FirstName" VARCHAR(255),')
    script_lines.append('"LastName" VARCHAR(255),')
    script_lines.append('"Deceased" VARCHAR(255),')
    script_lines.append('"DoNotContact" VARCHAR(255),')
    script_lines.append('"PreferredPhone" VARCHAR(255),')
    script_lines.append('"PreferredEmail" VARCHAR(255),')
    script_lines.append('"HomePhone" VARCHAR(255),')
    script_lines.append('"MobilePhone" VARCHAR(255),')
    script_lines.append('"WorkPhone" VARCHAR(255),')
    script_lines.append('"PersonalEmail" VARCHAR(255),')
    script_lines.append('"WorkEmail" VARCHAR(255),')
    script_lines.append('"AccountId" VARCHAR(255),')
    script_lines.append('"npsp__Primary_Affiliation__c" VARCHAR(255),')
    script_lines.append('PRIMARY KEY (id)')
    script_lines.append(');')

    account_assignments = []

    for index in range(num_records):
      account_assignments.append(fake.random_int(min=0, max=(num_records - 1)))

    account_assignments.sort()

    for index in range(num_records):
      account_line = 'INSERT INTO "Contact" VALUES('
      account_line += str(index) + ','
      if (index % 2) == 0:
        account_line += '\'' + fake.first_name_male() + '\','
        account_line += '\'' + fake.last_name_male() + '\','
      else:
        account_line += '\'' + fake.first_name_female() + '\','
        account_line += '\'' + fake.last_name_female() + '\','
      # account_line += '\'' + fake.date_of_birth(minimum_age=18).strftime("%d-%m-%Y") + '\','
      account_line += '\'' + str(fake.boolean(chance_of_getting_true=5)) + '\','
      account_line += '\'' + str(fake.boolean(chance_of_getting_true=5)) + '\','
      account_line += '\'' + fake.word(ext_word_list=['Home', 'Work', 'Mobile']) + '\','
      account_line += '\'' + fake.word(ext_word_list=['Personal', 'Work']) + '\','
      account_line += '\'' + fake.phone_number() + '\','
      account_line += '\'' + fake.phone_number() + '\','
      account_line += '\'' + fake.phone_number() + '\','
      account_line += '\'' + fake.ascii_safe_email() + '\','
      account_line += '\'' + fake.ascii_safe_email() + '\','
      account_line += '\'' + str(account_assignments[index]) + '\','
      account_line += '\'' + str(account_assignments[index]) + '\''
      account_line += ');'
      script_lines.append(account_line)



    # print(fake.word(ext_word_list=['Partners','General','Global','Campus 1', 'Campus 2']))'

    script_lines.append('COMMIT;')

    with open(self.options["sql_path"], "w") as outfile:
        outfile.write("\n".join(script_lines))
        print("File created at " + self.options["sql_path"])