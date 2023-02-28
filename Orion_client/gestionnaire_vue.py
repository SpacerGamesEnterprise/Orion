"""Gestionnaire de tout ce qui est côté client. Aucune communication directe
avec le serveur.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable


if TYPE_CHECKING:
    from controleur_serveur import Controleur
    from tkinter import Canvas

import tkinter as tk

from vue import Vue, VueSplash, VueLobby

class GestionnaireVue(ABC):
    """Classe de base pour tous les gestionnaires de vues."""
    def __init__(self, parent: GestionnaireVue, controleur: Controleur):
        self.vue: Vue
        """Vue de chaque gestionnaire."""
        self.parent = parent
        """Parent du gestionnaire (le gestionnaire qui l'a créé)."""
        self.controleur = controleur
        """Contrôleur de l'application."""

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
        super().__init__(parent, controleur)
        self.root = tk.Tk()

        self.vue = VueSplash(self.root)

        self.vue.input_url.insert(0, self.controleur.urlserveur)
        self.vue.input_url.bind(
            "<Return>",
            lambda _: setattr(self.controleur, 'urlserveur', self.vue.value_url.get())
        )

        self.vue.input_nom.insert(0, self.controleur.mon_nom)
        self.vue.input_nom.bind(
            "<Return>",
            lambda _: setattr(self.controleur, 'mon_nom', self.vue.value_nom.get())
        )
        

        self.vue.main_canvas.tag_bind(
            self.vue.bouton_connecter, "<Button-1>",
            self.ignore_event(self.controleur.connecter_serveur)
        )

        self.vue.main_canvas.tag_bind(
            self.vue.bouton_creer_partie, "<Button-1>",
            self.ignore_event(self.controleur.creer_partie)
        )

        self.vue.main_canvas.tag_bind(
            self.vue.bouton_inscrire_joueur, "<Button-1>",
            self.ignore_event(self.controleur.inscrire_joueur)
        )

        self.vue.main_canvas.tag_bind(
            self.vue.bouton_reinitialiser_partie, "<Button-1>",
            self.ignore_event(self.controleur.reset_partie)
        )


    def ignore_event(self, func: Callable) -> Callable:
        def inner(self, *_):
            func()
        return inner

    def debuter(self):
        self.vue.afficher()
        self.vue.master.mainloop()

    def quitter(self):
        self.root.destroy()

    def entrer(self, cls_gestionaire: type[GestionnaireVue]):
        self.vue.destroy()
        gestionnaire = cls_gestionaire(self, self.controleur)
        gestionnaire.debuter()
        
    def update_splash(self, etat):
        canvas: Canvas = self.vue.main_canvas
        msg: int = self.vue.message
        if "attente" in etat or "courante" in etat:
            pass
            #self.btncreerpartie.config(state=DISABLED)
        if "courante" in etat:
            canvas.itemconfigure(msg, text="Desole - partie encours !")
            #self.btninscrirejoueur.config(state=DISABLED)
        elif "attente" in etat:
            canvas.itemconfigure(msg, text="Partie en attente de joueurs !")
            #self.btninscrirejoueur.config(state=NORMAL)
        elif "dispo" in etat:
            canvas.itemconfigure(msg, text="Bienvenue ! Serveur disponible")
            #self.btninscrirejoueur.config(state=DISABLED)
            #self.btncreerpartie.config(state=NORMAL)
        else:
            canvas.itemconfigure(msg, text="ERREUR - un probleme est survenu")


class GestionnaireLobby(GestionnaireVue):
    """Gestionnaire du lobby de l'application."""

    def __init__(self, parent: GestionnaireVue, controleur: Controleur):
        super().__init__(parent, controleur)
        self.vue = VueLobby(parent.vue.main_frame)

    def debuter(self):
        self.vue.afficher()

    def quitter(self):
        raise NotImplementedError
