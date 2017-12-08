# -*- coding: utf-8 -*-

#### IMPORTS 1.0

import os
import re
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup


#### FUNCTIONS 1.0

def validateFilename(filename):
    filenameregex = '^[a-zA-Z0-9]+_[a-zA-Z0-9]+_[a-zA-Z0-9]+_[0-9][0-9][0-9][0-9]_[0-9QY][0-9]$'
    dateregex = '[0-9][0-9][0-9][0-9]_[0-9QY][0-9]'
    validName = (re.search(filenameregex, filename) != None)
    found = re.search(dateregex, filename)
    if not found:
        return False
    date = found.group(0)
    now = datetime.now()
    year, month = date[:4], date[5:7]
    validYear = (2000 <= int(year) <= now.year)
    if 'Q' in date:
        validMonth = (month in ['Q0', 'Q1', 'Q2', 'Q3', 'Q4'])
    elif 'Y' in date:
        validMonth = (month in ['Y1'])
    else:
        try:
            validMonth = datetime.strptime(date, "%Y_%m") < now
        except:
            return False
    if all([validName, validYear, validMonth]):
        return True


def validateURL(url):
    try:
        r = urllib2.urlopen(url)
        count = 1
        while r.getcode() == 500 and count < 4:
            print ("Attempt {0} - Status code: {1}. Retrying.".format(count, r.status_code))
            count += 1
            r = urllib2.urlopen(url)
        sourceFilename = r.headers.get('Content-Disposition')

        if sourceFilename:
            ext = os.path.splitext(sourceFilename)[1].replace('"', '').replace(';', '').replace(' ', '')
        else:
            ext = os.path.splitext(url)[1]
        validURL = r.getcode() == 200
        validFiletype = ext.lower() in ['.csv', '.xls', '.xlsx']
        return validURL, validFiletype
    except:
        print ("Error validating URL.")
        return False, False

def validate(filename, file_url):
    validFilename = validateFilename(filename)
    validURL, validFiletype = validateURL(file_url)
    if not validFilename:
        print filename, "*Error: Invalid filename*"
        print file_url
        return False
    if not validURL:
        print filename, "*Error: Invalid URL*"
        print file_url
        return False
    if not validFiletype:
        print filename, "*Error: Invalid filetype*"
        print file_url
        return False
    return True


def convert_mth_strings ( mth_string ):
    month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
    for k, v in month_numbers.items():
        mth_string = mth_string.replace(k, v)
    return mth_string


#### VARIABLES 1.0

entity_id = "E2001_EROYC_gov"
url = "http://www2.eastriding.gov.uk/council/governance-and-spending/budgets-and-spending/council-spending-and-salaries/"
errors = 0
data = []
user_agent = {'User-agent': 'Mozilla/5.0'}
datadict = {'AjaxManager': 'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$updConsolePanel|esctl_20242569$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords',
'EasySitePostBack': '', 'LinkState': '', 'PostbackAction': '', 'PostbackData': '', 'ScrollPos': '1828', '__ASYNCPOST': 'true', '__EVENTARGUMENT': '1', '__EVENTTARGET': 'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords',
'__EVENTVALIDATION': '/wEdABXBqwlJ0fM40ik8AyoZALD6Rww5ZtSA5diJbW2I/HREwEKMkDkEXVh/BozJJLZWmIJmZ3BDZPIC19uZp/PiF+75LWoQ3bQPxQZmxra1evH7kXYaIXBD9DWgLluI6zSsSbY42rd/vkmf9UUXmZ3CDBLAOX/G12jEMC/Tcm94u8rO4JK/Uc+TPhpkpSdGZC0jDmPqvD3ns0PYdvnc0DERQYSHYgtLRDO3IDOy1wVC5Jg4lsJfTQctkyI2vXf2rEcdTQq5cNTWwVoADv7aS41FQxItheDqUygEONgMkzQK5UXx6+RHr/MnmGMHQFwE9UPu1qwztcwdOlJIAQa1bX6DjX0dei2in64I7lLLlRgAzDLYuDhApZ2cCVTQiQJ6hjXOSSL6JCRp7T6PQmjN1AnbpU5rfebm+qWxvFnjAVTolseOqc7NJ6TJvlCk+xQgmXL824/AYvd2kuuq1WI6UX4BmKThzVAn8jbBNRhy+E83o64NLw==',
'__LASTFOCUS': '', '__VIEWSTATE': '/wEPZmRqNjs2tNXqh4Lvt46Eq6Emah7D3i8KU0s9y71iHC6Jzw==', '__VIEWSTATEGENERATOR': '090FE928', '__VIEWSTATEZIP': '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',
'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$cKeywords$txtKeywords':'',
'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$consoleMessagePanel$hfState':'',
'esctl_20242569$ctlAssetManager$flwBrowseAssets$console$resultsPerPageControl$ddlRecords':'84',
}


#### READ HTML 1.2

import requests   # import requests for making post requests

html = requests.post(url, data= datadict, headers=user_agent)     # using requests for making post requests
soup = BeautifulSoup(html.text, 'lxml')

#### SCRAPE DATA

block = soup.find('div', 'clear grid-inner')
links = soup.findAll('a', href=True)
for link in links:
    csvfile = link.text.strip()
    if '500'  in csvfile:
        urls = link['href']
        code_url = urls[-8:-2]
        url = 'http://www2.eastriding.gov.uk/EasysiteWeb/getresource.axd?AssetID={}&type=full&servicetype=Attachment'.format(code_url)
        csvMth =csvfile.split(' ')[-2][:3]
        csvYr =csvfile.split(' ')[-1]
        if 'July2016' in csvYr:
            csvMth = '06'
            csvYr = '2016'
        csvMth = convert_mth_strings(csvMth.upper())
        data.append([csvYr, csvMth, url])

#### STORE DATA 1.0

for row in data:
    csvYr, csvMth, url = row
    filename = entity_id + "_" + csvYr + "_" + csvMth
    todays_date = str(datetime.now())
    file_url = url.strip()

    valid = validate(filename, file_url)

    if valid == True:
        scraperwiki.sqlite.save(unique_keys=['l'], data={"l": file_url, "f": filename, "d": todays_date })
        print filename
    else:
        errors += 1

if errors > 0:
    raise Exception("%d errors occurred during scrape." % errors)


#### EOF

