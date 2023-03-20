import re
import validators
import requests
from requests import ConnectionError, ReadTimeout


class WebPageToScrap:

    def __init__(self, url=None, id_=None, tag=None, class_=None, attribute=None, xpath=None):
        self._url = url
        self._id = id_
        self._tag = tag
        self._class = class_
        self._attribute = attribute
        self._xpath = xpath

    def url(self):
        return self._url

    def tag(self):
        return self._tag

    def class_(self):
        return self._class

    def attribute(self):
        return self._attribute

    def check_url(self):
        validation_result = validators.url(self.url())
        if validation_result is not True:
            return "Url invalida"
        try:
            requests.get(self.url(), timeout=7)
            return True
        except ConnectionError:
            return "Error de conexion. Web posiblemente caida"
        except ReadTimeout:
            return "Error de conexion. Se tarda mas de 7 seg al cargar la web"


    def is_direct_image_url(self):
        last_characters_of_url = self._extract_last_5_characters()
        possible_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        if any([x in last_characters_of_url for x in possible_extensions]):
            return True
        return False

    def extension_of_url_image(self):
        last_characters_of_url = self._extract_last_5_characters()
        extension = re.search("(jpg|jpeg|png|webp)", last_characters_of_url)
        return extension[0]

    def _extract_last_5_characters(self):
        len_url = len(self.url())
        last_characters_of_url = self.url()[len_url - 5:]
        return last_characters_of_url
