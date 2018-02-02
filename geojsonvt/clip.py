from __future__ import division
from .feature import createFeature
from .geometry import Geometry


def clip(features, scale, k1, k2, axis, minAll, maxAll):
    k1 /= scale
    k2 /= scale

    if minAll >= k1 and maxAll <= k2:
        return features

    elif minAll > k2 or maxAll < k1:
        return None

    clipped = []

    for feature in features:
        geometry = feature['geometry']
        if not isinstance(geometry, Geometry):
            geometry = Geometry(geometry)
        ftype = feature['type']

        minCoord = feature['minX'] if axis == 0 else feature['minY']
        maxCoord = feature['maxX'] if axis == 0 else feature['maxY']

        if minCoord >= k1 and maxCoord <= k2:
            clipped.append(feature)
            continue
        elif minCoord > k2 or maxCoord < k1:
            continue

        newGeometry = Geometry()

        if ftype == 'Point' or ftype == 'MultiPoint':
            clipPoints(geometry, newGeometry, k1, k2, axis)

        elif ftype == 'LineString':
            clipLine(geometry, newGeometry, k1, k2, axis, False)

        elif ftype == 'MultiLineString':
            clipLines(geometry, newGeometry, k1, k2, axis, False)

        elif ftype == 'Polygon':
            clipLines(geometry, newGeometry, k1, k2, axis, True)

        elif ftype == 'MultiPolygon':
            for part in geometry:
                polygon = Geometry()
                clipLines(part, polygon, k1, k2, axis, True)
                if polygon:
                    newGeometry.append(polygon)

        if newGeometry:
            if ftype == 'LineString' or ftype == 'MultiLineString':
                if len(newGeometry) == 1:
                    ftype = 'LineString'
                    newGeometry = newGeometry[0]
                else:
                    ftype = 'MultiLineString'

            if ftype == 'Point' or ftype == 'MultiPoint':
                ftype = 'Point' if len(newGeometry) == 3 else 'MultiPoint'

            clipped.append(createFeature(
                feature.get('id', None), ftype, newGeometry,
                feature.get('tags', None)))

    return clipped if clipped else None


def clipPoints(geom, newGeom, k1, k2, axis):
    for i in range(0, len(geom), 3):
        a = geom[i + axis]

        if a >= k1 and a <= k2:
            newGeom.extend(geom[i:(i+3)])


def clipLine(geom, newGeom, k1, k2, axis, isPolygon):
    gslice = Geometry()
    intersect = intersectX if axis == 0 else intersectY

    for i in range(0, len(geom) - 3, 3):
        ax = geom[i]
        ay = geom[i + 1]
        az = geom[i + 2]
        bx = geom[i + 3]
        by = geom[i + 4]
        a = ax if axis == 0 else ay
        b = bx if axis == 0 else by
        sliced = False

        if a < k1:
            # ---|-->  |
            if b >= k1:
                intersect(gslice, ax, ay, bx, by, k1)
        elif a > k2:
            # |  <--|---
            if b <= k2:
                intersect(gslice, ax, ay, bx, by, k2)
        else:
            addPoint(gslice, ax, ay, az)

        if b < k1 and a >= k1:
            # <--|---  | or <--|-----|---
            intersect(gslice, ax, ay, bx, by, k1)
            sliced = True

        if b > k2 and a <= k2:
            # |  ---|--> or ---|-----|-->
            intersect(gslice, ax, ay, bx, by, k2)
            sliced = True

        if (not isPolygon) and sliced:
            gslice.size = geom.size
            newGeom.append(gslice)
            gslice = Geometry()

    # add the last point
    last = len(geom) - 3
    ax = geom[last]
    ay = geom[last + 1]
    az = geom[last + 2]
    a = ax if axis == 0 else ay
    if a >= k1 and a <= k2:
        addPoint(gslice, ax, ay, az)

    # close the polygon if its endpoints are not the same after clipping
    last = len(gslice) - 3
    if isPolygon and last >= 3 and \
            (gslice[last] != gslice[0] or gslice[last + 1] != gslice[1]):
        addPoint(gslice, gslice[0], gslice[1], gslice[2])

    # add the final slice
    if gslice:
        gslice.size = geom.size
        newGeom.append(gslice)


def clipLines(geom, newGeom, k1, k2, axis, isPolygon):
    for part in geom:
        if not isinstance(part, Geometry):
            part = Geometry(part)
        clipLine(part, newGeom, k1, k2, axis, isPolygon)


def addPoint(out, x, y, z):
    out.extend([x, y, z])


def intersectX(out, ax, ay, bx, by, x):
    out.extend([x, ay + (x - ax) * (by - ay) / (bx - ax), 1])


def intersectY(out, ax, ay, bx, by, y):
    out.extend([ax + (y - ay) * (bx - ax) / (by - ay), y, 1])
