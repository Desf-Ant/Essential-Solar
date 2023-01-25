import json

class PV :

    id = 0

    def __init__(self, ref="no_ref", prix_par_kWh=0, type="", dimension=0, gamme_puissance=0, efficacite=0, poids=0, region="", prix=0) :
        self.id             = PV.id 
        self.ref            = ref
        self.prix_par_kWh   = prix_par_kWh
        self.type           = type
        self.dimension      = dimension 
        self.surface        = "--"
        self.gamme_puissance= gamme_puissance
        self.efficacite     = efficacite
        self.poids          = poids
        self.region         = region
        self.prix           = prix
        PV.id               += 1

        if self.prix != "--" : self.prix = round(float(self.prix),2)

        if self.dimension != "--" : self.surface = float(self.dimension.split("x")[0]) * float(self.dimension.split("x")[1])/1_000_000

    def __str__(self) -> str:
        return "id: {id},\n {ref},\n {type},\n {parkWh} €/kWh, \n {surface} m2,\n {prix} €\n".format(id=self.id, ref=self.ref, type=self.type, parkWh=self.prix_par_kWh,prix=self.prix, surface=self.surface)
    
    def toJson(self) :
        return {
            "id" : self.id,
            "reference" : self.ref,
            "prix_par_kWh": self.prix_par_kWh,
            "type" : self.type,
            "dimension":self.dimension,
            "surface":self.surface,
            "gamme_puissance":self.gamme_puissance,
            "efficacite":self.efficacite,
            "poids":self.poids,
            "region":self.region,
            "prix":self.prix
        }