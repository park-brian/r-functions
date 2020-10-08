import asyncio
import sys
import unittest
from os import path
from r_functions import create_async, run_async

if sys.platform == "win32":
    asyncio.set_event_loop(asyncio.ProactorEventLoop())


class TestRAsync(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.test_file = path.join(path.dirname(__file__), "test.R")

    def test_create_add(self):
        params = {"a": 2, "b": 3}
        add = create_async(self.test_file, "add")
        output = self.loop.run_until_complete(add(**params))
        self.assertEqual(5, output)

    def test_create_reverse(self):
        params = [["a", "b", "c"]]
        reverse = create_async(self.test_file, "reverse")
        output = self.loop.run_until_complete(reverse(*params))
        self.assertEqual(["c", "b", "a"], output)

    def test_create_exception(self):
        throw_exception = create_async(self.test_file, "throw_exception")
        self.assertRaises(
            Exception,
            lambda: self.loop.run_until_complete(throw_exception()),
        )

    def test_run_add(self):
        params = {"a": 2, "b": 3}
        output = self.loop.run_until_complete(run_async(self.test_file, "add", params))
        self.assertEqual(5, output)

    def test_run_reverse(self):
        params = [["a", "b", "c"]]
        output = self.loop.run_until_complete(
            run_async(self.test_file, "reverse", params)
        )
        self.assertEqual(["c", "b", "a"], output)

    def test_run_exception(self):
        self.assertRaises(
            Exception,
            lambda: self.loop.run_until_complete(
                run_async(self.test_file, "throw_exception")
            ),
        )


if __name__ == "__main__":
    unittest.main()
