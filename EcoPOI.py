from API_KEY import api_key
from geopy.distance import great_circle
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import openai
import overpy
import requests


def get_location_by_ip():
    """
    Purpose: This function retrieves the location of the user by their
    IP address using the ip-api.com API and the Nominatim API.

    Input: N/A

    Output: Returns the location of the user as a Nominatim object.
    """

    try:
        ip = requests.get('https://api.ipify.org?format=json').json()['ip']
        print(f"\nIP address: {ip}")

        coords = requests.get(f'http://ip-api.com/json/{ip}').json()
        lat, lon = coords['lat'], coords['lon']
        print(f"\nCoordinates: {lat}, {lon}")

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(f"{lat}, {lon}")

        return location
    except GeocoderTimedOut:
        return get_location_by_ip()
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_manual_location():
    """
    Purpose: This function prompts the user to manually enter their location and retrieves it using the Nominatim API.

    Input: An address or location.

    Output: Returns the location of the user as a Nominatim object.
    """

    print("""
    Here are some examples of how you can enter your location:

        Standard address: 123 State St, Ann Arbor, MI 48104
        Street name and city: State Street, Ann Arbor
        City and state: Ann Arbor, MI
        City only : Ann Arbor
        County and state: Washtenaw County, MI
        City and country: Ann Arbor, USA
        Country: USA

    Many other variations will work as well, as you can be as specific or ambiguous as you want.
    Keep in mind that less specific addresses may result in less accurate locations.

    It should work on any location worldwide.
    """)
    address = input("\nPlease enter your address: ")
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(address)
        if location:
            return location
        else:
            print("Unable to find the entered address. Please try again.")
            return get_manual_location()
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_user_choice():
    """
    Purpose: This function prompts the user to choose between automatically detecting their location using their IP address or manually entering their location.

    Input: binary (1 or 2)

    Output: Returns the location of the user as a Nominatim object.
    """

    print("\n\n1. Automatically detect location (using IP address)\n")
    print("2. Manually enter location\n")
    choice = input("How would you like to input your location (1 or 2): ")

    if choice == "1":
        return get_location_by_ip()
    elif choice == "2":
        return get_manual_location()
    else:
        print("Invalid option. Please try again.")
        return get_user_choice()


def generate_content(prompt, api_key):
    """
    Purpose: This function generates content using the OpenAI API.

    Input:
        prompt: A string containing the prompt to generate the content from.
        api_key: A string containing the API key for the OpenAI API.

    Output: Returns the generated content as a string.
    """

    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message


def ask_to_print(content_name, content):
    """
    Purpose: This function prompts the user if they want to print the content.

    Input:
        content_name: A string containing the name of the content.
        content: A string containing the content to be printed.

    Output: Prints the content if the user chooses to do so.
    """

    user_input = input(f"\nDo you want to print the {content_name}? (yes/no): ").lower()

    if user_input == "yes" or user_input == '':
        print(f"\n{content_name}:\n{content}")
    elif user_input == "no":
        pass
    else:
        print("\nInvalid option. Please try again.")
        ask_to_print(content_name, content)


def group_nearby_locations(points_of_interest, distance_threshold=50):
    """
    Purpose: This function groups nearby locations based on their coordinates and returns the location with the most tags, which is considered the most representative of the group.

    Input:
        points_of_interest: A list of dictionaries containing the points of interest to group.
        distance_threshold: A float representing the maximum distance between two points of interest for them to be considered in the same group. The default value is 50.

    Output: Returns a list of dictionaries containing the most representative points of interest for each group.
    """

    clusters = []

    for poi in points_of_interest:
        added_to_cluster = False
        for cluster in clusters:
            if any(great_circle((poi['lat'], poi['lon']), (point['lat'], point['lon'])).meters <= distance_threshold for point in cluster):
                cluster.append(poi)
                added_to_cluster = True
                break

        if not added_to_cluster:
            clusters.append([poi])

    seen = set()
    filtered_clusters = []
    for cluster in clusters:
        max_poi = max(cluster, key=lambda x: (len(x['tags']), x['tags'].get('name', '')))
        name = max_poi['tags'].get('name', None)
        if name and name not in seen:
            filtered_clusters.append(max_poi)
            seen.add(name)

    return filtered_clusters


