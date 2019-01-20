import unittest
import sys
sys.path.insert(0, '../')

import main_DCF

class TestDCF ( unittest.TestCase ):
	def test_presentValue(self):
		#pV = main_DCF.presentVal( futureVal ,rate, time ):
		
		self.assertAlmostEqual( 8065.096007, main_DCF.presentVal( 10808, 5, 6), places=6)
		self.assertAlmostEqual( 9160.482332, main_DCF.presentVal( 10808.57, 2.5, 6.7), places=6)

if __name__ == "__main__":
	unittest.main()
