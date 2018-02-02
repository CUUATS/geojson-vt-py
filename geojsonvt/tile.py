from __future__ import division
import math
from .geometry import Geometry


def createTile(features, z2, tx, ty, tolerance, noSimplify):
    tile = {
        'features': [],
        'numPoints': 0,
        'numSimplified': 0,
        'numFeatures': 0,
        'source': None,
        'x': tx,
        'y': ty,
        'z2': z2,
        'transformed': False,
        'minX': 2,
        'minY': 1,
        'maxX': -1,
        'maxY': 0
    }

    for feature in features:
        tile['numFeatures'] += 1
        addFeature(tile, feature, tolerance, noSimplify)

        minX = feature['minX']
        minY = feature['minY']
        maxX = feature['maxX']
        maxY = feature['maxY']

        if minX < tile['minX']:
            tile['minX'] = minX
        if minY < tile['minY']:
            tile['minY'] = minY
        if maxX > tile['maxX']:
            tile['maxX'] = maxX
        if maxY > tile['maxY']:
            tile['maxY'] = maxY

    return tile


def addFeature(tile, feature, tolerance, noSimplify):
    geom = feature['geometry']
    ftype = feature['type']
    simplified = Geometry()

    if ftype == 'Point' or ftype == 'MultiPoint':
        for i in range(0, len(geom), 3):
            simplified.extend([geom[i], geom[i + 1]])
            tile['numPoints'] += 1
            tile['numSimplified'] += 1

    elif ftype == 'LineString':
        addLine(simplified, geom, tile, tolerance, noSimplify, False, False)

    elif ftype == 'MultiLineString' or ftype == 'Polygon':
        for (i, part) in enumerate(geom):
            addLine(simplified, part, tile, tolerance, noSimplify,
                    ftype == 'Polygon', i == 0)

    elif ftype == 'MultiPolygon':
        for polygon in geom:
            for (i, part) in enumerate(polygon):
                addLine(simplified, part, tile, tolerance, noSimplify, True,
                        i == 0)

    if simplified:
        tileFeature = {
            'geometry': simplified,
            'type': 3 if (
                ftype == 'Polygon' or ftype == 'MultiPolygon') else (
                2 if ftype == 'LineString' or
                ftype == 'MultiLineString' else 1),
            'tags': feature.get('tags', None)
        }
        if feature['id'] is not None:
            tileFeature['id'] = feature['id']

        tile['features'].append(tileFeature)


def addLine(result, geom, tile, tolerance, noSimplify, isPolygon, isOuter):
    sqTolerance = tolerance * tolerance

    if (not noSimplify) and (
            geom.size < (sqTolerance if isPolygon else tolerance)):
        tile['numPoints'] += int(len(geom) / 3)
        return

    ring = Geometry()

    for i in range(0, len(geom), 3):
        if noSimplify or geom[i + 2] > sqTolerance:
            tile['numSimplified'] += 1
            ring.extend([geom[i], geom[i + 1]])

        tile['numPoints'] += 1

    if isPolygon:
        rewind(ring, isOuter)

    result.append(ring)


def rewind(ring, clockwise):
    area = 0
    rlen = len(ring)
    j = rlen - 2

    for i in range(0, rlen, 2):
        area += (ring[i] - ring[j]) * (ring[i + 1] + ring[j + 1])
        j = i

    if (area > 0) == clockwise:
        rlen = len(ring)
        for i in range(0, int(math.ceil(rlen / 2)), 2):
            x = ring[i]
            y = ring[i + 1]
            ring[i] = ring[rlen - 2 - i]
            ring[i + 1] = ring[rlen - 1 - i]
            ring[rlen - 2 - i] = x
            ring[rlen - 1 - i] = y
