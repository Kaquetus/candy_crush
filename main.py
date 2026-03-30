import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from random import randint
import csv
import time

##########################
## FONCTIONS D'UTILITES ##
##########################

def injecter(liste1, liste2):
    """Prend les éléments de liste1 et les mets dans liste2 seulement si ils ne
       sont pas encore présents
    Entrées:
     - liste1 (list): liste qui donne
     - liste2 (list): liste qui reçoit
    Sorties:
     - Rien
    """
    for elem in liste1:
        if elem not in liste2:
            liste2.append(elem)


def copie_mat(mat):
    """Réalise une copie d'une matrice
    Entrées:
     - mat (list 2D): Liste 2D de données
    Sorties:
     - mat_copie (list 2D): Copie de mat
    """
    mat_copie = []
    for ligne in mat:
        mat_copie.append([])
        for elem in ligne:
            mat_copie[-1].append(elem)
    return mat_copie


def copie_liste(liste):
    """Réalise une copie d'une liste
    Entrées:
     - liste (list): Liste de données
    Sorties:
     - liste_copie (list): Copie de liste
    """
    liste_copie = []
    for elem in liste:
        liste_copie.append(elem)
    return liste_copie


def maximum(mat):
    """Renvoie la valeur maximum de la matrice
    Entrées:
     - mat (list 2D): Liste 2D de données
    Sorties:
     - maxi (int): La valeur maximum de la matrice
    """
    maxi = -1
    for ligne in mat:
        for elem in ligne:
            if elem > maxi:
                maxi = elem
    return maxi


###########################
## FONCTIONS D'AFFICHAGE ##
###########################

def affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h):
    """Prend en paramètre une liste 2D mat et présente de manière lisible celle ci
    Entrée:
     - mat (list): Liste 2D à afficher
     - nb_couleurs (int): Le nombre de couleurs possibles moins un
     - affiche (matplotlib.collections.PathCollection): La variable qui contient la
       représentation de la matrice
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
    Sortie:
     - Rien
    """
    scat_offsets, scat_array = mat_vers_scat(mat, taille_v, taille_h)
    affiche.set_offsets(scat_offsets)
    affiche.set_array(scat_array)
    fig.canvas.draw_idle()
    plt.pause(0.35)

def affichage_spyder(mat,nb_couleur,taille_v,taille_h):
    pass

def size_from_diameter(diametre_px, fig):
    """Outil de convertion. Prend le diamètre souhaité d'un marker en pixels, et
       le renvoie en points², l'unité prise par plt.scatter()
    Entrées:
     - diametre_px (flt): Le diamètre souhaité d'un marker en pixels
     - fig (Figure): La figure sur laquelle est placé le scatter plot
    Sorties:
     - diametre_points (flt): Le diamètre souhaité d'un marker en points²
    """
    dpi = fig.dpi
    diametre_points = diametre_px * 72.0 / dpi
    return diametre_points ** 2


def mat_vers_scat(mat, taille_v, taille_h):
    """Prend en paramètre la matrice sur laquelle on fait les calculs, et la renvoie
       sous un format accepté par matplotlib pour changer les données de la scatter
       plot
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - taille_v (int): Nombre de cases dans la matrice à la verticale
     - taille_h (int): Nombre de cases dans la matrice à l'horizontale
    Sorties:
     - scat_offsets (list 2D): Les coordonées de tous les points de la grille
     - scat_array (list): Les valeurs associées à chaque point
    """
    scat_offsets = []
    scat_array = []
    for i in range(taille_v):
        for j in range(taille_h):
            if mat[i][j] != -1:
                scat_offsets.append([j, taille_v - 1 - i])
                scat_array.append(mat[i][j])
    return scat_offsets, scat_array


############################
## FONCTIONS DE RECHERCHE ##
############################

