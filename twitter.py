'''
Lab 2, Task 3. Archakov Vsevolod.
'''
import requests
import folium
import geopy
from geopy.exc import GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
import random


def twitter_get_friends_json(nickname: str, token: str) -> dict:
    """
    Get json with friends by username from twitter.
    """
    reqest_url = "https://api.twitter.com/1.1/friends/list.json"

    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    params = {
        'screen_name': f'@{nickname}',
        'count': 30
    }

    response = requests.get(
        reqest_url, headers=headers, params=params)

    return response.json()['users']


def generate_friends_data(friends_dict: dict) -> list:
    '''
    Get dictionary with info about friends from twitter, geocode their coordinates,
    and return tuple with them and nickname.
    '''
    geolocator = geopy.Nominatim(user_agent='my-aplication')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    result = []
    used_locations = []

    for user in friends_dict:
        try:
            location = geolocator.geocode(user['location'])
            coordinates = [location.latitude, location.longitude]

            if coordinates in used_locations:
                coordinates[0] += random.randrange(1, 2) / 10000
                coordinates[1] += random.randrange(1, 2) / 10000

            used_locations.append(coordinates)
            result.append(
                (user['screen_name'], coordinates[0], coordinates[1]))

        except:
            continue

    return result


def generate_map(map_info: list):
    '''
    Generate map with all info about users.
    '''
    twitter_map = folium.Map()
    friends = folium.FeatureGroup(name='twitter friends')

    for user in map_info:
        friends.add_child(folium.Marker(
            location=[user[1], user[2]], popup=user[0]))

    twitter_map.add_child(friends)
    twitter_map.save('templates/twitter_map.html')
