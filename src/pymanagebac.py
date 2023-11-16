from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time


class Class:
    def __init__(self, subject_name: str, class_id: int, class_name: str):
        self.class_id = class_id
        self.subject_name = subject_name
        self.class_name = class_name


class Task:
    def __init__(self, task_name: str, task_description: str, subject: Class, task_id: int):
        self.subject = subject
        self.Task_id = task_id
        self.task_description = task_description
        self.task_name = task_name


class Grade:
    def __init__(self, subject: Class, task: Task, max_grade: int, grade: int, criteria: []):
        self.criteria = criteria
        self.subject = subject
        self.task = task
        self.max_grade = max_grade
        self.grade = grade


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

        counter = 1
        classes = []

        while True:
            # update the page source at every iteration
            page_source = self.driver.page_source
            counter += 1
            # use regex to find classes
            classes_found = re.findall(
                pattern=r'<a\s+href="/student/classes/(\d+)">(.*?)\s*<span>(.*?)<\/span>\s*<\/a>',
                string=page_source)

            # no new classes found thus we break
            if classes_found == 0:
                break

            """at the Managebac classes page, there can only be 10 displayed at a time. If the length of the classes 
            variable is 10, we can assume that there are more classes on the second page. This is all done locally 
            and is more efficient due to that."""
            classes += classes_found
            if len(classes) % 10 == 0:
                self.driver.get(domain + f'?page={counter}')
                time.sleep(0.5)  # just to be safe
                continue
            # len(classes) % 10 != 0 thus no more new classes
            break

        classes_list: [Class] = []
        for i in classes:
            # unpackage values from tuple
            (class_id, subject_name, class_name) = i

            # put it in a class which is easily accessible
            classes_list += [Class(class_id=class_id, subject_name=subject_name, class_name=class_name)]

        # done and return
        return classes_list

    def get_grade(self, subject: Class = None, task: Task = None):
        if not subject or task:
            raise Exception  # TODO exceptions

        if subject:
            self.driver.get(f"https://{self.subdomain}.managebac.com/student/classes/{subject.class_id}/core_tasks")
            time.sleep(0.5)
            page_source = self.driver.page_source

            # find the progress check id
            progress_check_id = re.match(pattern=r'<option[^>]*value="(\d+)"[^>]*>Progress Check<\/option>',
                                         string=page_source)

            print(progress_check_id)


class Exceptions:
    class SubdomainException(Exception):
        pass


mbapi = Pymanagebac(subdomain="maartens")
mbapi.login(login="112590@maartens.nl", password="12-09-2007")
classes = mbapi.get_classes()
mbapi.get_grade(subject=classes[5])
