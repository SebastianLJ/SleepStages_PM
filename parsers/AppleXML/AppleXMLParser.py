import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from json import dumps, loads
import xml.etree.ElementTree as ET
from datetime import datetime
import csv

class AppleXMLParser():
    def __init__(self, filename):
        self.filename = filename
        self.xml_file = open(filename, "r")

    def parse_to_csv(self):
        # parse xml file
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        # open the file in the write mode
        header = ["caseId", "startDate", "endDate", "activity"]
        with open('out/log.csv', 'w', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write header
            writer.writerow(header)
            for record in root.findall("Record"):
                row = []
                activity = record.attrib["value"]
                if (self.is_sleep_stage_valid(activity)):
                    created_date = datetime.strptime(record.attrib["creationDate"], "%Y-%m-%d %H:%M:%S %z")
                    start_date = datetime.strptime(record.attrib["startDate"], "%Y-%m-%d %H:%M:%S %z")
                    end_date = datetime.strptime(record.attrib["endDate"], "%Y-%m-%d %H:%M:%S %z")
                    row.append(created_date.replace(tzinfo=None))
                    row.append(start_date.replace(tzinfo=None))
                    row.append(end_date.replace(tzinfo=None))
                    row.append(self.convert_apple_sleep_stage_to_text(activity))
                    writer.writerow(row)
                

    def convert_apple_sleep_stage_to_text(self, stage):
        if (stage == "HKCategoryValueSleepAnalysisAsleepCore"):
            return "Core"
        elif (stage == "HKCategoryValueSleepAnalysisAsleepREM"):
            return "REM"
        elif (stage == "HKCategoryValueSleepAnalysisAsleepDeep"):
            return "Deep"
        elif (stage == "HKCategoryValueSleepAnalysisAwake"):
            return "Awake"
        else:
            return "Unknown"
    
    def is_sleep_stage_valid(self, stage):
        return self.convert_apple_sleep_stage_to_text(stage) != "Unknown"

if __name__ == "__main__":
    parser = AppleXMLParser("test.xml")
    parser.parse_to_csv()