from flask import Flask, jsonify
from sklearn.externals import joblib
import pandas as pd

app = Flask(__name__)

#Decode Labels from predicted output
def decode_predicted(value):
	if value == 0:
		return "Negativo"
	else:
		if value == 1:
			return "Positivo"
		else:
			return "Neutral"


@app.route('/', methods=['POST'])
def test():
	return jsonify({'respuesta':'hola mundo'})

@app.route('/predict/<text>', methods=['POST'])
def predict(text):
	clf = joblib.load('model.pkl')
	vectorizer = joblib.load('vectorizer.pkl')
	data = [text]
	new_data = vectorizer.transform((data))
	prediction = clf.predict(new_data)
	return jsonify({'sentiment': decode_predicted(prediction)})

if __name__ == '__main__':
     app.run(port=5000)

