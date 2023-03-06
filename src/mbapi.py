import re
import time
import threading

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.options import Options

import bs4
import lxml

class classe:
    def __init__(self, class_id: int, name: str):
        self.class_id = class_id
        self.name = name

class grade:
    def __init__(self, number: int, task: object, date: str):
        """
        :type number: int
        :type task: object
        :type date: str
        """
        self.number = number
        self.task = task
        self.date = date

class task:
    def __init__(self, date, title: str, description: str):
        """

        :type date: str
        :type title: str
        :type description: str
        """
        self.date = date
        self.description = description
        self.name = title

class mbapi:

    def __init__(self, mail: str, password: str, impl_wait=5., hide_window=True, logging_level=None):

        def get_subdomain(mail2):
            to_ret = []
            first_if = False
            for i in mail2:
                if i == "@" or first_if:
                    if not first_if:
                        first_if = True
                        continue

                    if i == ".":
                        break
                    to_ret.append(i)

            ret = ""
            for i in to_ret:
                ret += i

            return ret

        self.options = None
        if hide_window:
            self.options = Options()
            self.options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=self.options)
        self.mail = mail
        self.subdomain = get_subdomain(mail)
        self.password = password
        self.driver.implicitly_wait(impl_wait)


    def login(self):
        # login
        self.driver.get(f"https://{self.subdomain}.managebac.com/login")
        email_box = self.driver.find_element(By.ID, "session_login")
        email_box.send_keys(self.mail)
        password_box = self.driver.find_element(By.ID, "session_password")
        password_box.send_keys(self.password)
        submit_button = self.driver.find_element(By.NAME, "commit")

        login_button = ActionChains(driver=self.driver)
        login_button.click(on_element=submit_button)
        login_button.perform()

        # sometimes it'll fail so we wait a little bit
        sleep(1)

    def get_schedule(self):
        more_button = self.driver.find_elements(By.CLASS_NAME, "fc-more")

        # TODO need to test this
        if more_button:
            fc_more = ActionChains(driver=self.driver)
            fc_more.click(on_element=more_button)
            fc_more.perform()

        days = self.driver.find_elements(By.CLASS_NAME, "day")

        temp = []

        # put raw information in list
        for day in days:
            text = re.split("\n", day.text, flags=re.DOTALL)
            temp.append(text)

        all_days = temp
        temp = []

        # sort the raw information by date and remove empty dates
        for day in all_days:
            if len(day) == 1:
                continue
            temp.append(day)

        all_days = temp

        return all_days

    def get_classes(self):
        self.driver.get(f"https://{self.subdomain}.managebac.com/student/classes/my")
        sleep(0.2)
        source = self.driver.page_source

        print("[DEBUG] now using bs4")

        soup = bs4.BeautifulSoup(source, "html.parser")
        html_classes = soup.find("div", {"id": "classes"})
        h_classes = html_classes.find_all("div",
                                          {"class": "fusion-card-item fusion-card-item-collapse ib-class-component"})

        temp1 = []
        temp_t = []

        # get the name out of the html
        for i in h_classes:
            temp = i.text.split(sep="\n")
            for a in temp:
                if a != "":
                    if not len(a) in [1,2]:
                        # filter some strings out of a
                        if a not in ["Units","Tasks","Updates"]:
                            temp_t.append(a)


        # get the ID of the html
        for line in str(h_classes).splitlines():
            if " id=" in line:
                for i in line.split():
                    if "id=" in i:
                        for a in i.split(sep="\""):
                            if "ib" in a:
                                for b in a.split(sep="_"):
                                    if any([x in b for x in "1234567890"]): temp1.append(b)

        temp5 = []

        # print(len(temp_t))
        # print(len(temp1))

        for i in range(0, (len(temp1))):
            item = classe(class_id=int(temp1[i]), name=temp_t[i])
            temp5.append(item)

        return temp5

    def home(self):
        self.driver.get(f"https://{self.subdomain}.managebac.com/student")

    def get_grades(self):
        # first we must get the classes
        self.driver.get(f"https://{self.subdomain}.managebac.com/student/classes")
        sleep(0.2)
        classe = self.driver.find_element(By.ID, "classes")




    def quit(self):
        self.driver.quit()


