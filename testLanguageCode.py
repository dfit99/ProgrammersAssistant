from pygments.lexers import guess_lexer
import re


with open("sample_code.txt") as f:
    line = f.read()
    comments = line.split("\",\"")

def get_languages(comments):

    for comment in comments:
        line = re.sub('\"','', comment)
        try:
            guess_lexer(line)
        except:
            pass
        else:
            return True
    return False

print(get_languages(comments))
