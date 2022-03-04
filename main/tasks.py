import datetime
import hashlib
import json
import os

import numpy as np
import pandas as pd
import tweepy
from background_task import background
from dateutil.utils import today
from django.db.models import Count
from dotenv import load_dotenv

from main.models import Report

load_dotenv()


def tweetStats():
    # Authenticate to Twitter
    api_key = os.getenv("TWITTER_KEY")
    api_key_secret = os.getenv("TWITTER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(api_key, api_key_secret)

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    today = datetime.date.today()

    yesterday = today - datetime.timedelta(days=2)
    reports = (
        Report.objects.filter(createdDay__gte=yesterday)
        .values("typeOfBike")
        .annotate(count=Count("typeOfBike"))
        .order_by("count")
    )

    tweet = (
        "Es wurden am "
        + yesterday.strftime("%d.%m.%Y")
        + " folgende Fahrräder in Berlin als gestohlen gemeldet:\n"
    )
    for data in reports:
        tweet += str(data["count"]) + "x " + data["typeOfBike"] + "\n"
    tweet += "\n[1/2]"

    answer = api.update_status(tweet)

    data = Report.objects.filter(createdDay__gte=yesterday).values(
        "beginHour", "endHour", "beginDay", "endDay", "damage"
    )

    newDataset = [0 for x in range(0, 24)]

    for i in data:
        dayDifference = abs((i["beginDay"] - i["endDay"]).days)
        if dayDifference > 1:
            tmpDays = [0 for x in range(0, dayDifference * 24)]
            amoundOfHours = (i["endHour"] - i["beginHour"]) % 24
            amoundOfHours += (dayDifference - 1) * 24
            if amoundOfHours != 0:
                avg = round(i["damage"] / amoundOfHours, 2)
            else:
                avg = i["damage"]

            for j in range(i["beginHour"], i["beginHour"] + amoundOfHours):
                tmpDays[j % (24 * dayDifference)] += avg

            for k in range(0, len(tmpDays)):
                newDataset[k % 24] += tmpDays[k]
        else:
            j = (i["endHour"] - i["beginHour"]) % 24
            if j != 0:
                avg = round(i["damage"] / j, 2)
            else:
                avg = i["damage"]
            for tmp in range(i["beginHour"], i["beginHour"] + j):
                newDataset[tmp % 24] += avg
    newDataset = list(map(lambda x: round(x, 2), newDataset))
    idmax = np.array(newDataset).argmax()
    tweet = "Die maximale Schadenshöhe aus den vermuteten Tatzeiträumen von Diebstählen, die gestern angelegt wurden beträgt:\n"
    tweet += (
        str(newDataset[idmax]).replace(".", ",")
        + "€ um "
        + str(idmax)
        + " Uhr.\n\nZudem waren "
    )

    amountOfReports = Report.objects.filter(createdDay__gte=yesterday).count()
    amountOfSuccessfullTries = Report.objects.filter(
        createdDay__gte=yesterday, tryBike="Nein"
    ).count()
    proportion = amountOfSuccessfullTries / amountOfReports
    tweet += (
        str(round(proportion, 4) * 100) + "% der versuchten Diebstähle erfolgreich.\n\n"
    )
    tweet += (
        "Weitere Informationen findet ihr unter Fahrraddiebstahl-berlin.de\n\n[2/2]"
    )
    api.update_status(tweet, answer.id)
    print("Alle Tweets geposted!")


def transform_date(datestr):
    """Transform date string

    from dd.mm.YYYY to YYYY-mm-dd
    """
    return "-".join(datestr.split(".")[::-1])


@background(schedule=60)
def get_data():
    url = "https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv"
    csv = pd.read_csv(url, encoding="unicode_escape")

    csv["ANGELEGT_AM"] = csv["ANGELEGT_AM"].apply(transform_date)
    csv["TATZEIT_ANFANG_DATUM"] = csv["TATZEIT_ANFANG_DATUM"].apply(transform_date)
    csv["TATZEIT_ENDE_DATUM"] = csv["TATZEIT_ENDE_DATUM"].apply(transform_date)

    newData = False
    for _, row in csv.iterrows():

        lor = str(row["LOR"])
        if len(lor) < 8:
            lor = lor.zfill(8)

        tmp = (
            str(row["ANGELEGT_AM"])
            + str(row["TATZEIT_ANFANG_DATUM"])
            + str(row["TATZEIT_ANFANG_STUNDE"])
            + str(row["TATZEIT_ENDE_DATUM"])
            + str(row["TATZEIT_ENDE_STUNDE"])
            + lor
            + str(row["ART_DES_FAHRRADS"])
            + str(row["DELIKT"])
        )
        hash = hashlib.md5(tmp.encode()).hexdigest()

        if Report.objects.filter(pk=hash).exists():
            continue
        else:
            newData = True
            print(f"Creating record {hash}")

            Report.objects.create(
                createdDay=row["ANGELEGT_AM"],
                beginDay=row["TATZEIT_ANFANG_DATUM"],
                beginHour=row["TATZEIT_ANFANG_STUNDE"],
                endDay=row["TATZEIT_ENDE_DATUM"],
                endHour=row["TATZEIT_ENDE_STUNDE"],
                lor=lor,
                damage=row["SCHADENSHOEHE"],
                tryBike=row["VERSUCH"],
                typeOfBike=row["ART_DES_FAHRRADS"],
                delict=row["DELIKT"],
                reason=row["ERFASSUNGSGRUND"],
                hashvalue=hash,
                date_published=today(),
            )

    twitter = os.getenv("USE_TWITTER", "0")
    if newData and twitter:
        tweetStats()
