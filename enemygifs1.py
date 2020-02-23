from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame
    
#Enemy1 - tamni, gifovi

'''
Gif ima 2 brzine i isti limit za svaki prikaz:
slowAfter - najvise usporen prikaz kada je igrac stunovan
normalAfter - normalan prikaz kada igrac igra sve spellove
'''           
class EnemyGif1:
    def __init__(self, root, canvas, x, y, app, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.enemyTexts = app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
            self.hitX = x - 290 #mesto za primanje udarca
        else:
            self.enemyTexts = app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy1.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
            self.hitX = app.rootWidth - (x - 290) #mesto za primanje udarca
            
            
        self.dodgeGifs = app.dodgeGifs
        self.app = app
        
        self.slowAfter = 105
        self.normalAfter = 67
        self.after = self.normalAfter
        self.animating = True
        self.pausing = True
        self.size = 3 #najveca velicina
        
        self.animate(0)
        
    def animate(self, counter):
        if counter<len(self.sequence):
            self.canvas.itemconfig(self.image, image = self.sequence[counter])
        if not self.animating:
            return
            
        if not self.pausing and counter<len(self.sequence):
            self.root.after(self.after, lambda: self.animate(counter+1))
        else: 
            self.root.after(self.after, lambda: self.animate(0))
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
    
    def goOn(self):
        self.pausing = False
        
    def wait(self):
        return
        
    #podesavanje brzine, prikaza, ispisa i dodgea na pocetku odigravanja poteza  
    def setSpell(self, spell):
    
        if self.app.players[self.playerIndex].stunned:
            self.after = self.slowAfter
        else:
            self.after = self.normalAfter
        
        ispis = ""
        color = "white"
            
        if isinstance(spell, AttackSpell):
            if not self.app.players[self.playerIndex].stunned and spell.dodged:
                    self.dodgeGifs[1-self.playerIndex].goOn()
                    
        self.app.showText(self.enemyTexts, ispis, color)        
 
'''
Gif u pokretu koji se zaustavlja i uvecava
'''     
class EnemyAttackGif1:
    def __init__(self, root, canvas, x, y, afterTime, app, spellIndex, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.x0 = x
        self.x = x
        self.dx = 11
        self.y0 = y
        self.y = y
        self.afterTime = afterTime//2
        self.dy = app.enemyGif.size - app.playerGif.size    
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        res = 0.06 #slike u gifu se uvecavaju
        self.sequence = []
        
        if playerIndex == 1:
            self.playerTexts = self.app.playerTexts
            for img in ImageSequence.Iterator(Image.open("resources/enemy1attack.gif")):
                width, height = img.size
                image = img.resize((int(res*width), int(res*height)))
                self.sequence.append(ImageTk.PhotoImage(image)) 
                res+=0.06
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = E, state = "hidden")
        else:
            self.dx = -self.dx
            self.dy = -self.dy
            self.playerTexts = self.app.enemyTexts
            for img in ImageSequence.Iterator(Image.open("resources/enemy1attack.gif")):
                width, height = img.size
                image = img.resize((int(res*width), int(res*height)))
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                self.sequence.append(ImageTk.PhotoImage(image)) 
                res+=0.06
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = W,  state = "hidden")
            self.x0 = self.x = app.rootWidth - x
        
        self.width = self.sequence[len(self.sequence)-1].width()/2
        self.after = int(30*afterTime/1500)
        self.animating = True
        self.pausing = True
        
        self.attackSound = pygame.mixer.Sound("resources/enemy1attack.wav")
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.attackSound.set_volume(self.app.musicVolume/100)
        self.criticalHitSound.set_volume(self.app.musicVolume/100)
        self.animate(0)
                
    def animate(self, counter):
        if not self.animating:
            return
    
        if not self.pausing:  #prikazivanje
            self.canvas.itemconfig(self.image, image = self.sequence[counter])
            self.canvas.itemconfig(self.image, state="normal")
            
            #kretanje
            if counter+1<len(self.sequence) and ((self.playerIndex == 0 and self.x + self.width < self.app.enemyGif.hitX) or (self.playerIndex == 1 and self.x - self.width > self.app.playerGif.hitX)):                   
                self.x -= self.dx
                self.y += self.dy
                self.canvas.move(self.image, -self.dx, self.dy)
                
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.canvas.itemconfig(self.image, image = self.sequence[0])
                self.pausing = True
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged: 
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.playerTexts, healthText, spell.color)   
                
        else: #skrivanje
            self.canvas.itemconfig(self.image, state="hidden")
           
            
        if not self.pausing:
            self.root.after(self.after, lambda: self.animate(counter+1))
        else: self.root.after(self.after, lambda: self.animate(0))    
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.canvas.move(self.image, self.x0-self.x, self.y0-self.y)
        self.y = self.y0
        self.x = self.x0
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.attackSound.play()
        
'''
Gif koji se zaustavlja
'''            
class EnemyEnergyAttackGif1:
    def __init__(self, root, canvas, x, y, afterTime, app, spellIndex, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.playerTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1energy.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.playerTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy1energy.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
            
        self.after = int(80*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/enemy1energy.wav")
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.attackSound.set_volume(self.app.musicVolume/100)
        self.criticalHitSound.set_volume(self.app.musicVolume/100)
        self.animate(0)
        
    def animate(self, counter):
        if not self.animating:
            return
            
        if self.pausing:
            self.root.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.root.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.playerTexts, healthText, spell.color)    
                        
                self.root.after(self.after, lambda: self.animate(0))
        
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.attackSound.play()
        
'''
Gif koji se zaustavlja
'''            
class EnemyBurnAttackGif1:
    def __init__(self, root, canvas, x, y, afterTime, app, spellIndex, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.playerTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1burn.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.playerTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy1burn.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        

        self.after = int(80*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/enemy1burn.wav")
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.attackSound.set_volume(self.app.musicVolume/100)
        self.criticalHitSound.set_volume(self.app.musicVolume/100)
        self.animate(0)
        
    def animate(self, counter):
        if not self.animating:
            return
            
        if self.pausing:
            self.root.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.root.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.playerTexts, healthText, spell.color)    
                        
                self.root.after(self.after, lambda: self.animate(0))
        
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.attackSound.play()

'''
Gif koji se zaustavlja
'''    
class EnemyWeakenAttackGif1:
    def __init__(self, root, canvas, x, y, afterTime, app, spellIndex, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.playerTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1weaken.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.playerTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy1weaken.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        

        self.after = int(80*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/enemy1weaken.wav")
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.attackSound.set_volume(self.app.musicVolume/100)
        self.criticalHitSound.set_volume(self.app.musicVolume/100)
        self.animate(0)
        
    def animate(self, counter):
        if not self.animating:
            return
            
        if self.pausing:
            self.root.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.root.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.playerTexts, healthText, spell.color)    
                self.root.after(self.after, lambda: self.animate(0))
        
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.attackSound.play()
        
'''
Gif koji se neprstano vrti
'''    
class EnemyDodgeGif1:
    def __init__(self, root, canvas, x, y, app, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        
        if playerIndex == 1:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1dodge.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy1dodge.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/enemydodge.wav")
        self.sound.set_volume(app.musicVolume/100)
        self.animate(0)
        
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image = self.sequence[counter])
        if not self.animating:
            return
            
        if not self.pausing:
            self.root.after(self.after, lambda: self.animate((counter+1)%len(self.sequence)))
        else: self.root.after(self.after, lambda: self.animate(0))
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.sound.play()
        