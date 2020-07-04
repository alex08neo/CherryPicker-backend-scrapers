# Venue Class
class Venue:
    venue = {}

    def __init__(self, ratings, link, images, title, location, tags, price, pax, description, facilities=[], roomName=[""], promos=""):
        self.venue = {
            "ratings": ratings,
            "link": link,
            "images": images,
            "title": title,
            "location": location,
            "tags": tags,
            "price": price,
            "pax": pax,  # Pax is standing capacity
            "description": description,
            "facilities": facilities,
            "roomName": roomName,  # Some venues might have more than 1 room
            "promos": promos,  # Promo string
        }

    def getVenue(self):
        return self.venue

# price is a list object of either of the 2 format
# (1)
# {
# "dayOfWeek": "",
# "time": "",
# "pricing": ""
# }
# (2)
# [{"room": "", "price": ""},
# {"room": "", "price": ""}
# {"room": "", "price": ""}
# ]
