from random import randint
from static.scripts.genetique.Genetique.BasesDonnees.BD_PV import *

class Solution: 

    ## 1er attribut  ->  type de PV
    ## 2nd attribut  ->  nb de PV
    ## 3eme attribut ->  onduleur

    max_attribut_borne = [BD_PV.nb_panneaux-1, 7_500, ]
    odd_to_mutate = [0.2, 0.75]
    nb_attribut = len(max_attribut_borne)

    def __init__(self) :
        self.attributs = []
        score = -1000

        for i in range (Solution.nb_attribut) :
            mini = 1 if i == 1 else 0
            self.attributs.append(randint(mini,Solution.max_attribut_borne[i]))

    def setAttributs(self, lst_attributs:list) :
        self.attributs = lst_attributs
    
    def getPrice(self,bd:BD_PV) -> int:
        prix = bd.getPanneaux(self.attributs[0]).prix 
        if prix == "--" : return 999_999
        return prix * self.attributs[1]

    def getPuissanceTotale(self,bd:BD_PV) -> float:
        puissance = bd.getPanneaux(self.attributs[0]).gamme_puissance.split(" ")[0]
        if puissance == "--" : return 1
        return float(puissance) * self.attributs[1]
    
    def getSurfaceTotale(self, bd:BD_PV) -> float:
        surface = bd.getPanneaux(self.attributs[0]).surface 
        if surface == "--" : return 999_999_999_999
        return round(surface,2) * self.attributs[1]