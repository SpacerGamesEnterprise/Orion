"""Gestionnaire de tout ce qui est côté client. Aucune communication directe
avec le serveur.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable
from modeles.vaisseau import Vaisseau

from modeles.planete import Planete


if TYPE_CHECKING:
    from controleur_serveur import Controleur
    from tkinter import Canvas

import tkinter as tk

from vue import Vue, VueSplash, VueLobby,VueCosmos,VueHUD
from orion_modele import Modele

class GestionnaireVue(ABC):
    """Classe de base pour tous les gestionnaires de vues."""
    def __init__(self, parent: GestionnaireVue, controleur: Controleur):
        self.vue: Vue
        """Vue de chaque gestionnaire."""
        self.parent = parent
        """Parent du gestionnaire (le gestionnaire qui l'a créé)."""
        if self.parent:
            self.root = self.parent.root
           
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

    def entrer(self, cls_gestionaire: type[GestionnaireVue])->GestionnaireVue:
        self.vue.destroy()
        gestionnaire = cls_gestionaire(self, self.controleur)
        gestionnaire.debuter()
        return gestionnaire
        
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
        self.vue = VueLobby(self.root)
        
        self.vue.main_canvas.tag_bind(
                self.vue.bouton_commencer, "<Button-1>",
                self.ignore_event(self.controleur.lancer_partie)
            )

    def ignore_event(self, func: Callable) -> Callable:
        def inner(self, *_):
            func()
        return inner

    def entrer(self, cls_gestionaire: type[GestionnaireVue])->GestionnaireVue:
        self.vue.destroy()
        gestionnaire = cls_gestionaire(self, self.controleur)
        gestionnaire.debuter()
        return gestionnaire

    def debuter(self):
        self.vue.afficher()

    def quitter(self):
        raise NotImplementedError
    
    def update_lobby(self,dico):

        self.vue.update_lobby(dico)


        if self.controleur.joueur_createur:
            #self.btnlancerpartie.config(state=NORMAL) #TODO Faire que le joueur créateur est le seul a commencer une partie
            pass
    
class GestionnairePartie(GestionnaireVue):
    def __init__(self, parent: GestionnaireVue, controleur: Controleur):
        super().__init__(parent,controleur)

        self.root.resizable(False,False)

        self.controleur = controleur
        self.game_frame = tk.Frame(self.root)

        self.ma_selection = None

        self.vueCosmos = VueCosmos(self.root, self.game_frame,self.controleur.modele)
        self.vueHUD = VueHUD(self.root, self.game_frame,self.controleur.modele)
        
        self.root.geometry(f"{self.vueHUD.background_width}x{self.vueHUD.background_height}")

    def bind_controls(self):
        #self.vueCosmos.canvas_cosmos.bind("<MouseWheel>", self.vueCosmos.do_zoom)
        self.vueCosmos.canvas_cosmos.bind("<Button-1>", self.cosmos_clic)
        self.vueHUD.minimap.bind("<Button-3>", self.vueHUD.cacher_mini)
        self.vueHUD.minimap_button.bind("<Button-1>",self.vueHUD.montrer_mini)
        self.vueHUD.minimap.bind("<Button-1>", self.mini_clic)
        self.vueHUD.minimap.bind("<Button-1>", self.mini_clic)

        self.vueHUD.bouton_combat.bind("<Button-1>", self.creer_vaisseau)
        self.vueHUD.bouton_cargo.bind("<Button-1>", self.creer_vaisseau)
        self.vueHUD.bouton_eclaireur.bind("<Button-1>", self.creer_vaisseau)
        #self.vueHUD.bouton_batiment.bind("<Button-1>", self.construire_batiment)

    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.controleur.creer_vaisseau(type_vaisseau)
        self.vueCosmos.afficher_vaisseau()

    def cosmos_clic(self,e):
        before_x = self.vueCosmos.canvas_cosmos.canvasx(e.x)
        before_y = self.vueCosmos.canvas_cosmos.canvasy(e.y)
        self.vueCosmos.centrer_clic(e)
        after_x = self.vueCosmos.canvas_cosmos.canvasx(e.x)
        after_y = self.vueCosmos.canvas_cosmos.canvasy(e.y)

        move_x = after_x - before_x
        move_y = after_y - before_y

        self.vueHUD.reposition_cursor(move_x,move_y)
        
        #self.vueHUD.reposition_cursor()
        t = self.vueCosmos.canvas_cosmos.gettags(tk.CURRENT)
        if t:  # il y a des tags
            if t[0] == self.controleur.mon_nom:  # et
                self.ma_selection = [self.controleur.mon_nom, t[1], t[2]]
                if t[2] == "Etoile":
                    self.afficher_menu_planete(self.ma_selection)
                    #self.montrer_etoile_selection()
                elif t[3] == "Vaisseau":
                    self.afficher_menu_vaisseau(self.ma_selection)
                    #self.montrer_flotte_selection()
            elif ("Etoile" in t or "Porte_de_ver" in t) and t[0] != self.controleur.mon_nom:
                if self.ma_selection:
                    #self.parent.cibler_flotte(self.ma_selection[1], t[1], t[2])
                    pass
                self.ma_selection = None
                self.vueCosmos.canvas_cosmos.delete("marqueur")
        else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
            print("Region inconnue")
            self.ma_selection = None
            self.vueCosmos.canvas_cosmos.delete("marqueur")

    def afficher_menu_planete(self, info_click: list):
        for joueur in self.controleur.modele.joueurs.keys():
            if self.controleur.modele.joueurs[joueur].nom == info_click[0]:
                for planete in self.controleur.modele.joueurs[joueur].etoilescontrolees:
                    if planete.id == info_click[1]:
                        planete_clique: Planete  = planete
            
        self.vueHUD.afficher_menu_planete(planete_clique)
    
    def afficher_menu_vaisseau(self, info_click: list):
        self.vueHUD.afficher_menu_vaisseau(self.controleur.modele.joueurs[info_click[0]].flotte[info_click[2]][info_click[1]])


    def mini_clic(self,e):
        self.vueCosmos.mini_clic(e)
        self.vueHUD.mini_clic(e)
        
    def debuter(self):
        self.vueCosmos.afficher_decor()
        self.vueCosmos.afficher()

        self.vueHUD.afficher()
        self.vueHUD.afficher_info_joueur(self.controleur.mon_nom)
        self.vueHUD.afficher_mini_cosmos()
        self.bind_controls()
        self.game_frame.mainloop()

    
    def quitter(self):
        self.root.destroy()

    def entrer(self, cls_gestionaire: type[GestionnaireVue]) -> GestionnaireVue:
        self.vue.destroy()
        gestionnaire = cls_gestionaire(self, self.controleur)
        gestionnaire.debuter()
        return gestionnaire
    