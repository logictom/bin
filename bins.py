
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--postcode", required=True)
parser.add_argument("-n", "--number", required=True)
args = parser.parse_args()
houseno = args.number
postcode = args.postcode

from seleniumbase import SB
# 1. Python script to load this webpage using seleniumbase
# https://www.gateshead.gov.uk/article/3150/Bin-collection-day-checker
resulting_data = None
with SB(uc=True, test=True, locale="en-GB") as sb:
    url = "https://www.gateshead.gov.uk/article/3150/Bin-collection-day-checker"
    sb.activate_cdp_mode(url)
    # 2. Script then waits for the page to load
    
    # 3. Script should reject any cookies
    print("Rejecting cookies")
    sb.click('button[name="rejectall"]')
    
    # 4. Solve any captchas if presented
    print("Solving captcha if present")
    sb.solve_captcha()
    
    # 5. Script then enters this postcode: "NE21 6EZ" into the "BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPPOSTCODE" input 
    print("Entering postcode")
    sb.type('input#BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPPOSTCODE', postcode)
    

    # 6. Click the "Find address" button
    print("Submitting postcode")
    sb.click('input#BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPSEARCH')
    # sb.sleep(2)

    # 7. Script then waits for the <select> element to appear and selects the address with the partial match "41"
    select_id = "#BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPADDRESS"
    print("Waiting for address select element")
    sb.wait_for_element(select_id, timeout=15)
    print("Waiting for address options to populate")
    sb.wait_for_element(select_id + " option", timeout=15)
    # Try to find an option that contains 'houseno' and select it by value
    print(f"Scanning options for a match containing '{houseno}'")
    options = sb.execute_script(
        "return Array.from(document.querySelectorAll('" + select_id + " option')).map(function(o){return {t:o.textContent.trim(), v:o.value};});"
    )
    match = None
    for opt in options:
        if opt and isinstance(opt, dict) and 't' in opt and houseno in opt['t']:
            match = opt
            print("Match found:", match)
            break
    if match:
        print(f"Selecting option: {match['t']}")
        sb.select_option_by_value(select_id, match['v'])
        print("Option selected")
        sb.sleep(2)
        #sb.assert_selected_option(select_id, match['t'])
        print("Selection confirmed")
        sb.sleep(2)
    else:
        # Provide debug output of available options to help diagnosis
        print("Available options:")
        for opt in options:
            print(repr(opt))
        raise Exception("No address option containing '41' was found")

    # 8. Script waits for the new table, bincollections__table, to load and selects the table contents and prints it to the console
    print("Waiting for bin collection table to load")
    sb.wait_for_element("table.bincollections__table", timeout=15)
    table_text = sb.get_text("table.bincollections__table")
    print("Bin Collection Table:")
    print(table_text)
    # 9. Finally, the script should close the browser
    print("Test completed, closing browser")
    resulting_data = table_text


    # with open("Output.txt", "w") as text_file:
    #     text_file.write(resulting_data)

import calendar
from datetime import datetime, date

month_to_num = {name: num for num, name in enumerate(calendar.month_name) if num}
month = month_to_num['January']

today = date.today()
year = today.year

# resulting_data = None
# with open('Output.txt', 'r') as file:
#     resulting_data = file.read()
txt = resulting_data

# strip leading/trailing whitespace characters from each line and remove lines equal to "Thursday"
txt = '\n'.join([line.strip() for line in txt.splitlines() if line.strip() != "Thursday"])

# remove empty lines
txt = '\n'.join([line for line in txt.splitlines() if line.strip() != ""])

# if the line ends with a digit, move the next line to the end of the current line
lines = txt.splitlines()
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line and line[-1].isdigit() and i + 1 < len(lines):
        line = line + ' ' + lines[i + 1]
        i += 1
    new_lines.append(line)
    i += 1
txt = '\n'.join(new_lines)

month = ""
first_month = None

op = '{"processeddate":"'
op = op + datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'","bins":['

op = '{"processeddate":"'
op = op + datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'","bins":['

for i, line in enumerate(txt.splitlines()):
    if line[0].isdigit():
        [date, bin, *excess] = line.split(' ')

        # print(f"{date}:{month}:{year} : {bin}")
        date_str = f"{year}-{month}-{date} 7:00:00"
        date_format = '%Y-%m-%d %H:%M:%S'
        date_obj = datetime.strptime(date_str, date_format)
        op = op + '{"date":' +f'"{date_obj}", "bin": "{bin}"' + "},"

    else:
        first = line.split(maxsplit=1)[0]
        month = month_to_num[first]
        if first_month == None:
            first_month = month
        else:
            if month < first_month:
                year += 1
        [x, date, bin, *excess] = line.split(' ')

op = op[:-1]
op = op + "],"

date_str = f"{year}-{month}-{int(date)+1} 7:00:00"
date_format = '%Y-%m-%d %H:%M:%S'
date_obj = datetime.strptime(date_str, date_format)

op = op + f'"triggerdate" : "{date_obj}"' + '}'

print("Writing json file")
with open("bins.json", mode="w") as f:
    f.write(op)
print("Done")


