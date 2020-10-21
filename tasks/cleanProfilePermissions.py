from cumulusci.core.tasks import BaseTask
import xml.etree.ElementTree as ET
import os

class CleanProfile(BaseTask):

    def _run_task(self):

        unwantedValues = [
            "AllowUniversalSearch",
            "AllowViewKnowledge",
            "EditKnowledge",
            'FieldServiceAccess',
            "ManageKnowledge",
            "ManageKnowledgeImportExport",
            "ManageSearchPromotionRules",
            "SendExternalEmailAvailable",
            "ShareInternalArticles",
            "ViewDataLeakageEvents",
            "WorkCalibrationUser",
            "CreateWorkBadgeDefinition",
            "Contact.CleanStatus",
            "Case.Positive_Behavior"
        ]

        folder = "force-app/main/default/profiles"
        files = os.listdir(folder)
        # for every file in the directory
        for f in files:
            # if the file is a .xml file
            if ".xml" in f:
                profileLocation = folder + "/" + f

                tree = ET.parse(profileLocation)
                root = tree.getroot()

                entriesToRemove = []

                # for all of the categories
                for category in root:
                    # for all of the fields/values
                    for field in category:
                        if field.text in unwantedValues:
                            entriesToRemove.append(category)

                removedItems = 0
                for entry in entriesToRemove:
                    root.remove(entry)
                    removedItems += 1

                print(f)
                print("Removed Items:", removedItems)

                # tree.write(open("testOutput.xml", "wb"))
                tree.write(profileLocation)

                file = open(profileLocation)

                newOutput = file.read().replace("ns0:", "")
                newOutput = newOutput.replace(":ns0", "")
                file.close()

                f = open(profileLocation, "w")
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + newOutput)
                f.close()
