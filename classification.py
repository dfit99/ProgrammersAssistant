import nltk

syntax = {"String", "int", "for" "public", ":", ";" "private", "void", "def", "[]", "//",
          "yield", "raise", "return", "pass", "exec", "del", "lambda", "elif",
          "const", "char","float","implements", "interface", "long",
          "extends", "static", "super", "abstract", "boolean", "byte",
          "break", "the","of","to","a",
          }


def programming_features(document):
    features = {}
    document_words = [nltk.word_tokenize(line) for line in document]
    document_words = [val for sublist in document_words for val in sublist]

    for word in syntax:
        features['contains({})'.format(word)] = (word in document_words)

    return features


def train():
    import os
    train_set = []
    for file in os.listdir("classifier/python_train/"):
        with open("classifier/python_train/" + file, 'rb') as py_file:
            py_train = (programming_features(py_file), "Python")
            train_set.append(py_train)
    for file in os.listdir("classifier/java_train/"):
        with open("classifier/java_train/" + file, 'rb') as java_file:
            java_train = (programming_features(java_file), "Java")
            train_set.append(java_train)
    for file in os.listdir("classifier/english_train/"):
        with open("classifier/english_train/" + file, 'rb') as java_file:
            english_train = (programming_features(java_file), "English")
            train_set.append(english_train)
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    return classifier


def classify(classifier, document):
    return classifier.classify(programming_features(document))


def test(classifier):
    import os
    test_set = []
    for file in os.listdir("classifier/python_test/"):
        with open("classifier/python_test/" + file, 'rb') as py_file:
            py_test = (programming_features(py_file), "Python")
            test_set.append(py_test)
    for file in os.listdir("classifier/java_test/"):
        with open("classifier/java_test/" + file, 'rb') as java_file:
            java_test = (programming_features(java_file), "Java")
            test_set.append(java_test)
    for file in os.listdir("classifier/english_test/"):
        with open("classifier/english_test/" + file, 'rb') as java_file:
            english_test = (programming_features(java_file), "English")
            test_set.append(english_test)

    for file in os.listdir("classifier/mixed_python_test/"):
        with open("classifier/mixed_python_test/" + file, 'rb') as java_file:
            py_test = (programming_features(java_file), "Python")
            test_set.append(py_test)
    for file in os.listdir("classifier/mixed_java_test/"):
        with open("classifier/mixed_java_test/" + file, 'rb') as java_file:
            py_test = (programming_features(java_file), "Java")
            test_set.append(py_test)
    #print(classifier.pseudocode(depth=4))
    return nltk.classify.accuracy(classifier, test_set)

