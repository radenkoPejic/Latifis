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
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        self.spellGifs = app.enemySpellGifs
        self.enemyTexts = app.enemyTexts
        self.dodgeGifs = app.dodgeGifs
        self.app = app
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1.gif"))]
        
        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        self.slowAfter = 105
        self.normalAfter = 67
        self.after = self.normalAfter
        self.animating = True
        self.pausing = True
        self.size = 3 #najveca velicina
        self.hitX = 510 #mesto za primanje udarca
        self.animate(0)
        
    def animate(self, counter):
        if counter<len(self.sequence):
            self.canvas.itemconfig(self.image, image = self.sequence[counter])
        if not self.animating:
            return
            
        if not self.pausing and counter<len(self.sequence):
            self.parent.after(self.after, lambda: self.animate(counter+1))
        else: 
            self.parent.after(self.after, lambda: self.animate(0))
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
    
    def goOn(self):
        self.pausing = False
        
    #podesavanje brzine, prikaza, ispisa i dodgea na pocetku odigravanja poteza  
    def setSpell(self, spell):
    
        if self.app.players[1].stunned:
            self.after = self.slowAfter
        else:
            self.after = self.normalAfter
        
        ispis = ""
        color = "white"
            
        if isinstance(spell, AttackSpell):
            if not self.app.players[1].stunned and spell.dodged:
                    self.dodgeGifs[0].goOn()
                    
        self.app.showText(self.enemyTexts, ispis, color)        
        
'''
Gif u pokretu koji se zaustavlja i uvecava
'''     
class EnemyAttackGif1:
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
        self.parent = parent
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
        
        self.sequence = []
        res = 0.06 #slike u gifu se uvecavaju
        for img in ImageSequence.Iterator(Image.open("resources/enemy1attack.gif")):
            width, height = img.size
            image = img.resize((int(res*width), int(res*height)))
            self.sequence.append(ImageTk.PhotoImage(image)) 
            res+=0.06
        
        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = E)
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
            
        if self.pausing:
            self.parent.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.x -= self.dx
            self.y += self.dy
            self.canvas.move(self.image, -self.dx, self.dy)
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.parent.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[1].spells[self.spellIndex]
                
                if not self.app.players[1].stunned and not spell.dodged: 
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[0], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.app.playerTexts, healthText, spell.color)    
                        
                self.parent.after(self.after, lambda: self.animate(0))
        
    
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
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
        self.parent = parent
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1energy.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
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
            self.parent.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.parent.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[1].spells[self.spellIndex]
                
                if not self.app.players[1].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[0], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.app.playerTexts, healthText, spell.color)    
                        
                self.parent.after(self.after, lambda: self.animate(0))
        
    
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
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
        self.parent = parent
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1burn.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
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
            self.parent.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.parent.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[1].spells[self.spellIndex]
                
                if not self.app.players[1].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[0], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.app.playerTexts, healthText, spell.color)    
                        
                self.parent.after(self.after, lambda: self.animate(0))
        
    
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
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
        self.parent = parent
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1weaken.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
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
            self.parent.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.parent.after(self.after, lambda: self.animate(counter+1))
            else: #zaustavljanje i prikazivanje posledica udara
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[1].spells[self.spellIndex]
                
                if not self.app.players[1].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[0], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.app.playerTexts, healthText, spell.color)    
                self.parent.after(self.after, lambda: self.animate(0))
        
    
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
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1dodge.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
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
            self.parent.after(self.after, lambda: self.animate((counter+1)%len(self.sequence)))
        else: self.parent.after(self.after, lambda: self.animate(0))
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.sound.play()
        