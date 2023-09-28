from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By


def is_website(input_str):
    # Convert input string to lowercase for case-insensitive comparison
    lower_input_str = input_str.lower()

    # Check if the input string contains 'www.' and a domain extension like '.com', '.org', etc.
    if 'www.' in lower_input_str or (any(ext in lower_input_str for ext in ['.com', '.org', '.net', '.io', '.co.uk']) and "@" not in lower_input_str):
        return True

    return False


def is_valid_phone_number(input_str):
    # Remove spaces and hyphens from the input string
    cleaned_str = input_str.replace(" ", "").replace("-", "")

    # Check if the cleaned string contains only numeric characters
    if cleaned_str.isdigit() or (cleaned_str.startswith("+44") and cleaned_str[1:].isdigit()) or (cleaned_str.startswith("+1") and cleaned_str[1:].isdigit()):
        return True
    else:
        return False


filename = "data"
link = "https://www.google.com/maps/search/vet+clinic+in+london/@51.547699,-0.1323168,13z?entry=ttu"
city = "London"
browser = webdriver.Chrome()
record = []


def Selenium_extractor():
    # action = ActionChains(browser)
    time.sleep(15)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
    print(len(a))

    for i in range(len(a)):
        business_element = a[i]
        browser.execute_script("arguments[0].scrollIntoView(true);", business_element)
        a[i].click()
        time.sleep(1)
        try:
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')
            Name_Html = soup.findAll('h1', {"class": "DUwDvf"})
            name = Name_Html[0].text
            divs = soup.findAll('div', {"class": "Io6YTe"})
            business_data = {}
            business_data["name"] = name
            for z in range(len(divs)):
                item = divs[z].text
                if z == 0:
                    business_data["address"] = item
                elif is_website(item):
                    business_data["website"] = item
                elif is_valid_phone_number(item):
                    business_data["number"] = item
                else:
                    pass
            # print(business_data)
            # ratings
            div_rating_element = soup.findAll('div', class_='F7nice')
            rating = div_rating_element[0].text
            business_data["rating"] = rating
            # print("------------------------------------------------------------------------------------")
            record.append(business_data)
        except:
            print("error")

    # CSV file name
    csv_file = 'londonvets.csv'
    df = pd.DataFrame(record)
    df.to_csv(csv_file, index=False)
    print(f"CSV file '{csv_file}' has been created successfully.")


browser.get(str(link))
time.sleep(10)
Selenium_extractor()
