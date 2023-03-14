import os
import unittest
import uuid

from scrap.Spreadsheet import Spreadsheet

name_spread_test = "Test_WebScraping"
name_sheet_test = "Hoja1"
column_number_of_images_test = 9
column_number_of_names_test = 1


class TestSpreadsheet(unittest.TestCase):

    def test01_has_secret_key(self):
        os.chdir("..")
        self.assertTrue(os.path.exists("static/secret_key.json"))

    def test02_open_correct_spreadsheet(self):
        spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
        self.assertTrue(str(spreadsheet).find(name_spread_test) != -1)

    def test03_try_open_incorrect_spreadsheet(self):
        with self.assertRaises(Exception):
            Spreadsheet.get_spreadsheet("xxx")

    def test04_open_correct_sheet(self):
        spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
        sheet = spreadsheet.get_sheet(name_sheet_test)
        self.assertTrue(str(sheet).find(name_sheet_test) != -1)

    def test05_try_open_incorrect_sheet(self):
        with self.assertRaises(Exception):
            incorrect_sheet_name = "xxx"
            spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
            spreadsheet.get_sheet(incorrect_sheet_name)

    def test06_get_images(self):
        spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
        sheet = spreadsheet.get_sheet(name_sheet_test)
        images_list, images_amount = spreadsheet.get_images(sheet, column_number_of_images_test)
        self.assertTrue(images_amount > 0)

    def test07_cant_get_images_empty_column(self):
        with self.assertRaises(Exception):
            spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
            sheet = spreadsheet.get_sheet(name_sheet_test)
            spreadsheet.get_images(sheet, 11)

    def test08test_cant_get_duplicated_names_of_images(self):
        with self.assertRaises(Exception):
            spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
            sheet = spreadsheet.get_sheet(name_sheet_test)
            images_list, images_amount = spreadsheet.get_images(sheet, column_number_of_images_test)
            sheet.update(f"{chr(64 + column_number_of_names_test)}2", "same_name")
            sheet.update(f"{chr(64 + column_number_of_names_test)}3", "same_name")
            spreadsheet.get_name_of_images(sheet, column_number_of_names_test, images_amount)

    def test09_get_name_of_images(self):
        spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
        sheet = spreadsheet.get_sheet(name_sheet_test)
        images_list, images_amount = spreadsheet.get_images(sheet, column_number_of_images_test)
        sheet.update(f"{chr(64 + column_number_of_names_test)}2", str(uuid.uuid4()))
        sheet.update(f"{chr(64 + column_number_of_names_test)}3", str(uuid.uuid4()))
        names_list = spreadsheet.get_name_of_images(sheet, column_number_of_names_test, images_amount)
        self.assertTrue(len(names_list) > 0)

    def test10_get_name_of_images_different_amount_between_images_and_names(self):
        with self.assertRaises(Exception):
            spreadsheet = Spreadsheet.get_spreadsheet(name_spread_test)
            sheet = spreadsheet.get_sheet(name_sheet_test)
            images_list, images_amount = spreadsheet.get_images(sheet, column_number_of_images_test)
            images_amount -= 1
            spreadsheet.get_name_of_images(sheet, column_number_of_names_test, images_amount)
