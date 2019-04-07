#test_classifier

import classifier
import os
from decimal import Decimal

cwd = classifier.current_working_dir()
demo_train_data = "{}/pytest_data/training_data/".format(cwd)
test_data_dir = "{}/pytest_data/testing_data/".format(cwd)
dir_of_nonsports = demo_train_data+"/non_sports_data"
dir_of_sports = demo_train_data+"/sports_data"

def test_current_working_dir():
    assert classifier.current_working_dir() == "{}" .format(cwd)

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
    assert classifier.count_possible_words(demo_train_data) == 7

def test_count_duplicate():
    assert classifier.count_duplicates(test_data_dir) == {'election':2, 'game':1, 'match':1, 'time':1}
    assert classifier.count_duplicates(dir_of_nonsports) == {'election':2, 'close':1}
    assert classifier.count_duplicates(dir_of_sports) == {'clean': 2, 'game': 2, 'forgettable': 1, 'great': 1, 'match': 1}
    
def test_trained_datas():
    assert classifier.train_data(demo_train_data) == {'non_sports_data':{'election':0.299999999999999988897769753748434595763683319091796875,
                                                                            'close':0.200000000000000011102230246251565404236316680908203125},
                                                         'sports_data':{'clean':0.2142857142857142738190390218733227811753749847412109375,
                                                                        'game':0.2142857142857142738190390218733227811753749847412109375,
                                                                        'forgettable':0.142857142857142849212692681248881854116916656494140625,
                                                                        'great':0.142857142857142849212692681248881854116916656494140625,
                                                                        'match':0.142857142857142849212692681248881854116916656494140625}}

def test_count_files():
    list_directory = os.listdir(demo_train_data)
    path = demo_train_data
    assert classifier.count_files(list_directory, path) == 5

def test_prob_of_absent():
    assert classifier.probability_of_absence(demo_train_data) == {'sports_data': Decimal('0.0714285714285714246063463406244409270584583282470703125'),
                                                                  'non_sports_data': Decimal('0.1000000000000000055511151231257827021181583404541015625')}
    

def test_list_test_data():
    assert classifier.get_words_for_test(test_data_dir, "sports data") == {'sports data': {'game': None, 'match': None}}

    
def test_prediction():
    trained_data = {'non_sports_data':{'election':0.299999999999999988897769753748434595763683319091796875,
                                       'close':0.200000000000000011102230246251565404236316680908203125},
                    'sports_data':{'clean':0.2142857142857142738190390218733227811753749847412109375,
                                   'game':0.2142857142857142738190390218733227811753749847412109375,
                                   'forgettable':0.142857142857142849212692681248881854116916656494140625,
                                   'great':0.142857142857142849212692681248881854116916656494140625,
                                   'match':0.142857142857142849212692681248881854116916656494140625}}
    prob_of_absence = {'sports_data': Decimal('0.0714285714285714246063463406244409270584583282470703125'),
                       'non_sports_data': Decimal('0.1000000000000000055511151231257827021181583404541015625')}
    test_dict = {'sports data': {'game': None, 'match': None}}

    assert classifier.predict(trained_data, test_dict, demo_train_data, prob_of_absence) =={'sports data':
                                                                                               {'non_sports_data': Decimal('0.004000000000000000666133814773'),
                                                                                                'sports_data': Decimal('0.01836734693877550748516810296')}}


def test_percentage():
    predicted_data =  {'sports data': {'non_sports_data': Decimal('0.004000000000000000666133814773'),
                                       'sports_data': Decimal('0.01836734693877550748516810296')},
                       'non_sports data': {'non_sports_data':Decimal('0.01200000000000000088817841970'),
                                           'sports_data': Decimal('0.003061224489795917914194683827')}}
    assert classifier.get_percentage(predicted_data) == {'sports data': {'non_sports_data': Decimal('17.88321167883212140771907556'),
                                                                         'sports_data': Decimal('82.11678832116787859228092445')},
                                                         'non_sports data': {'non_sports_data': Decimal('79.67479674796748327060137526'),
                                                                             'sports_data': Decimal('20.32520325203251672939862472')}}
    

