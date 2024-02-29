from bs4 import BeautifulSoup
import requests
import pandas as pd

total_page_num = 143
page_num = 0

PRICES = []
LOCATION = []
BEDS = []
BATHS = []
TOILETS = []


def split_rooms(array, array_child):
    """ A function that splits texts from number of rooms e.g Baths, Bed, Toilet"""
    try:
        new_number = array_child.text.split()  # e.g "2 Toilets" becomes ["2", "Toilets"]
        array.append(int(new_number[0]))  # Converts the first position to an integer
    except ValueError:
        array.append(float("nan"))  # If the value is not a number.
    return array


while page_num < total_page_num:
    parameters = None
    if page_num > 0:
        parameters = {
            "page": page_num
        }
    URL = "https://www.propertypro.ng/property-for-rent/flat-apartment/in/lagos"
    data = requests.get(URL, params=parameters).text
    soup = BeautifulSoup(data, "html.parser")
    page_num += 1

    # SPONSORED PROPERTIES

    sponsored_property_price = soup.select_one(selector=".single-room-sale .single-room-text .n50 h3").text
    new_price = sponsored_property_price.split("/")
    PRICES.append(new_price[0].strip())

    sponsored_property_location = soup.select_one(selector=".single-room-sale .single-room-text > h4").text
    LOCATION.append(sponsored_property_location)

    sponsored_property_bed = soup.select_one(selector=".single-room-sale .single-room-text .fur-areea span:first-child")
    split_rooms(BEDS, sponsored_property_bed)

    sponsored_property_baths = soup.select_one(selector=".single-room-sale .single-room-text .fur-areea "
                                                        "span:nth-child(2)")
    split_rooms(BATHS, sponsored_property_baths)

    sponsored_property_toilets = soup.select_one(selector=".single-room-sale .single-room-text .fur-areea "
                                                          "span:nth-child(2)")
    split_rooms(TOILETS, sponsored_property_toilets)

    # OTHER PROPERTIES
    next_sibling = soup.find(attrs={"itemtype" : "https://schema.org/ItemList"})

    prices_markup = next_sibling.select(".single-room-text .n50 h3")
    for price in prices_markup:
        new_price = price.text.split("/")
        PRICES.append(new_price[0].strip())

    property_location_markup = next_sibling.select(".single-room-text > h4")
    for location in property_location_markup:
        LOCATION.append(location.text)

    bed_markup = next_sibling.select(".single-room-text .fur-areea span:first-child")
    for bed in bed_markup:
        split_rooms(BEDS, bed)

    baths_markup = next_sibling.select(".single-room-text .fur-areea span:nth-child(2)")
    for bath in baths_markup:
        split_rooms(BATHS, bath)

    toilets_markup = next_sibling.select(".single-room-text .fur-areea span:nth-child(3)")
    for toilet in toilets_markup:
        split_rooms(TOILETS, toilet)


housing_data = {
    "Location": LOCATION,
    "Prices_per_year (₦ or $)": PRICES,
    "Bedrooms": BEDS,
    "Baths": BATHS,
    "Toilets": TOILETS
}

# NOTE: There are dollars data in here
df_housing_data = pd.DataFrame(data=housing_data)
df_housing_data.to_csv("Apartments_for_rent_Lagos.csv", sep=',', encoding='utf-8', index=False)


# df_new = pd.read_csv("./Apartments_for_rent_Lagos.csv")
#
# print(df_new)

