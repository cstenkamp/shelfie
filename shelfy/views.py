# Imports
import os
import sys



import flask
from werkzeug.utils import secure_filename



SHELFY_BASE_PATH = os.path.dirname(__file__)
sys.path.append(SHELFY_BASE_PATH + '/models')
import book_functions, scraper, server, utility



# Define views
views = flask.Blueprint('views', __name__)



def format_file_path_for_routing(file_path):
    file_path = file_path.replace(SHELFY_BASE_PATH, '')
    return file_path

@views.route('/submission/<submission_id>/admin', methods=['GET'])
def submission_admin(submission_id):




    raw_img_file_path = format_file_path_for_routing(server.get_raw_image_path_from_submission_id(submission_id))
    proc_img_file_path = format_file_path_for_routing(server.get_processed_image_path_from_submission_id(submission_id))
    books = server.load_pickle_from_submission_id(submission_id)

    return flask.render_template('submission-admin.html', rawimgfilepath = raw_img_file_path, procimgfilepath = proc_img_file_path, books = books)#, tokens = tokens)


@views.route('/submission/<submission_id>/user', methods=['GET'])
def submission_user(submission_id):




    raw_img_file_path = format_file_path_for_routing(server.get_raw_image_path_from_submission_id(submission_id))
    proc_img_file_path = format_file_path_for_routing(server.get_processed_image_path_from_submission_id(submission_id))


    print('proc img file path!', proc_img_file_path)

    # Load books
    books = server.load_pickle_from_submission_id(submission_id)

    # Sort by x-position
    books = sorted(books, key = lambda book: book.center_x)


    return flask.render_template('submission-user.html', rawimgfilepath = raw_img_file_path, procimgfilepath = raw_img_file_path, books = books)





@views.route('/', methods=['GET', 'POST'])
def index():
    '''
    The index; a simple interface for allowing a user to submit an image
    to query
    methods:
        GET: The main page, has a 'submit image' button
        POST: After the submit/query/request button is hit, the file will be saved
        to the server and the user will be redirected to the uploads page
    '''




    # Get method type
    method = flask.request.method



    if method == 'GET':
        return flask.render_template('index.html')



    if method == 'POST':


        # No file found in the POST submission
        if 'file' not in flask.request.files:
            return flask.redirect(flask.request.url)



        # File was found
        file = flask.request.files['file']

        # No file name submitted
        if file.filename == '':
            return flask.redirect(request.url)

        # File was found, and is an allowable file type
        if file:

            # Create a new submission folder for the submission
            submission_id = server.create_new_submission(file)

            # Full pipeline
            raw_file_path = server.get_raw_image_path_from_submission_id(submission_id)
            books = utility.full_pipeline(raw_file_path)


            # Save the processed image
            proc_file_path = server.get_processed_image_path_from_submission_id(submission_id)
            book_functions.generate_processed_image(books, raw_file_path, save_path = proc_file_path)

            # Pickle and save the books
            server.pickle_save_books(books, submission_id)

            # Save json of book info
            server.save_book_info(books, submission_id)



            return flask.redirect('/submission/' + submission_id + '/user')
            #return flask.redirect('/submission/' + submission_id + '/admin')
