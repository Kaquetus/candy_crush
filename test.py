from main import *
#########################
#  TEST DES FONCTIONS   #
#########################

def test(fonction, returns, *param, **kw):
    """
    fonction testant la bonne marche du code
    :param fonction: la fonction a tester
    :param returns: ce que doit retourner la fonction
    :param param: les paramètres de la fonction à tester
    :param kw: les paramètres rentrés par keywords
    :return: None
    """
    try:
        # si ce bloc s'exécute normalement, la fonction testée fonctionne correctement
        assert fonction(*param,**kw)==returns
        print(f'aucun problème détecté avec la fonction {fonction.__name__}')
    except AssertionError:
        print(f'la fonction {fonction.__name__} retourne {fonction(*param)} au lieu de {returns}')


def test_injecter(retour, liste1, liste2):
    l1 = liste1
    l2 = liste2
    injecter(l1, l2)
    l2.sort()
    if l2 == retour:
        print('aucun problème détécté avec la fonction injecter')
    else:
        print(f'la fonction injecter retourne {l2} au lieu de {retour}')


def test_tri(retour, matrice):
    tri(matrice)
    if matrice == retour:
        print('aucun problème détécté avec la fonction tri')
    else:
        print(f'la fonction tri retourne {matrice} au lieu de {retour}')


def test_destruction(retour, matrice, a_detruire):
    destruction(matrice, a_detruire)
    if matrice == retour:
        print('aucun problème détécté avec la fonction destruction')
    else:
        print(f'la fonction destruction retourne {matrice} au lieu de {retour}')


def test_remplir_grille(matrice,taille_v, taille_h, nb_couleurs):
    remplir_grille(matrice,nb_couleurs,taille_v, taille_h)
    marche = True
    for l in matrice:
        for e in l:
            if e == -1:
                marche = False
    if marche:
        print('aucun problème détécté avec la fonction remplir_grille')
    else:
        print(f'la fonction remplir_grille retourne {matrice} et en remplit pas toutes les cases vides')

def test_grille_aleatoire(taille_v, taille_h, nb_couleurs):
    matrice = grille_aleatoire(taille_v, taille_h, nb_couleurs)
    tv = len(matrice)
    if tv != 0:
        th = len(matrice[0])
        nbc = maximum(matrice)
    else:
        th = 0
        nbc = -1
    if tv == taille_v and th == taille_h and nbc == nb_couleurs:
        print('aucun problème détécté avec la fonction grille_aleatoire')
    else:
        print(
            f'la fonction grille_aleatoire retourne {matrice} qui n\'est pas en accord avec les conditions initiales données')


print("lancement des tests")

# --- injecter ---
test_injecter([1, 2, 3, 4, 5], [1, 2, 3], [3, 4, 5])  # Général
test_injecter([1, 2, 3], [1, 2, 3], [1, 2, 3])  # Listes identiques
test_injecter([1, 2, 3], [1, 2, 3], [])  # Une liste vide

# --- copie_mat ---
test(copie_mat, [[1, 2], [3, 4]], [[1, 2], [3, 4]])  # Général
test(copie_mat, [[0]], [[0]])  # Un élément
test(copie_mat, [], [])  # Matrice vide

# --- copie_liste ---
test(copie_liste, [1, 2, 3], [1, 2, 3])  # Général
test(copie_liste, [0], [0])  # Un élément
test(copie_liste, [], [])  # Liste vide

# --- maximum ---
test(maximum, 9, [[1, 9], [3, 4]])  # Général
test(maximum, 0, [[0, 0], [0, 0]])  # Que des zéros
test(maximum, -1, [])  # Liste vide

# --- mat_vers_scat ---
test(mat_vers_scat, ([[0, 1], [1, 1], [0, 0], [1, 0]], [1, 2, 3, 4]), [[1, 2], [3, 4]], 2, 2)  # Général
test(mat_vers_scat, ([], []), [[-1, -1]], 1, 1)  # Que des -1
test(mat_vers_scat, ([], []), [], 0, 0)  # Matrice vide

# --- point_alignes ---
test(point_alignes, [[2, 1], [1, 1], [0, 1]], [[1, 5, 3], [4, 5, 6], [7, 5, 9]], [1, 1], 3, 3)  # Des points alignés
test(point_alignes, [], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 1], 3, 3)  # rien d'aligné
test(point_alignes, [[2, 3], [2, 2], [2, 1], [3, 2], [1, 2], [2, 4], [4, 2]],
     [[1, 2, 1, 4, 5], [1, 2, 3, 4, 5], [1, 3, 3, 3, 3], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]], [2, 2], 5, 5,n=5)  # Pour n=5

# --- trois_alignes (vertical) ---
test(trois_alignes, [[2, 0], [1, 0], [0, 0]], [[1, 0], [1, 0], [1, 0]], [1, 0], 3, 2,
     orientation='v')  # orientation='v'
