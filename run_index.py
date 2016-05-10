from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import re

INDEX_NAME = 'programmers_assistant'
DOC_TYPE = 'posts'
ES = Elasticsearch()


def q_total(size=0): #returns total count for all docs
    query = json.dumps({"query": {"match_all": {}}})
    return ES.count(index=INDEX_NAME, doc_type=DOC_TYPE, body=query)


def q_field(key, value): #returns match for key value pair
    query = json.dumps({"query": {
        "query": {"match": {key: {'query': value, 'operator': 'and'}},
                  }
    }})
    return ES.search(index=INDEX_NAME, doc_type=DOC_TYPE, body=query)

from flask import Flask, render_template
from flask import request, redirect, url_for, abort

app = Flask(__name__)

@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html')


@app.route("/search", methods=["POST"])
def srp():
    query = request.form['Search']

    results = q_field('body', query )
    #print(q_total())
    total = (results['hits']['total'])  # get total hits count
    new_res = []
    res = results['hits']['hits']
    #test = ["\\\n\nwtf this should be escaped \n\n why oh why is this being ignored?","hey you yeah you \t what are you\'re thoughts on socialism"]
    for i in res:
        thread =  i['_source']['body'].encode('ascii','ignore')
        #print thread, "\n\n", thread.__class__
        new_res.append(thread)
    
    return render_template('srp.html', total=total,  my_list=new_res)


@app.route("/")
def load_base():
    return render_template('base.html')



if __name__ == '__main__':
    import sys
    debug = False
    app.run(debug=True)
