from Onduleur import *

class BD_Onduleur :

    nb_onduleur = 5
    
    def __init__(self) :
        self.type_onduleur = []

        for _ in range(BD_Onduleur.nb_onduleur) :
            self.type_onduleur.append(Onduleur())