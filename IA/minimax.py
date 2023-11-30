from copy import deepcopy
import random
from checkers import constantes

COULEUR_MAX = constantes.PION_BLANC
COULEUR_MIN = constantes.PION_NOIR

# Algo minimax explore tous les états possibles à partir d'un état courant, jusqu'à une profondeur donnée
def minimax(etat_courant, profondeur, joueur_Max, eval):
     # Condition d'arrêt
    if profondeur == 0 or etat_courant.jeu_termine():
        if(eval == constantes.PROFONDEUR_SIMPLE):
            return etat_courant.evaluation_facile(), etat_courant
        elif(eval == constantes.PROFONDEUR_INTER):
            return etat_courant.evaluation_inter(), etat_courant
        else:
            return etat_courant.evaluation_difficile(), etat_courant
    
    if joueur_Max:
        max_valeur = float('-inf')
        meilleurs_coups = [] # liste des coups de score max (il peut y en avoir plusieurs avec la même valeur max)
        # Pour chaque état possibles à partir d'un état courant
        etats_possibles = get_all_etats_possibles(etat_courant, COULEUR_MAX)
        for etat in etats_possibles:
            evaluation = minimax(etat, profondeur-1, False)[0] # On récupère seulement l'évaluation de l'état
            if evaluation >= max_valeur: # Si l'état à un meilleur score que l'ancienne max valeur
                if(evaluation > max_valeur):
                    meilleurs_coups = [etat]
                    max_valeur = evaluation # mise à jour de max_valeur
                elif evaluation == max_valeur:        
                    meilleurs_coups.append(etat)

        if(not meilleurs_coups): # pas de meilleurs coups possible car aucune possibilité de mouvement
            return -1, etat_courant # pas de nouvel état possible, on est obligé de renvoyer l'état courant
        meilleur_coup = random.choice(meilleurs_coups) # On choisit un état aléatoire parmi les meilleurs coups possibles
        return max_valeur, meilleur_coup

    else: # c'est à Min de jouer, idem que pour Max
        min_valeur = float('inf')
        meilleurs_coups = []
        etats_possibles = get_all_etats_possibles(etat_courant, COULEUR_MIN)
        for etat in etats_possibles:
            evaluation = minimax(etat, profondeur-1, True)[0] 
            if evaluation <= min_valeur:
                if(evaluation < min_valeur):
                    meilleurs_coups = [etat]
                    min_valeur = evaluation
                elif evaluation == min_valeur:        
                    meilleurs_coups.append(etat)


        if(not meilleurs_coups):
            return 1, etat_courant
        meilleur_coup = random.choice(meilleurs_coups)
        return min_valeur, meilleur_coup

# fonction qui retourne tous les prochains états possibles à partir d'un état donné (tous les prochains coups possibles)
def get_all_etats_possibles(etat_courant, couleurJoueur):
    etats_possibles = [] # Prochains états possible du damier à partir d'un état courant

    # Pour chaque pion du joueur à l'état courant, on simule tous les déplacements possible de ce pion
    for pion in etat_courant.get_all_pions(couleurJoueur):
        deplacements_valides = etat_courant.get_deplacements_obligatoires(pion)
        for deplacement, pions_a_manger in deplacements_valides.items(): 
            # deplacements_valides est un dictionnaire dont les clés sont les positions où un déplacement est possible 
            # et les valeurs sont soit des listes vides si les cases sont vides, soit la couleur des pions qu'on peut manger
            etat_temp = deepcopy(etat_courant) # copie indépendante de l'état courant
            pion_temp = etat_temp.get_pion(pion.ligne, pion.col) # copie indépendante du pion à déplacer
            etat_possible = simulation_deplacement(pion_temp, deplacement, etat_temp, pions_a_manger)
            # On obtient un nouvel etat possible
            etats_possibles.append(etat_possible)
    return etats_possibles

