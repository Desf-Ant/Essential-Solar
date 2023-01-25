from flask import Flask, request, session
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
    if request.method == "POST" or not "dieu" in session:
        # Récupération de la courbe de charge avec le point de récupération request.form["access_point"] sur l'API Enedis
        
        # Creation de la courbe de charge simplifié
        create_load_simple()
        
        # Création de la monotonne de puissance depuis la courbe de charge
        calc_create_monotone()
        
        
        
        # Algorithme évolutionniste pour la meilleure réponse
        dieu = Dieu(consommation_max=380_000,surface_disponible=int(request.form["surface"]))
        session["dieu"] = dieu.toJson() # On save le résultat dans une variable de session
        
        # Creation des deux semaines types
        semaine_type()
        
    return render_template("pages/dashboard/dashboard.html")

@app.route("/details")
def details():
    return render_template("pages/dashboard/details.html")

@app.route("/maintenance")
def maintenance():
    return render_template("pages/dashboard/maintenance.html")

@app.route("/roi")
def roi() :
    return render_template("pages/dashboard/roi.html")


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
        freq_cumul[i] = round(freq_cumul[i]*8760,2)

    
    
    cons.reverse()

    with open("static/data/monotone_puissance_lycee_cassin.csv", "w", newline='') as file :
        writer = csv.writer(file)
        for i in range(len(cons)) :
            writer.writerow([freq_cumul[i],cons[i]])

def create_load_simple(path="static/data/courbe_puissance_charge_lycee_cassin.csv") :
    conso = {}
    nb = 0
    with open(path, mode='r') as file :
        reader =csv.reader(file)
        reader = list(reader)
        for i in range(1,len(reader)) :
            date = reader[i][0].split(" ")[0].split("/")

            # on regarde si le mois existe dans les conso
            if not date[1] in conso :
                conso[date[1]] = { date[0] : int(reader[i][1]) }
            # si le mois existe, on regarde si le jour existe
            else :
                if not date[0] in conso[date[1]] :
                    conso[date[1]][date[0]] = int(reader[i][1])
                    nb = 1
                else :
                    conso[date[1]][date[0]] += int(reader[i][1])
                    nb +=1

    for key in conso.keys() :
        for k in conso[key].keys():
            conso[key][k] /= nb

    x = []
    y = []
    for key in conso.keys() :
        for k in conso[key].keys():
            x.append('{}/{}'.format(key,k))
            y.append(round(conso[key][k],2))

    with open("static/data/simplified_"+path.split("static/data/")[1], mode="w", newline="") as file :
        writer = csv.writer(file)
        for i in range(len(x)) :
            writer.writerow([x[i],y[i]])

def semaine_type (path="static/data/courbe_puissance_charge_lycee_cassin.csv") :

    conso_h = {}
    conso_e = {}
    with open(path, "r") as file : 
        reader = csv.reader(file)
        reader = list(reader)
        for i in range(1,len(reader)) :
            #01/01/2022 01:10:00
            date = reader[i][0].split(" ")[0].split("/")
            horaire = reader[i][0].split(" ")[1].split(":")
            
            # On reagrde si on est dans les mois d'hiver
            if int(date[1]) <= 3 :
                if not i % 7 in conso_h : 
                    conso_h[i % 7] = {horaire[0] : float(reader[i][1]), "nb_"+horaire[0]:1}
                else : 
                    if not horaire[0] in conso_h[i % 7] :
                        conso_h[i % 7][horaire[0]] = float(reader[i][1])
                        conso_h[i % 7]["nb_"+horaire[0]] = 1
                    else : 
                        conso_h[i % 7][horaire[0]] += float(reader[i][1])
                        conso_h[i % 7]["nb_"+horaire[0]] += 1
                        
            
            # On regarde si on est dans les mois d'été
            elif  int(date[1]) == 7 or int(date[1]) == 8 : 
                if not i % 7 in conso_e : 
                    conso_e[i % 7] = {horaire[0] : float(reader[i][1]), "nb_"+horaire[0]:1}
                else : 
                    if not horaire[0] in conso_e[i % 7] :
                        conso_e[i % 7][horaire[0]] = float(reader[i][1])
                        conso_e[i % 7]["nb_"+horaire[0]] = 1
                    else : 
                        conso_e[i % 7][horaire[0]] += float(reader[i][1])
                        conso_e[i % 7]["nb_"+horaire[0]] += 1

    consommation_h = []
    consommation_e = []
    for key in conso_h.keys() : 
        for k in conso_h[key].keys() :
            if not "nb_" in k :
                consommation_h.append( conso_h[key][k] /  conso_h[key]["nb_"+k])
            
    for k in conso_e.keys() : 
        for k in conso_e[key].keys() :
            if not "nb_" in k :
                consommation_e.append( conso_e[key][k] /  conso_e[key]["nb_"+k])

    with open("static/data/conso_semaine_hiver.csv", "w", newline='') as file :
        writer = csv.writer(file)
        for i in range(len(consommation_h)) :
            #i/24 if i % 24 == 0 else ""
            writer.writerow([ i%24,consommation_h[i]])
            
    with open("static/data/conso_semaine_ete.csv", "w", newline='') as file :
        writer = csv.writer(file)
        for i in range(len(consommation_e)) :
            writer.writerow([i%24,consommation_e[i]])

if __name__ == "__main__" :
    app.secret_key = "the secret key"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host='0.0.0.0', port=5000)



@app.route("/hello/")
@app.route("/hello/<name>")
def hello_world(name=None):
    #return f"<p>Hello {escape(name)}</p>"
    return render_template("test_pages/hello.html",name=name)