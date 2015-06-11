import csv
import json

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

print("Converting movies...")
movies = []
with open("data/movies.dat", encoding="windows-1252") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for row in reader:
        movies.append({"model": "ratings.Movie",
                       "pk": row[0],
                       "fields": {
                           "title": row[1]
                       }})

with open("ratings/fixtures/movies.json", "w") as outfile:
    outfile.write(json.dumps(movies))

print("Converting ratings...")
ratings = []
with open("data/ratings.dat") as infile:
    reader = csv.reader((line.replace("::", "_") for line in infile),
                        delimiter="_")
    for idx, row in enumerate(reader):
        ratings.append({"model": "ratings.Rating",
                        "pk": idx + 1,
                        "fields": {
                            "userid": row[0],
                            "movieid": row[1],
                            "rating": row[2]
                        }})

with open("ratings/fixtures/ratings.json", "w") as outfile:
    outfile.write(json.dumps(ratings))