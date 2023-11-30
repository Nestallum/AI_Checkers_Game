import pygame as pyg
# Fichier .py qui contient toutes les constantes du code
# Utile d'avoir un fichier à part afin de rapidement pouvoir accéder à nos constantes

# Définition de la hauteur et de la largeur du damier
LARGEUR = 800
HAUTEUR = 800

# Définition des lignes et des colonnes pour le damier
LIGNES = 8
COLS = 8

# Définition de la taille d'une case du damier
TAILLE_CASE = LARGEUR//COLS # équivalent à faire HAUTEUR//LIGNES


# valeur des couleurs des pions
PION_BLANC = (255, 255, 255) 
PION_NOIR = (0, 0, 0) 

# Couleur des indications
CONTOUR_CASE = (53, 83, 96)

# Taux d'images par secondes
FPS = 60

# Profondeur des IAs
PROFONDEUR_SIMPLE = 1
PROFONDEUR_INTER = 3
PROFONDEUR_DIFF = 5
