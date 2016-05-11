import os
from os import path
import pprint
from bs4 import BeautifulSoup
#given a java document in unicode text, parse through the text and gather methods+descriptions in dictionary, then return dict
def parse_java_text(full_text, text_name):
    method_header = False
    full_text = full_text.split("\n")
    file_methods = {}
    for line in full_text:

        method_signature = "("in line and line.strip().endswith(")")
        has_space = line.strip().find(" ")

        if method_signature and has_space<0:
            method_header=True
            current_description = ""
            method = line.strip("\n")
            file_methods[method] = current_description
            #print line
        elif method_header==True:
            if len(file_methods[method])>150:
                method_header=False
            else:
                file_methods[method]+=line.strip()
        elif line.isspace() or not method_signature:
            method_header==False
        else:
            method_header==False
    return file_methods

#parse through the python documentation and collect methods+descriptions for each document, return as dict
def parse_python_docs():
    doc_dict={}
    for filename in os.listdir("library/python"):

        filepath = path.relpath('library/python/'+filename)
        with open(filepath, 'r') as k:
            method_header = False
            txt_tag = filename.find(".txt")
            clean_file_name = filename[0:txt_tag]
            doc_dict[clean_file_name]={}
            file_methods = doc_dict[clean_file_name]
            for line in k:
                indented = line.startswith(" ")
                method_signature = "("in line and line.strip().endswith(")")
                if not indented and method_signature:
                    method_header=True
                    current_description = ""
                    method = line.strip()
                    file_methods[method] = current_description
                    print line
                elif indented and method_header==True:
                    file_methods[method]+=line.strip()
                else:
                    pass
            pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(doc_dict[clean_file_name])
    return doc_dict
#parse through the java documentation and collect methods + descriptions for each java doc, return as dict
def parse_java_docs():
    java_dict={}
    pp = pprint.PrettyPrinter(indent=4)
    for path, dirs, files in os.walk("library/java/"):
        for filename in files:
            fullpath = os.path.join(path, filename)
            with open(fullpath, 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
                full_text = soup.get_text()
                html_tag = filename.find(".html")
                clean_file_name = filename[0:html_tag]

                print clean_file_name, "hey over here"
                #print full_text
                full_text = full_text.encode('ascii','ignore')
                doc_dict = parse_java_text(full_text,clean_file_name)
                if doc_dict:
                    java_dict[clean_file_name]=doc_dict

                    #pp.pprint(java_dict[clean_file_name])
    return java_dict
#java_dict = parse_java_docs()
#print len(java_dict)
