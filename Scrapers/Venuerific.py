from bs4 import BeautifulSoup
from requests import get
import VenueClass
import json
from DataFormatting.FormatTime import FormatTime
from DataFormatting.FormatPrice import FormatPrice
from DataFormatting.FormatText import FormatSentence, FormatTitle

allVenues = []  # Array to store all Venues of type VenueClass
visitedVenues = []

debug = False

# For each venue, there might be more than 1 room
# First, we will check whether there are more than 1 room for each venue.
# If there are, we will extract those [title, imagesLink, price, pax, description, facilities] details
# individually for each room and create VenueClass objects individually for them
# Otherwise, only 1 VenueClass object will be created


def extractVenue(venue):
    print("--Venuerific--")

    # (1)
    # Extract Rating from this page first
    ratingsHtml = venue.find('p', class_="reviews")
    ratings = len(ratingsHtml.findAll(
        'span', class_="fa fa-star", style="color: #fa5f4a"))

    linkToGo = venue.find('a')['href']
    # Request actual Link to entire page
    url = "https://www.venuerific.com{}".format(linkToGo)
    if(url in visitedVenues):
        return
    else:
        visitedVenues.append(url)

    response = get(url)
    html_soup_individual_venue = BeautifulSoup(response.text, 'html.parser')
    # Extract main link
    link = url

    # (2)
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
        promos += FormatSentence(promoHtml.getText().strip())

    # Time available
    searchHtml = html_soup_individual_venue.findAll(
        'div', class_="col-xs-12")
    availabilities = []
    for indvClass in searchHtml:
        if(indvClass.find("h3") and indvClass.find("h3").getText().strip() == "AVAILABILITY"):
            availRows = indvClass.findAll('dl')
            for eachDay in availRows:
                key = eachDay.find('dt').getText().strip()
                val = eachDay.find('dd').getText().strip()
                if(val != '–'):
                    item = {
                        "dayOfWeek": key,
                        "time":  FormatTime(val)
                    }
                    availabilities.append(item)
                else:
                    break

    # Price info for the different rooms
    price = []
    priceHtmls = html_soup_individual_venue.findAll(
        'div', class_="abstract price-info")
    for index, prices in enumerate(priceHtmls):
        if prices:
            priceVal = prices.getText().strip().replace("PRICE INFO", "")
            if(len(availabilities) == 0):
                item = {"pricing": priceVal}
                price.append(item)
            else:
                for available in availabilities:
                    item = {"pricing": priceVal}
                    item.update(available)
                    price.append(item)

    # Starting Price
    # Only use this as pricing if none is specified above
    if(len(price) == 0):
        priceHtml = html_soup_individual_venue.find('div', class_="price")
        priceVal = ""
        if(priceHtml and priceHtml.find('label')):
            priceVal += priceHtml.find('label').getText().strip()
        priceVal += " "
        if(priceHtml and priceHtml.find('strong')):
            priceVal += priceHtml.find('strong').getText().strip()

        if(len(availabilities) == 0):
            if(priceVal.strip() == ""):
                price = [{
                    "pricing": "Inquire for Pricing",
                    "dayOfWeek": "Inquire for days availabilities",
                    "time": "Inquire for timing availabilities"
                }]
            else:
                price = [{
                    "pricing": priceVal.strip(),
                    "dayOfWeek": "Inquire for days availabilities",
                    "time": "Inquire for timing availabilities"
                }]

        else:
            for available in availabilities:
                if(priceVal.strip() == ""):
                    item = {"pricing": "Inquire for Pricing"}
                else:
                    item = {"pricing": priceVal.strip()}
                item.update(available)
                price.append(item)

    # Description, Main description for venue
    descriptionHtml = html_soup_individual_venue.find(
        'div', id="description-to-view")
    description = ""
    if(descriptionHtml):
        description = descriptionHtml.get_text()

    # Extract Title
    title = html_soup_individual_venue.find(
        'div', class_="title col-sm-12 col-md-12").find('h1').get_text().strip()

    # (3)
    # Extracting rooms details
    # Extract id
    roomName = []
    for item in html_soup_individual_venue.find_all(attrs={"data-id": True, "data-type": False, "data-price": True}):
        roomName.append(item['data-id'])

    allVenuesHtml = html_soup_individual_venue.find(
        'div', {'id': 'venue-room-wrapper'})
    if(allVenuesHtml):
        allVenuesHtml = allVenuesHtml.findChildren("div", recursive=False)

    index = 0
    # If there are more than 1 room, we will generate VenueClasses for each of them
    if(allVenuesHtml):
        baseUrl = link
        baseTitle = title
        baseDescription = description
        for index, eachVenueHtml in enumerate(allVenuesHtml):

            link = baseUrl + "?room_id={}#room-wrappper".format(
                roomName[index])

            a = eachVenueHtml.find('div', class_="photo-video-slider")
            imagesHtml = a.findAll('li')
            imagesLink = []
            for i in imagesHtml:
                imagesLink.append(i.find('img')['src'])

            # Title
            title = FormatTitle(baseTitle + " | " + eachVenueHtml.find(
                'div', class_="info-title").find('h2').getText().strip())

            infoHtml = eachVenueHtml.find(
                'div', class_="info-title").findAll('p')

            # Capacity
            paxHtml = infoHtml[1].getText().replace(
                "Capacity", "").strip()
            pax = paxHtml.split(" - ")[1]

            moreInfoHtml = eachVenueHtml.find('div', class_="info-description").find(
                'div', class_="row").findAll('div', class_="col-xs-12")

            # Main venue description + current room description
            description = baseDescription + " " + moreInfoHtml[0].find(
                'div', class_="abstract").getText().strip()

            facilities = moreInfoHtml[1].find(
                'div', class_="abstract").getText().strip()

            pricing = None
            if(len(moreInfoHtml) == 3):
                pricingHtml = moreInfoHtml[2].find(
                    'div', class_="abstract price-info")
                if(pricingHtml):
                    pricing = pricingHtml.getText().replace("PRICE INFO", "").strip()
            elif(len(moreInfoHtml) == 4):
                pricingHtml = moreInfoHtml[3].find(
                    'div', class_="abstract price-info")
                if(pricingHtml):
                    pricing = pricingHtml.getText().replace("PRICE INFO", "").strip()

            if(len(availabilities) > 0 and pricing):
                price = []
                for available in availabilities:
                    item = {"pricing": pricing}
                    item.update(available)
                    price.append(item)
            elif pricing:
                price = [{
                    "pricing": pricing,
                    "dayOfWeek": "Inquire for day availabilities",
                    "time": "Inquire for timings availabilities"
                }]

            # FORMAT PRICE OBJECT
            price = FormatPrice(price)

            # Create Venue Class
            singleVenue = VenueClass.Venue(
                ratings, link, imagesLink, title, location, tags, price, pax, description, facilities, roomName, promos)

            # Add Venue to object
            allVenues.append(singleVenue.getVenue())

    else:
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

        # Pax
        paxHtml = html_soup_individual_venue.find(
            'div', class_="col-md-3 col-xs-12")
        pax = ""
        if(paxHtml):
            pax = paxHtml.find('p').get_text().strip().split(" - ")[1]

        # Facilities
        facilitiesHtml = html_soup_individual_venue.findAll(
            'div', class_="col-md-4 col-xs-6 col-sm-6 venuerific-icon-wrapper")
        facilities = []
        for facility in facilitiesHtml:
            if(not facility.find('div', class_="venuerific-icon-food-beverage-chinese")):
                facilities.append(facility.getText().strip())

        # FORMAT PRICE OBJECT
        price = FormatPrice(price)

        # Create Venue Class
        singleVenue = VenueClass.Venue(ratings, link, imagesLink, title, location,
                                       tags, price, pax, description, facilities, roomName, promos)

        # Add Venue to object
        allVenues.append(singleVenue.getVenue())


def getVenuesOnPage(html_soup):
    venues = html_soup.find_all(
        'article', class_='venue-item flex-column col-md-4 col-sm-4 col-xs-12')

    for venue in venues:
        try:
            extractVenue(venue)
        except:
            print("Error in scraper for {}".format("Venuerific Scraper " + venue.find('a')['href']))


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

with open('Data/Venuerific.json', 'w', encoding='utf-8') as outfile:
    json.dump(allVenues,
              outfile, ensure_ascii=False)
print("Finished Venuerific Scraper")

if debug:
    print("The End")
