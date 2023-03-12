import os
import unittest

import warnings

from gspread import SpreadsheetNotFound

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

from scrap.Spreadsheet import Spreadsheet

name_spread_test = "Test_WebScraping"
name_sheet_test = "Hoja1"
column_number_of_images_test = 9
column_number_of_names_test = 1


class TestSpreadsheet(unittest.TestCase):

    def setUp(self):
        super(TestSpreadsheet, self).setUp()
        self.spreadsheet = Spreadsheet()

    def test01_has_secret_key(self):
        os.chdir("..")
        self.assertTrue(os.path.exists("static/secret_key.json"))

    def test02_open_correct_spreadsheet(self):
        spreadsheet_file = self.spreadsheet.get_spreadsheet(name_spread_test)
        self.assertTrue(str(spreadsheet_file).find(name_spread_test) != -1)

    def test03_try_open_incorrect_spreadsheet(self):
        with self.assertRaises(Exception):
            incorrect_spreadsheet_name = "xxx"
            self.spreadsheet.get_spreadsheet(incorrect_spreadsheet_name)

    def test04_open_correct_sheet(self):
        self.spreadsheet.get_spreadsheet(name_spread_test)
        sheet = self.spreadsheet.get_sheet(name_sheet_test)
        self.assertTrue(str(sheet).find(name_sheet_test) != -1)

    def test05_try_open_incorrect_spreadsheet(self):
        with self.assertRaises(Exception):
            incorrect_sheet_name = "xxx"
            self.spreadsheet.get_spreadsheet(name_spread_test)
            self.spreadsheet.get_sheet(incorrect_sheet_name)

    def test06_get_images(self):
        self.spreadsheet.get_spreadsheet(name_spread_test)
        sheet = self.spreadsheet.get_sheet(name_sheet_test)
        images_list, images_amount = self.spreadsheet.get_images(sheet, column_number_of_images_test)
        self.assertTrue(images_amount > 0)

    def test07_cant_get_images_empty_column(self):
        with self.assertRaises(Exception):
            self.spreadsheet.get_spreadsheet(name_spread_test)
            sheet = self.spreadsheet.get_sheet(name_sheet_test)
            self.spreadsheet.get_images(sheet, 11)

    def test08_get_name_of_images(self):
        self.spreadsheet.get_spreadsheet(name_spread_test)
        sheet = self.spreadsheet.get_sheet(name_sheet_test)
        images_list, images_amount = self.spreadsheet.get_images(sheet, column_number_of_images_test)
        names_list = self.spreadsheet.get_name_of_images(sheet, column_number_of_names_test, images_amount)
        self.assertTrue(len(names_list) > 0)

    def test09_get_name_of_images_different_amount_between_images_and_names(self):
        with self.assertRaises(Exception):
            self.spreadsheet.get_spreadsheet(name_spread_test)
            sheet = self.spreadsheet.get_sheet(name_sheet_test)
            images_list, images_amount = self.spreadsheet.get_images(sheet, column_number_of_images_test)
            images_amount -= 1
            names_list = self.spreadsheet.get_name_of_images(sheet, column_number_of_names_test, images_amount)

    




