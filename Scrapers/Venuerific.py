from bs4 import BeautifulSoup
from requests import get
import VenueClass

allVenues = []  # Array to store all Venues of type VenueClass

debug = False


def extractVenue(venue):
    print("------")
    # Extract Rating from this page first
    ratingsHtml = venue.find('p', class_="reviews")
    ratings = len(ratingsHtml.findAll(
        'span', class_="fa fa-star", style="color: #fa5f4a"))

    # Extract Link
    link = venue.find('a')['href']

    # Request actual Link to entire page
    url = "https://www.venuerific.com{}".format(link)
    response = get(url)
    html_soup_individual_venue = BeautifulSoup(response.text, 'html.parser')

    # Extract Images
    imagesLink = []
    bigImage = html_soup_individual_venue.find(
        'div', class_="col-md-6 big-image").find('img')['src']
    imagesLink.append(bigImage)
    smallImages = html_soup_individual_venue.findAll(
        'div', class_="col-md-6 small-image")
    for image in smallImages:
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

    # Optional Starting Price
    priceHtml = html_soup_individual_venue.find('div', class_="price")
    price = ""
    if(priceHtml and priceHtml.find('label')):
        price += priceHtml.find('label').getText().strip()
    price += " "
    if(priceHtml and priceHtml.find('strong')):
        price += priceHtml.find('strong').getText().strip()

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

    # Create Venue Class
    singleVenue = VenueClass.Venue(
        ratings, link, imagesLink, title, location, tags, promos, price, pax, description)

    # Add Venue to object
    allVenues.append(singleVenue.getVenue())

    if debug:
        print(singleVenue.getVenue())


def getVenuesOnPage(html_soup):
    venues = html_soup.find_all(
        'article', class_='venue-item flex-column col-md-4 col-sm-4 col-xs-12')

    for venue in venues:
        extractVenue(venue)


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

if debug:
    print(allVenues)
    print("The End")
