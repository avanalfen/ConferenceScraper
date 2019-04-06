from requests import get
from bs4 import BeautifulSoup
import os

yearsOfTalksToDownload = 20
currentYearDownloading = 1

year = 2006
month = 10

while currentYearDownloading < yearsOfTalksToDownload:

    URL_MONTH = str(month)

    if URL_MONTH == '4':
        URL_MONTH = '04'

    base = 'https://www.lds.org'
    url = 'https://www.lds.org/general-conference/' + str(year) + '/' + URL_MONTH + '?lang=eng'

    response = get(url)

    html_soup = BeautifulSoup(response.text, 'html.parser')

    talk_containers = html_soup.find_all('div', class_='lumen-tile lumen-tile--horizontal lumen-tile--list')

    totalTalks = len(talk_containers)
    print(url)

    while len(talk_containers) > 0:
        print('Downloading year: ' + str(currentYearDownloading) + '/' + str(yearsOfTalksToDownload) + ' talk: ' + str(totalTalks - (len(talk_containers)) + 1) + '/' + str(totalTalks))  # update progress

        first = talk_containers[0]
        titleDiv = first.find_all('div', class_='lumen-tile__title')[0].div

        if titleDiv is None:  # crash fix
            talk_containers.pop(0)
            continue

        title = titleDiv.text
        author = first.find_all('div', class_='lumen-tile__content')[0].text
        detailURL = base + first.a['href']
        imageURL = first.img['data-src']

        sleep(3)  # Don't shotgun blast the website
            
        detailResponse = get(detailURL)
        detailSoup = BeautifulSoup(detailResponse.text, 'html.parser')

        fullTalkDiv = detailSoup.find_all('div', class_ = 'body-block')

        if len(fullTalkDiv) == 0:  # crash fix
            talk_containers.pop(0)
            continue

        fullTalk = fullTalkDiv[0].text

        talksDir = 'talks/'
        authorDir = author + '/'
        directory = talksDir + authorDir

        if not os.path.exists(talksDir):  # create talk folder if not there
            os.mkdir(talksDir)

        if not os.path.exists(talksDir + authorDir):  # create author folder if it doesn't exist
            os.mkdir(talksDir + authorDir)

        with open(directory + title, 'w+') as the_file:  # write talk to file
            the_file.write(fullTalk)

        talk_containers.pop(0)

        sleep(3)  # Don't shotgun blast the website

    if str(month) == '04':
        month = 10
    else:
        year -= 1
        month = 4
        currentYearDownloading += 1

print('Done')
