from bs4 import BeautifulSoup
from requests import get
import VenueClass
import json
import os

allVenues = []  # Array to store all Venues of type VenueClass

def extractVenue(venue):

    # extract title
    title_html = venue.find('div', class_='event-name')
    title = ''
    if title_html:
        title = title_html.text

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
        image = 'venuexplorer.com.sg' + str(venue_image['href'])
        images.append(image)

    # extract starting price - same for all rooms within this venue
    price_html = indiv_venue.find_all('div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[1]
    price = ''
    if price_html:
        price = price_html.text.strip()

    # extract general capacity
    capacity_html = indiv_venue.find_all('div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[2]
    capacity = ''
    if capacity_html:
        capacity = capacity_html.text.split(' ')[0].strip()

    # extract the different rooms and their capacity in this venue
    rooms_html = indiv_venue.find_all('ul', class_='space')
    rooms = []
    if rooms_html and len(rooms_html) > 1:
        for index, room in enumerate(rooms_html[1].find_all('li')):
            if room:
                tokens = room.text.split(' ')
                room_name = tokens[3].strip()
                room_cap = tokens[0].strip()
                rooms.append({
                    "room" : room_name,
                    "capacity" : room_cap
                })

    # for room_html in rooms_html.find_all('li'):
    #     if room_html:
    #         texts = room_html.text.split(' ')
    #         capacity = texts[0].strip() # but this one sometimes is empty. might need to take the above capacity and take it
    #     # as a general capacity across all events
    #         roomName = texts[3].strip()
    #         roomNames.append(roomName)
    #     else:
    #         capacity = indiv_venue.find_all('div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[2].text.split(' ')[0].strip()
    #         break

    # extract location
    location_html = indiv_venue.find_all('div', class_='col-lg-3 col-md-3 col-sm-3 text-center')[3]
    location = ''
    if location_html:
        location = location_html.text.strip()

    # extract facilities
    facs = indiv_venue.find('ul', class_='feature')
    facilities = []
    for fac in facs.find_all('li'):
        facilities.append(fac.text.strip())

    # extract description
    desc_html = indiv_venue.find('div', class_='quick-enquiry').p
    desc = ''
    if desc_html:
        desc = desc_html.text.strip()
    
    # no ratings, promos
    ratings = ''
    promos = ''

    # create Venue Class with all inputs
    singleVenue = VenueClass.Venue(
        ratings, venue_link, images, title, location, tags, price, capacity, desc, facilities, rooms, promos)

    # add this venue to the Venue Class array
    if(not singleVenue in allVenues):
        allVenues.append(singleVenue.getVenue())


##### MAIN FUNCTION #####
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
        extractVenue(venue)

    # Increase counter to go next page
    currentPage += 1

# write all data into a json file
os.chdir(r'../Data/')
with open('venuExplorer.json', 'w') as outfile:
    json.dump(allVenues, outfile)

##### END OF MAIN FUNCTION #####