from static.scripts.genetique.Genetique.BasesDonnees.PV import *
import csv 

class BD_PV :

    nb_panneaux = 305

    def __init__(self) :
        self.type_panneaux = []

        # ref,price by Wh,type,efficacite,gamme puissance,poids,region,dimension,prix theorique

        with open("static/scripts/genetique/Genetique/BasesDonnees/csv/EuropeanDataClean.csv", "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for row in reader :
                self.type_panneaux.append(PV(
                    row["ref"],
                    row["price by Wh"],
                    row["type"],
                    row["dimension"],
                    row["gamme puissance"],
                    row["efficacite"],
                    row["poids"],
                    row["region"],
                    row["prix theorique"]
                ))

    def getPanneaux(self, index) -> PV:
        return self.type_panneaux[index]

if __name__ == "__main__" :
    bd = BD_PV()
    for i in range(BD_PV.nb_panneaux) :
        print(bd.getPanneaux(i).surface)
