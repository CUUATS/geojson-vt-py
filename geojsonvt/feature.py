def createFeature(fid, ftype, geom, tags):
    feature = {
        'id': fid or None,
        'type': ftype,
        'geometry': geom,
        'tags': tags,
        'minX': float('inf'),
        'minY': float('inf'),
        'maxX': -float('inf'),
        'maxY': -float('inf')
    }
    calcBBox(feature)
    return feature


def calcBBox(feature):
    geom = feature['geometry']
    ftype = feature['type']

    if ftype == 'Point' or ftype == 'MultiPoint' or ftype == 'LineString':
        calcLineBBox(feature, geom)

    elif ftype == 'Polygon' or ftype == 'MultiLineString':
        for part in geom:
            calcLineBBox(feature, part)

    elif ftype == 'MultiPolygon':
        for polygon in geom:
            for part in polygon:
                calcLineBBox(feature, part)


def calcLineBBox(feature, geom):
    for i in range(0, len(geom), 3):
        feature['minX'] = min(feature['minX'], geom[i])
        feature['minY'] = min(feature['minY'], geom[i + 1])
        feature['maxX'] = max(feature['maxX'], geom[i])
        feature['maxY'] = max(feature['maxY'], geom[i + 1])
