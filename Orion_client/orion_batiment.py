from abc import ABC

from Orion_client.orion_ressources import Ressources

class Batiment(ABC):
    """Classe parente des types de batiments"""
    cout_fonctionnement: Ressources = Ressources()  # À implementer
    cout_construction: Ressources
    lien_image: str = ""  # À implementer
    nom: str = ""   
    def __init__(self):
        self.niveau: int = 1  # À implementer
     
    def ameliorer(self):
        raise NotImplementedError
    
    def reparer(self):
        raise NotImplementedError
    
    def consommerRessources(self):
        raise NotImplementedError
    
    def produireRessources(self):
        raise NotImplementedError
    
    def detruire(self):
        raise NotImplementedError

class Mine(Batiment):
    """Batiment qui produit du metal"""
    nom: str = "Mine"
    cout_constrution = Ressources(metal=10, bois=20, nourriture=5)
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(metal=10)

class Scierie(Batiment):
    """Batiment qui produit du bois"""
    nom: str = "Scierie"
    cout_constrution = Ressources(metal=20, bois=10, nourriture=5) 
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(bois=10)

class Eglise(Batiment):
    """Batiment qui permet de convertir la population"""
    nom: str = "Eglise" 
    cout_constrution = Ressources(metal=175, bois=500, nourriture=55, population=25)

    def __init__(self):
        super().__init__()

class Ferme(Batiment):
    """Batiment qui produit de la nourriture"""
    nom: str = "Ferme"
    cout_constrution = Ressources(metal=15, bois=15, nourriture=5)
 
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(nourriture=10)


class Centrale(Batiment):
    """Batiment qui produit de l'energie"""
    nom: str = "Centrale électrique" 
    cout_constrution = Ressources(metal=75, bois=50, nourriture=10)
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources = Ressources(energie=50)


class Defense(Batiment):
    """Batiment qui ajoute a la puissance de la planete"""
    nom: str = "Defense Anti-Aérienne"
    cout_constrution = Ressources(metal=500, bois=100, nourriture=50)
    
    def __init__(self):
        super().__init__()

class Hangar(Batiment):
    """Batiment qui permet de creer des vaisseaux"""
    nom: str = "Hangar" 
    cout_constrution = Ressources(metal=750, bois=10, nourriture=20) 
    
    def __init__(self):
        super().__init__()

class Laboratoire(Batiment):
    """Batiment qui permet de debloquer des competences"""
    nom: str = "Laboratoire" 
    cout_constrution = Ressources(metal=125, bois=500, nourriture=45)  
   
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

 
 
