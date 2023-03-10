from django.shortcuts import render
from django.views import generic


# Create your views here.

class SetValues(generic.TemplateView):
    template_name = "setValues.html"

    def get(self, request, *args, **kwargs):
        # spreadsheet_name = None
        image_extension = "jpg"
        column_number_of_names = 1
        column_number_of_images = 9
        column_number_to_insert = 10
        tag = "img"
        class_ = "ImgSrc"
        attribute = "src"

        context = {
            # 'spreadsheet_name': spreadsheet_name,
            'image_extension': image_extension,
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
        spreadsheet_name = request.POST["spreadsheet_name"]
        image_extension = request.POST["image_extension"]
        column_number_of_names = int(request.POST["column_number_of_names"])
        column_number_of_images = int(request.POST["column_number_of_images"])
        column_number_to_insert = int(request.POST["column_number_to_insert"])
        tag = request.POST["tag"]
        class_ = request.POST["class_"]
        attribute = request.POST["attribute"]

        context = {
            'spreadsheet_name': spreadsheet_name,
            'image_extension': image_extension,
            'column_number_of_names': column_number_of_names,
            'column_number_of_images': column_number_of_images,
            'column_number_to_insert': column_number_to_insert,
            'tag': tag,
            'class_': class_,
            'attribute': attribute
        }
        return render(request, self.template_name, context)
