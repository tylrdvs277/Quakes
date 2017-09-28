# Name:         Tyler Davis
# Course:       CPE 101
# Instructor:   Nupur Garg
# Assignment:   Project 5
# Term:         Spring 2017

from urllib.request import urlopen
from json import loads
from datetime import datetime
from operator import attrgetter


# Create/Display Earthquakes

class Earthquake:

    def __init__(self, place, mag, longitude, latitude, time):
        self.mag = mag
        self.latitude = latitude
        self.longitude = longitude
        self.time = time 
        self.place = place

    def __eq__(self, other):
        return (self.mag == other.mag and
                self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.time == other.time and
                self.place == other.place)

    def __str__(self):
        return ("({0:.2f}){1:>41} at {2} ({3:>8.3f}, {4:.3f})"
                .format(self.mag, self.place, time_to_str(self.time), 
                      self.longitude, self.latitude))

def time_to_str(time):
    """Converts integer seconds since unix epoch to a string.
    Args:
        time (int): Unix time
    Returns:
        A nicely formated time string
    """
    return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

def read_quakes_from_file(filename):
    file_1 = open(filename, "r")
    quakes = []
    for line in file_1:
        (mag, longi, lat, time, place) = line.strip().split(" ", 4)
        quakes.append(Earthquake(place, float(mag), float(longi), 
                                 float(lat), int(time)))
    file_1.close()
    return quakes

# Writes to the original file in the same way as read
def write_new_file(quakes, filename = "quakes.txt"):
    file_1 = open(filename, "w")
    for quake in quakes:
        file_1.write("{0} {1} {2} {3} {4}\n".format(quake.mag,
                     quake.longitude, quake.latitude, quake.time,
                     quake.place))
    file_1.close()

def display_quakes(quakes):
    print("\nEarthquakes:\n------------")
    for quake in quakes:
        print(quake)


# Sort By Quakes

def sort_quakes(quakes, option):
    if option in "mM":
        quakes.sort(key = attrgetter("mag"), reverse = True)
    elif option in "tT":
        quakes.sort(key = attrgetter("time"), reverse = True)
    elif option in "lL":
        quakes.sort(key = attrgetter("longitude"))
    elif option in "aA":
        quakes.sort(key = attrgetter("latitude"))
    return tuple(quakes)


# Filer Functions

def filter_by_mag(quakes, low, high):
    return (quake for quake in quakes 
            if low <= quake.mag <= high)

def filter_by_place(quakes, word):
    return (quake for quake in quakes 
            if word.lower() in quake.place.lower())


# Gets Data From USGS

def get_json(url):
    """Function to get a JSON dictionary from a website.
    Args:
        url (str): The url from which to get the JSON
    Returns:
        A Python dictionary containing the information from the JSON object
    """
    with urlopen(url) as response:
        html = response.read()
    htmlstr = html.decode("utf-8")
    return loads(htmlstr)

def quake_from_feature(feature):
    return Earthquake(feature["properties"]["place"],
                      float(feature["properties"]["mag"]), 
                      float(feature["geometry"]["coordinates"][0]),
                      float(feature["geometry"]["coordinates"][1]),
                      int(feature["properties"]["time"] / 1000))

# Creates a list of earthquake objects from the features array 
def get_new_quakes(features_dict):
    return (quake_from_feature(feature_dict) 
            for feature_dict in features_dict)

# Determines if there are any new quakes, adds if there are
def add_if_new(quakes, new_quakes):
    for new_quake in new_quakes:
        if new_quake not in quakes:
            quakes.append(new_quake)
    return tuple(quakes)

# Takes the new quakes list and old list to see if they are
# different. Returns the appropriate and prints message
def update_quakes_list(quakes, temp_quakes):
    if len(temp_quakes) != len(quakes):
        print("\nNew quakes found!!!")
        return temp_quakes
    return quakes


# Takes User Input

def get_input():
    category = sub_cat = string = low_bound = up_bound = None
    category = input("\nOptions:\n  (s)ort\n  (f)ilter\n  (n)ew quakes\n"
                     "  (q)uit\n\nChoice: ")
    if category in "sS":
        sub_cat = input("Sort by (m)agnitude, (t)ime, (l)ongitude,"
                        " or l(a)titude? ")
    elif category in "fF":
        sub_cat = input("Filter by (m)agnitude or (p)lace? ")
        if sub_cat in "pP":
            string = input("Search for what string? ")
        else:
            low_bound = float(input("Lower bound: "))
            up_bound = float(input("Upper bound: "))
    return (category, sub_cat, string, low_bound, up_bound)
