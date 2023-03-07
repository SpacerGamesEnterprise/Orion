from abc import ABC
from typing import cast

import random
import logging

from modeles.position import Point, Vecteur
from modeles.ressources import Ressources

from id import get_prochain_id
from helper import Helper as hlp

def log(*args, **kwargs):
    logging.debug(f"Event called. Args: {args}, Kwargs: {kwargs}")

class Vaisseau(ABC):  
    """Classe parente des types de vaisseau"""

    def __init__(self, nom, position: Point):
        #self.parent = parent
        self.id: int = get_prochain_id()
        self.proprietaire: str = nom
        self.position: Point = position
        self.inventaire_ressources: Ressources = Ressources()
        self.max_inventaire: Ressources = Ressources()
        self.taille: int = 5
        self.vitesse: int = 20
        self.nom_vaisseau: str = ""
        self.niveau: int = 1
        self.cout_construction: Ressources = Ressources()

        self.cible: Point = None
        self.type_cible = None
        #self.angle_cible = 0
        self.mouvement = Vecteur(0, 0)
        """Vecteur de la position actuelle vers la cible"""
        self.arriver = {
            None: log,
            "Planete": log, #self.arriver_planete,
            "Porte_de_vers": log, #self.arriver_porte,
        }
                        
                        
    def ameliorer(self, inventaire_planete: Ressources) -> Ressources:
        """Retourne l'inventaire de la planète et augmente
        le niveau du vaissseau
        """
        if inventaire_planete >= (2 * self.cout_construction):
            self.cout_construction *= 2        
            inventaire_planete -= self.cout_construction
            self.niveau += 1
        return inventaire_planete 
    
    

    def jouer_prochain_coup(self, trouver_nouveau=0):
        if self.cible is not None:
            return self.avancer()
        elif trouver_nouveau:
            # NOTE: Accéder au parent est très mal
           # cible = random.choice(self.parent.parent.planetes)
            #self.acquerir_cible(cible, "Planete")
            pass

    def acquerir_cible(self, cible, type_cible):
        self.type_cible = type_cible
        self.cible = cible.position

    def avancer(self):
        """Avance le vaisseau vers sa cible selon sa vitesse."""
        if self.cible is not None:
            vec_total = self.cible - self.position
            mouvement = vec_total.clamp(self.vitesse)
            self.position += mouvement
            if vec_total.norm <= self.vitesse:
                self.cible = None
                return self.arriver[self.type_cible]()

    def arriver_planete(self):
        # NOTE: Accéder au parent est très mal
        self.parent.log.append(
            ["Arrive:", self.parent.parent.cadre_courant, "Planete", self.id, self.cible.id, self.cible.proprietaire])
        if not self.cible.proprietaire:
            self.cible.proprietaire = self.proprietaire
        cible = self.cible
        self.cible = 0
        return ["Planete", cible]

    def arriver_porte(self):
        # NOTE: Accéder au parent est très mal
        self.parent.log.append(["Arrive:", self.parent.parent.cadre_courant, "Porte", self.id, self.cible.id, ])
        cible = self.cible
        trou = cible.parent
        if cible == trou.porte_a:
            self.x = trou.porte_b.x + random.randrange(6) + 2
            self.y = trou.porte_b.y
        elif cible == trou.porte_b:
            self.x = trou.porte_a.x - random.randrange(6) + 2
            self.y = trou.porte_a.y
        self.cible = 0
        return ["Porte_de_ver", cible]


class Cargo(Vaisseau):
    """Vaisseau qui transporte des ressources"""
    def __init__(self, nom, position):
        super().__init__(nom, position)
        self.nom_vaisseau = "Cargo"
        self.cout_construction = Ressources(metal=1000, bois=500, energie=1500)
        self.max_inventaire = Ressources(
            metal=1000, 
            bois=1000,
            energie=50000,
            nourriture=1000,
            population=50
        )
        self.taille = 8
        self.vitesse = 1

class Eclaireur(Vaisseau):
    """Vaisseau avec une puissance faible dont le but est d'explorer rapidement"""
    def __init__(self, nom, position):
        super().__init__(nom, position)
        self.nom_vaisseau = "Éclaireur"
        self.cout_construction = Ressources(metal=250, bois=150, energie=500)
        self.max_inventaire = Ressources(
            metal=150, 
            bois=150,
            energie=500,
            nourriture=100,
            population=3
        )
        self.taille = 2
        self.vitesse = 7

class Combat(Vaisseau):
    """Vaisseau avec une haute puissance dont le but est de combatre """
    def __init__(self, nom, position):
        super().__init__(nom, position)
        self.nom_vaisseau = "Combat"
        self.cout_construction = Ressources(metal=500, bois=100, energie=750)
        self.max_inventaire = Ressources(
            metal=200, 
            bois=200,
            energie=5000,
            nourriture=500,
            population=15)
        self.taille = 4
        self.vitesse = 4
