from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import json
import getpass
import datetime

from datetime import datetime

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']


def googleCal():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # # Call the Calendar API

        # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming 10 events')
        # events_result = service.events().list(calendarId='primary', timeMin=now,
        #                                       maxResults=10, singleEvents=True,
        #                                       orderBy='startTime').execute()
        # events = events_result.get('items', [])

        # if not events:
        #     print('No upcoming events found.')
        #     return

        # # Prints the start and name of the next 10 events
        # for event in events:
        #     start = event['start'].get('dateTime', event['start'].get('date'))
        #     print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)
    return service


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

service = googleCal()

with open('json_data.json') as data_file:
    data = json.load(data_file)
    for v in data.values():
        # print(v['deadline'], v['title'], v['company'])

        eventDeadline = s = v['deadline']
        eventDeadline = eventDeadline.replace(',', '')
        datetime_object = datetime.strptime(
            eventDeadline + ' PST', '%b %d %Y %Z')
        eventDeadline = datetime_object.isoformat()
        print(eventDeadline)
        # print(v)

        yourIndexToReplace = 12  # e letter
        newLetter = '9'
        eventDeadlineEnd = "".join(
            (eventDeadline[:yourIndexToReplace], newLetter, eventDeadline[yourIndexToReplace+1:]))
        print(eventDeadlineEnd)
        event = {
            'summary': "Job Application Deadline reminder: " + v['title'] + " at " + v['company'],
            # 'location': '800 Howard St., San Francisco, CA 94103',
            'description': v['description'],
            'start': {
                'dateTime': eventDeadline,
                'timeZone': 'America/Vancouver',
            },
            'end': {
                'dateTime': eventDeadlineEnd,
                'timeZone': 'America/Vancouver',
            },
            # 'recurrence': [
            #     'RRULE:FREQ=DAILY;COUNT=2'
            # ],
            # 'attendees': [
            #     {'email': 'lpage@example.com'},
            #     {'email': 'sbrin@example.com'},
            # ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        print(event)
        try:
            print('Adding the event')
            # events_result = service.events().list(calendarId='primary', timeMin=now,
            #                                       maxResults=10, singleEvents=True,
            #                                       orderBy='startTime').execute()
            # events = events_result.get('items', [])

            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
            # exit(0)

            # if not events:
            #     print('No upcoming events found.')
            #     exit(0)

            # # Prints the start and name of the next 10 events
            # for event in events:
            #     start = event['start'].get('dateTime', event['start'].get('date'))
            #     print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)
            # exit(1)


now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2022-01-27T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2022-01-27T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    # 'recurrence': [
    #     'RRULE:FREQ=DAILY;COUNT=2'
    # ],
    # 'attendees': [
    #     {'email': 'lpage@example.com'},
    #     {'email': 'sbrin@example.com'},
    # ],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}


# try:
#     print('Getting the upcoming 10 events')
#     # events_result = service.events().list(calendarId='primary', timeMin=now,
#     #                                       maxResults=10, singleEvents=True,
#     #                                       orderBy='startTime').execute()
#     # events = events_result.get('items', [])

#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print('Event created: %s' % (event.get('htmlLink')))
#     exit(0)

#     # if not events:
#     #     print('No upcoming events found.')
#     #     exit(0)

#     # # Prints the start and name of the next 10 events
#     # for event in events:
#     #     start = event['start'].get('dateTime', event['start'].get('date'))
#     #     print(start, event['summary'])

# except HttpError as error:
#     print('An error occurred: %s' % error)
#     exit(1)


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
