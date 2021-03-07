import pygame  
from random import *
from pygame.locals import *
import math

  
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
    
class element_graphique_anime(element_avec_vie):

    def __init__(self, images, x=0, y=0, vie = 0, speed=0):
        # Pour construire un element animé, on construit
        # d'abord un element graphique (avec la premiere image de la liste)
        super().__init__(images[0],x,y, vie, speed)

        # On ajoute toutes les variables utiles a la gestion de l'animation
        self.images = images
        self.timer = 0  # un timer pour l'animation
        self.numAnim = 0 # le numero de l'image courante
        self.vie = 3

    def afficher(self,fenetre) :
        self.timer+=1
        if self.timer > 10: # on change d'image tous les 10 tours de boucles...
            self.timer = 0
            self.numAnim+=1
            if self.numAnim >= len(self.images):
                self.numAnim=0
            self.image = self.images[self.numAnim]

        super().afficher(fenetre)

class boss_anime(element_graphique_anime):

    def __init__(self,  images, x=0, y=0):
        # Pour construire un element animé, on construit
        # d'abord un element animé
        super().__init__(images,x,y)

        self.t = 0.0
        self.truc = 20
        self.centerx = x
        self.centery = y

    def deplacer(self):
        self.t+=1.0
        self.rect.x = 500*math.cos(self.t/self.truc) + self.centerx 
        self.rect.y = 100*math.sin(1.5*self.t/self.truc) + self.centery


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
    def __init__(self, image, x , y, vie = 10, speed = 15):
        element_avec_vie.__init__(self,image, x , y, vie, speed)
        self.image = self.image_origin = image
        self.rect = self.image.get_rect()
        # puis on positionne l'element.
        self.rect.x = x
        self.rect.y =y
        self.alive = True
        self.chargeur = 10
        self.score = 0
    def perdre_vie(self):
        self.vie -= 1

    def vie(self):
        return self.vie

    def chargeur(self):
        return self.chargeur

    def reload(self):
        self.chargeur = 10
        
    def shoot(self):
        self.chargeur -= 1
    
    def score(self):
        return self.score

    def deplacer(self,touches):
        if touches [pygame.K_RIGHT] and self.rect.x < largeur  - 64:
            self.direction = "right"
            self.rect.x += self.speed

        if touches [pygame.K_LEFT] and self.rect.x > 0:
            self.direction = "left"
            self.rect.x -= self.speed 

##=====Element Graphique enemi=====##
class enemi(element_avec_vie):
    def __init__(self,img,x,y, vie, speed):
        element_avec_vie.__init__(self, img,x,y, vie, speed)
        self.rect.y = y
        self.rect.x = x
        self.vie = vie
        self.speed = speed
        self.alive = True

    def deplacer(self):
        if  self.rect.y < hauteur - 85:
            self.rect.y += self.speed
        else:
            self.alive = False

##=====Element Graphique enemi teleguide=====##    
class enemi_teleguide(element_avec_vie):
    def __init__(self,img,x,y, vie, speed):
        element_avec_vie.__init__(self, img,x,y, vie, speed)
        self.rect.y = y
        self.rect.x = x
        self.vie = vie
        self.speed = speed
        self.alive = True

    def deplacer(self,joueur):
        dx = joueur.rect.x - self.rect.x
        dy = joueur.rect.y - self.rect.y

        if dx>0:
            self.rect.x+=self.speed
        if dx <0:
            self.rect.x-=self.speed

        if dy>0:
            self.rect.y+=self.speed
        if dy <0:
            self.rect.y-=self.speed

##=====Element Graphique Pour les tirs=====##
class tir_haut(element_avec_vie) :
    def __init__(self, image, x, y, vie = 1, speed = 20) :
        element_avec_vie.__init__(self,image, x , y, vie, speed)
        self.rect.x = x
        self.rect.y = y
        self.speed = 20
        self.vie = vie
        self.alive = True
        self.nom = 'MK1'

    def deplacer(self, joueur):
        self.rect.y -= self.speed

    def nom(self):
        return self.nom

