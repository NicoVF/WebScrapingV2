

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
