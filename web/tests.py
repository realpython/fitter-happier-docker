import unittest
from app import app


class MainTestCase(unittest.TestCase):

    def test_two_and_two(self):
        four = 2 + 2
        self.assertEqual(four, 4)
        self.assertNotEqual(four, 5)

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