def point_alignes(mat, pos, taille_v, taille_h, n=3):
    """Prend en paramètre une position dans la matrice et renvoie toutes les
       cases alignés dans une croix de diamètre n de cases
    Entrées:
     - mat (list): Liste 2D de la grille
     - pos (list): liste de deux valeurs contenant les coordonnées d'un point
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - n (int): le diamètre de la crois (peut avoir comme valeur 3 ou 5)
    Sorties:
     - alignes (list 2D): liste avec les coordonnées des cases qui sont alignées
    """
    alignes = []
    if n == 3:
        for o in ['h', 'v']:
            temp = trois_alignes(mat, pos, taille_v, taille_h, orientation=o)
            injecter(temp, alignes)
    elif n == 5:
        for i in range(-1, 2):
            for o in ['h', 'v']:
                temp = trois_alignes(mat, pos, taille_v, taille_h, orientation=o, centre=i)
                injecter(temp, alignes)
    return alignes


def trois_alignes(mat, pos, taille_v, taille_h, orientation, centre=0):
    """Prend en paramètre une position dans la matrice et regarde si les
       trois cases orientées soit horizontalement soit verticalement ont
       la même valeur
    Entrées:
     - mat (list): Liste 2D de la grille
     - pos (list): liste de deux valeurs contenant les coordonnées d'un point
     - orientation (str): "v" si il regarde à la verticale, et "h" si il
       regarde à l'horizontale
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - centre (int): le centre des trois cases qu'il regarde (peut avoir
       comme valeur -1, 0, ou 1)
    Sorties:
     - trois (list 2D): liste avec les trois coordonnées des cases qui
       sont alignées
    """
    trois = []
    if orientation == 'v':
        if pos[0] - 1 + centre >= 0 and pos[0] + 1 + centre < taille_v and 0 <= pos[0] + centre and pos[
            0] + centre < taille_v:
            if mat[pos[0] + centre][pos[1]] == mat[pos[0] + 1 + centre][pos[1]] and mat[pos[0] + centre][pos[1]] == \
                    mat[pos[0] - 1 + centre][pos[1]]:
                trois.append([pos[0] + 1 + centre, pos[1]])
                trois.append([pos[0] + centre, pos[1]])
                trois.append([pos[0] - 1 + centre, pos[1]])
    elif orientation == 'h':
        if pos[1] - 1 + centre >= 0 and pos[1] + 1 + centre < taille_h and 0 <= pos[1] + centre and pos[
            1] + centre < taille_h:
            if mat[pos[0]][pos[1] + centre] == mat[pos[0]][pos[1] + 1 + centre] and mat[pos[0]][pos[1] + centre] == \
                    mat[pos[0]][pos[1] - 1 + centre]:
                trois.append([pos[0], pos[1] + 1 + centre])
                trois.append([pos[0], pos[1] + centre])
                trois.append([pos[0], pos[1] - 1 + centre])
    return trois


def cases_a_detruire(mat, taille_v, taille_h):
    """Prend en paramètre la matrice, et renvoie une liste de tous les
       éléments à détruire
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
    Sorties:
     - a_detruire (list 2D): liste avec les coordonnées des points qui sont
       à détruire
    """
    a_detruire = []
    for y in range(taille_v):
        for x in range(taille_h):
            inter = point_alignes(mat, [y, x], taille_v, taille_h)
            injecter(inter, a_detruire)
    return a_detruire


def recherche(mat, liste):
    """Prend en paramètre la matrice du jeu et une liste de cases. Recherche et
       renvoie toutes les cases ayant la même valeur et étant adjacentes aux cases
       de la liste.
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - liste (list 2D): liste contenant les coordonnées des cases à analyser
    Sorties:
     - liste_validee (list 2D): liste contenant les coordonnées des cases ayant
       la même valeur et étant adjacentes aux cases de la liste initiale
    """
    liste_verifier = copie_liste(liste)
    liste_validee = []
    taille_v = len(mat)
    taille_h = len(mat[0])

    while liste_verifier:  # Continue tant que la liste n'est pas vide
        coord_x, coord_y = liste_verifier.pop(0)
        val_xy = mat[coord_x][coord_y]
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            coord_xmod = coord_x + i
            coord_ymod = coord_y + j

            if 0 <= coord_xmod < taille_v and 0 <= coord_ymod < taille_h:
                val_xymod = mat[coord_xmod][coord_ymod]
                if val_xymod == val_xy:
                    if ([coord_xmod, coord_ymod] not in liste_verifier) and (
                            [coord_xmod, coord_ymod] not in liste_validee):
                        liste_verifier.append([coord_xmod, coord_ymod])
        if [coord_x, coord_y] not in liste_validee:
            liste_validee.append([coord_x, coord_y])
    return liste_validee


