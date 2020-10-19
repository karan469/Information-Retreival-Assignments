from tfidf import Tfidf
import numpy as np
import operator
from tqdm import tqdm

class QuerySearch(object):
	"""docstring for QuerySearch"""
	def __init__(self, posting_list_path, data_path):
		super(QuerySearch, self).__init__()
		self.posting_list_path = posting_list_path
		self.data_path = data_path
		self.TfidfObj = Tfidf(self.posting_list_path, self.data_path)
		
	def find_best_doc(self, data_dict, num_docs_retrieval=2):
		'''
			Find sum of all tf-idfs of all words in data_dict for all documents.
		'''
		
		# Dictionary. {docid: (sum of tf-idf of all words from query)}
		lst_tfidf = {}
		for key in (data_dict):
			for docid in data_dict[key]:
				try:
					lst_tfidf[docid] += self.TfidfObj.tfidf(key,docid)
				except:
					lst_tfidf[docid] = self.TfidfObj.tfidf(key,docid)
		
		# Sorting dictionary in descending manner
		# lst_tfidf = {k: v for k, v in sorted(lst_tfidf.items(), key=lambda item: -1*item[1])}
		arr = sorted(lst_tfidf.items(), key=lambda item: -1*item[1])
		return arr[:num_docs_retrieval]

	def search_query(self, query):
		'''
			Assuming query is similar to N:new* | new*
		'''
		temp = query.split(':')
		res = {}
		if(temp[0]=='P'):
			res = {key:val for key, val in self.TfidfObj.data.items()  
				if key.startswith('person_'+temp[-1].split('*')[0])}
		elif(temp[0]=='O'):
			res = {key:val for key, val in self.TfidfObj.data.items()  
				if key.startswith('org_'+temp[-1].split('*')[0])}
		elif(temp[0]=='L'):
			res = {key:val for key, val in self.TfidfObj.data.items()  
				if key.startswith('loc_'+temp[-1].split('*')[0])}
		elif(temp[0]=='N'):
			res = {	
					key:val for key, val in self.TfidfObj.data.items()  
					if (key.startswith('person_'+temp[-1].split('*')[0]) 
					or key.startswith('loc_'+temp[-1].split('*')[0]) 
					or key.startswith('org_'+temp[-1].split('*')[0]))
				}
		else:
			res = {key:val for key, val in self.TfidfObj.data.items()  
				if key.startswith(temp[-1].split('*')[0])}
		# print('Refined posting list to relevant queries')
		return self.find_best_doc(res)

	def search_queries(self, queries, num_docs_retrieval=2):
		res = {}
		for query in queries:
			temp = query.split(':')
			if(len(temp)>1):
				res = dict({key:val for key, val in self.TfidfObj.data.items()  
						if (temp[0]=='P' and key.startswith('person_'+temp[-1].split('*')[0]))
						or (temp[0]=='O' and key.startswith('org_'+temp[-1].split('*')[0]))
						or (temp[0]=='L' and key.startswith('loc_'+temp[-1].split('*')[0]))
						or (temp[0]=='N' and (key.startswith('person_'+temp[-1].split('*')[0]) 
						or key.startswith('loc_'+temp[-1].split('*')[0]) 
						or key.startswith('org_'+temp[-1].split('*')[0])))
					}, **res)
			else:
				res = dict({key:val for key, val in self.TfidfObj.data.items()  
					if key.startswith(temp[-1].split('*')[0])}, **res)
		return self.find_best_doc(res, num_docs_retrieval=num_docs_retrieval)


if __name__=='__main__':
	queryObj = QuerySearch('./posting_list.json', './data.csv')
	print(queryObj.search_queries(['O:cbs*' ,'mit*']))
