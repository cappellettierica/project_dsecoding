import numpy as np
import pandas as pd

class BaseRetrieval:
    """
    The base method for retrieving documents given a certain query.
    """
    def __init__(self, random_state=None):
        self.random_state = random_state
        
    def score(self, y_true, y_pred):
        """
        Evaluate the performance of the model computing a score.

        Parameters
        ----------
        y_true: iter of iter of int
            The correct documents associated to each query.
        y_pred: iter of iter of int
            The predicted documents associated to each query.
            
        Returns
        -------
        score: float
            A score representing the ratio between corrected predicted
            over total predictions.
        """
        values = np.empty((len(y_true,)))
        for i, _ in enumerate(y_true):
            values[i] = len(np.intersect1d(y_pred[i], y_true[i])) / len(y_pred)
        score = np.mean(values)
        return score


class RandomRetrieval(BaseRetrieval):
    """
    A method for retrieving `n` random movies for a quiz.
    """
    def __init__(self, n=4, random_state=None):
        super().__init__(random_state)
        self.n = n
    
    def predict(self, documents):
        """
        Predict a set of random movies for each query.

        Parameters
        ----------
        documents: pd.DataFrame
            A dataframe representing movies (documents).
            
        Returns
        -------
        predictions: list of pd.Series
            For each query, a random sample of movies.
        """
        np.random.seed(self.random_state)
        return [documents.sample(self.n).reset_index(drop=True)]


class TermFrequencyRetrieval(BaseRetrieval):
    """
    A method for retrieving movies based on similarity with a query, using term frequency.
    """
    def __init__(self, n=4, random_state=None):
        super().__init__(random_state)
        self.n = n
        self.vocabulary = None
        self.term_frequency = None
    
    def fit(self, documents):
        """
        Build a term frequency matrix from movie overviews.

        Parameters
        ----------
        documents: pd.Series
            A Series of strings representing movie descriptions.
        """
        vocabulary = set(' '.join(documents).split(' '))
        term_frequency = np.zeros((len(documents), len(vocabulary)))
        vocabulary = dict(zip(vocabulary, range(len(vocabulary))))
        for i, txt in enumerate(documents):
            for word in txt.split(' '):
                term_frequency[i][vocabulary[word]] += 1
        term_frequency /= term_frequency.sum(axis=1, keepdims=True)
        self.vocabulary = vocabulary
        self.term_frequency = term_frequency
        
    def predict(self, query):
        """
        Predict a set of movies based on similarity to the query.

        Parameters
        ----------
        query: str
            A string representing the query for which we want similar movies.

        Returns
        -------
        predictions: list of int
            Indexes of movies most similar to the query.
        """
        query_words = [self.vocabulary.get(word) for word in query.split() if word in self.vocabulary]
        if not query_words:
            return []  # Return empty if query words are not in the vocabulary

        similarity = self.term_frequency[:, query_words].sum(axis=1)
        predictions = similarity.argsort()[-self.n:][::-1]  # Top `n` most similar documents
        return predictions
