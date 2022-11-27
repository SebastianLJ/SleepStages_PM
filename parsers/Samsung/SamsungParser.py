import csv
from datetime import datetime


def is_noise(row):
    start = datetime.strptime(row[1], '%Y-%m-%d %H:%M')
    end = datetime.strptime(row[2], '%Y-%m-%d %H:%M')
    duration = end - start
    duration = duration.total_seconds() / 60

    if duration == 1:
        return True
    else:
        return False


def clean():
    with open('samsung_log_raw.csv') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        csv_titles = data[0]
        del data[0]
        data = [row for row in data if row]

        case_ids = []

        for row in data:
            if not row[0] in case_ids:
                case_ids.append(row[0])

        data = [row for row in data if not is_noise(row)]

        # combining identical activities that appears sequentially within the same day
        new_list = []
        current_index = 0

        indicies = range(len(data))

        while current_index in indicies:

            print(current_index)
            current_event = data[current_index]

            if current_index == len(data) - 1:
                new_list.append(current_event)
                break

            next_index = current_index + 1

            while next_index in range(len(data)):
                next_event = data[next_index]
                if current_event[0] == next_event[0] and current_event[3] == next_event[3]:
                    current_event[2] = next_event[2]
                    next_index += 1
                else:
                    current_index = next_index
                    break

            new_list.append(current_event)

        data = new_list

        myFile = open('samsung_log_cleaned.csv', 'w')
        writer = csv.writer(myFile)
        writer.writerow(csv_titles)
        for data_list in data:
            writer.writerow(data_list)
        myFile.close()


def enumerated():
    with open('samsung_log_cleaned.csv') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        csv_titles = data[0]
        del data[0]
        data = [row for row in data if row]

        case_ids = []

        for row in data:
            if not row[0] in case_ids:
                case_ids.append(row[0])

        for case in case_ids:
            case_events = [event for event in data if event[0] == case]

            REM_index = 1
            Light_index = 1
            Deep_index = 1
            Awake_index = 1

            for event in case_events:
                if event[3] == "REM":
                    event[3] = "REM" + str(REM_index)
                    REM_index += 1
                if event[3] == "Light":
                    event[3] = "Light" + str(Light_index)
                    Light_index += 1
                if event[3] == "Deep":
                    event[3] = "Deep" + str(Deep_index)
                    Deep_index += 1
                if event[3] == "Awake":
                    event[3] = "Awake" + str(Awake_index)
                    Awake_index += 1

        myFile = open('samsung_log_cleaned_enumerated.csv', 'w')
        writer = csv.writer(myFile)
        writer.writerow(csv_titles)
        for data_list in data:
            writer.writerow(data_list)
        myFile.close()

def durations():
    with open('samsung_log_cleaned.csv') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        csv_titles = data[0]
        del data[0]
        data = [row for row in data if row]

        case_ids = []

        for row in data:
            if not row[0] in case_ids:
                case_ids.append(row[0])

        for case in case_ids:
            case_events = [event for event in data if event[0] == case]

            for event in case_events:
                start = datetime.strptime(event[1], '%Y-%m-%d %H:%M')
                end = datetime.strptime(event[2], '%Y-%m-%d %H:%M')
                duration = end - start
                duration = duration.total_seconds() / 60
                duration = round(duration, -1)

                if duration == 0:
                    event[3] += '<10min'
                if duration == 10:
                    event[3] += '10min'
                if duration == 20:
                    event[3] += '20min'
                if duration == 30:
                    event[3] += '30min'
                if duration == 40:
                    event[3] += '40min'
                if duration == 50:
                    event[3] += '50min'
                if duration == 60:
                    event[3] += '60min'
                if duration > 60:
                    event[3] += '>60min'

        myFile = open('samsung_log_cleaned_duration.csv', 'w')
        writer = csv.writer(myFile)
        writer.writerow(csv_titles)
        for data_list in data:
            writer.writerow(data_list)
        myFile.close()

def main():
    clean()
    #enumerated()
    #durations()

