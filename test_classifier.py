#test_classifier

import classifier
import os

cwd = classifier.current_working_dir()

def test_current_working_dir():
    assert classifier.current_working_dir() == "{}".format(cwd)

def test_path_train_data():
    assert classifier.path_train_data() == "{}/training_data/".format(cwd)

def test_test_data():
    assert classifier.path_test_data() == "{}/testing_data".format(cwd)

def test_clean_data():
    assert classifier.clean_data("hello  i am // here. :") == ['am', 'hello', 'here', 'i']

def test_remove_stop_words():
    classifier.remove_stop_words(['am', 'hello', 'here', 'i']) == ['hello']
