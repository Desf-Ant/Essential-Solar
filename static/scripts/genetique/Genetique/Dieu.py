from static.scripts.genetique.Genetique.BasesDonnees.BD_PV import *
from static.scripts.genetique.Genetique.Solution import Solution
from random import randint, random

class Dieu :

    def __init__ (self, consommation_max=300_000, surface_disponible=1000) :
        self.liste_solutions = []
        self.liste_next_generation = []
        self.nb_solutions = 10
        self.score_min = 5_000_000
        self.best_solution = None
        self.current_generation = 0
        self.generation_max = 1000

        self.consommation_max = consommation_max
        self.surface_disponible = surface_disponible

        self.BD_pv = BD_PV()

        self.run()

    def run(self) : 
        self.initialize()
        index_score, score = self.anotherGeneration()
        while True:
            self.current_generation += 1
            self.calcul_score()
            self.selectionAndCroisement()
            self.mutation()
            self.goToNextGeneration()

            index_score, score = self.anotherGeneration()

            if self.current_generation > self.generation_max : break
            print(self.current_generation)

        self.best_solution = self.liste_solutions[index_score]


    def initialize(self):
        for _ in range(self.nb_solutions) :
            self.liste_solutions.append( Solution() )

    def calcul_score (self) :
        for sol in self.liste_solutions :
            fit = self.fitness_function(sol)
            pen = self.penality_function(sol)
            sol.score = fit + pen
            # print("fit", fit, "pen", pen, "total", fit-pen, "score", sol.score)
        
        #Trier la liste des toutes les solutions dans l'ordre des meilleures (ici meilleur score est le plus bas)
        self.liste_solutions.sort(key= lambda sol: sol.score, reverse=False)

    def fitness_function (self, solution:Solution) :
        somme = solution.getPrice(self.BD_pv) / solution.getPuissanceTotale(self.BD_pv)
        return somme 
    
    def penality_function(self, solution:Solution) -> int:
        penality = 0
        if solution.getPuissanceTotale(self.BD_pv) < self.consommation_max :
            penality += 10_000
        if solution.getSurfaceTotale(self.BD_pv) > self.surface_disponible : 
            penality += (100_000_000 * solution.getSurfaceTotale(self.BD_pv)- self.surface_disponible)
        return penality

    def selectionAndCroisement(self) :
        for i in range(int(self.nb_solutions/2)):
            indexS1, indexS2 = self.selection()
            self.croisement(indexS1, indexS2)
            
        if len(self.liste_next_generation) != self.nb_solutions :
            print("Moins de solution dans la nouvelle génération")
        


    def selection(self) -> int:
        #selectionner parmi les meilleurs (minimum fenetre 5%)
        borne_superieure = max(int((1-self.current_generation/self.generation_max)*self.nb_solutions), int(self.nb_solutions*0.05))
        s1, s2 = randint(0,borne_superieure), randint(0,borne_superieure)
        return s1, s2
    
    def croisement(self,indexS1:int, indexS2:int) :
        pivot = randint(0, Solution.nb_attribut-1)
        attributs_1 = self.liste_solutions[indexS1].attributs[:pivot] + self.liste_solutions[indexS2].attributs[pivot:]
        attributs_2 = self.liste_solutions[indexS2].attributs[:pivot] + self.liste_solutions[indexS1].attributs[pivot:]

        new_sol_1 = Solution()
        new_sol_2 = Solution()
        new_sol_1.setAttributs(attributs_1)
        new_sol_2.setAttributs(attributs_2)

        self.liste_next_generation.append(new_sol_1)
        self.liste_next_generation.append(new_sol_2)
    
    def mutation(self) :
        for i in range(len(self.liste_next_generation)) :
            for j in range(len(self.liste_next_generation[i].attributs)) :
                if random() <= Solution.odd_to_mutate[j] :
                    # S'il s'agit de l'attribut nombre de panneaux, changer la fenetre de randint
                    if j == 1 :
                        milieu = self.liste_next_generation[i].attributs[j]
                        amplitude = max(int((1 - self.current_generation / self.generation_max)*1000), int(100*0.1))
                        borne_inf = max(1,milieu-amplitude)
                        borne_sup = min(Solution.max_attribut_borne[j], milieu+amplitude)
                        self.liste_next_generation[i].attributs[j] = randint(borne_inf,borne_sup)
                    else :
                        self.liste_next_generation[i].attributs[j] = randint(0,Solution.max_attribut_borne[j])
                    
    
    def goToNextGeneration(self):
        self.liste_solutions = list(self.liste_next_generation)
        self.liste_next_generation = []

    def anotherGeneration(self) -> int:
        scores = []
        for sol in self.liste_solutions: 
            fit = self.fitness_function(sol)
            pen = self.penality_function(sol)
            scores.append(fit-pen)
        return scores.index(max(scores)), max(scores)

  
if __name__ == "__main__" :
    d = Dieu()
    print("La meilleure solution est", d.best_solution.attributs)
    print("\n",d.BD_pv.getPanneaux(d.best_solution.attributs[0]))
    print("\n\nprix panneaux:", d.best_solution.attributs[1] * d.BD_pv.getPanneaux(d.best_solution.attributs[0]).prix)
    print( "surface prise:",d.best_solution.attributs[1] * d.BD_pv.getPanneaux(d.best_solution.attributs[0]).surface)
    print( "puissance atteinte:",d.best_solution.attributs[1] * float(d.BD_pv.getPanneaux(d.best_solution.attributs[0]).gamme_puissance.split(" ")[0]))
    