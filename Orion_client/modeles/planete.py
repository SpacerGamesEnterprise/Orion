import random
from modeles.batiment import Batiment
from modeles.ressources import Ressources
from id import get_prochain_id


class Planete():
    def __init__(self, x, y):
        self.id = get_prochain_id()
        #self.parent = parent
        self.proprietaire = ""
        self.x = x
        self.y = y
        self.taille = random.randrange(4, 8)
        self.ressources_disponibles = Ressources(
            metal=random.randrange(1_000, 10_000_000),
            bois=random.randrange(1_000, 10_000_000),
            nourriture=random.randrange(1_000, 10_000_000)
        )
        self.inventaire_ressources = Ressources()
        self.max_inventaire = Ressources(
            metal=10_000,
            bois=10_000,
            energie=50_000,
            nourriture=10_000,
            population=10_000
        )
        self.batiments: list[Batiment] = []
        self.limite_batiment = 4
        self.vaisseaux = []
        
    def espace_batiment_dispo(self) -> bool:
        """Retourne si il reste de la place pour un bâtiment sur la planète"""
        return len(self.batiments) < self.limite_batiment
    
    def ajouter_batiment(self, batiment: Batiment) -> bool:
        """Retourne si un batiment est ajouté dans la liste de la planete"""
        if self.espace_batiment_dispo() \
                and self.inventaire_ressources.has_more(batiment.cout_construction):
            self.inventaire_ressources -= batiment.cout_construction
            self.batiments.append(batiment)
            return True  
        return False
    
    def produire_ressources(self):
        """Ajoute des ressources dans la plenete"""
        for bati in self.batiments:
            self.inventaire_ressources += bati.quantites_production
        
        