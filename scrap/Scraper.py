import re
import requests
import validators
from bs4 import BeautifulSoup
from requests import ConnectionError


class Scraper:

    def get_content_in_lxml(self, url):
        result = requests.get(url)
        content = result.text
        return BeautifulSoup(content, 'lxml')

    def get_scrap(self, content, tag, class_, attribute=None, image_number=0):
        all_tags_with_class = content.find_all(tag, class_=class_)
        if len(all_tags_with_class) == 0:
            raise Exception(f"No se encontro ningun tag {tag} de clase {class_}")
        scrap = all_tags_with_class[image_number].get(attribute)
        if scrap is None:
            raise Exception(f"Se encontraron elementos con el tag {tag} y clase {class_},"
                   f" pero no el atributo {attribute} en la imagen {image_number + 1}")
        return scrap

    def check_access_to(self, url):
        try:
            requests.get(url)
            return True
        except ConnectionError:
            return "Error de conexion. Url de imagen obtenida posiblemente caida o invalida"
        except Exception:
            return False

    def is_direct_image(self, url):
        last_characters_of_url = self._extract_last_5_characters_of(url)
        possible_extensions = [".jpg", ".jpeg", ".png"]
        if any([x in last_characters_of_url for x in possible_extensions]):
            return True
        return False

    def extension_of_url_image(self, url):
        last_characters_of_url = self._extract_last_5_characters_of(url)
        extension = re.search("(jpg|jpeg|png)", last_characters_of_url)
        return extension[0]

    def _extract_last_5_characters_of(self, url):
        len_url = len(url)
        last_characters_of_url = url[len_url - 5:]
        return last_characters_of_url

