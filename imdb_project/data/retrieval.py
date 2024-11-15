import numpy as np
import pandas as pd

class BaseRetrieval:
    # this class is the base for different ways of retrieving documents (movies in this case)
    def __init__(self, random_state=None):
        # initializes the class and sets the random state for reproducibility
        self.random_state = random_state
        
    def score(self, y_true, y_pred):
        # this function calculates the accuracy of our predictions
        # y_true is the correct answers (documents), and y_pred are the predicted ones
        
        values = np.empty((len(y_true,)))  # create an empty array to store our scores
        for i, _ in enumerate(y_true):  # loop through each query
            # for each query check how many predicted documents match the true ones
            values[i] = len(np.intersect1d(y_pred[i], y_true[i])) / len(y_pred)  
        score = np.mean(values)  # take the average score across all queries
        return score


class RandomRetrieval(BaseRetrieval):
    # class that randomly selects documents (movies) from the dataset
    def __init__(self, n=4, random_state=None):
        # initialize with n as the number of random movies to select and random_state for reproducibility
        super().__init__(random_state)
        self.n = n
    
    def predict(self, documents):
        # function to select n random movies from the documents (dataset)
        
        np.random.seed(self.random_state)  # set the SEED! for random selection so it's repeatable
        # randomly samples n movies and return them as a list of pandas Series (each Series is a set of movies)
        return [documents.sample(self.n).reset_index(drop=True)]


class TermFrequencyRetrieval(BaseRetrieval):
    # class select documents based on how similar they are to a given query, using word frequency
    def __init__(self, n=4, random_state=None):
        # initializes with n as the number of similar movies to retrieve and random_state for reproducibility
        super().__init__(random_state)
        self.n = n
        self.vocabulary = None  # to store all the unique words from the movie descriptions
        self.term_frequency = None  # store how often each word appears in each document
    
    def fit(self, documents):
        # this function creates the vocabulary and term frequency matrix from movie descriptions
        
        vocabulary = set(' '.join(documents).split(' '))  # get all unique words from the documents
        term_frequency = np.zeros((len(documents), len(vocabulary)))  # greate an empty matrix for word frequencies
        vocabulary = dict(zip(vocabulary, range(len(vocabulary))))  # map each word to a unique index
        
        for i, txt in enumerate(documents):  # loop through each document (movie description)
            for word in txt.split(' '):  # split the description into words
                term_frequency[i][vocabulary[word]] += 1  # count how many times each word appears
        term_frequency /= term_frequency.sum(axis=1, keepdims=True)  # normalise each row (document) so that the sum of words is 1
        
        self.vocabulary = vocabulary  # store vocabulary
        self.term_frequency = term_frequency  # store the term frequency matrix
        
    def predict(self, query):
        # function to predict the most similar movies based on the query

        query_words = [self.vocabulary.get(word) for word in query.split() if word in self.vocabulary]
        # gt the index for each word in the query if it exists in the vocabulary
        if not query_words:
            return []  # if none of the query words are in the vocabulary return an empty list

        similarity = self.term_frequency[:, query_words].sum(axis=1)  # clculate similarity based on word frequencies
        predictions = similarity.argsort()[-self.n:][::-1]  # sort the documents by similarity and pick the top n
        return predictions  # return the most similar documents
