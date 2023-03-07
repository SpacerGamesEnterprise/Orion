from abc import ABC

from modeles.ressources import Ressources
from modeles.vaisseau import Vaisseau

class Batiment(ABC):
    """Classe parente des types de batiments"""
    cout_fonctionnement: Ressources = Ressources()  # À implementer
    cout_construction: Ressources
    
    lien_image: str = ""  # À implementer
    nom: str = ""   
    def __init__(self):
        self.niveau: int = 1
        self.quantites_production: Ressources = Ressources()
     
    def ameliorer(self, inventaire_planete: Ressources) -> Ressources:
        """Retourne l'inventaire de la planete augmente le niveau du batiment"""
        if inventaire_planete >= (self.cout_construction * (self.niveau + 1)):
            inventaire_planete -= self.cout_construction
            self.niveau += 1
            self.quantites_production *= self.niveau
        return inventaire_planete      
    
    def reparer(self):
        raise NotImplementedError
    
    def consommer_ressources(self):
        raise NotImplementedError
    
    def detruire(self):
        raise NotImplementedError

class Mine(Batiment):
    """Batiment qui produit du metal"""
    nom: str = "Mine"
    cout_construction = Ressources(metal=10, bois=20, nourriture=5)
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(metal=10)

class Scierie(Batiment):
    """Batiment qui produit du bois"""
    nom: str = "Scierie"
    cout_construction = Ressources(metal=20, bois=10, nourriture=5) 
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(bois=10)

class Eglise(Batiment):
    """Batiment qui permet de convertir la population"""
    nom: str = "Eglise" 
    cout_construction = Ressources(metal=175, bois=500, nourriture=55, population=25)

    def __init__(self):
        super().__init__()

class Ferme(Batiment):
    """Batiment qui produit de la nourriture"""
    nom: str = "Ferme"
    cout_construction = Ressources(metal=15, bois=15, nourriture=5)
 
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(nourriture=10)
        
class Centrale(Batiment):
    """Batiment qui produit de l'energie"""
    nom: str = "Centrale électrique" 
    cout_construction = Ressources(metal=75, bois=50, nourriture=10)
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(energie=50)


class Defense(Batiment):
    """Batiment qui ajoute a la puissance de la planete"""
    nom: str = "Defense Anti-Aérienne"
    cout_construction = Ressources(metal=500, bois=100, nourriture=50)
    
    def __init__(self):
        super().__init__()

class Hangar(Batiment):
    """Batiment qui permet de creer des vaisseaux"""
    nom: str = "Hangar" 
    cout_construction = Ressources(metal=750, bois=10, nourriture=20) 
    
    def __init__(self):
        super().__init__()
        
        
    def creer_vaisseau(
            self,
            vaisseau: Vaisseau,
            inventaire_planete: Ressources,
            liste_vaisseaux: list[Vaisseau]
    ) -> Ressources:
        """Retourne l'inventaire de la planete"""
        if inventaire_planete >= (vaisseau.cout_construction):
            inventaire_planete -= vaisseau.cout_construction
            liste_vaisseaux.append(vaisseau)
        return inventaire_planete       
        

class Laboratoire(Batiment):
    """Batiment qui permet de debloquer des competences"""
    nom: str = "Laboratoire" 
    cout_construction = Ressources(metal=125, bois=500, nourriture=45)  
   
    def __init__(self):
        super().__init__()

class Usine(Batiment):
    """Batiment qui produit un peu de tout (batiment de depart)"""
    nom: str = "Usine"
    cout_construction =  Ressources()
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(
            metal=1, 
            bois=1,
            energie=5,
            nourriture=1
        )

 
 
