import pygame
from pygame.locals import *
import time

  
pygame.init()
class element_graphique():                  
    # Le constructeur basique
    def __init__(self, img, x , y):
        self.image = img
        self.rect = self.image.get_rect()
        self.alive = True
        # puis on positionne l'element.
        self.rect.x = x
        self.rect.y = y
        self.vie =3

    ## Methode affichage
    def afficher(self, window):
        window.blit(self.image, self.rect)

    def collide(self,other):
        if self.rect.colliderect(other.rect):
            self.alive = False
            return True
        return False

    def en_vie(self):
        return self.alive

class button(element_graphique):
    def __init__(self, color, x,y,largeur,hauteur):
        self.color = color
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.largeur+4,self.hauteur+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.largeur,self.hauteur),0)

    def isOver(self, touches):
        #Pos is the mouse position or a tuple of (x,y) coordinates

        if touches [pygame.K_UP]:
                return True
            
        return False

##=====Element Graphique joueur=====##
class joueur(element_graphique):
    def __init__(self, img, x , y):
        self.image = self.image_origin = img
        self.rect = self.image.get_rect()

        # puis on positionne l'element.
        self.rect.x = x
        self.rect.y = y
        self.vie = 10
        self.speed = 10
        self.en_vie = True
        self.points = 0
        self.angle = 100
        

    def deplacer(self,touches):
        touches = pygame.key.get_pressed()

        if touches [pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed   
            self.image = pygame.transform.rotate(self.image_origin, 0)

        if touches [pygame.K_DOWN] and self.rect.y < hauteur - 64:
            self.rect.y += self.speed
            self.image = pygame.transform.rotate(self.image_origin, 180)


        if touches [pygame.K_RIGHT] and self.rect.x < largeur  - 64:
            self.rect.x += self.speed
            self.image = pygame.transform.rotate(self.image_origin, -90)


        if touches [pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed 
            self.image = pygame.transform.rotate(self.image_origin, 90)

        if touches [pygame.K_LEFT] and touches [pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image_origin, 45)

        if touches [pygame.K_RIGHT] and touches [pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image_origin, -45)

        if touches [pygame.K_LEFT] and touches [pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image_origin, 135)

        if touches [pygame.K_RIGHT] and touches [pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image_origin, -135)

##Fonction menu principal
def main_menu():
    menu = True
    while menu:
        touches = pygame.key.get_pressed()

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:     
                pygame.quit()
                quit()
        if touches [pygame.K_p]:
            menu = False

        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        fenetre.fill(couleurs["rouge"])
        bouton_test.draw(fenetre)
        if touches [pygame.K_UP]:
            bouton_test.color = couleurs["rouge"]
            time.sleep(1.5)
            break
            menu = False


        

        pygame.display.flip()


## Fonction pour lire les images   
def lire_image():
    images = {}
    images["perso"] = pygame.image.load("perso.png").convert_alpha()

    return images

##Fonction pour les couleurs
def lire_couleur():
    couleurs = {}
    couleurs["bleu"] =(0,0,255)
    couleurs["vert"] = (0,255,0)
    couleurs["rouge"] = (255,0,0)
    couleurs["blanc"] = (255,255,255)
    couleurs["noir"] = (0,0,0)

    return couleurs


## initialisation de la fenetre 
largeur = 1000
hauteur = 700
fenetre = pygame.display.set_mode((largeur, hauteur))
BLANC = (255,255,0)
BANC = (255,50,0)
couleurs = lire_couleur()
images = lire_image()
joueur = joueur(images["perso"],300, 30)
bouton_test = button(couleurs["blanc"], largeur/4,hauteur/2, largeur/2, 100)

frame = pygame.time.Clock()

##Fonction boucle du jeu 
def game_loop():
    continuer = True
      
    while continuer:
        touches = pygame.key.get_pressed()
        joueur.deplacer(touches)
        
        frame.tick(30) # Max 30 FPS
        for event in pygame.event.get():    #Attente des événements clavier
            if event.type == QUIT:
                continuer = False


        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        fenetre.fill(couleurs["bleu"])
        joueur.afficher(fenetre)

        pygame.display.flip()


main_menu()
game_loop()
pygame.quit()