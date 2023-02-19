"""
Contrôleur de tout ce qui est côté client. Aucune communication directe
avec le serveur.
"""

from __future__ import annotations
from abc import ABC, abstractmethod

import tkinter as tk


class ControleurClient(ABC):
    def __init__(self, root: tk.Tk):
        self.root = root

        self.main_frame = tk.Frame(root)

        self.vue: Vue
        """Vue de chaque contrôleur."""

    @abstractmethod
    def debuter(self):
        """Débute le contrôleur et affiche la vue."""
        pass

    @abstractmethod
    def quitter(self):
        """Quitter le contrôleur."""
        pass

    def entrer(self, controleur: ControleurClient):
        """Entre dans un nouveau contrôleur imbriqué (sous-menu)."""
        raise NotImplementedError
