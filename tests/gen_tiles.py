import json
import math
import pprint
import sys
from geojsonvt import GeoJSONVT


def genTiles(data, maxZoom=0, maxPoints=10000):
    index = GeoJSONVT(data, {
        'indexMaxZoom': maxZoom,
        'indexMaxPoints': maxPoints
    })

    output = {}

    ln2 = math.log(2)
    for tid in index.tiles:
        tile = index.tiles[tid]
        z = int(math.log(tile['z2']) / ln2)
        output['z%i-%i-%i' % (z, tile['x'], tile['y'])] = \
            index.getTile(z, tile['x'], tile['y'])['features']

    return output


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as in_file:
        result = genTiles(json.parse(in_file), sys.argv[2], sys.argv[3])
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)
