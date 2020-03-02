"""
Author:
    * Jeremiah D 'JD' Smith

Description:
    * Takes in texts and breaks them down to tokens/words
    * Then counts the frequency of the tokens/words
"""
import os
import operator
from nltk.stem import PorterStemmer  # imported because I can't use java based Porter stemmer


# TODO: Reformat entire code into functions and modules


# convert stopwords text to list
def stopwords(stop_path):
    # create list of stopwords
    stop_list = []
    with open(stop_path, 'r') as stop_words:
        for entry in stop_words:
            stop_list.append(entry[:-1])
    return stop_list


stop_words_path = input('Please enter the full path to the stop words file:\n')
stop_words_list = stopwords(stop_words_path)

# alphabet will help eliminate unnecessary characters
alphabet = 'abcdefghijklmnopqrstuvwxyz'
# list used to build a token/word character by character
word = []
# dictionary to count frequency of tokens/words
word_list = {}
porter = PorterStemmer()


# TODO: do better about breaking this down into functions
def token_dictionary(corpus_folder):
    count = 0
    with os.scandir(corpus_folder) as filenames:
        for file in filenames:
            if file.is_file():
                with open(file, 'r') as f:
                    # then breaking each file down line by line
                    for line in f:
                        # then breaking each line down character by character
                        for character in line.lower():
                            # filtering out unnecessary characters
                            if character in alphabet:
                                # building token/word character by character
                                word.append(character)
                            else:
                                # completed token/word
                                current_word = ''.join(word)
                                count += 1
                                # clearing word list to create new word
                                word.clear()
                                # filters stopwords
                                if current_word not in stop_words_list:
                                    # stems the token
                                    current_word = porter.stem(current_word)
                                    if current_word not in word_list:
                                        # initializes a dictionary entry
                                        word_list[current_word] = 1
                                    else:
                                        # adds to the frequency of the dictionary entry
                                        word_list[current_word] += 1
                f.close()

    # sorts word_list by value as a list of tuples and types as a dictionary
    sorted_dictionary = dict(sorted(word_list.items(), key=operator.itemgetter(1),
                                    reverse=True))
    sorted_dictionary.pop('')
    return sorted_dictionary


# opening files in directory cranfieldDocs
corpus_directory = input('Please enter the full path to the corpus directory:\n')
word_dictionary = token_dictionary(corpus_directory)
