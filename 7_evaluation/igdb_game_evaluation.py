
import jsonlines
import re
from collections import defaultdict
import random

def create_block():
    ## generating blocks

    with jsonlines.open('igdb_games.jl') as reader:
        with jsonlines.open('g2a_games_with_requirements.jl') as g2a_reader:
            block = defaultdict(lambda: [[], []])
            for igdb_obj in reader:
                for key, val in igdb_obj.items():
                    game_name = val['game_name'].lower()
                    if 'duplicate' in game_name:
                        game_name = re.sub('duplicate', '', game_name)
                        game_name = re.sub('\[.*?\]', '', game_name)
                    if game_name.startswith(' '):
                        print('starts with space')
                        game_name = game_name[1:]
                        print(game_name)
                    gen_block_key = re.sub(' ', '', game_name)
                    gen_block_key = gen_block_key.lower()
                    first_word = gen_block_key[:3]
                    if first_word == 'the':
                        first_word = gen_block_key[3:6]
                    block_key = first_word
                    block[block_key][0].append({key: game_name})
            for g2a_obj in g2a_reader:
                for key, val in g2a_obj.items():
                    g2a_game_name = val['title'].lower()
                    if 'lego ' in g2a_game_name:
                        g2a_game_name = re.sub('lego', '', g2a_game_name)
                    if g2a_game_name.startswith(' '):
                        g2a_game_name = g2a_game_name[1:]

                    g2a_block_key = re.sub(' ', '', g2a_game_name)
                    g2a_block_key = g2a_block_key.lower()
                    first_word = g2a_block_key[:3]
                    if first_word == 'the':
                        first_word = g2a_block_key[3:6]
                    block_key = first_word
                    block[block_key][1].append({key: g2a_game_name})
    return block

def calc_reduction_ratio(block):
    # total no of comparisons in rxr
    with jsonlines.open('../data_with_ids/igdb_games.jl') as igdb_reader:
        igdb_lines = 0
        for obj in igdb_reader:
            igdb_lines += 1
    with jsonlines.open('../data_with_ids/g2a_games_with_requirements.jl') as g2a_reader:
        g2a_lines = 0
        for obj in g2a_reader:
            g2a_lines += 1
    total_comp = igdb_lines * g2a_lines

    # no. of comparisons after blocking
    total_comp_after_blocking = 0
    for key in list(block.keys()):
        igdb_len = len(block[key][0])
        g2a_len = len(block[key][1])
        total_comp_after_blocking += igdb_len * g2a_len

    efficiency = total_comp_after_blocking/total_comp
    return efficiency

def generate_ground_truth_candidates(block):
    count = 0
    igdb_sample = []
    g2a_sample = []
    for key in list(block.keys()):
        if count == 100:
            break
        ig_samp = random.sample(range(10), 5)
        g2a_samp = random.sample(range(10), 5)
        if len(block[key][0]) >= 10 and len(block[key][1]) >= 10:
            for i, d in enumerate(block[key][0]):
                if i in ig_samp:
                    igdb_sample.append(list(d.keys())[0])
            for i, d in enumerate(block[key][1]):
                if i in g2a_samp:
                    g2a_sample.append(list(d.keys())[0])
            count += 1
    assert len(igdb_sample) == len(g2a_sample)
    file_writer = open('../ground_truth_data/igdb_g2a_gt.txt', 'w')
    for l in list(zip(igdb_sample, g2a_sample)):
        file_writer.write(l[0] + ',' + l[1] + '\n')

def calc_metrics():
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    with open('../ground_truth_data/igdb_g2a_gt.txt') as reader:
        for i,line in enumerate(reader.readlines()):
            if i == 50:
                break
            id_1,id_2,gt_val = line.split(',')[0],line.split(',')[1],int(line.split(',')[2])
            total += 1
            with jsonlines.open('../data_er/er_g2a_igdb_levenshtein_jaro_rijul_v4.jl') as er_reader:
                for obj in er_reader:
                    if obj['igdb_key'] == id_1:
                        if gt_val == 1:
                            if obj['similar_g2a_key'] != '':
                                if obj['similar_g2a_key'] == id_2:
                                    tp += 1
                                else:
                                    fp += 1
                            else:
                                fn += 1
                        if gt_val == 0:
                            if obj['similar_g2a_key'] != '':
                                if obj['similar_g2a_key'] == id_2:
                                    fp += 1
                                else:
                                    tn += 1
                            else:
                                tn += 1
            print(i, tp, tn, fp, fn, total, id_1, id_2)
    return tp,tn,fp,fn,total


if __name__ == '__main__':

    #block = create_block()
    #efficiency = calc_reduction_ratio(block)
    #enerate_ground_truth_candidates(block)
    tp,tn,fp,fn,total = calc_metrics()
    recall = tp/(tp+fn)
    precision = tp/(tp+fp)
    accuracy = (tp + tn)/total
    print(recall,precision,accuracy)

