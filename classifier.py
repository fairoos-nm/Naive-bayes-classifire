#classifier.py

import os
import re
from prettytable import PrettyTable
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

def clean_data(data_for_clean):
    """Make given string of data in to useable format"""
    data_contents = re.sub(r'[^\w\s]', '', data_for_clean) #remove punctuation
    data_contents = ''.join([i for i in data_contents if not i.isdigit()]) #remove digits
    contents_list = data_contents.split()
    contents_list.sort()
    contents_list = [x.lower() for x in contents_list] #to lower case all words    
    contents_list = remove_stop_words(contents_list)
    return contents_list

def remove_stop_words(input_words):
    """Remove commen words like us, was, is etc.."""
    cwd = current_working_dir()
    Stopwords_file_path = '{}/stop_words_dir/stop_words.txt'.format(cwd)
    Stopwords_file = open(Stopwords_file_path)
    StopWord_file_contents = Stopwords_file.read()
    list_of_StopWords = StopWord_file_contents.split()
    NonStopWords = list()
    for word in input_words: 
        if word not in list_of_StopWords:
            NonStopWords.append(word)    
    return NonStopWords

def words_in_dir(path_to_dir):
    """return all words in the given directory after clean"""
    files_contents = ''
    files_in_dir = os.listdir(path_to_dir)
    for FileName in files_in_dir:
        file_path = os.path.join(path_to_dir, FileName)
        File = open(file_path)
        file_content = File.read()
        files_contents += file_content
    list_of_words = clean_data(files_contents)
    return list_of_words 

def count_possible_words(train_data_path):
    """to count all possible words in training data"""
    list_of_possible_words = []
    directories = os.listdir(train_data_path)
    for directory in directories:
        path = ("{}{}".format(train_data_path, directory))
        list_of_possible_words.extend(words_in_dir(path)) # combain lists
        list_of_possible_words = list(dict.fromkeys(list_of_possible_words)) # remove duplicates from List:
        list_words = remove_stop_words(list_of_possible_words)
    count_of_possible_words = len(list_of_possible_words)
    return count_of_possible_words

def count_duplicates(path):
    """count number of same words"""
    list_words = words_in_dir(path)
    count_of_duplicates = Counter(list_words)
    return count_of_duplicates

def train_data(path):
    """train avilable data"""
    count_of_possible_words = count_possible_words(path)
    GnereProbability = {} #synthax = {gnere:{word:probability}}
    genres_directories_list = os.listdir(path)
    for genre_directory in genres_directories_list:
        WordProbability = {}  #synthax = {word:probability}
        path_to_genre_directory = os.path.join(path, genre_directory)
        count_of_total_words = len(words_in_dir(path_to_genre_directory))
        words_count = count_duplicates(path_to_genre_directory)
        for word, number_of_word in words_count.items():
            probability = Decimal((number_of_word + 1) / (count_of_total_words + count_of_possible_words ))
            WordProbability.update({word:probability})
        GnereProbability.update({genre_directory:WordProbability})
        GnereProbability = OrderedDict(GnereProbability)
    return GnereProbability

def count_files(list_directory, path):
    """count files in a directory"""
    count = 0
    for directory in list_directory:
        count += len(os.listdir("{}{}".format(path, directory)))
    return count

def probability_of_absence(path):
    """If a word is not in trained data ,we assign a value as per lapscale smoothing"""
    absence_dict = {}
    count_of_possible_words = count_possible_words(path)
    for gnere_dire in os.listdir(path):
        dir_path = os.path.join(path, gnere_dire)
        count_of_total_words = len(words_in_dir(dir_path))
        probability = Decimal( 1 / (count_of_possible_words + count_of_total_words))
        absence_dict.update({gnere_dire:probability})
    return absence_dict

def get_words_for_test(path_test_data, filename):
    """take words for testing as a dict"""
    words = dict()
    test_file = open("{}/{}".format(path_test_data, filename))
    contents = test_file.read()
    list_of_words = clean_data(contents)
    words_for_test =  dict.fromkeys(list_of_words)
    words.update({filename:words_for_test})
    return words

#In train data directory, some subdirectories be there. subdirectories are in the name of artists.

def predict(trained_data, test_data, path_train_data, prob_of_absence):
    """predict given song belonges to which artist using trained data"""
    prediction = dict()
    for file_name, testData in test_data.items():
        GenreFileprob = dict()   
        for genre, trained_words in trained_data.items():
            absent = prob_of_absence.get(genre)
            total_files = count_files(os.listdir(path_train_data), path_train_data)
            number_of_files_in_gerne_dir = len(os.listdir('{}{}'.format(path_train_data, genre)))
            probability_of_genre = Decimal(number_of_files_in_gerne_dir / total_files)
            probability_of_present = 1
            probability_of_absent = 1
            for word in testData:
                if word in trained_words:
                    value = trained_words.get(word)
                    probability_of_present = Decimal(probability_of_present * Decimal(value))
                else:
                    probability_of_absent = Decimal(probability_of_absent * absent)        
            AddedProb = Decimal(probability_of_present * probability_of_absent)
            probability = Decimal(AddedProb * probability_of_genre)
            GenreFileprob.update({genre:probability})
        prediction.update({file_name:GenreFileprob})    
    return prediction

def get_percentage(predicted_data):
    """calculate the percentage of prediction"""
    SongPercentage = dict()
    for name_of_song, prdictions in predicted_data.items():
        predicted_values = prdictions.values()
        sum_of_predicted_values = sum(predicted_values)
        GenrePercentage = dict()
        for genre ,predicted_value in prdictions.items():
            try:
                percentage = (predicted_value / sum_of_predicted_values) * 100
                GenrePercentage.update({genre:percentage})
            except ZeroDivisionError:
                percentage = 0
        SongPercentage.update({name_of_song:GenrePercentage})
    return SongPercentage

def display_status(percentage_data):
    success = 0
    wrong = 0
    count = 0
    table = PrettyTable(['Name of Songs', 'Prediction'])
    for name_of_song , percentage in percentage_data.items():
        count += 1
        HighestPercentageGenre = max(percentage.items(), key=operator.itemgetter(1))[0]
        table.add_row([name_of_song, HighestPercentageGenre])
        #In our data every song's name start with thair artist's name and directory in test data are in the name of artist.
        #If song's first name and HighestPercentageGenre(highest probability artist) are start with same name we can decide thath this prediction is correct.
        name = name_of_song.split()
        highest = HighestPercentageGenre.split()
        name = name[0].lower()
        highest = highest[0].lower()
        if highest[0] == name[0]:
            success += 1
        else:
            wrong += 1
    print(table)
    print()
    print("Your model predict {} success and {} Wrong".format(success, wrong))
    print()
    success_percentage = (success/count)* 100
    print("Your system is {} % accurate".format(success_percentage))
    print()
    print("💖💖 ⮘⮘Thank You⮚⮚ 💖💖")
    
def main():
    train_data_path = path_train_data()
    test_data_path = path_test_data()
    prob_of_absence = probability_of_absence(train_data_path)      
    trained_data = train_data(train_data_path)
    predicted_datas = dict()
    for filename in os.listdir(test_data_path):
        test_words = get_words_for_test(test_data_path, filename)
        predicted_data = predict(trained_data, test_words, train_data_path, prob_of_absence)
        predicted_datas.update(predicted_data)
    percentage_of_predictions= get_percentage(predicted_datas)    
    display_status(percentage_of_predictions)

if __name__ == "__main__" :
    main()