################################
## FONCTIONS D'INITIALISATION ##
################################

def grille_aleatoire(taille_v, taille_h, nb_couleurs):
    """Prend en paramètre la taille de la grille et renvoie une liste 2D sans 3 ou
       plus même couleur en ligne.
    Entrées:
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - nb_couleurs (int): Le nombre de couleurs possibles moins un
    Sorties:
     - mat (list): Liste 2D de la grille
    """
    mat = []
    for y in range(taille_v):
        mat.append([])
        for x in range(taille_h):
            mat[y].append(randint(0, nb_couleurs))

    destroy = cases_a_detruire(mat, taille_v, taille_h)
    while destroy:  # Continue tant que destroy n'est pas vide
        destruction(mat, destroy)
        tri(mat)
        remplir_grille(mat, nb_couleurs, taille_v, taille_h)
        destroy = cases_a_detruire(mat, taille_v, taille_h)

    return mat


def fichier_vers_liste(fichier):
    """Prend en paramètre le nom d'un fichier, en extrait le csv et le
       transforme en liste 2D.
    Entrées:
     - fichier (str): Le nom du fichier csv qui contient la grille
    Sorties:
     - mat (list 2D): Liste 2D utilisable par le reste du programme
    """
    mat = []
    with open(fichier, newline="") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            mat.append([])
            for elem in row[0]:
                if elem != ' ':
                    mat[-1].append(int(elem))
    return mat


def initialisation():
    """Demande à l'utilisateur si il veut rentrer un fichier, ou si il veut
       une grille aléatoire. Si il choisi le fichier, lui demander le nom du
       fichier. Si il choisi aléatoire, lui demander la  taille de la grille
       et la valeur max. Crée la grille correspondante et la renvoie, ainsi que
       ses valeurs associées.
    Entrées:
     - Rien
    Sorties:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - nb_couleurs (int): Le nombre de couleurs moins un
    """
    type_jeu = None
    while type_jeu not in ['1', '2']:
        type_jeu = input(
            "Voulez-vous entrer un fichier de jeu, ou voulez-vous avoir un jeu aléatoire? Entrez 1 pour la première option, et 2 pour la deuxième.\n>>> ")
    if type_jeu == '1':
        nom_fichier = input("Entrez le nom du fichier.\n>>> ")
        mat = fichier_vers_liste(nom_fichier)
        taille_v = len(mat)
        taille_h = len(mat[0])
        nb_couleurs = maximum(mat)
    else:
        taille_h = int(input("Que voulez-vous comme taille horizontale de grille?\n>>> "))
        taille_v = int(input("Que voulez-vous comme taille verticale de grille?\n>>> "))
        nb_couleurs = int(input("Combien de couleurs voulez-vous??\n>>> ")) - 1
        mat = grille_aleatoire(taille_v, taille_h, nb_couleurs)
        while verifie_fin(mat, taille_v, taille_h, nb_couleurs):
            mat = grille_aleatoire(taille_v, taille_h, nb_couleurs)
    return mat, taille_v, taille_h, nb_couleurs


###############################
## FONCTIONS DE VERIFICATION ##
###############################

def cote_a_cote(case1, case2):
    """Renvoie si les deux cases sont bien cote à cote
    Entrées:
     - case1 (list): Les coordonnés de la première case
     - case2 (list): Les coordonnés de la deuxième case
    Sorties:
     - a_cote (bool): True si cote à cote, False sinon
    """
    a_cote = False
    for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if case1[0] + i == case2[0] and case1[1] + j == case2[1]:
            a_cote = True
    #print("valeur a coté ",a_cote)
    return a_cote


