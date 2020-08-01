from bs4 import BeautifulSoup
from requests import get
import json
from DataFormatting.FormatText import FormatSentence
from DataFormatting import VenueClass

allVenues = []  # Array to store all Venues of type VenueClass


def extractVenue(tag, venue):

    print("--Huone--")

    # extract link into the venue
    venue_link = venue.find_all('a')[0]['href']
    response = get(venue_link)
    indiv_venue = BeautifulSoup(response.text, 'html.parser')

    # extract title
    title_html = indiv_venue.find('div', class_='space-title').find('h1')
    title = ''
    if title_html:
        title = "HUONE | " + title_html.text.strip()

    # if venue already exist in the array, just add the tag, no need add a new venue
    for venue in allVenues:
        if venue['title'] == title:
            venue['tags'].append(tag)
            return

    # location - fixed
    location = 'HUONE Clarke Quay, 3D River Valley Road, #03-01, Clarke Quay, Singapore 179023'

    # extract capacity
    cap_html = indiv_venue.find('p', class_='persons-count')
    capacity = ''
    if cap_html:
        capacity = cap_html.text.split(' ')[3].strip()

    # extract description
    desc_html = indiv_venue.find_all('div', class_='lead')[0]
    desc = ''
    if desc_html:
        desc = desc_html.text.strip() + '.'

    # extract image links
    venue_images = str(indiv_venue.find(
        'div', class_='image-lift three-images'))
    images = extract_huone_image_links(venue_images)

    # extract facilities
    facs = indiv_venue.find('div', class_='amenities block')
    facilities = []
    for fac in facs.find_all('li'):
        facilities.append(fac.text.strip())

    # extract price
    price_html = facs.find('p')
    price = ''
    if price_html:
        price = [{
            "dayOfWeek": "Inquire for day availabilities",
            "time": "Inquire for timing availabilities",
            "pricing": FormatSentence(price_html.text.strip())
        }]

    # no ratings, promos
    ratings = 0
    tags = [tag]

    # create Venue Class with all inputs
    singleVenue = VenueClass.Venue(
        ratings, venue_link, images, title, location, tags, price, int(capacity), desc, facilities)

    # add this venue to the Venue Class array
    allVenues.append(singleVenue.getVenue())

# function to extract the 3 image links on the individual venue site


def extract_huone_image_links(html_string):
    links = []
    # first link
    links.append('https://huone.events' +
                 str(html_string[html_string.find("url(")+4:html_string.find(")")]))
    # second link
    links.append('https://huone.events' + str(html_string[html_string.find(
        "url(", html_string.find("url(") + 1)+4:html_string.find(")", html_string.find(")") + 1)]))
    # third link
    links.append('https://huone.events' + str(html_string[html_string.find("url(", html_string.find(
        "url(", html_string.find("url(") + 1) + 1)+4:html_string.find(")", html_string.find(")", html_string.find(")") + 1) + 1)]))
    return links


##### MAIN FUNCTION #####
tags = ['meeting-rooms', 'conference-and-seminar-rooms',
        'training-rooms', 'function-rooms']

for tag in tags:

    # Request html from website
    url = 'https://www.huone.events/sg/rooms/{}/'.format(tag)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    venues = html_soup.find_all('div', class_='room col-6 col-md-4 col-lg-3')

    # extract venue info for all venues on this page
    for venue in venues:
        extractVenue(tag, venue)

# write all data into a json file
with open('Data/Huone.json', 'w', encoding='utf-8') as outfile:
    json.dump(allVenues, outfile, ensure_ascii=False)

##### END OF MAIN FUNCTION #####
