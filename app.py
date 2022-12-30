from flask import Flask, request
from flask import render_template
from static.scripts.genetique.Genetique.Dieu import *
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pages/index.html")


@app.route("/form")
def form():
    return render_template("pages/form.html")

@app.route("/dashboard", methods=("GET","POST"))
def dashboard():
    if request.method == "POST" :
        print(request.form["surface"])
    d = Dieu()
    return render_template("pages/dashboard/dashboard.html", surface=d.best_solution.attributs[1] * d.BD_pv.getPanneaux(d.best_solution.attributs[0]).surface)

@app.route("/dashboard/load_curve")
def load_curve():
    return render_template("pages/dashboard/load_curve.html")


def open_csv(path="static/data/courbe_puissance_charge_lycee_cassin.csv") :
    dates = []
    conso = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        reader = list(reader)
        for i in range(len(reader)):
            dates.append(reader[i][0])
            conso.append(reader[i][1])
    # Enlever les entêtes
    dates.pop(0)
    conso.pop(0)
    return dates, conso

def calc_create_monotone(path="static/data/courbe_puissance_charge_lycee_cassin.csv") :
    conso = {}
    nb_tot = 0

    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for col in reader :
            puissance_key = int(col[" IDC 12102954 | Consommation | EA"])

            if puissance_key in conso.keys() :
                conso[puissance_key] = conso[puissance_key]+1
                nb_tot += 1
            else :
                conso[puissance_key] = 1
                nb_tot += 1

    cons = []
    effec = []
    freq = []
    freq_cumul = []
    for i in range(max(conso.keys())+1) :
        if i in conso.keys() :
            cons.append(i)
            effec.append(conso[i])

    for i in range(len(effec)) :
        freq.append(effec[i]/nb_tot)
        if i > 0 :
            freq_cumul.append((freq_cumul[i-1]+freq[i]))
        else :
            freq_cumul.append(freq[i])
    
    for i in range(len(freq_cumul)):
        freq_cumul[i] = round(freq_cumul[i]*100,2)
    
    cons.reverse()
    freq_cumul.reverse()

    with open("static/data/monotone_puissance_lycee_cassin.csv", "w", newline='') as file :
        writer = csv.writer(file)
        for i in range(len(cons)) :
            writer.writerow([freq_cumul[i],cons[i]])


if __name__ == "__main__" :
    app.run(debug=True, host='0.0.0.0', port=5000)



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_world(name=None):
    #return f"<p>Hello {escape(name)}</p>"
    return render_template("test_pages/hello.html",name=name)