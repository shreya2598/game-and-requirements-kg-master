import time
import jsonlines


if __name__ == '__main__':
    st = time.time()
    file_write = jsonlines.open('../data_er/er_cpu_benchmark_techpowerup_all_fields.jl', 'w')
    with jsonlines.open('../data_er/er_techpowerup_cpu_benchmark.jl') as er_reader:
        for i, er_obj in enumerate(er_reader):
            if i % 5 == 0:
                print('time taken for {} is {}'.format(i, time.time() - st))
            d = {}
            er_techpowerup_key, er_cpubenchmark_key, sim_score = list(er_obj.items())[0][1]['id'], \
                                                                 list(er_obj.items())[1][1]['similar_cpubenchmark_key'], \
                                                                 list(er_obj.items())[1][1]['sim_score']

            with jsonlines.open('../data_with_ids/techpowerup_cpu_cleaned.jl') as tech_reader:
                for tech_obj in tech_reader:
                    tech_key = list(tech_obj.items())[0][0]
                    if tech_key == er_techpowerup_key:
                        d['techpowerup'] = tech_obj
            if er_cpubenchmark_key != '':
                with jsonlines.open('../data_with_ids/cpubenchmark.jl') as cpu_reader:
                    for cpu_obj in cpu_reader:
                        cpu_key = list(cpu_obj.items())[0][0]
                        if cpu_key == er_cpubenchmark_key:
                            d['cpubenchmark'] = cpu_obj
                            d['sim_score'] = sim_score
            else:
                d['cpubenchmark'] = {}
                d['sim_score'] = -1

            file_write.write(d)