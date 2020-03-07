"""
Author:
    * Jeremiah D 'JD' Smith

Description:
    * Takes in corpus texts and breaks them down to tokens/words
    * Then counts the frequency of the tokens/words
    * Takes in a query and breaks it down to tokens/words
    * Calculate the idf of a query token
    * Calculate the tf-idf
"""
import math
import operator
import os
from nltk.stem import PorterStemmer  # imported because I can't use java based Porter stemmer


# convert stopwords text to list
def stopwords(stop_path):
    # create list of stopwords
    stop_list = []
    with open(stop_path, 'r') as stop_words:
        for entry in stop_words:
            stop_list.append(entry[:-1])
    stop_words.close()
    return stop_list


stop_words_path = input('Please enter the path to the stop words file:\n'
                        'Press Enter to default to stopwords.txt.\n')
# defaulting to stopwords.txt in project directory
if stop_words_path == '':
    stop_words_path = 'stopwords.txt'
    print(stop_words_path)
stop_words_list = stopwords(stop_words_path)

# porter word stemmer
porter = PorterStemmer()
# alphabet will help eliminate unnecessary characters
alphabet = 'abcdefghijklmnopqrstuvwxyz'


# iterates through a directory and counts files
def doc_count(directory):
    document_count = 0
    for path in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, path)):
            document_count += 1
    return document_count


file_directory = input('Please enter the full path to the corpus directory:\n'
                       'Hit Enter to default to the cranfield directory\n')
# defaulting to the cranfield directory
if file_directory == '':
    file_directory = 'cranfieldDocs'
    print(file_directory)

file_count = doc_count(file_directory)


# TODO: do better about breaking this down into multiple functions
def term_frequency_dictionary(corpus_file):
    # list used to build a token/word character by character
    word_builder = []
    # dictionary to count frequency of tokens/words
    word_dictionary = {}
    total_word_count = 0
    with open(corpus_file, 'r') as file:
        # then breaking each file down line by line
        for line in file:
            # then breaking each line down character by character
            for character in line.lower():
                # filtering out unnecessary characters
                if character in alphabet:
                    # building token/word character by character
                    word_builder.append(character)
                else:
                    # completed token/word
                    current_word = ''.join(word_builder)
                    # clearing word list to create new word
                    word_builder.clear()
                    # filters stopwords
                    if current_word not in stop_words_list:
                        # stems the token
                        current_word = porter.stem(current_word)
                        if current_word not in word_dictionary:
                            # initializes a dictionary entry
                            word_dictionary[current_word] = 1
                        else:
                            # adds to the frequency of the dictionary entry
                            word_dictionary[current_word] += 1
    file.close()

    word_dictionary.pop('')

    for value in word_dictionary.values():
        total_word_count += value

    for word_dictionary_key, word_dictionary_value in word_dictionary.items():
        word_dictionary[word_dictionary_key] = word_dictionary_value / total_word_count

    return dict(sorted(word_dictionary.items(), key=operator.itemgetter(1), reverse=True))


# TODO: do better about breaking this down into multiple functions
def single_query(question):
    query_word_list = []
    word_builder = []
    for character in question.lower():
        if character in alphabet:
            word_builder.append(character)
        else:
            current_word = ''.join(word_builder)
            # clearing word list to create new word
            word_builder.clear()
            if current_word not in stop_words_list:
                stemmed_word = porter.stem(current_word)
                if stemmed_word not in query_word_list:
                    query_word_list.append(stemmed_word)
    query_word_list.remove('')
    return query_word_list


query_file = input('Please enter the full path to the query file:\n'
                   'Hit Enter to default to queries\n')
# defaulting to the queries file in the project directory
if query_file == '':
    query_file = 'queries'
    print(query_file)


# TODO: fix the idf each query term should have it's own idf
# TODO: multiply the idf of each query term to the term frequency of each term in each document
def main():
    for filename in os.listdir(file_directory):
        with open(f'{file_directory}/{filename}', 'r'):
            word_frequency_dictionary = term_frequency_dictionary(f'{file_directory}/{filename}')
            with open(query_file, 'r') as question_file:
                for query in question_file:
                    query_document_count = 0
                    query_idf_dictionary = {}
                    query_entry = single_query(query)
                    for entry in query_entry:
                        if entry in word_frequency_dictionary.keys():
                            query_document_count += 1
                    if query_document_count != 0:
                        idf = math.log(file_count / query_document_count)
                        for entry in query_entry:
                            query_idf_dictionary[entry] = idf
    print("I'm sorry the program doesn't work the way it needs to. The problem is I \n"
          "calculate the idf for a single search term, but that idf gets applied to all of \n"
          "the search terms in a query term dictionary (that holds the query term and the \n"
          "idf for that term) I'm not sure how to fix it. Maybe if I was on a development \n"
          "team (not a class project team where I don't have a conducive schedule to meet \n"
          "with other people) I could consult with someone but I'm not and this is two \n"
          "days late despite my best efforts. Maybe if we weren't made to re-invent the \n"
          "wheel to prove I understand the concept I'd have done better. \n")


if __name__ == '__main__':
    main()
