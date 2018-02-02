import unittest
from .gen_tiles import genTiles
from .utils import load_json, json_str


class TestFull(unittest.TestCase):

    def _tiles_equal(self, inputFile, expectedFile, maxZoom=0,
                     maxPoints=10000):
        tiles = genTiles(load_json(inputFile), maxZoom, maxPoints)
        expected = load_json(expectedFile)
        self.assertEqual(json_str(tiles), json_str(expected))

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
        self.assertEqual(json_str(genTiles(load_json('empty.json'))), '{}')

    def test_null_geometry(self):
        # should ignore features with null geometry
        self.assertEqual(json_str(genTiles(
            load_json('feature-null-geometry.json'))), '{}')


if __name__ == '__main__':
    unittest.main()
