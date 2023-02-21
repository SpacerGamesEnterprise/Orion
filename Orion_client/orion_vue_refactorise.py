import tkinter as tk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
from PIL import Image, ImageTk
import math
from abc import ABC
from orion_vue import Vue as v


import random

class Vue(ABC):
    def __init__(self,main_frame:tk.Frame, url_serveur: str):
        self.main_frame = main_frame
        self.url_serveur = url_serveur
    
    def destroy(self):
        """Méthode de destruction de la vue"""
        self.main_frame.forget()

    def forget(self):
        """Méthode d'oublie de la vue"""
        for content in self.main_frame.winfo_children():
            content.pack_forget()
        self.main_frame.pack_forget()

    def img_format(self,file: str, dimensions: tuple[int, int]) -> tk.PhotoImage:
        img = Image.open(file)
        img = img.resize(dimensions)
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

class VueSplash(Vue):
    def __init__(self, main_frame: tk.Frame, url_serveur: str):
        super().__init__(main_frame, url_serveur)
        self.background_width = 800
        self.background_height = 800

        self.main_canvas = tk.Canvas(
            self.main_frame,
            width=self.background_width,
            height=self.background_height,
            highlightthickness=0)
        self.background_img = self.img_format(
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
        self.input_nom = tk.Entry(
            self.main_frame,
            font=('Helvetica 20 bold'))

        self.input_url = tk.Entry(
            self.main_frame,
            font=('Helvetica 20 bold'))
        self.input_url.insert(0,self.url_serveur)


        self.main_canvas.place(x=0,y=0)

        self.input_nom.place(x=self.background_width/2-200,y=self.background_height/4,
                             width=400,height=50)
        
        self.input_url.place(x=self.background_width/2-200,y=self.background_height/4+100,
                             width=400,height=50)
        
        

class VueLobby(Vue):
    def __init__(self, main_frame: tk.Frame, url_serveur: str):
        super().__init__(main_frame, url_serveur)
        self.background_width = 800
        self.background_height = 800

        self.main_canvas = tk.Canvas(
            self.main_frame,
            width=self.background_width,
            height=self.background_height,
            highlightthickness=0)
        self.background_img = self.img_format(
            "Orion_client/graphics/menuBackground.png", (self.background_width,
                                        self.background_height)
        )
        self.background = self.main_canvas.create_image(
            self.background_width/2, self.background_height/2,
            image=self.background_img)
        self.bouton_connecter = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height-200,
            self.background_width/2+100, self.background_height-150,
            fill="black")

        self.url = self.main_canvas.create_text(
            self.background_width*0.5,self.background_height*0.23,
            text=self.url_serveur, font=('Helvetica 15 bold'),fill="white"
        )

        self.liste_lobby = tk.Listbox(self.main_frame,borderwidth=0)

        self.main_canvas.place(x=0,y=0)

        self.liste_lobby.place(relx=0.35,rely=0.25,relheight=0.4,relwidth=0.3)

    def afficher_joueurs(self, joueurs : list[str]):
           for joueur in joueurs:
                self.liste_lobby.insert(END, joueur)
                
class VuePartie(Vue):
    def __init__(self, main_frame: tk.Frame, url_serveur: str):
        super().__init__(main_frame, url_serveur)
        
        self.background_width = 1200
        self.background_height = 800
        
        self.taille_minimap = 240
        self.ecart_minimap = 25
        
        root.geometry(f"{self.background_width}x{self.background_height}")
        
        self.minimap = tk.Canvas(self.main_frame, width=self.taille_minimap, height=self.taille_minimap,
                                      bg="pink")
        #self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.minimap.place(x=(self.background_width-self.taille_minimap-self.ecart_minimap),y=self.ecart_minimap)
        self.cadreoutils_v = tk.Frame(self.main_frame, width=200, height=200, bg="darkgrey")
        self.cadreoutils_v.pack(side=LEFT, fill=Y)
        self.cadreoutils_h = tk.Frame(self.main_frame, width=75, height=75, bg="darkgrey")
        self.cadreoutils_h.pack(side=BOTTOM, fill=X)
        self.cadreinfo = tk.Frame(self.cadreoutils_v, width=200, height=200, bg="black")
        self.cadreinfo.pack(fill=BOTH)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.resizable(False,False)
    main_frame = tk.Frame(root)
    
    
    
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    #vue = VueLobby(main_frame,"http://127.0.0.1:8000")
    joueurs = ["joeyy","Pierrot601","xX_454DPuG_Xx"]
    #vue.afficher_joueurs(joueurs)
    
    
    #vue = VueSplash(main_frame,"http://127.0.0.1:8000")
    
    vue = VuePartie(main_frame, "http://127.0.0.1:8000")
    root.mainloop()