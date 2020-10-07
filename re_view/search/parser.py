import requests
from bs4 import BeautifulSoup

class PlaystoreAppParser():
    
    def __init__(self,url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
    
    def get_icon(self):
        icon_soup = self.soup.find('div', class_="xSyT2c")
        return icon_soup.find("img")["src"]

    def get_title(self):
        title_soup = self.soup.find('h1', class_="AHFaub").find('span')
        return title_soup.text

    def get_publisher(self):
        publisher_soup = self.soup.find('a',class_="hrTbp R8zArc")
        return publisher_soup.text

    def get_description(self):
        description_soup = self.soup.find('div',attrs = {'jsname':'sngebd'})
        return description_soup.text

    def get_matrials(self):
        matrials_soup = self.soup.find('div', class_ = 'SgoUSc')
        video_urls = []
        for video in matrials_soup.find_all('div',class_='MSLVtf Q4vdJd'):
            video_urls.append(video.find('img')['src'])

        image_urls = []
        for image in matrials_soup.find_all('button',class_='Q4vdJd'):
            image_soup = image.find('img')
            try:
                image_urls.append(image_soup['data-src'])
            except KeyError:
                try:
                    image_urls.append(image_soup['srcset'])
                except KeyError:
                    image_urls.append(image_soup['src'])
            print(image_soup)
        return (video_urls,image_urls)
        