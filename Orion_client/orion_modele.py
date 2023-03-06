# -*- coding: utf-8 -*-
##  version 2022 14 mars - jmd

import ast
import random
from modeles.position import Point
from modeles.vaisseau import Cargo, Eclaireur, Combat
from modeles.batiment import Usine
from id import get_prochain_id
from modeles.planete import Planete

class Porte_de_vers():
    def __init__(self, parent, x, y, couleur, taille):
        self.parent = parent
        self.id = get_prochain_id()
        self.x = x
        self.y = y
        self.pulsemax = taille
        self.pulse = random.randrange(self.pulsemax)
        self.couleur = couleur

    def jouer_prochain_coup(self):
        self.pulse += 1
        if self.pulse >= self.pulsemax:
            self.pulse = 0


class Trou_de_vers():
    def __init__(self, x1, y1, x2, y2):
        self.id = get_prochain_id()
        taille = random.randrange(6, 20)
        self.porte_a = Porte_de_vers(self, x1, y1, "red", taille)
        self.porte_b = Porte_de_vers(self, x2, y2, "orange", taille)
        self.liste_transit = []  # pour mettre les vaisseaux qui ne sont plus dans l'espace mais maintenant l'hyper-espace

    def jouer_prochain_coup(self):
        self.porte_a.jouer_prochain_coup()
        self.porte_b.jouer_prochain_coup()            


class Joueur():
    def __init__(self, parent, nom, etoilemere, couleur):
        self.id = get_prochain_id()
        self.parent = parent
        self.nom = nom
        self.etoilemere = etoilemere
        self.etoilemere.proprietaire = self.nom
        self.couleur = couleur
        self.log = []
        self.etoilescontrolees = [etoilemere]
        self.flotte = {"Eclaireur": {},
                       "Cargo": {},
                       "Combat": {}}
        self.actions = {"ciblerflotte": self.ciblerflotte,
                        "creervaisseau": self.creervaisseau}

    def creervaisseau(self, type_vaisseau): #TODO update hangar
        type_vaisseau =  type_vaisseau[0]
        x, y = self.etoilemere.position
        position = Point(x + 10, y)
        if type_vaisseau == "Cargo":
            v = Cargo(self.nom, position)
        elif type_vaisseau == "Eclaireur":
            v = Eclaireur(self.nom, position)
        else:
            v = Combat(self.nom, position)
        self.flotte[type_vaisseau][v.id] = v
        #if self.nom == self.parent.parent.mon_nom:
            #self.parent.parent.lister_objet(type_vaisseau, v.id)
        self.parent.parent.gestionnaire_partie.vue_cosmos.afficher_vaisseau()
        
        return v


    def ciblerflotte(self, ids):
        idori, iddesti, type_cible = ids
        ori = None
        for i in self.flotte.keys():
            if idori in self.flotte[i]:
                ori = self.flotte[i][idori]

        if ori:
            if type_cible == "Etoile":
                for j in self.parent.etoiles:
                    if j.id == iddesti:
                        ori.acquerir_cible(j, type_cible)
                        return
            elif type_cible == "Porte_de_ver":
                cible = None
                for j in self.parent.trou_de_vers:
                    if j.porte_a.id == iddesti:
                        cible = j.porte_a
                    elif j.porte_b.id == iddesti:
                        cible = j.porte_b
                    if cible:
                        ori.acquerir_cible(cible, type_cible)
                        return

    def jouer_prochain_coup(self):
        self.avancer_flotte()

    def avancer_flotte(self, chercher_nouveau=0):
        for i in self.flotte:
            for j in self.flotte[i]:
                j = self.flotte[i][j]
                rep = j.jouer_prochain_coup(chercher_nouveau)
                if rep:
                    if rep[0] == "Etoile":
                        # NOTE  est-ce qu'on doit retirer l'etoile de la liste du modele
                        #       quand on l'attribue aux etoilescontrolees
                        #       et que ce passe-t-il si l'etoile a un proprietaire ???
                        self.etoilescontrolees.append(rep[1])
                        self.parent.parent.afficher_etoile(self.nom, rep[1])
                    elif rep[0] == "Porte_de_ver":
                        pass


# IA- nouvelle classe de joueur
class IA(Joueur):
    def __init__(self, parent, nom, etoilemere, couleur):
        Joueur.__init__(self, parent, nom, etoilemere, couleur)
        self.cooldownmax = 1000
        self.cooldown = 20

    def jouer_prochain_coup(self):
        return
        # for i in self.flotte:
        #     for j in self.flotte[i]:
        #         j=self.flotte[i][j]
        #         rep=j.jouer_prochain_coup(1)
        #         if rep:
        #             self.etoilescontrolees.append(rep[1])
        self.avancer_flotte(1)

        if self.cooldown == 0:
            v = self.creervaisseau(["Eclaireur"])
            cible = random.choice(self.parent.etoiles)
            v.acquerir_cible(cible, "Etoile")
            self.cooldown = random.randrange(self.cooldownmax) + self.cooldownmax
        else:
            self.cooldown -= 1


