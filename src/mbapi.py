import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


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
        pass
