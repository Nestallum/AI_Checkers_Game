import pygame as pyg
from checkers.constantes import *
from checkers.jeu import Jeu
import sys

def main():
    clock = pyg.time.Clock() # Pour que le jeu s'éxécute à fréquence constante
    jeu = Jeu()

    jeu.menu(clock)
    #jeu.facile_vs_difficile(clock)
    #jeu.facile_vs_inter(clock)
    #jeu.difficile_vs_inter(clock)
    
main()

