#test_classifier

import classifier
import os

cwd = classifier.current_working_dir()
demo_train_data = "{}/pytest_data/training_data/".format(cwd)
test_data_dir = "{}/pytest_data/testing_data/".format(cwd)
dir_of_nonsports = demo_train_data+"/non_sports_data"
dir_of_sports = demo_train_data+"/sports_data"

def test_current_working_dir():
    assert classifier.current_working_dir() == "{}".format(cwd)

def test_path_train_data():
    assert classifier.path_train_data() == "{}/training_data/".format(cwd)

def test_test_data():
    assert classifier.path_test_data() == "{}/testing_data".format(cwd)

def test_clean_data():
    assert classifier.clean_data("hello  i am // here. :") == ['hello']

def test_remove_stop_words():
    classifier.remove_stop_words(['am', 'hello', 'here', 'i']) == ['hello']
    
def test_words_in_dir():
    assert classifier.words_in_dir(test_data_dir) == ['election', 'election', 'game', 'match', 'time']
    assert classifier.words_in_dir(dir_of_nonsports) == ['close', 'election', 'election']

def test_possible_words():
    assert classifier.possible_words(demo_train_data) == 7

def test_count_duplicate():
    assert classifier.count_duplicate(test_data_dir) == {'election':2, 'game':1, 'match':1, 'time':1}
    assert classifier.count_duplicate(dir_of_nonsports) == {'election':2, 'close':1}
    assert classifier.count_duplicate(dir_of_sports) == {'clean': 2, 'game': 2, 'forgettable': 1, 'great': 1, 'match': 1}
    
def test_trained_datas():
    assert classifier.trained_datas(demo_train_data) == {'non_sports_data':{'election':0.299999999999999988897769753748434595763683319091796875,
                                                                            'close':0.200000000000000011102230246251565404236316680908203125},
                                                         'sports_data':{'clean':0.2142857142857142738190390218733227811753749847412109375,
                                                                        'game':0.2142857142857142738190390218733227811753749847412109375,
                                                                        'forgettable':0.142857142857142849212692681248881854116916656494140625,
                                                                        'great':0.142857142857142849212692681248881854116916656494140625,
                                                                        'match':0.142857142857142849212692681248881854116916656494140625}}
    
