import jsonlines



if __name__ == '__main__':
    with jsonlines.open('../data_er/ER_g2a_games_gpus_and_techpowerup_gpus_score_thresh.jl','w') as writer:
        with jsonlines.open('../data_er/ER_g2a_games_gpus_and_techpowerup_gpus.jl') as reader:
            for obj in reader:
                d = {}
                d['g2a_games_id'] = obj['g2a_games_id']

                if len(obj['tpowerup_gpu1']) != 0:
                    score = obj['tpowerup_gpu1']['max_score']
                    if score > 0.60:
                        d['tpowerup_gpu1'] = obj['tpowerup_gpu1']
                    else:
                        d['tpowerup_gpu1'] = {}
                else:
                    d['tpowerup_gpu1'] = {}

                if len(obj['tpowerup_gpu2']) != 0:
                    score = obj['tpowerup_gpu2']['max_score']
                    if score > 0.60:
                        d['tpowerup_gpu2'] = obj['tpowerup_gpu2']
                    else:
                        d['tpowerup_gpu2'] = {}
                else:
                    d['tpowerup_gpu2'] = {}

                writer.write(d)
