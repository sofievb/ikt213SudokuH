import imghdr
import os
import cv2
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
from main import main

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg','.png','.jpeg']
app.config['UPLOAD_PATH'] = 'upload'
def validate_image(stream):
    #first 512 bytes to check filetype
    header = stream.read(512)
    stream.seek(0)
    #the detected image format
    format = imghdr.what(None, header)
    if not format:
        return None
    return  '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    processed_files = os.listdir('solutions')
    return render_template('webapp.html', files=files, processed_files=processed_files)

'''@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204'''
@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(filepath)

        #process uploaded file from main and view image
        processed_img_path = main(filepath)  # Use the main function from main.py
        if processed_img_path:
            processed_filename = os.path.basename(processed_img_path)
            files = os.listdir(app.config['UPLOAD_PATH'])
            processed_files = os.listdir('solutions')
            return render_template('webapp.html', files=files, processed_files=processed_files,
                                   uploaded_file=filename,processed_file=processed_filename)
            #return redirect(url_for('processed_image', filename=processed_filename))
        else:
            return "Error processing image", 500
    return '', 204

@app.route('/upload/<filename>')
def upload(filename):
    files = send_from_directory(app.config['UPLOAD_PATH'], filename)
    return files
def run_solution(filepath):
    # Read the image using OpenCV
    img = cv2.imread(filepath)
    # Process the image with the main function from main.py
    solution_file_path = main(img)
    # Return the path to the processed image
    return solution_file_path

@app.route('/processed_image/<filename>')
def processed_image(filename):
    return send_from_directory('solutions', filename)

if __name__ == '__main__':
    app.run(debug=True, port=8001)