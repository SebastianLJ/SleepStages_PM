import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from json import dumps, loads
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import csv

class AppleXMLParser():
    def __init__(self, filename, enumerate=False, duration=False):
        self.filename = filename
        self.xml_file = open(filename, "r")
        self.enumerate = enumerate
        self.duration = duration
        
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
                    #if self.get_duration_interval(start_date, end_date).seconds == 0:
                    #    continue
                    row.append("AW-" + created_date.strftime("%Y-%m-%d"))
                    row.append(start_date.replace(tzinfo=None))
                    row.append(end_date.replace(tzinfo=None))
                    if (self.enumerate):
                        row.append(self.enumerate_sleep_stages(self.convert_apple_sleep_stage_to_text(activity)))
                    elif (self.duration and self.get_duration_interval(start_date, end_date).seconds > 0):
                        row.append(self.duration_sleep_stages(self.convert_apple_sleep_stage_to_text(activity), start_date, end_date))
                    elif (not self.enumerate and not self.duration):
                        row.append(self.convert_apple_sleep_stage_to_text(activity))
                    writer.writerow(row)
                
    def enumerate_sleep_stages(self, stage):
        if stage == "Core":
            self.core_count += 1
            return "Core " + str(self.core_count)
        elif stage == "REM":
            self.REM_count += 1
            return "REM " + str(self.REM_count)
        elif stage == "Deep":
            self.deep_count += 1
            return "Deep " + str(self.deep_count)
        elif stage == "Awake":
            self.awake_count += 1
            return "Awake " + str(self.awake_count)

    def duration_sleep_stages(self, stage, start_date, end_date):
        return stage + " " + str(int(self.get_duration_interval(start_date, end_date).seconds/60)) + " min"
    
    def get_duration_interval(self, start_date, end_date):
        delta = timedelta(minutes=10)
        return self.round_dt(end_date - start_date, delta)
    
    def convert_apple_sleep_stage_to_text(self, stage, verify=False):
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
        return self.convert_apple_sleep_stage_to_text(stage, verify=True) != "Unknown"

    # https://stephenallwright.com/python-round-time-15-minutes/
    def round_dt(self, dt, delta):
        return round((dt) / delta) * delta

if __name__ == "__main__":
    parser = AppleXMLParser("sleep_nov_6.xml", enumerate=False, duration=True)
    parser.parse_to_csv("single_bad_sleep_enum_10.csv")