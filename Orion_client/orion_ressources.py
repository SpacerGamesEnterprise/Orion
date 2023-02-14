from __future__ import annotations

class Ressources(dict):
    """Classe qui contient les ressources
    
    Types de ressources :
        - metal
        - energie
        - nourriture
        - population
    """
    def __init__(self, metal: float, energie: float, nourriture: float, population: float):
        super().__init__()
        self: dict[str, float]
        self ["metal"] = metal
        self ["energie"] = energie
        self ["nourriture"] = nourriture
        self ["population"] = population
        
    def __add__(self, other: Ressources) -> Ressources: 
        return Ressources(
            metal=self["metal"] + other["metal"],
            energie=self["energie"] + other["energie"],
            nourriture=self["nourriture"] + other["nourriture"],
            population=self["population"] + other["population"]
        )

    def __sub__(self, other: Ressources) -> Ressources: 
        return Ressources(
            metal=self["metal"] - other["metal"],
            energie=self["energie"] - other["energie"],
            nourriture=self["nourriture"] - other["nourriture"],
            population=self["population"] - other["population"]
        )

   
