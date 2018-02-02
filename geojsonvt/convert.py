from __future__ import division
import math
from .simplify import simplify
from .feature import createFeature
from .geometry import Geometry


def convert(data, tolerance):
    """converts GeoJSON feature into an intermediate projected JSON vector
    format with simplification data"""

    features = []

    if data['type'] == 'FeatureCollection':
        for feature in data['features']:
            convertFeature(features, feature, tolerance)

    elif data['type'] == 'Feature':
        convertFeature(features, data, tolerance)

    else:
        # single geometry or a geometry collection
        convertFeature(features, {'geometry': data}, tolerance)

    return features


def convertFeature(features, geojson, tolerance):
    if not geojson.get('geometry', None):
        return

    coords = geojson['geometry'].get('coordinates', None)
    ftype = geojson['geometry']['type']
    tol = tolerance * tolerance
    geometry = Geometry()

    if ftype == 'Point':
        convertPoint(coords, geometry)

    elif ftype == 'MultiPoint':
        for coord in coords:
            convertPoint(coord, geometry)

    elif ftype == 'LineString':
        convertLine(coords, geometry, tol, False)

    elif ftype == 'MultiLineString':
        convertLines(coords, geometry, tol, False)

    elif ftype == 'Polygon':
        convertLines(coords, geometry, tol, True)

    elif ftype == 'MultiPolygon':
        for coord in coords:
            polygon = Geometry()
            convertLines(coord, polygon, tol, True)
            geometry.append(polygon)

    elif ftype == 'GeometryCollection':
        for geom in geojson['geometry']['geometries']:
            convertFeature(features, {
                'geometry': geom,
                'properties': geojson.get('properties', None)
            }, tolerance)
        return

    else:
        raise ValueError('Input data is not a valid GeoJSON object.')

    features.append(createFeature(
        geojson.get('id', None), ftype, geometry,
        geojson.get('properties', None)))


def convertPoint(coords, out):
    out.extend([projectX(coords[0]), projectY(coords[1]), 0])


def convertLine(ring, out, tol, isPolygon):
    x0 = 0
    y0 = 0
    size = 0

    for (j, point) in enumerate(ring):
        x = projectX(point[0])
        y = projectY(point[1])

        out.extend([x, y, 0])

        if j > 0:
            if isPolygon:
                # area
                size += (x0 * y - x * y0) / 2
            else:
                # length
                size += math.sqrt(math.pow(x - x0, 2) + math.pow(y - y0, 2))

        x0 = x
        y0 = y

    last = len(out) - 3
    out[2] = 1
    simplify(out, 0, last, tol)
    out[last + 2] = 1

    out.size = abs(size)


def convertLines(rings, out, tol, isPolygon):
    for ring in rings:
        geom = Geometry()
        convertLine(ring, geom, tol, isPolygon)
        out.append(geom)


def projectX(x):
    return x / 360 + 0.5


def projectY(y):
    sin = math.sin(y * math.pi / 180)

    # Avoid invalid math
    if sin == 1:
        return 0
    elif sin == -1:
        return 1

    y2 = 0.5 - 0.25 * math.log((1 + sin) / (1 - sin)) / math.pi
    return 0 if y2 < 0 else (1 if y2 > 1 else y2)
