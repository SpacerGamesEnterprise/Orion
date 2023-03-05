from abc import ABC
from ctypes import WinDLL
from dis import dis
from doctest import master
import tkinter as tk

from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math

#import temporaire
from orion_modele import *

import random



# Actual imports from here
from abc import ABC

import os.path

import tkinter as tk
from PIL import Image, ImageTk


def img_format(file: str) -> tk.PhotoImage:
    img = Image.open(file)
    img = img.convert('RGBA')
    data = img.getdata()

    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 0:  # finding yellow colour
            # replacing it with a transparent value
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return ImageTk.PhotoImage(img)

def img_resize(file:str, dimensions: tuple[int, int]) -> tk.PhotoImage:
    img = Image.open(file)
    img = img.resize(dimensions)
    
    return ImageTk.PhotoImage(img)

def getimg(name: str) -> str:
    """Retourne le liens vers l'image demandée"""
    return os.path.join(os.path.dirname(__file__), "graphics", name)

class Vue(ABC):
    def __init__(self, master: tk.Widget):
        self.master = master
        self.main_frame = tk.Frame(master)
        self.url_serveur = "http://127.0.0.1:8000"

    def afficher(self):
        """Méthode d'affichage de la vue"""
        self.main_frame.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor=tk.CENTER)

    def destroy(self):
        """Méthode de destruction de la vue"""
        self.main_frame.forget()

    def forget(self):
        """Méthode d'oublie de la vue"""
        for content in self.main_frame.winfo_children():
            content.pack_forget()
        self.main_frame.pack_forget()

class VueSplash(Vue):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.master.geometry("800x800")
        self.background_width = 800
        self.background_height = 800

        self.main_canvas = tk.Canvas(
            self.main_frame,
            width=self.background_width,
            height=self.background_height,
            highlightthickness=0)
            
        self.background_img = img_resize(
            "Orion_client/graphics/menuBackground.png", (self.background_width,
                                        self.background_height)
        )
        self.background = self.main_canvas.create_image(
            self.background_width/2, self.background_height/2,
            image=self.background_img)
        self.bouton_connecter = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height/2,
            self.background_width/2+100, self.background_height/2+50,
            fill="black")
        self.bouton_creer_partie = self.main_canvas.create_rectangle(
            self.background_width/4-150, self.background_height-100,
            self.background_width/4+50, self.background_height-50,
            fill="blue")
        self.bouton_inscrire_joueur = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height-100,
            self.background_width/2+100, self.background_height-50,
            fill="blue")
        self.bouton_reinitialiser_partie = self.main_canvas.create_rectangle(
            ((self.background_width/4)*3)-50, self.background_height-100,
            ((self.background_width/4)*3)+150, self.background_height-50,
            fill="blue"
        )
        self.message = self.main_canvas.create_text(
            self.background_width/2, self.background_height/5,
            text="Non connecté", font=('Helvetica 15 bold'),fill="white"
        )
        self.bouton_reinitialiser_partie_message = self.main_canvas.create_text(
            ((self.background_width/4)*3)+50, self.background_height-75,
            text="Reinitialiser partie", font=('Helvetica 10 bold'),fill="white"
        )
        self.bouton_rejoindre_partie_message = self.main_canvas.create_text(
            self.background_width/2, self.background_height-75,
            text="Rejoindre partie", font=('Helvetica 10 bold'),fill="white"
        )
        self.bouton_connecter_message = self.main_canvas.create_text(
            self.background_width/2, self.background_height/2+25,
            text="Connecter", font=('Helvetica 10 bold'),fill="white"
        )
        self.bouton_creer_partie_message = self.main_canvas.create_text(
            self.background_width/4-50, self.background_height-75,
            text="Creer partie", font=('Helvetica 10 bold'),fill="white"
        )
        #Essaie pour lier les boutons avec les canvas
        #self.bouton_creer_partie = tk.Button(text=self.bouton_creer_partie_message, width=self.background_width, height=self.background_height,
        #    bg="blue", command=v.creer_partie)


        self.value_nom = tk.StringVar()
        self.value_url = tk.StringVar()

        self.input_nom = tk.Entry(
            self.main_frame,
            textvariable=self.value_nom,
            font=('Helvetica 20 bold'))

        self.input_url = tk.Entry(
            self.main_frame,
            textvariable=self.value_url,
            font=('Helvetica 20 bold'))
        


        self.main_canvas.place(x=0,y=0)

        self.input_nom.place(x=self.background_width/2-200,y=self.background_height/4,
                             width=400,height=50)
        
        self.input_url.place(x=self.background_width/2-200,y=self.background_height/4+100,
                             width=400,height=50)     

