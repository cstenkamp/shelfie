# Python standard library
import io
import os
import pickle
import sys

# Scipy
import numpy as np
import matplotlib.pyplot as plt

# Shelfy
import shelfy
from shelfy.models import book_functions

# Google cloud visionfrom google.cloud import vision
from google.cloud import vision
from google.cloud.vision import types





def generate_unique_id_incremental():
    '''
    Generates a key for a submission
    Submissions are 9 digit numbers that incrementally increase
    '''

    # Get all folder names
    submissions_path = shelfy.SHELFY_BASE_PATH + '/static/submissions'
    submission_ids = os.listdir(submissions_path)

    # If no submissions, initialize with first submission value
    if submission_ids == []:
        return '000000000'

    # Submissions exist; find the latest submission and increment
    submission_ids = [int(submission_id) for submission_id in submission_ids]
    submission_ids.sort()
    last_submission_id = submission_ids[-1]
    new_submission_id = str(last_submission_id + 1).zfill(9)

    return new_submission_id



def create_new_submission(file):
    '''
    Saves a new submission to the server;
    Generates the correct folder and subfolders for the submission,
    and saves the file to the folder.
    Returns the id of the new submission
    '''

    # Get a unique ID for the submission
    id = generate_unique_id_incremental()


    # Create the main and sub folders for the submission
    directory = shelfy.SHELFY_BASE_PATH + '/static/submissions/' + id

    os.makedirs(directory)
    os.makedirs(directory + '/raw_img')
    os.makedirs(directory + '/annotated_imgs')
    os.makedirs(directory + '/books')
    os.makedirs(directory + '/info')

    # Save the image to the newly created folder
    file_name = file.filename
    file_extension = file_name.split('.')[-1]
    file.save(directory + '/raw_img/raw_img' + '.' + file_extension)



    return id


def get_raw_image_path_from_submission_id(submission_id):
    '''
    Returns the full file path to the raw_img associated iwth submission_id
    '''

    # Get the directory of the raw_file file for the submission_id
    file_directory = shelfy.SHELFY_BASE_PATH + '/static/submissions/' + submission_id + '/raw_img'


    # get file path
    file_name = [file_name for file_name in os.listdir(file_directory) \
     if os.path.isfile(os.path.join(file_directory, file_name))][0]




    file_path = file_directory + '/' + file_name


    return file_path



def get_pickle_directory_from_submission_id(submission_id):
    '''
    Returns the correct path to the pickle directory for submission_id
    '''



    # Get the directory of the raw_file file for the submission_id
    pickle_directory = shelfy.SHELFY_BASE_PATH + '/static/submissions/' + submission_id + '/books'


    return pickle_directory

def get_info_directory_from_submission_id(submission_id):
    '''
    Returns the correct path to the info directory for submission_id
    '''

    info_directory = shelfy.SHELFY_BASE_PATH + '/static/submissions/' + submission_id + '/info'


def pickle_save_books(books, submission_id):
    '''
    Pickles book objects and saves them to the correct submission folder
    '''


    # Get the directory to which to save the book
    pickle_directory = get_pickle_directory_from_submission_id(submission_id)

    # Pickle and save the books to the correct directory

    sys.setrecursionlimit(5000)    # Necessary to pickle objects

    for i, book in enumerate(books):
        print(book)
        print([word.string for word in book.spine.words])

        with open(pickle_directory + '/' + str(i), 'wb') as file_handle:
            pickle.dump(book, file_handle)



def save_book_info(books, submission_id):
    '''
    Saves the found book information in a json format to allow fellow humans
    to parse easily
    '''

    # Get the directory to which to save the book information
    info_directory = get_info_directory_from_submission_id(submission_id)


    # Dump the info to a json file
    with open(info_directory + '/info.json', 'wb') as file_handle:
        json.dump([book.book_info for book in books], file_handle)
