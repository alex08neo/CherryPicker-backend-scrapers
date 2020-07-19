from bs4 import BeautifulSoup
from requests import get
import VenueClass
import json
from DataFormatting.FormatTime import FormatTime

debug = False
# Hardcoded venue types
# Note that the below are only a subset of what is offered on the site

if debug:
    venueTypes = ["xmas-party"]
else:
    venueTypes = ["academic-venues", "activity-day",
                  "afternoon-tea", "ball", "anniversary-party", "art-studio", "asian-weddings", "auditorium-venues",
                  "away-day-venues", "baby-shower", "bbq-venues", "bowling-alley", "birthday-dinner", "birthday-party", "boat", "unique",
                  "cafe-venues", "garden", "terrace", "kitchen"]


allVenues = []  # Array to store all Venues of type VenueClass
visitedVenues = []


def extractVenue(room, venueType):
    print("----")

    # Get ratings
    ratings = room["room_rating"]

    # Get images link
    images = room["photos"]

    # Get Title
    title = room["venue_name"] + " | " + room["room_name"]

    # Get Room Name
    roomName = [room["room_name"]]

    # Tags
    tags = [venueType]

    # description
    description = room["room_description"]

    # promos
    promos = ""

    # Get Link
    link = room["room_url"]

    if(link in visitedVenues):
        return
    else:
        visitedVenues.append(link)

    # Request actual Link to entire page
    response = get(link)
    html_soup_individual_venue = BeautifulSoup(response.text, 'html.parser')

    # Get Location
    locationHtml = html_soup_individual_venue.find(
        'div', class_="c-room-header__location js-open-map-modal")
    location = locationHtml.find(
        "span", class_="c-room-header__text_link").getText().strip()

    # price
    priceTable = html_soup_individual_venue.findAll(
        "div", {"class": "c-pricing-table", "data-type": "pricing"})
    pricingPerDay = priceTable[0].findAll(
        "div", class_="c-pricing-table__day")
    price = []
    for day in pricingPerDay:
        dayOfWeek = day.find(
            'div', class_='c-pricing-table__item c-pricing-table__item--day').getText().strip()
        time = day.find(
            'div', class_='c-pricing-table__item c-pricing-table__item--time').getText().strip()

        priceHtml = day.find(
            'div', class_='c-pricing-table__item c-pricing-table__item--price').getText().strip().replace(" ", "").split("\n")
        actualPrice = ""
        for text in priceHtml:
            if(text != ""):
                actualPrice += text+" "

        priceForDay = {
            "dayOfWeek": dayOfWeek,
            "time": FormatTime(time),
            "pricing": actualPrice
        }
        price.append(priceForDay)

    # Facilities
    # -> Get all venues with class room_feature then remove those appearing
    # in the classname with strikethrough
    allFacilitiesStrikeArr = []
    allFacilitiesStrike = html_soup_individual_venue.findAll(
        "div", class_="room__feature room__feature--strikethrough")
    for facility in allFacilitiesStrike:
        allFacilitiesStrikeArr.append(facility.getText().strip())

    facilities = []
    allFacilities = html_soup_individual_venue.findAll(
        "div", class_="room__feature")
    for facility in allFacilities:
        if not facility.getText().strip() in allFacilitiesStrikeArr:
            facilities.append(facility.getText().strip())

    # Get PAX
    paxHtml = html_soup_individual_venue.findAll(
        'div', class_='room__wrapper--header')
    if(paxHtml):
        paxInfo = paxHtml[0].find(
            'div', class_="c-venue-feature__label").getText().split()
        pax = paxInfo[2].replace("seats", "").replace("standing", "")

    # Create Venue Class
    singleVenue = VenueClass.Venue(
        ratings, link, images, title, location, tags, price, pax, description, facilities, roomName, promos)

    # Add Venue
    allVenues.append(singleVenue.getVenue())

    if debug:
        print(singleVenue.getVenue())


# MAIN FUNCTION
print("Start TagVenue Scraper")
for venueType in venueTypes:
    # Request json from website
    url = "https://www.tagvenue.com/ajax/search-list?longitude_from=103.41156005859375&longitude_to=104.2767333984375&latitude_from=1.219047114735722&latitude_to=1.453815835138326&center_latitude=1.336434280186183&center_longitude=103.84414672851562&hideRoomsData=false&room_tag={}&supervenues_only=false&iso_country_code=SG&view=results".format(
        venueType)
    response = get(url).json()

    for index, room in enumerate(response["rooms"]):
        try:
            extractVenue(room, venueType)
        except:
            print("Error in scraper for {}".format(room["venue_name"]))

with open('Data/TagVenue.json', 'w', encoding='utf-8') as outfile:
    json.dump(allVenues,
              outfile, ensure_ascii=False)

if debug:
    print("The End")
