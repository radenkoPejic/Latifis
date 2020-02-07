from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from Spell import *
import pygame
	
		
class EnemyGif1:
	def __init__(self, parent, canvas, x, y, players, spellGifs, playerText, enemyText, dodgeGifs, criticalImages):
		self.parent = parent
		self.canvas = canvas
		self.spellGifs = spellGifs
		self.playerText = playerText
		self.enemyText = enemyText
		self.dodgeGifs = dodgeGifs
		self.players = players
		self.criticalImages = criticalImages
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1.gif"))]
		
		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.normalAfter = 67
		self.after = self.normalAfter
		self.slowAfter = 105
		self.animating = True
		self.pausing = True
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
			
		self.canvas.itemconfig(self.enemyText, text = "")
		self.canvas.itemconfig(self.criticalImages[1], state = "hidden")
		
		self.canvas.itemconfig(self.playerText, text = "")
		self.canvas.itemconfig(self.criticalImages[0], state = "hidden")
			
		if isinstance(spell, AttackSpell):

			if not self.players[1].stunned and spell.dodged:
					self.dodgeGifs[0].goOn()
				

class EnemyAttackGif1:
	def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
		self.parent = parent
		self.canvas = canvas
		self.x0 = x
		self.x = x
		self.y0 = y
		self.y = y
		self.afterTime = afterTime//2
			
		self.app = app
		self.spell = self.app.players[1].spells[spellIndex]
		
		self.sequence = []
		res = 0.06
		for img in ImageSequence.Iterator(Image.open("resources/enemyFire.gif")):
			width, height = img.size
			image = img.resize((int(res*width), int(res*height)))
			self.sequence.append(ImageTk.PhotoImage(image))	
			res+=0.06
		
		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = E)
		self.after = int(30*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.enabled = False
		self.canvas.itemconfig(self.image, state="hidden")
		self.attackSound = pygame.mixer.Sound("resources/enemy1attack.wav")
		self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
		self.animate(0)
		
	def animate(self, counter):
		if not self.animating:
			return
			
		if self.pausing:
			self.parent.after(self.after, lambda: self.animate(0))
			
		elif not self.pausing:
			self.x -= 11
			self.y += 1
			self.canvas.move(self.image, -11, 1)
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
		self.canvas.move(self.image, self.x0-self.x, self.y0-self.y)
		self.y = self.y0
		self.x = self.x0
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
	
	def goOn(self):
		self.pausing = False
		self.canvas.itemconfig(self.image, state="normal")
		self.attackSound.play()
		
	def enable(self):
		self.enabled = True


class EnemyDodgeGif1:
	def __init__(self, parent, canvas, x, y):
		self.parent = parent
		self.canvas = canvas
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1dodge.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = 33
		self.animating = True
		self.pausing = True
		self.canvas.itemconfig(self.image, state="hidden")
		self.sound = pygame.mixer.Sound("resources/enemydodge.wav")
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
		
class EnemyEnergyAttackGif1:
	def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
		self.parent = parent
		self.canvas = canvas
		self.afterTime = afterTime//2
			
		self.app = app
		self.spell = self.app.players[1].spells[spellIndex]
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1energy.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(80*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.enabled = False
		self.canvas.itemconfig(self.image, state="hidden")
		self.attackSound = pygame.mixer.Sound("resources/enemy1energy.wav")
		self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
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

class EnemyBurnAttackGif1:
	def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
		self.parent = parent
		self.canvas = canvas
		self.afterTime = afterTime//2
			
		self.app = app
		self.spell = self.app.players[1].spells[spellIndex]
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1burn.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(80*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.enabled = False
		self.canvas.itemconfig(self.image, state="hidden")
		self.attackSound = pygame.mixer.Sound("resources/enemy1burn.wav")
		self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
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

class EnemyWeakenAttackGif1:
	def __init__(self, parent, canvas, x, y, afterTime, app, spellIndex):
		self.parent = parent
		self.canvas = canvas
		self.afterTime = afterTime//2
			
		self.app = app
		self.spell = self.app.players[1].spells[spellIndex]
		
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open("resources/enemy1weaken.gif"))]

		self.image = self.canvas.create_image(x, y, image=self.sequence[0], anchor = SE)
		self.after = int(80*afterTime/1500)
		self.animating = True
		self.pausing = True
		self.enabled = False
		self.canvas.itemconfig(self.image, state="hidden")
		self.attackSound = pygame.mixer.Sound("resources/enemy1weaken.wav")
		self.criticalHitSound = pygame.mixer.Sound("resources/criticalHit.wav")
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
