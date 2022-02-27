# Fahrraddiebstahl Berlin

Internetadresse: [https://fahrraddiebstahl-berlin.de/](https://fahrraddiebstahl-berlin.de/)

Diese kleine Django-Webapp visualisiert die Daten der Polizei Berlin von Fahrraddiebstählen in Berlin. Die Daten werden von der Internetwache der Berliner Polizei im Zuge der Open Data Initiative täglich um 12:00 Uhr veröffentlicht.

Mehr Infos zu den Daten: https://daten.berlin.de/datensaetze/fahrraddiebstahl-berlin

Daten direkt herunterladen unter: https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv

Presse: https://www.golem.de/news/berlin-polizei-testet-open-data-gegen-fahrradklau-2109-159424.html

## Geographische Informationen (LOR)

Die Geographie von Berlin ist durch den Senat in lebensweltlich orientierte Räume (LOR) organisiert.
Die Daten liegen in drei Hierarchiestufen vor: Prognoseraum (PGR), Bezirksregion (BZR) und Planungsraum (PLZ).

Es handelt sich um Vektordaten, die für das Projekt in `geojson` umgewandelt wurden.
Der verwendete Datensatz ist Stand 01.01.2021 (542 PLR)

[Überblick](https://www.stadtentwicklung.berlin.de/planen/basisdaten_stadtentwicklung/lor/de/download.shtml)

## Technologie

### Django 3.2.7

### Django Background Task - https://django-background-tasks.readthedocs.io/en/latest/

to run tasks to this:

`python manage.py process_tasks`
