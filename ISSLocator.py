"""
Written by Hayden Gebhardt and James Kunstle, (6/25/2020)

Where is the ISS, and what is it's current distance from me?
We use an API that has already scraped the ISS Long/Lat data from
a public website in order to determine what the current Long/Lat distance
is from some initial location to the ISS.

We are intentionally failing to consider, at the moment, the altitude of the
ISS, because it would be ridiculous to care about that.

Non-standard libraries used:

    Geocoder
    Requests
    JSON

"""


"""
Imports
"""
import urllib.request
import json
import requests
import time as t
import math
import geocoder
from datetime import datetime as dt


"""
Global Variables
"""

API_Link: str = "http://api.open-notify.org/iss-now.json"


"""
Object Declaration
"""

class ISS_Locator(object):

    def __init__(self, current_long: int, current_lat: int, ISS_API: str)->None:
        #where the ISS is currently
        self.lat:  float = current_lat
        self.long: float = current_long

        #where the user is currently
        self.user_lat:  float = 0.0
        self.user_long: float = 0.0

        #current distance between user and ISS
        self.current_distance:  float = 0.0

        #current timestamp from the ISS API
        self.current_timestamp: float = 0.0

        #API for the ISS current location
        self.api:  str = ISS_API

        #API for the user current location
        self.user_IP_URL: str = 'http://freegeoip.net/json'

        #standard variable define
        self.SLEEP_TIME: float = 1.0

        return

    def get_ISS_location(self)->None:
        with urllib.request.urlopen(self.api) as url:
            data = json.loads(url.read().decode())
            self.long = float(data['iss_position']['longitude'])
            self.lat = float(data['iss_position']['latitude'])
            self.current_timestamp = float(data["timestamp"])
        return


    def get_user_location(self)->None:
        #code taken from:
        # https://stackoverflow.com/questions/24906833/get-your-location-through-python

        g = geocoder.ip('me')
        self.user_lat = g.latlng[0]
        self.user_long = g.latlng[1]
        return


    def get_real_distance(self)->None:
        #code taken from:
        # https://kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python

        #earth radius, this determines the unit of distance
        R: float = 6373.0

        self.get_ISS_location()
        self.get_user_location()

        lat1: float = math.radians(self.lat)
        lon1: float = math.radians(self.long)
        lat2: float = math.radians(self.user_lat)
        lon2: float = math.radians(self.user_long)

        dlon: float = lon2 - lon1
        dlat: float = lat2 - lat1

        #Haversine formula, takes the curvature of Earth into account in distance calculation
        a: float = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c: float = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance: float = R * c

        self.current_distance = distance
        return

    def print_ISS_location(self)->None:
        print("")
        print("Current ISS Location:")
        print("-----------------------")
        print("Longitude:", self.long)
        print("Latitude: ", self.lat)
        print("")

    def print_ISS_location_repeating(self, num_prints: int = 0)->None:
        self.get_ISS_location()
        print("")
        print("Current ISS Location:")
        print("-----------------------")
        print("Longitude:", self.long)
        print("Latitude: ", self.lat)
        print("")


        #NOTE(James): I was drunk when I wrote this so it could definitely be
        #   more concise.
        if num_prints == 0:
            while(1):
                t.sleep(self.SLEEP_TIME)
                self.get_ISS_location()
                print("-----------------------")
                print("Longitude:", self.long)
                print("Latitude: ", self.lat)
                print("")
            return
        else:
            prints: int = 0
            while prints < num_prints:
                t.sleep(self.SLEEP_TIME)
                self.get_ISS_location()
                print("-----------------------")
                print("Longitude:", self.long)
                print("Latitude: ", self.lat)
                print("")

    def print_real_distance(self, num_prints: int = 0)->None:
        if num_prints == 0:
            while(1):
                t.sleep(self.SLEEP_TIME)
                self.get_real_distance()
                print("-----------------------")
                print("Current Distance:", self.current_distance, "kilometers")
                self.print_datetime()
            return
        else:
            prints: int = 0
            while prints < num_prints:
                t.sleep(self.SLEEP_TIME)
                self.get_real_distance()
                print("-----------------------")
                print("Current Distance:", self.current_distance, "kilometers")
                self.print_datetime()
        return

    def print_datetime(self)->None:
        #code taken from:
        # https://www.programiz.com/python-programming/datetime/timestamp-datetime
        dt_object = dt.fromtimestamp(self.current_timestamp)
        print("Current Time:", dt_object)

"""
Main
"""

def main() -> None:
    locator_obj = ISS_Locator(0, 0, API_Link)
    locator_obj.print_real_distance()

if __name__ == "__main__":
    main()
