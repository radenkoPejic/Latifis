from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame

class PlayerGif1:
	maxLimit = 88
	midLimit = 30
	launchLimit = 31
	enableLimit = 45

	def __init__(self, parent, canvas, x, y, afterTime, app):
		self.parent = parent
		self.canvas = canvas
		self.sequence = []
		self.afterTime = afterTime
		self.playerSpellGifs = app.playerSpellGifs
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player1.gif"))]
		self.playerText = app.playerText
		self.enemyText = app.enemyText
		self.dodgeGifs = app.dodgeGifs
		self.players = app.players
		self.criticalImages = app.criticalImages
		self.app = app
		
		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.limit = PlayerGif1.maxLimit
		self.after = afterTime//len(self.sequence)
		self.animating = True
		self.pausing = True
		self.animate(0)
		
	def animate(self, counter):
		if counter<self.limit:
			self.canvas.itemconfig(self.image, image = self.sequence[counter])
			
		if counter == PlayerGif1.launchLimit: #pokretanje zvuka
			self.playerSpellGifs[0].launch()	
		elif counter == PlayerGif1.enableLimit: #pokretanje gifa
			self.playerSpellGifs[0].enable()
			
		if not self.animating:
			return
		
		if self.pausing or self.limit==counter==PlayerGif1.midLimit: 
			self.parent.after(self.after, lambda: self.animate(0))
		else:
			self.parent.after(self.after, lambda: self.animate(counter+1))
	
	def stop(self):
		self.animating = False
		
	def pause(self):
		self.pausing = True
	
	def goOn(self):
		self.pausing = False
		
	def setSpell(self, spell):
		
		self.dodgeGifs[0].pause()
		
		self.limit = PlayerGif1.midLimit
		self.after = (self.afterTime//len(self.sequence))*2
		

		ispis = ""
		color = "white"
		
		self.canvas.itemconfig(self.criticalImages[0], state = "hidden")
			
		if isinstance(spell, AttackSpell):
			self.limit = PlayerGif1.maxLimit
			self.after = self.afterTime//len(self.sequence)
			
			if not self.players[0].stunned and spell.dodged:
				self.dodgeGifs[1].goOn()
			
		elif isinstance(spell, Charge):
			ispis = spell.bonus
			color = spell.color
		
		elif isinstance(spell, Heal):
			ispis = spell.health
			color = spell.color
		
		elif isinstance(spell, Stun):
			if spell.dodged:
				self.dodgeGifs[1].goOn()
			else: 
				self.app.enemyGif.after = self.app.enemyGif.slowAfter
			
		self.canvas.itemconfig(self.playerText, text = ispis, fill = color)
			

class PlayerWinnerGif1:
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player1winner.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = NW)
		self.after = 67
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/playerwinner.wav")
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
	def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
		self.parent = parent
		self.canvas = app.backgroundCanvas
		self.x0 = x
		self.x = x
		self.y0 = y
		self.y = y
		self.afterTime = afterTime//2
		self.app = app
		self.spell = self.app.spells[spellIndex]
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/fireball.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(30*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.enabled = False
		
		self.launchSound = pygame.mixer.Sound("resources/player1launch.wav")
		self.hitSound = pygame.mixer.Sound("resources/player1hit.wav")
		self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
	
		self.animate(0)
		
	def animate(self, counter):
		if not self.animating:
			return
	
		if self.enabled and not self.pausing: #prikazivanje
			self.canvas.itemconfig(self.image, state="normal")
			self.canvas.itemconfig(self.image, image = self.sequence[counter])
			
			if (self.x<510): #kretanje
				self.x += 15	
				self.y -= 2
				self.canvas.move(self.image, 15, -2)
				
			else: #zaustavljanje i prikazivanje posledica udara
				if not self.app.players[0].stunned and not self.spell.dodged:
					if self.spell.criticalHit:
						self.criticalHitSound.play()
						self.canvas.itemconfig(self.app.criticalImages[1], state = "normal")
					else:
						self.hitSound.play()
					healthText = str(int(-self.spell.damageDone))
					self.canvas.itemconfig(self.app.enemyText, text = healthText, fill = self.spell.color)
				
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
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/healing.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player1heal.wav")
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
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/charging.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player1charge.wav")
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
	def __init__(self, parent, canvas, x, y, afterTime):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/stued.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(67*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player1stun.wav")
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
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/playerDodge.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player1dodge.wav")
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
		
		