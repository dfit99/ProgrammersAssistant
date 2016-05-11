from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json, csv
import testLanguageCode
import classification
import sys
from doc_parser import parse_python_docs, parse_java_docs
import pprint

reload(sys)
sys.setdefaultencoding('utf8')
with open('es_mapping', 'r') as outfile:
    SCHEMA = json.load(outfile)


class BuildIndex:
    def __init__(self, index_name, schema):  # mantain some state for practical purposes
        self.index_name = index_name
        self.es = es = Elasticsearch()
        self.schema = schema

    def init_index(self):  # create index
        self.es.indices.create(index=self.index_name, body=self.schema)

    def delete_index(self, indices="*"):  # clear all indices for hygiene purposes
        self.es.indices.delete(indices)

    def format_comment(self, value):  # insertion helper
        return {
            '_op_type': 'create',
            "_index": self.index_name,
            "_type": "posts",
            "body": value.get("body", ""),
            "source_code": value.get("source_code", False),
            "language": value.get("language", 'English')
        }
    def format_documentation(self, name,description,title,language):  # insertion helper
        return {
            '_op_type': 'create',
            "_index": self.index_name,
            "_type": "methods",
            "name": name,
            "description": description,
            "title":title,
            "language": language
        }

    def bulk_insert(self):  # insert all documents from the movies json
        model = classification.train()

        actions = []
        for i in range(1, 2):
            with open("month" + str(i) + ".csv", 'rb') as datafile:
                csv_file_obj = csv.reader(datafile)
                csv.field_size_limit(500 * 1024 * 1024)
                for row in csv_file_obj:
                    try:
                        v = {'body': '\n'.join(row), 'source_code': testLanguageCode.get_languages(row),
                         'language': classification.classify(model, row)}
                    except UnicodeDecodeError:
                        print "unicode error"

                    actions.append(self.format_comment(v))  # add new document into array
        python_dict = parse_python_docs()
        for key in python_dict:
            name = key
            document = python_dict[key]
            for method in document:
                description = document[method]
                actions.append(self.format_documentation(method,description,name,"Python"))
        java_dict = parse_java_docs()
        for key in java_dict:
            name = key
            document = java_dict[key]
            for method in document:
                description = document[method]
                actions.append(self.format_documentation(method,description,name,"Java"))

        return helpers.bulk(self.es, actions,
                            stats_only=True)  # perform bulk insert Input: array of nested dictionaries





if __name__ == '__main__':
    import sys

    new_index = BuildIndex('may_2015', SCHEMA)  # take index name from command line
    new_index.delete_index()
    new_index.init_index()
    #test_doc()
    new_index.bulk_insert()
