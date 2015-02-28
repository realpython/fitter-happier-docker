import unittest


class MainTestCase(unittest.TestCase):

    def test_two_and_two(self):
        four = 2 + 2
        self.assertEqual(four, 4)
        self.assertNotEqual(four, 5)
        self.assertNotEqual(four, 6)
        self.assertNotEqual(four, 22)

if __name__ == '__main__':
    unittest.main()
