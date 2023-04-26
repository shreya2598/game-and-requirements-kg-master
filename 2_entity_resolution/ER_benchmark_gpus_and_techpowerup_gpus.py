import numpy as np
import json
import jsonlines
import re
import rltk
import time

techpowerup_gpus = None
benchmark_gpus = None

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def cleanGPUText(input_gpu):
    # Removing sizes (mb, gb)
    input_gpu = input_gpu.lower()
    input_gpu = input_gpu.replace("intel", "")
    input_gpu = re.sub("^\d+(mb|gb)", "", input_gpu)
    input_gpu = re.sub("^\d+", "", input_gpu)
    input_gpu = input_gpu.strip()

    return input_gpu

def getMostSimilarGPU_Benchmark(input_gpu):
    global benchmark_gpus

    max_score = -1
    max_match_id = None
    max_match_val = None

    for key, val in benchmark_gpus.items():
        bench_gpu = cleanGPUText(val["videocard_name"])
        cur_score = rltk.levenshtein_similarity(input_gpu, bench_gpu)
        if cur_score > max_score:
            max_score = cur_score
            max_match_id = key
            max_match_val = val["videocard_name"]

    return max_match_id, max_score, max_match_val

if __name__ == "__main__":

    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs.jl"
    benchmark_gpu_file = "../../data_with_ids/gpu_benchmarks.jl"
    out_file = "ER_benchmark_gpus_and_techpowerup_gpus.jl"

    techpowerup_gpus = constructDictfromJL(techpowerup_gpu_file)
    benchmark_gpus = constructDictfromJL(benchmark_gpu_file)
    er_mapping_result = []
    start_time = time.time()

    index = 0
    for key, val in techpowerup_gpus.items():
        if index%100==0:
            cur_time = time.time()
            seconds_elapsed = cur_time - start_time
            print("Progress count = ", index, ", Seconds elapsed = ", seconds_elapsed)


        cur_dict = {}
        cur_dict["tpowerup_gpu_id"] = key
        try:
            cur_gpu = cleanGPUText(val["Product Name"])
            cur_dict["tpowerup_gpu_val"] = val["Product Name"]
            benchmark_gpu_id, score, match_val = getMostSimilarGPU_Benchmark(cur_gpu)
            cur_dict["benchmark_gpu_id"] = benchmark_gpu_id
            cur_dict["max_score"] = score
            cur_dict["max_match_val"] = match_val
        except:
            cur_dict["max_score"] = -1
            cur_dict["benchmark_gpu_id"] = None
            cur_dict["max_match_val"] = None

        er_mapping_result.append(cur_dict)
        index = index + 1

    cur_time = time.time()
    seconds_elapsed = cur_time - start_time
    print("Progress count = ", index, ", Seconds elapsed = ", seconds_elapsed)
    with jsonlines.open(out_file, "w") as f:
        f.write_all(er_mapping_result)


