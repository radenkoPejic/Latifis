from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame

	
class PlayerGif2:
	maxLimit = 21
	midLimit = 1
	enableLimit = 7
	
	def __init__(self, parent, canvas, x, y, afterTime, app):
		self.parent = parent
		self.canvas = canvas
		self.sequence = []
		self.afterTime = afterTime
		self.playerSpellGifs = app.playerSpellGifs
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2.gif"))]
		self.playerText = app.playerText
		self.enemyText = app.enemyText
		self.dodgeGifs = app.dodgeGifs
		self.players = app.players
		self.criticalImages = app.criticalImages
		self.app = app
		
		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.limit = PlayerGif2.maxLimit
		self.after = afterTime//len(self.sequence) + 5
		self.animating = True
		self.pausing = True
		self.animate(0)
		
	def animate(self, counter):
		if counter<self.limit:
			self.canvas.itemconfig(self.image, image = self.sequence[counter])
			
		if counter == PlayerGif2.enableLimit: #pokretanje animacije i zvuka?
			self.playerSpellGifs[0].enable()
			
		if not self.animating:
			return
		
		if self.pausing or self.limit==counter==PlayerGif2.maxLimit: 
			self.parent.after(self.after, lambda: self.animate(0))
		else:
			self.parent.after(self.after, lambda: self.animate((counter+1)%(len(self.sequence))))
	
	def stop(self):
		self.animating = False
		
	def pause(self):
		self.pausing = True
	
	def goOn(self):
		self.pausing = False
		
	def setSpell(self, spell):
		
		self.dodgeGifs[0].pause()
		
		self.limit = PlayerGif2.midLimit
		self.after = (self.afterTime//len(self.sequence))*2
		

		ispis = ""
		color = "white"
		
		self.canvas.itemconfig(self.criticalImages[0], state = "hidden")
			
		if isinstance(spell, AttackSpell):
			self.limit = PlayerGif2.maxLimit
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
			
			
class PlayerWinnerGif2:
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2winner.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = NW)
		self.after = 67
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/playerwinner.wav")
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
				#self.canvas.itemconfig(self.image, state="hidden")
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
		
class PlayerAttackGif2:
	def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
		self.parent = parent
		self.canvas = canvas
		self.x0 = x
		self.x = x
		self.y0 = y
		self.y = y
		self.afterTime = afterTime//2
		self.dodged = False
		self.app = app
		self.spell = self.app.spells[spellIndex]
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2attack.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(35*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.enabled = False
		
		self.launchSound = pygame.mixer.Sound("resources/player2launch.wav")
		self.hitSound = pygame.mixer.Sound("resources/player1hit.wav")
		self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
		
		self.animate(0)
		
	def animate(self, counter):
		if not self.animating:
			return
		
		if self.enabled==True and self.pausing==False:#prikazivanje
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
		
		
class PlayerFlexGif2:
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2flex.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player2flex.wav")
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


class PlayerChargeGif2:
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2charge.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player2charge.wav")
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
		
		
class PlayerDrainGif2:
	def __init__(self, parent, canvas, x, y, afterTime):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2drain.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(100*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player2drain.wav")
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


class PlayerDodgeGif2:
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/player2dodge.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/player2dodge.wav")
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
