import json
import numpy as np

# Findings: First level blocking: [radeon, geforce & geforce2 & geforce3 & geforce4, quadro, mobility, others]
# Second Level for radeon: hd, rx, r7, r9 and model numbers
# Second Level for geforce: gtx, gt, gts, fx, rtx, go and model numbers

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

if __name__ == "__main__":
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs.jl"
    g2a_games_file = "../../data_with_ids/g2a_games_with_requirements.jl"

    # g2a_games = constructDictfromJL(g2a_games_file)
    techpowerup_gpus = constructDictfromJL(techpowerup_gpu_file)

    fl = dict()
    for key, val in techpowerup_gpus.items():
        try:
            cur_gpu = val["Product Name"]
            flevel = cur_gpu.lower().split()
            for i in flevel:
                if not i.isnumeric():
                    if fl.get(i) is None:
                        fl[i] = 0
                    fl[i] += 1
        except:
            pass

    sl = dict()
    split_words = [" / ", ", ", " or "]
    for key, val in g2a_games.items():
        try:
            min_req = val["min_requirements"]
            cur_gpu = min_req["Graphics"]
            input_gpu = cur_gpu

            game_gpus = [input_gpu]
            for cur_word in split_words:
                if cur_word in input_gpu:
                    game_gpus = input_gpu.split(cur_word)
                    break

            for gpu in game_gpus:
                flevel = gpu.lower().split()
                for i in flevel:
                    if sl.get(i) is None:
                        sl[i] = 0
                    sl[i] += 1

        except:
            pass


    fl = dict(sorted(fl.items(), key=lambda x: x[1], reverse=True))
    print(len(fl.keys()))
    print(fl)

    sl = dict(sorted(sl.items(), key=lambda x: x[1], reverse=True))
    for key, val in sl.items():
        print(key, val)

