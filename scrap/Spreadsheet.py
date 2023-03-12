import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("static/secret_key.json", scopes=scopes)


class Spreadsheet:
    def __init__(self, name):
        self._name = name

    def get_first_sheet(self):
        file = gspread.authorize(creds)
        spreadsheet = file.open(self.name())
        sheet = spreadsheet.sheet1
        return sheet

    def get_name_of_images(self, sheet, column, images_amount):
        if column == 0:
            names_list = []
            for image in range(images_amount):
                names_list.append(image + 1)
            return names_list

        names_list = sheet.col_values(column)
        names_list.pop(0)
        return names_list

    def get_images(self, sheet, column):
        images_list = sheet.col_values(column)
        images_list.pop(0)
        return images_list, len(images_list)

    def write_values_in(self, sheet, column_number_to_insert, values_list):
        values_list.insert(0, "foto-agencia")
        columns_lists = [values_list]
        state = sheet.insert_cols(columns_lists, column_number_to_insert)
        return

    def name(self):
        return self._name
