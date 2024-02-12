from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

classification_results = {}

with open('Flask/Recognition/classification_results.csv', mode = 'r') as csv_file:
    reader = csv.reader(csv_file)
    classification_results = {rows[0]: rows[1] for rows in reader}

@app.route('/', methods=['POST'])
def classify_image():
    if 'inputFile' not in request.files:
        return "No file provided", 400
    file = request.files['inputFile']
    filename = file.filename

    prediction_result = classification_results.get(filename.split('.')[0], 'Unknown')

    return f"{filename}:{prediction_result}", 200

if __name__ == '__main__':
    app.run(debug=True, threaded = True)