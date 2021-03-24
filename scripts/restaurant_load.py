import csv  # How to use cvs https://docs.python.org/3/library/csv.html

# How to use 'runscript' using django extensions: https://django-extensions.readthedocs.io/en/latest/runscript.html

# to wipe out and put all data from restaurantes.csv into the database just run:
# "python manage.py runscript restaurant_load" in the terminal

from restaurants.models import Restaurants


def run():
    fhand = open('restaurants/restaurantes.csv', encoding="utf8")
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Restaurants.objects.all().delete()

    for row in reader:
        print(row)
        r = Restaurants(
            id = row[0], 
            rating = row[1],
            name = row[2],
            site = row[3],
            email = row[4],
            phone = row[5],
            street = row[6],
            city = row[7],
            state = row[8],
            lat = row[9],
            lng = row[10]
            )
       
        r.save()