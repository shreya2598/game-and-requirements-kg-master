import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import json
import jsonlines
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def train(X_train, y_train):
    regr = RandomForestRegressor(max_depth=4, random_state=0)
    regr.fit(X_train, y_train)

    feat_imp = regr.feature_importances_
    feat_labels = list(X_train.columns)

    feat_importances = {}
    for key, val in zip(feat_labels, feat_imp):
        feat_importances[key] = val

    feat_importances = dict(sorted(feat_importances.items(), key=lambda x: x[1], reverse=True))

    print("Top-5 most important features:")
    print(list(feat_importances.items())[0:5], "\n")
    return regr

def convertToDataFrame(json_lines_file, gpu_map, benchmark_gpus):
    train_cols = []
    train_data = []

    test_cols = []
    test_data = []
    with open(json_lines_file, "r") as f:
        for cur_line in f:
            cur_dict = json.loads(cur_line)
            key = list(cur_dict.keys())[0]
            val = list(cur_dict.values())[0]

            if gpu_map.get(key) is not None:
                if len(train_cols) == 0:
                    train_cols = ["gpu_id"] + list(val.keys()) + ["g3d_mark"]

                train_data.append([key] + list(val.values()) + [benchmark_gpus[gpu_map[key]]["g3d_mark"]])
            else:
                if len(test_cols) == 0:
                    test_cols = ["gpu_id"] + list(val.keys()) + ["g3d_mark"]

                test_data.append([key] + list(val.values()) + [-1])

    df_train = pd.DataFrame(data=train_data, columns=train_cols)
    df_test = pd.DataFrame(data=test_data, columns=test_cols)
    return df_train, df_test

def convertToJsonLines(input_df, out_file_name):
    input_df = input_df.set_index("gpu_id")
    input_df.to_json("temp.json", orient="index")
    with open("temp.json", "r") as f:
        temp_dict = json.load(f)

    result_list = []
    for key, val in temp_dict.items():
        cur_dict = {}

        # Un-escaping the product url string
        val["product_url"] = val["product_url"].encode().decode('unicode_escape')

        cur_dict[key] = val
        result_list.append(cur_dict)

    result_list.sort(key=lambda x: int(list(x.keys())[0].split("_")[-1]))

    with jsonlines.open(out_file_name, "w") as f:
        f.write_all(result_list)

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

    return result_dict

def normalizeCols(col_name, df, scaler):
    out_data = scaler.fit_transform(np.array(df[col_name]).reshape(-1, 1))
    out_data = np.squeeze(out_data)
    return out_data

if __name__ == "__main__":
    # Config:
    techpowerup_gpu_file = "../../data_with_ids/techpowerup_gpu_specs_cleaned.jl"
    benchmark_gpu_file = "../../data_with_ids/gpu_benchmarks.jl"
    mapping_file = "../../data_er/ER_benchmark_gpus_and_techpowerup_gpus.jl"

    benchmark_gpus = constructDictfromJL(benchmark_gpu_file)
    gpu_map = createMap(mapping_file)
    df_train, df_test = convertToDataFrame(techpowerup_gpu_file, gpu_map, benchmark_gpus)
    df_total = pd.concat([df_train, df_test], axis=0)

    num_train_rows = df_train.shape[0]

    # Handle Categorical Variables:
    memory_type_feat_cols = pd.get_dummies(df_total["memory_type"], prefix="memory_type")

    df_total_v2 = pd.concat([df_total, memory_type_feat_cols], axis=1)

    # Normalize the features:
    df_total_v2.fillna(0, inplace=True)
    df_total_v2.replace(-1, 0, inplace=True)
    cols_to_normalize = ["released_year", "memory_val_mb", "memory_bits", "gpu_clock_mhz",
                         "memory_clock_mhz", "shader_1", "shader_2", "tmus", "rops"]
    scaler = MinMaxScaler()
    for col in cols_to_normalize:
        df_total_v2[col] = normalizeCols(col, df_total_v2, scaler)

    # Train on the whole available data:
    df_train_v2 = df_total_v2[:num_train_rows]
    df_test_v2 = df_total_v2[num_train_rows:]

    X_train = df_train_v2.drop(columns=["gpu_chip", "memory_type", "bus_info", "product_name", "product_url", "gpu_id", "g3d_mark"])
    y_train = df_train_v2["g3d_mark"]
    model = train(X_train, y_train)

    # Predict on the un-available data:
    X_test = df_test_v2.drop(columns=["gpu_chip", "memory_type", "bus_info", "product_name", "product_url", "gpu_id", "g3d_mark"])
    y_pred = model.predict(X_test)
    df_test["g3d_mark"] = list(y_pred)
    df_test["g3d_mark"] = df_test["g3d_mark"].astype(int)
    df_train["g3d_mark"] = df_train["g3d_mark"].astype(int)

    # Convert to the previous format and store:
    new_df = pd.concat([df_train, df_test], axis=0)
    convertToJsonLines(new_df, "techpowerup_gpu_specs_cleaned_with_scores.jl")


