from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time


class Class:
    def __init__(self, subject_name: str, class_id: int, class_name: str):
        self.class_id = class_id
        self.subject_name = subject_name
        self.class_name = class_name


class Pymanagebac:

    def __init__(self, subdomain=""):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)

        self.check_login = False
        self.subdomain: str = subdomain

    def login(self, login: str, password: str):
        # get the domain
        domain = f"https://{self.subdomain}.managebac.com/login"
        self.driver.get(domain)

        # Perform the login using Selenium
        self.driver.find_element("name", "login").send_keys(login)
        self.driver.find_element("name", "password").send_keys(password)
        # press the "sign in" button
        self.driver.find_element("name", "commit").send_keys(Keys.RETURN)

        time.sleep(1)

        # set the login variable true
        self.check_login = True

    def get_classes(self):
        # get the domain
        domain = f"https://{self.subdomain}.managebac.com/student/classes/my"
        self.driver.get(domain)
        page_source = self.driver.page_source

        while True:
            classes = re.findall(pattern=r'<a\s+href="/student/classes/(\d+)">(.*?)\s*<span>(.*?)<\/span>\s*<\/a>',
                                 string=page_source)
            break

        print(classes)


class Exceptions:
    class SubdomainException(Exception):
        pass


mbapi = Pymanagebac(subdomain="maartens")
mbapi.login(login="112590@maartens.nl", password="12-09-2007")
mbapi.get_classes()
