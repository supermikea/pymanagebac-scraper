import re
import time
import threading

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.firefox.options import Options


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
        classes_button_elmnt = self.driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[7]")
        classes_button = ActionChains(driver=self.driver)
        classes_button.click(on_element=classes_button_elmnt)
        classes_button.perform()

        # TODO this is sometimes broken
        classes = self.driver.find_element(By.XPATH, "//*[@id=\"action-show\"]")
        entries = classes.find_elements(By.TAG_NAME, "li")

        to_ret = []
        sleep(1)

        # get the right information out of everything
        for entry in entries:
            temp = re.split("\n", entry.text, flags=re.DOTALL)
            if len(temp) == 1:
                continue
            to_ret.append(temp)

        to_ret = to_ret[0]

        to_ret.pop(0)
        to_ret.pop(-1)

        return to_ret

    def home(self):
        invoked = True
        count = 0

        # a Timeout function using threads
        while True:
            if invoked:
                print("[DEBUG] CREATING THREAD")
                t1 = threading.Thread(target=self.driver.get, args=(f"https://{self.subdomain}.managebac.com/student",))
                t1.start()
                t1.join(timeout=5.0)
                print("[DEBUG] THREAD JOINED")
                if t1.is_alive():
                    print(f"[DEBUG] THREAD STILL ALIVE: Count = {count}")
                    if count >= 3:
                        print("[DEBUG] count is 3 and the thread is still alive...\n[DEBUG] Deciding to just return and pray...")
                        return
                    count += 1
                else:
                    break

    def get_grades(self):

        to_ret_grades = []

        classes_button_elmnt = self.driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[7]")
        classes_button = ActionChains(driver=self.driver)
        classes_button.click(on_element=classes_button_elmnt)
        classes_button.perform()

        # TODO this may be broken
        classes = self.driver.find_element(By.XPATH, "//*[@id=\"action-show\"]")
        entries = classes.find_elements(By.TAG_NAME, "li")

        to_ret = []
        sleep(0.8)

        # get the right information out of everything
        for entry in entries:
            temp = re.split("\n", entry.text, flags=re.DOTALL)
            if len(temp) == 1:
                continue
            to_ret.append(temp)

        to_ret = to_ret[0]

        to_ret.pop(0)
        to_ret.pop(-1)

        final = []

        for entry in entries:
            for i in to_ret:
                if entry.text == i:
                    final.append(entry)

        # for i in final:
        #     print(i.text)

        classes_objs = final

        # print(classes_objs)

        index = 0

        for i in classes_objs:
            index += 1
            try:
                action = ActionChains(driver=self.driver)
                action.click(on_element=i)
                action.perform()
                # sleep(1)
            except Exception as e:
                if index == 1:
                    raise e
                self.home()
                sleep(0.2)
                action = ActionChains(driver=self.driver)
                action.click(on_element=self.driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[7]"))
                action.perform()

                classes = self.driver.find_element(By.XPATH, "//*[@id=\"action-show\"]")
                entries = classes.find_elements(By.TAG_NAME, "li")

                to_ret = []
                sleep(0.8)

                # get the right information out of everything
                for entry in entries:
                    # print(f"[DEBUG] RAW CLASSES ITEMS = {entry.text}")
                    temp = re.split("\n", entry.text, flags=re.DOTALL)
                    if len(temp) == 1:
                        continue
                    to_ret.append(temp)

                to_ret = to_ret[0]

                to_ret.pop(0)
                to_ret.pop(-1)

                final = []

                for entry in entries:
                    for i in to_ret:
                        # print(f"[DEBUG] ITEM IN to_ret = {i}")
                        if entry.text == i:
                            final.append(entry)

                # for i in final:
                #     print(i.text)

                classes_objs = final

                try:
                    i = classes_objs[index-1]
                except IndexError as e:
                    print(e)
                    print(f"[DEBUG] to_ret = {to_ret}")
                    self.quit()

                action = ActionChains(driver=self.driver)
                action.click(on_element=i)
                action.perform()

            tasks_unit = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div[2]/ul/li[1]/a")

            action = ActionChains(driver=self.driver)
            action.click(on_element=tasks_unit)
            action.perform()
            # sleep(1)

            try:
                all_tasks = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[3]/div[2]/div[2]/div/p[2]/a")
            except selenium.common.exceptions.NoSuchElementException:
                all_tasks = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[3]/div[2]/div[2]/div")
            action = ActionChains(driver=self.driver)
            action.click(on_element=all_tasks)
            action.perform()
            # sleep(1)

            terms = self.driver.find_element(By.CLASS_NAME, "selection")

            action = ActionChains(driver=self.driver)
            action.click(on_element=terms)
            action.perform()
            # sleep(1)

            for i in range(4):

                try:
                    tasks = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[3]/div[4]")
                    grades = tasks.find_elements(By.TAG_NAME, "div")
                    for grade in grades:
                        try:
                            if len(grade.text) > 3:
                                continue
                            to_ret_grades.append(grade.text)
                        except selenium.common.exceptions.StaleElementReferenceException:
                            pass

                except selenium.common.exceptions.NoSuchElementException:
                    pass


                terms1 = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[3]/div[2]/div/span")

                action = ActionChains(driver=self.driver)
                action.click(terms1)
                action.perform()

                terms = self.driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li/ul")
                terms = terms.find_elements(By.TAG_NAME, "li")

                action = ActionChains(driver=self.driver)
                action.click(terms[i])
                action.perform()
                sleep(0.2)

        # and finally we're done
        return to_ret_grades

    def quit(self):
        self.driver.quit()


