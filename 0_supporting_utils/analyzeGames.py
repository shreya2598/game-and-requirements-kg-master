import json
import numpy as np
import string

# Findings:
# Common attributes: Game name and Game summary
# Game name: levenstein similarity and game summary: Cosine similarity on word embeddings (or) tf-idf
# Blocking key: Remove the words "the" and "duplicate" and use 3-grams to block.

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict


def findBlockingKeysStats(g2a_games, igdb_games):
    # For finding the n-gram blocking key:
    for i in range(1, 5):
        fn = dict()
        for key, val in igdb_games.items():
            game_name = val["game_name"].lower()
            for punc in string.punctuation:
                game_name = game_name.replace(punc, " ")
            game_name = "".join(game_name.split())

            first_chars = game_name[0:i]
            if fn.get(first_chars) is None:
                fn[first_chars] = 0

            fn[first_chars] += 1

        num_blocks = len(fn.keys())

        max_val = -1
        for key, val in fn.items():
            if val > max_val:
                max_val = val

        print("IGDB")
        print("N-grams = ", i)
        print("Number of blocks = ", num_blocks)
        print("Max block size = ", max_val)

        gn = dict()
        for key, val in g2a_games.items():

            game_name = val["title"].lower()
            for punc in string.punctuation:
                game_name = game_name.replace(punc, " ")
            game_name = "".join(game_name.split())

            first_chars = game_name[0:i]
            if gn.get(first_chars) is None:
                gn[first_chars] = 0

            gn[first_chars] += 1

        # gn = sorted(gn.items(), key=lambda x: x[1], reverse=True)
        # gn = dict(gn)

        num_blocks = len(gn.keys())

        max_val = -1
        for key, val in gn.items():
            if val > max_val:
                max_val = val

        print("G2A")
        print("N-grams = ", i)
        print("Number of blocks = ", num_blocks)
        print("Max block size = ", max_val)


def findFirstWordFrequencies(g2a_games, igdb_games):

    fword = {}
    for key, val in igdb_games.items():
        game_name = val["game_name"].lower()
        for punc in string.punctuation:
            game_name = game_name.replace(punc, " ")

        try:
            first_chars = game_name.split()[0]
            if fword.get(first_chars) is None:
                fword[first_chars] = 0

            fword[first_chars] += 1
        except:
            pass

    for key, val in g2a_games.items():
        game_name = val["title"].lower()
        for punc in string.punctuation:
            game_name = game_name.replace(punc, " ")

        try:
            first_chars = game_name.split()[0]
            if fword.get(first_chars) is None:
                fword[first_chars] = 0

            fword[first_chars] += 1
        except:
            pass

    fword = dict(sorted(fword.items(), key=lambda x: x[1], reverse=True))
    print(fword)

if __name__ == "__main__":
    g2a_games_file = "../../data_with_ids/g2a_games_with_requirements.jl"
    igdb_games_file = "../../data_with_ids/igdb_games.jl"

    g2a_games = constructDictfromJL(g2a_games_file)
    igdb_games = constructDictfromJL(igdb_games_file)

    # findBlockingKeysStats(g2a_games, igdb_games)
    # findFirstWordFrequencies(g2a_games, igdb_games)

    t = dict()
    for key, val in g2a_games.items():
        try:
            tt = val['seller_feedback_msg']
            if tt is None:
                print(tt)

            if t.get(tt) is None:
                t[tt] = 0

            t[tt] += 1
        except:
            pass

    print(t)




