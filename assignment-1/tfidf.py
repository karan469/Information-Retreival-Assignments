from create_posting_list import posting_list
import json
import math
import pandas as pd

class Tfidf(object):
	"""docstring for Tfidf"""
	def __init__(self, posting_list_path, data_path):
		super(Tfidf, self).__init__()
		self.posting_list_path = posting_list_path
		
		with open(self.posting_list_path) as json_file: 
			self.data = json.load(json_file)

		print('json loaded')
		
		df = pd.read_csv(data_path)
		self.num_files = len(df)
		del df
		print('Posting list loaded...')
		
	def tf(self, word, docid):
		if(word not in self.data or docid not in self.data[word]):
			return math.log(1)
		word_dict = self.data[word]
		return math.log(1+self.data[word][docid])

	def idf(self, word):
		if word not in self.data:
			dfi = 1
		else:
			dfi = 1+len(self.data[word])
		return math.log(1+self.num_files/(dfi))

	def tfidf(self, word, docid):
		return self.tf(word, docid)*self.idf(word)

if __name__=='__main__':
	TfidfObj = Tfidf('./posting_list.json', './data.csv')
	print(TfidfObj.tfidf('and','AP880212-0'))