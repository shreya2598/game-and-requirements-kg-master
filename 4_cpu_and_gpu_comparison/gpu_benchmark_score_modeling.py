import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
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

def testRegression(model, X_test, y_test):
    r2_val = model.score(X_test, y_test)
    n = X_test.shape[0]
    p = X_test.shape[1]
    adjusted_r2_val = 1 - ((1 - r2_val) * (n - 1) / (n - p - 1))
    print("Regression results: ")
    print("R^2 value = ", r2_val)
    print("Adjusted R^2 value = ", adjusted_r2_val, "\n")

def testClassification(model, X_test, y_test):
    y_pred = model.predict(X_test)

    y_pred = list(y_pred)
    y_test = list(y_test)

    y_pred_scores = {}
    y_test_scores = {}
    keys = []
    index = 0
    for i, j in zip(y_pred, y_test):
        y_pred_scores[index] = i
        y_test_scores[index] = j
        keys.append(index)
        index += 1

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    n = len(keys)
    num_samples = 3
    for ind in range(5, n - 5):
        cur_key = keys[ind]
        prev_keys = np.random.choice(keys[:ind], num_samples, replace=False)
        next_keys = np.random.choice(keys[ind + 1:], num_samples, replace=False)

        for p_key in prev_keys:
            if y_test_scores[cur_key] >= y_test_scores[p_key]:
                if y_pred_scores[cur_key] >= y_pred_scores[p_key]:
                    tp += 1
                else:
                    fn += 1
            else:
                if y_pred_scores[cur_key] < y_pred_scores[p_key]:
                    tn += 1
                else:
                    fp += 1

        for n_key in next_keys:
            if y_test_scores[cur_key] >= y_test_scores[n_key]:
                if y_pred_scores[cur_key] >= y_pred_scores[n_key]:
                    tp += 1
                else:
                    fn += 1
            else:
                if y_pred_scores[cur_key] < y_pred_scores[n_key]:
                    tn += 1
                else:
                    fp += 1

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1_score = 2 * precision * recall / (precision + recall)

    print("Classification results: ")
    print("Precision = ", precision)
    print("Recall = ", recall)
    print("F1 score = ", f1_score, "\n")

def normalizeCols(col_name, df, scaler):
    out_data = scaler.fit_transform(np.array(df[col_name]).reshape(-1, 1))
    out_data = np.squeeze(out_data)
    return out_data

if __name__ == "__main__":
    regression_dataset_file = "gpu_regression_dataset.csv"
    df = pd.read_csv(regression_dataset_file)

    # Handle Categorical Variables:
    memory_type_feat_cols = pd.get_dummies(df["memory_type"], prefix="memory_type")

    # Drop low importance features:
    df.drop(columns=["gpu_chip", "memory_type", "bus_info"], inplace=True)

    df_total = pd.concat([df, memory_type_feat_cols], axis=1)

    # Normalize the features:
    cols_to_normalize = ["released_year", "memory_val_mb", "memory_bits", "gpu_clock_mhz",
                         "memory_clock_mhz", "shader_1", "shader_2", "tmus", "rops"]
    scaler = MinMaxScaler()
    for col in cols_to_normalize:
        df_total[col] = normalizeCols(col, df_total, scaler)

    df_total.fillna(0, inplace=True)
    df_total.replace(-1, 0, inplace=True)

    # Split the data set into train and test
    X_data = df_total.drop(columns=["g3d_mark"])
    y_data = df_total["g3d_mark"]
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=1)

    # Train the model
    model = train(X_train, y_train)

    # Test the model
    testRegression(model, X_test, y_test)
    testClassification(model, X_test, y_test)