def verification(mat, case1, case2, taille_v, taille_h, nb_couleurs):
    """Regarde si un échange est valide; si c'est le cas, renvoie toutes les cases
       qui seront alignés dû à cet échange
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - case1 (list): Les coordonnés de la première case
     - case2 (list): Les coordonnés de la deuxième case
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - nb_couleurs (int): Le nombre de couleurs moins un
    Sorties:
     - alignes (list 2D): les cases qui seront alignés dû à cet échange
    """
    if cote_a_cote(case1, case2):
        #print(2)
        mat_copie = copie_mat(mat)
        #print(case1,case2)
        temp = mat_copie[case1[0]][case1[1]]
        mat_copie[case1[0]][case1[1]] = mat_copie[case2[0]][case2[1]]
        mat_copie[case2[0]][case2[1]] = temp
        alignes = point_alignes(mat_copie, case1, taille_v, taille_h, n=5)
        alignes_2 = point_alignes(mat_copie, case2, taille_v, taille_h, n=5)
        injecter(alignes_2, alignes)
    else:
        alignes = []
    #print(alignes)
    return alignes


def verifie_fin(mat, taille_v, taille_h, nb_couleurs):
    """Prend en paramètre la matrice de données ainsi que ses valeurs associées et
       renvoie False si le joueur peut effectuer une action, et True sinon.
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - nb_couleurs (int): Le nombre de couleurs moins un
    Sorties:
     - cont (bool): True si le joueur peut effectuer une action, et False sinon
    """
    verif = []
    y = 0
    # première boucle: complexité o(taille_v)
    while y < taille_v and not verif:  # Continue tant que la liste n'est pas vide
        x = 0
        # deuxième boucle: complexité o(taille_h)
        while x < taille_h and not verif:
            if x + 1 < taille_h:
                verif = verification(mat, [y, x], [y, x + 1], taille_v, taille_h, nb_couleurs)
            if not verif and y + 1 < taille_v:
                verif = verification(mat, [y, x], [y + 1, x], taille_v, taille_h, nb_couleurs)
            x += 1
        y += 1
    #print('verif')
    return not verif


############################################
## FONCTIONS DE CONSEQUENCES D'UN ECHANGE ##
############################################

def tour(mat, case1, case2, nb_couleurs, taille_v, taille_h, score):
    """Prend les deux cases que le joueur veut échanger, vérifie que c'est un
       échange valide, échange les cases, supprime les cases nécessaires, fait
       tomber les cases qu'il faut, remplit la grille, et continue ce cycle
       jusqu'à que la grille est stable.
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - case1 (list): Les coordonnés de la première case
     - case2 (list): Les coordonnés de la deuxième case
     - nb_couleurs (int): Le nombre de couleurs moins un
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - score (int): Le nombre de points que le joueur a
    Sorties:
     - score (int): Le nombre de points que le joueur a
    """
    alignes = verification(mat, case1, case2, taille_v, taille_h, nb_couleurs)  # Vérifie que l'échange est valide
    if alignes:  # Si la liste n'est pas vide
        # Réalise l'échange des cases
        temp = mat[case1[0]][case1[1]]
        mat[case1[0]][case1[1]] = mat[case2[0]][case2[1]]
        mat[case2[0]][case2[1]] = temp

        toutes_alignes = recherche(mat, alignes)  # Trouve toutes les cases alignées
        affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
        destruction(mat, toutes_alignes)  # Détruit les cases nécessaires
        score += len(toutes_alignes)
        affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
        ax.set_title(f'Points: {score}')
        tri(mat)  # Fait remonter les cases vides
        affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
        remplir_grille(mat, nb_couleurs, taille_v, taille_h)  # Remplit les cases vides
        affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
        detruire = recherche(mat, cases_a_detruire(mat, taille_v, taille_h))  # Trouve toutes les cases à détruire
        while detruire:
            destruction(mat, detruire)  # Détruit les cases nécessaires
            score += len(detruire)
            affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
            ax.set_title(f'Points: {score}')
            tri(mat)  # Fait remonter les cases vides
            affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
            remplir_grille(mat, nb_couleurs, taille_v, taille_h)  # Remplit les cases vides
            affichage_grille(mat, nb_couleurs, affiche, taille_v, taille_h)  # Affiche la grille
            detruire = recherche(mat, cases_a_detruire(mat, taille_v, taille_h))  # Trouve toutes les cases à détruire
    else:
        ax.set_title("Ceci n'est pas un échange valide, veuillez réessayer")
        fig.canvas.draw_idle()  # Mise a jour de la figure
        plt.pause(0.001)
    return score


