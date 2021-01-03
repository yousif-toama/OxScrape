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
    return [x.get('href') + '\n' for x in soup.find_all('a') if x.get('href') is not None]


result = get_links(target_url)
# filter for links containing 'node' (i.e. the ones containing resources and filtering out other linked websites)
filtered = [i[:-1] for i in result if 'node' in i]

# list of links to course materials pages (turns paths into links)
course_materials = ['https://courses.maths.ox.ac.uk' + i + '/materials' for i in filtered]

# go through each course_materials link
for i in course_materials:
    cm_links = get_links(i)  # get links on course materials page
    # get all links with 'download' in them
    download = ['https://courses.maths.ox.ac.uk' + j[:-1] for j in cm_links if 'download' in j]
    for j in download:
        r = requests.get(j)
        with open(j[-5:] + '.zip', 'wb') as f:  # download the files
            f.write(r.content)