nature_tags = [
        'leisure=park',
        'natural=wood',
        'landuse=forest',
        'landuse=meadow',
        'landuse=recreation_ground',
        'landuse=winter_sports',
        'leisure=beach_resort',
        'leisure=bandstand',
        'leisure=bird_hide',
        'leisure=disc_golf_course',
        'leisure=dog_park',
        'leisure=firepit',
        'leisure=fishing',
        'leisure=garden',
        'leisure=horse_riding',
        'leisure=nature_reserve',
        'leisure=park',
        'leisure=playground',
        'leisure=swimming_area',
        'man_made=lighthouse',
        'man_made=pier',
        'natural=fell',
        'natural=grassland',
        'natural=heath',
        'natural=scrub',
        'natural=beach',
        'natural=coastline',
        'natural=geyser',
        'natural=glacier',
        'natural=hot_spring',
        'natural=reef',
        'natural=spring',
        'natural=wetland',
        'natural=arch',
        'natural=cave_entrance',
        'natural=cliff',
        'natural=dune',
        'natural=hill',
        'natural=ridge',
        'natural=rock',
        'natural=volcano',
        'tourism=camp_pitch',
        'tourism=camp_site',
        'tourism=picnic_site',
        'tourism=viewpoint',
        'boundary=national_park',
        'water=river',
        'water=lake',
        'water=reservoir',
        'water=pond',
        'water=stream_pool',
        'waterway=river',
        'waterway=riverbank',
        'waterway=stream',
        'waterway=tidal_channel',
        'waterway=waterfall',
        'amenity=ranger_station',
        'amenity=dive_centre',
        'amenity=hunting_stand',
        'boundary=forest',
        'boundary=national_park',
        'boundary=protected_area'
    ]


def get_poi_category(tags):
    """
    Purpose: This function returns the category of a point of interest based on its tags.

    Input:
        tags: A list of strings containing the tags of the point of interest.

    Output: Returns a string containing the category of the point of interest.
    """

    category_mapping = {
        'leisure=park': 'Park',
        'natural=wood': 'Wood',
        'landuse=forest': 'Forest',
        'landuse=meadow': 'Meadow',
        'landuse=recreation_ground': 'Recreation Ground',
        'landuse=winter_sports': 'Winter Sports Location',
        'leisure=beach_resort': 'Beach Resort',
        'leisure=bandstand': 'Bandstand',
        'leisure=bird_hide': 'Bird Hide',
        'leisure=disc_golf_course': 'Disc Golf Course',
        'leisure=dog_park': 'Dog Park',
        'leisure=firepit': 'Firepit',
        'leisure=fishing': 'Fishing Spot',
        'leisure=garden': 'Garden',
        'leisure=horse_riding': 'Horse Riding Location',
        'leisure=nature_reserve': 'Nature Reserve',
        'leisure=park': 'Park',
        'leisure=playground': 'Playground',
        'leisure=swimming_area': 'Swimming Area',
        'man_made=lighthouse': 'Lighthouse',
        'man_made=pier': 'Pier',
        'natural=fell': 'Fell',
        'natural=grassland': 'Grassland',
        'natural=heath': 'Heath',
        'natural=scrub': 'Scrub',
        'natural=beach': 'Beach',
        'natural=coastline': 'Coastline',
        'natural=geyser': 'Geyser',
        'natural=glacier': 'Glacier',
        'natural=hot_spring': 'Hot Spring',
        'natural=reef': 'Reef',
        'natural=spring': 'Spring',
        'natural=wetland': 'Wetland',
        'natural=arch': 'Natural Arch',
        'natural=cave_entrance': 'Cave',
        'natural=cliff': 'Cliff',
        'natural=dune': 'Dune',
        'natural=hill': 'Hill',
        'natural=ridge': 'Ridge',
        'natural=rock': 'Rock',
        'natural=volcano': 'Volcano',
        'tourism=camp_pitch': 'Camp Pitch',
        'tourism=camp_site': 'Campsite',
        'tourism=picnic_site': 'Picnic Site',
        'tourism=viewpoint': 'Viewpoint',
        'water=river': 'River',
        'water=lake': 'Lake',
        'water=reservoir': 'Reservoir',
        'water=pond': 'Pond',
        'water=stream_pool': 'Stream Pool',
        'waterway=river': 'River',
        'waterway=riverbank': 'Riverbank',
        'waterway=stream': 'Stream',
        'waterway=tidal_channel': 'Tidal Channel',
        'waterway=waterfall': 'Waterfall',
        'amenity=ranger_station': 'Ranger Station',
        'amenity=dive_centre': 'Dive Center',
        'amenity=hunting_stand': 'Hunting Stand',
        'boundary=forest': 'Forest',
        'boundary=national_park': 'National Park',
        'boundary=protected_area': 'Protected Area'
    }

    for tag_key in category_mapping:
        if any(tag_key in tag for tag in tags):
            return category_mapping[tag_key]


