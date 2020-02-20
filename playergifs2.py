from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame

#Charizard X - sivo-plavi, gifovi koji mogu biti flipovani u zavisnosti od playerIndexa

'''
Gif ima 4 brzine:
slowAfter - najvise usporen prikaz kada je igrac stunovan
waitAfter - usporen prikaz dok igrac ne odabere spell
normalAfter - normalan prikaz kada igrac igra obicne spellove
fastAfter - brzi prikaz kada igrac napada

Gif ima dva prikaza:
maxLimit - prikaz kada je igrac napao i ispalio kuglu
midLimit - osnovni prikaz
'''    
class PlayerGif2:
    def __init__(self, parent, canvas, x, y, afterTime, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        self.sequence = []
        self.afterTime = afterTime
        self.playerIndex = playerIndex
        
        if playerIndex == 0:
            self.playerSpellGifs = app.playerSpellGifs
            self.playerTexts = app.playerTexts
            self.enemyGif = app.enemyGif
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
            self.hitX = x - 15
        else:
            self.playerSpellGifs = app.enemySpellGifs
            self.playerTexts = app.enemyTexts
            self.enemyGif = app.playerGif
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player2.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
            self.hitX = app.rootWidth - x + 15 #mesto za primanje udarca
        
        self.maxLimit = len(self.sequence)
        self.midLimit = 7
        self.enableLimit = 10
        self.limit = self.maxLimit
        
        self.dodgeGifs = app.dodgeGifs
        self.criticalImages = app.criticalImages
        self.app = app
        
        self.slowAfter = (self.afterTime//len(self.sequence))*2-3
        self.waitAfter = (self.afterTime//len(self.sequence))*2-3
        self.normalAfter = (self.afterTime//len(self.sequence))*2-4
        self.fastAfter = self.afterTime//len(self.sequence)
        self.after = self.normalAfter
        self.animating = True
        self.pausing = True
        self.size = 1 #najmanja velicina
        self.animate(0)
        
    def animate(self, counter):
        if counter<self.limit:
            self.canvas.itemconfig(self.image, image = self.sequence[counter])
            
        if counter == self.enableLimit: #pokretanje animacije i zvuka?
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
        self.after = self.waitAfter
        self.pausing = False

    #podesavanje brzine, prikaza, ispisa i dodgea na pocetku odigravanja poteza          
    def setSpell(self, spell):
        
        self.limit = self.midLimit
        if self.app.players[self.playerIndex].stunned:
            self.after = self.slowAfter
        else:
            self.after = self.normalAfter

        ispis = ""
        color = "white"
        
        if not self.app.players[self.playerIndex].stunned:         
            if isinstance(spell, AttackSpell):
                self.limit = self.maxLimit
                self.after = self.fastAfter
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
            
        self.app.showText(self.playerTexts, ispis, color)
        
'''
Gif koji se zaustavlja i iskace preko celog ekrana nakon sto je igrac pobedio u borbi
'''
class PlayerWinnerGif2:
    def __init__(self, parent, canvas, x, y, app):
        self.parent = parent
        self.canvas = canvas
        
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2winner.gif"))]

        self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = NW)
        self.after = 67
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/playerwinner.wav")
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
                self.pausing = True
                self.parent.after(self.after, lambda: self.animate(0))
             
    
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
        
'''
Gif u pokretu koji se zaustavlja sa zvukom pri ispaljivanju i pogotku 
'''        
class PlayerAttackGif2:
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        self.x0 = x
        self.x = x
        self.dx = 11
        self.y0 = y
        self.y = y
        self.dy = app.enemyGif.size - app.playerGif.size
        self.afterTime = afterTime//2
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if self.playerIndex == 0:
            self.enemyTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2attack.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.dx = -self.dx
            self.dy = -self.dy
            self.enemyTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player2attack.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
            self.x0 = self.x = app.rootWidth - x
        
        self.after = int(35*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.enabled = False
        
        self.launchSound = pygame.mixer.Sound("resources/player2launch.wav")
        self.hitSound = pygame.mixer.Sound("resources/playerhit.wav")
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

            #kretanje
            if (self.playerIndex == 0 and self.x < self.app.enemyGif.hitX) or (self.playerIndex == 1 and self.x > self.app.playerGif.hitX):
                self.x += self.dx 
                self.y -= self.dy
                self.canvas.move(self.image, self.dx, -self.dy)
                
            else: #zaustavljanje i prikazivanje posledica udara
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged:
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    else:
                        self.hitSound.play()
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.enemyTexts, healthText, spell.color)
                
                self.enabled = False
        else: #skrivanje
            self.canvas.itemconfig(self.image, state="hidden")
           
            
        if self.enabled and not self.pausing:
            self.parent.after(self.after, lambda: self.animate((counter+1)%len(self.sequence)))
        else: self.parent.after(self.after, lambda: self.animate(0))
    
    def stop(self):
        self.animating = False
    
    def pause(self):
        self.canvas.move(self.image, self.x0-self.x, self.y0-self.y)
        self.y = self.y0
        self.x = self.x0
        self.pausing = True
        self.enabled = False
    
    def goOn(self):
        self.pausing = False
        self.launchSound.play()#
        
    def enable(self):
        self.enabled = True
        
'''
Gif koji se neprstano vrti
'''            
class PlayerFlexGif2:
    def __init__(self, parent, canvas, x, y, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2flex.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player2flex.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player2flex.wav")
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

'''
Gif koji se neprstano vrti
'''    
class PlayerChargeGif2:
    def __init__(self, parent, canvas, x, y, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2charge.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player2charge.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)
        
        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player2charge.wav")
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
        
'''
Gif koji se zaustavlja
'''        
class PlayerDrainGif2:
    def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas   
        self.app = app
        self.spellIndex = spellIndex
        self.playerIndex = playerIndex
        
        if playerIndex == 0:
            self.enemyTexts = self.app.enemyTexts
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2drain.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.enemyTexts = self.app.playerTexts
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player2drain.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        self.after = int(100*afterTime/1500)
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.attackSound = pygame.mixer.Sound("resources/player2drain.wav")
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
                spell = self.app.players[self.playerIndex].spells[self.spellIndex]
                
                if not self.app.players[self.playerIndex].stunned and not spell.dodged: 
                    if spell.criticalHit:
                        self.criticalHitSound.play()
                        self.canvas.itemconfig(self.app.criticalImages[1-self.playerIndex], state = "normal")
                    healthText = str(int(-spell.damageDone))
                    self.app.showText(self.enemyTexts, healthText, spell.color)
                        
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
class PlayerDodgeGif2:
    def __init__(self, parent, canvas, x, y, app, playerIndex = 0):
        self.parent = parent
        self.canvas = canvas
        
        if playerIndex == 0:
            self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2dodge.gif"))]
            self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
        else:
            self.sequence = [ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)) for img in ImageSequence.Iterator(Image.open("resources/player2dodge.gif"))]
            self.image = self.canvas.create_image(app.rootWidth - x, y, image=self.sequence[0], anchor = SW)

        self.after = 33
        self.animating = True
        self.pausing = True
        self.canvas.itemconfig(self.image, state="hidden")
        self.sound = pygame.mixer.Sound("resources/player2dodge.wav")
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
