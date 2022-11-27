# Sleep Assesment via Process Mining

## Apple Watch Event Log Parser
How to run the parser
1. Enter the path to the file to parse on line 102 in AppleXMLParser.py
`parser = AppleXMLParser("your_apple_data.xml", enumerate=False, duration=False)`
2. Enter the name of the output file with the parsed data
`parser.parse_to_csv("your_event_log.csv")`
3. A parsed file in csv format is now located in /out/

## Samsung Watch Event Log Parser