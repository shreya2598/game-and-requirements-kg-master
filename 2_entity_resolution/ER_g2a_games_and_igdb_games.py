import numpy as np
import json
import jsonlines
import rltk

igdb_games = None
g2a_games = None

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def getMostSimilarGame_G2A(input_game):
    max_match_id = "NA"
    max_score = -1

    return max_match_id, max_score

if __name__ == "__main__":

    igdb_games_file = "../../data_with_ids/sample_igdb_games.jl"
    g2a_games_file = "../../data_with_ids/sample_g2a_games_with_requirements.jl"
    out_file = "ER_g2a_games_and_igdb_games.jl"

    igdb_games = constructDictfromJL(igdb_games_file)
    g2a_games = constructDictfromJL(g2a_games_file)
    er_mapping_result = []

    index = 0
    for key, val in igdb_games.items():
        if index%100==0:
            print("Progress count = ", index)

        cur_dict = {}
        cur_dict["igdb_games_id"] = key
        try:
            cur_game = val
            g2a_games_id, score = getMostSimilarGame_G2A(cur_game)
            cur_dict["g2a_games_id"] = g2a_games_id
            cur_dict["similarity_score"] = score
        except:
            cur_dict["g2a_games_id"] = "NA"
            cur_dict["similarity_score"] = -1

        er_mapping_result.append(cur_dict)
        index = index + 1

    with jsonlines.open(out_file, "w") as f:
        f.write_all(er_mapping_result)


