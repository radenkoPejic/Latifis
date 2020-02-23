from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame

#Enemy2 - tamni, gifovi

'''
Gif ima 2 brzine i isti limit za svaki prikaz:
slowAfter - najvise usporen prikaz kada je igrac stunovan
normalAfter - normalan prikaz kada igrac igra sve spellove
'''   
class EnemyGif2:
    def __init__(self, root, canvas, x, y, app, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.enemyTexts = app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
            self.hitX = x - 290 #mesto za primanje udarca
        else:
            self.enemyTexts = app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy2.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
            self.hitX = app.rootWidth - x + 290 #mesto za primanje udarca
        

        self.dodgeGifs = app.dodgeGifs
        self.app = app  
 
        self.slowAfter = 110
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
Gif koji se zaustavlja a na pocetku prikazuje posledice udara
'''                       
class EnemyAttackGif2:
    def __init__(self, root, canvas, x, y, app, spellIndex, playerIndex = 1):
        self.root = root
        self.canvas = canvas
            
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.playerTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2attack.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.playerTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy2attack.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
        
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/enemy2attack.wav")
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.attackSound.set_volume(self.app.musicVolume/100)
        self.criticalHitSound.set_volume(self.app.musicVolume/100)
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
        self.attackSound.play()
        spell = self.app.players[self.playerIndex].spells[self.spellIndex]
        ispis = ""

        if not self.app.players[self.playerIndex].stunned and not spell.dodged: #prikazivanje posledice udara
            if spell.criticalHit:
                self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                self.criticalHitSound.play()
            ispis = str(int(-spell.damageDone))
        
        self.app.showText(self.playerTexts, ispis, spell.color)    

'''
Gif koji se neprstano vrti
'''   
class EnemyHealGif2:
    def __init__(self, root, canvas, x, y, app, playerIndex = 1):
        self.root = root
        self.canvas = canvas
                
        if playerIndex == 1:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2heal.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy2heal.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/enemy2heal.wav")
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

'''
Gif koji se neprstano vrti
'''           
class EnemyRewindGif2:
    def __init__(self, root, canvas, x, y, app, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        
        if playerIndex == 1:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2rewind.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy2rewind.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/enemy2rewind.wav")
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

'''
Gif koji se zaustavlja
'''  
class EnemyWeakenAttackGif2:
    def __init__(self, root, canvas, x, y, afterTime, app, spellIndex, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if playerIndex == 1:
            self.playerTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2weaken.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.playerTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy2weaken.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
        
        self.after = int(100*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/enemy2weaken.wav")
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
            else:
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged: #zaustavljanje i prikazivanje posledica udara
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
class EnemyDodgeGif2:
    def __init__(self, root, canvas, x, y, app, playerIndex = 1):
        self.root = root
        self.canvas = canvas
        
        if playerIndex == 1:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2dodge.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/enemy2dodge.gif"))]
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
