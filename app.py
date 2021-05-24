import csv

from flask import *
from flask import render_template
import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri
import pandas as pd
from rpy2.robjects import pandas2ri

#rpy2.objects for importing the models
pandas2ri.activate()
r = robjects.r
numpy2ri.activate()
pred = ''

app = Flask(__name__)


class Model(object):

    def _init_(self):
        self.model = None

    #function to load the RF Algorith model saved as '.rds' file from R programming Language
    def loadRfModel(self, path, dep_path):
        model_rf_path = "{}.rds".format(path)
        model_dep_path = "{}.dep".format(dep_path)
        self.model = r.readRDS(model_rf_path)
        return self

    #function to load the D-Tree Algorith model saved as '.rds' file from R programming Language
    def load(self, path, dep_path):
        model_rds_path = "{}.rds".format(path)
        model_dep_path = "{}.dep".format(dep_path)
        self.model = r.readRDS(model_rds_path)
        return self

    #Function to use the predict function in D-Tree model
    def predict(self, csvobj):
        data = csvobj
        arr = data.to_numpy()
        print(arr)
        with open('Rough.csv', newline='') as f:
            csv_reader = csv.reader(f)
            csv_headings = next(csv_reader)
            first_line = next(csv_reader)
        if self.model is None:
            raise Exception("There is no Model")
        pred = r.predict(self.model, newdata=data, type="raw")
        return pred

    # Function to use the predict function in Random Forest model
    def predictrf(self, csvobj):
        data = csvobj
        if self.model is None:
            raise Exception("There is no Model")
        pred = r.predict(self.model, newdata=data)
        return pred

#Routing to the Random Forest upload page
@app.route('/dtree')
def upload():
    return render_template("file_upload.html")

#Routing to the Random Forest upload page
@app.route('/rfupload')
def upload_rf():
    return render_template("file_upload_rf.html")

#Routing to the Home Page
@app.route('/')
def home():
    return render_template("home.html")

#To Download the Templates
@app.route('/download')
def download_file():
    path = "template.csv"
    return send_file(path, as_attachment=True)


#Getting predicted results for the D-Tree Algorith
@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        f.save("Rough.csv")
        MODEL_PATH = "/Users/loshigamohan/PycharmProjects/flaskProject/dtree_fit"
        DEP_PATH = "/Users/loshigamohan/PycharmProjects/flaskProject/losProject"
        #Loading D-Tree model
        model = Model().load(MODEL_PATH, DEP_PATH)
        data = pd.read_csv("Rough.csv", nrows=1)
        pred = model.predict(data)
        return render_template("success.html", name=pred)

#Getting predicted results for the Random Forest Algorith
@app.route('/success_rf', methods = ['POST'])
def success_rf():
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        f.save("Rough.csv")
        MODEL_PATH = "/Users/loshigamohan/PycharmProjects/flaskProject/ran_for"
        DEP_PATH = "/Users/loshigamohan/PycharmProjects/flaskProject/losProject"
        #Loading the RF model
        model = Model().loadRfModel(MODEL_PATH, DEP_PATH)
        data = pd.read_csv("Rough.csv", nrows=1)
        pred = model.predictrf(data)
        return render_template("successRF.html", name=pred)


if __name__ == '_main_':
    app.run(debug=True)