from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import csv
from utils import StatisticProcessControl
import base64
import matplotlib.pyplot as plt

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

            # Read the header row of the CSV file
            with open(file_path, 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # Read the first row (header)

            session['file_path'] = file_path
            session['header'] = header

            # Create an instance of the SPC class with the CSV file path
            # spc_instance = StatisticProcessControl(file_path)
            #
            # # Store the SPC instance in the session
            # session['spc_instance'] = spc_instance
            # session['spc_instance'] = spc_instance.to_dict()

            # Read the CSV file and extract the first 5 rows of the first column
            # columns = spc_instance.print_columns()

            return redirect(url_for('dashboard', header=header))

    return 'File upload failed'


@app.route('/dashboard')
def dashboard():
    data = session.get('header', [])

    return render_template('dashboard.html', data=data)


@app.route('/process_selection', methods=['POST'])
def process_selection():
    selected_item = request.form.get('selected_item')
    data = session.get('header', [])

    # Redirect to the route for calculations with the selected item as a parameter
    return redirect(url_for('calculate', selected_item=selected_item, data=data))


# New route for computing
@app.route('/compute/<selected_item>')
def compute(selected_item):
    # Retrieve the file path passed from the previous route
    file_path = session.get('file_path')
    data = session.get('header', [])
    spc_instance = StatisticProcessControl(file_path, selected_item)

    # Perform the specific calculation based on the selected item
    result = spc_instance.normality_test()

    # Generate and save the graph
    graph = spc_instance.plot_graph()
    graph_file = 'static/graph.png'  # Choose a path to save the graph
    graph.savefig(graph_file)
    plt.close(graph)  # Close the figure to free up resources

    # Encode the graph as base64
    with open(graph_file, 'rb') as image_file:
        graph_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    return render_template('compute_result.html', result=result, data=data, graph_base64=graph_base64,selected_item=selected_item)

@app.route('/calculate/<selected_item>')
def calculate(selected_item):
    # Redirect to the new computation route
    return redirect(url_for('compute', selected_item=selected_item))

if __name__ == "__main__":
    app.run()
