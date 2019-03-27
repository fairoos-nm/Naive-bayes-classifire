#test_classifier

import classifier
import os
cwd = os.getcwd()
def test_current_working_dir():
    assert classifier.current_working_dir() == "{}".format(cwd)

def test_path_train_data():
    assert classifier.path_train_data == "{}".format(cwd)+ "/training_data/"
