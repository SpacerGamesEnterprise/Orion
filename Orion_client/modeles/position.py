# Copyright (c) 2023 Grainus
# Licence Libre MIT

# L’autorisation est accordée, gracieusement, à toute personne acquérant une copie
# de ce logiciel et des fichiers de documentation associés (le « logiciel »), de commercialiser
# le logiciel sans restriction, notamment les droits d’utiliser, de copier, de modifier,
# de fusionner, de publier, de distribuer, de sous-licencier et / ou de vendre des copies du logiciel,
# ainsi que d’autoriser les personnes auxquelles la logiciel est fournie à le faire,
# sous réserve des conditions suivantes :
#
# La déclaration de copyright ci-dessus et la présente autorisation doivent être incluses dans
# toutes copies ou parties substantielles du logiciel.
#
# LE LOGICIEL EST FOURNI « TEL QUEL », SANS GARANTIE D’AUCUNE SORTE, EXPLICITE OU IMPLICITE,
# NOTAMMENT SANS GARANTIE DE QUALITÉ MARCHANDE, D’ADÉQUATION À UN USAGE PARTICULIER ET D’ABSENCE
# DE CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU TITULAIRES DU DROIT D’AUTEUR NE SERONT RESPONSABLES
# DE TOUT DOMMAGE, RÉCLAMATION OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS LE CADRE D’UN CONTRAT,
# D’UN DÉLIT OU AUTRE, EN PROVENANCE DE, CONSÉCUTIF À OU EN RELATION AVEC LE LOGICIEL OU SON UTILISATION,
# OU AVEC D’AUTRES ÉLÉMENTS DU LOGICIEL.
"""Contient plusieurs classes utiles à la manipulation de positions."""
from __future__ import annotations
from typing import overload, Iterator, Any

import math
import cmath


class Vecteur(complex):
    """Représente un vecteur dans un plan cartésien 2D."""

    def __eq__(self, other: Any) -> bool:
        """Détermine si les deux objets sont égaux en compensant pour
        les erreurs d'arrondissement.
        """
        if not isinstance(other, Vecteur):
            return NotImplemented
        return cmath.isclose(self, other)

    def __add__(self, *args, **kwargs):
        return self.__class__(super().__add__(*args, **kwargs))

    def __sub__(self, *args, **kwargs):
        return self.__class__(super().__sub__(*args, **kwargs))

    def __mul__(self, *args, **kwargs):
        return self.__class__(super().__mul__(*args, **kwargs))

    def __pow__(self, *args, **kwargs):
        return self.__class__(super().__pow__(*args, **kwargs))

    def __truediv__(self, *args, **kwargs):
        return self.__class__(super().__truediv__(*args, **kwargs))

    def __radd__(self, *args, **kwargs):
        return self.__class__(super().__radd__(*args, **kwargs))

    def __rsub__(self, *args, **kwargs):
        return self.__class__(super().__rsub__(*args, **kwargs))

    def __rmul__(self, *args, **kwargs):
        return self.__class__(super().__rmul__(*args, **kwargs))

    def __rpow__(self, *args, **kwargs):
        return self.__class__(super().__rpow__(*args, **kwargs))

    def __rtruediv__(self, *args, **kwargs):
        return self.__class__(super().__rtruediv__(*args, **kwargs))

    def __neg__(self, *args, **kwargs):
        return self.__class__(super().__neg__(*args, **kwargs))

    def __pos__(self, *args, **kwargs):
        return self.__class__(super().__pos__(*args, **kwargs))

    def __iter__(self) -> Iterator:
        return iter(self.get_coords())

    def conjugate(self):
        return self.__class__(super().conjugate())

    @property
    def norm(self) -> float:
        """Retourne ou modifie la norme du vecteur sans changer sa
        direction.
        """
        return abs(self)

    def rescale(self, value: float):
        """Retourne un nouveau vecteur avec la norme spécifiée et la
        même direction.
        """
        if self.norm:
            return self.__class__(*(self * value / self.norm))
        else:
            return self

    def normalize(self):
        """Retourne un vecteur unitaire dans la direction du vecteur."""
        return self / self.norm
    
    def rotate(self, angle: float):
        """Retourne un vecteur avec une rotation appliquée."""
        return self * complex(math.cos(angle), math.sin(angle))

    def get_coords(self) -> tuple[float, float]:
        """Retourne les coordonnées du Point en tuple."""
        return (self.real, self.imag)

    # It's not pretty, but without return self, the overload has the
    # wrong return type.
    @overload
    def clamp(self, *, max_length: float): return self

    @overload
    def clamp(self, *, min_length: float): return self

    @overload
    def clamp(self, *, min_length: float, max_length: float): return self

    @overload
    def clamp(self, max_length: float, /): return self

    @overload
    def clamp(self, min_length: float, max_length: float, /): return self

    def clamp(self, *args, **kwargs):
        """Retourne un nouveau vecteur avec une norme limitée entre
        les valeurs spécifiées.
        """
        arglen = len(args)
        if arglen == 1:
            # Un seul argument, on le considère comme max_length
            min_length, max_length = 0, args[0]
        elif arglen == 2:
            # Deux arguments, on les considère comme min_length et max_length
            min_length, max_length = args
        elif arglen > 2:
            raise TypeError(f"clamp() takes 1 or 2 positional arguments but {arglen} were given")

        if not args:
            min_length = kwargs.get("min_length", 0)
            max_length = kwargs.get("max_length", float("inf"))

        if min_length == 0 and max_length == float("inf"):
            raise TypeError("clamp() missing 1 required positional argument: 'max_length'")

        if min_length > max_length:
            raise ValueError("min_length must be less than or equal to max_length")

        if self.norm < min_length:
            ret = self.rescale(min_length)
        elif self.norm > max_length:
            ret = self.rescale(max_length)
        else:
            ret = self
        return ret
        

    @classmethod
    def zero(cls):
        """Retourne un vecteur nul."""
        return cls(0, 0)

    @classmethod
    def gauche(cls):
        """Retourne un vecteur unitaire vers la gauche (x = -1)."""
        return cls(-1, 0)

    @classmethod
    def droite(cls):
        """Retourne un vecteur unitaire vers la droite (x = 1)."""
        return cls(1, 0)

    @classmethod
    def haut(cls):
        """Retourne un vecteur unitaire vers le haut (y = -1)."""
        return cls(0, -1)

    @classmethod
    def bas(cls):
        """Retourne un vecteur unitaire vers le bas (y = 1)."""
        return cls(0, 1)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self}"

    def __str__(self) -> str:
        return f"{{{self.real}, {self.imag}}}"