def tri(mat):
    """Prend en paramètre une liste 2D et fait remonter les -1
    Entrées:
     - mat(list): Liste 2D à trier
    Sorties:
     - Rien
    """
    taille_v = len(mat)
    taille_h = len(mat[0])
    for x in range(taille_h):
        changement = True
        while changement:
            changement = False
            for y in range(taille_v - 1):
                if mat[y][x] != -1 and mat[y + 1][x] == -1:
                    changement = True
                    mat[y + 1][x], mat[y][x] = mat[y][x], mat[y + 1][x]


def remplir_grille(mat, nb_couleurs, taille_v, taille_h):
    """Rempli aléatoirement les cases de code -1 de la grille avec des
       couleurs (nouveaux bonbons)
    Entrée:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - nb_couleurs (int): Le nombre de couleurs moins un
    Sorties:
     - Rien
    """
    for y in range(taille_v):
        for x in range(taille_h):
            if mat[y][x] == -1:
                mat[y][x] = randint(0, nb_couleurs)


def destruction(mat, a_detruire):
    """Prend en paramètre la matrice de données et la liste de coordonnés
       de cases à détruire, et remplace toutes les cases à détruire par -1
    Entrées:
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - a_detruire (list 2D): liste avec les coordonnées des points qui sont à détruire
    Sorties:
     - Rien
    """
    for case in a_detruire:
        mat[case[0]][case[1]] = -1


#############################
## FONCTIONS D'INTERACTION ##
#############################


def choix_cases(grille:list[list[int]])->list[list[int]]:
    """fonction servant à récupérer les entrées utilisateur des cases à échanger
    entrée:
        grille: grille de jeu, permet de s'assurer que les cases échangées existent
    sortie:
        cases: les coordonnées x et y des deux cases à inverser
    """
    cases = []
    while len(cases)<2:
        case_x1 = input("entrez la coordonnée x de la première case\n>>> ")
        case_y1 = input("entrez la coordonnée y de la première case\n>>> ")
        case_x2 = input("entrez la coordonnée x de la seconde case\n>>> ")
        case_y2 = input("entrez la coordonnée y de la seconde case\n>>> ")
        try:
            if 0 <= int(case_x1) < taille_h and 0 <= int(case_y1) < taille_v:
                if 0 <= int(case_x2) < taille_h and 0 <= int(case_y2) < taille_v:
                    case_x1 = int(case_x1)
                    case_y1 = taille_v- 1 - int(case_y1)
                    case_x2 = int(case_x2)
                    case_y2 = taille_v- 1 - int(case_y2)
                    cases = [[case_y1,case_x1],[case_y2,case_x2]]
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            print("ERREUR")
            time.sleep(1.5)
            for _ in range(10):
                print("ERREUR")
                time.sleep(0.1)
            print("VEUILLEZ ENTREZ DES DONNEES CONFORMES !! ! ! ! ! ! ! ")
            time.sleep(0.8)
            print("ERREUR")
            time.sleep(0.5)
    #print(type(cases[0][1]))
    return cases

def on_click(event):
    """Récupère les coordonnées x, y d'un click sur les axes de la grille, et
       les stocke dans une liste. Quand deux clicks ont été effectués, active
       la fonction tour(). Si le jeu est fini, ne récupère plus les clicks, et
       affiche que le jeu est fini.
    Entrées:
     - event (matplotlib.backend_bases.MouseEvent): Le click, ainsi que toutes
       les données sur la position de la souris
    Globaux:
     - Je sais que c'est une mauvaise pratique, mais cette fonction ne peut que
       prendre en paramètre event, et ne peut rien return
     - mat (list 2D): Liste 2D de données contenant les valeurs de chaque case
     - nb_couleurs (int): Le nombre de couleurs moins un
     - affiche (matplotlib.collections.PathCollection): La variable qui contient la
       représentation de la matrice
     - taille_v (int): nombre de cases dans la matrice à la verticale
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
     - score (int): Le nombre de points que le joueur a
    Sorties:
     - Rien
    """
    global mat, nb_couleurs, affiche, taille_v, taille_h, cases, score

    if event.xdata != None and event.ydata != None and -0.5 <= event.xdata <= taille_h and -0.5 <= event.ydata <= taille_v:  # Si on clique dans la grille
        if not verifie_fin(mat, taille_v, taille_h, nb_couleurs):  # Si le jeu n'est pas finit
            cases.append([taille_v - 1 - int(event.ydata), int(event.xdata)])  # Ajoute la cases a la liste de cases
            if len(cases) == 2:
                score = tour(mat, cases[0], cases[1], nb_couleurs, taille_v, taille_h, score)  # Réalise un tour
                cases = []  # Vide la liste de cases
        else:
            ax.set_title(f"Le jeu est fini! Merci d'avoir joué. Votre score est {score}")
            fig.canvas.draw_idle()  # Mise a jour de la figure



