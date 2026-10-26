import unittest
from src.preprocessing import normalize
from src.matching import content_similarity
from src.tracker import track


class TrackingTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize(' int x = 1; '), 'intx=1;')

    def test_identical(self):
        rows = track(['a', 'b'], ['a', 'b'])
        self.assertEqual([(r['old'], r['new']) for r in rows], [(1, [1]), (2, [2])])

    def test_insert(self):
        rows = track(['alpha', 'omega'], ['alpha', 'inserted', 'omega'])
        self.assertTrue(any(r['type'] == 'added' and r['new'] == [2] for r in rows))

    def test_delete(self):
        rows = track(['alpha', 'deleted', 'omega'], ['alpha', 'omega'])
        self.assertTrue(any(r['type'] == 'deleted' and r['old'] == 2 for r in rows))

    def test_reorder(self):
        rows = track(['unique_alpha', 'unique_beta'], ['unique_beta', 'unique_alpha'])
        pairs = {(r['old'], tuple(r['new'])) for r in rows}
        self.assertIn((1, (2,)), pairs)
        self.assertIn((2, (1,)), pairs)

    def test_split(self):
        rows = track(['function(first,second,third);'], ['function(first,', 'second,third);'])
        self.assertTrue(any(r['old'] == 1 and r['new'] == [1, 2] for r in rows))

    def test_similarity(self):
        self.assertEqual(content_similarity('abc', 'abc'), 1.0)
        self.assertEqual(content_similarity('abc', 'xyz'), 0.0)


if __name__ == '__main__':
    unittest.main()
