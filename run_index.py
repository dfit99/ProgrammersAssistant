from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

INDEX_NAME = 'may_2015'
DOC_TYPE = 'posts'
ES = Elasticsearch()


def q_total(size=0):  # returns total count for all docs
    query = json.dumps({"query": {"match_all": {}}})
    return ES.count(index=INDEX_NAME, doc_type='methods', body=query)


def q_field(body, language, doc_type='posts', offset=0, size=10):  # returns match for key value pair
    if str(language) != str(None):
        query = json.dumps({"from": offset, "size": size,
                            "query": {"bool": {
                                "must": {
                                    "match": {"body": body}
                                },
                                "filter": {
                                    "term": {"language": language}
                                },

                            }}})
    else:
        query = json.dumps({"from": offset, "size": size,
                            "query": {"match": {"body": {'query': body}}}
                            })
    return ES.search(index=INDEX_NAME, doc_type=doc_type, body=query)


def q_field_methods(description, language, doc_type='methods', offset=0, size=10):  # returns match for key value pair

    if str(language) != str(None):
        query = json.dumps({"from": offset, "size": size,
                            "query": {"bool": {
                                "must": {
                                    "match": {"description": description}
                                },
                                "filter": {
                                    "term": {"language": language}
                                },

                            }}})
    else:
        query = json.dumps({"from": offset, "size": size,
                            "query": {"match": {"description": {'query': description}}}

                            })
    return ES.search(index=INDEX_NAME, doc_type=doc_type, body=query)


# def q_field(key, value):  # returns match for key value pair
#     query = json.dumps({"query": {
#         "function_score": {
#             "query": {"match": {key: {'query': value, 'operator': 'and'}},
#                       },
#             "boost_mode": "multiply",
#             "functions": [
#                 {
#                     # "filter": {'source_code': True},
#                  "script_score": {
#                         "script": "_score  * 1.5"
#                     }
#                 }],
#
#         }
#
#     }})
#     return ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query)


from flask import Flask, render_template
from flask import request, redirect, url_for, abort

app = Flask(__name__)


@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html')


@app.route("/search", methods=["POST"])
def srp():
    try:
        query = request.form['Search']

        try:
            type = request.form['type']
        except KeyError:
            type = 'posts'
        try:
            offset = request.form['offset']
        except KeyError:
            offset = 0

        try:
            language = request.form['language']
        except KeyError:
            language = None
        try:
            type = request.form['type']
        except KeyError:
            type = "posts"

        if type == 'posts':
            results = q_field(query, language, type, offset)
        else:
            results = q_field_methods(query, language, type, offset)

        total = str(results['hits']['total'])  # get total hits count
        offset = int(offset) + 10

        if type == "posts":
            return render_template('srp.html', type=type, total=total, raw=query, language=language, offset=offset,
                                   my_list=results['hits']['hits'])
    except Exception:
        abort(405)
    return render_template('srp2.html', type=type, total=total, raw=query, language=language, offset=offset,
                           my_list=results['hits']['hits'])


@app.route("/")
def load_base():
    return render_template('home.html')


if __name__ == '__main__':
    import sys

    debug = False
    app.run(debug=debug)
