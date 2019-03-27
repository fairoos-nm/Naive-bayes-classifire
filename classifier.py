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
    return contents_list
