import unittest
from geojsonvt.clip import clip
from .utils import closed, integerize, json_str


class TestClip(unittest.TestCase):
    GEOM1 = [0, 0, 0, 50, 0, 0, 50, 10, 0, 20, 10, 0, 20, 20, 0, 30, 20, 0,
             30, 30, 0, 50, 30, 0, 50, 40, 0, 25, 40, 0, 25, 50, 0, 0, 50, 0,
             0, 60, 0, 25, 60, 0]
    GEOM2 = [0, 0, 0, 50, 0, 0, 50, 10, 0, 0, 10, 0]

    def test_clip_polylines(self):
        clipped = clip([
            {
                'geometry': TestClip.GEOM1,
                'type': 'LineString',
                'tags': 1,
                'minX': 0,
                'minY': 0,
                'maxX': 50,
                'maxY': 60
            },
            {
                'geometry': TestClip.GEOM2,
                'type': 'LineString',
                'tags': 2,
                'minX': 0,
                'minY': 0,
                'maxX': 50,
                'maxY': 10
            }
        ], 1, 10, 40, 0, -float('inf'), float('inf'))

        expected = [
            {
                'id': None,
                'type': 'MultiLineString',
                'geometry': [
                    [10, 0, 1, 40, 0, 1],
                    [40, 10, 1, 20, 10, 0, 20, 20, 0, 30, 20, 0, 30, 30, 0, 40,
                     30, 1],
                    [40, 40, 1, 25, 40, 0, 25, 50, 0, 10, 50, 1],
                    [10, 60, 1, 25, 60, 0]
                ],
                'tags': 1,
                'minX': 10,
                'minY': 0,
                'maxX': 40,
                'maxY': 60
            },
            {
                'id': None,
                'type': 'MultiLineString',
                'geometry': [
                    [10, 0, 1, 40, 0, 1],
                    [40, 10, 1, 10, 10, 1]
                ],
                'tags': 2,
                'minX': 10,
                'minY': 0,
                'maxX': 40,
                'maxY': 10
            }
        ]

        self.assertEqual(json_str(integerize(clipped)), json_str(expected))

    def test_clip_polygons(self):
        clipped = clip([
            {
                'geometry': closed(TestClip.GEOM1),
                'type': 'Polygon',
                'tags': 1,
                'minX': 0,
                'minY': 0,
                'maxX': 50,
                'maxY': 60
            },
            {
                'geometry': closed(TestClip.GEOM2),
                'type': 'Polygon',
                'tags': 2,
                'minX': 0,
                'minY': 0,
                'maxX': 50,
                'maxY': 10
            }
        ], 1, 10, 40, 0, -float('inf'), float('inf'))

        expected = [
            {
                'id': None,
                'type': 'Polygon',
                'geometry': [
                    [10, 0, 1, 40, 0, 1, 40, 10, 1, 20, 10, 0, 20, 20, 0, 30,
                     20, 0, 30, 30, 0, 40, 30, 1, 40, 40, 1, 25, 40, 0, 25, 50,
                     0, 10, 50, 1, 10, 60, 1, 25, 60, 0, 10, 24, 1, 10, 0, 1]
                ],
                'tags': 1,
                'minX': 10,
                'minY': 0,
                'maxX': 40,
                'maxY': 60
            },
            {
                'id': None,
                'type': 'Polygon',
                'geometry': [
                    [10, 0, 1, 40, 0, 1, 40, 10, 1, 10, 10, 1, 10, 0, 1]
                ],
                'tags': 2,
                'minX': 10,
                'minY': 0,
                'maxX': 40,
                'maxY': 10
            }
        ]

        self.assertEqual(json_str(integerize(clipped)), json_str(expected))

    def test_clip_points(self):
        clipped = clip([
            {
                'geometry': TestClip.GEOM1,
                'type': 'MultiPoint',
                'tags': 1,
                'minX': 0,
                'minY': 0,
                'maxX': 50,
                'maxY': 60
            },
            {
                'geometry': TestClip.GEOM2,
                'type': 'MultiPoint',
                'tags': 2,
                'minX': 0,
                'minY': 0,
                'maxX': 50,
                'maxY': 10
            }
        ], 1, 10, 40, 0, -float('inf'), float('inf'))

        expected = [
            {
                'id': None,
                'type': 'MultiPoint',
                'geometry': [20, 10, 0, 20, 20, 0, 30, 20, 0, 30, 30, 0, 25,
                             40, 0, 25, 50, 0, 25, 60, 0],
                'tags': 1,
                'minX': 20,
                'minY': 10,
                'maxX': 30,
                'maxY': 60
            }
        ]

        self.assertEqual(json_str(integerize(clipped)), json_str(expected))
