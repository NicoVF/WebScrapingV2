import base64
import binascii
import re


class Image:

    def __init__(self, name, extension):
        self._name = name
        self._extension = extension
        self.if_is_webp_covert_to_jpg()

    @classmethod
    def is_encoded(cls, encoded_image):
        if encoded_image.find("base64,") != -1:
            return True, "Base64"
        return False, None

    @classmethod
    def switch_decode(cls, scrap, encode_type):
        if encode_type == "Base64":
            return Image.decoded_base64(scrap)

    @classmethod
    def decoded_base64(cls, scrap):
        base64_image = scrap.split("base64,")[1]
        try:
            decoded_image = base64.b64decode(base64_image)
            return decoded_image
        except binascii.Error:
            return False

    @classmethod
    def extension_of_decoded_image(cls, scrap, encode_type):
        return re.search("data:image/" + '(.+?)' + ";base64", scrap).group(1)

    def create_file(self, data_image):
        file = open(f"scrap/images/{self.name()}.{self.extension()}", "wb")
        file.write(data_image)
        file.close()

    def send_image_file_for_ftp(self, client_name_and_current_time, session, ftp_path):
        file = open(f"scrap/images/{self.name()}.{self.extension()}", 'rb')
        state = session.storbinary(f"STOR {ftp_path}/{client_name_and_current_time}/{self.name()}.{self.extension()}", file)
        file.close()
        if state.find("226-File successfully transferred") != -1:
            return True
        return state

    def name(self):
        return self._name

    def extension(self):
        return self._extension

    def if_is_webp_covert_to_jpg(self):
        if self.extension() == "webp":
            self._set_jpg_extension()
        return

    def _set_jpg_extension(self):
        self._extension = "jpg"


