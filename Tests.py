from WikiFetch import *
import unittest


class TestGetJson(unittest.TestCase):

	#Test a null input
	def test_nullPageId(self):

		with self.assertRaises(MissingPage):
			WikiFetch._getJson(None,None)

	#Test a not-a-number input
	def test_nan(self):
		with self.assertRaises(MissingPage):
			WikiFetch._getJson(None,"gabriel")

	#Test a decimal number:
	def test_bellowZero(self):
		with self.assertRaises(MissingPage):
			WikiFetch._getJson(None,3.14)

	#Test a negative number:
	def test_bellowZero(self):
		with self.assertRaises(MissingPage):
			WikiFetch._getJson(None,-1)

	#Test zero input			
	def test_zero(self):
		with self.assertRaises(MissingPage):
			WikiFetch._getJson(None,0)

	#Test arbitrary low index non-existent query
	def test_lowIndex(self):
		with self.assertRaises(MissingPage):
			WikiFetch._getJson(None,1)

	#Test query without internet connection
	def test_noConnection(self):
		with self.assertRaises(ConnError):
			WikiFetch._getJson(None,21721040)						

class TestProcessData(unittest.TestCase):

	#Test Null input
	def test_nullInput(self):
		with self.assertRaises(AttributeError):
			WikiFetch._processData(None,None)

	#Test One word string input
	def test_oneWord(self):
		
		oneWordList = ['hello']
		outputDictionary = {}
		outputDictionary[1] = oneWordList
	
		self.assertEqual(WikiFetch._processData(None,"hello"),outputDictionary)

	#Test More than one word input
	def test_onePlusWords(self):
		firstList = ['hello','world']
		secondList = ['beautiful']
		outputDictionary = {}
		outputDictionary[2] = firstList
		outputDictionary[1] = secondList

		self.assertEqual(WikiFetch._processData(None,"hello! world?, (hello) beautiful world."),outputDictionary)		

class TestPrintResult(unittest.TestCase):

	#Test Null data input excecution
	def test_nullDictionaryInput(self):
		with self.assertRaises(TypeError):
			WikiFetch._printResult(None,5,None,"Title","URL")

	#Test Asking more results than the available.
	def test_moreRows(self):
		
		wordList1 = ['first','second']		
		wordList2 = ['third']
		
		dataInput = {}
				
		dataInput[15] = wordList1
		dataInput[9] = wordList2
		
		with self.assertRaises(NotEnoughRows):
			WikiFetch._printResult(None,3,dataInput,"Title","URL")

if __name__ == '__main__':
	unittest.main()