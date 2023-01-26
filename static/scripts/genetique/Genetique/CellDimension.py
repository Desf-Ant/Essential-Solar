
class CellDimension :
    
    def __init__(self, panneau, consommation, coeff_region=1):
        self.x = [i for i in range(0,145)]
        self.efficacite_panneau = []
        self.panneau = panneau
        self.coeff_region = coeff_region
        self.consommation = consommation
        self.capacite_batterie = 200_000
        self.charge_batterie = self.capacite_batterie
        
        self.run()
        self.optimize()
        
    def getCapacite(self) -> float :
        return self.capacite_batterie
        
    def run (self) :
        self.efficacite_panneau = self.create_efficacite_panneau(self.x, self.efficacite_panneau)

    def eff_phase_1(self,x) :
        return (5.55*x - 266.6)/100

    def eff_phase_2(self,x) :
        return 1

    def eff_phase_3(self,x) :
        return (-5.55 * x + 533.3)/100

    def create_efficacite_panneau (self,x,y) :
        for i in x :
            # 00h (00) - 08h (48) _
            if i < 48 : y.append(0)
            # 08h (48) - 11h (66) /
            elif i >= 48 and i < 66 : y.append(self.eff_phase_1(x[i]))
            # 11h (66) - 13h (78) -
            elif i >= 66 and i < 78 : y.append(self.eff_phase_2(x[i]))
            # 13h (78) - 16h (96) \
            elif i >= 78 and i < 96 : y.append(self.eff_phase_3(x[i]))
            # 16h (96) - 24h (144) _
            else : y.append(0)
            
        return y
    
    def optimize(self) :
        puissance_max = int(self.panneau.gamme_puissance.split(" ")[0])
        for el in self.consommation :
            horaire = el[0].split(" ")[1].split(":")
            heure_10 = int(int(horaire[0])*6 + int(horaire[1])/10)
            production = self.coeff_region * self.efficacite_panneau[heure_10] * puissance_max
            conso = int(el[1])
            self.charge_batterie += production
            
            # Consommation hors creuse
            if int(horaire[0]) < 8 or int(horaire[0]) >= 20 :    
                self.charge_batterie -= conso
                
            # Si Batterie pleine 
            if self.charge_batterie > self.capacite_batterie :
                self.charge_batterie = self.capacite_batterie
        
        if self.charge_batterie >= 0.75 * self.capacite_batterie :
            self.capacite_batterie *= 1.25
        elif self.charge_batterie < 0.33 * self.capacite_batterie :
            self.capacite_batterie *= 0.75