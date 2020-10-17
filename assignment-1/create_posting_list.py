import pandas as pd
import numpy as np
from tqdm import tqdm
import json

class posting_list:
    def __init__(self,csv_path):
        self.df = pd.read_csv(csv_path, keep_default_na=False)
        self.df.columns = ['ID','Text']
        
    def _terms_frequency_in_document(self,text):
        doc_specific_dict = {}
        doc_id = text[0]
        for i in text[1].split(' '):
            try:
                doc_specific_dict[i] += 1
            except:
                doc_specific_dict[i] = 1
        res = {}
        for i in doc_specific_dict:
            try:
                res[i][doc_id]=doc_specific_dict[i]
            except:
                res[i]={}
                res[i][doc_id]=doc_specific_dict[i]
        return res
    
    def _merge_dicts(self, dict_1, dict_2):
        for i in dict_2:
            if i not in dict_1:
                dict_1[i] = dict_2[i]
            else:
                dict_1_1=dict_1[i]
                dict_2_1=dict_2[i]
                for j in dict_2_1:
                    if j not in dict_1_1:
                        dict_1[i][j]=dict_2_1[j]
                    else:
                        dict_1[i][j]+=dict_2_1[j]
        return dict_1
    
    def return_posting_list(self):
        d1 = self._terms_frequency_in_document(self.df.iloc[0])
        for i in tqdm(range(1,int(len(self.df)))):
            d1 = self._merge_dicts(d1,self._terms_frequency_in_document(self.df.iloc[i]))
        return d1

if __name__=='__main__':
    postingObj = posting_list('./data.csv')

    with open('./posting_list.json', 'w') as fp:
        json.dump(postingObj.return_posting_list(), fp)