def get_user_preferred_radius():
    """
    Purpose: This function prompts the user to enter the preferred radius of their search.

    Input: The user's preferred radius of the POI search in meters.

    Output: Returns a float representing the preferred radius of the search.
    """

    try:
        radius_input = input("\n\nPlease enter the preferred radius of your search in meters (e.g, 1000)\nor press 'Enter' to use the default value of 1609 meters (appr. 1 mi): ")
        if radius_input == "":
            return 1609
        else:
            radius = float(radius_input)
            return radius
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
        return get_user_preferred_radius()


def get_points_of_interest(lat, lon, radius):
    """
    Purpose: This function retrieves the points of interest within a certain radius from a given location using the Overpass API.

    Input:
        lat: A float representing the latitude of the location.
        lon: A float representing the longitude of the location.
        radius: A float representing the radius of the search in meters.

    Output: Returns a list of dictionaries containing the points of interest found.
    """

    api = overpy.Overpass()

    tag_query = ";".join([f'node[{tag}](around:{radius},{lat},{lon})' for tag in nature_tags]) + ";"
    tag_query += ";".join([f'way[{tag}](around:{radius},{lat},{lon})' for tag in nature_tags]) + ";"
    tag_query += ";".join([f'relation[{tag}](around:{radius},{lat},{lon})' for tag in nature_tags]) + ";"

    query = f"""
    [out:json];
    (
      {tag_query}
    );
    out center;
    """
    try:
        result = api.query(query)
        points_of_interest = []
        unique_locations = set()

        for node in result.nodes:
            if 'name' in node.tags and (node.lat, node.lon) not in unique_locations:
                points_of_interest.append({"id": node.id, "lat": node.lat, "lon": node.lon, "tags": node.tags})
                unique_locations.add((node.lat, node.lon))

        for way in result.ways:
            if 'name' in way.tags and (way.center_lat, way.center_lon) not in unique_locations:
                points_of_interest.append({"id": way.id, "lat": way.center_lat, "lon": way.center_lon, "tags": way.tags})
                unique_locations.add((way.center_lat, way.center_lon))

        for rel in result.relations:
            if 'name' in rel.tags and (rel.center_lat, rel.center_lon) not in unique_locations:
                points_of_interest.append({"id": rel.id, "lat": rel.center_lat, "lon": rel.center_lon, "tags": rel.tags})
                unique_locations.add((rel.center_lat, rel.center_lon))
        if not points_of_interest:
            print(f"\n\nNo points of interest found within the specified radius. You might want to expand the radius to find more results.\n")

        return points_of_interest
    except Exception as e:
        print(f"\nError: {e}")
        return []


