import os
import re
from collections import Counter
from decimal import Decimal

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
    return probability_dict

def train_data():
    pass

#probability_of_words(path_train_data())

# data_path= path_test_data()
# print(count_duplicate(data_path))
