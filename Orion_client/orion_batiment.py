from abc import ABC

from Orion_client.orion_ressources import Ressources

class Batiment(ABC):
    """Classe parente des types de batiments"""
    cout_constrution: Ressources(0,0,0,0)  # À implementer
    cout_fonctionnement: Ressources(0,0,0,0)  # À implementer
    lien_image: str = ""  # À implementer
    nom: str = ""   
    def __init__(self):
        self.niveau: int = 1  # À implementer
     
    def ameliorer():
        raise NotImplementedError
    
    def reparer():
        raise NotImplementedError
    
    def consommerRessources():
        raise NotImplementedError
    
    def produireRessources():
        raise NotImplementedError
    
    def detruire():
        raise NotImplementedError

class Mine(Batiment):
    """Batiment qui produit du metal"""
    nom: str = "Mine"
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources(10, 0, 0, 0)

class Eglise(Batiment):
    """Batiment qui permet de convertir la population"""
    nom: str = "Eglise" 
    
    def __init__(self):
        super().__init__()

class Ferme(Batiment):
    """Batiment qui produit de la nourriture"""
    nom: str = "Ferme" 
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources(0, 0, 10, 0)


class Centrale(Batiment):
    """Batiment qui produit de l'energie"""
    nom: str = "Centrale électrique" 
    
    def __init__(self):
        super().__init__()
        self.quantites_production: Ressources(0, 50, 0, 0)


class Defense(Batiment):
    """Batiment qui ajoute a la puissance de la planete"""
    nom: str = "Defense Anti-Aérienne" 
    
    def __init__(self):
        super().__init__()

class Hangar(Batiment):
    """Batiment qui permet de creer des vaisseaux"""
    nom: str = "Hangar" 
    
    def __init__(self):
        super().__init__()

class Laboratoire(Batiment):
    """Batiment qui permet de debloquer des competences"""
    nom: str = "Laboratoire" 
    
    def __init__(self):
        super().__init__()


 
 
