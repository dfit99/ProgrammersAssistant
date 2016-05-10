
import nltk

syntax = {"and","del","is", "from","not","public" "private" ,"{" , "}",";", "svoid", "print" "def", "static", "throws", "instanceof", "if", "||", "for", "int"}

def programming_features(document):
    features = {}
    document_words = [nltk.word_tokenize(line) for line in document]
    document_words = [val for sublist in document_words for val in sublist]

    for word in syntax:
        features['contains({})'.format(word)] = (word in document_words)
    return features

def train():
    train_set = []
    with open("py_train.txt", 'r') as py_file:
        py_train = (programming_features(py_file), "Python")
        train_set.append(py_train)
    with open("java_train", 'r') as java_file:
        java_train = (programming_features(java_file), "Java")
        train_set.append(java_train)
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    with open("py_test", 'r') as java_file:
        print classifier.classify(programming_features(java_file))

train()