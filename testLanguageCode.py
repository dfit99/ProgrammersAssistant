from pygments.lexers import guess_lexer
import re


with open("sample_code.txt") as f:
    line = f.read()
    comments = line.split("\",\"")

for comment in comments:
    line = re.sub('\"','', comment)
    try:
        print guess_lexer(line)
        #print line, "\n|\n|\n|\n"
    except:        
        print "no language found!"
