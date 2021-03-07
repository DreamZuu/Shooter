import pygame  
from random import *
from pygame.locals import *
from math import *

  
pygame.init()
class element_graphique():                  
    # Le constructeur basique
    def __init__(self, img, x , y):
        self.image = img
        self.rect = self.image.get_rect()
        # puis on positionne l'element.
        self.rect.x = x
        self.rect.y = y

    ## Methode affichage
    def afficher(self, window):
        window.blit(self.image, self.rect)

    

## class pour les personnages avec de la vie
class element_avec_vie(element_graphique):
    def __init__(self, image, x , y, vie, speed):
        self.image = self.image_origin = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.vie = vie
        self.alive = True  

    def collide(self,other):
        if self.rect.colliderect(other.rect):
            self.alive = False
            return True
        return False 
        
    def en_vie(self):
        return self.alive    
    

##Element graphique texte
class Texte(element_graphique):
    # Le constructeur basique
    def __init__(self, msg, x=0,y=0, fontsize=34, rgb=(100, 255, 255)):
        self.font = pygame.font.Font(None, fontsize)
        self.rgb = rgb
        image = self.font.render(msg, True, rgb)
        element_graphique.__init__(self, image,x,y)

        #print (self.rect.x,self.rect.y)

    def update(self, msg):
        self.image = self.font.render(msg, True, self.rgb)

       

##=====Element Graphique joueur=====##
class joueur(element_avec_vie):
    def __init__(self, image, x , y, vie = 10, speed = 15, angle = 0):
        self.image = self.image_origin = image
        self.rect = self.image.get_rect()
        # puis on positionne l'element.

        self.alive = True
        self.angle = angle
        self.direction = "top"
        element_avec_vie.__init__(self,image, x , y, vie, speed)
    def perdre_vie(self):
        self.vie -= 1

    def vie(self):
        return self.vie
        
    def deplacer(self,touches):
        touches = pygame.key.get_pressed()

        if touches [pygame.K_UP] and self.rect.y > 0:
            self.direction = "top"
            self.rect.y -= self.speed   
            self.image = pygame.transform.rotate(self.image_origin, 0)

        if touches [pygame.K_DOWN] and self.rect.y < hauteur - 64:
            self.direction = 1
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

class enemi(element_avec_vie):
    def __init__(self,img,x,y):
        element_graphique.__init__(self, img,x,y)
        self.rect.y = y
        self.rect.x = x
        self.centerx = 500
        self.centery = 60
        self.speed = 10
        self.alive = True

    def deplacer(self):
        self.rect.y += self.speed

           
class Tir(element_avec_vie) :
    def __init__(self, image, x, y) :
        element_graphique.__init__(self,image, x , y)
        self.rect.x = x
        self.rect.y = y
        self.vits = 20
        self.alive = True

    def deplacer(self, joueur):
        self.rect.y -= self.vits

        
def ajouter_missiles(joueur):
    if joueur.direction == "top":   
        missiles.append(Tir(images["MK1"],joueur.rect.x +23, joueur.rect.y -20))


def ajouter_balle(i):
    if (i%60)==0:
        tab_meteorite.append(enemi(images["balle"], randint(0,largeur), 100))
    ## Fonction pour lire les images   
def lire_image():
    images = {}
    images["perso"] = pygame.image.load("Images/medfighter.png").convert_alpha()
    images["MK1"] = pygame.image.load("Images/feu.png").convert_alpha()
    images["balle"] = pygame.image.load("Images/balle.png").convert_alpha()
    images["background"] = pygame.image.load("Images/background.png").convert_alpha()

    return images
