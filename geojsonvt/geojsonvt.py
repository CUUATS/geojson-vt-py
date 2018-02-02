from __future__ import division
import math
from .convert import convert  # GeoJSON conversion and preprocessing
from .transform import transformTile  # coordinate transformation
from .clip import clip  # stripe clipping algorithm
from .wrap import wrap  # date line processing
from .tile import createTile  # final simplified tile generation


def toID(z, x, y):
    return (((1 << z) * y + x) * 32) + z


class GeoJSONVT:
    OPTIONS = {
        'maxZoom': 14,             # max zoom to preserve detail on
        'indexMaxZoom': 5,         # max zoom in the tile index
        'indexMaxPoints': 100000,  # max number of points per tile
                                   # in the tile index
        'tolerance': 3,            # simplification tolerance
                                   # (higher means simpler)
        'extent': 4096,            # tile extent
        'buffer': 64,              # tile buffer on each side
        'debug': 0                 # logging level (0, 1 or 2)
    }

    def __init__(self, data, options={}):
        self.options = GeoJSONVT.OPTIONS.copy()
        self.options.update(options)

        options = self.options
        debug = options['debug']

        if debug:
            print('preprocess data')

        if options['maxZoom'] < 0 or options['maxZoom'] > 24:
            raise ValueError('maxZoom should be in the 0-24 range')

        z2 = 1 << options['maxZoom']  # 2^z
        features = convert(
            data, options['tolerance'] / (z2 * options['extent']))

        self.tiles = {}
        self.tileCoords = []

        if debug:
            # TODO: Add timing
            # console.timeEnd('preprocess data');
            print('index: maxZoom: %i, maxPoints: %i' % (
                options['indexMaxZoom'], options['indexMaxPoints']))
            # console.time('generate tiles');
            self.stats = {}
            self.total = 0

        features = wrap(features, options['buffer'] / options['extent'])

        # start slicing from the top tile down
        if features:
            self.splitTile(features, 0, 0, 0)

        if debug:
            if features:
                print('features: %i, points: %i' % (
                    self.tiles[0]['numFeatures'], self.tiles[0]['numPoints']))
            # console.timeEnd('generate tiles');
            print('tiles generated: %i %s' % (self.total, str(self.stats)))

    def splitTile(self, features, z, x, y, cz=None, cx=None, cy=None):
        stack = [features, z, x, y]
        options = self.options
        debug = options['debug']

        # avoid recursion by using a processing queue
        while (stack):
            y = stack.pop()
            x = stack.pop()
            z = stack.pop()
            features = stack.pop()

            z2 = 1 << z
            tid = toID(z, x, y)
            tile = self.tiles.get(tid, None)
            tileTolerance = 0 if z == options['maxZoom'] \
                else options['tolerance'] / (z2 * options['extent'])

            if not tile:
                if (debug > 1):
                    pass
                    # console.time('creation');

                tile = createTile(
                    features, z2, x, y, tileTolerance, z == options['maxZoom'])
                self.tiles[tid] = tile
                self.tileCoords.append({'z': z, 'x': x, 'y': y})

                if debug:
                    if debug > 1:
                        print(('tile z%i-%i-%i (features: %i, points: %i, ' +
                              'simplified: %i)') % (
                                    z, x, y, tile['numFeatures'],
                                    tile['numPoints'], tile['numSimplified']))
                        # console.timeEnd('creation');
                    key = 'z' + str(z)
                    self.stats[key] = self.stats.get(key, 0) + 1
                    self.total += 1

            # save reference to original geometry in tile so that we can
            # drill down later if we stop now
            tile['source'] = features

            #  if it's the first-pass tiling
            if not cz:
                # stop tiling if we reached max zoom, or if the tile is
                # too simple
                if z == options['indexMaxZoom'] or \
                        tile['numPoints'] <= options['indexMaxPoints']:
                    continue

            # if a drilldown to a specific tile
            else:
                # stop tiling if we reached base zoom or our target tile zoom
                if z == options['maxZoom'] or z == cz:
                    continue

                # stop tiling if it's not an ancestor of the target tile
                m = 1 << (cz - z)
                if x != math.floor(cx / m) or y != math.floor(cy / m):
                    continue

            # if we slice further down, no need to keep source geometry
            tile['source'] = None

            if len(features) == 0:
                continue

            if debug > 1:
                pass
                # TODO: timing
                # console.time('clipping')

            # values we'll use for clipping
            k1 = 0.5 * options['buffer'] / options['extent']
            k2 = 0.5 - k1
            k3 = 0.5 + k1
            k4 = 1 + k1
            tl = None
            bl = None
            tr = None
            br = None

            left = clip(
                features, z2, x - k1, x + k3, 0, tile['minX'], tile['maxX'])
            right = clip(
                features, z2, x + k2, x + k4, 0, tile['minX'], tile['maxX'])
            features = None

            if left:
                tl = clip(
                    left, z2, y - k1, y + k3, 1, tile['minY'], tile['maxY'])
                bl = clip(
                    left, z2, y + k2, y + k4, 1, tile['minY'], tile['maxY'])
                left = None

            if right:
                tr = clip(
                    right, z2, y - k1, y + k3, 1, tile['minY'], tile['maxY'])
                br = clip(
                    right, z2, y + k2, y + k4, 1, tile['minY'], tile['maxY'])
                right = None

            if debug > 1:
                pass
                # TODO: timing
                # console.timeEnd('clipping')

            stack.extend([tl or [], z + 1, x * 2,     y * 2])
            stack.extend([bl or [], z + 1, x * 2,     y * 2 + 1])
            stack.extend([tr or [], z + 1, x * 2 + 1, y * 2])
            stack.extend([br or [], z + 1, x * 2 + 1, y * 2 + 1])

    def getTile(self, z, x, y):
        options = self.options
        extent = options['extent']
        debug = options['debug']

        if z < 0 or z > 24:
            return None

        z2 = 1 << z
        x = ((x % z2) + z2) % z2  # wrap tile x coordinate

        tid = toID(z, x, y)
        if tid in self.tiles:
            return transformTile(self.tiles[tid], extent)

        if debug > 1:
            print('drilling down to z%i-%i-%i' % (z, x, y))

        z0 = z
        x0 = x
        y0 = y
        parent = None

        while (not parent) and z0 > 0:
            z0 -= 1
            x0 = math.floor(x0 / 2)
            y0 = math.floor(y0 / 2)
            parent = self.tiles.get(toID(z0, x0, y0), None)

        if (not parent) or (not parent['source']):
            return None

        # if we found a parent tile containing the original geometry,
        # we can drill down from it
        if debug > 1:
            print('found parent tile z%i-%i-%i' % (z0, x0, y0))
            # TODO: timing
            # console.time('drilling down');

        self.splitTile(parent['source'], z0, x0, y0, z, x, y)

        if debug > 1:
            pass
            # TODO timing
            # console.timeEnd('drilling down');

        return transformTile(self.tiles[tid], extent) \
            if tid in self.tiles else None
