import numpy as np
import io
from gensim.models import KeyedVectors
from gensim.test.utils import datapath, get_tmpfile
from gensim.scripts.glove2word2vec import glove2word2vec

class WordEmbeddingsModel:
    def __init__(self, embeddings_file_name, embeddings_dimensions):
        self.embeddings_file = embeddings_file_name
        self.num_dims = embeddings_dimensions

        glove_file = self.embeddings_file
        word2vec_glove_file = get_tmpfile("temp_embeddings_file.txt")
        glove2word2vec(glove_file, word2vec_glove_file)
        self.embeddings_model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
        self.vocab_size = len(self.embeddings_model.vocab.keys())
        print("Done loading words...")

    def __load_vectors(self):
        f = io.open(self.embeddings_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
        e_model = {}
        for line in f:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            e_model[word] = embedding
        print("Done.", len(e_model), " words loaded!")
        return e_model

    # Generate word embeddings for each word in the sentence:
    def __getWordEmbeddings(self, tokens_list):
        word_embeddings = []
        for word in tokens_list:
            try:
                word_embeddings.append(list(self.embeddings_model[word]))
            except:
                error_word = word
            # print("Key error :", error_word)
        if len(word_embeddings) == 0:
            return None
        else:
            return np.array(word_embeddings)

    # Compute the sentence embeddings using the individual word embeddings:
    def __getSentenceEmbeddings(self, word_embeddings):
        avg_sent_embeddings = np.mean(word_embeddings, axis=0)
        return avg_sent_embeddings

    def containsWord(self, query_word):
        try:
            cur_vector = self.embeddings_model[query_word]
            return True
        except:
            return False

    def getVocabWords(self):
        return list(self.embeddings_model.vocab.keys())

    def getMostSimilarWords(self, query_word, top_k, probs=True):
        if top_k == -1:
            word_neighbors_probs = self.embeddings_model.most_similar(query_word, topn=self.vocab_size)
        else:
            word_neighbors_probs = self.embeddings_model.most_similar(query_word, topn=top_k)
        if probs == True:
            return word_neighbors_probs
        else:
            word_neighbors_list = []
            for cur_neighbor in word_neighbors_probs:
                word_neighbors_list.append(cur_neighbor[0])
            return word_neighbors_list

    def getEmbeddingsForWord(self, query_word):
        if self.containsWord(query_word):
            cur_word_embedding = self.__getWordEmbeddings([query_word])[0]
            return cur_word_embedding
        else:
            return None

    def getEmbeddingsForSentence(self, query_sentence):
        cur_sentence_tokens = query_sentence.split()
        word_embeddings_list = self.__getWordEmbeddings(cur_sentence_tokens)
        if word_embeddings_list is None:
            return None
        else:
            sentence_embeddings = self.__getSentenceEmbeddings(word_embeddings_list)
            return sentence_embeddings

    def getEmbeddingsForTokenList(self, query_token_list):
        word_embeddings_list = self.__getWordEmbeddings(query_token_list)
        if word_embeddings_list is None:
            return None
        else:
            sentence_embeddings = self.__getSentenceEmbeddings(word_embeddings_list)
            return sentence_embeddings

if __name__ == "__main__":
    embeddings_file = "../../ontology_reconstruction/embeddings/sampleFasttext.vec"
    embeddings_dims = 100

    embeddings_model = WordEmbeddingsModel(embeddings_file, embeddings_dims)
    sample_sentence = "This men s dress is blue in color"
    temp = embeddings_model.getEmbeddingsForSentence(sample_sentence)
    # print(temp)