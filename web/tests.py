import unittest


class MainTestCase(unittest.TestCase):

    def silly_test(self):
        five = 2 + 2  # two and two always equals five
        self.assertEqual(five, 5)
        self.assertNotEqual(five, 4)


if __name__ == '__main__':
    unittest.main()
