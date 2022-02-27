
# Create your models here.
# -*- coding: utf-8 -*-
from django.db import models

class Report(models.Model):
    BIKE_TYPES = [
        ("HF", "Herrenfahrrad"),
        ("FF", "Fahrrrad"),
        ("DF", "Damenfahrrad"),
        ("MB", "Mountainbike"),
        ("RB", "Rennrad"),
        ("KF", "Kinderfahrrad"),
        ("LF", "Lastenfahrrad"),
        ("DF", "diverse Fahrräder"),
    ]
    TRYBIKE = [("T", "Ja"), ("F", "Nein"), ("U", "Unbekannt")]
    DELICT = [("FD", "Fahrraddiebstahl"), ("KB", "Keller- und Bodeneinbruch")]
    REASON = [
        ("SF", "Sonstiger schwerer Diebstahl von Fahrrädern"),
        ("SK", "Sonstiger schwerer Diebstahl in/aus Keller/Boden von Fahrrädern"),
        ("EF", "Einfacher Diebstahl von Fahrrädern"),
        ("EK", "Einfacher Diebstahl aus Keller/Boden von Fahrrädern"),
    ]

    createdDay = models.DateField()
    beginDay = models.DateField()
    beginHour = models.PositiveSmallIntegerField()
    endDay = models.DateField()
    endHour = models.PositiveSmallIntegerField()
    lor = models.CharField(max_length=8)
    damage = models.IntegerField()
    tryBike = models.CharField(max_length=1, choices=TRYBIKE)
    typeOfBike = models.CharField(max_length=2, choices=BIKE_TYPES)
    delict = models.CharField(max_length=2, choices=DELICT)
    reason = models.CharField(max_length=2, choices=REASON)
    hashvalue = models.CharField(max_length=32, primary_key=True)
    date_published = models.DateField(auto_now_add=True, verbose_name="date published")
