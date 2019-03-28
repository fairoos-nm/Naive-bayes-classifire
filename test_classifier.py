#test_classifier

import classifier
import os

cwd = classifier.current_working_dir()
demo_train_data = "{}/pytest_data/training_data/".format(cwd)

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
    assert classifier.words_in_dir(demo_train_data) == ['am', 'hello', 'here', 'i']
    
def test_train_data():
    assert classifirer.train_data(demo_train_data) == {"sports_data":{"grate":1, "game":2, "very":1, "clean":2, "match":1, "forgettable":1}, "non_sports_data":{"election":2, "close":1}}
