import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep


class mbapi:

    def __init__(self, mail: str, password: str, impl_wait=5.0):

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

        self.driver = webdriver.Firefox()
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

        classes = self.driver.find_element(By.XPATH, "//*[@id=\"action-show\"]")
        entries = classes.find_elements(By.TAG_NAME, "li")

        add_to_list = False
        to_ret = []
        sleep(1)

        for entry in entries:
            temp = re.split("\n", entry.text, flags=re.DOTALL)

            if add_to_list or temp == "Classes":
                if not add_to_list:
                    add_to_list = True
                    continue

            if temp == "Join More Classes...":
                break

            if len(temp) == 1:
                continue

            to_ret.append(temp)

        to_ret = to_ret[0]

        to_ret.pop(0)
        to_ret.pop(-1)

        return to_ret

    def quit(self):
        self.driver.quit()
