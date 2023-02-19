import tkinter as tk
from tkinter.simpledialog import *
from tkinter.messagebox import *
from helper import Helper as hlp
import math
from abc import ABC


import random

class Vue(ABC):
    def __init__(self, main_frame: tk.Frame, url_serveur: str):
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

class SplashVue(Vue):
    def __init__(self, main_frame: tk.Frame, url_serveur: str):
        super().__init__(main_frame, url_serveur)
        
        self.background_width = 800
        self.background_height = 800



        self.main_canvas = tk.Canvas(
            self.main_frame,
            width=self.background_width,
            height=self.background_height,
            highlightthickness=0)
        
        self.bouton_connecter = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height/2,
            self.background_width/2+100, self.background_height/2+50,
            fill="black")
        self.bouton_creer_partie = self.main_canvas.create_rectangle(
            self.background_width/4-150, self.background_height-100,
            self.background_width/4+50, self.background_height-50,
            fill="red")
        self.bouton_inscrire_joueur = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height-100,
            self.background_width/2+100, self.background_height-50,
            fill="blue")
        self.bouton_inscrire_joueur = self.main_canvas.create_rectangle(
            self.background_width/2-100, self.background_height-100,
            self.background_width/2+100, self.background_height-50,
            fill="blue")
        self.bouton_reinitialiser_partie = self.main_canvas.create_rectangle(
            ((self.background_width/4)*3)-50, self.background_height-100,
            ((self.background_width/4)*3)+150, self.background_height-50,
            fill="green"
        )
        self.message = self.main_canvas.create_text(
            self.background_width/2, self.background_height/5,
            text="Non connecté", font=('Helvetica 15 bold'),fill="black"
        )
        self.input_nom = tk.Text(main_frame, width=20, height=1,font=('Helvetica 30 bold'))

        self.input_url = tk.Text(main_frame, width=20, height=1,font=('Helvetica 30 bold'))
        self.main_canvas.place(x=0,y=0)
        self.input_nom.place(x=self.background_width/2-200,y=self.background_height/4,
                             width=400,height=50)
        self.input_url.place(x=self.background_width/2-200,y=self.background_height/4+100,
                             width=400,height=50)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.resizable(False,False)
    main_frame = tk.Frame(root)
    
    
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    vue = SplashVue(main_frame,"huidf")
    root.mainloop()