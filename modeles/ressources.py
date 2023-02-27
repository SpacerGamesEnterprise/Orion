from __future__ import annotations

class Ressources(dict):
    """Classe qui contient les ressources
    
    Types de ressources :
        - metal
        - bois
        - energie
        - nourriture
        - population
    """
    def __init__(self, metal: float = 0, bois: float = 0, energie: float = 0, nourriture: float = 0, population: float = 0):
        super().__init__()
        self: dict[str, float]
        self ["metal"] = metal
        self ["bois"] = bois
        self ["energie"] = energie
        self ["nourriture"] = nourriture
        self ["population"] = population
        
    def __add__(self, other: Ressources) -> Ressources: 
        return Ressources(
            metal=self["metal"] + other["metal"],
            bois=self["bois"] + other["bois"],
            energie=self["energie"] + other["energie"],
            nourriture=self["nourriture"] + other["nourriture"],
            population=self["population"] + other["population"]
        )
    def __sub__(self, other: Ressources) -> Ressources: 
        return Ressources(
            metal=self["metal"] - other["metal"],
            bois=self["bois"] - other["bois"],
            energie=self["energie"] - other["energie"],
            nourriture=self["nourriture"] - other["nourriture"],
            population=self["population"] - other["population"]
        )

#ajouter multiplier et diviser

    def has_more(self, other: Ressources) -> bool:
        for key, value in other.items():
           if self[key] < value:
               return False
        return True
