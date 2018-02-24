import unittest

import my_functions

class TestMyFunc(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_increment_one_1(self): 
        self.assertEqual( my_functions.increment_by_one(1), 2)
  
    def test_increment_one_2(self):
        self.assertEqual( my_functions.increment_by_one(0), 1)

if __name__ == '__main__':
    unittest.main()
