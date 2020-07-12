import time
import tkinter as tk
import warnings
from datetime import datetime
from random import randint

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

warnings.filterwarnings("ignore")


class LinkedinScraper:
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password
        self.emails = []
        self.pageLoadDelay = 15

        CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        CHROMEDRIVER_PATH = 'C:\src\chromedriver.exe'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # comment this line if you want to see the scraper working
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = CHROME_PATH

        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    def GetProfiles(self):
        try:
            PROFILE_CLASS_NAME = "search-result__image-wrapper"
            NEXT_CLASS_NAME = "artdeco-pagination__button--next"
            CONTACT_INFO_WAIT_CLASS_NAME = "artdeco-modal__content"
            EMAIL_CLASS_NAME = "ci-email"

            # Login
            self.driver.get("https://www.linkedin.com/login/")
            inputUsername = WebDriverWait(self.driver, self.pageLoadDelay).until(EC.presence_of_element_located((By.ID, "username")))

            inputUsername.send_keys(self.email)

            inputPassword = self.driver.find_element_by_id('password')
            inputPassword.send_keys(self.password)

            inputPassword.submit()
            WebDriverWait(self.driver, self.pageLoadDelay).until(EC.presence_of_element_located((By.TAG_NAME, 'head')))

            # Go to requested Search Page
            self.driver.get(self.url)

            profiles = []
            while True:
                WebDriverWait(self.driver, self.pageLoadDelay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                time.sleep(0.5)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                try:
                    btnNext = WebDriverWait(self.driver, self.pageLoadDelay).until(
                        EC.presence_of_element_located((By.CLASS_NAME, NEXT_CLASS_NAME)))
                except:
                    btnNext = False

                profileDivs = self.driver.find_elements_by_class_name(PROFILE_CLASS_NAME)
                for div in profileDivs:
                    profiles.append(div.find_element_by_tag_name("a").get_attribute("href"))

                if not btnNext:
                    break

                if "artdeco-button--disabled" in btnNext.get_attribute("class"):
                    break
                self.driver.execute_script("arguments[0].click();", btnNext)

            for profile in profiles:
                self.driver.get(profile + "detail/contact-info/")
                contactInfo = WebDriverWait(self.driver, self.pageLoadDelay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, CONTACT_INFO_WAIT_CLASS_NAME)))
                try:
                    emailDiv = contactInfo.find_element_by_class_name(EMAIL_CLASS_NAME)
                    self.emails.append(emailDiv.find_element_by_tag_name("a").text)
                except:
                    continue

        except TimeoutException:
            print("Page took too long to load. Aborting.")

        finally:
            if self.emails:
                df = pd.DataFrame({'Emails': self.emails})
                try:
                    fileName = 'emails_{datetime}.csv'.format(datetime=datetime.today().strftime("%d-%m-%Y--%H-%M-%S"))
                    df.to_csv(fileName, index=False, encoding='utf-8')
                    print('emails.csv file was still open so we saved it as ', fileName)
                except PermissionError:
                    fileName = 'emails{randomNumber}.csv'.format(randomNumber=randint(1, 100000))
                    df.to_csv(fileName, index=False, encoding='utf-8')
                    print('emails.csv file was still open so we saved it as ', fileName)
            self.driver.quit()
            print("Closed Driver")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Search URL Label
        lblEnterUrl = tk.Label(self, text="Search URL")
        lblEnterUrl.grid(row=0, column=0, pady=15)

        # Search URL text box
        self.url = tk.StringVar()
        self.tbUrl = tk.Entry(self, width=100, textvariable=self.url)
        self.tbUrl.grid(row=0, column=1, pady=15)

        # Email Label
        lblEnterEmail = tk.Label(self, text="Email")
        lblEnterEmail.grid(row=1, column=0, pady=15)

        # Email text box
        self.email = tk.StringVar()
        self.tbEmail = tk.Entry(self, width=100, textvariable=self.email)
        self.tbEmail.grid(row=1, column=1, pady=15)

        # Password Label
        lblEnterPassword = tk.Label(self, text="Password")
        lblEnterPassword.grid(row=2, column=0, pady=15)

        # Password text box
        self.password = tk.StringVar()
        self.tbPassword = tk.Entry(self, width=100, textvariable=self.password)
        self.tbPassword.grid(row=2, column=1, pady=15)

        # GetEmails button
        self.btnGetEmails = tk.Button(self)
        self.btnGetEmails["text"] = "Get Emails"
        self.btnGetEmails["command"] = self.getEmails
        self.btnGetEmails.grid(row=3, column=1, pady=15)

    def getEmails(self):
        self.btnGetEmails["state"] = "disabled"
        print("Fetching URLs")

        scraper = LinkedinScraper(self.url.get(), self.email.get(), self.password.get())
        scraper.GetProfiles()


root = tk.Tk()

# Window title and minsize
root.title("LinkedIn Email Scraper")
root.minsize(800, 200)

app = Application(master=root)
app.mainloop()
