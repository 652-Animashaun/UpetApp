import unittest
from api_test_pagination import pagination_test, git_get_test

class Tests(unittest.TestCase):

    def test_1(self):
        """Check that 1 is not prime."""
        self.assertTrue(pagination_test(10))

    def test_2(self):
    	self.assertTrue(git_get_test(5))

if __name__ == "__main__":
    unittest.main()