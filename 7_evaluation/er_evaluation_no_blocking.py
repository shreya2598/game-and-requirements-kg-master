import jsonlines

def cpu_gpu_er_evaluation(ground_truth_file,file_path,g2a_id,req_id_1,req_id_2):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    total = 0

    with open(ground_truth_file) as reader:
        for i,line in enumerate(reader.readlines()):
            if i == 30:
                break
            id_1,id_2,ground_truth_value = line.split(',')[0],line.split(',')[1],int(line.split(',')[2])
            total += 1
            #print(type(ground_truth_value))

            with jsonlines.open(file_path) as cpu_reader:
                for obj in cpu_reader:
                    match_id_1 = ''
                    match_id_2 = ''
                    if obj[g2a_id] == id_1:
                        if len(obj[req_id_1]) != 0:
                            #print('i_1')
                            match_id_1 = obj[req_id_1]['max_match_id']
                            #print(match_id_1)
                        if len(obj[req_id_2]) != 0:
                            #print('i_2')
                            match_id_2 = obj[req_id_2]['max_match_id']
                            #print(match_id_2)

                        if ground_truth_value == 1:
                            if match_id_1 != '' or match_id_2 != '':
                                if id_2 == match_id_1 or id_2 == match_id_2:
                                    tp += 1
                                if id_2 != match_id_1 and id_2 != match_id_2:
                                    fp += 1
                            if match_id_1 == '' and match_id_2 == '':
                                fn += 1
                            '''if id_2 == match_id_1 or id_2 == match_id_2:
                                tp += 1
                            if match_id_1 == '' and match_id_2 == '':
                                fn += 1
                            if (id_2 != match_id_1 and match_id_1 != '') and (id_2 != match_id_2 and match_id_2 != ''):
                                print(i)
                                fp += 1
                            if (id_2 != match_id_1 and match_id_1 != '' and match_id_2 == '') or (id_2 != match_id_2 and match_id_2 != '' and match_id_1 == ''):
                                print(i)
                                fp += 1'''


                        if ground_truth_value == 0:
                            if match_id_1 == '' and match_id_2 == '':
                                tn += 1
                            if match_id_1 != '' or match_id_2 != '':
                                if match_id_1 != id_2 and match_id_2 != id_2:
                                    tn += 1
                                if match_id_1 == id_2 or match_id_2 == id_2:
                                    fp += 1
                            '''        
                            if match_id_1 != id_2 and match_id_2 != id_2:
                                tn += 1
                            if (match_id_1 != '' and id_2 == match_id_1) or (match_id_2 != '' and id_2 ==match_id_2):
                                fp += 1'''
                        print(i,tp,tn,fp,fn,total,id_1,id_2)
    return tp,tn,fp,fn,total

if __name__ == '__main__':

    # cpu evaluation
    cpu_gt_file_path = '../ground_truth_data/g2a_cpu_tech_cpu_gt.txt'
    cpu_er_file = '../data_er/ER_g2a_game_cpus_techpowerup_cpus.jl'
    tp,tn,fp,fn,total = cpu_gpu_er_evaluation(cpu_gt_file_path,cpu_er_file,'g2_games_id','tpowerup_cpu1','tpowerup_cpu2')
    print(tp,tn,fp,fn,total)
    precision = tp/(tp + fp)
    recall = tp/(tp + fn)
    accuracy = (tp + tn)/total
    print(precision,recall,accuracy)



