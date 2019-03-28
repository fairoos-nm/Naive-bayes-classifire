import os
import re


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
        print(filename)
        file_path = os.path.join(path, filename)
        opened_file = open(file_path)
        content = opened_file.read()
        files_contents += content
    words_list = clean_data(files_contents)
    return words_list

def train_data():
    pass

path = path_test_data()
print(words_in_dir(path))
