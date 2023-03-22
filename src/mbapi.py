import re
import requests as req
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.options import Options
import logging
from logging import log
import bs4


class classe:
    def __init__(self, class_id: int, name: str, grade: list):
        """
        :type class_id: int
        :type name: str
        :type grade: list
        """

        self.class_id = class_id
        self.name = name
        self.grades = grade


class a_grade:
    def __init__(self, number: str, max_number: str, name: str):
        """
        :type number: str
        :type name: str
        """
        self.grade = number
        self.max_grade = max_number
        self.name = name


class a_task:
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

    def __init__(self, mail: str, password: str, impl_wait=5., hide_window=True, subdomain="" ,logging_level=None):

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
        if subdomain:
            self.subdomain = subdomain
        else:
            self.subdomain = get_subdomain(mail)
        self.password = password
        self.driver.implicitly_wait(impl_wait)
        self.session_cookie = None

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

        # use session cookies for increased speed
        cookie = self.driver.get_cookie(name="_managebac_session")
        cookie = {"_managebac_session": cookie.get("value"), "hide_osc_announcement_modal": "true"}
        result = req.get(f"https://{self.subdomain}.managebac.com/student/", cookies=cookie)

        if str(result) == "<Response [200]>":
            self.session_cookie = cookie
        else:
            print("[DEBUG] couldn't get session cookie for some reason... [CONTINUING]")

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

    def get_classes(self, target=1):
        # TODO half broken
        self.driver.get(f"https://{self.subdomain}.managebac.com/student/classes/my?page={target}")
        sleep(0.2)
        source = self.driver.page_source

        if "No classes found" in source:
            return []

        # print("[DEBUG] now using bs4")

        soup = bs4.BeautifulSoup(source, "html.parser")
        html_classes = soup.find("div", {"id": "classes"})
        h_classes = html_classes.find_all("div",
                                          {"class": "fusion-card-item fusion-card-item-collapse ib-class-component"})

        # print("[DEBUG] now using own implementation")

        temp1 = []
        temp_t = []

        # get the name out of the html
        for i in h_classes:
            temp = i.text.split(sep="\n")
            for a in temp:
                if a != "":
                    if not len(a) in [1, 2]:
                        # filter some strings out of a
                        if a not in ["Units", "Tasks", "Updates", "Unit", "Task", "Update"]:
                            temp_t.append(a)

        # get the ID of the html
        for line in str(h_classes).splitlines():
            if " id=" in line:
                for i in line.split():
                    if "id=" in i:
                        for a in i.split(sep="\""):
                            if "ib" in a:
                                for b in a.split(sep="_"):
                                    if any([x in b for x in "1234567890"]):
                                        temp1.append(b)

        temp5 = []
        count = target + 1
        # print(len(temp_t))
        # print(len(temp1))

        for i in range(0, (len(temp1))):
            item = classe(class_id=int(temp1[i]), name=temp_t[i], grade=[])
            temp5.append(item)

        # check if there is a second page (or more)
        self.driver.get(f"https://{self.subdomain}.managebac.com/student/classes/my?page={count}")
        sleep(0.2)
        source = self.driver.page_source
        if "No classes found" not in source:
            temp = self.get_classes(target=count)
            for i in temp:
                temp5.append(i)

        return temp5

    def get_grades(self, target: classe, term: int = 0):

        self.driver.get(f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks")
        sleep(0.1)
        if term:
            url = self.driver.current_url
            url_id = int(url.split(sep="=")[-1])
            current_month = datetime.now().month
            if term == 1:
                if 1 <= current_month <= 4:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id-1}")
                    sleep(0.1)
                elif current_month >= 9:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id}")
                    sleep(0.1)
                else:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id-2}")
                    sleep(0.1)
            elif term == 2:
                if 1 <= current_month <= 4:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id - 0}")
                    sleep(0.1)
                elif current_month >= 9:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id + 1}")
                    sleep(0.1)
                else:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id - 1}")
                    sleep(0.1)
            elif term == 3:
                if 1 <= current_month <= 4:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id + 1}")
                    sleep(0.1)
                elif current_month >= 9:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id + 2}")
                    sleep(0.1)
                else:
                    self.driver.get(
                        f"https://{self.subdomain}.managebac.com/student/classes/{target.class_id}/core_tasks?term={url_id - 0}")
                    sleep(0.1)
            else:
                raise TypeError("the argument term must be 1, 2, 3 or 4")
        source = self.driver.page_source

        # print("[DEBUG] now using own implementation")

        temp_names = []
        temp_grades = []
        temp_max_grades = []

        criterion = False

        source = source.splitlines()
        for item in source:
            # get the name out of the task
            if f"href=\"/student/classes/{target.class_id}/core_tasks" in item:
                if "<div class=\"indicator program-label m" in item:
                    continue
                parts = item.split(sep=">")
                parts.pop(0)
                parts.pop(-1)
                temp_names.append(parts[0][:-3])

            # get the grade out of the task
            if "<div class=\"label label-score\">" in item:
                parts = item.split(sep=">")
                parts.pop(0)
                parts.pop(-1)
                temp_grades.append(parts[0][:-5])

            # get the max_grade out of the task
            if "<div class=\"label label-points\">" in item:
                parts = item.split(sep=">")
                parts.pop(0)
                parts.pop(-1)
                temp_max_grades.append(parts[0][:-5])

            # if the grade is N/A
            if "<div class=\"label label-not-applicable\">" in item:
                parts = item.split(sep=">")
                parts.pop(0)
                parts.pop(-1)
                temp = (parts[0][:-5])

                temp_max_grades.append(temp)
                temp_grades.append(temp)

            # TODO if this happens, add a dictionary for easier access
            # check if grade has criterion (basically always)
            if "<div class=\"cell criterion-grade\">" in item or criterion:
                if not criterion:
                    criterion = True
                    continue
                criterion = False
                part = item[:-1]
                # print(temp_grades)

                temp_grades.append(part)
                temp_max_grades.append(part)

        # print("[DEBUG] done getting all the grades using my own implementation!")
        # print("[DEBUG] now fixing potential errors...")

        # print(temp_grades)
        # print(temp_max_grades)

        new_grades = []
        new_max_grades = []
        count = 0
        value = "number"

        # print(temp_max_grades)

        # fix the list
        for item in temp_grades:
            if item in "ABCD":
                key = item
                value = temp_grades[count + 1]
                to_insert = {key: value}
                try:
                    # print(new_grades)
                    if isinstance(new_grades[-1], dict):

                        new_grades[-1].update(to_insert)

                    else:
                        new_grades.append(to_insert)
                except IndexError:  # assume that the first entry is a criterion
                    new_grades.append(to_insert)

                count += 1
                continue

            if item == value:
                count += 1
                continue

            new_grades.append(item)
            count += 1

        count = 0
        # OPTIMIZATION NEEDED
        for item in temp_max_grades:
            if item in "ABCD":
                key = item
                value = temp_max_grades[count + 1]
                to_insert = {key: value}
                try:
                    if isinstance(new_max_grades[-1], dict):
                        new_max_grades[-1].update(to_insert)
                    else:
                        new_max_grades.append(to_insert)
                except IndexError:
                    new_max_grades.append(to_insert)

                count += 1
                continue

            if item == value:
                count += 1
                continue

            new_max_grades.append(item)
            count += 1

        temp_grade_obj = []

        # count = 0

        # print(len(temp_grades))
        # print(len(temp_max_grades))
        # print(len(temp_names))

        # print("\n\n\n\n\n\n")

        # print(new_grades)
        # print(new_max_grades)
        # print(temp_names)

        # print("[DEBUG] Fixed potential errors!")

        for i in range(0, len(new_grades)):
            # print(i)
            grade_item = a_grade(number=new_grades[i], max_number=new_max_grades[i], name=temp_names[i])
            temp_grade_obj.append(grade_item)
        item = classe(class_id=target.class_id, name=target.name, grade=temp_grade_obj)

        # print("[DEBUG] Ready to return!")

        return item

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    print("this is something you should import, not run directly")
