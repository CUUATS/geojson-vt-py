# GeoJSON Vector Tiles for Python

A Python port of [JS GeoJSON-VT](https://github.com/mapbox/geojson-vt) for
generating vector map tiles.

## Usage
```py
import json
from geojsonvt import GeoJSONVT

with open('data.json', 'r') as json_file:
  geojson = json.load(json_file)

vt = GeoJSONVT(geojson)
vt.getTile(0, 0, 0)
```

For additional details and options, see the
[JS GeoJSON-VT documentation](https://github.com/mapbox/geojson-vt).

## Development
To run the tests:
```
python -m unittest tests
```

## Credits
[JS GeoJSON-VT](https://github.com/mapbox/geojson-vt) was created by
[Mapbox](https://github.com/mapbox) and licensed under the
[ISC License](https://github.com/mapbox/geojson-vt/blob/master/LICENSE).

The Python port was created by [Matt Yoder](https://github.com/yomatters)
for [CUUATS](https://github.com/CUUATS) and is licensed under the
[ISC License](https://github.com/CUUATS/geojson-vt-py/blob/master/LICENSE.md).
