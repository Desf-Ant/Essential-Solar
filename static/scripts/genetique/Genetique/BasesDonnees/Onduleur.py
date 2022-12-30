
class Onduleur :

    id = 0

    def __init__(self, name, prix) :
        self.id         = Onduleur.id
        self.name       = name
        self.prix       = prix
        Onduleur.id     += 1