class progress_bar(element_graphique):
    def __init__(self, x, y, width, rgb=(100, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.rgb = rgb

    def afficher(self, element, coef, fenetre):
        pygame.draw.rect(fenetre, self.rgb , (self.x, self.y, element*coef, self.width))

    def update(self, element, coef, fenetre):
        pygame.draw.rect(fenetre, self.rgb , (self.x, self.y, element*coef, self.width))



def supprime_element(tab):
    newtab = []
    for e in tab:
        if e.en_vie():
            newtab.append(e)  
    return newtab

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
largeur = 1200
hauteur = 800
fenetre = pygame.display.set_mode((largeur, hauteur))
##Fonction usuelles de base
tailleImageY = 100
tailleImageX = 100
couleurs = lire_couleur()
images = lire_image()
missiles=[]
tab_meteorite = []
##Chargement des persos 
joueur = joueur(images["perso"],550, hauteur -170,vie = 10,speed = 20 ,angle = 20)
meteorite = enemi(images["balle"], randint(0,largeur), 0)

healthbar = progress_bar(70,730,10,rgb=couleurs["rouge"])
fond = element_graphique(images["background"], 0, 0)

##Texte de l'interface
texte_health_bar = Texte('Health :', fontsize=25,x=0,y=725,rgb=couleurs["blanc"])
texte_echap = Texte('Echap pour quitter', fontsize=20,x=0,y=0,rgb=couleurs["blanc"])
texte_pause = Texte(('PAUSE '), fontsize=95,x= largeur/2,y= hauteur//3,rgb=(couleurs["noir"]))

#differents types de munitions
MK1 = Tir(images["MK1"],joueur.rect.x /2, joueur.rect.y/2)



fps = 30
timer = 0
i = 0
last_pause = -50

frame = pygame.time.Clock()

continuer = True
game_state = "jeu"
while continuer:
    timer +=1
    i+=1

    print(i)
    #recupere des événements
    touches = pygame.key.get_pressed()
    events = pygame.event.get() 

    # Max 30 FPS
    frame.tick(fps)

    # Sortie en cas de QUIT
    for event in events:    
        if event.type == QUIT:
            continuer = False

     
    
    # Debut de l'etat pause
    if game_state == "pause":
        fenetre.fill(couleurs["bleu"])
        if touches[pygame.K_p]:
            if timer - last_pause > fps/2:
                game_state = "jeu"
                last_pause = timer

        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        ##Affichage des éléments
        texte_pause.afficher(fenetre)
        texte_echap.afficher(fenetre)
        # Fin de l'etat pause

    # Debut de l'etat jeu
    if game_state == "jeu":
        
        ##Interactions utilisateur
        if touches[pygame.K_p]:
            if timer - last_pause > fps/2:
                game_state = "pause"
                last_pause = timer

        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        if touches[pygame.K_SPACE]:
            if timer - last_pause > fps/2:
                ajouter_missiles(joueur)
                last_pause = timer
        ##Déplacement des différents elements
        joueur.deplacer(touches)

        for MK1 in missiles:
            MK1.deplacer(joueur)
     
        for meteorite in tab_meteorite:
            meteorite.deplacer()

        ##Collision des différents éléments 
        for MK1 in missiles:
            for meteorite in tab_meteorite:
                meteorite.collide(MK1)
                MK1.collide(meteorite)

        for meteorite in tab_meteorite:
            if meteorite.collide(joueur):
                joueur.perdre_vie()
                print(joueur.vie)     

        ##Suppressions des éléments
        missiles = supprime_element(missiles)
        tab_meteorite = supprime_element(tab_meteorite)

        #Ajout de certains éléments
        ajouter_balle(i)

        ##Affichage des éléments
        fenetre.fill(couleurs["bleu"])
        fond.afficher(fenetre)
        healthbar.afficher((joueur.vie), 10, fenetre)
        healthbar.update((joueur.vie), 10, fenetre)
        texte_health_bar.afficher(fenetre)
        joueur.afficher(fenetre)
        texte_echap.afficher(fenetre)
        for MK1 in missiles:
            MK1.afficher(fenetre)
        for meteorite in tab_meteorite:
            meteorite.afficher(fenetre)

        # Fin de l'etat jeu

    pygame.display.flip()
pygame.quit()
