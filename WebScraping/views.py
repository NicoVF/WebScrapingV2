import ftplib
import os
import datetime
from django.shortcuts import render
from django.views import generic

import requests

from scrap.Image import Image
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
        client_name = request.POST["client_name"].lower().replace(" ", "-")
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

        current_time = datetime.datetime.now()
        date_and_time = f"--{current_time.year}-{current_time.month}-{current_time.day}--{current_time.hour}-{current_time.minute}-{current_time.second}"
        client_name_and_current_time = client_name + date_and_time

        ftp_host = os.environ['FTP_HOST']
        ftp_user = os.environ['FTP_USER']
        ftp_pass = os.environ['FTP_PASS']
        ftp_path = os.environ['FTP_PATH']

        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)
        session.encoding = "utf-8"
        session.cwd(ftp_path)
        session.mkd(client_name_and_current_time)

        spreadsheet = Spreadsheet.get_spreadsheet(spreadsheet_name)
        sheet = spreadsheet.get_sheet(sheet_name)

        images_list, images_amount = spreadsheet.get_images(sheet, column_number_of_images)
        names_list = spreadsheet.get_name_of_images(sheet, column_number_of_names, images_amount)

        scraper = Scraper()
        global image

        header_of_images = [['foto-agencia']]
        header_of_errors = [['ERRORES']]
        sheet.insert_cols(header_of_images, column_number_to_insert)
        sheet.insert_cols(header_of_errors, column_number_to_insert + 1)

        for img, name in zip(images_list, names_list):
            errors_list = []
            image = None
            new_url_of_image = os.environ['HOST_PUBLIC_URL']

            web = WebPageToScrap(img, class_=class_, tag=tag, attribute=attribute)
            result_check_url = web.check_url()
            is_url_finished_in_image_extension = web.is_direct_image_url()
            if result_check_url is not True:
                errors_list.append(result_check_url)
                if len(errors_list) > 0:
                    error = ' | '.join(errors_list)
                    spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert + 1, images_list.index(img) + 2,
                                               error)
                continue

            if result_check_url is True and is_url_finished_in_image_extension is True:
                if upload_images_to_own_host is False:
                    state = spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert,
                                                       images_list.index(img) + 2, web.url())
                    if state is not True:
                        errors_list.append(state)

                if upload_images_to_own_host is True:
                    extension = web.extension_of_url_image()
                    data_image = requests.get(web.url()).content
                    image = Image(name, extension)
                    image.create_file(data_image)
                    state = image.send_image_file_for_ftp(client_name_and_current_time, session, ftp_path)
                    if state is not True:
                        errors_list.append(state)
                    new_url_of_image += client_name_and_current_time + "/" + image.name() \
                                        + "." + image.extension()
                    state = spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert,
                                                       images_list.index(img) + 2, new_url_of_image)
                    if state is not True:
                        errors_list.append(state)

            if result_check_url is True and is_url_finished_in_image_extension is False:
                content = scraper.get_content_in_lxml(web.url())
                scrap, error = scraper.get_scrap(content, web.tag(), web.class_(), web.attribute())
                if error is not None:
                    errors_list.append(error)
                    if len(errors_list) > 0:
                        error = ' | '.join(errors_list)
                        spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert + 1,
                                                   images_list.index(img) + 2, error)
                    continue
                result_check_access_to_scrap = scraper.check_access_to(scrap)
                result_is_encoded_image = Image.is_encoded(scrap)
                is_scraped_url_finished_in_image_extension = scraper.is_direct_image(scrap)
                if result_check_access_to_scrap is not True:
                    if result_is_encoded_image[0] is False:
                        errors_list.append("No se puede identificar el tipo de encode de la imagen")
                        if len(errors_list) > 0:
                            error = ' | '.join(errors_list)
                            spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert + 1,
                                                       images_list.index(img) + 2, error)
                        continue
                    if result_is_encoded_image[0] is True:
                        decoded_image = Image.switch_decode(scrap, result_is_encoded_image[1])
                        if decoded_image is False:
                            errors_list.append(f"Error al decodificar la imagen en {result_is_encoded_image[1]}")
                            if len(errors_list) > 0:
                                error = ' | '.join(errors_list)
                                spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert + 1,
                                                           images_list.index(img) + 2, error)
                            continue
                        if decoded_image is not False:
                            extension = Image.extension_of_decoded_image(scrap, result_is_encoded_image[1])
                            image = Image(name, extension)
                            image.create_file(decoded_image)
                            state = image.send_image_file_for_ftp(client_name_and_current_time, session, ftp_path)
                            if state is not True:
                                errors_list.append(state)
                            new_url_of_image += client_name_and_current_time + "/" + image.name() \
                                + "." + image.extension()
                            state = spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert,
                                                               images_list.index(img) + 2, new_url_of_image)
                            if state is not True:
                                errors_list.append(state)

                if result_check_access_to_scrap is True and is_scraped_url_finished_in_image_extension is True:
                    if upload_images_to_own_host is False:
                        state = spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert,
                                                           images_list.index(img) + 2, scrap)
                        if state is not True:
                            errors_list.append(state)

                    if upload_images_to_own_host is True:
                        extension = scraper.extension_of_url_image(scrap)
                        data_image = requests.get(scrap).content
                        image = Image(name, extension)
                        image.create_file(data_image)
                        state = image.send_image_file_for_ftp(client_name_and_current_time, session, ftp_path)
                        if state is not True:
                            errors_list.append(state)
                        new_url_of_image += client_name_and_current_time + "/" + image.name() \
                                            + "." + image.extension()
                        state = spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert,
                                                           images_list.index(img) + 2, new_url_of_image)
                        if state is not True:
                            errors_list.append(state)

            if len(errors_list) > 0:
                error = ' | '.join(errors_list)
                spreadsheet.write_value_in(sheet, sheet_name, column_number_to_insert + 1, images_list.index(img) + 2, error)

        try:
            session.quit()
        except ftplib.error_temp:
            pass

        file_list = os.listdir("scrap/images")
        if len(file_list) > 0:
            for file in file_list:
                os.remove(f"scrap/images/{file}")


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