##=====Element Graphique Pour les tirs=====##
class tir_gauche(element_avec_vie):
    def __init__(self, image, x, y, vie = 1, speed = 20) :
        element_avec_vie.__init__(self,image, x , y, vie, speed)
        self.rect.x = x
        self.rect.y = y
        self.speed = 25
        self.vie = vie
        self.alive = True
        self.nom = 'MK2'

    def nom(self):
        return self.nom

    def deplacer(self, joueur):
        self.rect.x -= self.speed

##=====Element Graphique Pour les tirs=====##
class tir_droite(element_avec_vie):
    def __init__(self, image, x, y, vie = 1, speed = 20) :
        element_avec_vie.__init__(self,image, x , y, vie, speed)
        self.rect.x = x
        self.rect.y = y
        self.speed = 25
        self.vie = vie
        self.alive = True
        self.nom = 'MK3'

    def nom(self):
        return self.nom

    def deplacer(self, joueur):
        self.rect.x += self.speed


##=====Element Graphique progress bar=====##
class progress_bar(element_graphique):
    def __init__(self, x=0, y=0, width=0, rgb=(100, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.rgb = rgb

    def afficher(self, element, coef, fenetre):
        pygame.draw.rect(fenetre, self.rgb , (self.x, self.y, element*coef, self.width))

    def update(self, element, coef, fenetre):
        pygame.draw.rect(fenetre, self.rgb , (self.x, self.y, element*coef, self.width))


class bouton(element_graphique):
    def __init__(self, x,y,width,height, rgb=(100, 255, 255), text=''):
        self.rgb = rgb
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def afficher(self,fenetre,outline):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(fenetre, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(fenetre, self.rgb, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, 1, (0,0,0))
            fenetre.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    def isClicked(self, pos):
        if self.isOver(pos_mouse):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True    
        return False

##=====FONCTIONS SIMPLE=====##
def ajouter_missiles(joueur, tir):
    if tir.nom == 'MK1':
        MK1s.append(tir_haut(images["MK1"],joueur.rect.x -20 + joueur.rect.w//2 ,joueur.rect.y - 30))
        joueur.shoot()

    if tir.nom == 'MK2':
        MK2s.append(tir_gauche(images["MK1"],joueur.rect.x -20 + joueur.rect.w//2 ,joueur.rect.y - 30))
        joueur.shoot()

    if tir.nom == 'MK3':
        MK3s.append(tir_droite(images["MK1"],joueur.rect.x -20 + joueur.rect.w//2 ,joueur.rect.y - 30))
        joueur.shoot()

## Ajout des enemis
def ajouter_objet(i):
    if (i%30)==0:
        tab_meteorite.append(enemi(images["balle"], randint(0,largeur), 100,1, 10))
    
    if (i%60)==0:
        kamikazes.append(enemi_teleguide(images["balle"], randint(0,largeur), 0, 1, 5))
def ajouter_objet_anime(balles, images, compteur, fps, duree):
  if compteur/fps % duree==0:
    boss.append(boss_anime(images["flame"], largeur/2, 100))

## Fonction pour lire les images   
def lire_image():
    images = {}
    images["perso"] = pygame.image.load("Images/Ships/medfrighter.png").convert_alpha() 

    images["flame"] = []
    for i in range(4):
        images["flame"].append(pygame.image.load("Images/monster/monsterParts-0"+str(i)+".png").convert_alpha())

    images["MK1"] = pygame.image.load("Images/feu.png").convert_alpha()
    images["balle"] = pygame.image.load("Images/enemy.png").convert_alpha()
    images["background"] = pygame.image.load("Images/background.png").convert_alpha()
    images["background_menu"] = pygame.image.load("Images/background_menu.png").convert_alpha()


    return images

## Suppression de certains elements
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
    couleurs["gris_clair"] = (171,171,171)
    couleurs["jaune_vif"] = (255,246,49)
    couleurs["vert_clair_vif"] = (99,255,49)
    couleurs["marron"] = (110,44,0)

    return couleurs


pygame.init()

## initialisation de la fenetre 
largeur = 1200
hauteur = 800
fenetre = pygame.display.set_mode((largeur, hauteur))

## Fonction de lecture 
couleurs = lire_couleur()
images = lire_image()

## Conteneur pour les objets
MK1s=[]
MK2s=[]
MK3s=[]
boss =[]
kamikazes = []
tab_meteorite = []

##Chargement des persos 
joueur = joueur(images["perso"], largeur//2 - 64, hauteur - 170 ,vie = 10,speed = 20 )
meteorite = enemi(images["balle"], randint(0,largeur), 0, 1, 20)
kamikaze = enemi_teleguide(images["balle"], 0,0,0,0)
## Bars du jeu
healthbar = progress_bar(70,730,10,rgb=couleurs["rouge"])
chargeur_missile =progress_bar(80,760,10,rgb=couleurs["marron"])
fond = element_graphique(images["background"], 0, 0)
fond_menu = element_graphique(images["background_menu"], 0, 0)


## Boutons de l'interface
bouton_jeu = bouton( largeur//3, hauteur//3, 400, 50,  rgb=(100, 255, 255), text='JOUER')
bouton_htp =bouton ( largeur//3, hauteur//1.8, 400, 50,  rgb=(100, 255, 255), text='TOUCHES')
bouton_cdt =bouton ( largeur//3, hauteur//2.25, 400, 50,  rgb=(100, 255, 255), text='CREDIT')
bouton_quit = bouton( largeur//3, hauteur//1.5, 400, 50,  rgb=(100, 255, 255), text='QUITTER')

bouton_menu =bouton ( largeur//3, hauteur//1.8, 400, 50,  rgb=(100, 255, 255), text='MENU')
bouton_end = bouton( largeur//3, hauteur//2.25, 400, 50,  rgb=(100, 255, 255), text='QUITTER')

bouton_z =  bouton( 300, 200, 400, 40,  rgb=couleurs["blanc"], text='Z (Vers le haut)')
bouton_q =  bouton( 500, 243, 400, 40,  rgb=couleurs["blanc"], text='Q (Vers la gauche)')
bouton_d =  bouton( 100, 243, 400, 40,  rgb=couleurs["blanc"], text='D (Vers la droite)')



##Texte de l'interface
#Texte du menu
texte_titre_jeu = Texte('SPACE INVADERS', fontsize= 100, x=largeur//4, y = hauteur//8, rgb=(couleurs["blanc"]))

#Texte du jeu
texte_health_bar = Texte('Vie :', fontsize=25,x=0,y=725,rgb=couleurs["noir"])
texte_chargeur = Texte('Missiles :', fontsize=25,x=0,y=755,rgb=couleurs["noir"])
texte_echap = Texte('Echap pour quitter', fontsize=20,x=0,y=0,rgb=couleurs["blanc"])
texte_reload = Texte('R pour recharger les missiles', fontsize=25,x=500,y=725,rgb=couleurs["noir"])

#Texte de la pause 
texte_pause = Texte(('PAUSE '), fontsize=95,x= largeur/2,y= hauteur//3,rgb=(couleurs["noir"]))

#Texte de l'option
texte_option = Texte(('TOUCHES'), fontsize=50,x= 0,y= 25,rgb=(couleurs["noir"]))
texte_deplacer = Texte(('Vous devez vous deplacer avec les fleches directionnelles.'), fontsize=50,x= 0,y=150,rgb=(couleurs["noir"]))
texte_tir = Texte(('Pour tirer :'), fontsize=50,x= 0,y=200,rgb=(couleurs["noir"]))
texte_retour = Texte('Tab pour retourner dans le menu', fontsize=20,x= 0,y=hauteur - 20,rgb=couleurs["blanc"])

#Texte du Go
texte_GO = Texte('GAME OVER', fontsize= 100, x=largeur//2.9, y = hauteur//8, rgb=(couleurs["blanc"]))


#differents types de munitions
MK1 = tir_haut(images["MK1"],joueur.rect.w /2, joueur.rect.h/2)
MK2 = tir_gauche(images["MK1"],joueur.rect.w /2, joueur.rect.h/2)
MK3 = tir_droite(images["MK1"],joueur.rect.w /2, joueur.rect.h/2)




fps = 30
timer = 0
i = 0
level = 1
nombre_enemi = 10
last_pause = -50

frame = pygame.time.Clock()

continuer = True
game_state = "menu"
while continuer:
    timer +=1
    i+=1

    #recupere des événements
    touches = pygame.key.get_pressed()
    events = pygame.event.get() 
    pos_mouse = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()


    # Max 30 FPS
    frame.tick(fps)

    # Sortie en cas de QUIT
    for event in events:    
        if event.type == QUIT:
            continuer = False

     
    # Debut de l'etat menu
    if game_state == "menu":
        
        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
            
        ## Bouton du jeu
        if bouton_jeu.isOver(pos_mouse):
            bouton_jeu.rgb = couleurs["jaune_vif"]
            if bouton_jeu.isClicked(pos_mouse):
                ## Pour eviter le click intensif (ca peut etre necessaire).
                if timer - last_pause > fps/2:
                    game_state = "jeu"
                last_pause = timer
        else:
            bouton_jeu.rgb = couleurs["blanc"]

        ## Bouton pour quitter
        if bouton_quit.isOver(pos_mouse):
            bouton_quit.rgb = couleurs["vert_clair_vif"]
            if bouton_quit.isClicked(pos_mouse):
                ## Pour eviter le click intensif (ca peut etre necessaire).
                    continuer = False
        else:
            bouton_quit.rgb = couleurs["blanc"]

         ## Bouton pour option
        if bouton_htp.isOver(pos_mouse):
            bouton_htp.rgb = couleurs["vert_clair_vif"]
            if bouton_htp.isClicked(pos_mouse):
                ## Pour eviter le click intensif (ca peut etre necessaire).
                    game_state = "touches"
        else:
            bouton_htp.rgb = couleurs["blanc"]

       
        ##Affichage des éléments
        fond_menu.afficher(fenetre)
        texte_titre_jeu.afficher(fenetre)
        texte_echap.afficher(fenetre)
        bouton_jeu.afficher(fenetre, 1)
        bouton_quit.afficher(fenetre, 1)
        bouton_htp.afficher(fenetre, 1)
        bouton_cdt.afficher(fenetre, 1)


        # Fin de l'etat menu

    # Debut de l'etat option
    if game_state == "touches":
        fenetre.fill(couleurs["gris_clair"])

        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
        
        if touches[pygame.K_TAB]:
            game_state = "menu"

        size = (50, 50)
        line = pygame.Surface(size)
        texte_echap.afficher(fenetre)
        texte_deplacer.afficher(fenetre)
        texte_option.afficher(fenetre)
        texte_tir.afficher(fenetre)
        texte_retour.afficher(fenetre)

        pygame.draw.rect(fenetre,couleurs["noir"],(0,60,largeur,5))
        bouton_q.afficher(fenetre,1)
        bouton_z.afficher(fenetre,1)
        bouton_d.afficher(fenetre,1)

        #Fin de l'etat option

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

        ##Interractions clavier
        if touches[pygame.K_p]:
            if timer - last_pause > fps/2:
                game_state = "pause"
                last_pause = timer

        if joueur.chargeur > 0:
            if touches[pygame.K_z]:
                if timer - last_pause > fps/2:
                    ajouter_missiles(joueur, MK1)
                    last_pause = timer

            if touches[pygame.K_q]:
                if timer - last_pause > fps/2:
                    ajouter_missiles(joueur, MK2)
                    last_pause = timer

            if touches[pygame.K_d]:
                if timer - last_pause > fps/2:
                    ajouter_missiles(joueur, MK3)
                    last_pause = timer

        if touches[pygame.K_r] and joueur.chargeur == 0:
            joueur.reload()  

        if touches[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        ##Déplacement des différents elements
        joueur.deplacer(touches)

        for b in boss:
            b.deplacer()

        for MK1 in MK1s:
            MK1.deplacer(joueur)
        
        for MK2 in MK2s:
            MK2.deplacer(joueur)

        for MK3 in MK3s:
            MK3.deplacer(joueur)

        for meteorite in tab_meteorite:
            meteorite.deplacer()

        for kamikaze in kamikazes:
            kamikaze.deplacer(joueur)
        ##Collision des différents éléments 
        for MK1 in MK1s:
            for meteorite in tab_meteorite:
                meteorite.collide(MK1)
                MK1.collide(meteorite)

        for MK2 in MK2s:
            for meteorite in tab_meteorite:
                meteorite.collide(MK2)
                MK2.collide(meteorite)

        for MK3 in MK3s:
            for meteorite in tab_meteorite:
                meteorite.collide(MK3)
                MK3.collide(meteorite)

        for meteorite in tab_meteorite:
            if meteorite.collide(joueur):
                joueur.perdre_vie()
                print(joueur.vie) 
         

        for kamikaze in kamikazes:
            if kamikaze.collide(joueur):
                joueur.perdre_vie()
                print(joueur.vie)      
        ##Condition de fin de jeu
        if joueur.vie == 0:
            game_state ="game_over"
        ##Suppression des éléments
        MK1s = supprime_element(MK1s)
        MK2s = supprime_element(MK2s)
        MK3s = supprime_element(MK3s)


        tab_meteorite = supprime_element(tab_meteorite)
        kamikazes = supprime_element(kamikazes)

        ##Ajout des éléments
        ajouter_objet(i)

        if len(boss) < 1:   
            ajouter_objet_anime(boss, images, i, 50, 1)

        
        ##Affichage des éléments
        fenetre.fill(couleurs["gris_clair"])
        fond.afficher(fenetre)
        
        healthbar.afficher((joueur.vie), 10, fenetre)
        healthbar.update((joueur.vie), 10, fenetre)

        chargeur_missile.afficher((joueur.chargeur), 10, fenetre)
        chargeur_missile.update((joueur.chargeur), 10, fenetre)
        if joueur.chargeur == 0:
            texte_reload.afficher(fenetre)
        texte_health_bar.afficher(fenetre)
        joueur.afficher(fenetre)
        texte_chargeur.afficher(fenetre)
        texte_echap.afficher(fenetre)
        kamikaze.afficher(fenetre)


        for b in boss:
            b.afficher(fenetre)
        for MK1 in MK1s:
            MK1.afficher(fenetre)

        for MK2 in MK2s:
            MK2.afficher(fenetre)

        for MK3 in MK3s:
            MK3.afficher(fenetre)

        for meteorite in tab_meteorite:
            meteorite.afficher(fenetre)
        
        # Fin de l'etat jeu
    if game_state == "game_over":
        
         ## Bouton pour option
        if bouton_end.isOver(pos_mouse):
            bouton_end.rgb = couleurs["vert_clair_vif"]
            if bouton_end.isClicked(pos_mouse):
                pygame.quit()
                quit()
        else:
            bouton_end.rgb = couleurs["blanc"]

       
        ##Affichage des éléments
        fenetre.fill(couleurs["gris_clair"])
        texte_GO.afficher(fenetre)
        bouton_end.afficher(fenetre, 1)


    pygame.display.flip()

pygame.quit()
