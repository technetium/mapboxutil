## Installation

Use pip to install ```mapboxutils```:

```
pip install mapboxutils
```

## Usage

An example script to generate a map
with (some) locations of Olympic Games:

```python
from mapboxutil import *

# Define tokens
MAPBOX_PUBLIC = 'pk.aRandomString0f5ixtySevenUpperAndL0werCaseCharactersAndNumb3rsPo1nt.andThenYet1other22M0re'
MAPBOX_SECRET = 'sk.aDiff3rentStr1ngWithRand0mUpperCaseAndLowerCaseCharactersAndNumbers.0fC0urseThese1sAreFak3'

# Define personal data
username = 'yourusername'
stylename = 'Olympic'

# Mapbox has it's own country tileset let's use that one
source_name = 'country_boundaries'
tileset_id = 'mapbox.country-boundaries-v1'

# Set the keys in the global module variables
set_mapbox_token(
    public_key = MAPBOX_PUBLIC,
    secret_key = MAPBOX_SECRET
)

# Define the style
style = make_style(
    stylename,
    add_sources([tileset_id]),
    [
        make_layer(
            source_name,
            make_paint('#CCC', '#FFF')
        ),
        make_layer(
            source_name,
            make_paint('#00C', '#006'),
            make_filter(2035743) # This is the id for Brazil
        ),
        make_layer(
            source_name,
            make_paint('#C00', '#600'),
            [
                "all",
                make_filter('China', 'name_en'),
                # China has some disputed borders
                # To select which version that is used
                # the worldview has to be added
                # This selects China's own worldview
                make_filter('CN', 'worldview')
            ],
        ),
        make_layer(
            source_name,
            make_paint('#CC0', '#660'),
            make_filter('AU', 'iso_3166_1') # Code for Australia
        ),
        make_layer(
            source_name,
            make_paint('#0C0', '#060'),
            make_filter('ESP', 'iso_3166_1_alpha_3') # Code for Spain
        ),
    ]
)

# Check if there is already a style with the name
style_id = get_style_id_by_name(stylename, username=username)
if style_id:
    # Update if the style already exists
    style = update_style(username, style_id, style)
else:
    # Create the style if it's not
    style = create_style(username, style)

# Determine the url
url = mapbox_url(
    **{
        **mapbox_dimensions(
            south = -43.643611,
            north =  53.550000,
            west  = -73.984444,
            east  = 153.638889,
            width = 600,
            height= 360
        ),
        **{
            'username': username,
            'style': style_id,
            'width': 640,
            'height': 400,
            'overlays': [
                overlay_marker(-22.911366, -43.205916, '66F', 'r'), # Rio de Janeiro
                overlay_marker( 39.906667, 116.397500, 'F66', 'p'), # Beijing / Peking
                overlay_marker(-33.865000, 151.209444, 'FF6', 's'), # Sidney
                overlay_marker( 41.383333,   2.183333, '6F6', 'b'), # Barcelona
            ]

        }
    }
)
# Print the url
print(url)
```