if __name__ == "__main__":
    print("\n\nWelcome to EcoPOI!\n\nEcoPOI uses a location provided by you to gather information pertaining to that location's local flora, fauna, and ecosystem in general.\nIt also gathers information on nearby 'nature locations', which range from dog parks to streams to volcanoes!\n\nPlease follow the instructions below to learn more about your local environment!")
    location = get_user_choice()

    if location:
        print(f"\nLocation: {location.address}")
    else:
        print("\nUnable to retrieve location.")

    api_key = api_key ### YOU CAN ENTER YOUR OWN OPENAI GPT-4 API KEY HERE ###

    prompt1 = f"""Please provide a NUMBERED list of the 10 most common types of local flora in {location}, 
    with a total character limit of 2048 to ensure that the response does not cut off in the middle of a sentence. 
    After each name of a flora, in parantheses, please specify what it is (Ex. Sugar maple (tree)). 
    The list must include more than just trees. At least one thing in the list must be something other than a tree.
    Ex.:
    1. American Beech (tree)
    2. Blackgum (tree)
    3. Speckled Alder (shrub)
    4. Moonseed (vine)
    5. Boneset (perennial)
    6. Royal Fern (fern)
    7. Wool-grass (grass)
    (Do not use things from this example list unless they are actually common at the location)
    """
    content1 = generate_content(prompt1, api_key)
    prompt2 = f"""Please provide a NUMBERED list of the 10 most common types of local fauna in {location}, 
    with a total character limit of 2048 to ensure that the response does not cut off in the middle of a sentence. 
    Ex.:
    1. Pileated Woodpecker
    2. American Badger
    3. American Red Squirrel
    (Do not use things from this example list unless they are actually common at the location)
    """
    content2 = generate_content(prompt2, api_key)
    prompt3 = f"""Please provide a description of {location}'s natural environment. What type of biomes are there?
    Use a total character limit of 2048 to ensure that the response does not cut off in the middle of a sentence.
    PLEASE DO NOT REPEAT THE FULL NAME OF THE LOCATION, USE A SHORTENED NAME (such as city name).
    (ex. Instead of '6810, Gulf Freeway, Houston, Harris County, Texas, United States', just say the city name,
    so in this example, just say 'Houston')
    """
    content3 = generate_content(prompt3, api_key)
    print("\nIf you click 'Enter' for the following questions, it will answer as 'yes':")
    ask_to_print("Local Flora", content1)
    ask_to_print("Local Fauna", content2)
    ask_to_print("Local Environment", content3)

    outer_loop = True
    while outer_loop:
        radius = get_user_preferred_radius()
        points_of_interest = get_points_of_interest(location.latitude, location.longitude, radius)
        filtered_points_of_interest = group_nearby_locations(points_of_interest)
        sorted_points_of_interest = sorted(filtered_points_of_interest, key=lambda poi: poi['tags'].get('name', 'Unnamed'))

        if sorted_points_of_interest:
            print("\nPoints of Interest:")
            for poi in sorted_points_of_interest:
                name = poi['tags'].get('name', 'Unnamed')
                category = get_poi_category(poi['tags'])
                print(f"\n- {name} ({category})")
                print(f"Tags: {poi['tags']}")

        while True:
            repeat_search = input("\nDo you want to search with another radius (yes/no): ").lower()
            if repeat_search == "no":
                print("\n\n\nThanks for visiting EcoPOI!\n\nPlease try to leave the Earth better than you found it!\n")
                outer_loop = False
                break
            elif repeat_search == "yes" or repeat_search == '':
                break
            else:
                print("Invalid input. Please enter 'yes' (or just click 'Enter') or 'no'.")
