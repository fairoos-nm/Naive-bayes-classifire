import os


def current_working_dir():
    cwd = os.getcwd()
    return cwd

def path_train_data():
    cwd = current_working_dir()
    return "{}/training_data/".format(cwd)

def path_test_data():
    cwd = current_working_dir()
    return "{}/testing_data".format(cwd)

