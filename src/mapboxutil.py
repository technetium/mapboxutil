"""
Utilities for MapBox
especially to create static choropleth map images.
"""
import hashlib
import json
import math
import requests
#from pprint import pprint


_MAPBOX_PUBLIC_KEY = 'pk.Use set_mapbox_token to set the public key' # aRandomString0f5ixtySevenUpperAndL0werCaseCharactersAndNumb3rsPo1nt.andThenYet1other22M0re
_MAPBOX_SECRET_KEY = 'sk.Use set_mapbox_token to set the secret key' # aDiff3rentStr1ngWithRand0mUpperCaseAndLowerCaseCharactersAndNumbers.0fC0urseThese1sAreFak3
DEFAULT_USERNAME = 'mapbox'

def set_mapbox_token(public_key = None, secret_key = None):
    """Set the mapbox tokens"""
    global _MAPBOX_PUBLIC_KEY, _MAPBOX_SECRET_KEY
    if secret_key: _MAPBOX_SECRET_KEY = secret_key
    if public_key: _MAPBOX_PUBLIC_KEY = public_key

def get_zoom(web_mercator, pixel):
    """Get the zoom level from size in web mercator and number of pixels."""
    return math.log(pixel * math.pi / web_mercator / 256, 2)

def latitude_to_webmercator(latitude):
    """Convert a latitude (in degrees) to web mercator."""
    return math.pi - math.log(math.tan((math.pi/2 + math.radians(latitude))/2))

def longitude_to_webmercator(longitude):
    """Convert a longitude (in degrees) to web mercator."""
    return math.radians(longitude) + math.pi

def webmercator_to_latitude(web_mercator):
    """Convert web mercator to latitude (in degrees)."""
    return math.degrees(2 * math.atan(math.exp(math.pi - web_mercator)) - math.pi/2)

def webmercator_to_longitude(web_mercator):
    """Convert web mercator to longitude (in degrees)."""
    return math.degrees(web_mercator - math.pi)

def mapbox_dimensions(south, north, west, east, width, height):
    """
    Get the parameters for a static mapbox image.

    :param south: The southern border (in degrees)
    :param north: The northern border (in degrees)
    :param west: The western border (in degrees)
    :param east: The eastern border (in degrees)
    :param width: The resulting width of the image (in pixels)
    :param height: The resulting width of the image (in pixels)
    :return: a dict with parameters for the mapbox_url function
    """
    # convert to webmercator
    south_wm = latitude_to_webmercator(south)
    north_wm = latitude_to_webmercator(north)
    west_wm = longitude_to_webmercator(west)
    east_wm = longitude_to_webmercator(east)

    # size in web mercator
    width_wm  = east_wm  - west_wm
    height_wm = south_wm - north_wm

    zoom = round(
        max(
            0, # Zoom levels cannot be negative
            min(                             # Calculate zoom levels for
                get_zoom(height_wm, height), # heigth and
                get_zoom(width_wm,  width)   # width
            )                                # and take the lowest value
        )
        , 2 # zoom levels will be rounded to two decimal places
    )
    # zoomfactor to convert web mercator to pixels
    zoom_factor = 256/math.pi * 2**zoom

    return {
        'width':  round(width_wm  * zoom_factor),
        'height': round(height_wm * zoom_factor),
        'latitude':  webmercator_to_latitude( (north_wm + south_wm) / 2),
        'longitude': webmercator_to_longitude((west_wm  + east_wm ) / 2),
        'zoom': zoom,
    }

def overlay_marker(
    latitude
    , longitude
    , color = ''
    , label = ''
    , size = 's'
):
    """
    Generate the partial url for a marker overlay
    :param latitude:    The latitude of the maker in degrees
    :param longitude:   The longitude of the marker in degrees
    :param color:       The 3- or 6-digit hexadecimal color code
    :param label:       The label, see MapBox documentation for the options.
    :param size:        The size options are 'l' (large) or 's' (small)

    :return: the url part for an marker overlay.
    """
    name = 'pin-s' if 's' == size else 'pin-l'
    if color: color = '+' + color
    if label: label = '-' + label
    return '%(name)s%(label)s%(color)s(%(longitude)s,%(latitude)s)' % locals()