class Point:
    """Représente un point dans un plan cartésien 2D."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other: Any) -> bool:
        """Détermine si les deux objets sont égaux."""
        if not isinstance(other, Point):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __add__(self, vecteur: Any):
        """Additionne le vecteur au point (translation)."""
        if not isinstance(vecteur, complex):
            return NotImplemented
        return self.__class__(self.x + vecteur.real, self.y + vecteur.imag)

    @overload
    def __sub__(self, other: Point) -> Vecteur: ...

    @overload
    def __sub__(self, other: Vecteur) -> Point: ...

    def __sub__(self, other: Any) -> Point | Vecteur:
        """Calcule la soustraction selon un autre point ou vecteur.
        Returns:
            Si other est un Point, un Vecteur avec le déplacement.
            Si other est un Vecteur, un Point déplacé.
        """
        if isinstance(other, Point):
            return Vecteur(self.x - other.x, self.y - other.y)
        elif isinstance(other, complex):
            return self.__add__(-other)
        else:
            return NotImplemented

    def __iter__(self) -> Iterator:
        return iter(self.get_coordonnee())

    def distance(self, other: Point) -> float:
        """Calcule la distance entre deux points."""
        return math.dist(self.get_coordonnee(), other.get_coordonnee())

    def get_coordonnee(self) -> tuple[float, float]:
        """Retourne les coordonnées du Point en tuple."""
        return (self.x, self.y)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self}"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Dimension2D(Vecteur):
    """Représente une taille en 2 dimensions."""
    def to_points(
            self,
            origin: Point = Point(0, 0),
            fromcenter: bool | None = None
    ) -> tuple[Point, Point]:
        if fromcenter:
            origin = origin - self / 2
        return (origin, origin + self)

    @property
    def width(self):
        return self.real

    @width.setter
    def width(self, value):
        self.real = value

    @property
    def height(self):
        return self.imag

    @height.setter
    def height(self, value):
        self.imag = value
