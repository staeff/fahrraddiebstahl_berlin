"""Import bike theft data from csv file."""
import pandas as pd
import hashlib
from dateutil.utils import today
from main.models import Report
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Import bike theft data from a csv file."""

    help = "Import bike theft data from a csv file"

    @staticmethod
    def transform_date(datestr):
        """Transform date string

        from dd.mm.YYYY to YYYY-mm-dd
        """
        return "-".join(datestr.split(".")[::-1])

    def handle(self, *args, **options):
        """Process the CSV file to create invites records."""

        url = "https://www.internetwache-polizei-berlin.de/vdb/Fahrraddiebstahl.csv"
        csv = pd.read_csv(url, encoding="unicode_escape")

        csv["ANGELEGT_AM"] = csv["ANGELEGT_AM"].apply(self.transform_date)
        csv["TATZEIT_ANFANG_DATUM"] = csv["TATZEIT_ANFANG_DATUM"].apply(self.transform_date)
        csv["TATZEIT_ENDE_DATUM"] = csv["TATZEIT_ENDE_DATUM"].apply(self.transform_date)

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
