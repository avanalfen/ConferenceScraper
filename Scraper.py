from requests import get
from bs4 import BeautifulSoup

year = "2013" # you can choose any year
month = "04" # months to choose are either '04' or '10'

base = 'https://www.lds.org'
url = 'https://www.lds.org/general-conference/' + year + '/' + month + '?lang=eng'

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')

talk_containers = html_soup.find_all('div', class_ = 'lumen-tile lumen-tile--horizontal lumen-tile--list')

while len(talk_containers) > 0:

    first = talk_containers[0]
    titleDiv = first.find_all('div', class_='lumen-tile__title')[0].div

    if titleDiv is None: // Crash fix
        talk_containers.pop(0)
        continue

    title = titleDiv.text
    author = first.find_all('div', class_='lumen-tile__content')[0].text
    detailURL = base + first.a['href']
    imageURL = first.img['data-src']

    sleep(2) # don't shotgun the website
    
    detailResponse = get(detailURL)
    detailSoup = BeautifulSoup(detailResponse.text, 'html.parser')
    fullTalk = detailSoup.find_all('div', class_ = 'body-block')[0].text

    filename = author + ' - ' + title + '.txt'

    with open(filename, 'a') as the_file:
        utf8 = fullTalk.encode("utf8")
        the_file.write(utf8)
    
    sleep(2) // # don't shotgun the website
    
    talk_containers.pop(0)

print('Done')
