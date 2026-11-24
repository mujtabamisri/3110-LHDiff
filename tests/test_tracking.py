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

    
    def test_rename_variable(self):
        old = ["int total = a + b;", "return total;"]
        new = ["int sum = a + b;", "return sum;"]

        rows = track(old, new)
        pairs = {(r["old"], tuple(r["new"])) for r in rows}

        self.assertIn((1, (1,)), pairs)
        self.assertIn((2, (2,)), pairs)

    def test_change_number(self):
        old = ["int count = 100;"]
        new = ["int count = 101;"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_change_operator(self):
        old = ["int result = a + b;"]
        new = ["int result = a - b;"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_rename_function(self):
        old = ["void calculateTotal() {"]
        new = ["void calculateTotals() {"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_capitalization(self):
        old = ["int total = computeValue(value);"]
        new = ["int Total = computeValue(value);"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_whitespace(self):
        old = ["int x=10;"]
        new = ["int   x = 10;"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1
            and r["new"] == [1]
            and r["type"] == "unchanged"
            for r in rows
        ))

    def test_add_comment(self):
        old = ["int x = 10;"]
        new = ["// Initialize x", "int x = 10;"]

        rows = track(old, new)

        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [2]
            for r in rows
        ))
        self.assertTrue(any(
            r["type"] == "added" and r["new"] == [1]
            for r in rows
        ))

    def test_delete_comment(self):
        old = ["// Initialize x", "int x = 10;"]
        new = ["int x = 10;"]

        rows = track(old, new)

        self.assertTrue(any(
            r["old"] == 1 and r["type"] == "deleted"
            for r in rows
        ))
        self.assertTrue(any(
            r["old"] == 2 and r["new"] == [1]
            for r in rows
        ))

    def test_move_multiple_lines(self):
        old = [
            "unique_alpha();",
            "unique_beta();",
            "unique_gamma();",
            "unique_delta();"
        ]
        new = [
            "unique_delta();",
            "unique_alpha();",
            "unique_beta();",
            "unique_gamma();"
        ]

        rows = track(old, new)
        pairs = {(r["old"], tuple(r["new"])) for r in rows}

        self.assertIn((1, (2,)), pairs)
        self.assertIn((2, (3,)), pairs)
        self.assertIn((3, (4,)), pairs)
        self.assertIn((4, (1,)), pairs)

    def test_split_three_lines(self):
        old = ["calculate(first,second,third);"]
        new = [
            "calculate(first,",
            "second,",
            "third);"
        ]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1, 2, 3]
            for r in rows
        ))

    def test_insert_multiple_lines(self):
        old = [
            "start();",
            "finish();"
        ]
        new = [
            "start();",
            "logStart();",
            "validate();",
            "finish();"
        ]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))
        self.assertTrue(any(
            r["old"] == 2 and r["new"] == [4]
            for r in rows
        ))
        self.assertTrue(any(
            r["type"] == "added" and r["new"] == [2]
            for r in rows
        ))
        self.assertTrue(any(
            r["type"] == "added" and r["new"] == [3]
            for r in rows
        ))

    def test_add_if_statement(self):
        old = ["processOrder();"]
        new = [
            "if (ready) {",
            "processOrder();",
            "}"
        ]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [2]
            for r in rows
        ))

    def test_change_if_condition(self):
        old = ["if (x > 5 && enabled) {"]
        new = ["if (x >= 5 && enabled) {"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_change_loop(self):
        old = ["for (int i=0; i<10; i++) {"]
        new = ["for (int i=0; i<=10; i++) {"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_add_function(self):
        old = ["void run() {}"]
        new = [
            "void run() {}",
            "void stop() {}"
        ]

        rows = track(old, new)
        self.assertTrue(any(
            r["type"] == "added" and r["new"] == [2]
            for r in rows
        ))

    def test_delete_function(self):
        old = [
            "void run() {}",
            "void stop() {}"
        ]
        new = ["void run() {}"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 2 and r["type"] == "deleted"
            for r in rows
        ))

    def test_change_list_initial_capacity(self):
        old = ["ArrayList<String> names = new ArrayList<>();"]
        new = ["ArrayList<String> names = new ArrayList<>(10);"]

        rows = track(old, new)
        self.assertTrue(any(
            r["old"] == 1 and r["new"] == [1]
            for r in rows
        ))

    def test_multiple_changes(self):
        old = [
            "int total = 10;",
            "print(total);",
            "finish();"
        ]
        new = [
            "start();",
            "int sum = 20;",
            "finish();",
            "print(sum);"
        ]

        rows = track(old, new)
        pairs = {(r["old"], tuple(r["new"])) for r in rows}

        self.assertIn((1, (2,)), pairs)
        self.assertIn((2, (4,)), pairs)
        self.assertIn((3, (3,)), pairs)
        self.assertIn((None, (1,)), pairs)


if __name__ == '__main__':
    unittest.main()
