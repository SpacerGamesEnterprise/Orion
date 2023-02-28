from modeles.batiment import Ferme, Hangar, Mine
from modeles.planete import Planete
from modeles.position import Point
from modeles.ressources import Ressources
from modeles.vaisseau import Eclaireur


p1: Planete = Planete(10, 100000)

b1: Hangar = Hangar()

p1.inventaire_ressources += Ressources(1500,1500,1500,1500,1500)

p1.ajouter_batiment(b1)


print(p1.batiments[0].nom)

v1: Eclaireur = Eclaireur("mathis", Point(10,20))

p1.inventaire_ressources = b1.creer_vaisseau(v1, p1.inventaire_ressources, p1.vaisseaux)

print(p1.vaisseaux[0].nom_vaisseau)

p1.inventaire_ressources += Ressources(1500,1500,1500,1500,1500)


p1.inventaire_ressources = b1.ameliorer(p1.inventaire_ressources)

print(b1.niveau)


b2: Ferme = Ferme()

p1.ajouter_batiment(b2)

p1.inventaire_ressources = b2.ameliorer(p1.inventaire_ressources)

b3: Mine = Mine()

p1.ajouter_batiment(b3)

print(p1.inventaire_ressources)

p1.produire_ressources() 

print(p1.inventaire_ressources)



