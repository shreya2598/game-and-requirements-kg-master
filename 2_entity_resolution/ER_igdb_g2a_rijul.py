import jsonlines
import rltk
import re
import time

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

def er_task(block):
    st = time.time()
    similar = defaultdict(lambda: [])

    for i, (key, val) in enumerate(block.items()):
        if (i + 1) % 1 == 0:
            print("time taken for {} is {}".format(i, time.time() - st))
        for igdb_obj in val[0]:
            for igdb_game_key, igdb_game_name in igdb_obj.items():
                max_score = -1
                matching_key = ''
                matching_name = ''
                max_lev_score = -1
                max_jw_score = -1

                if len(val[1]) != 0:
                    for g2a_obj in val[1]:
                        for g2a_game_key, g2a_game_name in g2a_obj.items():
                            lev_score = rltk.levenshtein_similarity(igdb_game_name, g2a_game_name)
                            jw_score = rltk.jaro_winkler_similarity(igdb_game_name, g2a_game_name)
                            score = lev_score + jw_score
                            if score > max_score:
                                max_score = score
                                max_lev_score = lev_score
                                max_jw_score = jw_score
                                matching_key = g2a_game_key
                                matching_name = g2a_game_name
                    if max_score > 1.2:
                        similar[key].append({(igdb_game_key, igdb_game_name): (matching_key, matching_name, max_score)})
                    else:
                        similar[key].append({(igdb_game_key, igdb_game_name): ('', '', -1)})
                else:
                    similar[key].append({(igdb_game_key, igdb_game_name): ('', '', -1)})
    print("total time taken: ", time.time() - st)

    return similar

def write_result_to_jl(similar):
    with jsonlines.open('er_g2a_igdb_levenshtein__jaro_rijul_v4.jl', 'w') as writer:
        for key, val in similar.items():
            for obj in val:
                obj_to_write = {"igdb_key": '', 'igdb_game_name': '', 'similar_g2a_key': '','similar_g2a_game_name': ''}
                obj_to_write['igdb_key'] = list(obj.items())[0][0][0]
                obj_to_write['igdb_game_name'] = list(obj.items())[0][0][1]
                obj_to_write['similar_g2a_key'] = list(obj.items())[0][1][0]
                obj_to_write['similar_g2a_game_name'] = list(obj.items())[0][1][1]
                obj_to_write['similarity_score'] = list(obj.items())[0][1][2]
                writer.write(obj_to_write)


if __name__ == '__main__':
    block = create_block()
    similar = er_task(block)
    write_result_to_jl(similar)
