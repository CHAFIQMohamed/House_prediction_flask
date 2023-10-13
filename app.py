"""from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def student():
    return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
    return render_template("result.html",result = result)
if __name__ == '__main__':
    app.run(debug = True)"
from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the model
model = pickle.load(open('models/model.pkl', 'rb'))  # Replace 'model.pkl' with your actual model file

# Sample data for label encoding
train = {
    'mainroad': ['yes', 'yes', 'yes', 'yes', 'yes'],
    'guestroom': ['no', 'no', 'no', 'no', 'yes'],
    'basement': ['no', 'no', 'yes', 'yes', 'yes'],
    'hotwaterheating': ['no', 'no', 'no', 'no', 'no'],
    'airconditioning': ['yes', 'yes', 'no', 'yes', 'yes'],
    'prefarea': ['yes', 'no', 'yes', 'yes', 'no'],
    'furnishingstatus': ['furnished', 'furnished', 'semi-furnished', 'furnished', 'furnished']
}

# Label encoding
le = LabelEncoder()
cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in cols:
    train[col] = le.fit_transform(train[col])

@app.route('/')
def index():
    return render_template('house.html')

@app.route('/submit-property', methods=['POST'])
def submit_property():
    features = [float(x) if i < 2 else x for i, x in enumerate(request.form.values())]
    features[5:] = [1 if val.lower() == 'yes' else 0 for val in features[5:]]
    features = np.array(features).reshape(1, -1)

    # Label encoding for categorical features
    for i in range(5, len(features[0])):
        features[0][i] = le.transform([request.form.getlist(list(request.form.keys())[i])])[0]

    predicted_price = model.predict(features)

    return render_template('result.html', predicted_price=predicted_price[0])

if __name__ == '__main__':
    app.run(debug=True)
"""
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
model = pickle.load(open('models/model.pkl', 'rb'))  # Replace 'model.pkl' with your actual model file

@app.route('/')
def index():
    return render_template('house.html')

@app.route('/submit-property', methods=['POST'])
def submit_property():
    features = [float(x) if i < 4 else int(x) for i, x in enumerate(request.form.values())]
    features = np.array(features).reshape(1, -1)

    # Sample data about the house
    house_info = {
        'area': features[0][0],
        'bedrooms': features[0][1],
        'bathrooms': features[0][2],
        'stories': features[0][3],
        'mainroad': features[0][4],
        'guestroom': features[0][5],
        'basement': features[0][6],
        'hotwaterheating': features[0][7],
        'airconditioning': features[0][8],
        'parking': features[0][9],
        'prefarea': features[0][10],
        'furnishingstatus': features[0][11]
    }

    predicted_price = model.predict(features)

    return render_template('result.html', predicted_price=predicted_price[0], house_info=house_info)

if __name__ == '__main__':
    app.run(debug=True)

