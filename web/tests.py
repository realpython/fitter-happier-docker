import unittest


class MainTestCase(unittest.TestCase):

    def silly_test(self):
        four = 2 + 2
        self.assertEqual(four, 4)
        self.assertNotEqual(four, 5)


if __name__ == '__main__':
    unittest.main()