class VueLobby(Vue):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.background_width = 800
        self.background_height = 800

        self.main_canvas = tk.Canvas(
            self.main_frame,
            width=self.background_width,
            height=self.background_height,
            highlightthickness=0)
        self.background_img = img_resize(
            "Orion_client/graphics/menuBackground.png",
            (2000,2000)
        )

        self.background = self.main_canvas.create_image(
            self.background_width/2, self.background_height/2,
            image=self.background_img)
        self.bouton_commencer = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height-200,
            self.background_width/2+100, self.background_height-150,
            fill="black")
        
        self.text_commencer = self.main_canvas.create_text(
            self.background_width/2-15, self.background_height-175,
            text="Commencer Partie", font=('Helvetica 10 bold'),fill="white"
        )
        
        self.url = self.main_canvas.create_text(
            self.background_width*0.5,self.background_height*0.23,
            text="Joueurs", font=('Helvetica 15 bold'),fill="white" 
        )

        self.liste_lobby = tk.Listbox(self.main_frame,borderwidth=0)

        self.main_canvas.place(x=0,y=0)

        self.liste_lobby.place(relx=0.35,rely=0.25,relheight=0.4,relwidth=0.3)

    def update_lobby(self, dico):
        self.liste_lobby.delete(0, tk.END)
        for i in dico:
            self.liste_lobby.insert(tk.END, i[0])
        


    def afficher_joueurs(self, joueurs : list[str]):
           for joueur in joueurs:
                self.liste_lobby.insert(tk.END, joueur)               

