# coding:utf-8

from somed_rtc.driver import ChromeDriver
from somed_rtc.actions import Actions
from somed_rtc.actions import URLBuilder
from somed_rtc.utils import downloadFileFromUrl
from selenium.common.exceptions import TimeoutException

import re
import urllib3
import sys, traceback
from pathlib import Path

driver = ChromeDriver(driver_path = './chromedriver_win32_77/chromedriver.exe')

urlBuilder = URLBuilder()
#driver.goto(urlBuilder.getUrl('OlySandBox'))
#driver.goto('http://www.google.com')
try:
    driver.authenticate('username', 'password')

    if driver.gotoProjectPage('OlySandBox') is True:
        print('go to project page success')
    else:
        print('go to project page failed')

    driver.gotoProjectWorkItemPage('OlySandBox', '7843')
    #print(driver.uploadFileToWorkItem('OlySandBox', '7924', './avatar.png'))
    infos = driver.retrieveWorkItemAttachmentInfos('OlySandBox', '7924')
    print('found {} resources.'.format(len(infos)))
    for info in infos:
        print(info.fileName, info.uploader, info.attachmentId, info.size, flush=True)
        url = info.href
        #downloadFileFromUrl(driver, url,'dest')
    workItemList = driver.retrieveSavedQueryWorkItemList('IPF-3OTV_SW_Project', '自動同期用', shared = True)
    for workItem in workItemList:
        print(workItem.get('タイプ'))
        print(workItem.get('コメント'))

    driver.addWorkItemSubscriber('OlySandBox', 8050, '王 詩博')


except TimeoutException as e:
    print(e)
except Exception as e:
    traceback.print_exc()
    print(e)

driver.quit()
