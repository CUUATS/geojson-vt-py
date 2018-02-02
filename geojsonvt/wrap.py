from .clip import clip
from .feature import createFeature
from .geometry import Geometry


def wrap(features, buf):
    merged = features
    # left world copy
    left = clip(features, 1, -1 - buf, buf,     0, -1, 2)
    # right world copy
    right = clip(features, 1,  1 - buf, 2 + buf, 0, -1, 2)

    if left or right:
        # center world copy
        merged = clip(features, 1, -buf, 1 + buf, 0, -1, 2) or []

        # merge left into center
        if left:
            merged = shiftFeatureCoords(left, 1) + merged
        # merge right into center
        if right:
            merged = merged + shiftFeatureCoords(right, -1)

    return merged


def shiftFeatureCoords(features, offset):
    newFeatures = []

    for feature in features:
        ftype = feature['type']

        if ftype == 'Point' or ftype == 'MultiPoint' or ftype == 'LineString':
            newGeometry = shiftCoords(feature['geometry'], offset)

        elif ftype == 'MultiLineString' or ftype == 'Polygon':
            newGeometry = []
            for part in feature['geometry']:
                newGeometry.append(shiftCoords(part, offset))
        elif ftype == 'MultiPolygon':
            newGeometry = []
            for polygon in feature['geometry']:
                newPolygon = []
                for part in polygon:
                    newPolygon.append(shiftCoords(part, offset))
                newGeometry.append(newPolygon)

        newFeatures.append(createFeature(
            feature['id'], ftype, newGeometry, feature['tags']))

    return newFeatures


def shiftCoords(points, offset):
    newPoints = Geometry()
    newPoints.size = points.size

    for i in range(0, len(points), 3):
        newPoints.extend([points[i] + offset, points[i + 1], points[i + 2]])

    return newPoints
