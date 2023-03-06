"""Gestionnaire de tout ce qui est côté client. Aucune communication directe
avec le serveur.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable
from enum import Enum

from modeles.batiment import (
    Batiment,
    Centrale,
    Defense,
    Eglise,
    Ferme,
    Hangar,
    Laboratoire,
    Mine,
    Scierie
)
from modeles.vaisseau import Vaisseau
from modeles.planete import Planete


if TYPE_CHECKING:
    from controleur_serveur import Controleur
    from tkinter import Canvas



import tkinter as tk

from vue import Vue, VueSplash, VueLobby,VueCosmos,VueHUD
from orion_modele import Modele, Point

class EtatClic(Enum):
    DEFAULT = 0 
    BOUGER_VAISSEAU = 1

class EtatMenu(Enum):
    DEFAULT = 0
    MENU_PLANETE = 1
    MENU_VAISSEAU = 2
    MENU_BATIMENT = 3

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
        self.modele = self.controleur.modele
        self.game_frame = tk.Frame(self.root)

        self.ma_selection = None

        self.etat_clic =  EtatClic.DEFAULT
        self.etat_menu = EtatClic.DEFAULT

        self.vue_cosmos = VueCosmos(self.root, self.game_frame, self.modele)
        self.vue_HUD = VueHUD(self.root, self.game_frame, self.modele)
        
        self.root.geometry(f"{self.vue_HUD.background_width}x{self.vue_HUD.background_height}")

    def update_jeu(self):
        if self.ma_selection is not None:
            if self.ma_selection[2] == "Planete":
                self.vue_HUD.update_info_planete(self.planete_select)
        """Mise à jour de la vue du jeu."""
        for joueur in self.modele.joueurs.values():
            for vaisseaumap in joueur.flotte.values():
                for vaisseau in vaisseaumap.values():
                    self.vue_cosmos.update_vaisseau(vaisseau)


    def bind_controls(self):
        #self.vueCosmos.canvas_cosmos.bind("<MouseWheel>", self.vueCosmos.do_zoom)
        self.vue_cosmos.canvas_cosmos.bind("<Button-1>", self.cosmos_clic)
        self.vue_HUD.minimap.bind("<Button-3>", self.vue_HUD.cacher_mini)
        self.vue_HUD.minimap_button.bind("<Button-1>",self.vue_HUD.montrer_mini)
        self.vue_HUD.minimap.bind("<Button-1>", self.mini_clic)
        self.vue_HUD.minimap.bind("<Button-1>", self.mini_clic)

        self.vue_HUD.bouton_combat.bind("<Button-1>", self.creer_vaisseau)
        self.vue_HUD.bouton_cargo.bind("<Button-1>", self.creer_vaisseau)
        self.vue_HUD.bouton_eclaireur.bind("<Button-1>", self.creer_vaisseau)
        self.vue_HUD.bouton_bouger.bind("<Button-1>",self.bouger_vaisseau)
        self.vue_HUD.bouton_conquerir.bind("<Button-1>",self.conquerir)
        self.vue_HUD.bouton_batiment.bind("<Button-1>", self.afficher_menu_batiment)
        self.vue_HUD.bouton_defense.bind("<Button-1>", self.bind_batiment(Defense))
        self.vue_HUD.bouton_ferme.bind("<Button-1>", self.bind_batiment(Ferme))
        self.vue_HUD.bouton_centrale.bind("<Button-1>", self.bind_batiment(Centrale))
        self.vue_HUD.bouton_mine.bind("<Button-1>", self.bind_batiment(Mine))
        self.vue_HUD.bouton_hangar.bind("<Button-1>", self.bind_batiment(Hangar))
        self.vue_HUD.bouton_laboratoire.bind("<Button-1>", self.bind_batiment(Laboratoire))
        self.vue_HUD.bouton_scierie.bind("<Button-1>", self.bind_batiment(Scierie))
        self.vue_HUD.bouton_eglise.bind("<Button-1>", self.bind_batiment(Eglise))

    @property
    def planete_select(self) -> Planete | None:
        """Retourne la planète actuellement sélectionnée, si possible."""
        if (self.ma_selection is not None 
                and self.ma_selection[2] == "Planete"
        ):
            joueur = self.modele.joueurs[self.ma_selection[0]]
            return [
                planete
                for planete in joueur.planetes_controlees
                if planete.id == self.ma_selection[1]
            ][0]
        else:
            return None

    def bind_batiment(self, type_batiment: type[Batiment]):
        def inner(*args, **kwargs):
            self.planete_select.ajouter_batiment(type_batiment())
        return inner

    def afficher_menu_batiment(self, e):
        self.vue_HUD.afficher_menu_batiments(self.planete_select)

    def bouger_vaisseau(self,e):
        self.etat_clic = EtatClic.BOUGER_VAISSEAU
        v_select = self.modele.joueurs[self.ma_selection[0]].flotte[self.ma_selection[2]][self.ma_selection[1]]

    def conquerir(self, e): # TODO: use tags
        for planete in self.modele.planetes:
            pos_vaisseau = self.modele.joueurs[self.ma_selection[0]].flotte[self.ma_selection[2]][self.ma_selection[1]].position
            if pos_vaisseau.y - 100 < planete.position.y < pos_vaisseau.y + 100:
                if pos_vaisseau.x - 100 < planete.position.x < pos_vaisseau.x + 100:
                    if planete.proprietaire == "":
                        planete.proprietaire = self.modele.joueurs[self.ma_selection[0]].nom
                        self.modele.planetes.remove(planete)
                        self.modele.joueurs[self.ma_selection[0]].planetes_controlees.append(planete)
                        self.vue_cosmos.coloniser(planete)
        self.vue_HUD.afficher_mini_cosmos()
        


    def creer_vaisseau(self, evt):
        type_vaisseau = evt.widget.cget("text")
        self.controleur.creer_vaisseau(type_vaisseau)
        self.vue_cosmos.afficher_vaisseau()

    def cosmos_clic(self, event: tk.Event):
        if self.etat_clic == EtatClic.BOUGER_VAISSEAU:
            v_select: Vaisseau = self.modele.joueurs[self.ma_selection[0]].flotte[self.ma_selection[2]][self.ma_selection[1]]

            destination_x = self.vue_cosmos.canvas_cosmos.canvasx(event.x)
            destination_y = self.vue_cosmos.canvas_cosmos.canvasy(event.y)

            v_select.cible = Point(destination_x, destination_y)

            self.etat_clic = EtatClic.DEFAULT

        elif self.etat_clic == EtatClic.DEFAULT: 
            self.centre_ecran_canvas_x = self.vue_cosmos.canvas_cosmos.canvasx(event.x)
            self.centre_ecran_canvas_y = self.vue_cosmos.canvas_cosmos.canvasy(event.y)

            self.vue_cosmos.centrer_canvas(self.centre_ecran_canvas_x ,self.centre_ecran_canvas_y )

            after_x = self.vue_cosmos.canvas_cosmos.canvasx(event.x)
            after_y = self.vue_cosmos.canvas_cosmos.canvasy(event.y)

            move_x = after_x - self.centre_ecran_canvas_x 
            move_y = after_y - self.centre_ecran_canvas_y 

            self.vue_HUD.reposition_cursor(move_x,move_y)
            
            if self.etat_menu == EtatMenu.MENU_VAISSEAU:
                self.vue_HUD.cacher_menu_vaisseau()
                self.etat_menu = EtatMenu.DEFAULT
            #self.vueHUD.reposition_cursor()

            t = self.vue_cosmos.canvas_cosmos.gettags(tk.CURRENT)

            if t:  # il y a des tags
                if t[0] == self.controleur.mon_nom:  # et
                    self.ma_selection = [self.controleur.mon_nom, t[1], t[2]]
                    if t[2] == "Planete":
                        self.etat_menu = EtatMenu.MENU_PLANETE
                        self.afficher_menu_planete(self.ma_selection)
                        #self.montrer_etoile_selection()
                    elif t[3] == "Vaisseau":
                        self.etat_menu = EtatMenu.MENU_VAISSEAU
                        self.afficher_menu_vaisseau(self.ma_selection)
                        #self.montrer_flotte_selection()
                elif ("Planete" in t or "Porte_de_ver" in t) and t[0] != self.controleur.mon_nom:
                    if self.ma_selection:
                        #self.parent.cibler_flotte(self.ma_selection[1], t[1], t[2])
                        pass
                    self.ma_selection = None
                    self.vue_cosmos.canvas_cosmos.delete("marqueur")
            else:  # aucun tag => rien sous la souris - sinon au minimum il y aurait CURRENT
                print("Region inconnue")
                self.ma_selection = None
                self.vue_cosmos.canvas_cosmos.delete("marqueur")

    def afficher_menu_planete(self, info_click: list):
        self.vue_HUD.afficher_menu_planete(self.planete_select)
    
    def afficher_menu_vaisseau(self, info_click: list):
        self.vue_HUD.afficher_menu_vaisseau(self.modele.joueurs[info_click[0]].flotte[info_click[2]][info_click[1]])


    def mini_clic(self,e):
        self.vue_cosmos.mini_clic(e)
        self.vue_HUD.mini_clic(e)
        
    def debuter(self):
        self.vue_cosmos.afficher_decor()
        self.vue_cosmos.afficher()

        self.vue_HUD.afficher()
        self.vue_HUD.afficher_info_joueur(self.controleur.mon_nom)
        self.vue_HUD.afficher_mini_cosmos()
        self.bind_controls()
        #self.game_frame.mainloop()

    
    def quitter(self):
        self.root.destroy()

    def entrer(self, cls_gestionaire: type[GestionnaireVue]) -> GestionnaireVue:
        self.vue.destroy()
        gestionnaire = cls_gestionaire(self, self.controleur)
        gestionnaire.debuter()
        return gestionnaire
    