def on_resize(event):
    """S'active dès que la fenêtre d'affichage change de dimensions, permet de
       changer la taille des markers et l'épaisseur des lignes dynamiquement
    Entrées:
     - event (matplotlib.backend_bases.ResizeEvent): Contient les données de taille
       de la fenêtre
    Globaux:
     - affiche (matplotlib.collections.PathCollection): La variable qui contient la
       représentation de la matrice
     - taille_h (int): nombre de cases dans la matrice à l'horizontale
    Sorties:
     - Rien
    """
    global affiche, taille_h

    # Recalcule la taille des markers
    fig.canvas.draw()
    bbox = ax.get_window_extent()
    width_px = bbox.width
    size = size_from_diameter((width_px / taille_h) * 0.8, fig)

    # Change la taille des markers
    affiche.set_sizes([size])

    # Mise a jour de la figure
    fig.canvas.draw_idle()

def candy_crush(nb_iter):
    score = 0
    nb_tour = 0
    while not verifie_fin(mat,taille_v,taille_h,nb_couleurs) and nb_iter>=nb_tour:
        case1, case2 = choix_cases(mat)
        score = tour(mat,case1, case2,nb_couleurs,taille_v,taille_h,score)
        nb_tour += 1
    ax.set_title(f"le jeu est fini, merci d'avoir joué, vous finissez avec un score de {score}")


#########################
## PROGRAMME PRINCIPAL ##
#########################


# Initialisation des variables
if __name__=="__main__":

    cases = []
    score = 0
    # Initialisation de la matrice
    mat, taille_v, taille_h, nb_couleurs = initialisation()


    # Initialisation de la figure et de l'axe
    fig, ax = plt.subplots()

    # Affichage orthonormé et stable du scatter plot
    ax.set_xlim(-0.5, taille_h-0.5)
    ax.set_ylim(-0.5, taille_v-0.5)
    ax.xaxis.set_ticks(range(0, taille_h,1))
    ax.yaxis.set_ticks(range(0, taille_v,1))
    ax.set_aspect('equal', 'box')

    # Determination de la taille des markers
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = ax.get_window_extent(renderer=renderer)
    width_px = bbox.width
    height_px = bbox.height
    size = size_from_diameter((width_px / taille_h) * 0.8, fig)

    # Affichage des lignes de la grille
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))


    ax.grid(which='minor', lw=(width_px / taille_h) * 0.05 * 72 / fig.dpi)
    # Convertion initiale des données de type matrice à un type compris par ax.scatter
    scat_x = []
    scat_y = []
    scat_col = []
    for i in range(taille_v):
        for j in range(taille_h):
            scat_x.append(j)
            scat_y.append(taille_v - 1 - i)
            scat_col.append(mat[i][j])

    # Initialisation de la grille
    affiche = ax.scatter(scat_x, scat_y, c=scat_col, cmap='jet', s=size)
    ax.set_title(f'Points: {score}')

    # Connecte la figure aux fonctions on_click et on_resize
    #fig.canvas.mpl_connect("button_press_event", on_click)
    #fig.canvas.mpl_connect("resize_event", on_resize)

    # Affiche la grille
    plt.show(block=False)
    plt.pause(0.001)
    #print(choix_cases(mat))

    candy_crush(40)
