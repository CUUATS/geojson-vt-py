import unittest
from geojsonvt import GeoJSONVT
from .utils import load_json, json_str


class TestGetTile(unittest.TestCase):

    SQUARE = [
        {
            'geometry': [
                [
                    [-64, 4160],
                    [-64, -64],
                    [4160, -64],
                    [4160, 4160],
                    [-64, 4160]
                ]
            ],
            'type': 3,
            'tags': {
                'name': 'Pennsylvania',
                'density': 284.3
            },
            'id': '42'
        }
    ]

    @classmethod
    def setUpClass(cls):
        cls.index = GeoJSONVT(load_json('us-states.json'), {'debug': 2})

    def test_get_tiles(self):
        features = self.index.getTile(7, 37, 48)['features']
        expected = load_json('us-states-z7-37-48.json')
        self.assertEqual(json_str(features), json_str(expected))

        features = self.index.getTile(9, 148, 192)['features']
        self.assertEqual(json_str(features), json_str(TestGetTile.SQUARE))

        self.assertEqual(self.index.total, 37)

    def test_non_existant_tile(self):
        tile = self.index.getTile(11, 800, 400)
        self.assertEqual(tile, None)

    def test_invalid_tile(self):
        tile = self.index.getTile(-5, 123.25, 400.25)
        self.assertEqual(tile, None)

    def test_invalid_zoom(self):
        tile = self.index.getTile(25, 200, 200)
        self.assertEqual(tile, None)
