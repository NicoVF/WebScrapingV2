import gspread
from gspread import SpreadsheetNotFound, WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("static/secret_key.json", scopes=scopes)


class Spreadsheet:
    def __init__(self, spreadsheet_file):
        self._spreadsheet_file = spreadsheet_file

    def __str__(self):
        return str(self.spreadsheet_file())

    @classmethod
    def get_spreadsheet(cls, spreadsheet_name):
        file = gspread.authorize(creds)
        try:
            spreadsheet = file.open(spreadsheet_name)
        except SpreadsheetNotFound:
            raise Exception(f"No se encontro ningun Spreadsheet con el nombre {spreadsheet_name}")
        return cls(spreadsheet)

    def get_sheet(self, sheet_name):
        try:
            sheet = self.spreadsheet_file().worksheet(sheet_name)
        except WorksheetNotFound:
            raise Exception(f"No se encontro ninguna hoja con el nombre {sheet_name}")
        return sheet

    def get_name_of_images(self, sheet, column, images_amount):
        if column == 0:
            names_list = []
            for image in range(images_amount):
                names_list.append(image + 1)
            return names_list

        names_list = sheet.col_values(column)
        if len(names_list) == 0:
            raise Exception(f"En la columna {column} no se encuentran valores / imagenes")
        names_list.pop(0)

        if images_amount != len(names_list):
            raise Exception(f"La cantidad de imagenes ({images_amount}) no coincide con la cantidad de nombres "
                            f"({len(names_list)})")
        return names_list

    def get_images(self, sheet, column):
        images_list = sheet.col_values(column)
        if len(images_list) == 0:
            raise Exception(f"En la columna {column} no se encuentran valores / imagenes")
        images_list.pop(0)
        return images_list, len(images_list)

    def write_values_in(self, sheet, column_number_to_insert, values_list):
        values_list.insert(0, "foto-agencia")
        columns_lists = [values_list]
        state = sheet.insert_cols(columns_lists, column_number_to_insert)
        return

    def spreadsheet_file(self):
        return self._spreadsheet_file
