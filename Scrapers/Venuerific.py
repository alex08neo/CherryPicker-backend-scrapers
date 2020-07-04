from bs4 import BeautifulSoup
from requests import get
import VenueClass
import json

allVenues = []  # Array to store all Venues of type VenueClass

debug = False


def extractVenue(venue):
    print("------")

    # Extract Rating from this page first
    ratingsHtml = venue.find('p', class_="reviews")
    ratings = len(ratingsHtml.findAll(
        'span', class_="fa fa-star", style="color: #fa5f4a"))

    linkToGo = venue.find('a')['href']
    # Request actual Link to entire page
    url = "https://www.venuerific.com{}".format(linkToGo)
    response = get(url)
    html_soup_individual_venue = BeautifulSoup(response.text, 'html.parser')
    # Extract Link
    link = url

    # Extract Images
    imagesLink = []

    bigImage = html_soup_individual_venue.find(
        'div', class_="col-md-6 big-image").find('img')['src']
    imagesLink.append(bigImage)

    smallImages = html_soup_individual_venue.findAll(
        'div', class_="col-md-6 small-image")
    for image in smallImages:
        if(image.find('img')):
            imagesLink.append(image.find('img')['src'])

    # Extract Title
    title = html_soup_individual_venue.find(
        'div', class_="title col-sm-12 col-md-12").find('h1').get_text().strip()

    # Extract Location
    location = html_soup_individual_venue.find(
        'span', class_="area").get_text().replace('(see map)', '').strip()

    # Extract Venue Type/Tags
    tagHtml = html_soup_individual_venue.find('span', class_="venue-type")
    tags = []
    if(tagHtml):
        tagsList = tagHtml.get_text().split(", ")
        for tag in tagsList:
            tags.append(tag)

    # Optional Promotion
    promoHtml = html_soup_individual_venue.find(
        'div', id="promotion-description")
    promos = ""
    if(promoHtml):
        promos += promoHtml.getText().strip()

    # Rooms available
    allRoomsHtml = html_soup_individual_venue.findAll(
        'div', class_="info-title")
    roomName = []
    for roomHtml in allRoomsHtml:
        roomName.append(roomHtml.find("h2").getText().strip())

    # Price info for the different rooms
    price = []
    priceHtmls = html_soup_individual_venue.findAll(
        'div', class_="abstract price-info")
    for index, prices in enumerate(priceHtmls):
        if prices:
            priceVal = prices.getText().strip(). replace("PRICE INFO", "")
            room = roomName[index]
            price.append({
                "room": room,
                "price": priceVal
            })

    # Starting Price
    # Only use this as pricing if none is specified above
    if(len(price) == 0):
        priceHtml = html_soup_individual_venue.find('div', class_="price")
        price = ""
        if(priceHtml and priceHtml.find('label')):
            price += priceHtml.find('label').getText().strip()
        price += " "
        if(priceHtml and priceHtml.find('strong')):
            price += priceHtml.find('strong').getText().strip()

        price = [price.strip()]

    # Pax
    paxHtml = html_soup_individual_venue.find(
        'div', class_="col-md-3 col-xs-12")
    pax = ""
    if(paxHtml):
        pax = paxHtml.find('p').get_text().strip()

    # Description
    descriptionHtml = html_soup_individual_venue.find(
        'div', id="description-to-view")
    description = ""
    if(descriptionHtml):
        description = descriptionHtml.get_text()

    # Facilities
    facilitiesHtml = html_soup_individual_venue.findAll(
        'div', class_="col-md-4 col-xs-6 col-sm-6 venuerific-icon-wrapper")
    facilities = []
    for facility in facilitiesHtml:
        if(not facility.find('div', class_="venuerific-icon-food-beverage-chinese")):
            facilities.append(facility.getText().strip())

    # Create Venue Class
    singleVenue = VenueClass.Venue(
        ratings, link, imagesLink, title, location, tags, price, pax, description, facilities, roomName, promos)

    # Add Venue to object
    if(not singleVenue in allVenues):
        allVenues.append(singleVenue.getVenue())

    if debug:
        print(singleVenue.getVenue())


def getVenuesOnPage(html_soup):
    venues = html_soup.find_all(
        'article', class_='venue-item flex-column col-md-4 col-sm-4 col-xs-12')

    for venue in venues:
        try:
            extractVenue(venue)
        except:
            print("Error in scraper for {}".format(venue.find('a')['href']))


# MAIN FUNCTION
print("Start Venuerific Scraper")
currentPage = 1  # Initialised to first page
while True:
    # Request html from website
    url = "https://www.venuerific.com/sg/search?page={}".format(currentPage)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # Check for last page
    blankPage = html_soup.find_all('div', class_='blank-slate extra-large')
    if(len(blankPage) == 1):
        break
    # Call function to get venues
    getVenuesOnPage(html_soup)
    # Increase counter to go next page
    currentPage += 1

with open('../Data/venuerific.json', 'w') as outfile:
    json.dump(allVenues, outfile)


if debug:
    print("The End")