class Modele():
    def __init__(self, parent, joueurs):
        self.parent = parent
        self.largeur = 9000
        self.hauteur = 9000
        self.nb_etoiles = int((self.hauteur * self.largeur) / 500000)
        self.joueurs = {}
        self.actions_a_faire = {}
        self.etoiles = []
        self.trou_de_vers = []
        self.cadre_courant = None
        self.creeretoiles(joueurs, 1)
        nb_trou = int((self.hauteur * self.largeur) / 5000000)
        self.creer_troudevers(nb_trou)

    def creer_troudevers(self, n):
        bordure = 10
        for i in range(n):
            x1 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y1 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            x2 = random.randrange(self.largeur - (2 * bordure)) + bordure
            y2 = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.trou_de_vers.append(Trou_de_vers(x1, y1, x2, y2))

    def creeretoiles(self, joueurs, ias=0):
        bordure = 10
        for i in range(self.nb_etoiles):
            x = random.randrange(self.largeur - (2 * bordure)) + bordure
            y = random.randrange(self.hauteur - (2 * bordure)) + bordure
            self.etoiles.append(Planete(Point(x, y)))
        np = len(joueurs) + ias
        etoile_occupee = []
        while np:
            p = random.choice(self.etoiles)
            if p not in etoile_occupee:
                etoile_occupee.append(p)
                self.etoiles.remove(p)
                np -= 1

        couleurs = ["red", "blue", "lightgreen", "yellow",
                    "lightblue", "pink", "gold", "purple"]
        for i in joueurs:
            etoile = etoile_occupee.pop(0)
            self.joueurs[i] = Joueur(self, i, etoile, couleurs.pop(0))
            x, y = etoile.position
            usine: Usine = Usine()
            etoile.ajouter_batiment(usine)
            dist = 500
            for e in range(5):
                x1 = random.randrange(x - dist, x + dist)
                y1 = random.randrange(y - dist, y + dist)
                self.etoiles.append(Planete(Point(x1, y1)))

        # IA- creation des ias
        couleursia = ["orange", "green", "cyan",
                      "SeaGreen1", "turquoise1", "firebrick1"]
        for i in range(ias):
            self.joueurs["IA_" + str(i)] = IA(self, "IA_" + str(i), etoile_occupee.pop(0), couleursia.pop(0))
        print(self.joueurs)

    ##############################################################################
    def jouer_prochain_coup(self, cadre):
        #  NE PAS TOUCHER LES LIGNES SUIVANTES  ################
        self.cadre_courant = cadre
        # insertion de la prochaine action demandée par le joueur
        if cadre in self.actions_a_faire:
            for i in self.actions_a_faire[cadre]:
                self.joueurs[i[0]].actions[i[1]](i[2])
                """
                i a la forme suivante [nomjoueur, action, [arguments]
                alors self.joueurs[i[0]] -> trouve l'objet représentant le joueur de ce nom
                """
            del self.actions_a_faire[cadre]
        # FIN DE L'INTERDICTION #################################

        # demander aux objets de jouer leur prochain coup
        # aux joueurs en premier
        for joueur in self.joueurs:
            self.joueurs[joueur].jouer_prochain_coup()
            for planete in self.joueurs[joueur].etoilescontrolees:
                planete.produire_ressources()

        # NOTE si le modele (qui représent.keyse l'univers !!! )
        #      fait des actions - on les activera ici...
        for i in self.trou_de_vers:
            i.jouer_prochain_coup()
            

    def creer_bibittes_spatiales(self, nb_biittes=0):
        pass

    #############################################################################
    # ATTENTION : NE PAS TOUCHER
    def ajouter_actions_a_faire(self, actionsrecues):
        cadrecle = None
        for i in actionsrecues:
            cadrecle = i[0]
            if cadrecle:
                if (self.parent.cadrejeu - 1) > int(cadrecle):
                    print("PEUX PASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
                action = ast.literal_eval(i[1])

                if cadrecle not in self.actions_a_faire.keys():
                    self.actions_a_faire[cadrecle] = action
                else:
                    self.actions_a_faire[cadrecle].append(action)
    # NE PAS TOUCHER - FIN
##############################################################################
