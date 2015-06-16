import csv
import json
from datetime import date

print("Converting users...")
users = []
with open("data/users.dat") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for row in reader:
        users.append({"model": "ratings.Rater",
                      "pk": row[0],
                      "fields": {
                          "age": row[2],
                          "gender": row[1],
                          "zipcode": row[4]
                      }})

with open("ratings/fixtures/users.json", "w") as outfile:
    outfile.write(json.dumps(users))


print("Converting genres...")
genres = set()
genre_list = []
genre_dict = {}
with open("data/movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for row in reader:
        genres.update(row[2].split("|"))
    for idx, genre in enumerate(sorted(genres)):
        genre_dict[genre] = idx
    for genre, idx in genre_dict.items():
        genre_list.append({"model": "ratings.Genre",
                        "pk": idx + 1,
                       "fields": {
                        "name": genre
                       }})

with open("ratings/fixtures/genres.json", "w") as outfile:
    outfile.write(json.dumps(genre_list))

print("Converting movies...")
movies = []
with open("data/movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for row in reader:
        movies.append({"model": "ratings.Movie",
                       "pk": row[0],
                       "fields": {
                           "title": row[1],
                           "genre": [genre_dict[genre]+1 for genre in row[2].split("|")]
                       }})

with open("ratings/fixtures/movies.json", "w") as outfile:
    outfile.write(json.dumps(movies))

print("Converting ratings...")
ratings = []
with open("data/ratings.dat") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for idx, row in enumerate(reader):
        date2 = date.fromtimestamp(int(row[3])).__str__()
        ratings.append({"model": "ratings.Rating",
                        "pk": idx + 1,
                        "fields": {
                            "userid": row[0],
                            "movieid": row[1],
                            "rating": row[2],
                            "date": date2
                        }})

with open("ratings/fixtures/ratings.json", "w") as outfile:
    outfile.write(json.dumps(ratings))