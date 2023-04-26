import random
import jsonlines

igdb_cand_numbers = random.sample(range(58470),100)
g2a_cand_numbers = random.sample(range(34700),100)

file_to_write = open('../ground_truth_data/igdb_g2a_gt.txt','w')

for l in list(zip(igdb_cand_numbers,g2a_cand_numbers)):
    file_to_write.write('mgns_igdb_games_'+str(l[0])+','+'mgns_g2a_games_with_requirements_'+str(l[1])+'\n')