# simule un déplacement sur une copie de l'état courant du damier (deepcopy => copie indépendante)
def simulation_deplacement(pion_temp, deplacement, etat_temp, pion_parcourus):
    ligne = deplacement[0]
    col = deplacement[1]
    etat_temp.deplacer(pion_temp, ligne, col)

    # Si on a mangé des pions durant ce déplacement, on les supprime du damier
    if pion_parcourus:
        etat_temp.supprimer(pion_parcourus)

    return etat_temp

# minimax élagué (prend alpha et beta en argument)
def alpha_beta(etat_courant, profondeur, alpha, beta, joueur_Max, eval):
    # Condition d'arrêt, ne renvoie pas la même valeur d'évaluation en fonction de la difficulté de l'IA
    if profondeur == 0 or etat_courant.jeu_termine(): # profondeur max atteinte ou fin de partie
        if(eval == constantes.PROFONDEUR_SIMPLE):
            return etat_courant.evaluation_facile(), etat_courant # évalue l'état courant (facile)
        elif(eval == constantes.PROFONDEUR_INTER):
            return etat_courant.evaluation_inter(), etat_courant # évalue l'état courant (inter)
        else:
            return etat_courant.evaluation_difficile(), etat_courant # évalue l'état courant (difficile)
        
    if joueur_Max:
        max_valeur = float('-inf')
        meilleurs_coups = [] # Liste pour stocker les meilleurs coups trouvés
        etats_possibles = get_all_etats_possibles(etat_courant, COULEUR_MAX)
        for etat in etats_possibles: # pour chaque coup possible à partir de l'état courant 
            evaluation = alpha_beta(etat, profondeur-1, alpha, beta, False, eval)[0] # Appel récursif de la fonction alpha_beta pour l'état suivant
            if evaluation > max_valeur: # Si l'évaluation de l'état est meilleure que la valeur maximale trouvée jusqu'à présent
                meilleurs_coups = [etat] 
                max_valeur = evaluation
            elif evaluation == max_valeur: # Si l'évaluation de l'état est égale à la valeur maximale trouvée jusqu'à présent
                meilleurs_coups.append(etat)
            alpha = max(alpha, max_valeur) # Mise à jour de la valeur alpha avec la valeur maximale trouvée jusqu'à présent
            if beta <= alpha:
                # Si la valeur beta est inférieure ou égale à la valeur alpha, on arrête la recherche pour cette branche
                # car min n'ira pas chercher une plus grande valeur que alpha, sachant que max prendra alpha ou + il est donc inutile de continuer sur la branche
                break
                
        if(not meilleurs_coups): # Si aucun meilleur coup n'a été trouvé, on retourne une valeur par défaut et l'état courant
            return -1, etat_courant
        meilleur_coup = random.choice(meilleurs_coups) # On choisit aléatoirement l'un des meilleurs coups trouvés
        return max_valeur, meilleur_coup # On retourne la valeur maximale trouvée et le meilleur coup
    
    else: # joueur min, idem que pour max mais cette fois cherche à minimiser son score
        min_valeur = float('inf')
        meilleurs_coups = []
        etats_possibles = get_all_etats_possibles(etat_courant, COULEUR_MIN)
        for etat in etats_possibles:
            evaluation = alpha_beta(etat, profondeur-1, alpha, beta, True, eval)[0]
            if evaluation < min_valeur:
                meilleurs_coups = [etat]
                min_valeur = evaluation
            elif evaluation == min_valeur:
                meilleurs_coups.append(etat)
            beta = min(beta, min_valeur)
            if beta <= alpha: 
                # Si la valeur beta est inférieure ou égale à la valeur alpha, on arrête la recherche pour cette branche
                # car max n'ira pas chercher une plus petite valeur que beta, sachant que min prendra beta ou - il est donc inutile de continuer sur la branche
                break

        if(not meilleurs_coups):
            return 1, etat_courant
        meilleur_coup = random.choice(meilleurs_coups)
        return min_valeur, meilleur_coup