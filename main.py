import requests
from bs4 import BeautifulSoup
import time
import re
import os
import sys
from seleniumbase import Driver

def clear(operating_system):
    match operating_system:
        case 'win32':
            os.system('cls')
        case 'linux':
            os.system('clear')

def phone_records(driver: Driver):
    phone_number = input("Phone Number: ")
    phone_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', str(phone_number))
    driver.open(f'https://www.usphonebook.com/{phone_number}')
    driver.wait_for_element('a.ls_contacts-btn.newcolor')
    driver.click('a.ls_contacts-btn.newcolor')
    name = driver.find_element('p.ls_contacts__sub').text
    age = driver.find_element('p.ls_contacts__age').text
    address = driver.find_element('p.ls_contacts__text').text
    print(name, age, address)

def phone_carrier():
    phone_number = input("Phone Number: ")
    soup = BeautifulSoup(requests.get(f"https://whocalld.com/+1{phone_number}").content, "html.parser")

    data = str(soup.find("div", {"class": "page"}).find('p')).split('.')
    device_type = data[0].split('<p> This seems to be a ')[1]
    device_carrier_info = data[1].split(' The carrier for this number is ')[1].split(' in ')
    device_carrier = device_carrier_info[0]
    device_carrier_location = device_carrier_info[1]
    print(device_type, device_carrier, device_carrier_location)

def breach_data(driver: Driver):
    email = input("E-mail Address (ex. johndoe@gmail.com): ")
    driver.open("https://haveibeenpwned.com/")
    driver.type('input#Account.form-control', email)
    driver.click('button#searchPwnage.btn.btn-primary.btn-lg')
    driver.wait_for_element('div#breachDescription.pwnedSearchResult.pwnTypeDefinition.pwnedWebsite.panel-collapse.collapse.in')
    companyTitles = driver.find_elements('div.row span.pwnedCompanyTitle')
    dataClasses = driver.find_elements('div.row p.dataClasses')
    breach = dict(zip([element.text for element in companyTitles], [element.text for element in dataClasses]))

    with open('./breach_data.txt', 'w') as writer:
        writer.write(f"{email}\n\n")
        for i, v in breach.items():
            print(f"\033[0;91m{i} \033[0m-> {v}\033[0m")
            writer.write(f"{i} -> {v}\n")

logo = """\033[0;35m
  ______   _______    ______    ______   ______  __    __  ________ 
 /      \ |       \  /      \  /      \ |      \|  \  |  \|        \\
|  $$$$$$\| $$$$$$$\|  $$$$$$\|  $$$$$$\ \$$$$$$| $$\ | $$ \$$$$$$$$
| $$   \$$| $$__| $$| $$  | $$| $$___\$$  | $$  | $$$\| $$   | $$   
| $$      | $$    $$| $$  | $$ \$$    \   | $$  | $$$$\ $$   | $$   
| $$   __ | $$$$$$$\| $$  | $$ _\$$$$$$\  | $$  | $$\$$ $$   | $$   
| $$__/  \| $$  | $$| $$__/ $$|  \__| $$ _| $$_ | $$ \$$$$   | $$   
 \$$    $$| $$  | $$ \$$    $$ \$$    $$|   $$ \| $$  \$$$   | $$   
  \$$$$$$  \$$   \$$  \$$$$$$   \$$$$$$  \$$$$$$ \$$   \$$    \$$   
                                                                    
"""

menu = r"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                           1. Phone Records                                                                      ┃
┃                           2. Phone Carrier                                                                      ┃
┃                           3. Breach Data                                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

driver = Driver(uc=True, headed=True)

operating_system = sys.platform
while True:
    clear(operating_system)
    print(logo)
    print(menu)
    choice = int(input("\t\tChoice: "))
    match choice:
        case 1:
            clear(operating_system)
            phone_records(driver)
            time.sleep(30)
        case 2:
            clear(operating_system)
            phone_carrier()
            time.sleep(30)
        case 3:
            clear(operating_system)
            breach_data(driver)
            time.sleep(30)

