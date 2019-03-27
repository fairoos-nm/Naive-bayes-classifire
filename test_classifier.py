#test_classifier

import classifier
import os
cwd = os.getcwd()
def test_current_working_dir():
    assert classifier.current_working_dir() == "{}".format(cwd)

def test_data_for_train():
    assert classifier.data_for_train == "{}".format(cwd)+ "/training_data/"
