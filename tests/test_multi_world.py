import unittest
from geojsonvt import GeoJSONVT


class TestMultiWorld(unittest.TestCase):

    LEFT_POINT = {
        'type': 'Feature',
        'properties': {},
        'geometry': {
            'coordinates': [-540, 0],
            'type': 'Point'
        }
    }

    RIGHT_POINT = {
        'type': 'Feature',
        'properties': {},
        'geometry': {
            'coordinates': [540, 0],
            'type': 'Point'
        }
    }

    def test_point_right_side(self):
        vt = GeoJSONVT(self.RIGHT_POINT)
        self.assertEqual(vt.tiles[0]['features'][0]['geometry'][0], 1)
        self.assertEqual(vt.tiles[0]['features'][0]['geometry'][1], 0.5)

    def test_point_left_side(self):
        vt = GeoJSONVT(self.LEFT_POINT)
        self.assertEqual(vt.tiles[0]['features'][0]['geometry'][0], 0)
        self.assertEqual(vt.tiles[0]['features'][0]['geometry'][1], 0.5)

    def test_points_both_sides(self):
        vt = GeoJSONVT({
            'type': 'FeatureCollection',
            'features': [self.LEFT_POINT, self.RIGHT_POINT]
        })

        self.assertEqual(vt.tiles[0]['features'][0]['geometry'][0], 0)
        self.assertEqual(vt.tiles[0]['features'][0]['geometry'][1], 0.5)

        self.assertEqual(vt.tiles[0]['features'][1]['geometry'][0], 1)
        self.assertEqual(vt.tiles[0]['features'][1]['geometry'][1], 0.5)