class VueHUD(Vue):
    def __init__(self, master: tk.Widget,game_frame:tk.Frame,modele:Modele):
        super().__init__(master)
        
        self.main_frame = game_frame
        self.modele = modele
        self.background_width = 1200
        self.background_height = 800
        self.button_size = 50
        self.map_size = 9000
        self.minimap_size = 240
        self.ecart_minimap = 25
        self.cursor_height = 20
        self.cursor_width = 28

        self.cadre_h_width = self.background_width
        self.cadre_h_height = self.background_height * 0.1
        self.cadre_v_width = self.background_width * 0.2
        self.cadre_v_height = self.background_height * 0.9
        
        if(master!=None):
            master.geometry(f"{self.background_width}x{self.background_height}")
    
        self.minimap_button_img = img_resize(
            "Orion_client/graphics/minimapButton.png",
            (self.button_size,self.button_size)
        )
        self.minimap_background_img = img_resize(
            "Orion_client/graphics/gameBackground.png",
            (self.minimap_size,self.minimap_size)
        )

        self.minimap_button = tk.Label(
            self.main_frame,image=self.minimap_button_img,
            borderwidth=0,highlightthickness=2,
            highlightcolor="#525252"
        )

        self.minimap = tk.Canvas(
            self.main_frame,
            width=self.minimap_size, height=self.minimap_size,                      
            bg="#000000",highlightbackground ="#a48dc2"
        )
        self.minimap_background = self.minimap.create_image(
            self.minimap_size/2,self.minimap_size/2,
            image = self.minimap_background_img,
        )
        self.minimap_cursor = self.minimap.create_rectangle(
            0,0,
            self.cursor_width,self.cursor_height,
            width=2,outline="#a48dc2",dash=(5, 1, 2, 1)
        )
        self.cadre_outils_h = tk.Canvas(
            self.main_frame, bg="darkgrey",
            highlightthickness="3",
            highlightbackground="#525252"
        )
        self.cadre_outils_v = tk.Canvas(
            self.main_frame, bg="darkgrey",
            highlightthickness="3",
            highlightbackground="#525252"
        )
        self.cadre_info = tk.Canvas(
            self.cadre_outils_v,
            width=200, height=200,
            bg="#525252", highlightthickness="3",
            highlightbackground="darkgrey"
        )
        self.minimap.place(
            x=(self.background_width-self.minimap_size-self.ecart_minimap),
            y=self.ecart_minimap
        )
        self.cadre_outils_h.place(x=0,rely=0.9,relheight=0.1,relwidth=1)
        self.cadre_outils_v.place(x=0,y=0,relheight=0.9,relwidth=0.2)
        self.cadre_info.pack(fill=tk.BOTH)

        self.load_menu_planete()
        self.load_menu_vaisseau()
        
    def load_menu_planete(self):
        self.bouton_batiment = tk.Button(self.cadre_outils_h,
            width= 10,height = 10,
            text="Construire Batiment",
            font=('Helvetica 8 bold')
        )

        self.bouton_cargo = tk.Button(self.cadre_outils_h, #Temporaire
            text="Cargo",
            font=('Helvetica 8 bold')
        )
        self.bouton_eclaireur = tk.Button(self.cadre_outils_h, #Temporaire
            text="Eclaireur",
            font=('Helvetica 8 bold')
        )
        self.bouton_combat = tk.Button(self.cadre_outils_h, #Temporaire
            text="Combat",
            font=('Helvetica 8 bold')
        )

        self.info_planete = tk.Canvas(
            self.cadre_outils_v, 
            width= int(self.cadre_v_width), 
            height = int(self.cadre_v_height), 
            bg="black"
        )

        self.ressources_planete = self.info_planete.create_text(
            self.cadre_v_width/2, 
            self.cadre_v_height/11,
            font=('Helvetica 10 bold'),
            fill="white" 
        )

        self.info_sup_planete = self.info_planete.create_text(
            self.cadre_v_width/2, 
            self.cadre_v_height/2,
            font=('Helvetica 10 bold'),
            fill="white"
        )

        self.liste_batiments = self.info_planete.create_text(
            self.cadre_v_width/2, 
            self.cadre_v_height/5,
            font=('Helvetica 10 bold'),
            fill="white"
        )


    def update_info_planete(self, planete: Planete):
        string_batiments: str = ""

        for batiment in planete.batiments:
            string_batiments = string_batiments  + "\n" + batiment.nom + " Niveau : " + str(batiment.niveau)

        self.info_planete.itemconfig(self.liste_batiments,
            text=" Batiments: " +  "\n" + string_batiments)

        self.info_planete.itemconfig(self.info_sup_planete,
            text=" Limite batiments: " + 
                    str(len(planete.batiments)) + 
                    "/" +
                    str(planete.limite_batiment)
                )
        
        self.info_planete.itemconfig(self.ressources_planete,
            text=" Metal: " + 
                str(planete.inventaire_ressources["metal"]) +
                "/" +
                str(planete.max_inventaire["metal"]) + 
                "\n Bois: " +
                str(planete.inventaire_ressources["bois"]) +
                "/" +
                str(planete.max_inventaire["bois"]) + 
                "\n Energie: " +
                str(planete.inventaire_ressources["energie"]) +
                "/" +
                str(planete.max_inventaire["energie"]) + 
                "\n Nourriture: " +
                str(planete.inventaire_ressources["nourriture"]) +
                 "/" +
                str(planete.max_inventaire["nourriture"]) + 
                "\n Population: " +
                str(planete.inventaire_ressources["population"]) +
                 "/" +
                str(planete.max_inventaire["population"]), 
        )

    def load_menu_vaisseau(self):
        self.ressources_vaisseau = self.info_planete.create_text(
            self.cadre_v_width/2, 
            self.cadre_v_height/11,
            font=('Helvetica 10 bold'),
            fill="white" 
        )

    def afficher_menu_planete(self, planete: Planete):
        self.bouton_batiment.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.8)
        self.bouton_eclaireur.place(relx=0.31, rely=0.1, relwidth=0.1, relheight=0.8)
        self.bouton_cargo.place(relx=0.42, rely=0.1, relwidth=0.1, relheight=0.8)
        self.bouton_combat.place(relx=0.53, rely=0.1, relwidth=0.1, relheight=0.8)
        self.update_info_planete(planete)
        self.info_planete.pack()

    def afficher_menu_vaisseau(self):
        pass

    def afficher_info_joueur(self, nom: str):
        self.nom = self.cadre_info.create_text(
            50, 20,
            text=nom, font=('Helvetica 10'),fill="white"
        )

    def afficher_mini_cosmos(self):  # univers(self, mod):
        for j in self.modele.etoiles:
            minix = j.x / self.modele.largeur * self.minimap_size
            miniy = j.y / self.modele.hauteur * self.minimap_size
            self.minimap.create_rectangle(
                minix, miniy, minix + 3, miniy + 3,
                fill="#FFFFFF",
                tags=("mini", "Etoile")
            )
        for i in self.modele.joueurs.keys():
            for j in self.modele.joueurs[i].etoilescontrolees:
                minix = j.x / self.modele.largeur * self.minimap_size
                miniy = j.y / self.modele.hauteur * self.minimap_size
                self.minimap.create_rectangle(
                    minix, miniy, minix + 5, miniy + 5,
                    fill=self.modele.joueurs[i].couleur,
                    tags=(j.proprietaire, str(j.id), "Etoile")
                )
    
    def mini_clic(self,e):
        self.minimap.delete(self.minimap_cursor)
        self.minimap_cursor = self.minimap.create_rectangle(
            e.x-self.cursor_width/2,e.y - self.cursor_height/2,
            e.x+self.cursor_width/2,e.y + self.cursor_height/2,
            width=2,outline="#a48dc2",dash=(5, 1, 2, 1)
        )
    
    def reposition_cursor(self,move_x,move_y):
        cursor_move_x = (move_x / self.map_size)*self.minimap_size
        cursor_move_y = (move_y / self.map_size)*self.minimap_size
        self.minimap.move(self.minimap_cursor,cursor_move_x,cursor_move_y)


    def cacher_mini(self,e):
        self.minimap.place_forget()
        self.minimap_button.place(
            x=self.background_width-self.button_size-self.ecart_minimap,y=self.ecart_minimap
        )
    
    def montrer_mini(self,e):
        self.minimap.place(
            x=(self.background_width-self.minimap_size-self.ecart_minimap),
            y=self.ecart_minimap
        )
        self.minimap_button.place_forget()
        
    
    

