from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame

class PlayerGif1:
    def __init__(self, parent, canvas, x, y, afterTime, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        self.sequence = []
        self.afterTime = afterTime
        self.playerIndex = playerIndex
        
        if playerIndex == 0:
            self.playerSpellGifs = app.playerSpellGifs
            self.playerText = app.playerText
            self.enemyGif = app.enemyGif
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player1.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
            self.hitX = x - 10
        else:
            self.playerSpellGifs = app.enemySpellGifs
            self.playerText = app.enemyText
            self.enemyGif = app.playerGif
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player1.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
            self.hitX = app.rootWidth - x + 5
    
        self.maxLimit = len(self.sequence)
        self.midLimit = 30
        self.launchLimit = 31
        self.enableLimit = 45
        self.limit = self.maxLimit
       
        self.dodgeGifs = app.dodgeGifs
        self.criticalImages = app.criticalImages
        self.app = app
        
        self.after = afterTime//len(self.sequence)
        self.slowAfter = (self.afterTime//len(self.sequence))*4
        self.animating = True
        self.pausing = True
        self.size = 1
        self.animate(0)
        
    def animate(self, counter):
        if counter<self.limit:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])
            
        if counter == self.launchLimit: #pokretanje zvuka
            self.playerSpellGifs[0].launch()    
        elif counter == self.enableLimit: #pokretanje gifa
            self.playerSpellGifs[0].enable()
            
        if not self.animating:
            return
        
        if self.pausing or self.limit==counter==self.midLimit: 
            self.parent.after(self.after, lambda: self.animate(0))
        else:
            self.parent.after(self.after, lambda: self.animate(counter+1))
    
    def stop(self):
        self.animating = False
        
    def pause(self):
        self.pausing = True
    
    def goOn(self):
        self.pausing = False
    
    def wait(self):
        self.limit = self.midLimit
        self.after = (self.afterTime//len(self.sequence))*4
        self.pausing = False
        
    def setSpell(self, spell):
        
        self.dodgeGifs[self.playerIndex].pause()
        
        self.limit = self.midLimit
        self.after = (self.afterTime//len(self.sequence))*3
        

        ispis = ""
        color = "white"
        
        self.canvas.itemconfig(self.criticalImages[self.playerIndex], state = "hidden")
            
        if isinstance(spell, AttackSpell):
            if not self.app.players[self.playerIndex].stunned:
                self.limit = self.maxLimit
                self.after = self.afterTime//len(self.sequence)
                if spell.dodged:
                    self.dodgeGifs[1-self.playerIndex].goOn()
            
        elif isinstance(spell, Charge):
            ispis = spell.bonus
            color = spell.color
        
        elif isinstance(spell, Heal):
            ispis = spell.health
            color = spell.color
        
        elif isinstance(spell, Stun):
            if spell.dodged:
                self.dodgeGifs[1-self.playerIndex].goOn()
            else: 
                self.app.enemyGif.after = self.app.enemyGif.slowAfter
            
        self.canvas.itemconfig(self.playerText, text = ispis, fill = color)
            

class PlayerWinnerGif1:
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player1winner.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = NW)
        self.after = 67
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/playerwinner.wav")
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
        self.canvas.pack_forget()
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.pack()
        self.canvas.itemconfig(self.image, state="normal")
        self.sound.play()
        

class PlayerAttackGif1:
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex, playerIndex = 0):
        self.parent = parent
        self.canvas = app.backgroundCanvas
        self.x0 = x
        self.x = x
        self.dx = 15
        self.y0 = y
        self.y = y
        self.dy = app.enemyGif.size - app.playerGif.size
        self.afterTime = afterTime//2
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if self.playerIndex == 0:
            self.enemyText = self.app.enemyText
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/fireball.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.dx = -self.dx
            self.dy = -self.dy
            self.enemyText = self.app.playerText
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/fireball.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
            self.x0 = self.x = app.rootWidth - x
        
        self.after = int(30*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.enabled = False
        
        self.launchSound = pygame.mixer.Sound("resources/player1launch.wav")
        self.hitSound = pygame.mixer.Sound("resources/player1hit.wav")
        self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
        self.launchSound.set_volume(self.app.musicVolume/100)
        self.hitSound.set_volume(self.app.musicVolume/100)
        self.criticalHitSound.set_volume(self.app.musicVolume/100)
    
        self.animate(0)
        
    def animate(self, counter):
        if not self.animating:
            return
    
        if self.enabled and not self.pausing: #prikazivanje
            self.canvas.itemconfig(self.image, state="normal")
            self.canvas.itemconfig(self.image, image = self.sequence[counter])
            spell = self.app.players[self.playerIndex].spells[self.spellIndex]

            #kretanje
            if (self.playerIndex == 0 and self.x < self.app.enemyGif.hitX) or (self.playerIndex == 1 and self.x > self.app.playerGif.hitX):
                self.x += self.dx 
                self.y -= self.dy
                self.canvas.move(self.image, self.dx, -self.dy)
                
            else: #zaustavljanje i prikazivanje posledica udara
                if not self.app.players[self.playerIndex].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    else:
                        self.hitSound.play()
                    healthText = str(int(-spell.damageDone))
                    self.canvas.itemconfig(self.enemyText, text = healthText, fill = spell.color)
                
                self.enabled = False
        else: #skrivanje
            self.canvas.itemconfig(self.image, state="hidden")
           
            
        if self.enabled and not self.pausing:
            self.parent.after(self.after, lambda: self.animate((counter+1)%len(self.sequence)))
        else: self.parent.after(self.after, lambda: self.animate(0))
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.canvas.move(self.image, self.x0-self.x, self.y0-self.y)#povratak na pocetak
        self.y = self.y0
        self.x = self.x0
        self.pausing = True
        self.enabled = False
        
    def goOn(self):
        self.pausing = False
        
    def enable(self):
        self.enabled = True
        
    def launch(self):
        self.launchSound.play()
        
    
class PlayerHealGif1:
    def __init__(self, parent, canvas, x, y, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/healing.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/healing.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player1heal.wav")
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
        
        
class PlayerChargeGif1:
    def __init__(self, parent, canvas, x, y, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/charging.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/charging.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player1charge.wav")
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



class PlayerStunGif1:
    def __init__(self, parent, canvas, x, y, afterTime, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/stued.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/stued.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        self.after = int(67*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player1stun.wav")
        self.sound.set_volume(app.musicVolume/100)
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
                self.parent.after(self.after, lambda: self.animate(0))
        
        
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
    
    def goOn(self):
        self.pausing = False
        self.canvas.itemconfig(self.image, state="normal")
        self.sound.play()
        

class PlayerDodgeGif1:
    def __init__(self, parent, canvas, x, y, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/playerDodge.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/playerDodge.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        #self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player1dodge.wav")
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
        
        