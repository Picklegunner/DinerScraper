from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
from entry import *

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

#TODO create update_database that skims all available recipes and adds to sql database
def scrape_recipe(url, name):

    # Get html
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, "html.parser")
    font_elements = html.select('font')

    scraped_entry = Entry()

    # Individually scrape important elements
    two_liners = ("Serving Size", "Total Fat", "Tot. Carb.", "Sat. Fat", "Dietary Fiber", "Trans Fat", "Sugars", "Cholesterol", "Protein", "Sodium")
    calories_fat_re = re.compile(r'Calories from Fat.?(\d+)')
    calories_re = re.compile(r'Calories.?(\d+)') # .? is bad but spaces won't match with \s for some reason

    for i, font_element in enumerate(font_elements):

        # Match regexs
        cal_search = calories_re.search(font_elements[i].text)
        cal_fat_search = calories_fat_re.search(font_elements[i].text)
        stripped_element = font_element.text.strip()

        if stripped_element in two_liners and font_elements[i + 1].text.strip() != "":
            if stripped_element == "Serving Size":
                pass
            elif stripped_element == "Total Fat":
                scraped_entry.total_fat = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Tot. Carb.":
                scraped_entry.total_carb = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Sat. Fat":
                scraped_entry.sat_fat = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Dietary Fiber":
                scraped_entry.fiber = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Trans Fat":
                scraped_entry.trans_fat = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Sugars":
                scraped_entry.sugar = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Cholesterol":
                scraped_entry.cholesterol = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'mg')
            elif stripped_element == "Protein":
                scraped_entry.protein = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'g')
            elif stripped_element == "Sodium":
                scraped_entry.sodium = Nutrient(re.sub('[^0-9\\.]','', font_elements[i + 1].text.strip()), 'mg')
        elif cal_fat_search: # Calories from Fat
            scraped_entry.calories_from_fat = cal_fat_search.group(1)
        elif cal_search: # Calories
            scraped_entry.calories = cal_search.group(1)

        scraped_entry.name = name

    return scraped_entry


def log_error(e):
    #Sometime save this to a log file
    print(e)

def gather_links(url):

        # Get html
    #raw_html = simple_get(url)
    html = BeautifulSoup(open(url), "html.parser") # TODO THIS NEEDS TO BE CHANGED FOR ONLINE HTML - REMOVE OPEN

    links = []

    for link in html.find_all('a', href=True):
        if("http://nutrition.umd.edu/label.aspx?" in link['href']):
            links.append(link)

    return links

def scrape_menu(url):

    food_links = gather_links("This Week's Menus.htm") # TODO this function needs to gather menus by itself

    for link in food_links:
        print(scrape_recipe(link['href'], link.text)) # TODO add to data structure




#scrape_recipe("http://nutrition.umd.edu/label.aspx?locationNum=16&locationName=%3cfont+style%3d%22color%3aRed%22%3eSouth+Campus%3c%2ffont%3e&dtdate=05%2f04%2f2018&RecNumAndPort=119369*1")

scrape_menu("This Week's Menus.htm")