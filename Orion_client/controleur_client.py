"""
Gestionnaire de tout ce qui est côté client. Aucune communication directe
avec le serveur.
"""

from __future__ import annotations
from abc import ABC, abstractmethod

import tkinter as tk


class GestionnaireVue(ABC):
    """Classe de base pour tous les gestionnaires de vues."""
    def __init__(self, root: tk.Tk):
        self.root = root

        self.main_frame = tk.Frame(root)

        self.vue: Vue  # TODO: Importer Vue
        """Vue de chaque gestionnaire."""

    @abstractmethod
    def debuter(self):
        """Débute le gestionnaire et affiche la vue."""
        pass

    @abstractmethod
    def quitter(self):
        """Quitter le gestionnaire."""
        pass

    def entrer(self, gestionaire: GestionnaireVue):
        """Entre dans un nouveau gestionnaire imbriqué (sous-menu)."""
        raise NotImplementedError


class GestionnaireMenuPrincipal(GestionnaireVue):
    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.vue = VueMenuPrincipal(self)

    def debuter(self):
        self.vue.afficher()

    def quitter(self):
        self.root.destroy()

    def entrer(self, gestionaire: GestionnaireVue):
        self.vue.cacher()
        gestionaire.debuter()

