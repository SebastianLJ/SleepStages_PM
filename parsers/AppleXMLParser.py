import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from json import dumps, loads
import xml.etree.ElementTree as ET
from datetime import datetime

class AppleXMLParser():
    def __init__(self, filename):
        self.filename = filename
        self.xml_file = open(filename, "r")

    def parse_to_xes(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        for record in root.findall("Record"):
            print(record.attrib)

if __name__ == "__main__":
    parser = AppleXMLParser("test.xml")
    parser.parse_to_xes()