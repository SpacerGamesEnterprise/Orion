from abc import ABC
from ctypes import WinDLL
from dis import dis
from doctest import master
import tkinter as tk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
from PIL import Image, ImageTk
import math

#import temporaire
from orion_modele import *

import random


def img_format(file: str, dimensions: tuple[int, int]) -> tk.PhotoImage:
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
        self.background_img = img_format(
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
        self.input_url.insert(0, self.url_serveur)
        


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
            text=self.url_serveur, font=('Helvetica 15 bold'),fill="white"  # TODO: CHANGE URL
        )

        self.liste_lobby = tk.Listbox(self.main_frame,borderwidth=0)

        self.main_canvas.place(x=0,y=0)

        self.liste_lobby.place(relx=0.35,rely=0.25,relheight=0.4,relwidth=0.3)

    def afficher_joueurs(self, joueurs : list[str]):
           for joueur in joueurs:
                self.liste_lobby.insert(END, joueur)
                
class VueHUD(Vue):
    def __init__(self, master: tk.Widget,game_frame:tk.Frame):
        super().__init__(master)
        
        self.main_frame = game_frame
        
        self.background_width = 1200
        self.background_height = 800
        
        self.taille_minimap = 240
        self.ecart_minimap = 25
        
        root.geometry(f"{self.background_width}x{self.background_height}")
        
        self.minimap = tk.Canvas(self.main_frame, width=self.taille_minimap, height=self.taille_minimap,
                                      bg="#525252")
        #self.canevas_minimap.bind("<Button>", self.positionner_minicanevas)
        self.minimap.place(x=(self.background_width-self.taille_minimap-self.ecart_minimap),y=self.ecart_minimap)
        self.cadreoutils_h = tk.Frame(self.main_frame, width=75, height=75, bg="darkgrey", highlightthickness="3",highlightbackground="#525252")
        self.cadreoutils_h.place(x=0,rely=0.9,relheight=0.1,relwidth=1)
        self.cadreoutils_v = tk.Frame(self.main_frame, width=200, height=200, bg="darkgrey", highlightthickness="3",highlightbackground="#525252")
        self.cadreoutils_v.place(x=0,y=0,relheight=0.9,relwidth=0.2)
        
        self.cadreinfo = tk.Frame(self.cadreoutils_v, width=200, height=200, bg="#525252", highlightthickness="3",highlightbackground="darkgrey")
        self.cadreinfo.pack(fill=BOTH)
        
class VueCosmos(Vue):
    def __init__(self, master: tk.Widget,game_frame:tk.Frame):
        super().__init__(master)
        
        self.main_frame = game_frame
        
        self.background_width = 1200
        self.background_height = 80
        self.map_size = 9000
        self.zoom = 2
        
        self.modele = None #initialisé avec "initialiser_avec_modele"
        
        
        
        
        self.main_canvas = tk.Canvas(self.main_frame,
            height=self.map_size,width=self.map_size,
            bg="#2f2d38",
            scrollregion=(0,0,self.map_size,self.map_size))
        
        self.scrollX = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL)
        self.scrollY = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        
        self.scrollX.config(command=self.main_canvas.xview)
        self.scrollY.config(command=self.main_canvas.yview)
        self.main_canvas.config(yscrollcommand=self.scrollX.set,
            xscrollcommand=self.scrollY.set)
        

        
        self.scrollX.pack(side=tk.BOTTOM,fill=tk.X)
        self.scrollY.pack(side=tk.LEFT,fill=tk.Y)
        self.main_canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        
        
        #TEMP FOR DEBUG
        ##########################################################
        #
        #ZOOM NE FONCTIONNE PLUS ACAUSE DE CENTRER_COSMOS
        #
        #self.main_canvas.bind("<MouseWheel>", self.do_zoom)
        #
        self.main_canvas.bind("<Button-1>", self.centrer_cosmos )
        ##########################################################
        
    
    def do_zoom(self,e):
        x = self.main_canvas.canvasx(e.x)
        y = self.main_canvas.canvasy(e.y)
        factor = 1.001 ** e.delta
        self.main_canvas.scale(tk.ALL, x, y, factor, factor)   
        
    def centrer_cosmos(self, e):
        # permet de defiler l'écran jusqu'à cet objet
        x = self.main_canvas.canvasx(e.x)/4500
        y = self.main_canvas.canvasy(e.y)/4500
        
        self.main_canvas.xview_moveto(x)
        self.main_canvas.yview_moveto(y)
        
        
        print(x,y)
        print(self.scrollX.get()[0],self.scrollY.get()[0],"\n\n")
    
    def afficher_decor(self, mod): # TODO: faire un truc plus propre
        # on cree un arriere fond de petites etoieles NPC pour le look
        
        for i in range(len(mod.etoiles) * 50):
            x = random.randrange(int(mod.largeur))
            y = random.randrange(int(mod.hauteur))
            n = random.randrange(3) + 1
            col = random.choice(["LightYellow", "azure1", "pink"])
            self.main_canvas.create_oval(x, y, x + n, y + n, fill=col, tags=("fond",))
        # affichage des etoiles
        for i in mod.etoiles:
            t = i.taille * self.zoom
            self.main_canvas.create_oval(i.x - t, i.y - t, i.x + t, i.y + t,
                                     fill="grey80", outline=col,
                                     tags=(i.proprietaire, str(i.id), "Etoile",))
        # affichage des etoiles possedees par les joueurs
        for i in mod.joueurs.keys():
            for j in mod.joueurs[i].etoilescontrolees:
                t = j.taille * self.zoom
                self.main_canvas.create_oval(j.x - t, j.y - t, j.x + t, j.y + t,
                                         fill=mod.joueurs[i].couleur,
                                         tags=(j.proprietaire, str(j.id), "Etoile"))
                # on affiche dans minimap
                #minix = j.x / self.modele.largeur * self.taille_minimap
                #miniy = j.y / self.modele.hauteur * self.taille_minimap
                #self.canevas_minimap.create_rectangle(minix, miniy, minix + 3, miniy + 3,
                #                                      fill=mod.joueurs[i].couleur,
                #                                      tags=(j.proprietaire, str(j.id), "Etoile"))
                
    def initialiser_avec_modele(self, modele):
        #self.mon_nom = self.parent.mon_nom
        self.modele = modele
        self.main_canvas.config(scrollregion=(0, 0, modele.largeur, modele.hauteur))

        #self.labid.config(text=self.mon_nom)
        #self.labid.config(fg=self.modele.joueurs[self.mon_nom].couleur)

        self.afficher_decor(modele)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x800")
    root.resizable(False,False)
    game_frame = tk.Frame(root)
    
    # modele temporaire pour gameView
    modele = Modele(None, [])
    
    # vue = VueLobby(main_frame,"http://127.0.0.1:8000")
    joueurs = ["joeyy","Pierrot601","xX_454DPuG_Xx"]
    # vue.afficher_joueurs(joueurs)
    vueCosmos = VueCosmos(root,game_frame)
    #vueHUD = VueHUD(root,game_frame)
    
    
    
    
    
    vueCosmos.initialiser_avec_modele(modele)
    vueCosmos.afficher()
    
    #vueHUD.afficher()
    
    

    
    # vueCosmos.initialiser_avec_modele(modele)
    # vueCosmos.afficher_decor(modele)
    
    # game_frame.place(relx=0, rely=0,relheight=1,relwidth=1)
    root.mainloop()