test(trois_alignes, [[0, 2], [0, 1], [0, 0]], [[0, 0, 0], [1, 1, 1]], [0, 1], 2, 3, orientation='h')  # orientation='h'
test(trois_alignes, [[0, 2], [0, 1], [0, 0]], [[0, 0, 0], [1, 1, 1]], [0, 2], 2, 3, orientation='h',
     centre=-1)  # pas centré

# --- cases_a_detruire ---
test(cases_a_detruire, [[2, 0], [1, 0], [0, 0]], [[1, 2, 3], [1, 5, 6], [1, 8, 9]], 3, 3)  # Cases à détruire
test(cases_a_detruire, [], [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, 3)  # Rien à détruire
test(cases_a_detruire, [], [], 0, 0)  # Matrice vide

# --- recherche ---
test(recherche, [[0, 0], [1, 0], [0, 1]], [[1, 1, 2], [1, 3, 4], [5, 6, 7]], [[0, 0]])  # Case liée
test(recherche, [[0, 2]], [[1, 1, 2], [1, 3, 4], [5, 6, 7]], [[0, 2]])  # Case isolée
test(recherche, [[0, 0], [2, 2], [1, 0], [0, 1], [1, 2], [2, 1]], [[1, 1, 2], [1, 3, 7], [5, 7, 7]],
     [[0, 0], [2, 2]])  # Cases de différentes valeurs

# --- grille aleatoire ---

test_grille_aleatoire(3, 2, 3) # Grille aléatoire
test_grille_aleatoire(3, 3, 3) # Grille carrée
test_grille_aleatoire(0, 0, -1) # Taille nulle

# --- cote_a_cote ---
test(cote_a_cote, True, [0, 0], [0, 1])  # Cote à cote
test(cote_a_cote, False, [0, 0], [1, 1])  # Pas cote à cote
test(cote_a_cote, False, [0, 0], [0, 0])  # Même case

# --- verification ---
test(verification, [[2, 1], [1, 1], [0, 1], [2, 2], [1, 2], [0, 2]],
     [[1, 2, 1, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1]], [1, 1], [1, 2], 5, 5,
     2)  # Echange valide
test(verification, [], [[3, 7, 1, 4, 2], [6, 2, 3, 5, 8], [1, 9, 3, 4, 0], [5, 0, 7, 2, 6], [4, 1, 8, 9, 3]], [0, 0],
     [0, 1], 5, 5, 2)  # Echange non valide
test(verification, [], [[1, 2, 1, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1]], [1, 1],
     [1, 3], 5, 5, 2)  # Cases pas cote à cote

# --- verifie_fin ---
test(verifie_fin, True, [[3, 7, 1, 4, 2], [6, 2, 3, 5, 8], [1, 9, 3, 4, 0], [5, 0, 7, 2, 6], [4, 1, 8, 9, 3]], 5, 5,
     10)  # Le jeu est fini
test(verifie_fin, False, [[1, 2, 1, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1], [2, 1, 2, 1, 2], [1, 2, 1, 2, 1]], 5, 5,
     2)  # Le jeu n'est pas fini
test(verifie_fin, True, [], 0, 0, 2)

# --- tri ---
test_tri([[-1, -1, 2], [1, -1, 4], [1, 1, 7]], [[1, 1, 2], [1, -1, 4], [-1, -1, 7]])  # Matrice à trier
test_tri([[-1, -1, 2], [1, 3, 4], [5, 6, 7]], [[-1, -1, 2], [1, 3, 4], [5, 6, 7]])  # Matrice triée
test_tri([[1, 1, 2], [1, 3, 4], [5, 6, 7]], [[1, 1, 2], [1, 3, 4], [5, 6, 7]])  # Matrice sans éléments à trier

# --- remplir_grille ---
test_remplir_grille([[-1,-1,2],[1,-1,4],[1,1,7]],3,3,7) #Matrice triée avec vides
test_remplir_grille([[1,1,2],[1,-1,4],[-1,-1,7]],3,3,7) #Matrice non triée avec vides
test_remplir_grille([[1,1,2],[1,3,4],[5,6,7]],3,3,7) #Matrice sans vides

# --- destruction ---
test_destruction([[-1, -1, 2], [-1, 3, 4], [5, 6, 7]], [[1, 1, 2], [1, 3, 4], [5, 6, 7]],
                 [[0, 0], [0, 1], [1, 0]])  # Général
test_destruction([[1, 1, 2], [1, 3, 4], [5, 6, 7]], [[1, 1, 2], [1, 3, 4], [5, 6, 7]], [])  # Rien à détruire
test_destruction([[-1, -1, 2], [-1, 3, 4], [5, 6, 7]], [[-1, -1, 2], [-1, 3, 4], [5, 6, 7]],
                 [[0, 0], [0, 1], [1, 0]])  # Cases déja détruites

print("fin des tests")