from flask import Flask, render_template, request, redirect, url_for, flash
from utils import StatisticProcessControl

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    selected_column = None
    columns = []  # Initialize the columns variable

    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        # Check if it's a CSV file
        if not file.filename.endswith('.csv'):
            flash('File must be in CSV format', 'error')
            return redirect(request.url)

        # Process the CSV file
        spc = StatisticProcessControl(file)
        columns = spc.print_columns()

        if 'selected_column' in request.form:
            selected_column = request.form['selected_column']

    return render_template('upload.html', columns=columns, selected_column=selected_column)

if __name__ == '__main__':
    app.run(debug=True)
