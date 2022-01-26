from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import json

import getpass

# from __future__ import print_function

# import datetime
# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

import getpass

usernameStr = input('Enter StudentID:')
passwordStr = getpass.getpass("Entering password: ")


browser = webdriver.Chrome(
    executable_path='/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages/chromedriver/chromedriver')
browser.get(('https://langara-csm.symplicity.com/students'))

# <input class="input-text" autocapitalize="off" autocorrect="off" type="text" id="username" name="username" value="" alt="Username">
username = browser.find_element_by_id('username')
username.send_keys(usernameStr)

# <input class = "input-password" type = "password" autocomplete = "off" id = "password" name = "password" alt = "Password" >
password = browser.find_element_by_id('password')
password.send_keys(passwordStr)

# Waiting for captcha
signInButton = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'input-submit')))

signInButton.click()

# navigating to the co-op job listings
# <a href="/students/app/jobs/discover" target=""><i aria-hidden="true" class="icn-chevron_right"></i><span> Search </span></a>
# jobsButton = browser.find_element_by_partial_link_text(
#     '/students/app/jobs/discover')

browser.get(('https://langara-csm.symplicity.com/students/app/jobs/discover'))
# /html/body/ul/li[1]/a
positionType = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, 'simple-btn-keyboard-nav-1')))

positionType.click()

coop = browser.find_element_by_id('job_type-3')
coop.click()

apply = browser.find_element_by_id('job_type-apply')
apply.click()


all_jobs = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, 'job-element')))

# print(all_jobs)

all_jobs = browser.find_elements_by_tag_name('job-element')

jobContainer = browser.find_element_by_class_name('job-list-container')

links = jobContainer.find_elements_by_tag_name('a')
l = []
for link in links:
    l.append(link.get_attribute('href'))
l = list(filter(None, l))
# print(l)
allJobListings = {}
for a in l:
    browser.get(a)

    applyByContainer = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'edfab414adccd8b67f7727e3ae03b85b')))
    deadline = applyByContainer.find_element_by_css_selector(
        '#edfab414adccd8b67f7727e3ae03b85b > div:nth-child(2) > p:nth-child(2)').text
    # print(deadline)

    titleContainer = browser.find_element_by_class_name('header-title')
    title = titleContainer.find_element_by_tag_name('h1').text
    # print(title)

    companyContainer = browser.find_element_by_class_name('subtitle')
    company = companyContainer.find_element_by_tag_name('a').text
    # print(company)

    description = browser.find_element_by_class_name('job_description').text
    # print(description)

    # print(major)

    quali = ""
    try:
        quali = browser.find_element_by_class_name('job_qualifications').text
        # print(quali)
    except NoSuchElementException:
        pass

    major = browser.find_element_by_id(
        'd98a63de27abfe4096b287bb61ebb7af').text

    jobListing = {"title": title, "company": company, "deadline": deadline,
                  "description": description, "qualifications": quali}
    WebDriverWait(browser, 30)
    # print(jobListing)
    substring = "Computer Science"
    if (major.find(substring) > 1):
        allJobListings[a] = jobListing
    else:
        pass
    # print(allJobListings)


with open('json_data.json', 'w') as outfile:
    json.dump(allJobListings, outfile)

# WebDriverWait(browser, 30)


# links = [link.get_attribute('href')
#          for link in browser.find_elements_by_tag_name('a').getAttribute("href")]
# for link in links:
#

# print(all_jobs)

# for job in all_jobs:

#     jobTitle = job.find_element_by_tag_name('h3').text
#     print(jobTitle)

#     # class="list-data-columns list-data-columns-location ng-binding ng-scope

#     location = job.find_element_by_class_name(
#         "list-data-columns-employer").get_attribute("textContent")
#     print(location)

#     l2 = job.find_element_by_tag_name('span').get_attribute("innerHTML")
#     print(l2)

#     jobLink = job.find_element_by_tag_name('a')
#     jobLink.click()
#     Thread.sleep(3000)

#     browser.execute_script("window.history.go(-1)")

# for i in range(0, 20):
#     allJobs = WebDriverWait(browser, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, 'job-element')))
#     link = allJobs[i].find_element_by_tag_name('a')
#     link.click()

# getTagName() to get tag of sub-elements
