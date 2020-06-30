# Venue Class
class Venue:
    venue = {}

    def __init__(self, ratings, link, images, title, location, tags, promos, price, pax, description):
        self.venue = {
            "ratings": ratings,
            "link": link,
            "images": images,
            "title": title,
            "location": location,
            "tags": tags,
            "promos": promos,
            "price": price,
            "pax": pax,
            "description": description
        }

    def getVenue(self):
        return self.venue
