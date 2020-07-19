from bs4 import BeautifulSoup
from requests import get
import VenueClass
import json
from DataFormatting.FormatTime import FormatTime
from DataFormatting.FormatPrice import FormatPrice
from DataFormatting.FormatText import FormatTitle

allVenues = []  # Array to store all Venues of type VenueClass


def extractVenue(venue):

    print("--VenuExplorer--")

    # extract title
    title_html = venue.find('div', class_='event-name')
    title = ''
    if title_html:
        title = FormatTitle(title_html.text.strip())

    # extract tags
    venue_tags = venue.find('b', class_='t-holder').text.split(",")
    tags = []
    for venue_tag in venue_tags:
        tags.append(venue_tag.strip())

    # extract link into the venue
    venue_link = venue.find_all('a')[1]['href']
    response = get(venue_link)
    indiv_venue = BeautifulSoup(response.text, 'html.parser')

    # extract image links
    venue_images = indiv_venue.find_all('a', class_='example-image-link')
    images = []
    for venue_image in venue_images:
        image = 'https://www.venuexplorer.com.sg' + str(venue_image['href'])
        images.append(image)

    # extract availablities
    availabilities = []
    avail_html = indiv_venue.find("ul", class_="days clearfix")
    for avail in avail_html.find_all('li', class_="active"):
        dayOfWeek = avail.text.strip()
        time = FormatTime(avail.find('a')["title"])
        availabilities.append({
            "dayOfWeek": dayOfWeek,
            "time": time
        })

    # extract starting price - same for all rooms within this venue
    price_html = indiv_venue.find_all(
        'div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[1]
    price = []
    if price_html:
        for eachAvailability in availabilities:
            pricing = price_html.text.strip()
            if(pricing):
                item = {
                    "pricing": pricing,
                }
            else:
                item = {
                    "pricing": "Inquire for pricing availabilities",
                }
            item.update(eachAvailability)
            price.append(item)

    # FORMAT PRICE OBJECT
    price = FormatPrice(price)

    # extract general capacity
    capacity_html = indiv_venue.find_all(
        'div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[2]
    capacity = ''
    if capacity_html:
        capacity = capacity_html.text.split(' ')[0].strip()

    # extract location
    location_html = indiv_venue.find_all(
        'div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[3]
    location = ''
    if location_html:
        location = location_html.text.strip()

    # extract facilities
    facs = indiv_venue.find('ul', class_='feature')
    facilities = []
    for fac in facs.find_all('li'):
        facilities.append(fac.text.strip())

    # Append more tags from Welcome Section
    moreTags_html = indiv_venue.find("ul", class_="welcomes")
    for eachTag in moreTags_html.find_all('li'):
        tags.append(eachTag.text.strip())

    # extract description
    desc_html = indiv_venue.find('div', class_='quick-enquiry').p
    desc = ''
    if desc_html:
        desc = desc_html.text.strip()

    # no ratings, promos
    ratings = 0

    # create Venue Class with all inputs
    singleVenue = VenueClass.Venue(
        ratings, venue_link, images, title, location, tags, price, capacity, desc, facilities)

    # add this venue to the Venue Class array
    if(not singleVenue in allVenues):
        allVenues.append(singleVenue.getVenue())


##### MAIN FUNCTION #####
print("Start VenuExplorer Scraper")
currentPage = 1  # Initialised to first

while True:

    # Request html from website
    url = "https://www.venuexplorer.com.sg/all-venue/{}".format(currentPage)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Check for last page
    venues = html_soup.find_all('div', class_='venue-box')
    if(len(venues) == 0):
        break

    # extract venue info for all venues on this page
    for venue in venues:
        try:
            extractVenue(venue)
        except:
            print("Error in scraper for {}".format("VenueExplorer Scraper "+
                venue.find('div', class_='event-name').text.strip()))

    # Increase counter to go next page
    currentPage += 1

# write all data into a json file
with open('Data/Venuexplorer.json', 'w', encoding='utf-8') as outfile:
    json.dump(allVenues, outfile, ensure_ascii=False)

print("Finished VenuExplorer Scraper")
##### END OF MAIN FUNCTION #####
