# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd
##  version  janvier 2023
#     enlever import inutile
from typing import Any, Literal

import json
import urllib.error
import urllib.parse
import urllib.request

from orion_modele import *
from orion_vue import *


class Controleur():
    """Controlleur du jeu Orion, qui gère les interactions entre le modèle et la vue
    
    Attributes
    -----------
    mon_nom: :class:`str`
        Nom de joueur, sert d'identifiant dans le jeu.
    joueur_createur: :class:`int`
        1 quand un joueur "Créer une partie", peut Demarrer la partie.
    cadrejeu: :class:`int`
        Compte les tours dans la boucle de jeu.
    actionsrequises: :class:`list`[:class:`tuple`[:class:`str`, :class:`str`, :class:`tuple`]]
        Les actions envoyées au serveur.
    joueurs: :class:`list`[:class:`str`]
        Specifies if the user is a system user (i.e. represents Discord officially).
        .. versionadded:: 1.3
    prochainsplash: Optional[:class:`str`]
        Requis pour sortir de cette boucle et passer au lobby du jeu.
    onjoue: :class:`int`
        Indicateur que le jeu se poursuive - sinon on attend qu'un autre joueur nous rattrape.
    maindelai: :class:`int`
        Delai en ms de la boucle de jeu.
    moduloappeler_serveur: :class:`int`
        Frequence des appel au serveur, evite de passer son temps a communiquer avec le serveur.
    urlserveur: :class:`str`
        URL du serveur.
    modele: :class:`Modele`
        La variable contenant la partie, après :meth:`~initialiserpartie`.
    vue: :class:`Vue`
        La vue pour l'affichage et les controles du jeu.
    """
    def __init__(self):
        self.mon_nom: str = self.generer_nom()
        """Nom de joueur, sert d'identifiant dans le jeu"""
        # ici, avec auto-generation
        self.joueur_createur: int = 0
        """1 quand un joueur "Créer une partie", peut Démarrer la partie"""
        self.cadrejeu: int = 0
        """Compte les tours dans la boucle de jeu (bouclersurjeu)"""
        self.actionsrequises: list[tuple[str, str, tuple[Any]]] = []
        """Les actions envoyées au serveur"""
        self.joueurs: list = []  # TODO: Find list type
        """Liste des noms de joueurs pour le lobby"""

        self.prochainsplash: bool | None = None  # TODO: Verify validity
        """Requis pour sortir de cette boucle et passer au lobby du jeu"""
        self.onjoue: int = 1
        """Indicateur que le jeu se poursuive - sinon on attend qu'un 
        autre joueur nous rattrape
        """
        self.maindelai: int = 50
        """Délai en ms de la boucle de jeu"""
        self.moduloappeler_serveur: int = 2
        """Fréquence des appel au serveur, évite de passer son temps à
        communiquer avec le serveur
        """
        # 127.0.0.1 pour tests,"http://votreidentifiant.pythonanywhere.com" pour web
        self.urlserveur: str = "http://127.0.0.1:8000"
        
        # self.urlserveur= "http://jmdeschamps.pythonanywhere.com"
        self.modele: Modele | None = None
        """La variable contenant la partie, après initialiserpartie()"""
        self.vue: Vue = Vue(
                self, self.urlserveur, self.mon_nom, "Non connecté"
        )
        """La vue pour l'affichage et les controles du jeu"""

        self.vue.root.mainloop()
        """La boucle des événements (souris, clavier, etc.)"""

    ##################################################################
    # FONCTIONS RESERVEES - INTERDICTION DE MODIFIER SANS AUTORISATION
    # PREALABLE SAUF CHOIX DE RANDOM SEED LIGNE 94-95
    def connecter_serveur(self, url_serveur: str) -> None:
        self.urlserveur = url_serveur
        """Le dernier avant le clic"""
        self.boucler_sur_splash()

    # a partir du splash
    def creer_partie(self, nom: str) -> None:
        if self.prochainsplash:
            # Si on est dans boucler_sur_splash, on doit supprimer
            # le prochain appel
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash = None
        if nom:  # Si c'est pas None, c'est un nouveau nom
            self.mon_nom = nom
        # On avertit le serveur qu'on crée une partie
        url = self.urlserveur + "/creer_partie"
        params = {"nom": self.mon_nom}
        reptext = self.appeler_serveur(url, params)
        """Réponse du serveur"""

        self.joueur_createur = 1
        """on est le createur"""
        self.vue.root.title("je suis " + self.mon_nom)
        # On passe au lobby pour attendre les autres joueurs
        self.vue.changer_cadre("lobby")
        self.boucler_sur_lobby()

    def inscrire_joueur(self, nom: str, urljeu: str) -> None:
        """Inscription d'un joueur à la partie, répétition de code avec
        creer_partie
        """
        # on quitte le splash et sa boucle
        if self.prochainsplash:
            self.vue.root.after_cancel(self.prochainsplash)
            self.prochainsplash = None
        if nom:
            self.mon_nom = nom
        # on s'inscrit sur le serveur
        url = self.urlserveur + "/inscrire_joueur"
        params = {"nom": self.mon_nom}
        reptext = self.appeler_serveur(url, params)

        self.vue.root.title("je suis " + self.mon_nom)
        self.vue.changer_cadre("lobby")
        self.boucler_sur_lobby()

    # a partir du lobby, le createur avertit le serveur de changer l'etat pour courant
    def lancer_partie(self) -> None:
        url = self.urlserveur + "/lancer_partie"
        params = {"nom": self.mon_nom}
        reptext = self.appeler_serveur(url, params)

    # Apres que le createur de la partie ait lancer_partie
    # boucler_sur_lobby a reçu code ('courant') et appel cette fonction pour tous
    def initialiser_partie(self, mondict: dict) -> None:
        print(f"Initialiser_partie: {mondict = }")
        initaleatoire = mondict[1][0][0]
        random.seed(12471)  # random FIXE pour test ou ...
        # random.seed(int(initaleatoire))   # qui prend la valeur generer par le serveur

        # on recoit la derniere liste des joueurs pour la partie
        listejoueurs = []
        for i in self.joueurs:
            listejoueurs.append(i[0])

        self.modele = Modele(self,
                             listejoueurs)  # on cree une partie pour les joueurs listes, qu'on conserve comme modele
        self.vue.initialiser_avec_modele(self.modele)  # on fournit le modele et mets la vue à jour
        self.vue.changer_cadre("partie")  # on change le cadre la fenetre pour passer dans l'interface de jeu

        self.boucler_sur_jeu()  # on lance la boucle de jeu

    ##########   BOUCLES: SPLASH, LOBBY ET JEU    #################
    # boucle de communication intiale avec le serveur pour creer ou s'inscrire a la partie
    def boucler_sur_splash(self):
        url = self.urlserveur + "/tester_jeu"
        params = {"nom": self.mon_nom}
        mondict = self.appeler_serveur(url, params)
        if mondict:
            self.vue.update_splash(mondict[0])
        self.prochainsplash = self.vue.root.after(50, self.boucler_sur_splash)

    # on boucle sur le lobby en attendant le demarrage
    def boucler_sur_lobby(self):
        url = self.urlserveur + "/boucler_sur_lobby"
        params = {"nom": self.mon_nom}
        mondict: list[tuple[str, int]] | tuple[Literal["courante"], tuple[int]] = self.appeler_serveur(url, params)
        print(f"{mondict = }")

        if "courante" in mondict[0]:  # courante, la partie doit etre initialiser
            self.initialiser_partie(mondict)
        else:
            self.joueurs = mondict
            self.vue.update_lobby(mondict)
            self.vue.root.after(50, self.boucler_sur_lobby)

    # BOUCLE PRINCIPALE
    def boucler_sur_jeu(self):
        self.cadrejeu += 1  # increment du compteur de boucle de jeu

        if self.cadrejeu % self.moduloappeler_serveur == 0:  # appel périodique au serveur
            if self.actionsrequises:
                actions = self.actionsrequises
            else:
                actions = None
            self.actionsrequises = []
            url = self.urlserveur + "/boucler_sur_jeu"
            params = {"nom": self.mon_nom,
                      "cadrejeu": self.cadrejeu,
                      "actionsrequises": actions}
            try:  # permet de récupérer des time-out, mais aussi des commandes de pause du serveur pour retard autre joueur
                mondict = self.appeler_serveur(url, params)
                if "ATTENTION" in mondict:  # verifie attente d'un joueur plus lent
                    print("ATTEND QUELQU'UN")
                    self.onjoue = 0
                else:  # sinon on ajoute l'action
                    self.modele.ajouter_actions_a_faire(mondict)
            except urllib.error.URLError as e:
                print("ERREUR ", self.cadrejeu, e)
                self.onjoue = 0

        # le reste du tour vers modele et vers vue, s'il y a lieu
        if self.onjoue:
            # envoyer les messages au modele et a la vue de faire leur job
            self.modele.jouer_prochain_coup(self.cadrejeu)
            self.vue.afficher_jeu()
        else:
            self.cadrejeu -= 1
            self.onjoue = 1

        self.vue.root.after(self.maindelai,
                            self.boucler_sur_jeu)  # appel ulterieur de la meme fonction jusqu'a l'arret de la partie

    ##############   FONCTIONS pour serveur #################
    # methode speciale pour remettre les parametres du serveur a leurs valeurs par defaut
    def reset_partie(self):
        leurl = self.urlserveur + "/reset_jeu"
        reptext = self.appeler_serveur(leurl, 0)
        self.vue.update_splash(reptext[0][0])
        return reptext

    #   retour de l'etat du serveur
    def tester_etat_serveur(self):
        leurl = self.urlserveur + "/tester_jeu"
        repdecode = self.appeler_serveur(leurl, None)[0]
        if "dispo" in repdecode:  # on peut creer une partie
            return ["dispo", repdecode]
        elif "attente" in repdecode:  # on peut s'inscrire a la partie
            return ["attente", repdecode]
        elif "courante" in repdecode:  # la partie est en cours
            return ["courante", repdecode]
        else:
            return "impossible"

    # fonction d'appel normalisee d'appel pendant le jeu
    def appeler_serveur(self, url, params):
        if params:
            query_string = urllib.parse.urlencode(params)
            data = query_string.encode("ascii")
        else:
            data = None
        rep = urllib.request.urlopen(url, data, timeout=None)
        reptext = rep.read()
        rep = reptext.decode('utf-8')
        rep = json.loads(rep)
        return rep

    ###  FIN DE L'INTERDICTION DE MODIFICATION
    #################################################################################

    ############            OUTILS           ###################
    # generateur de nouveau nom, peut y avoir collision
    def generer_nom(self):
        mon_nom = "JAJA_" + str(random.randrange(100, 1000))
        return mon_nom

    def abandonner(self):
        action = [self.mon_nom, "abandonner", [self.mon_nom + ": J'ABANDONNE !"]]
        self.actionsrequises = action
        self.root.after(500, self.root.destroy)

    ############        VOTRE CODE      ######################

    def creer_vaisseau(self, type_vaisseau):
        self.actionsrequises.append([self.mon_nom, "creervaisseau", [type_vaisseau]])

    def cibler_flotte(self, idorigine, iddestination, type_cible):
        self.actionsrequises.append([self.mon_nom, "ciblerflotte", [idorigine, iddestination, type_cible]])

    def afficher_etoile(self, joueur, cible):
        self.vue.afficher_etoile(joueur, cible)

    def lister_objet(self, objet, id):
        self.vue.lister_objet(objet, id)


if __name__ == "__main__":
    c = Controleur()
    print("End Orion_mini")
