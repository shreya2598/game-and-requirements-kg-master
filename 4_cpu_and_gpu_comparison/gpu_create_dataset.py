import numpy as np
import pandas as pd
import json
import jsonlines
import time

techpowerup_gpus = None
benchmark_gpus = None
gpu_map = None

def constructDictfromJL(json_lines_file):
    result_dict = {}
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]
            result_dict[key] = val

    return result_dict

def createMap(map_file):
    result_dict = {}
    with open(map_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            tid = cur_dict["tpowerup_gpu_id"]
            if cur_dict["max_score"] >= 0.99:
                result_dict[tid] = cur_dict["benchmark_gpu_id"]

    print("Num keys = ", len(result_dict.keys()))
    return result_dict

def createRegressionDataset():
    global techpowerup_gpus, benchmark_gpus, gpu_map

    data = []
    feature_cols = ["released_year", "gpu_chip", "bus_info", "memory_val_mb", "memory_type", "memory_bits",
                    "gpu_clock_mhz", "memory_clock_mhz", "shader_1", "shader_2", "tmus", "rops", "g3d_mark"]

    for tid, bid in gpu_map.items():
        cur_row = techpowerup_gpus[tid]
        cur_bench_row = benchmark_gpus[bid]

        if cur_row["released_year"] != -1:
            released_year = cur_row["released_year"]
        else:
            released_year = None

        if len(cur_row["gpu_chip"]) != 0:
            gpu_chip = cur_row["gpu_chip"]
        else:
            gpu_chip = None

        if len(cur_row["bus_info"]) != 0:
            bus_info = cur_row["bus_info"]
        else:
            bus_info = None

        if cur_row["memory_val_mb"] != -1:
            memory_val_mb = cur_row["memory_val_mb"]
        else:
            memory_val_mb = None

        if len(cur_row["memory_type"]) != 0:
            memory_type = cur_row["memory_type"]
        else:
            memory_type = None

        if cur_row["memory_bits"] != -1:
            memory_bits = cur_row["memory_bits"]
        else:
            memory_bits = None

        if cur_row["gpu_clock_mhz"] != -1:
            gpu_clock_mhz = cur_row["gpu_clock_mhz"]
        else:
            gpu_clock_mhz = None

        if cur_row["memory_clock_mhz"] != -1:
            memory_clock_mhz = cur_row["memory_clock_mhz"]
        else:
            memory_clock_mhz = None

        if cur_row["shader_1"] != -1:
            shader_1 = cur_row["shader_1"]
        else:
            shader_1 = None

        if cur_row["shader_2"] != -1:
            shader_2 = cur_row["shader_2"]
        else:
            shader_2 = None

        if cur_row["tmus"] != -1:
            tmus = cur_row["tmus"]
        else:
            tmus = None

        if cur_row["rops"] != -1:
            rops = cur_row["rops"]
        else:
            rops = None

        try:
            g3d_mark = int(cur_bench_row["g3d_mark"])
        except:
            g3d_mark = None

        feature_vals = [released_year, gpu_chip, bus_info, memory_val_mb, memory_type, memory_bits, gpu_clock_mhz, memory_clock_mhz,
                        shader_1, shader_2, tmus, rops, g3d_mark]

        data.append(feature_vals)

    df = pd.DataFrame(data=data, columns=feature_cols)
    df.to_csv("gpu_regression_dataset.csv", index=False)


def createClassificationDataset():
    global techpowerup_gpus, benchmark_gpus, gpu_map

    data = []
    cols = ["gpu_id1", "gpu_id2", "label"]

    score_dict = {}
    for tid, bid in gpu_map.items():
        cur_bench_row = benchmark_gpus[bid]
        try:
             cur_score = cur_bench_row["g3d_mark"]
             score_dict[tid] = int(cur_score)
        except:
            pass

    score_dict = dict(sorted(score_dict.items(), key=lambda x: x[1]))

    gpu_ids = []
    for key, val in score_dict.items():
        gpu_ids.append(key)

    n = len(gpu_ids)
    num_samples = 3
    for ind in range(10, n-10):
        cur_gpu = gpu_ids[ind]
        prev_gpus = np.random.choice(gpu_ids[:ind], num_samples, replace=False)
        next_gpus = np.random.choice(gpu_ids[ind+1:], num_samples, replace=False)

        for p_gpu in prev_gpus:
            data.append([cur_gpu, p_gpu, 1])

        for n_gpu in next_gpus:
            if score_dict[cur_gpu] < score_dict[n_gpu]:
                data.append([cur_gpu, n_gpu, 0])

    df = pd.DataFrame(data=data, columns=cols)
    df.to_csv("gpu_classification_dataset.csv", index=False)

if __name__ == "__main__":
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs_cleaned.jl"
    benchmark_gpu_file = "../../data_with_ids/gpu_benchmarks.jl"
    mapping_file = "../../data_er/ER_benchmark_gpus_and_techpowerup_gpus.jl"

    techpowerup_gpus = constructDictfromJL(techpowerup_gpu_file)
    benchmark_gpus = constructDictfromJL(benchmark_gpu_file)
    gpu_map = createMap(mapping_file)

    # Create Regression Dataset:
    createRegressionDataset()
    createClassificationDataset()