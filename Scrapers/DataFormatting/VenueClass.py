# TODO: Once all scrapers has been finalised, this file will be shifted to DataFormatting folder.
# roomName attr will also be removed.

# Venue Class
class Venue:
    venue = {}

    def __init__(self, ratings, link, images, title, location, tags, price, pax, description, facilities=[], promos=""):
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
            "promos": promos,  # Promo string
        }

    def getVenue(self):
        return self.venue

# price is a list object of the format
# {
# "dayOfWeek": "",
# "time": "",
# "pricing": ""
# }
