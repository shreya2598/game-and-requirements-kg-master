import re
import json
import string
import numpy as np
from modelUtils.LanguageModels import WordEmbeddingsModel

gl_embeddings_model = None

def cleanText(inp):
    inp = inp.lower()
    inp = re.sub(r"\\u[0-9,A-F]{4}", " ", inp)
    for char in string.punctuation:
        inp = inp.replace(char, " ")
    tokens = inp.split()
    return " ".join(tokens)

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def computeEmbeddingsForGame(cur_game_dict):
    global gl_embeddings_model

    game_name = cleanText(cur_game_dict["game_name"])
    game_name_emb = gl_embeddings_model.getEmbeddingsForSentence(game_name)

    try:
        game_summary = cleanText(cur_game_dict["game_summary"])
    except:
        game_summary = ""
    game_summary_emb = gl_embeddings_model.getEmbeddingsForSentence(game_summary)

    try:
        genre_label = cleanText(" ".join(cur_game_dict["genre"]))
    except:
        genre_label = ""

    try:
        theme_label = cleanText(" ".join(cur_game_dict["themes"]))
    except:
        theme_label = ""
    genre_theme_emb = gl_embeddings_model.getEmbeddingsForSentence(genre_label + " " + theme_label)

    try:
        game_mode_label = cleanText(" ".join(cur_game_dict["game_modes"]))
    except:
        game_mode_label = ""
    game_mode_emb = gl_embeddings_model.getEmbeddingsForSentence(game_mode_label)

    weights = 0.0
    cur_embedding = np.zeros(300)

    if game_name_emb is not None:
        weights += 2.0
        cur_embedding += (2 * game_name_emb)

    if game_summary_emb is not None:
        weights += 2.0
        cur_embedding += (2 * game_summary_emb)

    if genre_theme_emb is not None:
        weights += 4.0
        cur_embedding += (4 * genre_theme_emb)

    if game_mode_emb is not None:
        weights += 4.0
        cur_embedding += (4 * game_mode_emb)

    if weights == 0:
        return None
    else:
        cur_embedding /= weights
        return cur_embedding

def print_word_vecs(wordVectors, outFileName):
    outFile = open(outFileName, 'w')
    for word, values in wordVectors.items():
        outFile.write(word+' ')
        for val in wordVectors[word]:
            outFile.write('%.4f' %(val)+' ')
        outFile.write('\n')
    outFile.close()

def generateShortURI(input_uri):
    cur_list = input_uri.split("_")
    short_uri = ""
    for cur_val in cur_list[:-1]:
        short_uri += cur_val[0]
    short_uri += "_" + cur_list[-1]
    return short_uri

if __name__ == "__main__":
    igdb_game_file = "../../data_with_ids/igdb_games.jl"
    igdb_games = constructDictfromJL(igdb_game_file)

    embeddings_file_name = "fasttext_word_vectors_wiki_news_uncased_remapped.vec"
    gl_embeddings_model = WordEmbeddingsModel(embeddings_file_name, 300)

    count = 0
    out_embeddings_matrix = dict()
    for key, val in igdb_games.items():
        count += 1
        if count % 1000 == 0:
            print("Progress = ", count)
        cur_embedding = computeEmbeddingsForGame(val)
        if cur_embedding is not None:
            out_embeddings_matrix[generateShortURI(key)] = cur_embedding

    out_embeddings_file = "game_embeddings_constructed_with_fasttext.vec"
    print_word_vecs(out_embeddings_matrix, out_embeddings_file)