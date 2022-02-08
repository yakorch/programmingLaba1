"""A module that creates html file - a map with closest locations where movies
were filmed when year, coordinates and path to a file given"""
import argparse
from functools import lru_cache
from geopy import distance
from geopy.geocoders import Nominatim, ArcGIS
import folium


def distance_two_points(p1: tuple, p2: tuple):
    """
    Returns a distance between two points on the globe in km.
    Args:
        p1 (tuple): a first position (coords)
        p2 (tuple): a second position (coords)
    Returns:
        float: distance
    >>> distance_two_points((20, 20), (30, 30))
    1497.1489241504328
    """
    return distance.distance(p1, p2).km


arcgis = ArcGIS(timeout=10)
nominatim = Nominatim(timeout=10, user_agent="notme")
geocoders = [arcgis, nominatim]


@lru_cache(maxsize=None)
def geocode(address: str):
    """
    Returns a tuple of latitude and longtitude of an address
    Args:
        address (str): an address of a location
    Returns:
        tuple: tuple of float numbers
    >>> geocode("New York, USA")
    (40.71455000000003, -74.00713999999994)
    """
    i = 0
    try:
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude, location.address
        i += 1
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude, location.address
    except:
        return None


def get_movies(filename):
    """
    Returns a list of raws from a file 'filename'
    Args:
        filename (str): a path to a file
    Returns:
        a list of lines (strings)
    >>> get_movies("movieshere")[0][:11]
    '"#1 Single"'
    """
    with open(filename, mode="r", encoding="utf-8") as file:
        content = file.readlines()
    return list(map(lambda x: x.rstrip(), content))


def filter_movies(year: int, movies: list):
    """
    Returns movies that were filmed in 'year'.
    Args:
        year (int): a year to be filtered by
        movies (list): a list of raws
    Returns:
        a list of lines (strings)
    >>> filter_movies(1969, get_movies("movieshere"))[0][:19]
    '"60 Minutes" (1968)'
    """
    return list(filter(lambda x: str(year) in x, movies))


def name_finder(line: str):
    """
    Returns a name of the film from a line
    >>> name_finder('"Name of the film" (2022) Location, Country')
    'Name of the film'
    """
    if line.count('"') == 2:
        return line[1:line[1:].find('"') + 1]
    elif line.count('"') == 4:
        return line[1:line[1:].find('"') + 1]


def new_loc_finder(line: str):
    """
    Returns a location of a film from a line
    >>> new_loc_finder('New York, USA')
    'New York, USA'
    """
    line = line.split("\t")
    while line[-1].startswith("(") and line[-1].endswith(")"):
        line = line[:-1]
    return line[-1]


def create_pairs(movies):
    """
    Creates a list of pairs (movie_name, location)
    >>> create_pairs(get_movies("movieshere"))[100]
    ('#VanLifeAttila', 'Barkerville, British Columbia, Canada')
    """
    res = []
    for line in movies:
        name = name_finder(line)
        location = new_loc_finder(line)
        res.append((name, location))
    return res


def get_coords_from_pairs(movies: list):
    """
    Returns a differed list of tuples where second element - location
    is substituted with its coordinates on the globe
    >>> get_coords_from_pairs(create_pairs(get_movies("movieshere"))[100:102])[0]
    ('#VanLifeAttila', (53.06746000000004, -121.51612999999998))
    """
    return [(el[0], geocode(el[1])) for el in movies]


def calc_closest_dist(movies: list, my_pos: tuple):
    """
    Retunrs a sorted list of tuples (movie_name, movie_location)
    by closest location to 'my_pos'
    >>> calc_closest_dist(get_coords_from_pairs(create_pairs(get_movies("movieshere"))[100:102]), (43, -120))[0]
    ('#VanLifeAttila', (49.260380000000055, -123.11335999999994))
    """
    return sorted(movies,
                  key=lambda x: distance_two_points(
                      (x[1][0], x[1][1]), my_pos))


def create_html(movies: list, my_pos: tuple, year: int, far_movies: list,
                all_m: list):
    """
    Creates html file - a web map with 3 extra layers:
        first layer - all films from a year 'year'
        second layer - 10 closest filming locations from a year 'year'
        third layer - 10 furthest filming locations from a year 'year'
    Returns 'None'. All markers are distinguished by color. LayerControl added.
    """
    map = folium.Map(location=[my_pos[0], my_pos[1]], zoom_start=4)
    html = """
    Film name:<br>
    {}<br>
    Coordinates:<br>
    latitude: {}<br>
    longtitude: {}<br>
    Place:<br>
    {}
    """
    fg = folium.FeatureGroup(name=f"All filming locations in {year}")
    for pair in all_m:
        html_format = html.format(pair[0], round(pair[1][0], 3),
                                  round(pair[1][1], 3), pair[1][2])
        iframe = folium.IFrame(html=html_format, width=200, height=150)
        fg.add_child(
            folium.Marker(location=[pair[1][0], pair[1][1]],
                          popup=folium.Popup(iframe),
                          icon=folium.Icon(color='darkblue')))
    map.add_child(fg)
    fg = folium.FeatureGroup(name=f"Closest filming locations in {year}")
    for pair in movies:
        html_format = html.format(pair[0], round(pair[1][0], 3),
                                  round(pair[1][1], 3), pair[1][2])
        iframe = folium.IFrame(html=html_format, width=200, height=150)
        fg.add_child(
            folium.Marker(location=[pair[1][0], pair[1][1]],
                          popup=folium.Popup(iframe),
                          icon=folium.Icon(color='darkpurple')))
    map.add_child(fg)
    fg = folium.FeatureGroup(name=f"Furthermost filming locations in {year}")
    for pair in far_movies:
        html_format = html.format(pair[0], round(pair[1][0], 3),
                                  round(pair[1][1], 3), pair[1][2])
        iframe = folium.IFrame(html=html_format, width=200, height=150)
        fg.add_child(
            folium.Marker(location=[pair[1][0], pair[1][1]],
                          popup=folium.Popup(iframe),
                          icon=folium.Icon(color='red')))
    map.add_child(fg)
    map.add_child(folium.LayerControl())
    map.save('filmsmap.html')


if __name__ == "__main__":
    # parsing argumnets
    parser = argparse.ArgumentParser()
    parser.add_argument("year",
                        type=int,
                        help='a year of films to be displayed')
    parser.add_argument("lat", type=float, help='a latitude')
    parser.add_argument("lon", type=float, help='a longitude')
    parser.add_argument('path_to_dataset', type=str, help='a path to a file')
    args = parser.parse_args()
    year = args.year
    lat = args.lat
    lon = args.lon
    my_pos = (lat, lon)
    filename = args.path_to_dataset
    # main part. processing movies and sorting them
    movies = get_movies(filename)
    movies = filter_movies(year, movies)
    movies = create_pairs(movies)
    movies = get_coords_from_pairs(movies)
    movies = list(filter(lambda x: x[1] is not None, movies))
    movies = calc_closest_dist(movies, my_pos)
    if len(movies) > 10:
        sorted_movies = movies[:10]
        the_farest_movies = movies[-10:]
    else:
        sorted_movies = movies
        the_farest_movies = movies
    # creating an hmtl file and that's it
    create_html(sorted_movies, my_pos, year, the_farest_movies, movies)
