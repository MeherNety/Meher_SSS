from random import randrange
def get_rand(max_val):
    if max_val < 0:
        return 1
    else:
        val_1 = randrange(max_val)
        val_2 = randrange(max_val)
        return val_1/val_2
# Creating Unit Test Cases
import unittest
class UnitTestCase(unittest.TestCase):
    def testnegative(self): #testing for negative numbers
        for i in range(-2000, -1):
            self.assertEqual(get_rand(i), 1)

    def testpositive(self): #testing for positive numbers
        try:
            for j in range(1, 2000):
                self.assertIsInstance(get_rand(j),float)
        except ZeroDivisionError:
            pass

    def testzero(self): # testing for number zero
        try:
            self.assertRaises(get_rand(0),1)
        except ValueError:
            pass