def mapbox_url(
    username = 'mapbox'
    , style = 'streets-v11'
    , latitude = 0
    , longitude = 0
    , width = 512
    , height = 512
    , zoom = 0
    , overlays = []
    , access_token = None
):
    """
    Generates the url for the static mapbox image.
    :param username: The username owning the style
    :param style:           The style name to be used for the map
    :param latitude:        The latitude of the center of the map in degrees
    :param longitude:       The longitude of the center of the map in degrees
    :param width:           The width of the map in pixels
    :param height:          The height of the map in pixels
    :param zoom:            The zoom level used in the map
    :param overlays:        An array of overlays that will be added to the map
    :param access_token:    The MapBox public access token
    :return:    url to ret
    """
    if not access_token: access_token = _MAPBOX_PUBLIC_KEY
    overlay = ','.join(overlays)
    if overlay: overlay += '/'
    return 'https://api.mapbox.com/styles/v1/%(username)s/%(style)s/static/%(overlay)s%(longitude)s,%(latitude)s,%(zoom)s/%(width)dx%(height)d?access_token=%(access_token)s' % locals()


#########################
### Request Functions ###
#########################

def delete_request(url):
    """Send a delete request to the url, returns the json payload."""
    r = requests.delete(url)
    if 204 != r.status_code:
        raise Exception(r.status_code, r.text, url)
    return r.json()

def get_request(url):
    """Send a get request to the url, returns the json payload."""
    r = requests.get(url)
    if 200 != r.status_code:
        raise Exception(r.status_code, r.text, url)
    return r.json()

def patch_request(url, data):
    """Send a patch request to the url, returns the json payload."""
    r = requests.patch(url, json=data)
    if 200 != r.status_code:
        raise Exception(r.status_code, r.text, url)
    return r.json()

def post_request(url, data):
    """Send a post request to the url, returns the json payload."""
    r = requests.post(url, json=data)
    if 201 != r.status_code:
        raise Exception(r.status_code, r.text, url)
    return r.json()


###################
### Style stuff ###
###################

def get_styles(username = DEFAULT_USERNAME, draft = False):
    """Get all the styles for a specific account."""
    return get_request('https://api.mapbox.com/styles/v1/%s?access_token=%s%s' % (
        username,
        _MAPBOX_SECRET_KEY,
        '&draft' if draft else ''
    ))

def create_style(username, style = {}):
    """Create a style."""
    return post_request('https://api.mapbox.com/styles/v1/%s?access_token=%s' % (
        username,
        _MAPBOX_SECRET_KEY
    ), style)

def delete_style(username, style_id):
    """Delete a style."""
    return delete_request('https://api.mapbox.com/styles/v1/%s/%s?access_token=%s' % (
        username,
        style_id,
        _MAPBOX_SECRET_KEY,
    ))

def get_style(username, style_id):
    """Retreive a style."""
    return get_request('https://api.mapbox.com/styles/v1/%s/%s?access_token=%s' % (
        username,
        style_id,
        _MAPBOX_SECRET_KEY,
    ))

def update_style(username, style_id, style):
    """Update an existing style."""
    return patch_request('https://api.mapbox.com/styles/v1/%s/%s?access_token=%s' % (
        username,
        style_id,
        _MAPBOX_SECRET_KEY,
    ), style)

def get_style_id_by_name(name, styles = None, username = DEFAULT_USERNAME):
    """Get a style id by it's name."""
    styles = styles or get_styles(username)
    return ([x.get('id') for x in styles if name == x.get('name')] or [None])[0]

def make_style(
    name = ''
    , sources = {}
    , layers = []
    , version = 8
):
    """Make a style."""
    return {
        'draft': False,
        'name': name,
        'layers': layers,
        'metadata': {},
        'sources': sources,
        'version': version,
    }

def add_sources(source_ids, sources = None):
    """Add an array of source ids to the dict sources and return it."""
    sources = sources or {}
    url = sources.get('composite', {}).get('url', '')
    url += ',' if url else 'mapbox://'
    sources['composite'] = {
        'type': 'vector',
        'url': url + ','.join(source_ids),
    }
    return sources

def make_layer(source_layer, paint, filter = None):
    """Make a layer."""
    hash = hashlib.sha224(json.dumps(locals()).encode()).hexdigest()
    layer = {
        'id': 'layer%s' % (hash, ),
        'paint': paint,
        'source': 'composite',
        'source-layer': source_layer,
        'type': 'fill',
    }
    if filter:
        layer['filter'] = filter
    return layer

def make_paint(
    fill_color = None
    , fill_outline_color = None
    , fill_opacity = None
):
    """Make a paint property."""
    paint = {}
    if fill_color: paint['fill-color'] = fill_color
    if fill_outline_color: paint['fill-outline-color'] = fill_outline_color
    if fill_opacity: paint['fill-opacity'] = fill_opacity
    return paint

def make_filter(value = 0, key = 'id'):
    """Make a filter."""
    if key == 'id': id = ['id']
    else: id = ['get', key]
    return ['match', id, value, True, False]

# Messages still reported by pylint:
# pylint -dC0103,C0122,C0301,C0321,C0326,C0330,R0913,W0102,W0603,W0622,W0613,W0641 mapboxutil.py