class VueCosmos(Vue):
    def __init__(self, master: tk.Widget,game_frame:tk.Frame,modele:Modele):
        super().__init__(master)
        
        self.main_frame = game_frame
        
        self.modele = modele
        self.background_width = 1200
        self.background_height = 800
        self.minimap_size = 240

        self.planet_diameter = 75
        self.color_planet_diameter = 75

        self.map_size = 9000#taille du canvas du cosmos
        self.max_map_size = 1500
        self.min_map_size = 1500
        
        #variables pour effet de profondeur
        self.background_x = self.background_width/2
        self.background_y = self.background_height/2
        self.zoom = 3

        self.load_images()
        
        self.canvas_cosmos = tk.Canvas(self.main_frame,
            height=self.map_size,width=self.map_size,
            bg = "black", borderwidth=0,highlightthickness=0,
            scrollregion=(0,0,self.map_size,self.map_size)
        )
        
        self.background = self.canvas_cosmos.create_image(
            self.max_map_size/2,self.max_map_size/2,
            image = self.background_image
        )
        
        self.scrollX = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL)
        self.scrollY = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)

        
        self.scrollX.pack(side=tk.BOTTOM,fill=tk.X)
        self.scrollY.pack(side=tk.LEFT,fill=tk.Y)
        self.canvas_cosmos.place(
            relx=0.18,rely=0,
            relheight=0.91,relwidth=0.82
        )
        
        
        self.scrollX.config(command=self.canvas_cosmos.xview)
        self.scrollY.config(command=self.canvas_cosmos.yview)
        
        self.canvas_cosmos.config(
            yscrollcommand=self.scrollX.set,
            xscrollcommand=self.scrollY.set
        )

        

    def load_images(self):
        self.planete_image = img_resize(
            "Orion_client/graphics/planet.png",
            (self.planet_diameter,self.planet_diameter)
        )
        self.planete_ai_image = img_resize(
            "Orion_client/graphics/planetAI.png",
            (self.planet_diameter,self.planet_diameter)
        )
        self.planete_orange_image = img_resize(
            "Orion_client/graphics/planetOrange.png",
            (self.planet_diameter,self.planet_diameter)
        )
        self.planete_rouge_image = img_resize(
            "Orion_client/graphics/planetRed.png",
            (self.planet_diameter,self.planet_diameter)
        )
        self.background_image = img_resize(
            "Orion_client/graphics/gameBackground.png",
            (self.max_map_size,self.max_map_size)
        )
        
    
    def do_zoom(self,e):

        initial_map_size = self.map_size
        x = self.canvas_cosmos.canvasx(self.background_width/2)
        y = self.canvas_cosmos.canvasy(self.background_height/2)
        factor = 1.001 ** e.delta
        self.map_size = self.map_size * factor
        zoom_valide=False
        if(self.map_size>self.max_map_size):self.map_size=self.max_map_size
        elif(self.map_size<self.min_map_size):self.map_size=self.min_map_size
        else: zoom_valide = True
            
        
        if(zoom_valide):
            self.canvas_cosmos.scale(tk.ALL, x, y, factor, factor)
        else: self.map_size = initial_map_size
        self.canvas_cosmos.config(scrollregion=(0,0,self.map_size,self.map_size))
        
    def centrer_clic(self, e):
        self.centrer_canvas(self.canvas_cosmos.canvasx(e.x),self.canvas_cosmos.canvasy(e.y))

    def mini_clic(self,e):
        x= e.x/self.minimap_size * self.map_size
        y= e.y/self.minimap_size * self.map_size
        self.centrer_canvas(x,y)

    def centrer_sur_objet(self,objet)->None:
        self.centrer_canvas(objet.x,objet.y)

    def centrer_background(self,x,y):
        move_x = x - self.background_x
        move_y = y - self.background_y
          
        move_background_x = (move_x /(self.map_size-self.background_width))*(self.map_size - self.max_map_size)
        move_background_y = (move_y /(self.map_size-self.background_height))*(self.map_size - self.max_map_size)
        
        self.canvas_cosmos.move(self.background, move_background_x , move_background_y)
        self.background_x = x
        self.background_y = y
    
    def centrer_canvas(self,x,y):
        self.centrer_background(x,y)

        x1 = (self.canvas_cosmos.winfo_width() / 2)#pas au centre de l'écran car il y a le HUD
        y1 = (self.canvas_cosmos.winfo_height() / 2)

        pctx = (x - x1) / self.map_size
        pcty = (y - y1) / self.map_size

        self.canvas_cosmos.xview_moveto(pctx)
        self.canvas_cosmos.yview_moveto(pcty)

        print("x:",x,",y:",y,"\nbx:",self.background_x,",by:",self.background_y)

    def afficher_decor(self): # TODO: faire un truc plus propre

        # affichage des etoiles
        for i in self.modele.etoiles:
            self.canvas_cosmos.create_image(i.x, i.y,
                image=self.planete_image,
                tags=(i.proprietaire, str(i.id), "Etoile",)
            )
        # affichage des etoiles possedees par les joueurs
        for i in self.modele.joueurs.keys():
            for j in self.modele.joueurs[i].etoilescontrolees:
                #si la planète/étoile affiché appartient à un AI
                if(str(i)[0:2] == "IA"):
                    self.canvas_cosmos.create_image(j.x,j.y,
                        image= self.planete_ai_image,
                        tags=(j.proprietaire, str(j.id), "Etoile")
                    )
                    self.canvas_cosmos.create_image(j.x,j.y,
                        image= self.planete_orange_image,
                        tags=(j.proprietaire, str(j.id), "Etoile")
                    ) 
                #si la planète/étoile affiché appartient à un Joueur
                else:
                    self.canvas_cosmos.create_image(j.x,j.y,
                        image= self.planete_image,
                        tags=(j.proprietaire, str(j.id), "Etoile")
                    )
                    self.canvas_cosmos.create_image(j.x,j.y,
                        image= self.planete_rouge_image,
                        tags=(j.proprietaire, str(j.id), "Etoile")
                    )

                
                
                
                
                # on affiche dans minimap
                #minix = j.x / self.modele.largeur * self.taille_minimap
                #miniy = j.y / self.modele.hauteur * self.taille_minimap
                #self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                #                                      fill=mod.joueurs[i].couleur,
                #                                      tags=(j.proprietaire, str(j.id), "Etoile"))
