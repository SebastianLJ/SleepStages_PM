import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from json import dumps, loads
import xml.etree.ElementTree as ET
from datetime import datetime
import csv

class AppleXMLParser():
    def __init__(self, filename, enumerate=False):
        self.filename = filename
        self.xml_file = open(filename, "r")
        self.enumerate = enumerate
        
        self.reset_counters()
        self.previous_case_id = None

    def reset_counters(self):
        self.awake_count = 0
        self.core_count = 0
        self.deep_count = 0
        self.REM_count = 0

    def parse_to_csv(self, output_filename="output.csv"):
        # parse xml file
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        # open the file in the write mode
        header = ["caseId", "startDate", "endDate", "activity"]
        with open('out/'+output_filename, 'w', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write header
            writer.writerow(header)
            for record in root.findall("Record"):
                row = []
                activity = record.attrib["value"]
                if (self.is_sleep_stage_valid(activity)):
                    created_date = datetime.strptime(record.attrib["creationDate"], "%Y-%m-%d %H:%M:%S %z")
                    if (self.previous_case_id != created_date):
                        self.previous_case_id = created_date
                        self.reset_counters()
                    start_date = datetime.strptime(record.attrib["startDate"], "%Y-%m-%d %H:%M:%S %z")
                    end_date = datetime.strptime(record.attrib["endDate"], "%Y-%m-%d %H:%M:%S %z")
                    row.append("AW-" + created_date.strftime("%Y-%m-%d"))
                    row.append(start_date.replace(tzinfo=None))
                    row.append(end_date.replace(tzinfo=None))
                    row.append(self.convert_apple_sleep_stage_to_text(activity))
                    writer.writerow(row)
                

    def convert_apple_sleep_stage_to_text(self, stage, verify=False):
        if (stage == "HKCategoryValueSleepAnalysisAsleepCore"): 
            if (self.enumerate) and not verify:
                self.core_count += 1
                return "Core " + str(self.core_count)
            return "Core"
        elif (stage == "HKCategoryValueSleepAnalysisAsleepREM"):
            if (self.enumerate and not verify):
                self.REM_count += 1
                return "REM " + str(self.REM_count)
            return "REM"
        elif (stage == "HKCategoryValueSleepAnalysisAsleepDeep"):
            if (self.enumerate and not verify):
                self.deep_count += 1
                return "Deep " + str(self.deep_count)
            return "Deep"
        elif (stage == "HKCategoryValueSleepAnalysisAwake"):
            if (self.enumerate and not verify):
                self.awake_count += 1
                return "Awake " + str(self.awake_count)
            return "Awake"
        else:
            return "Unknown"
    
    def is_sleep_stage_valid(self, stage):
        return self.convert_apple_sleep_stage_to_text(stage, verify=True) != "Unknown"

if __name__ == "__main__":
    parser = AppleXMLParser("sleep_day_1-5.xml", enumerate=True)
    parser.parse_to_csv("log5_enumerated.csv")