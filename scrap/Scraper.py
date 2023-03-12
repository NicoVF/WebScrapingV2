import requests
from bs4 import BeautifulSoup
from requests import ConnectTimeout


class Scraper:

    def get_content_in_lxml(self, url):
        try:
            result = requests.get(url)
        except ConnectTimeout:
            raise Exception(f"No se pudo acceder a {url}")
        content = result.text
        return BeautifulSoup(content, 'lxml')

    def get_scrap(self, content, tag, class_, attribute=None, image_number=0):
        all_tags_with_class = content.find_all(tag, class_=class_)
        if len(all_tags_with_class) == 0:
            raise Exception(f"No se encontro ningun tag {tag} de clase {class_}")
        scrap = all_tags_with_class[image_number].get(attribute)
        return scrap
