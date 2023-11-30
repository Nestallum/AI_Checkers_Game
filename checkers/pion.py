import pygame as pyg
from .constantes import *

# Classe Pion qui représente un pion
class Pion:
    PADDING = 15
    CONTOUR = 4

    def __init__(self, ligne, col, couleur):
        self.ligne = ligne
        self.col = col
        self.couleur = couleur
        self.dame = False
        self.x = 0
        self.y = 0
        self.calculer_position()

    def calculer_position(self):
        self.x = TAILLE_CASE * self.col + TAILLE_CASE // 2 # on divise TAILLE_CASE par 2 pour être au milieu de la case
        self.y = TAILLE_CASE * self.ligne + TAILLE_CASE // 2

    def devenir_dame(self):
        self.dame = True
    
    def dessiner_pion(self, win):
        if(self.couleur == PION_BLANC):
            pion = pyg.image.load("checkers/assets/pion_blanc.png")
            win.blit(pion, (self.x-pion.get_width()//2, self.y-pion.get_width()//2))
        elif(self.couleur == PION_NOIR):
            pion = pyg.image.load("checkers/assets/pion_noir.png")
            win.blit(pion, (self.x-pion.get_width()//2, self.y-pion.get_width()//2))

        if self.dame:
            dame = pyg.image.load("checkers/assets/Dame.png")
            win.blit(dame, (self.x-dame.get_width()/2, self.y-dame.get_width()/2))
    
    def deplacer(self, ligne, col):
        self.ligne = ligne
        self.col = col
        self.calculer_position()
        
    # Représente le pion par sa couleur
    def __repr__(self):
        return str(self.couleur)
        

        