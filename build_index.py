from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, csv
import testLanguageCode
with open('es_mapping', 'r') as outfile:
    SCHEMA = json.load(outfile)

class BuildIndex:

    def __init__(self, index_name, schema): #mantain some state for practical purposes
        self.index_name = index_name
        self.es = es = Elasticsearch()
        self.schema = schema

    def init_index(self): #create index
        self.es.indices.create(index=self.index_name, body=self.schema)

    def delete_index(self, indices="*"): #clear all indices for hygiene purposes
        self.es.indices.delete(indices)

    def format_action(self, value): #insertion helper
        return {
            '_op_type': 'create',
            "_index": self.index_name,
            "_type": "posts",
            "body": value.get("body", ""),
            "source_code": value.get("source_code", False),
           }

    def bulk_insert(self): #insert all documents from the movies json
        actions = []
        for i in range(1, 13):
            with open("month"+str(i)+".csv", 'r', encoding='utf8') as datafile:
                csv_file_obj = csv.reader(datafile)
                csv.field_size_limit(500 * 1024 * 1024)
                for row in csv_file_obj:
                    v = {'body': row, 'source_code': testLanguageCode.get_languages(row)}
                    actions.append(self.format_action(v)) #add new document into array
        return helpers.bulk(self.es, actions, stats_only=True) #perform bulk insert Input: array of nested dictionaries



if __name__ == '__main__':
    import sys
    new_index = BuildIndex('may_2015',SCHEMA) #take index name from command line
    new_index.delete_index()
    new_index.init_index()
    new_index.bulk_insert()
