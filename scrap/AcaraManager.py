import time

from scrap.Result import Result
from scrap.Scraper import Scraper
from scrap.Spreadsheet import Spreadsheet
from scrap.WebPageToScrap import WebPageToScrap


class AcaraManager:
    def __init__(self, spreadsheet_name, sheet_name):
        self.link = "https://www.acara.org.ar/guia-oficial-de-precios.php?tipo=AUTOS"
        self.brands = None
        self.spreadsheet_name = spreadsheet_name
        self.sheet_name = sheet_name

    def scrap(self):
        scraper = Scraper()
        result = Result()
        web_state = WebPageToScrap(self.link).check_url()
        if web_state is not True:
            result.add_error(web_state)
            return result
        brands = self._get_brands(scraper, result)
        if not brands:
            return result
        units = self._create_dict(brands)
        self._append_models(units, brands, scraper, result)
        self._append_versions(units, brands, scraper, result)
        self._write_info(units)

        return result

    def _get_brands(self, scraper, result):
        tag_brands = "a"
        class_brands = "link-selector"
        content = scraper.get_content_in_lxml(self.link)
        scrap = scraper.get_scrap_list_of_texts(content, tag_brands, class_brands,
                                                after_number_element=4)
        self._check_get_scrap(scrap, result, "marcas", tag_brands, class_brands)
        return scrap

    def _get_models(self, brand, scraper, result):
        tag_models = "a"
        class_models = "opt-select"
        content = scraper.get_content_in_lxml(self.link + f"&marca={brand}")
        scrap = scraper.get_scrap_list_of_texts(content, tag_models, class_models,
                                                after_number_element=1, before_number_last_element=1)
        self._check_get_scrap(scrap, result, f"modelos de marca {brand}", tag_models, class_models)
        return scrap

    def _get_versions(self, brand, model, scraper, result):
        tag_versions = "a"
        class_versions = "opt-select"
        content = scraper.get_content_in_lxml(self.link + f"&marca={brand}" + f"&modelo={model}")
        scrap = scraper.get_scrap_list_of_texts(content, tag_versions, class_versions,
                                                after_element='TODAS LAS VERSIONES')
        self._check_get_scrap(scrap, result, f"versiones del modelo {model} de marca {brand}",
                              tag_versions, class_versions)
        return scrap

    def _check_get_scrap(self, scrap, result, items, tag, class_):
        if len(scrap) == 0:
            result.add_error(f"No se encontraron {items} con el tag {tag} y clase {class_}")

    def _create_dict(self, items):
        dic = {}
        for item in items:
            dic[item] = {}
        return dic

    def _append_models(self, units, brands, scraper, result):
        for brand in brands:
            models = self._get_models(brand, scraper, result)
            models_dict = self._create_dict(models)
            units[brand] = models_dict

    def _append_versions(self, units, brands, scraper, result):
        for brand in brands:
            models = list(units.get(brand).keys())
            for model in models:
                versions = self._get_versions(brand, model, scraper, result)
                units[brand][model] = versions

    def _write_info(self, units):
        spreadsheet = Spreadsheet.get_spreadsheet(self.spreadsheet_name)
        sheet = spreadsheet.get_sheet(self.sheet_name)
        self._insert_columns(sheet)
        index_acum = 2
        for brand in units.keys():
            for model in units.get(brand).keys():
                for index, version in enumerate(units.get(brand).get(model)):
                    spreadsheet.write_value_in(sheet, self.sheet_name, 3, index + index_acum, version)
                    spreadsheet.write_value_in(sheet, self.sheet_name, 2, index + index_acum, model)
                    spreadsheet.write_value_in(sheet, self.sheet_name, 1, index + index_acum, brand)
                    time.sleep(3)
                index_acum += len(units.get(brand).get(model))
                time.sleep(1)

    def _insert_columns(self, sheet):
        sheet.insert_cols([['Marca']], 1)
        sheet.insert_cols([['Modelo']], 2)
        sheet.insert_cols([['Version']], 3)
