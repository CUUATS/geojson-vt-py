import json
import os
import unittest
from .gen_tiles import genTiles


class TestFull(unittest.TestCase):

    def _load_json(self, file_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'fixtures', file_name)
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

    def _tiles_equal(self, inputFile, expectedFile, maxZoom=0,
                     maxPoints=10000):
        tiles = genTiles(self._load_json(inputFile), maxZoom, maxPoints)
        expected = self._load_json(expectedFile)
        self.assertEqual(json.dumps(tiles, sort_keys=True),
                         json.dumps(expected, sort_keys=True))

    def test_tiles_us_states(self):
        self._tiles_equal('us-states.json', 'us-states-tiles.json', 7, 200)

    def test_tiles_dateline(self):
        self._tiles_equal('dateline.json', 'dateline-tiles.json')

    def test_tiles_feature(self):
        self._tiles_equal('feature.json', 'feature-tiles.json')

    def test_tiles_collection(self):
        self._tiles_equal('collection.json', 'collection-tiles.json')

    def test_tiles_single_geom(self):
        self._tiles_equal('single-geom.json', 'single-geom-tiles.json')

    def test_invalid_geojson(self):
        with self.assertRaises(ValueError) as context:
            genTiles({'type': 'Pologon'})

        self.assertTrue('not a valid GeoJSON object' in str(context.exception))

    def test_empty_geojson(self):
        self.assertEqual(
            json.dumps(genTiles(self._load_json('empty.json'))), '{}')

    def test_null_geometry(self):
        # should ignore features with null geometry
        self.assertEqual(json.dumps(genTiles(
            self._load_json('feature-null-geometry.json'))), '{}')


if __name__ == '__main__':
    unittest.main()
