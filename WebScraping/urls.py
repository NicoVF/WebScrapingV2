from django.urls import path
from .views import SetValues, Processed

app_name = "WebScraping"

urlpatterns = [
    path("setValues/", SetValues.as_view(), name="Setear valores"),
    path("processed/", Processed.as_view(), name="Procesado")
]
