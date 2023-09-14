from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import csv
from utils import StatisticProcessControl

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

            # Create an instance of the SPC class with the CSV file path
            spc_instance = StatisticProcessControl(file_path)

            # Store the SPC instance in the session
            session['spc_instance'] = spc_instance
            session['spc_instance'] = spc_instance.to_dict()

            # Read the CSV file and extract the first 5 rows of the first column
            columns = spc_instance.print_columns()

            return redirect(url_for('dashboard', data=columns, spc_instance=spc_instance))

    return 'File upload failed'

@app.route('/dashboard')
def dashboard():
    data = request.args.getlist('data')
    spc_data = session.get('spc_instance')
    spc_instance = StatisticProcessControl.from_dict(spc_data)

    return render_template('dashboard.html', data=data, spc_instance=spc_instance)


@app.route('/process_selection', methods=['POST'])
def process_selection():
    selected_item = request.form.get('selected_item')

    # Redirect to the route for calculations with the selected item as a parameter
    return redirect(url_for('calculate', selected_item=selected_item))


@app.route('/calculate/<selected_item>')
def calculate(selected_item):
    # Retrieve the SPC instance passed from the previous route
    spc_data = session.get('spc_instance')
    spc_instance = StatisticProcessControl.from_dict(spc_data)

    # Perform the specific calculation based on the selected item
    result = spc_instance.normality_test() #selected_item

    # You can display the result or perform further actions here
    return f"Result for {selected_item}: {result}"


if __name__ == "__main__":
    app.run()
