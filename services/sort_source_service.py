
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class SortSourceService:
    def __init__(self):
        self.embedding_model=SentenceTransformer('all-miniLM-L6-v2')
    def sort_source(self, query:str,search_results:List[dict]):
        relevent_docs=[]
        query_embedding= self.embedding_model.encode(query)

        for result in search_results:
            res_embedding=self.embedding_model.encode(result['content'])

            similarity=np.dot(query_embedding,res_embedding)/(np.linalg.norm(query_embedding)*np.linalg.norm(res_embedding))

            result['relevence_score']=similarity

            if(similarity>0.45):
                relevent_docs.append(result)

        sorted_docs=sorted(relevent_docs,key=lambda x:x['relevence_score'],reverse=True)

        return sorted_docs