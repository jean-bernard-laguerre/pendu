import random
import pygame
import string


class Bouton():
    def __init__(self, message, x, y, police):
        self.texte = police.render(message, 1, 'black')
        self.rect = self.texte.get_rect()
        self.rect.topleft = (x, y)
        self.rect.w = self.texte.get_width()+20
        self.rect.h = self.texte.get_height()+20

    #Affiche le bouton retourne True lorsque l'on clique dessus
    def affichage(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if (pygame.mouse.get_pressed()[0] == 1):
                action = True

        pygame.draw.rect(surface, 'red', self.rect, 2)
        surface.blit(self.texte, ( self.rect.x+10, self.rect.y+10))

        return action


class Entree():

    def __init__(self, x, y, police):
        self.texte = ''
        self.rect = pygame.Rect(x, y, 100, 40)
        self.surface = police.render(self.texte, 1, 'black')
        self.rect.h = self.surface.get_height()+20

    #Affiche l'entree utilisateur permet d'ecrire lorsque la souris est dessus
    def affichage(self, surface, police):

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:
                        self.texte = self.texte[:-1]

                    elif pygame.key.name(event.key) in string.ascii_lowercase:
                        self.texte += pygame.key.name(event.key)

                self.surface = police.render(self.texte, 1, 'black')
                self.rect.w = max(100 ,self.surface.get_width()+20)
        
        pygame.draw.rect(surface, 'lightblue', self.rect, 2)
        surface.blit(self.surface, (self.rect.x+10, self.rect.y+10))


def partie(mot, trouve):

    retour = []

    for lettre in mot:
        
        if lettre == " ":
            retour += ["  "]

        elif lettre.lower() in trouve:
            retour += [lettre]

        else:
            retour += ["_"]

    return " ".join(retour)

#Recupere un mot au hasard d'un fichier defini
def mot_hasard(niveau):

    match niveau:
        case 1:
            f = open("dictionnaires/motsFacile.txt", "r")
        case 2:
            f = open("dictionnaires/motsMedium.txt", "r")
        case 3:
            f = open("dictionnaires/motsDifficile.txt", "r")
        case _:
            f = open("dictionnaires/mots.txt", "r")

    mots = f.read().splitlines()
    f.close()

    return random.choice(mots)

#Recupere les scores retourne les dix meilleurs
def recup_scores(police):

    topdix = []

    f = open("scores.txt", "r")
    scores = f.read().splitlines()

    for x in range(len(scores)):
        scores[x] = scores[x].split(",")
        scores[x][1] = int(scores[x][1])

    scores.sort(reverse= True, key = lambda score: score[1])

    i = 0

    while True:

        if i == 10 or i >= (len(scores)):
            break
        topdix += [police.render(f"{scores[i][0]}  :  {scores[i][1]}", 1, 'black')]

        i+=1
        

    return topdix

#Ajoute le score dans scores.txt
def ajout_score(st_pendu, mot, nom):
    score_final = (10-st_pendu)*len(mot)
    f = open("scores.txt", "a")
    if len(nom) > 0:
        f.write(f"{nom}, {score_final}\n")
    else:
        f.write(f"Anon, {score_final}\n")
    f.close()