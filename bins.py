from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


print("Bin Day Scraper")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--postcode", required=True)
parser.add_argument("-n", "--number", required=True)
args = parser.parse_args()
houseno = args.number
postcode = args.postcode

print("Launching Chrome")
# Options so that we can run headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)

# Set location to UK/London
params = {
    "latitude": 51.507351,
    "longitude": -0.127758,
    "accuracy": 100
}
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

# Set Timezone to London
tz_params = {'timezoneId': 'Europe/London'}
driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
print("Loading site")
# Initial page with postcode search option
driver.get('https://www.gateshead.gov.uk/article/3150/Bin-collection-day-checker')
# driver.implicitly_wait(5)

print("Rejecting cookies")
# Find the dumb cookies button that blocks us from proceeding
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, value="rejectall"))
)
# reject_cookies_button = driver.find_element(by=By.NAME, value="rejectall")
reject_cookies_button.click()
print("Entering postcode")

text_box = driver.find_element(by=By.ID, value='BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPPOSTCODE') #.send_keys('NE216EZ')
submit_button = driver.find_element(by=By.ID, value="BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPSEARCH")

# Add postcode to search box
text_box.send_keys(postcode)
submit_button.click()
print("Selecting house number")
# Find the address drop down and select our address - though any would do!
address_select = driver.find_element(by=By.ID, value="BINCOLLECTIONCHECKER_ADDRESSSEARCH_ADDRESSLOOKUPADDRESS")
select = Select(address_select)
option_list = select.options

opts_to_select = [o for o in option_list if houseno in o.text]
my_option = opts_to_select[0]
select.select_by_visible_text(my_option.text)

print("Processing Results")
# Grab the table with the collection data
table = driver.find_element(By.CLASS_NAME, "bincollections__table")
txt = table.text
#print(txt)
month = ""
'''
# Iterate and print out which bin on which date
for i, line in enumerate(txt.splitlines()):
    if line[0].isdigit():
        [date, day, bin, *excess] = line.split(' ')
        print(f"Putting the {bin} bin out on {day} the {date} of {month}")
    else:
        month = line
        #print(f"Processing the month of {line}")
'''
import calendar
month_to_num = {name: num for num, name in enumerate(calendar.month_name) if num}
month = month_to_num['January']

import datetime
today = datetime.date.today()
year = today.year


from datetime import datetime

txt = table.text
month = ""
op = '{"processeddate":"'
op = op + datetime.now().strftime("%Y-%m-%d %H:%M:%S") +'","bins":['
first_month = None
for i, line in enumerate(txt.splitlines()):
    if line[0].isdigit():
        [date, day, bin, *excess] = line.split(' ')
        date_str = f"{year}-{month}-{date} 7:00:00"
        date_format = '%Y-%m-%d %H:%M:%S'

        date_obj = datetime.strptime(date_str, date_format)
        op = op + '{"date":' +f'"{date_obj}", "bin": "{bin}"' + "},"
    else:
        month = month_to_num[line]
        if first_month == None:
            first_month = month
        else:
            if month < first_month:
                year = year + 1
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
