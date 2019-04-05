#classifier.py

import os
import re
from collections import Counter
from decimal import Decimal
from collections import OrderedDict
import operator

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

def probability_of_absence(path):
    absence_dict = {}
    count_of_possible_words = possible_words(path)
    for dire in os.listdir(path):
        dir_path = os.path.join(path, dire)
        total_words = len(words_in_dir(dir_path))
        probability = Decimal( 1 / (count_of_possible_words + total_words))
        absence_dict.update({dire:probability})
    return absence_dict

def list_test_data(path_test_data, filename):
    words_dict = dict()
    test_file = open("{}/{}".format(path_test_data, filename))
    contents = test_file.read()
    words_list_for_test = clean_data(contents)
    words_for_test =  dict.fromkeys(words_list_for_test)
    words_dict.update({filename:words_for_test})
    return words_dict

def prediction(trained_data, test_dict, path_train_data, prob_of_absence):
    final_out = dict()
    for file_name, testData in test_dict.items():
        gerne_prob = dict()   
        for gerne, trained_dict in trained_data.items():
            absent = prob_of_absence.get(gerne)
            total_files = count_files(os.listdir(path_train_data), path_train_data)
            file_count_in_gerne_dir = len(os.listdir('{}{}'.format(path_train_data, gerne)))
            prob_of_gerne = Decimal(file_count_in_gerne_dir / total_files)
            probability_of_present = 1
            probability_of_absent = 1
            for word in testData:
                if word in trained_dict:
                    value = trained_dict.get(word)
                    probability_of_present = Decimal(probability_of_present * value)
                else:
                    probability_of_absent = Decimal(probability_of_absent * absent)        
            probability = Decimal(probability_of_present * probability_of_absent)
            final_proba = Decimal(probability * prob_of_gerne)
            gerne_prob.update({gerne:final_proba})
        final_out.update({file_name:gerne_prob})    
    return final_out

def get_percentage(predicted_data):
    return_dict = dict()
    for name_of_song, prdictions in predicted_data.items():
        predicted_values = prdictions.values()
        sum_of_predicted_values = sum(predicted_values)
        dict_of_percent = {}
        for gerne ,predicted_value in prdictions.items():
            try:
                percentage = (predicted_value / sum_of_predicted_values) * 100
                dict_of_percent.update({gerne:percentage})
            except ZeroDivisionError:
                percentage = 0
        return_dict.update({name_of_song:dict_of_percent})
    return return_dict

def display_status(percentage_data):
    name_list = list()
    highest_lsit = list()
    success = 0
    wrong = 0
    count = 0
    for name_of_song , percentage in percentage_data.items():
        count += 1
        highest = max(percentage.items(), key=operator.itemgetter(1))[0]
        print("{} ➩ {}".format(name_of_song, highest ))
        name = name_of_song.split()
        highest = highest.split()
        name = [x.lower() for x in name]
        highest = [x.lower() for x in highest]
        if highest[0] == name[0]:
            success += 1
        else:
            wrong += 1
    print()
    print("Your model predict {} success and {} Wrong".format(success, wrong))
    print()
    success_percentage = (success/count)* 100
    print("Your system is {} % accurate".format(success_percentage))
    print()
    print("💖💖 ⮘⮘Thank You⮚⮚ 💖💖")
    
def main():
    train_data = path_train_data()
    test_data = path_test_data()
    prob_of_absence = probability_of_absence(train_data)      
    trained_data = trained_datas(train_data)
    predicted_data_dict = dict()
    for filename in os.listdir(test_data):
        test_dict = list_test_data(test_data, filename)
        predicted_data = prediction(trained_data, test_dict, train_data, prob_of_absence)
        predicted_data_dict.update(predicted_data)
    percentage_data = get_percentage(predicted_data_dict)    
    display_status(percentage_data)

if __name__ == "__main__" :
    main()
