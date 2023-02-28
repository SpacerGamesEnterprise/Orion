"""Gestionnaire de tout ce qui est côté client. Aucune communication directe
avec le serveur.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from Orion_client.vue import VueCosmos, VueHUD

if TYPE_CHECKING:
    from controleur_serveur import Controleur

import tkinter as tk

from vue import Vue, VueSplash

class GestionnaireVue(ABC):
    """Classe de base pour tous les gestionnaires de vues."""
    def __init__(self, parent: GestionnaireVue):
        self.vue: Vue
        """Vue de chaque gestionnaire."""
        self.parent = parent
        """Parent du gestionnaire (le gestionnaire qui l'a créé)."""

    @abstractmethod
    def debuter(self):  # TODO: Enlever ou changer le nom
        """Débute le gestionnaire et affiche la vue."""
        pass

    @abstractmethod
    def quitter(self):
        """Quitter le gestionnaire."""
        pass

    def entrer(self, gestionaire: GestionnaireVue):
        """Entre dans un nouveau gestionnaire imbriqué (sous-menu)."""
        self.vue.forget()


class GestionnaireSplash(GestionnaireVue):
    """Gestionnaire maître de l'application."""
    def __init__(self, parent: GestionnaireVue, controleur: Controleur):
        super().__init__(parent)
        self.root = tk.Tk()

        self.controleur = controleur
        self.vue = VueSplash(self.root)

        self.vue.input_url.bind("<Return>", self._update_url)
        self.vue.main_canvas.tag_bind(
            self.vue.bouton_connecter, "<Button-1>",
            self.controleur.connecter_serveur
        )

        self.vue.afficher()
        self.vue.master.mainloop()

    def _update_url(self, _):
        url = self.vue.value_url.get()
        self.controleur.urlserveur = url

    def debuter(self):
        self.vue.afficher()

    def quitter(self):
        self.root.destroy()

    def entrer(self, gestionaire: GestionnaireVue):
        self.vue.cacher()
        gestionaire.debuter()

class GestionnairePartie(GestionnaireVue):
    def __init__(self, parent: GestionnaireVue, controleur: Controleur):
        super.__init__(parent)
        
        self.controleur = controleur
        self.game_frame = tk.Frame()
        
        self.vueHUD = VueHUD(self.game_frame,self.parent.parent.root)
        self.vueCosmos = VueCosmos(self.game_frame,self.parent.parent.root)
        #self.vueCosmos.main_canvas.bind("<MouseWheel>", self.vueCosmos.do_zoom)
        #self.vueCosmos.main_canvas.bind("<MouseButton1>", self.vueCosmos.centrer_cosmos )
    