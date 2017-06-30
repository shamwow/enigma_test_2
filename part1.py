import csv
import re
from datetime import datetime
from date_formats import date_formats

state_code_to_name_map = None
def state_code_to_name(code):
    global state_code_to_name_map

    # Only get state name mapping from CSV once.
    if state_code_to_name_map is None:
        state_code_to_name_map = {}
        with open('state_abbreviations.csv', 'rb') as file:
            csv_file = csv.reader(file, delimiter=',', quotechar='"')
            for row in csv_file:
                state_code_to_name_map[row[0]] = row[1]

    return state_code_to_name_map[code]

def clean_bio(bio):
    return re.sub(r'\s+', ' ', bio.strip())


def try_parse_date(raw_date, date_format):
    try:
        return datetime.strptime(raw_date, date_format)
    except ValueError:
        return None


def parse_date(raw_date):
    for date_format in date_formats:
        post_parse_action = date_formats[date_format]

        parse_result = try_parse_date(raw_date, date_format)

        if parse_result is None:
            continue

        post_parse_result = post_parse_action(parse_result)

        return (post_parse_result.strftime('%Y-%m-%d'), '')

    return ('', raw_date)


with open('test.csv', 'rb') as file:
    csv_file = csv.reader(file, delimiter=',', quotechar='"')

    with open('solution.csv', 'wb') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"')

        for idx, row in enumerate(csv_file):
            print('Processing row %s' % idx)

            # Skip column rows.
            if idx == 0:
                row.insert(11, 'start_date_description',)
                writer.writerow(row)
                continue

            # Clean bio.
            row[8] = clean_bio(row[8])

            # Get state name.
            row[5] = state_code_to_name(row[5])

            # Parse date.
            formatted_date, date_desc = parse_date(row[10])
            row[10] = formatted_date
            row.insert(11, date_desc)

            writer.writerow(row)
