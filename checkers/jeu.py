import pygame as pyg
import sys
from checkers.damier import Damier
from .constantes import *
from IA.minimax import minimax, alpha_beta

class Jeu:
    def __init__(self):
        self._init() # Singleton

    def actualiser(self):
        self.damier.actualiser(self.win)
        self.dessiner_deplacements_valides(self.deplacements_valides)
        self.dessiner_pions_valides()
        pyg.display.update()
     
    def _init(self):
        self.win = None
        self.selected = None
        self.damier = Damier()
        self.tour = PION_NOIR # On commence la partie (en joueur contre IA, le joueur possède les pions noirs)
        self.deplacements_valides = {}
        self.prise_pion = False
        self.nb_tours = 0
        self.nb_pions_prec = self.nb_pion_cour = self.get_damier().blancs_restants +  self.get_damier().noirs_restants # nb de pions actuel
    
    def termine(self):
        return self.damier.jeu_termine()
    
    def affiche_gagnant(self):
        return self.damier.gagnant()
    
    def victoire_blocage(self, couleur): # Victoire par blocage => les pions adverses ne peuvent plus faire de mouvements légaux (on est bloqué)
        if couleur == PION_NOIR:
            print("Les pions noirs ne peuvent plus bouger. Victoire des pions blancs !")
        elif couleur == PION_BLANC:
            print("Les pions blancs ne peuvent plus bouger. Victoire des pions noirs !")

    def match_nul(self): # Si il n'y aucune prise au bout d'un certain nombre de répétitions => évite les parties infinies
        print("Match nul par limite de coups.")

    def limite_coup(self):
        self.nb_tours += 1
        self.nb_pion_cour = self.get_damier().blancs_restants +  self.get_damier().noirs_restants # nb de pions actuel
        if(self.nb_pion_cour < self.nb_pions_prec):
            self.prise_pion = True
        if(self.prise_pion):
            self.nb_tours = 0
            self.nb_pions_prec = self.nb_pion_cour
            self.prise_pion = False
        if(self.nb_tours == 500 and self.prise_pion == False):
            return True
        return False

    # Reset les attributs qui gèrent la limite de coups qui sert à éviter les parties interminables
    def reset_limite_coup(self):
        self.prise_pion = False
        self.nb_tours = 0
        self.nb_pions_prec = self.get_damier().blancs_restants +  self.get_damier().noirs_restants

    # Reset le jeu
    def reset(self): 
        self._init()

    def get_damier(self):
        return self.damier
    
    # Fonction appelée lors d'un clic sur une cases du damier
    # 2 possibilités :
    # - on vient de sélectionner un pion => fonction sélectionne le pion si c'est un pion allié
    # - un pion avait déjà été sélectionné donc on a cliqué sur une autre case => déplace le pion si la case est valide (appelle la méthode _deplacer()) 
    def select(self, ligne, col):
        if self.selected == None: # A ce stade, on vient de sélectionner quelque chose
            pion = self.damier.get_pion(ligne, col)
            if pion != 0 and pion.couleur == self.tour: #Si la case cliquée contient un pion de la bonne couleur
                self.selected = pion
                self.deplacements_valides = self.damier.get_deplacements_obligatoires(pion) #On récupère les déplacements possibles à partir de ce pion
                return True
            else:
                self.deplacements_valides = {}
        elif self.selected: # Si un pion est sélectionné
            resultat = self._deplacer(ligne, col)
            if not resultat: #Si le déplacement à échoué -> la case n'était pas valide
                self.selected = None
                self.select(ligne, col)
        return False

    # Sert à déplacer un pion sélectionné sur le damier aux coordonnées ligne, col
    def _deplacer(self, ligne, col):
        pion = self.damier.get_pion(ligne, col)
        if self.selected and pion == 0 and (ligne, col) in self.deplacements_valides: #Si un pion est bien sélectionné et le case cliquée est vide et les coordonnées sont dans le damier
            self.damier.deplacer(self.selected, ligne, col)
            pions_parcourus = self.deplacements_valides[(ligne, col)]
            if pions_parcourus:
               self.damier.supprimer(pions_parcourus)
            self.changer_tour()
            
        else:
            return False

        return True
    
    # Effectue le "déplacement" de l'ia
    # En fait, le déplacement a déjà été effectué lors du calcul des coups possible et l'ia a choisi le meilleur coup à faire => on obtient un nouvel état
    def deplacement_IA(self, nouvel_etat):
        self.damier = nouvel_etat # On change l'état du damier
        self.changer_tour()
    
    def joueur_bloque(self, couleurJoueur):
        joueur_bloque = True
        etat_courant = self.get_damier()
        for pion in etat_courant.get_all_pions(couleurJoueur):
            deplacements_valides = etat_courant.get_deplacements_valides(pion)
            if(deplacements_valides):
                joueur_bloque =  False
        if joueur_bloque:
            return True
        return False
    
    # Dessine un petit cercle aux endroits où un déplacement est possible
    def dessiner_deplacements_valides(self, deplacements):
        for deplacement in deplacements:
            ligne, col = deplacement
            point = pyg.image.load("checkers/assets/point.png")
            point = pyg.transform.scale(point, (point.get_width(), point.get_width()))
            self.win.blit(point, (col * TAILLE_CASE, ligne * TAILLE_CASE))

    # Dessine un contour sur les cases des pions qui peuvent se déplacer
    def dessiner_pions_valides(self):
        cote_carre = LARGEUR / COLS
        for pion in self.get_damier().get_all_pions(self.tour):
            if(self.get_damier().get_deplacements_obligatoires(pion) != {}):
                pyg.draw.rect(self.win, CONTOUR_CASE, [pion.x-cote_carre//2, pion.y-cote_carre//2, cote_carre, cote_carre], 3)

    def changer_tour(self):
        self.deplacements_valides = {} # Reset les déplacements valides
        if self.tour == PION_NOIR:
            self.tour = PION_BLANC
        elif self.tour == PION_BLANC:
            self.tour = PION_NOIR

    def get_ligne_col_souris(self, pos):
        x, y = pos
        ligne = y // TAILLE_CASE
        col = x // TAILLE_CASE
        return ligne, col
    
    def menu(self, clock):
        self.reset() # reset le jeu à chaque nouvel appel du menu

        # Affichage des éléments du menu
        print("\n***** Menu du jeu : Dames anglo-americaines *****")
        print("1- JOUEUR VS JOUEUR")
        print("2- JOUEUR VS IA")
        print("3- IA VS IA")
        print("4- Quitter")
        try:
            sys.stdin.flush()
            choix = int(input("Quel mode de jeu voulez-vous choisir ?"))    
        except (ValueError):
            print("Veuillez entrer une valeur.")
            self.menu(clock)

        # choix du mode de jeu
        match choix:
            case 1: self.joueur_vs_joueur(clock)
            case 2: self.joueur_vs_ia(clock)
            case 3: self.ia_vs_ia(clock)
            case 4: return
            case _: print("Mode de jeu invalide.\n"), self.menu(clock)

    # fonction qui fait jouer deux joueurs l'un contre l'autre
    def joueur_vs_joueur(self, clock):
        self.win = pyg.display.set_mode((LARGEUR, HAUTEUR))
        pyg.display.set_caption("Dames anglo-américaines : JOUEUR VS JOUEUR")
        print("\n***** JOUEUR VS JOUEUR *****")

        # Partie en cours
        while(True):
            clock.tick(FPS)
            for event in pyg.event.get():
                if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                    print("Fin de partie.")
                    pyg.quit()
                    sys.exit()
                # Le joueur joue
                if event.type == pyg.MOUSEBUTTONDOWN: # clic de la souris
                    pos = pyg.mouse.get_pos()
                    ligne, col = self.get_ligne_col_souris(pos)
                    if(self.joueur_bloque(self.tour)):
                        self.victoire_blocage(self.tour)
                        pyg.time.delay(5000)
                        pyg.quit()
                        break
                    self.select(ligne, col)

            if self.termine():
                print(self.affiche_gagnant())
                pyg.time.delay(5000)
                pyg.quit()
                break

            self.actualiser() # on actualise à chaque tour de boucle

        self.menu(clock) # rappel du menu après la partie
    
    # fonction qui fait jouer un joueur contre une intelligence artificielle
    def joueur_vs_ia(self, clock):
        self.reset_limite_coup()
        # choix IA
        print("\n***** JOUEUR VS IA *****")
        print("Difficulté IA :")        
        print("1- IA facile")
        print("2- IA intermediaire")
        print("3- IA difficile")
        try:
            choix = int(input("Faite votre choix :"))
        except (ValueError):
            print("Veuillez entrer une valeur.")
            self.joueur_vs_ia(clock)

        difficulte_IA1 = None
        profondeur = 0

        match choix:
            case 1: profondeur, difficulte_IA1 = PROFONDEUR_SIMPLE, "Facile"
            case 2: profondeur, difficulte_IA1 = PROFONDEUR_INTER, "Intermédiaire"
            case 3: profondeur, difficulte_IA1 = PROFONDEUR_DIFF, "Difficile"
            case _: print("Choix invalide.\n"), self.joueur_vs_ia(clock)

        evaluation_IA = profondeur
        print("\n***** Pions Blancs : IA", difficulte_IA1, "VS Pions Noirs : Joueur *****")
        self.win = pyg.display.set_mode((LARGEUR, HAUTEUR))
        pyg.display.set_caption("Dames anglo-américaines : IA VS JOUEUR")

        # Partie en cours
        while(True):
            clock.tick(FPS)
            # Tour IA
            if self.tour == PION_BLANC: # C'est au tour de l'IA
                if(difficulte_IA1 == "Facile" or difficulte_IA1 == "Intermédiaire"):
                    pyg.time.delay(500)
                if(self.joueur_bloque(PION_BLANC)):
                    self.victoire_blocage(PION_BLANC)
                    pyg.time.delay(5000)
                    pyg.quit()
                    break
                #_, nouvel_etat = minimax(self.get_damier(), profondeur, True, evaluation_IA1) # _ pour ignorer la valeur de retour correspondant au score final de minimax
                # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible
                _, nouvel_etat = alpha_beta(self.get_damier(), profondeur, float('-inf'), float('inf'), True, evaluation_IA)
                self.deplacement_IA(nouvel_etat) # le damier prend le nouvel état sélectionné par l'IA comme étant le meilleur coup
                if(self.limite_coup()):
                    self.match_nul()
                    pyg.time.delay(5000)
                    pyg.quit()
                    break

            # Tour Joueur
            for event in pyg.event.get(): 
                if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                    print("Fin de partie.")
                    pyg.quit()
                    sys.exit()
            #Pour faire jouer un joueur
                if event.type == pyg.MOUSEBUTTONDOWN:
                    pos = pyg.mouse.get_pos()
                    ligne, col = self.get_ligne_col_souris(pos)
                    if(self.joueur_bloque(self.tour)):
                        self.victoire_blocage(self.tour)
                        pyg.time.delay(5000)
                        pyg.quit()
                        break
                    self.select(ligne, col)
            

            # Test si partie est terminée        
            if self.termine():
                print(self.affiche_gagnant())
                pyg.time.delay(5000)
                pyg.quit()
                break

            self.actualiser() # on actualise à chaque tour de boucle

        self.menu(clock) # rappel du menu après la partie

    # fonction qui fait jouer deux IAs entre-elles
    def ia_vs_ia(self, clock):
        self.reset_limite_coup()
        # choix difficulté
        print("\n***** IA VS IA *****")
        print("Difficulté IA-1 (Pions blancs) :")        
        print("1- IA facile")
        print("2- IA intermédiaire")
        print("3- IA difficile")
        try:
            choix = int(input("Faite votre choix :"))
        except (ValueError):
            print("Veuillez entrer une valeur.")
            self.ia_vs_ia(clock)
        profondeur_IA1 = 0
        difficulte_IA1 = None
        match choix:
            case 1: profondeur_IA1, difficulte_IA1 = PROFONDEUR_SIMPLE, "Facile"
            case 2: profondeur_IA1, difficulte_IA1 = PROFONDEUR_INTER, "Intermédiaire"
            case 3: profondeur_IA1, difficulte_IA1 = PROFONDEUR_DIFF, "Difficile"
            case _: print("Choix invalide."), self.ia_vs_ia(clock)

        print("\nDifficulté IA-2 (Pions noirs) :")        
        print("1- IA facile")
        print("2- IA intermédiaire")
        print("3- IA difficile")
        try:
            choix = int(input("Faite votre choix :"))
        except (ValueError):
            print("Veuillez entrer une valeur.")
            self.ia_vs_ia(clock)
        profondeur_IA2 = 0
        difficulte_IA2 = None
        match choix:
            case 1: profondeur_IA2, difficulte_IA2 = PROFONDEUR_SIMPLE, "Facile"
            case 2: profondeur_IA2, difficulte_IA2 = PROFONDEUR_INTER, "Intermédiaire"
            case 3: profondeur_IA2, difficulte_IA2 = PROFONDEUR_DIFF, "Difficile"
            case _: print("Choix invalide.\n"), self.ia_vs_ia(clock)
        
        evaluation_IA1 = profondeur_IA1
        evaluation_IA2 = profondeur_IA2

        # Affichage de la fenêtre
        print("\n***** Pions Blancs : IA", difficulte_IA1, "VS Pions Noirs : IA", difficulte_IA2, "*****")
        self.win = pyg.display.set_mode((LARGEUR, HAUTEUR))
        pyg.display.set_caption("Dames anglo-américaines : IA VS IA")

        # Déroulement de la partie, on sort de la boucle si la partie est terminée ou si match nul
        while(True):
            clock.tick(FPS)
            # Tour IA
            if self.tour == PION_BLANC: # C'est au tour de l'IA 1
                pyg.time.delay(250)
                if(self.joueur_bloque(PION_BLANC)): # Si l'IA est bloquée (ne peut plus se déplacer)
                    self.victoire_blocage(PION_BLANC)
                    pyg.time.delay(5000)
                    pyg.quit()
                    break
                #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA1, True, evaluation_IA1) # _ pour ignorer la valeur de retour correspondant au score final de minimax
                # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible
                _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA1, float('-inf'), float('inf'), True, evaluation_IA1)
                self.deplacement_IA(nouvel_etat) # le damier prend le nouvel état sélectionné par l'IA comme étant le meilleur coup
                if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                    self.match_nul()
                    pyg.time.delay(5000)
                    pyg.quit()
                    break
            
            elif self.tour == PION_NOIR: # C'est au tour de l'IA 2
                pyg.time.delay(250)
                if(self.joueur_bloque(PION_NOIR)): 
                    self.victoire_blocage(PION_NOIR)
                    pyg.time.delay(5000)
                    pyg.quit()
                    break
                #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA2, False, evaluation_IA2)
                # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible   
                _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA2, float('-inf'), float('inf'), False, evaluation_IA2)    
                self.deplacement_IA(nouvel_etat)
                if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                    self.match_nul()
                    pyg.time.delay(5000)
                    pyg.quit()
                    break

            # Si on a cliqué sur la croix
            for event in pyg.event.get():
                if event.type == pyg.QUIT: # si le joueur ferme la fenêtre
                    print("Fin de partie.")
                    pyg.quit()
                    sys.exit()

            # Si la partie est terminée
            if self.termine():
                print(self.affiche_gagnant())
                pyg.time.delay(5000)
                pyg.quit()
                break

            self.actualiser() # on actualise à chaque tour de boucle

        self.menu(clock) # rappel du menu après la partie


    # Boucles de plusieurs parties => Permet de tester les performances des IAs
    # IA FACILE VS IA DIFFICILE
    # IA FACILE VS IA INTER
    # IA INTER VS IA DIFFICILE

    def facile_vs_difficile(self, clock):
        compteur = 0
        victoires_blancs = 0
        victoires_noirs = 0
        nuls_limite_coups = 0

        while(compteur < 1000):
            compteur += 1
            self.reset_limite_coup()
            self.reset()
            # choix difficulté
            print("\n***** Pions Blancs : IA Difficile VS Pions Noirs : IA Facile *****")
            print("PARTIE NUMERO :", compteur)
            print("Victoires des blancs:", victoires_blancs)
            print("Victoires des noirs:", victoires_noirs)
            print("Nuls par limite de coups:", nuls_limite_coups)
            profondeur_IA1 = PROFONDEUR_DIFF
            profondeur_IA2 = PROFONDEUR_SIMPLE
            evaluation_IA1 = profondeur_IA1
            evaluation_IA2 = profondeur_IA2
            # Affichage de la fenêtre
            self.win = pyg.display.set_mode((LARGEUR, HAUTEUR))
            pyg.display.set_caption("Dames anglo-américaines : IA VS IA")

            # Déroulement de la partie, on sort de la boucle si la partie est terminée ou si match nul
            while(True):
                clock.tick(FPS)
                # Tour IA
                if self.tour == PION_BLANC: # C'est au tour de l'IA 1
                    #pyg.time.delay(250)
                    if(self.joueur_bloque(PION_BLANC)): # Si l'IA est bloquée (ne peut plus se déplacer)
                        self.victoire_blocage(PION_BLANC)
                        victoires_noirs += 1
                        pyg.time.delay(50)
                        pyg.quit()
                        break
                    #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA1, True) # _ pour ignorer la valeur de retour correspondant au score final de minimax
                    # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible
                    _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA1, float('-inf'), float('inf'), True, evaluation_IA1)
                    self.deplacement_IA(nouvel_etat) # le damier prend le nouvel état sélectionné par l'IA comme étant le meilleur coup
                    if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                        self.match_nul()
                        pyg.time.delay(5000)
                        pyg.quit()
                        break
                    
                elif self.tour == PION_NOIR: # C'est au tour de l'IA 2
                    #pyg.time.delay(250)
                    if(self.joueur_bloque(PION_NOIR)): 
                        self.victoire_blocage(PION_NOIR)
                        victoires_blancs += 1
                        pyg.time.delay(50)
                        pyg.quit()
                        break
                    #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA2, False)
                    # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible   
                    _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA2, float('-inf'), float('inf'), False, evaluation_IA2)    
                    self.deplacement_IA(nouvel_etat)
                    if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                        self.match_nul()
                        nuls_limite_coups += 1
                        pyg.time.delay(5000)
                        pyg.quit()
                        break

                # Si on a cliqué sur la croix
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        print("Fin de partie.")
                        pyg.quit()
                        sys.exit()

                # Si la partie est terminée
                if self.termine():
                    print(self.affiche_gagnant())
                    if(self.get_damier().noirs_restants == 0):
                        victoires_blancs += 1
                    else:
                        victoires_noirs += 1
                    pyg.time.delay(50)
                    pyg.quit()
                    break

                self.actualiser()
        print("\n***** Pions Blancs : IA Difficile VS Pions Noirs : IA Facile *****")
        print("Total victoires des blancs:", victoires_blancs)
        print("Total victoires des noirs:", victoires_noirs)
        print("Nuls par limite de coups :", nuls_limite_coups)


    def difficile_vs_inter(self, clock):
        compteur = 0
        victoires_blancs = 0
        victoires_noirs = 0
        nuls_limite_coups = 0

        while(compteur < 500):
            compteur += 1
            self.reset_limite_coup()
            self.reset()
            # choix difficulté
            print("\n***** Pions Blancs : IA Difficile VS Pions Noirs : IA Intermédiaire *****")
            print("PARTIE NUMERO :", compteur)
            print("Victoires des blancs:", victoires_blancs)
            print("Victoires des noirs:", victoires_noirs)
            print("Nuls par limite de coups:", nuls_limite_coups)
            profondeur_IA1 = PROFONDEUR_DIFF
            profondeur_IA2 = PROFONDEUR_INTER
            evaluation_IA1 = profondeur_IA1
            evaluation_IA2 = profondeur_IA2
            # Affichage de la fenêtre
            self.win = pyg.display.set_mode((LARGEUR, HAUTEUR))
            pyg.display.set_caption("Dames anglo-américaines : IA VS IA")

            # Déroulement de la partie, on sort de la boucle si la partie est terminée ou si match nul
            while(True):
                clock.tick(FPS)
                # Tour IA
                if self.tour == PION_BLANC: # C'est au tour de l'IA 1
                    #pyg.time.delay(250)
                    if(self.joueur_bloque(PION_BLANC)): # Si l'IA est bloquée (ne peut plus se déplacer)
                        self.victoire_blocage(PION_BLANC)
                        victoires_noirs += 1
                        pyg.time.delay(50)
                        pyg.quit()
                        break
                    #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA1, True) # _ pour ignorer la valeur de retour correspondant au score final de minimax
                    # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible
                    _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA1, float('-inf'), float('inf'), True, evaluation_IA1)
                    self.deplacement_IA(nouvel_etat) # le damier prend le nouvel état sélectionné par l'IA comme étant le meilleur coup
                    if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                        self.match_nul()
                        nuls_limite_coups += 1
                        pyg.time.delay(5000)
                        pyg.quit()
                        break

                elif self.tour == PION_NOIR: # C'est au tour de l'IA 2
                    #pyg.time.delay(250)
                    if(self.joueur_bloque(PION_NOIR)): 
                        self.victoire_blocage(PION_NOIR)
                        victoires_blancs += 1
                        pyg.time.delay(50)
                        pyg.quit()
                        break
                    #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA2, False)
                    # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible   
                    _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA2, float('-inf'), float('inf'), False, evaluation_IA2)    
                    self.deplacement_IA(nouvel_etat)
                    if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                        self.match_nul()
                        nuls_limite_coups += 1
                        pyg.time.delay(5000)
                        pyg.quit()
                        break

                # Si on a cliqué sur la croix
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        print("Fin de partie.")
                        pyg.quit()
                        sys.exit()

                # Si la partie est terminée
                if self.termine():
                    print(self.affiche_gagnant())
                    if(self.get_damier().noirs_restants == 0):
                        victoires_blancs += 1
                    else:
                        victoires_noirs += 1
                    pyg.time.delay(50)
                    pyg.quit()
                    break

                self.actualiser()
        print("\n***** Pions Blancs : IA Difficile VS Pions Noirs : IA Intermédiaire *****")
        print("Total victoires des blancs:", victoires_blancs)
        print("Total victoires des noirs:", victoires_noirs)
        print("Nuls par limite de coups :", nuls_limite_coups)


    def facile_vs_inter(self, clock):
        compteur = 0
        victoires_blancs = 0
        victoires_noirs = 0
        nuls_limite_coups = 0
        while(compteur < 1000):
            compteur += 1
            self.reset_limite_coup()
            self.reset()
            # choix difficulté
            print("\n***** Pions Blancs : IA Intermédiaire VS Pions Noirs : IA Facile *****")
            print("PARTIE NUMERO :", compteur)
            print("Victoires des blancs:", victoires_blancs)
            print("Victoires des noirs:", victoires_noirs)
            print("Nuls par limite de coups:", nuls_limite_coups)

            profondeur_IA1 = PROFONDEUR_INTER
            profondeur_IA2 = PROFONDEUR_SIMPLE
            evaluation_IA1 = profondeur_IA1
            evaluation_IA2 = profondeur_IA2

            # Affichage de la fenêtre
            self.win = pyg.display.set_mode((LARGEUR, HAUTEUR))
            pyg.display.set_caption("Dames anglo-américaines : IA VS IA")

            # Déroulement de la partie, on sort de la boucle si la partie est terminée ou si match nul
            while(True):
                clock.tick(FPS)
                # Tour IA
                if self.tour == PION_BLANC: # C'est au tour de l'IA 1
                    #pyg.time.delay(250)
                    if(self.joueur_bloque(PION_BLANC)): # Si l'IA est bloquée (ne peut plus se déplacer)
                        self.victoire_blocage(PION_BLANC)
                        victoires_noirs += 1
                        pyg.time.delay(50)
                        pyg.quit()
                        break
                    #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA1, True) # _ pour ignorer la valeur de retour correspondant au score final de minimax
                    # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible
                    _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA1, float('-inf'), float('inf'), True, evaluation_IA1)
                    self.deplacement_IA(nouvel_etat) # le damier prend le nouvel état sélectionné par l'IA comme étant le meilleur coup
                    if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                        self.match_nul()
                        nuls_limite_coups += 1
                        pyg.time.delay(5000)
                        pyg.quit()
                        break
                
                elif self.tour == PION_NOIR: # C'est au tour de l'IA 2
                    #pyg.time.delay(250)
                    if(self.joueur_bloque(PION_NOIR)): 
                        self.victoire_blocage(PION_NOIR)
                        victoires_blancs += 1
                        pyg.time.delay(50)
                        pyg.quit()
                        break
                    #_, nouvel_etat = minimax(self.get_damier(), profondeur_IA2, False)
                    # Minimax nous renvoie l'état du damier qui nous donne le meilleur coup possible   
                    _, nouvel_etat = alpha_beta(self.get_damier(), profondeur_IA2, float('-inf'), float('inf'), False, evaluation_IA2)    
                    self.deplacement_IA(nouvel_etat)
                    if(self.limite_coup()): # vérifie s'il y a match nul par limite de coup
                        self.match_nul()
                        nuls_limite_coups += 1
                        pyg.time.delay(5000)
                        pyg.quit()
                        break

                # Si on a cliqué sur la croix
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        print("Fin de partie.")
                        pyg.quit()
                        sys.exit()

                # Si la partie est terminée
                if self.termine():
                    print(self.affiche_gagnant())
                    if(self.get_damier().noirs_restants == 0):
                        victoires_blancs += 1
                    else:
                        victoires_noirs += 1
                    pyg.time.delay(50)
                    pyg.quit()
                    break

                self.actualiser()
        print("\n***** Pions Blancs : IA Intermédiaire VS Pions Noirs : IA Facile *****")
        print("Total victoires des blancs:", victoires_blancs)
        print("Total victoires des noirs:", victoires_noirs)
        print("Nuls par limite de coups :", nuls_limite_coups)