import pyjion
import unittest


class FunctionCallsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pyjion.enable()

    def tearDown(self) -> None:
        pyjion.disable()

    def test_arg0(self):
        def arg0() -> int:
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d

        self.assertEqual(arg0(), 10)
        info = pyjion.info(arg0)
        self.assertTrue(info['compiled'])

    def test_arg1(self):
        def arg1(e):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e

        self.assertEqual(arg1(5), 15)
        info = pyjion.info(arg1)
        self.assertTrue(info['compiled'])

    def test_arg2(self):
        def arg2(e, f):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f

        self.assertEqual(arg2(5, 6), 21)
        info = pyjion.info(arg2)
        self.assertTrue(info['compiled'])

    def test_arg3(self):
        def arg3(e, f, g):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g

        self.assertEqual(arg3(5, 6, 7), 28)
        info = pyjion.info(arg3)
        self.assertTrue(info['compiled'])

    def test_arg4(self):
        def arg4(e, f, g, h):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h

        self.assertEqual(arg4(5, 6, 7, 8), 36)
        info = pyjion.info(arg4)
        self.assertTrue(info['compiled'])

    def test_arg5(self):
        def arg5(e, f, g, h, i):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i

        self.assertEqual(arg5(5, 6, 7, 8, 9), 45)
        info = pyjion.info(arg5)
        self.assertTrue(info['compiled'])

    def test_arg6(self):
        def arg6(e, f, g, h, i, j):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i + j

        self.assertEqual(arg6(5, 6, 7, 8, 9, 10), 55)
        info = pyjion.info(arg6)
        self.assertTrue(info['compiled'])

    def test_arg7(self):
        def arg7(e, f, g, h, i, j, k):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i + j + k

        self.assertEqual(arg7(5, 6, 7, 8, 9, 10, 11), 66)
        info = pyjion.info(arg7)
        self.assertTrue(info['compiled'])

    def test_arg8(self):
        def arg8(e, f, g, h, i, j, k, l):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i + j + k + l

        self.assertEqual(arg8(5, 6, 7, 8, 9, 10, 11, 12), 78)
        info = pyjion.info(arg8)
        self.assertTrue(info['compiled'])

    def test_arg9(self):
        def arg9(e, f, g, h, i, j, k, l, m):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i + j + k + l + m

        self.assertEqual(arg9(5, 6, 7, 8, 9, 10, 11, 12, 13), 91)
        info = pyjion.info(arg9)
        self.assertTrue(info['compiled'])

    def test_arg10(self):
        def arg10(e, f, g, h, i, j, k, l, m, n):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i + j + k + l + m + n

        self.assertEqual(arg10(5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 105)
        info = pyjion.info(arg10)
        self.assertTrue(info['compiled'])

    def test_arg11(self):
        def arg11(e, f, g, h, i, j, k, l, m, n, o):
            a = 1
            b = 2
            c = 3
            d = 4
            return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o

        self.assertEqual(arg11(5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), 120)
        info = pyjion.info(arg11)
        self.assertTrue(info['compiled'])


class MethodCallsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pyjion.enable()

    def tearDown(self) -> None:
        pyjion.disable()

    def test_arg0(self):
        class F:
            @classmethod
            def arg0(cls) -> int:
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d

        self.assertEqual(F.arg0(), 10)
        info = pyjion.info(F.arg0.__code__)
        self.assertTrue(info['compiled'])

    def test_arg1(self):
        class F:
            @classmethod
            def arg1(cls, e):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e

        self.assertEqual(F.arg1(5), 15)
        info = pyjion.info(F.arg1.__code__)
        self.assertTrue(info['compiled'])

    def test_arg2(self):
        class F:
            @classmethod
            def arg2(cls, e, f):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f

        self.assertEqual(F.arg2(5, 6), 21)
        info = pyjion.info(F.arg2.__code__)
        self.assertTrue(info['compiled'])

    def test_arg3(self):
        class F:
            @classmethod
            def arg3(cls, e, f, g):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g

        self.assertEqual(F.arg3(5, 6, 7), 28)
        info = pyjion.info(F.arg3.__code__)
        self.assertTrue(info['compiled'])

    def test_arg4(self):
        class F:
            @classmethod
            def arg4(cls, e, f, g, h):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h

        self.assertEqual(F.arg4(5, 6, 7, 8), 36)
        info = pyjion.info(F.arg4.__code__)
        self.assertTrue(info['compiled'])

    def test_arg5(self):
        class F:
            @classmethod
            def arg5(cls, e, f, g, h, i):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i

        self.assertEqual(F.arg5(5, 6, 7, 8, 9), 45)
        info = pyjion.info(F.arg5.__code__)
        self.assertTrue(info['compiled'])

    def test_arg6(self):
        class F:
            @classmethod
            def arg6(cls, e, f, g, h, i, j):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i + j

        self.assertEqual(F.arg6(5, 6, 7, 8, 9, 10), 55)
        info = pyjion.info(F.arg6.__code__)
        self.assertTrue(info['compiled'])

    def test_arg7(self):
        class F:
            @classmethod
            def arg7(cls, e, f, g, h, i, j, k):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i + j + k

        self.assertEqual(F.arg7(5, 6, 7, 8, 9, 10, 11), 66)
        info = pyjion.info(F.arg7.__code__)
        self.assertTrue(info['compiled'])

    def test_arg8(self):
        class F:
            @classmethod
            def arg8(cls, e, f, g, h, i, j, k, l):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i + j + k + l

        self.assertEqual(F.arg8(5, 6, 7, 8, 9, 10, 11, 12), 78)
        info = pyjion.info(F.arg8.__code__)
        self.assertTrue(info['compiled'])

    def test_arg9(self):
        class F:
            @classmethod
            def arg9(cls, e, f, g, h, i, j, k, l, m):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i + j + k + l + m

        self.assertEqual(F.arg9(5, 6, 7, 8, 9, 10, 11, 12, 13), 91)
        info = pyjion.info(F.arg9.__code__)
        self.assertTrue(info['compiled'])

    def test_arg10(self):
        class F:
            @classmethod
            def arg10(cls, e, f, g, h, i, j, k, l, m, n):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i + j + k + l + m + n

        self.assertEqual(F.arg10(5, 6, 7, 8, 9, 10, 11, 12, 13, 14), 105)
        info = pyjion.info(F.arg10.__code__)
        self.assertTrue(info['compiled'])

    def test_arg11(self):
        class F:
            @classmethod
            def arg11(cls, e, f, g, h, i, j, k, l, m, n, o):
                a = 1
                b = 2
                c = 3
                d = 4
                return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o

        self.assertEqual(F.arg11(5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), 120)
        info = pyjion.info(F.arg11.__code__)
        self.assertTrue(info['compiled'])


if __name__ == "__main__":
    unittest.main()
