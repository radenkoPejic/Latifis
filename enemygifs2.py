from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame


class EnemyGif2:
    def __init__(self, parent, canvas, x, y, players, spellGifs, playerText, enemyText, dodgeGifs, criticalImages, app):
        self.parent = parent
        self.canvas = canvas
        self.spellGifs = spellGifs
        self.playerText = playerText
        self.enemyText = enemyText
        self.dodgeGifs = dodgeGifs
        self.players = players
        self.criticalImages = criticalImages
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        self.normalAfter = 67
        self.after = self.normalAfter
        self.slowAfter = 110
        self.animating = True
        self.pausing = True
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.criticalHitSound.set_volume(app.musicVolume/100)
        self.size = 3
        self.hitX = 510
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
    
    def setSpell(self, spell):
        
        self.dodgeGifs[1].pause()
            
        self.canvas.itemconfig(self.enemyText, text = "", fill = "white")
        self.canvas.itemconfig(self.criticalImages[1], state = "hidden")
        
        self.canvas.itemconfig(self.playerText, text = "")
        self.canvas.itemconfig(self.criticalImages[0], state = "hidden")
            
        if isinstance(spell, AttackSpell):
            ispis = ""

            if not self.players[1].stunned:
                if spell.dodged:
                    self.dodgeGifs[0].goOn()
                else:
                    if spell.criticalHit:
                        self.canvas.itemconfig(self.criticalImages[0], state = "normal")
                        self.criticalHitSound.play()
                    ispis = str(int(-spell.damageDone))
            
            self.canvas.itemconfig(self.playerText, text = ispis, fill = spell.color)
        elif isinstance(spell, Stun):
            if spell.dodged:
                self.dodgeGifs[1].goOn()
            #else: 
                #self.app.enemyGif.after = self.app.enemyGif.slowAfter


class EnemyAttackGif2:
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2attack.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/enemy2attack.wav")
        self.attackSound.set_volume(app.musicVolume/100)
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
        self.attackSound.play()

class EnemyHealGif2:
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2heal.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
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
        
class EnemyDodgeGif2:
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2dodge.gif"))]

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
        
class EnemyRewindGif2:
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2rewind.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
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

class EnemyWeakenAttackGif2:
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
        self.parent = parent
        self.canvas = canvas
        self.afterTime = afterTime//2
            
        self.app = app
        self.spell = self.app.players[1].spells[spellIndex]
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy2weaken.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        self.after = int(100*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.enabled = False
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
            self.parent.after(self.after, lambda: self.animate(0))
            
        elif not self.pausing:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])

            if counter+1<len(self.sequence):
                self.parent.after(self.after, lambda: self.animate(counter+1))
            else:
                self.canvas.itemconfig(self.image, state="hidden")
                self.pausing = True
                
                if not self.app.players[1].stunned and not self.spell.dodged: #zaustavljanje i prikazivanje posledica udara
                    if self.spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[0], state = "normal")
                    healthText = str(int(-self.spell.damageDone))
                    self.canvas.itemconfig(self.app.playerText, text = healthText, fill = self.spell.color)
                        
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
        
    def enable(self):
        self.enabled = True

