from outils import *
import pygame
import string

pygame.init()

ecran = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pendu")
police_grand = pygame.font.SysFont('Verdana', 40)
police_petit = pygame.font.SysFont('Verdana', 20)
police_titre = pygame.font.SysFont('couriernew', 90)
clock = pygame.time.Clock()


solution = ''
scores = recup_scores(police_petit)
nom = Entree(425, 500, police_petit)
mot_manuel = Entree(475, 350, police_petit)
statut_pendu = 0
statut_partie = 0
correct = []
erreurs = []

images_pendu = []
for i in range(10):
    images_pendu += [pygame.image.load(f"images/pendu{i}.png")]

#Affiche la partie en cours
def ecran_jeu():

    ecran.fill((255, 255, 255))
    
    jeu = police_grand.render(partie(solution, correct), 1, 'black')
    reponse_fausse = police_petit.render(f"Erreurs: {' '.join(erreurs)}", 1, 'black')

    ecran.blit(jeu, (325,300))
    ecran.blit(reponse_fausse, (50,500))
    ecran.blit(images_pendu[statut_pendu], (0, 100))

#Menu du jeu
def ecran_menu():
    global statut_partie, solution, nom

    ecran.fill((255, 255, 255))

    lbl_nom = police_petit.render("Nom : ", 1, 'black')
    titre = police_titre.render("PENDU", 1, 'brown4')
    
    btn_Facile = Bouton("FACILE", 200, 250, police_petit)
    btn_medium = Bouton("MOYEN", 350, 250, police_petit)
    btn_difficile = Bouton("DIFFICILE", 500, 250, police_petit)
    btn_manuel = Bouton("MANUEL : ", 330, 350, police_petit)
    btn_scores = Bouton("Scores", 150, 500, police_petit)

    nom.affichage(ecran, police_petit)
    mot_manuel.affichage(ecran, police_petit)
    ecran.blit(lbl_nom, (350, 510))
    ecran.blit(titre, (270, 75))

    if btn_Facile.affichage(ecran):
        solution = mot_hasard(1)
        statut_partie = 1

    if btn_medium.affichage(ecran):
        solution = mot_hasard(2)
        statut_partie = 1

    if btn_difficile.affichage(ecran):
        solution = mot_hasard(3)
        statut_partie = 1

    if btn_manuel.affichage(ecran):
        if  2 < len(mot_manuel.texte) < 13:
            solution = mot_manuel.texte
            statut_partie = 1

    if btn_scores.affichage(ecran):
        statut_partie = 3

#Affiche message de fin de partie et solution
def ecran_fin():

    global statut_partie

    if victoire():
        message = "Felicitation!"
    else:
        message = "Dommage..."

    reponse = police_petit.render(f"Le mot etait : {solution}", 1, 'black')
    ecran.fill((255, 255, 255))
    
    partieFinie = police_grand.render(message, 1, 'black')

    #Boutons
    btn_menu = Bouton("Menu", 400, 500, police_petit)
    btn_scores = Bouton("Scores", 150, 500, police_petit)

    if btn_menu.affichage(ecran):
        nouvelle_partie()
        statut_partie = 0

    if btn_scores.affichage(ecran):
        statut_partie = 3

    ecran.blit(partieFinie, (275, 175))
    ecran.blit(reponse, (275, 250))

#Affiche les dix meilleurs scores
def ecran_scores():

    global statut_partie

    ecran.fill((255, 255, 255))

    for i in range(len(scores)):
        ecran.blit(scores[i], (325, (50+(i*40))))
    
    #bouton de retour au menu
    btn_menu = Bouton("Menu", 600, 500, police_petit)
    
    if btn_menu.affichage(ecran):
        nouvelle_partie()
        statut_partie = 0

#Remet le pendu a zero
def nouvelle_partie():

    global statut_pendu, correct, erreurs

    statut_pendu = 0
    correct = []
    erreurs = []

#teste si la lettre est presente dans le mot
def test_lettre(lettre, solution):

    global correct, erreurs, statut_pendu

    #ne fait rien si le charactere n'est pas une lettre ou a deja été tenté
    if (lettre in correct) or (lettre in erreurs) or (lettre not in string.ascii_lowercase):
        return

    #ajout la lettre a la liste d'essai corrects/erreurs si elle est dans le mot ou non
    if lettre in solution.lower():
        correct += [lettre]
    else:
        erreurs += [lettre]
        statut_pendu += 1

#teste si le mot a été trouvé
def victoire():

    for lettre in solution:
        if not (lettre.lower() in correct):
            return False

    return True
    

en_cours = True

# boucle principale
while en_cours:
    clock.tick(60)
    match statut_partie:
        case 0:
            ecran_menu()
        case 1:
            ecran_jeu()
        case 2:
            ecran_fin()
        case 3:
            ecran_scores()

    pygame.display.update()
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            en_cours = False

        if event.type == pygame.KEYDOWN and statut_partie == 1:

            lettre = pygame.key.name(event.key)
            test_lettre(lettre, solution)

            if statut_pendu == 10 or victoire():

                ajout_score(statut_pendu, solution, nom.texte)
                scores = recup_scores(police_petit)
                statut_partie = 2


pygame.quit()