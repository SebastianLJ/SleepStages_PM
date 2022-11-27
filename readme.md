# Sleep Assesment via Process Mining

## Apple Watch Event Log Parser
How to run the parser
1. Enter the path to the file to parse on line 102 in AppleXMLParser.py
> `parser = AppleXMLParser("your_apple_data.xml", enumerate=False, duration=False)`
2. Enter the name of the output file with the parsed data on line 103
> `parser.parse_to_csv("your_event_log.csv")`
4. Run AppleXMLParser
> `python3 AppleXMLParser.py`
3. A parsed file in csv format is now located in /out/

## Samsung Watch Event Log Parser
How to run the parser:<br />

The file is split into 3 methods: <br />
Clean(): Removes noise from the raw data. Noise is defined as a sleep stage lasting 1 minute or less. <br />
Enumerated(): Creates a version of the log where each stage has a number that indicates it's count in the current sleep.<br />
Durations(): Creates a version of the log where each stage ahs a number that indicates it's duration rounded to nearest 10.<br />

There is a main method at the bottom of the file that runs one of these, and where the rest are commented out.<br />

Each method has an input file path, and an export file path. A sample raw samsung data file is provided to rest the parser. 
