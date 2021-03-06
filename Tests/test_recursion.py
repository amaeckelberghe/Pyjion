import pyjion
import unittest


class RecursionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pyjion.enable()

    def tearDown(self) -> None:
        pyjion.disable()

    def test_basic(self):
        def _f():
            def add_a(z):
                if len(z) < 5:
                    z.append('a')
                    return add_a(z)
                return z
            return add_a([])

        self.assertEqual(_f(), ['a', 'a', 'a', 'a', 'a'])
        info = pyjion.info(_f)
        self.assertTrue(info['compiled'])


if __name__ == "__main__":
    unittest.main()
