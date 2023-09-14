from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import csv

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = 'upload_folder'
app.secret_key = 'your_secret_key'  # Change this to a secret key for security.


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('upload_form.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file
            file.save(file_path)
            flash('File uploaded successfully')

            # Read the CSV file and extract the first 5 rows of the first column
            first_column_data = []
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for i, row in enumerate(csv_reader):
                    if i >= 5:
                        break
                    if row:
                        first_column_data.append(row[0])

            return redirect(url_for('dashboard', data=first_column_data))

    return 'File upload failed'

@app.route('/dashboard')
def dashboard():
    data = request.args.get('data')
    return render_template('dashboard.html', data=data)


if __name__ == "__main__":
    app.run()
