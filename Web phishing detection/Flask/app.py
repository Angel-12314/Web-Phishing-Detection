import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
from markupsafe import escape
import pickle
import gzip
import inputScript   

app = Flask(__name__)
with open('phishing_website.pkl','rb') as f:
    model=pickle.load(f)

@app.route('/')
def predict1():
    return render_template("index.html")
@app.route('/predict')
def predict():
    return render_template('final.html')

@app.route('/y_predict',methods=["POST"])
def y_predict():
    url = request.form['url']
    check_predic = inputScript.main(url)
    predic = model.predict(check_predic)
    
    if(predic==-1):
        pred = "You are safe!! This is a Legimate Website :)"
    elif(predic==1):
        pred = "You are in a phishing site. Dont Trust :("
    else:
        pred = "You are in a suspecious site. Be Cautious ;("

    return render_template("final.html", pred_text = '{}'.format(pred), url = url)

#  takes ip parameters from URL by inputScript and returns the predictions
@app.route('/predict_api', methods = ['POST'])
def predict_api():

    data = request.get_json(force = True)
    predic = model.y_predict([np.array(list(data.values()))])
    result = predic[0]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)