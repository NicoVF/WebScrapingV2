import os
import unittest

import warnings

from gspread import SpreadsheetNotFound

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

from scrap.Spreadsheet import Spreadsheet

name_spread_test = "Test_WebScraping"
name_sheet_test = "Hoja1"


class TestSpreadsheet(unittest.TestCase):

    def test01_has_secret_key(self):
        os.chdir("..")
        self.assertTrue(os.path.exists("static/secret_key.json"))

    def test02_open_correct_spreadsheet(self):
        spreadsheet = Spreadsheet()
        spreadsheet_file = spreadsheet.get_spreadsheet(name_spread_test)
        self.assertTrue(str(spreadsheet_file).find(name_spread_test) != -1)

    def test03_try_open_incorrect_spreadsheet(self):
        with self.assertRaises(Exception):
            incorrect_spreadsheet_name = "xxx"
            spreadsheet = Spreadsheet()
            spreadsheet = spreadsheet.get_spreadsheet(incorrect_spreadsheet_name)

    def test04_open_correct_sheet(self):
        spreadsheet = Spreadsheet()
        spreadsheet_file = spreadsheet.get_spreadsheet(name_spread_test)
        sheet = spreadsheet.get_sheet(name_sheet_test)
        self.assertTrue(str(sheet).find(name_sheet_test) != -1)

    def test05_try_open_incorrect_spreadsheet(self):
        with self.assertRaises(Exception):
            incorrect_sheet_name = "xxx"
            spreadsheet = Spreadsheet()
            spreadsheet_file = spreadsheet.get_spreadsheet(name_spread_test)
            sheet = spreadsheet.get_sheet(incorrect_sheet_name)

