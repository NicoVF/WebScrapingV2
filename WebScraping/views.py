from django.shortcuts import render
from django.views import generic

from scrap.Scraper import Scraper
from scrap.Spreadsheet import Spreadsheet
from scrap.WebPageToScrap import WebPageToScrap

# Create your views here.


class SetValues(generic.TemplateView):
    template_name = "setValues.html"

    def get(self, request, *args, **kwargs):
        # client_name = None
        # spreadsheet_name = None
        # sheet_name = None
        column_number_of_names = 1
        column_number_of_images = 9
        column_number_to_insert = 10
        tag = "img"
        class_ = "ImgSrc"
        attribute = "src"

        context = {
            # 'spreadsheet_name': spreadsheet_name,
            # 'sheet_name': sheet_name,
            'column_number_of_names': column_number_of_names,
            'column_number_of_images': column_number_of_images,
            'column_number_to_insert': column_number_to_insert,
            'tag': tag,
            'class_': class_,
            'attribute': attribute
        }
        return render(request, self.template_name, context)


class Processed(generic.TemplateView):
    template_name = "processed.html"

    def post(self, request, *args, **kwargs):
        client_name = request.POST["client_name"].lower()
        spreadsheet_name = request.POST["spreadsheet_name"]
        sheet_name = request.POST["sheet_name"]
        yes_upload = request.POST.get("yes_upload")
        column_number_of_names = int(request.POST["column_number_of_names"])
        column_number_of_images = int(request.POST["column_number_of_images"])
        column_number_to_insert = int(request.POST["column_number_to_insert"])
        tag = request.POST["tag"]
        class_ = request.POST["class_"]
        attribute = request.POST["attribute"]

        upload_images_to_own_host = False

        if yes_upload == "True":
            upload_images_to_own_host = True

        spreadsheet = Spreadsheet.get_spreadsheet("Test_WebScraping")
        sheet = spreadsheet.get_sheet("Hoja1")

        images_list, images_amount = spreadsheet.get_images(sheet, column_number_of_images)
        names_list = spreadsheet.get_name_of_images(sheet, column_number_of_names, images_amount)

        scraper = Scraper()

        # for images in images_list:
        lista_de_errores = []
        # GET IMAGES WITH GET SCRAPING


        #   web = WebPageToScrap(images, class_=class_, tag=tag, attribute=attribute)
        #   if web.check_url() is True:
        #       content = scraper.get_content_in_lxml(web.url())
        #       scrap = scraper.get_scrap(content, web.tag(), web.class_(), web.attribute())
        #   if web.check_url() is not True:
        #       lista de errores.append("No se puede acceder a la url")
        #

        web = WebPageToScrap("http://192.168.1.40:8080/t.html", class_="ImgSrc", tag="img", attribute="src")
        if web.check_url() is True:
            scrap = scraper.get_content_in_lxml(web.url())
            scraper.get_scrap(scrap, web.tag(), web.class_(), web.attribute())
        # if web.check_url() is not True:
        #


        context = {
            'client_name': client_name,
            'spreadsheet_name': spreadsheet_name,
            'sheet_name': sheet_name,
            'upload_images_to_own_host': upload_images_to_own_host,
            'column_number_of_names': column_number_of_names,
            'column_number_of_images': column_number_of_images,
            'column_number_to_insert': column_number_to_insert,
            'tag': tag,
            'class_': class_,
            'attribute': attribute
        }
        return render(request, self.template_name, context)
