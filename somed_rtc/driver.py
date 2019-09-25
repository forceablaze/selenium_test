# coding:utf-8

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from somed_rtc.actions import URLBuilder
from somed_rtc.actions import Tabs
import time, re

import win32gui
import win32con
from pathlib import Path

urlBuilder = URLBuilder()
AUTH_URL = 'https://www.somed002.sony.co.jp/ccm/auth/authrequired'

class AttachmentInfo:
    def __init__(self, attachmentId, fileName, uploader, size, href):
        self.attachmentId = attachmentId
        self.fileName = fileName
        self.uploader = uploader
        self.size = size
        self.href = href

class Driver():

    def __init__(self, driver):
        self.driver = driver

    def goto(self, url, timeout = 30, ec = EC.presence_of_all_elements_located):
        wait = WebDriverWait(self.driver, timeout)
        self.driver.get(url)
        return wait.until(ec)

    def authenticate(self, username, password, timeout = 30):
        wait = WebDriverWait(self.driver, timeout)
        self.driver.get(AUTH_URL)

        loginButton = wait.until(
            #EC.presence_of_all_elements_located
            #EC.presence_of_element_located((By.LINK_TEXT, 'ログイン'))
            EC.presence_of_element_located((By.XPATH, '//button[text()="ログイン"]'))
        )

        usernameInput = self.driver.find_element_by_name("j_username")
        passwordInput = self.driver.find_element_by_name("j_password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(password)
        loginButton.click()


    def gotoProjectPage(self, projectName):
        element = self.goto(urlBuilder.getUrl(projectName),
                    ec = EC.presence_of_element_located(
                        (By.XPATH, '//span[text()="{}"]'.format(projectName)))
                )
        if element.text == projectName:
            return True
        return False

    def gotoProjectWorkItemPage(self, projectName, workItemId):
        element = self.goto(urlBuilder.getProjectWorkItemUrl(projectName, workItemId),
                    ec = EC.presence_of_element_located(
                        (By.XPATH, '//div[@aria-label="要約"]'))
                )
        return element.text


    def uploadFileToWorkItem(self, projectName, workItemId, filePath):
        element = self.goto(
                    urlBuilder.getProjectWorkItemUrl(
                        projectName, workItemId, Tabs['WORKITEM_TAB_LINKS']),

                    # wait for the upload widget ready
                    ec = EC.element_to_be_clickable(
                        (By.XPATH, '//div[@class="com-ibm-team-foundation-web-ui-views-attachments-AttachmentWidget AddAction"]'))
                )
        element.click()
        time.sleep(3)

        # selenium can not support non-input type file dialog
        dialog = win32gui.FindWindow('#32770', '開く')
        comboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)
        comboBox = win32gui.FindWindowEx(comboBoxEx32, 0, "ComboBox", None)
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)

        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None,
                str(Path(filePath).resolve()))
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)

        # sleep for the upload request
        time.sleep(3)

        # get the save button then click
        saveButton = self.driver.find_element_by_xpath('//button[text()="保存"]')
        saveButton.click()

    # return elements with <a> tag
    def retrieveWorkItemAttachmentInfos(self, projectName, workItemId):
        infos = []

        resourceLinkPattern = '//span[text()="添付"]'

        self.goto(
                urlBuilder.getProjectWorkItemUrl(
                    projectName, workItemId, Tabs['WORKITEM_TAB_LINKS']),

                # wait for the resource link ready
                ec = EC.presence_of_element_located(
                    (By.XPATH, resourceLinkPattern))
            )

        attachmentLabel = '//div[@class="AttachmentDetails"]/label[@class="AttachmentLabel"]'
        elements = self.driver.find_elements_by_xpath(attachmentLabel)

        for e in elements:
            meta = re.findall(r"(\d+): (.+)", e.text)[0]
            attachmentId = meta[0]
            fileName = meta[1]

            siblings = e.find_elements_by_xpath("following-sibling::*")
            meta = re.findall(r"(.+) - (.+)", siblings[0].text)[0]
            user = meta[0]
            size = meta[1]

            attachmentCommands = siblings[1]

            # get the download button
            downloadCommand = attachmentCommands.find_element_by_xpath('.//a[@class="AttachmentCommand DownloadCommand icon-download"]')
            href = downloadCommand.get_attribute('href')

            info = AttachmentInfo(attachmentId, fileName, user, size, href)
            infos.append(info)

        return infos

    def getCookieString(self):
        cookies = self.driver.get_cookies()
        cookieString = ''

        for item in cookies:
            cookieString += '{}={}; '.format(item['name'], item['value'])
        return cookieString


    def quit(self):
        self.driver.quit()

class ChromeDriver(Driver):

    def __init__(self, driver_path = None):

        if driver_path is not None:
            driver = webdriver.Chrome(executable_path = driver_path)
        else:
            driver = webdriver.Chrome()

        super().__init__(driver)

class FirefoxDriver(Driver):

    def __init__(self):
        driver = webdriver.Firefox()
        super().__init__(driver)
