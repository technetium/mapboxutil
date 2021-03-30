# The mapboxutil module

## Using

```
pip install mapboxutil
```


```python
from mapboxutil import *

MAPBOX_TOKEN  = 'sk.eyJ1IjoidGVjaG5ldGl1bSIsImEiOiJja2Vqbm9iOXIxdjgyMnJveXAxdmNwbzdpIn0.1cVVBOymux7J0_pTbZIpVQ'
MAPBOX_PUBLIC = 'pk.eyJ1IjoidGVjaG5ldGl1bSIsImEiOiJjazBjMnE3aXkweTB5M25vNGRldm56bTdpIn0.OXka1L7OThmbux37xMt3rg'

username = 'technetium'
stylename = 'Olympic'
# Mapbox has it's own country borders tileset let's use that one
source_name = 'country_boundaries'
tileset_id = 'mapbox.country-boundaries-v1'

set_mapbox_token(
    public_key = MAPBOX_PUBLIC,
    secret_key = MAPBOX_TOKEN
)

style = {
    **make_style(stylename),
    **{
        'sources': make_sources([tileset_id]),
        'layers': [
            make_layer(
                source_name,
                make_paint('#CCC', '#FFF')    
            ),
            make_layer(
                source_name,
                make_paint('#00C', '#006'),
                make_filter(2035743)
            ),
            make_layer(
                source_name,
                make_paint('#C00', '#600'),
                [ "all", make_filter('China', 'name_en'), make_filter('CN', 'worldview') ],
            ),
            make_layer(
                source_name,
                make_paint('#CC0', '#660'),
                make_filter('AU', 'iso_3166_1')
            ),
            make_layer(
                source_name,
                make_paint('#0C0', '#060'),
                make_filter('ESP', 'iso_3166_1_alpha_3')
            ),
        ],
    },
}

style_id = get_style_id_by_name(stylename, username=username)
if style_id:
    style = update_style(username, style_id, style)
else:
    style = create_style(username, style)

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
                overlay_marker( 39.906667, 116.397500, 'F66', 'p'), # Beijing
                overlay_marker(-33.865000, 151.209444, 'FF6', 's'), # Sidney
                overlay_marker( 41.383333,   2.183333, '6F6', 'b'), # Barcelona
            ]
                
        }
    }
)
print(urls)
```
