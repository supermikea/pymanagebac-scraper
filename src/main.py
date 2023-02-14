from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from getpass import getpass
import re

driver = webdriver.Firefox()

subdomain = input("subdomain: ")
email = input("school-mail: ")

# login
driver.get(f"https://{subdomain}.managebac.com/login")
email_box = driver.find_element(By.ID, "session_login")
email_box.send_keys(email)
password_box = driver.find_element(By.ID, "session_password")
# TODO after putting characters and then erasing it the page throws a javascript error
password_box.send_keys(getpass("Password for Managebac.com: "))
submit_button = driver.find_element(By.NAME, "commit")

login_button = ActionChains(driver=driver)
login_button.click(on_element=submit_button)
login_button.perform()

# TODO check if login info is correct

input("press enter when the page is loaded...")  # TODO remove this line with something automatic

# today = driver.find_element(By.CLASS_NAME, "")
days = driver.find_elements(By.CLASS_NAME, "day")
# print(days)

all_days = []

# put raw information in list
for day in days:
    text = re.split("\n", day.text, flags=re.DOTALL)
    all_days.append(text)

print(all_days)

temp = []

# sort the raw information by date and remove empty dates
for day in all_days:
    if len(day) == 1:
        continue
    temp.append(day)

all_days = temp

print(all_days)

# done extracting info so we quit
driver.quit()
