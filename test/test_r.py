import unittest
from os import path
from subprocess import CalledProcessError
from r_functions import create, run


class TestR(unittest.TestCase):
    def setUp(self):
        self.test_file = path.join(path.dirname(__file__), "test.R")

    def test_create_add(self):
        params = {"a": 2, "b": 3}
        add = create(self.test_file, "add")
        output = add(**params)
        self.assertEqual(5, output)

    def test_create_reverse(self):
        params = [["a", "b", "c"]]
        reverse = create(self.test_file, "reverse")
        output = reverse(*params)
        self.assertEqual(["c", "b", "a"], output)

    def test_create_exception(self):
        throw_exception = create(self.test_file, "throw_exception")
        self.assertRaises(CalledProcessError, throw_exception)

    def test_run_add(self):
        params = {"a": 2, "b": 3}
        output = run(self.test_file, "add", params)
        self.assertEqual(5, output)

    def test_run_reverse(self):
        params = [["a", "b", "c"]]
        output = run(self.test_file, "reverse", params)
        self.assertEqual(["c", "b", "a"], output)

    def test_run_exception(self):
        self.assertRaises(CalledProcessError, run, self.test_file, "throw_exception")


if __name__ == "__main__":
    unittest.main()
