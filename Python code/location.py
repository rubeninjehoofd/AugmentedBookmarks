# importing geopy library
from geopy.geocoders import Nominatim

class Location():

    # def __init__(self):
    #     self.location()

    def location(self):
        # calling the Nominatim tool
        loc = Nominatim(user_agent="GetLoc")

        # entering the location name
        getLoc = loc.geocode("jopenkerk, haarlem")

        # printing address
        print(getLoc.address)

        # printing latitude and longitude
        print("Latitude = ", getLoc.latitude)
        print("Longitude = ", getLoc.longitude)


if __name__ == "__main__":
    location = Location()