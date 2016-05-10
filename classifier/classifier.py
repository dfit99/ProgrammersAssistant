import nltk

syntax = {"String", "int", "for" "public", "private", "void", "def", "[]", "//"}


def programming_features(document):
    features = {}
    document_words = [nltk.word_tokenize(line) for line in document]
    document_words = [val for sublist in document_words for val in sublist]

    for word in syntax:
        features['contains({})'.format(word)] = (word in document_words)
    print features



    return features


def train():
    train_set = []
    with open("py_train.txt", 'r') as py_file:
        py_train = (programming_features(py_file), "Python")
        train_set.append(py_train)
    with open("java_train", 'r') as java_file:
        java_train = (programming_features(java_file), "Java")
        train_set.append(java_train)
    with open("english_train", 'r') as english_file:
        english_train = (programming_features(english_file), "English")
        train_set.append(english_train)
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    return classifier


def classify(classifier, document):
    return classifier.classify(programming_features(document))

train()