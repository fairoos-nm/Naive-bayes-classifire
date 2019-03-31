#classifier.py

import os
import re
from collections import Counter
from decimal import Decimal
from collections import OrderedDict
import time
from tqdm import tqdm

def current_working_dir():
    cwd = os.getcwd()
    return cwd

def path_train_data():
    cwd = current_working_dir()
    return "{}/training_data/".format(cwd)

def path_test_data():
    cwd = current_working_dir()
    return "{}/testing_data".format(cwd)

def clean_data(data):
    data_contents = re.sub(r'[^\w\s]', '', data) #remove punctuation
    data_contents = ''.join([i for i in data_contents if not i.isdigit()]) #remove digits
    contents_list = data_contents.split()
    contents_list.sort()
    contents_list = [x.lower() for x in contents_list] #to lower case all words
    contents_list = remove_stop_words(contents_list)
    return contents_list

def remove_stop_words(input_data):
    cwd = current_working_dir()
    stop_words_file = '{}/stop_words_dir/stop_words.txt'.format(cwd)
    stop_words_file = open(stop_words_file)
    contents = stop_words_file.read()
    list_contents = contents.split()
    all_words = input_data
    words = list()
    for word in all_words: 
        if word not in list_contents:
            words.append(word)    
    return words

def words_in_dir(path):
    files_contents = ''
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        opened_file = open(file_path)
        content = opened_file.read()
        files_contents += content
    words_list = clean_data(files_contents)
    return words_list

def possible_words(data_path):
    """to count all possible words in training data"""
    list_words = []
    for dir in os.listdir(data_path):
        path = ("{}{}".format(data_path, dir))
        list_words.extend(words_in_dir(path)) # combain lists
        list_words = list(dict.fromkeys(list_words)) # rm duplicates from List:
        list_words = remove_stop_words(list_words)
    count = len(list_words)
    return count

def count_duplicate(path):
    list_words = words_in_dir(path)
    counts = Counter(list_words)
    return counts

def trained_datas(path):
    count_of_possible_words = possible_words(path)
    probability_dict = {}
    for dire in os.listdir(path):
        list_of_probability = list()
        dict_of_an_item = {}
        dir_path = os.path.join(path, dire)
        total_words = len(words_in_dir(dir_path))
        words_count = count_duplicate(dir_path)
        keys = words_count.keys()
        values = words_count.values()
        for value in values:
            probability = Decimal((value + 1) / (total_words + count_of_possible_words ))
            list_of_probability.append(probability)
        for word, probability in zip(keys, list_of_probability):
            dict_of_an_item.update({word:probability})
        probability_dict.update({dire:dict_of_an_item})
        probability_dict = OrderedDict(probability_dict)
    return probability_dict

def count_files(list_directory, path):
    """count files in a directory"""
    count = 0
    for directory in list_directory:
        count += len(os.listdir("{}{}".format(path, directory)))
    return count

def probability_of_absence(path, item):
    count_of_possible_words = possible_words(path)
    dir_path = os.path.join(path, item)
    total_words = len(words_in_dir(dir_path))
    probability = Decimal( 1 / (count_of_possible_words + total_words))
    return probability

def prediction(path_train_data, path_test_data):
    #open the first file in test dir and convert that text file in to list of words.
    #the list dosent contain repeted words and stop words.
    final_out = dict()
    for filename in tqdm(os.listdir(path_test_data)):
        test_file = open("{}/{}".format(path_test_data, filename))
        contents = test_file.read()
        words_list_for_test = clean_data(contents)
        words_list_for_test = list(dict.fromkeys(words_list_for_test)) #remove repeted words
        
        #call trained data and convert them in to useable format.
        trained_words_dict = trained_datas(path_train_data) # format = {matalica :{"hello:4542444, good:45221"}, justin_b:{hello:243}}
        list_of_dict = list(trained_words_dict.values()) #list contains dict. in that dict we have key as words and values as probability 
        items = list(trained_words_dict.keys()) #list of items eg: metalica_lyrics ,justin_b....
        item_prob = dict()
        for item, single_dict in zip(items, list_of_dict):
            mux_list = list()
            absent = probability_of_absence(path_train_data, item)
            [mux_list.append(single_dict.get(word)) if word in single_dict
             else mux_list.append(absent) for word in words_list_for_test]

            probability_mux = 1
            #multiplyig all the values in list.
            for prob in mux_list:
                probability_mux = Decimal(probability_mux * prob)   
            total_files = count_files(os.listdir(path_train_data), path_train_data)
            file_count_in_item_dir = len(os.listdir('{}{}'.format(path_train_data, item)))
            prob_of_item = Decimal(file_count_in_item_dir / total_files)
            #Result of multiplication finaly multiply with probability of an item
            final_proba = Decimal(probability_mux * prob_of_item)
            item_prob.update({item:final_proba})
        final_out.update({filename:item_prob})
    return final_out

def get_percentage(predicted_data):
    name_of_songs = predicted_data.keys()
    list_of_prdiction = predicted_data.values()
    return_dict = dict()
    for name_of_song, dictionary in zip(name_of_songs, list_of_prdiction):
        items = dictionary.keys()
        predicted_values = dictionary.values()
        sum_of_predicted_values = sum(predicted_values)
        dict_of_percent = dict()
        for item, predicted_value in zip(items, predicted_values):
            try:
                percentage = (predicted_value / sum_of_predicted_values) * 100
                dict_of_percent.update({item:percentage})
            except ZeroDivisionError:
                percentage = 0
        return_dict.update({name_of_song:dict_of_percent})
    return return_dict

if __name__ == "__main__": 
    train_data = path_train_data()
    test_data = path_test_data()
    print(get_percentage(prediction(train_data, test_data )))
