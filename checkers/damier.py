import pygame as pyg
from .constantes import * 
from .pion import Pion

# Classe Damier qui représente le damier
class Damier :
    def __init__(self):
        # Représentation interne du damier
        self.damier = []

        # 12 pions de chaque couleur
        self.noirs_restants = self.blancs_restants = 12

        # Pas de dames au début du jeu
        self.dames_noires = self.dames_blanches = 0

        self.creer_damier()
    
    # Dessine les cases du damier sur la fenêtre
    def dessiner_cases(self, win):
        case_noire = pyg.image.load("checkers/assets/case_noire.png")
        case_blanche = pyg.image.load("checkers/assets/case_blanche.png")
        for ligne in range(LIGNES):
            for col in range(ligne % 2, LIGNES, 2):
                # On dessine une case sur deux claire (avec un décalage à chaque ligne -> ligne % 2 vaut 0 puis 1 et ainsi de suite)
                win.blit(case_blanche, (ligne*TAILLE_CASE, col*TAILLE_CASE))
            for col in range((ligne+1) % 2, LIGNES, 2):
                win.blit(case_noire, (ligne*TAILLE_CASE, col*TAILLE_CASE))

    # Créer la structure du damier et le remplit (un pion ou un 0 quand la case est vide)
    def creer_damier(self):
        for ligne in range(LIGNES):
            self.damier.append([]) # liste pour chaque ligne, qui contiendra les éléments de la ligne en question
            for col in range(COLS):
                if col % 2 == ((ligne + 1) % 2): 
                    if ligne < 3:
                        self.damier[ligne].append(Pion(ligne, col, PION_BLANC))
                    elif ligne > 4:
                        self.damier[ligne].append(Pion(ligne, col, PION_NOIR))
                    else:
                        self.damier[ligne].append(0) # case vide pour les lignes 3 et 4
                else:
                    self.damier[ligne].append(0) # case vide une fois sur 2

    # Échange le contenu de deux cases (un pion et une autre case) 
    def deplacer(self, pion, ligne, col):
        self.damier[pion.ligne][pion.col], self.damier[ligne][col] = self.damier[ligne][col], self.damier[pion.ligne][pion.col]
        pion.deplacer(ligne, col) # Change les coordonnées du pion par les nouvelles

        if ligne == LIGNES-1 or ligne == 0: # On atteint la ligne de Dame
            if(pion.couleur == PION_NOIR and ligne == 0 and pion.dame == False):
                pion.devenir_dame()
                self.dames_noires += 1 
            elif(pion.couleur == PION_BLANC and ligne == LIGNES-1 and pion.dame == False):
                pion.devenir_dame()
                self.dames_blanches += 1
    
    # Actualise l'affichage du damier (cases et pions)
    def actualiser(self, win):
        self.dessiner_cases(win)
        for ligne in range(LIGNES):
            for col in range(COLS):
                pion = self.damier[ligne][col]
                if pion != 0:
                    pion.dessiner_pion(win)

    # Fonction d'évaluation pour l'IA
    def evaluation_difficile(self):
        poids_pions = 5
        poids_dames = 2
        poids_prox_promo = 0.75
        poids_menaces = 0.50
        poids_bloque = -1
        nb_pions = (self.blancs_restants - self.noirs_restants) * poids_pions
        nb_dames = (self.dames_blanches - self.dames_noires) * poids_dames
        position_pions = self.evaluer_position_pions(poids_prox_promo, poids_menaces, poids_bloque)
        
        return nb_pions + nb_dames + position_pions
    
      # Fonction d'évaluation pour l'IA
    def evaluation_inter(self):
        poids_pions = 1
        poids_dames = 0.5
        nb_pions = (self.blancs_restants - self.noirs_restants) * poids_pions
        nb_dames = (self.dames_blanches - self.dames_noires) * poids_dames
        return nb_pions + nb_dames
    
     # Fonction d'évaluation pour l'IA
    def evaluation_facile(self):
        nb_pions = (self.blancs_restants - self.noirs_restants)
        return nb_pions
    
    def evaluer_position_pions(self, coeff_proximite_promotion, coeff_pions_menaces, coeff_chaine_bloquee):
        poids_proximite_promotion = coeff_proximite_promotion # proche de faire promotion Dame
        poids_pions_menaces = coeff_pions_menaces # nb de pions que l'on menace
        poids_chaine_bloquee = coeff_chaine_bloquee # des pions bloqués sont un inconvénient
        score = 0

        restants_blancs = self.blancs_restants
        restants_noirs = self.noirs_restants

        # Pions blancs cherchent à maximiser leur score
        for pion in self.get_all_pions(PION_BLANC):
            if pion.ligne > 4: # pion proche de la ligne de promotion
                score += poids_proximite_promotion
            cases = self.get_deplacements_obligatoires(pion)
            for case in cases.keys():
                if(len(cases[case]) > 0): # il y a un ennemi à manger
                    score += poids_pions_menaces
        pions_bloques = restants_blancs - self.pions_libres(PION_BLANC)
        score += pions_bloques * poids_chaine_bloquee 

        # Pions noirs cherchent => cherchent à minimiser leur score 
        for pion in self.get_all_pions(PION_NOIR):
            if pion.ligne < 3:
                score -= poids_proximite_promotion
            cases = self.get_deplacements_obligatoires(pion)
            for case in cases.keys():
                if(len(cases[case]) > 0):
                    score -= poids_pions_menaces
        pions_bloques = restants_noirs - self.pions_libres(PION_NOIR)
        score -= pions_bloques * poids_chaine_bloquee 
        return score

    def pions_libres(self, couleur):
        pions_libres = 0
        for pion in self.get_all_pions(couleur):
            if(self.get_deplacements_obligatoires(pion) != {}):
                pions_libres += 1
        return pions_libres
        
    # Permet de supprimer les pions mangés
    def supprimer(self, pions):
        for pion in pions:
            self.damier[pion.ligne][pion.col] = 0
            if pion.couleur == PION_NOIR:
                self.noirs_restants -= 1
            else:
                self.blancs_restants -=1

    # Détermine si une partie est terminée
    def jeu_termine(self):
        if(self.noirs_restants == 0 or self.blancs_restants == 0):
            return True
        return False
    
    # Notifie le gagnant
    def gagnant(self):
        if self.noirs_restants <= 0:
            return "Victoire des pions blancs !"
        elif self.blancs_restants <= 0:
            return "Victoire des pions noirs !"
        return None

    # retourne le pion aux coordonnées [ligne, col]
    def get_pion(self, ligne, col):
        return self.damier[ligne][col]
    
    # retourne tous les pions du damier de la couleur entrée en argument sous forme de liste
    def get_all_pions(self, couleur):
        pions = []
        for ligne in self.damier:
            for pion in ligne:
                if pion != 0 and pion.couleur == couleur:
                    pions.append(pion)
        return pions

    # Permet d'obtenir les déplacements valides du pion en paramètre
    def get_deplacements_valides(self, pion):
        deplacements = {} # dictionnaire dont la clé est un tuple (ligne et colonne) et la valeur de la clé est une liste de pions parcourus
        col_gauche = pion.col - 1
        col_droite = pion.col + 1
        ligne = pion.ligne
      
        if pion.couleur == PION_NOIR or pion.dame:
            deplacements.update(self._diagonale_gauche(ligne-1, max(ligne-3, -1), -1, pion.couleur, col_gauche)) # max(ligne-3, -1) pour aller jusqu'à 2 pions au dessus du notre où jusqu'à -1 exclu (bord supérieur du damier)
            deplacements.update(self._diagonale_droite(ligne-1, max(ligne-3, -1), -1, pion.couleur, col_droite))  
        if pion.couleur == PION_BLANC or pion.dame:
            deplacements.update(self._diagonale_gauche(ligne+1, min(ligne+3, LIGNES), 1, pion.couleur, col_gauche))
            deplacements.update(self._diagonale_droite(ligne+1, min(ligne+3, LIGNES), 1, pion.couleur, col_droite)) 
        
        #deplacements = self.deplacements_obligatoires(deplacements, pion.couleur)
        return deplacements
    
    # Détermine les déplacements obligatoires d'un pion (prise obligatoire)
    def get_deplacements_obligatoires(self, pion):
        deplacements_pion = self.get_deplacements_valides(pion)
        peut_manger = False
        
        # Calcule si au moins un pion du damier peut manger
        for pion in self.get_all_pions(pion.couleur):
            deplacements_autre_pion = self.get_deplacements_valides(pion)
            for deplacement_possible in deplacements_autre_pion.keys():
                if(len(deplacements_autre_pion[deplacement_possible]) > 0): # Il y a au moins un pion à manger
                    peut_manger = True
                    break
        
        if peut_manger:
            cases_vides = [] # Liste qui va servir à stocker les clé des déplacements "vides"
            # On peut parcourir à nouveau les déplacements et supprimer les déplacements vides (ceux où l'on ne mange pas)
            for deplacement_possible in deplacements_pion.keys():
                if(len(deplacements_pion[deplacement_possible]) == 0):
                    cases_vides.append(deplacement_possible)

            # On supprime chaque déplacement vide
            for deplacement in cases_vides:
                del deplacements_pion[deplacement]

        return deplacements_pion

    # Calcule les déplacements valides dans la diagonale gauche
    def _diagonale_gauche(self, debut, fin, pas, couleur, col_gauche, pions_parcourus = []):
        deplacements = {}
        pion_a_parcourir = []
        for ligne in range(debut, fin, pas):
            if col_gauche < 0: # colonne hors du damier
                break
            courant = self.damier[ligne][col_gauche] # on récupère le contenu de la case courante
            if courant != 0: # si courant est un pion
                if courant.couleur == couleur: # si courant est un pion allié
                    break
                pion_a_parcourir = [courant] # sinon, c'est un pion ennemi
            else: # sinon, courant est une case vide
                if pions_parcourus and not pion_a_parcourir: # si on a mangé un pion mais qu'il n'y a pas d'autre pion à parcourir => pas de sauts multiples
                    break
                elif pions_parcourus and pion_a_parcourir: # sinon, si on a rencontré un nouveau pion à parcourir => sauts multiples
                    deplacements[(ligne, col_gauche)] = pions_parcourus + pion_a_parcourir
                else: # sinon, saut simple
                    if pion_a_parcourir :
                        deplacements[(ligne, col_gauche)] = pion_a_parcourir
                        # on a mangé le pion, on regarde plus loin pour de potentiels sauts multiples (appels récursifs)
                        ligne_deb = ligne + pas
                        ligne_fin = self.calculer_ligne_fin(ligne, pas)
                        deplacements.update(self._diagonale_gauche(ligne_deb, ligne_fin, pas, couleur, col_gauche-1, pions_parcourus = pion_a_parcourir))
                        deplacements.update(self._diagonale_droite(ligne_deb, ligne_fin, pas, couleur, col_gauche+1, pions_parcourus = pion_a_parcourir))
                    else: # sinon, on saute sur une case vide
                        deplacements[(ligne, col_gauche)] = []
                    break
            col_gauche -= 1
        return deplacements
    
    # Calcule les déplacements valides dans la diagonale droite
    def _diagonale_droite(self, debut, fin, pas, couleur, col_droite, pions_parcourus = []):
        deplacements = {}
        pion_a_parcourir = []
        for ligne in range(debut, fin, pas):
            if col_droite >= COLS: # colonne hors du damier
                break
            courant = self.damier[ligne][col_droite] # on récupère le contenu de la case courante
            if courant != 0: # si courant est un pion
                if courant.couleur == couleur: # si courant est un pion allié
                    break
                pion_a_parcourir = [courant] # sinon, c'est un pion ennemi
            else: # sinon, courant est une case vide
                if pions_parcourus and not pion_a_parcourir: # si on a mangé un pion mais qu'il n'y a pas d'autre pion à parcourir => pas de sauts multiples
                    break
                elif pions_parcourus and pion_a_parcourir: # sinon, si on a rencontré un nouveau pion à parcourir => sauts multiples
                    deplacements[(ligne, col_droite)] = pions_parcourus + pion_a_parcourir
                else: # sinon, saut simple
                    if pion_a_parcourir :
                        deplacements[(ligne, col_droite)] = pion_a_parcourir
                        # on a mangé le pion, on regarde plus loin pour de potentiels sauts multiples (appels récursifs)
                        ligne_deb = ligne + pas
                        ligne_fin = self.calculer_ligne_fin(ligne, pas)
                        deplacements.update(self._diagonale_gauche(ligne_deb, ligne_fin, pas, couleur, col_droite-1, pions_parcourus = pion_a_parcourir))
                        deplacements.update(self._diagonale_droite(ligne_deb, ligne_fin, pas, couleur, col_droite+1, pions_parcourus = pion_a_parcourir))
                    else: # sinon, on saute sur une case vide
                        deplacements[(ligne, col_droite)] = []
                    break
            col_droite += 1
        return deplacements
    
    def calculer_ligne_fin(self, ligne, pas):
        if pas == -1:
            return max(ligne-3, -1)
        return min(ligne+3, LIGNES)
    
