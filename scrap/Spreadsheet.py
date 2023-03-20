import uuid

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

        duplicados = [name for name in names_list if names_list.count(name) > 1]
        if len(duplicados) > 0:
            duplicados = list(set(duplicados))
            raise Exception(f"En la columna {column} existen nombres / ids duplicados.\n"
                            f"Los valores duplicados son {duplicados}")

        if images_amount != len(names_list):
            raise Exception(f"La cantidad de imagenes ({images_amount}) no coincide con la cantidad de nombres "
                            f"({len(names_list)})")

        names_list = [str(uuid.uuid4()) if name == "" else name for name in names_list]

        return names_list

    def get_images(self, sheet, column):
        images_list = sheet.col_values(column)
        if len(images_list) == 0:
            raise Exception(f"En la columna {column} no se encuentran valores / imagenes")
        images_list.pop(0)
        return images_list, len(images_list)

    def write_value_in(self, sheet, sheet_name, column, row, value):
        state = str(sheet.update_cell(row, column, value))
        print(state)
        if state.find(f"'updatedRange': '{sheet_name}!{chr(64+column)}{row}'") != -1:
            return True
        return state

    def spreadsheet_file(self):
        return self._spreadsheet_file
