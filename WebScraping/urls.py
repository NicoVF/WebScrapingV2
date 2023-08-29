from django.urls import path
from .views import SetValues, Processed, SetValuesAcara

app_name = "WebScraping"

urlpatterns = [
    path("setValues/", SetValues.as_view(), name="Setear valores"),
    path("setValuesAcara/", SetValuesAcara.as_view(), name="Setear valores Acara"),
    path("processed/", Processed.as_view(), name="Procesado")
]
