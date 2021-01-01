# A program to download all undergraduate resources from the Oxford archives
# The files will be downloaded in numbered zip files which must then be extracted
# Also requires lxml to be installed despite it not being imported
from bs4 import BeautifulSoup
import requests

# Root: https://courses.maths.ox.ac.uk/

# url to scrape from
target_url = 'https://courses.maths.ox.ac.uk/overview/undergraduate'


# function to get href from all <a> elements on page with given url
def get_links(url):
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')  # requires lxml module

    links = []
    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is not None:
            links.append(link_url + '\n')  # link formatting

    return links


result = get_links(target_url)
filtered = []

# filter for links containing 'node' (i.e. the ones containing resources and filtering out other linked websites)
for i in result:
    if 'node' in i:
        filtered.append(i[:-1])

# list of links to course materials pages
course_materials = []
for i in filtered:
    course_materials.append('https://courses.maths.ox.ac.uk' + i + '/materials')

# go through each course_materials link
for i in course_materials:
    # get links on course materials page
    cm_links = get_links(i)
    # get all links with 'download' in them
    download = []
    for j in cm_links:
        if 'download' in j:
            download.append('https://courses.maths.ox.ac.uk' + j[:-1])
    for j in download:
        r = requests.get(j)
        with open(j[-5:] + '.zip', 'wb') as f:  # download the files
            f.write(r.content)
