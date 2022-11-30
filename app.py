from flask import Flask
from flask import render_template
import json
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pages/index.html")


@app.route("/form")
def form():
    return render_template("pages/form.html")

@app.route("/dashboard")
def dashboard():
    dates, conso = open_csv()
    return render_template("pages/dashboard.html", dates=json.dumps(dates), conso=json.dumps(conso))


def open_csv(path="static/data/courbe_puissance_charge_lycee_cassin.csv") :
    dates = []
    conso = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        reader = list(reader)
        for i in range(len(reader)):
            dates.append(reader[i][0])
            conso.append(reader[i][1])
    dates.pop(0)
    conso.pop(0)
    return dates, conso


if __name__ == "__main__" :
    app.run(debug=True, host='0.0.0.0', port=5000)



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_world(name=None):
    #return f"<p>Hello {escape(name)}</p>"
    return render_template("test_pages/hello.html",name=name)