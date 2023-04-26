from app import app
import os
import io
import numpy as np
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from app.queries import getGameInformation, getClassProperties, getLinkedDeviceData, getRecommendedGameInformation
from app.queries import generate_visualization_data, final_query, getGameRequirementsInformation
from app.queries import getGenres, getThemes, getGameModes

gl_device_config = None
gl_device_config_string = None
gl_embeddings_model = None

def load_vectors(embeddings_file):
    f = io.open(embeddings_file, 'r', encoding='utf-8', newline='\n', errors='ignore')
    e_model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        e_model[word] = embedding
    print("Done.", len(e_model), " words loaded!")
    return e_model

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/storeConfig', methods=['GET', 'POST'])
def storeConfig():
    global gl_device_config, gl_embeddings_model, gl_device_config_string

    if gl_embeddings_model is None:
        embeddings_file_name = "game_embeddings_constructed_with_fasttext.vec"
        gl_embeddings_model = load_vectors(embeddings_file_name)

    gl_device_config, valid_flag = getLinkedDeviceData(request.form)
    print(gl_device_config)
    gl_device_config_string = str(gl_device_config["ram_MB"]) + " MB RAM, " + str(gl_device_config["hdd_space_MB"]) + " MB HDD, " + "Processor = " + gl_device_config["processor_val"] + ", Graphics card = " + gl_device_config["graphics_card_val"]

    print(valid_flag)
    if valid_flag == 1:
        return "<h3 class=\"w3-green\">Successfully stored the device configuration!</h3>"
    else:
        return "<h3 class=\"w3-red\">The given device configuration is invalid! Please submit again!</h3>"

@app.route('/query')
def queryPage():
    global gl_device_config

    print(gl_device_config)
    genre_list = getGenres()
    game_mode_list = getGameModes()
    theme_list = getThemes()
    return render_template('query.html', genre_list=genre_list, theme_list=theme_list, game_mode_list=game_mode_list)

@app.route('/queryData', methods=['GET', 'POST'])
def queryData():
    global gl_device_config

    input_param_dict = dict(request.form)
    print(input_param_dict)
    result_dict = final_query(input_param_dict, gl_device_config)
    return result_dict


@app.route('/game', methods=['GET'])
def gamePage():
    '''
    pass game_id as 'mig_0'. do not pass the namespace -> mgns
    :return: game_info ---> dictionary (key, value pair with values being string)
                    keys are:
                    1. game_summary
                    2. name
                    3. released_year
                    4. platform_name
                    5. developer_name
                    6. publisher_name
                    7. game_mode_label
                    8. genre_label
                    9. theme_label
                    10. rating
                    11. seller_name
                    12. price
                    13. discount
                    14. url
             Note:
    '''
    global gl_device_config, gl_embeddings_model, gl_device_config_string

    game_id = request.args.get("game_id")
    if game_id is None:
        game_id = "mig_0"

    game_info = getGameInformation(game_id)
    game_req_list = getGameRequirementsInformation(game_id)

    recommended_games_info = getRecommendedGameInformation(game_id, gl_device_config, gl_embeddings_model)
    recommended_games_list = []
    for i in range(1, 6):
        recommended_games_list.append(recommended_games_info[i])
    print(recommended_games_info)

    return render_template('game.html', game_info=game_info, device_config_str=gl_device_config_string, game_req_list=game_req_list, rec_games_list=recommended_games_list)

@app.route('/getPropertiesForClass', methods=['GET', 'POST'])
def getPropertiesForClass():
    cur_class_name = request.args.get("class_name")
    class_properties_dict = getClassProperties()
    cur_prop_list = class_properties_dict[cur_class_name]
    result = {}
    result["vals"] = cur_prop_list
    return result

@app.route('/visualize')
def visualizationPage():
    class_properties_dict = getClassProperties()
    class_list = list(class_properties_dict.keys())
    return render_template('visualization.html', class_list=class_list)

@app.route('/getVisualizationData', methods=['GET', 'POST'])
def getVisualizationData():
    class_name = request.args.get("class_name")
    property_name = request.args.get("property_name")
    result = generate_visualization_data(class_name, property_name)
    result_dict = {}

    if not isinstance(result[0], tuple):
        result_dict["data_type"] = "continuous"
        result_dict["x_vals"] = result
    else:
        x_vals = []
        y_vals = []
        for key, val in result:
            x_vals.append(key)
            y_vals.append(val)

        result_dict = {}
        result_dict["data_type"] = "discrete"
        result_dict["x_vals"] = x_vals
        result_dict["y_vals"] = y_vals

    return result_dict
