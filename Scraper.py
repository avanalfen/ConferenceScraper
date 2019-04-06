from requests import get
from bs4 import BeautifulSoup

year = "2013"
month = "04"

base = 'https://www.lds.org'
url = 'https://www.lds.org/general-conference/' + year + '/' + month + '?lang=eng'

response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')

talk_containers = html_soup.find_all('div', class_ = 'lumen-tile lumen-tile--horizontal lumen-tile--list')

while len(talk_containers) > 0:

    first = talk_containers[0]
    titleDiv = first.find_all('div', class_='lumen-tile__title')[0].div

    if titleDiv is None:
        talk_containers.pop(0)
        continue

    title = titleDiv.text
    author = first.find_all('div', class_='lumen-tile__content')[0].text
    detailURL = base + first.a['href']
    imageURL = first.img['data-src']

    # print(type(talk_containers))

    #print(len(talk_containers))
    print('Author: ' + author)
    print('Title: ' + title)
    print('Full Talk: ' + detailURL)
    print('Image: ' + imageURL)

    print(' ')

    detailResponse = get(detailURL)
    detailSoup = BeautifulSoup(detailResponse.text, 'html.parser')
    fullTalk = detailSoup.find_all('div', class_ = 'body-block')[0].text

    #print(fullTalk)

    filename = author + ' - ' + title + '.txt'

    with open(filename, 'a') as the_file:
        utf8 = fullTalk.encode("utf8")
        the_file.write(utf8)

    #print(' ')

    talk_containers.pop(0)

print('Done')