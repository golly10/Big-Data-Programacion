import sys
import io
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd

nltk.download('stopwords', quiet=True)

class MapReducer():
    def __init__(self):

        self.punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        self.stop_words = set(stopwords.words('spanish'))
        
        self.line = None

        self.all_words_mapper = []

        self.all_words_reducer = {}
    
    def emit_mapper(self, line):
        self.line = line.strip()
        self.line = re.sub(r'[^\w\s]', '',self.line)
        self.line = self.line.lower()

        for x in self.line:

            if x in self.punctuations:
                self.line=self.line.replace(x, " ") 

        words=self.line.split()

        for word in words: 

            if (word not in self.stop_words and word in ["blanco", "rojo", "negro"]):
                self.all_words_mapper.append({word: 1})

    def print_results_mapper(self):
        print("///// RESULTADOS TRAS EJECUTAR MAPPER /////")

        for word in self.all_words_mapper:
            print('%s\t%s' % (word, 1))

        print()

    def emit_reducer(self):

        for word in self.all_words_mapper:
            
            if list(word.keys())[0] in self.all_words_reducer.keys():

                self.all_words_reducer[list(word.keys())[0]] += 1
            
            else:
                self.all_words_reducer[list(word.keys())[0]] = 1

    def print_results_reducer(self):
        print("///// RESULTADOS TRAS EJECUTAR REDUCER /////")

        for word in self.all_words_reducer:
            print('%s\t%s' % (word, self.all_words_reducer[word]))

        print()

if __name__ == "__main__":
    
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='latin1')
    m_p = MapReducer()

    for line in input_stream:
        
        m_p.emit_mapper(line=line)

        m_p.print_results_mapper()

        m_p.emit_reducer()

        m_p.print_results_reducer()
    