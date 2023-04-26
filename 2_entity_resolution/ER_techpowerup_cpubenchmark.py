import rltk
import jsonlines
import time
import sys

if __name__ == '__main__':
    st = time.time()

    sim_count = 0
    # sys.argv[3] ----> file path where er result need to be written
    similarity_file = jsonlines.open(sys.argv[3], 'w')
    # sys.argv[1] ----> path to techpowerup mapping file
    with jsonlines.open(sys.argv[1]) as techpowerup_reader:

        for i, tech_obj in enumerate(techpowerup_reader):
            if i % 5 == 0:
                print('time taken for {} is {}'.format(i, time.time() - st))
            tech_key, tech_value = list(tech_obj.items())[0][0], list(tech_obj.items())[0][1]['name']
            similar_cpu = {}
            max_score = -1
            similar_key = ''
            similar_cpu_name = ''
            # sys.argv[2] -----> path to cpu benchmark mapping file
            with jsonlines.open(sys.argv[2]) as cpubenchmark_reader:
                for cpu_obj in cpubenchmark_reader:
                    cpu_key, cpu_value = list(cpu_obj.items())[0][0], list(cpu_obj.items())[0][1]['cpu_name']
                    score = rltk.levenshtein_similarity(tech_value.lower(), cpu_value.lower())
                    if score > max_score:
                        max_score = score
                        similar_key = cpu_key
                        similar_cpu_name = cpu_value
                if max_score >= 0.5:
                    sim_count += 1
                    similar_cpu['techpowerup'] = {'id': tech_key, 'name': tech_value}
                    similar_cpu['similarity'] = {'similar_cpubenchmark_key': similar_key,
                                                 'similar_cpubenchmark_name': similar_cpu_name, 'sim_score': max_score}
                    similarity_file.write(similar_cpu)
                else:
                    similar_cpu['techpowerup'] = {'id': tech_key, 'name': tech_value}
                    similar_cpu['similarity'] = {'similar_cpubenchmark_key': '', 'similar_cpubenchmark_name': '',
                                                 'sim_score': -1}
                    similarity_file.write(similar_cpu)