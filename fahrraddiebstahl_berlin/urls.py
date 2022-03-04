from django.contrib import admin
from django.urls import include, path

from main.views import (
    DelictByDateTime,
    DmgByDateTime,
    FahrradtypByDateTime,
    ReasonByDateTime,
    TriesByDateTime,
    datenListView,
    datenschutz,
    impressum,
    main_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_view, name="main"),
    path("nach_datum/fahrradtyp", FahrradtypByDateTime, name="FahrradtypByDateTime"),
    path("nach_datum/schadenshoehe", DmgByDateTime, name="DmgByDateTime"),
    path("nach_datum/delikt", DelictByDateTime, name="DelictByDateTime"),
    path("nach_datum/erfassungsgrund", ReasonByDateTime, name="ReasonByDateTime"),
    path("nach_datum/versuche", TriesByDateTime, name="TriesByDateTime"),
    path("api/", include("main.api.urls", "main_api")),
    path("datenschutzhinweise", datenschutz, name="Datenschutz"),
    path("impressum", impressum, name="Impressum"),
    path("daten", datenListView.as_view(), name="daten"),
]
