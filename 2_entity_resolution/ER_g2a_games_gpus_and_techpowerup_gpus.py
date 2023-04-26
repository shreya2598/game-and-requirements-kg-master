import numpy as np
import json
import jsonlines
import rltk
import re
import time

g2a_games = None
gpu_blocks = None
techpowerup_gpus = None
gpu_vocab = {}

def containsDigit(input_str):
    for i in input_str:
        if i.isdigit():
            return True

    return False

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def createBlocks():
    global gpu_vocab, techpowerup_gpus

    cur_blocks = {}
    block_keys = ["radeon", "geforce", "quadro", "others"]
    for cur_key in block_keys:
        cur_blocks[cur_key] = dict()

    for key, val in techpowerup_gpus.items():
        try:
            cur_product_name = val["Product Name"].lower()
            split_list = cur_product_name.split()
            for cur_word in split_list:
                if not containsDigit(cur_word):
                    gpu_vocab[cur_word] = 1

            flag = 0
            for cur_key in block_keys:
                if cur_key in cur_product_name:
                    cur_blocks[cur_key][key] = 1
                    flag = 1
                    break

            if flag == 0:
                cur_blocks["others"][key] = 1
        except:
            pass

    return cur_blocks

def cleanGPUText(input_gpu):
    global gpu_vocab

    # Removing sizes (mb, gb)
    input_gpu = re.sub("\d+(mb|gb)", "", input_gpu)
    input_gpu = re.sub("^\d+(mb|gb)", "", input_gpu)
    input_gpu = re.sub("^\d+", "", input_gpu)
    input_gpu = re.sub("(mb|gb)", "", input_gpu)
    input_gpu = input_gpu.replace("®", "")

    cur_split = input_gpu.split()
    result_gpu = ""
    for cur_word in cur_split:
        if containsDigit(cur_word):
            result_gpu += " " + cur_word
        elif gpu_vocab.get(cur_word) is not None:
            result_gpu += " " + cur_word

    result_gpu = result_gpu.strip()
    return result_gpu

def getGPUBlockKey(input_gpu):
    global gpu_blocks
    for cur_key in gpu_blocks.keys():
        if cur_key in input_gpu:
            return cur_key

    return "others"


# Current Problems: (8670 vs 4670) and (6600 vs 600)
def getMostSimilarGPU_Techpowerup(input_gpu):
    global gpu_blocks, techpowerup_gpus

    split_words = [" / ", ", ", " or "]

    game_gpus = [input_gpu]
    for cur_word in split_words:
        if cur_word in input_gpu:
            game_gpus = input_gpu.split(cur_word)
            break


    gpu1 = {}
    gpu2 = {}

    # Base Cases:
    # Invalid input gpu
    if game_gpus[0] == "-" and len(game_gpus) == 1:
        return gpu1, gpu2

    # GPU1
    max_score = -1
    max_match_id = None
    max_match_val = None
    cur_game_gpu = cleanGPUText(game_gpus[0].lower())
    gpu1["actual_val"] = game_gpus[0].lower()
    cur_block_key = getGPUBlockKey(cur_game_gpu)
    for tgpu_id in gpu_blocks[cur_block_key].keys():
        try:
            tgpu_val = techpowerup_gpus[tgpu_id]
            cur_product_name = tgpu_val["Product Name"].lower()

            cur_score = rltk.levenshtein_similarity(cur_game_gpu, cur_product_name)

            if cur_score > max_score:
                max_score = cur_score
                max_match_id = tgpu_id
                max_match_val = cur_product_name
        except:
            pass

    gpu1["max_score"] = max_score
    gpu1["max_match_id"] = max_match_id
    gpu1["max_match_val"] = max_match_val

    # GPU2
    if len(game_gpus) >= 2:
        max_score = -1
        max_match_id = None
        max_match_val = None
        cur_game_gpu = cleanGPUText(game_gpus[1].lower())
        gpu2["actual_val"] = game_gpus[1].lower()
        cur_block_key = getGPUBlockKey(cur_game_gpu)
        for tgpu_id in gpu_blocks[cur_block_key].keys():
            try:
                tgpu_val = techpowerup_gpus[tgpu_id]
                cur_product_name = tgpu_val["Product Name"].lower()

                cur_score = rltk.levenshtein_similarity(cur_game_gpu, cur_product_name)

                if cur_score > max_score:
                    max_score = cur_score
                    max_match_id = tgpu_id
                    max_match_val = cur_product_name
            except:
                pass

        gpu2["max_score"] = max_score
        gpu2["max_match_id"] = max_match_id
        gpu2["max_match_val"] = max_match_val

    return gpu1, gpu2

if __name__ == "__main__":
    g2a_games_file = "../../data_with_ids/g2a_games_with_requirements.jl"
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs.jl"
    out_file = "ER_g2a_games_gpus_and_techpowerup_gpus.jl"

    techpowerup_gpus = constructDictfromJL(techpowerup_gpu_file)
    gpu_blocks = createBlocks()
    g2a_games = constructDictfromJL(g2a_games_file)
    er_mapping_result = []
    start_time = time.time()

    index = 0
    match_cnt = 0
    nonmatch_cnt = 0
    for key, val in g2a_games.items():
        if index%100==0:
            cur_time = time.time()
            seconds_elapsed = cur_time - start_time
            print("Progress count = ", index, ", Seconds elapsed = ", seconds_elapsed)

        cur_dict = {}
        cur_dict["g2a_games_id"] = key
        try:
            min_req = val["min_requirements"]
            cur_gpu = min_req["Graphics"]
            tpowerup_gpu1, tpowerup_gpu2 = getMostSimilarGPU_Techpowerup(cur_gpu)
            cur_dict["tpowerup_gpu1"] = tpowerup_gpu1
            cur_dict["tpowerup_gpu2"] = tpowerup_gpu2
            match_cnt += 1
        except:
            cur_dict["tpowerup_gpu1"] = {}
            cur_dict["tpowerup_gpu2"] = {}
            nonmatch_cnt += 1

        er_mapping_result.append(cur_dict)
        index = index + 1

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("Progress count = ", index, ", Seconds elapsed = ", seconds_elapsed)
    print("Matches = ", match_cnt, ", Non Matches = ", nonmatch_cnt)

    with jsonlines.open(out_file, "w") as f:
        f.write_all(er_mapping_result)


