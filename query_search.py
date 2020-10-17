from tfidf import Tfidf
import numpy as np
import operator
from tqdm import tqdm

def find_best_doc(data_dict):
	'''
		Find sum of all tf-idfs of all words in data_dict for all documents.
	'''
	
	# Dictionary. {docid: (sum of tf-idf of all words from query)}
	lst_tfidf = {}
	for key in tqdm(data_dict):
		for docid in data_dict[key]:
			try:
				lst_tfidf[docid] += TfidfObj.tfidf(key,docid)
			except:
				lst_tfidf[docid] = TfidfObj.tfidf(key,docid)
	
	# Sorting dictionary in descending manner
	lst_tfidf = {k: v for k, v in sorted(lst_tfidf.items(), key=lambda item: -1*item[1])}
	for jey in lst_tfidf:
		return (jey, lst_tfidf[jey])

def search_query(query,data_dict):
	'''
		Assuming query is similar to N:new* | new*
	'''
	temp = query.split(':')
	res = {}
	if(temp[0]=='P'):
		res = {key:val for key, val in data_dict.items()  
			if key.startswith('person_'+temp[-1].split('*')[0])}
	elif(temp[0]=='O'):
		res = {key:val for key, val in data_dict.items()  
			if key.startswith('org_'+temp[-1].split('*')[0])}
	elif(temp[0]=='L'):
		res = {key:val for key, val in data_dict.items()  
			if key.startswith('loc_'+temp[-1].split('*')[0])}
	elif(temp[0]=='N'):
		res = {	
				key:val for key, val in data_dict.items()  
				if (key.startswith('person_'+temp[-1].split('*')[0]) 
				or key.startswith('loc_'+temp[-1].split('*')[0]) 
				or key.startswith('org_'+temp[-1].split('*')[0]))
			}
	else:
		res = {key:val for key, val in data_dict.items()  
			if key.startswith(temp[-1].split('*')[0])}

	print('Refined posting list to relevant queries')
	return find_best_doc(res)

if __name__=='__main__':
	TfidfObj = Tfidf('./posting_list.json', './data.csv')
	print(search_query('O:cbs*',data_dict=TfidfObj.data))