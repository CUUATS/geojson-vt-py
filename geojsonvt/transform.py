def transformTile(tile, extent):
    """Transforms the coordinates of each feature in the given tile from
    mercator-projected space into (extent x extent) tile space."""

    if tile['transformed']:
        return tile

    z2 = tile['z2']
    tx = tile['x']
    ty = tile['y']

    for feature in tile['features']:
        geom = feature['geometry']
        ftype = feature['type']

        feature['geometry'] = []

        if ftype == 1:
            for j in range(0, len(geom), 2):
                feature['geometry'].append(transformPoint(
                    geom[j], geom[j + 1], extent, z2, tx, ty))
        else:
            for part in geom:
                ring = []
                for k in range(0, len(part), 2):
                    ring.append(transformPoint(
                        part[k], part[k + 1], extent, z2, tx, ty))
                feature['geometry'].append(ring)

    tile['transformed'] = True

    return tile


def transformPoint(x, y, extent, z2, tx, ty):
    return [
        int(round(extent * (x * z2 - tx))),
        int(round(extent * (y * z2 - ty)))
    ]
