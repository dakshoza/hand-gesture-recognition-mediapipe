from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np
import json

class GestureRecognizer:
    def __init__(self):
        self.data = [
    ['A', 'A A'],
    ['B', 'B B'],
    ['C', 'C'],
    ['D', 'C Point Up'],
    ['E', 'C Point In'],
    ['F', 'F F'],
    ['G', 'G G'],
    ['H', 'Palm Open Palm in'],
    ['I', 'Point Up'],
    ['J', 'J'],
    ['K', 'Inside Hook Point Up'],
    ['L', 'L'],
    ['M', 'Palm Open 3'],
    ['N', 'Palm Open V'],
    ['O', 'B'],
    ['P', 'Small Point Up'],
    ['Q', 'Circle Point Up'],
    ['R', 'Palm Out Upside Hook'],
    ['S', 'Downside Hook Upside Hook'],
    ['T', 'Point up Point in'],
    ['U', 'U'],
    ['V', 'V'],
    ['W', 'W W'],
    ['X', 'Point in Point in'],
    ['Y', 'L Point Up (Move)'],
    ['Z', 'Palm Side Palm Hook Palm Side Palm Hook'],
    ['1', 'Point Up'],
    ['2', 'V'],
    ['3', '3'],
    ['4', '4'],
    ['5', 'Palm Open'],
    ['6', 'Pinky'],
    ['7', 'Upside Hook'],
    ['8', '8'],
    ['9', 'sidewards thumsup'],
    ['Hello', 'C Palm Open'],
    ['Indian/India', 'B Move (up)'],
    ['Sign', 'Palm Open A Move A Palm Open Move Palm Open A Move A Palm Open Move'],
    ['Langauge', 'L L Move'],
    ['Bye-Bye', 'C Palm Open C Palm Open C Palm Open'],
    ['I/Me', 'Point In'],
    ['You', 'Point To (new)'],
    ['Man', 'Small Move - see later'],
    ['Woman', 'Point Up Move / Tap'],
    ['He', 'Man Point Up/ Point In'],
    ['She', 'Point Up Move (away)'],
    ['Deaf', 'Point Up/V(Move) V'],
    ['Teacher', 'G Point To Move / Tap'],
    ['Thankyou', '4 Move']
    ]

        self.vocabulary = self.build_vocabulary()
        self.word_to_index = {word: index for index, word in enumerate(self.vocabulary)}
        self.vectorized_data = self.vectorize_data()

    def build_vocabulary(self):
        vocabulary = set()
        for _, sequence in self.data:
            vocabulary.update(sequence.split())
        return vocabulary

    def sequence_to_bow(self, sequence):
        bow = np.zeros(len(self.word_to_index))
        word_counts = Counter(sequence.split())
        for word, count in word_counts.items():
            if word in self.word_to_index:
                bow[self.word_to_index[word]] = count
        return bow

    def vectorize_data(self):
        vectorized_data = []
        for word, sequence in self.data:
            bow = self.sequence_to_bow(sequence)
            vectorized_data.append((word, bow))
        return vectorized_data

    def save_embeddings(self, filename):
        embeddings = {word: vector.tolist() for word, vector in self.vectorized_data}
        with open(filename, 'w') as f:
            json.dump(embeddings, f)

    def load_embeddings(self, filename):
        with open(filename, 'r') as f:
            embeddings = json.load(f)
        return {word: np.array(embedding) for word, embedding in embeddings.items()}

    def find_most_similar_words(self, query_vector, num_words=3):
        similarities = []
        for word, vector in self.vectorized_data:
            similarity = cosine_similarity([query_vector], [vector])[0][0]
            similarities.append((word, similarity))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [word for word, _ in similarities[:num_words]]

    def find_most_similar_word_for_sequence(self, query_sequence):
        query_vector = self.sequence_to_bow(query_sequence)
        return self.find_most_similar_words(query_vector)
