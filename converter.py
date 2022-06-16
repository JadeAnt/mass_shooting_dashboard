import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import csv
import time
import geocoder
from dotenv import load_dotenv
import os
import numpy

load_dotenv()
bing_token = os.environ.get("TOKEN")

geolocator = Nominatim(user_agent="mass_shooting_dashboard", timeout=10)


def load_data(file):
    df = pd.read_csv(file)
    df.drop(df.columns[[0, 7]], 1, inplace=True)
    print(df)
    return df

def with_geopy():
    df = load_data("mass_shooting_database_2022.csv")
    values = []

    for index in range(0, 267):
        addr = str(df["Address"][index]) + " " + str(df['City Or County'][index]) + " " + str(df['State'][index])
        print(addr)

        location = geolocator.geocode(addr)
        if location:
            lat = location.latitude
            long = location.longitude
        else:
            lat = None
            long = None

        values += [lat, long]
        print(str([lat, long]))
        time.sleep(5)

    df.insert(0, "Location", values, False)
    print(df)
    df.to_csv("database_with_location.csv")


def convert_csv_bing():
    df = load_data("mass_shooting_database_2022.csv")

    values = []
    for index in range(0, 267):
        addr = str(df["Address"][index]) + " " + str(df['City Or County'][index]) + " " + str(df['State'][index])
        print(addr)

        g = geocoder.bing(addr, key=bing_token)
        if g.latlng:
            values += g.latlng
            print(g.latlng)
        else:
            values += "None"
        time.sleep(0.25)

    locations_df = pd.DataFrame(values, columns=["Latitude", "Longitude"])
    newframe = pd.concat([df, locations_df], axis=1)
    print(newframe)
    newframe.to_csv("mass_shooting_2022_locations.csv")


def split_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__converter__':
    #convert_csv_bing()
    df = pd.read_csv("frontend/mass_shooting_2022_locations.csv")
    print(df)



