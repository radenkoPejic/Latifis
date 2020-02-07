from tkinter import ttk
from igra import Igra
from playerstrategies import *
import pygame

class Application():

	def __init__(self, root):
		self.root = root		
		
		self.rootWidth = None
		self.rootHeight = None
		
		self.backgroundCanvas = None
		self.backgroundPhoto = None
		self.backgroundImage = None
		
		self.style = None
		self.playerHealth = None
		self.playerStartHealth = None
		self.playerEnergy = None
		self.playerStartEnergy = None

		self.enemyHealth = None
		self.enemyStartHealth = None
		self.enemyEnergy = None
		self.enemyStartEnergy = None
		
		self.playerStatusCanvas = None
		self.playerStatusPhoto = None
		self.playerStatusImage = None
		self.playerHealthText = None
		self.playerEnergyText = None
		
		self.playerHealthBar = None
		self.playerEnergyBar = None

		self.playerText = None
		
		self.enemyStatusCanvas = None
		self.enemyStatusPhoto = None
		self.enemyStatusImage = None
		self.enemyHealthText = None
		self.enemyEnergyText = None
		
		self.enemyHealthBar = None
		self.enemyEnergyBar = None

		self.enemyText = None
		
		self.turnCanvas = None
		self.turnPhoto = None
		self.turnImage = None
		self.turnText = None
		
		self.spellCanvas = None
		self.spellCanvasPhoto = None
		self.spellCanvasImage = None
		self.spellCanvasText = None
		
		self.spellCanvasImages = []
		self.spellCanvasTexts = []
		
		
		self.afterTime = 1500
		self.switchTime = 500
		self.level = 0
		
		self.potez = None
		self.cooldowns = []
		self.playerActionIndex = None
		self.enemyActionIndex = None
		
		self.spellImages = []
		self.spellImages0 = []
		self.spellImages1 = []
		self.spellImages2 = []
		self.spellImages3 = []
		
		
		self.spells = []
		
		self.looserImage = ImageTk.PhotoImage(Image.open("resources/looser.jpg"))
		self.buffImage = ImageTk.PhotoImage(Image.open("resources/transparent.png"))
		self.criticalImage = ImageTk.PhotoImage(Image.open("resources/criticalhit.png"))
		self.criticalImages = []

		self.playerBuffImages = []
		self.playerBuffTexts = []
		
		self.enemyBuffImages = []
		self.enemyBuffTexts = []
		
		self.players = []
		self.playerStrategy = None
		self.enemyStrategy = None

		self.dodgeGifs = []
		
		self.playerSpellGifs = []
		
		self.playerSpellGifs = []
		self.playerGif = None

		self.enemySpellGifs = []
		self.enemyGif = None
		
		self.env = None
		self.envTags = ["forest", "desert", "lava", "ice"]
		self.playerWinnerGif = None
		self.endGameCanvas = None
		
		self.endGameSound = pygame.mixer.Sound("resources/endgame.wav")
		
		self.menuCanvas = None
		
		self.game = None
		

	
	def showPlayerBuffs(self):
		for i in range (len(self.playerBuffImages)):
			
			if i < len(self.players[0].buffs):
				self.playerStatusCanvas.itemconfig(self.playerBuffImages[i], image = self.players[0].buffs[i].image, state = "normal")
				txt = ""
				if self.players[0].buffs[i].forTextBox != None: 
					txt = self.players[0].buffs[i].forTextBox.center(7)
				self.playerStatusCanvas.itemconfig(self.playerBuffTexts[i], text = txt)
			else:
				self.playerStatusCanvas.itemconfig(self.playerBuffImages[i], image = self.buffImage, state = "hidden")
				self.playerStatusCanvas.itemconfig(self.playerBuffTexts[i], text = "")
			
			
		for txt in self.enemyBuffTexts:
			self.enemyStatusCanvas.itemconfig(txt, text = "")
	
	def showEnemyBuffs(self):
		for i in range (len(self.enemyBuffImages)):
			if i < len(self.players[1].buffs):
				self.enemyStatusCanvas.itemconfig(self.enemyBuffImages[i], image = self.players[1].buffs[i].image, state = "normal")
				txt = ""
				if self.players[1].buffs[i].forTextBox != None: 
					txt = self.players[1].buffs[i].forTextBox.center(7)
				self.enemyStatusCanvas.itemconfig(self.enemyBuffTexts[i], text = txt)
			else:
				self.enemyStatusCanvas.itemconfig(self.enemyBuffImages[i], image = self.buffImage, state = "hidden")
				self.enemyStatusCanvas.itemconfig(self.enemyBuffTexts[i], text = "")
			
			
		for txt in self.playerBuffTexts:
			self.playerStatusCanvas.itemconfig(txt, text = "")
		
	def updateStatus(self):
		#apdejt svih progres barova
		self.playerHealthBar["value"] = 100*self.players[0].health/self.players[0].max_health
		self.playerEnergyBar["value"] = 100*self.players[0].energy/self.players[0].max_energy
		self.playerHealthBar.update()
		self.playerEnergyBar.update()
		self.playerStatusCanvas.itemconfig(self.playerHealthText, text = "Health "+str(int(self.players[0].health)))
		self.playerStatusCanvas.itemconfig(self.playerEnergyText, text = "Energy "+str(int(self.players[0].energy)))
		
		self.enemyHealthBar["value"] = 100*self.players[1].health/self.players[1].max_health
		self.enemyEnergyBar["value"] = 100
		self.enemyHealthBar.update()
		self.enemyEnergyBar.update()
		self.enemyStatusCanvas.itemconfig(self.enemyHealthText, text = "Health "+str(int(self.players[1].health)))
		

	def run(self):
		self.playerEnergyBar["maximum"] = 100
		self.playerHealthBar["maximum"] = 100
		self.enemyHealthBar["maximum"] = 100
		self.enemyEnergyBar["maximum"] = 100
		
		self.updateStatus()
		self.root.after(self.afterTime, self.updateStatus)
		
		if self.game.winner is None:
			turn = self.potez//2 + 1
			side = self.potez % 2
			self.potez += 1
			
			if self.players[0].health < 150:
				self.pulse.play()
		
			if (side == 0):
				self.game.doBuffsPlayer()
				self.playerActionIndex = self.players[0].get_next_action(self.players[0].prev_state)
				
				self.cooldowns = []
				for i in range (len(self.players[0].spells)):
					self.cooldowns.append(self.players[0].spells[i].curr_cooldown)
				self.cooldowns[self.playerActionIndex] = self.players[0].spells[self.playerActionIndex].cooldown
			
			
				self.players[0].take_action(self.playerActionIndex, self.players[1])
				action = self.players[0].spells[self.playerActionIndex]
				self.showPlayerBuffs()
			else:
				self.game.doBuffsEnemy()
				self.enemyActionIndex = self.players[1].stepFuzzy(self.players[0])
				action = self.players[1].spells[self.enemyActionIndex]
				self.showEnemyBuffs()
			
			
			
			
			
			#apdejt poteza
			if (side == 0):
				self.turnCanvas.itemconfig(self.turnText, text = "Player's turn " + str(turn))
				self.enemyGif.pause()
				self.enemySpellGifs[self.enemyActionIndex].pause()
				self.playerGif.setSpell(action)
				self.playerGif.goOn()
				if not self.players[0].stunned:
					self.playerSpellGifs[self.playerActionIndex].goOn()
					
			else:
				self.turnCanvas.itemconfig(self.turnText, text = "Enemy's turn " + str(turn))
				self.playerGif.pause()
				self.playerSpellGifs[self.playerActionIndex].pause()
				self.enemyGif.setSpell(action)
				self.enemyGif.goOn()
				if not self.players[1].stunned:
					self.enemySpellGifs[self.enemyActionIndex].goOn()
				
			#apdejt sve kucice
			for ix in range (len(self.cooldowns)):
				cooldown = self.cooldowns[ix]
				if (cooldown==0):
					self.spellCanvas.itemconfig(self.spellCanvasImages[ix], image = self.spellImages[ix][0])
					self.spellCanvas.itemconfig(self.spellCanvasTexts[ix], text = "")
				else: 
					self.spellCanvas.itemconfig(self.spellCanvasImages[ix], image = self.spellImages[ix][2])
					self.spellCanvas.itemconfig(self.spellCanvasTexts[ix], text = str(cooldown))
			
			#oznacavanje pogodjene kucice
			if (side==0):
				self.spellCanvas.itemconfig(self.spellCanvasImages[self.playerActionIndex], image = self.spellImages[self.playerActionIndex][1])
			
			self.game.game_winner()
			self.root.after(self.afterTime+self.switchTime, self.run)
			
		elif self.game.winner == "Malis":
			self.turnCanvas.itemconfig(self.turnText, text = "Player won")
			self.stopGame()
			self.root.after(2*self.afterTime, self.playerWinnerGif.goOn)
			pygame.mixer.music.fadeout(2*self.afterTime)
			if (self.level==1):
				self.root.after(2*self.afterTime, self.level2)
			else:
				self.root.after(2*self.afterTime, self.backToMenu)
			#povratak u glavni meni
		else:
			self.turnCanvas.itemconfig(self.turnText, text = "Enemy won")
			self.stopGame()
			pygame.mixer.music.fadeout(2*self.afterTime)
			self.root.after(2*self.afterTime, self.showLoser)
			self.root.after(2*self.afterTime, self.backToMenu)
			#povratak u glavni meni
			
	def stopGame(self):
		app.playerStrategy.stop(self)
		app.enemyStrategy.stop(self)
		
	def showLoser(self):
		self.endGameCanvas.pack()
		self.endGameCanvas.itemconfig(self.looserImageCanvas, state="normal")
		self.endGameSound.play()
	
	def hideLoser(self):
		self.endGameCanvas.itemconfig(self.looserImageCanvas, state="hidden")
	
	def startGame(self):
		self.rootWidth = 806
		self.rootHeight = 449
		root.geometry(""+str(self.rootWidth)+"x"+str(self.rootHeight))
		
		self.env = -1
		
		self.playerHealth = self.playerStartHealth = 1000
		self.playerEnergy = self.playerStartEnergy = 1000

		self.enemyHealth = self.enemyStartHealth = 2000
		self.enemyEnergy = self.enemyStartEnergy = 20000
		
		
	
		self.potez = 0
		
		self.style = ttk.Style()
		self.style.theme_use('clam')
		self.style.configure("yellow.Horizontal.TProgressbar", troughcolor='white', bordercolor='white', background='yellow')
		self.style.configure("red.Horizontal.TProgressbar", troughcolor='white', bordercolor='white', background='red')
	
		self.backgroundCanvas = Canvas(self.root, bd=0, highlightthickness=0, relief='ridge')
		self.backgroundCanvas.place(x = 0, y = 0, width = self.rootWidth, height = self.rootHeight)

		self.backgroundPhoto = Image.open("resources/background1.jpg")
		self.backgroundPhoto = self.backgroundPhoto.resize((self.rootWidth, self.rootHeight))
		self.backgroundImage = ImageTk.PhotoImage(self.backgroundPhoto)
		self.backgroundCanvas.create_image(0, 0, image = self.backgroundImage, anchor = NW)
		
		self.playerStatusCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief='ridge')
		self.playerStatusCanvas.place(width= 250, height = 100, x = 30, y = 2)
		self.playerStatusPhoto = Image.open("resources/box.png")
		self.playerStatusPhoto = self.playerStatusPhoto.resize((250, 100))
		self.playerStatusImage = ImageTk.PhotoImage(self.playerStatusPhoto)
		self.playerStatusCanvas.create_image(0, 0, image = self.playerStatusImage, anchor = NW)
		self.playerHealthText = self.playerStatusCanvas.create_text(10, 10, anchor = NW, text = "Health "+str(self.playerHealth), fill = "white")
		self.playerEnergyText = self.playerStatusCanvas.create_text(10, 31, anchor = NW, text = "Energy "+str(self.playerEnergy), fill = "white")

		self.playerHealthBar = ttk.Progressbar(self.playerStatusCanvas, style = "red.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
		self.playerHealthBar.place(width = 120, height = 15, x = 95, y = 10)
		self.playerEnergyBar = ttk.Progressbar(self.playerStatusCanvas, style = "yellow.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
		self.playerEnergyBar.place(width = 120, height = 15, x = 95, y = 31)

		
		self.enemyStatusCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief='ridge')
		self.enemyStatusCanvas.place(width= 250, height = 100, x = 549, y = 2)
		self.enemyStatusPhoto = Image.open("resources/box.png")
		self.enemyStatusPhoto = self.playerStatusPhoto.resize((250, 100))
		self.enemyStatusImage = ImageTk.PhotoImage(self.enemyStatusPhoto)
		self.enemyStatusCanvas.create_image(0, 0, image = self.enemyStatusImage, anchor = NW)
		self.enemyHealthText = self.enemyStatusCanvas.create_text(160, 10, anchor = NW, text = "Health "+str(self.enemyHealth), fill = "white")
		self.enemyEnergyText = self.enemyStatusCanvas.create_text(160, 31, anchor = NW, text = "Energy infinite", fill = "white")

		self.enemyHealthBar = ttk.Progressbar(self.enemyStatusCanvas, style = "red.Horizontal.TProgressbar",orient="horizontal", mode="determinate")
		self.enemyHealthBar.place(width = 120, height = 15, x = 30, y = 10)
		self.enemyEnergyBar = ttk.Progressbar(self.enemyStatusCanvas, style = "yellow.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
		self.enemyEnergyBar.place(width = 120, height = 15, x = 30, y = 31)
		

		self.turnCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief='ridge')
		self.turnCanvas.place(width= 200, height = 50, x = 316, y = 7)
		self.turnPhoto = Image.open("resources/turn.jpg")
		self.turnPhoto= self.turnPhoto.resize((200, 50))
		self.turnImage = ImageTk.PhotoImage(self.turnPhoto)
		self.turnCanvas.create_image(0, 0, image = self.turnImage, anchor = NW)
		self.turnText = self.turnCanvas.create_text(12, 12, anchor = NW, text = "", font = ("Purisa", 17))
		
		self.spellCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief='ridge')
		self.spellCanvas.place(width = 375, height = 75, x = 231, y = 350)
		self.spellCanvasPhoto = Image.open("resources/box.png")
		self.spellCanvasPhoto = self.spellCanvasPhoto.resize((375, 75))
		self.spellCanvasImage = ImageTk.PhotoImage(self.spellCanvasPhoto)
		self.spellCanvas.create_image(0, 0, image = self.spellCanvasImage, anchor = NW)
		self.spellCanvasText = self.spellCanvas.create_text(30, 22, anchor = NW, text = "Spells:", font = ("Purisa", 17), fill = "white")
		
		self.playerBuffImages = []
		self.playerBuffTexts = []

		for x in range (5, 230, 40):
			self.playerBuffImages.append(self.playerStatusCanvas.create_image(x, 55, image=self.buffImage, anchor = NW))
			self.playerStatusCanvas.itemconfig(self.playerBuffImages[len(self.playerBuffImages)-1], state="hidden")
			self.playerBuffTexts.append(self.playerStatusCanvas.create_text(x, 86, anchor = NW, text = "", font = ("Purisa", 8), fill = "white"))

		self.enemyBuffImages = []
		self.enemyBuffTexts = []

		for x in range (245, 20, -40):
			self.enemyBuffImages.append(self.enemyStatusCanvas.create_image(x, 55, image=self.buffImage, anchor = NE))
			self.enemyStatusCanvas.itemconfig(self.enemyBuffImages[len(self.enemyBuffImages)-1], state="hidden")
			self.enemyBuffTexts.append(self.enemyStatusCanvas.create_text(x, 86, anchor = NE, text = "", font = ("Purisa", 8), fill = "white"))
			
		self.pulse = pygame.mixer.Sound("resources/pulse.wav")
	
		self.menuCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief='ridge', width = self.rootWidth, height = self.rootHeight)
		self.endGameCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief='ridge', width = self.rootWidth, height = self.rootHeight)
		self.looserImageCanvas = self.endGameCanvas.create_image(0, 0, image=self.looserImage, anchor = NW)
		self.endGameCanvas.pack_forget()
			
		
	def startLevel(self): #pokretanje nivoa
		
		self.playerActionIndex = 0
		self.enemyActionIndex = 0
		
	
		self.backgroundCanvas.delete("all")
	
		self.selectEnvironment()
		self.backgroundCanvas.create_image(0, 0, image = self.backgroundImage, anchor = NW)
		
		self.spells = []
		self.spellCanvasImages = []
		self.spellCanvasTexts = []
		self.criticalImages = []
		
		self.spellImages = []
		self.spellImages0 = []
		self.spellImages1 = []
		self.spellImages2 = []
		self.spellImages3 = []
		
		self.cooldowns = [0, 0, 0, 0]
		
		self.playerStrategy.setPlayerTexts(self)
		self.enemyStrategy.setPlayerTexts(self)
		
			
		self.dodgeGifs = []
		self.playerSpellGifs = []
		self.enemySpellGifs = []

		self.players = []
		
		self.playerStrategy.setPlayer(self)
		self.enemyStrategy.setPlayer(self)
		
		self.playerStrategy.setPlayerSpells(self)
		
		i = 0
		for x in range (120, 290, 55):
			self.spellCanvasImages.append(self.spellCanvas.create_image(x, 12, image = self.spellImages[i][0], anchor = NW))
			self.spellCanvasTexts.append(self.spellCanvas.create_text(x+15, 20, anchor = NW, text = "", font = ("Purisa", 25, "bold"), fill = "red"))
			i+=1
		
		self.playerStrategy.setPlayerGif(self)
		self.enemyStrategy.setPlayerGif(self)
		
		self.playerStrategy.setPlayerDodgeGif(self)
		self.enemyStrategy.setPlayerDodgeGif(self)
		
		self.playerStrategy.setPlayerSpellGifs(self)
		self.enemyStrategy.setPlayerSpellGifs(self)
		
		self.potez = 0
		
		self.game = Igra(self.players[0], self.players[1])
		self.players[1].initFuzzy(self.players[0])
		
		#dodavanje environment buffova igracima
		self.playerStrategy.setEnvironmentBuff(self.envTags[self.env-1], self.players[0])
		self.enemyStrategy.setEnvironmentBuff(self.envTags[self.env-1], self.players[1])
		
		self.run()
		
	def level1(self):
		self.menuCanvas.pack_forget()
		self.playerHealth = self.playerStartHealth = 1000
		self.playerEnergy = self.playerStartEnergy = 1000
		self.enemyHealth = self.enemyStartHealth = 2000
		self.enemyEnergy = self.enemyStartEnergy = 20000
		
		if (self.selectedPlayer == 0):
			self.playerStrategy = PlayerStrategy1("Novi11100", 0.05)
			self.playerWinnerGif = PlayerWinnerGif1(root, self.endGameCanvas, 0, 0)
		else:
			self.playerStrategy = PlayerStrategy2("Novi11100", 0.05)
			self.playerWinnerGif = PlayerWinnerGif2(root, self.endGameCanvas, 0, 0)
		
		self.enemyStrategy = EnemyStrategy1("Enemy1", 1)
		
		self.level = 1
		self.startLevel()
		
	def level2(self):
		self.playerHealth = self.playerStartHealth = 1000
		self.playerEnergy = self.playerStartEnergy = 1000
		self.enemyHealth = self.enemyStartHealth = 1000
		self.enemyEnergy = self.enemyStartEnergy = 20000
		
		self.enemyStrategy = EnemyStrategy2("Enemy2", 1)
	
		self.level = 2
		self.root.after(self.afterTime*3, self.playerWinnerGif.pause)
		self.root.after(self.afterTime*3, self.startLevel)
	
	def backToMenu(self):
		self.root.after(self.afterTime*3, self.hideLoser)
		self.root.after(self.afterTime*3, self.playerWinnerGif.pause)
		self.root.after(self.afterTime*3, self.mainMenu)
		
	def selectEnvironment(self):
		while True:
			r = random.randint(1, 4)
			if r!=self.env:
				break
				
		self.env = r
		self.backgroundPhoto = Image.open("resources/background" + str(r)+".jpg")
		self.backgroundPhoto = self.backgroundPhoto.resize((self.rootWidth, self.rootHeight))
		self.backgroundImage = ImageTk.PhotoImage(self.backgroundPhoto)
		
		pygame.mixer.music.stop()
		pygame.mixer.music.load("resources/background" + str(r)+".mp3") 
		pygame.mixer.music.play(-1)
	
	def setMenu(self):
		self.menuCanvas.pack()
		self.menuCanvasPhoto = Image.open("resources/mainMenu2.png")
		self.menuCanvasPhoto = self.menuCanvasPhoto.resize((self.rootWidth, self.rootHeight))
		self.menuCanvasImage = ImageTk.PhotoImage(self.menuCanvasPhoto)
		self.menuCanvas.create_image(0, 0, image = self.menuCanvasImage, anchor = NW)
		
		self.maxPlayerWidth = 280
		self.maxPlayerHeight = 320
		self.maxPlayerX = 515
		self.maxPlayerY = 10
		
		self.selectedPlayer = 0
		self.numOfPlayers = 2
		
		self.menuPlayerImages = []
		
		self.menuPlayerPhoto1 = Image.open("resources/player1.png")
		self.menuPlayerImages.append(ImageTk.PhotoImage(self.menuPlayerPhoto1))
		
		self.menuPlayerPhoto2 = Image.open("resources/player2.png")
		self.menuPlayerImages.append(ImageTk.PhotoImage(self.menuPlayerPhoto2))
		
		self.playerX = int(self.maxPlayerX + (1-self.menuPlayerImages[self.selectedPlayer].width()/self.maxPlayerWidth)*self.maxPlayerWidth/2)
		self.playerY = int(self.maxPlayerY + (1-self.menuPlayerImages[self.selectedPlayer].height()/self.maxPlayerHeight)*self.maxPlayerHeight/2)

		self.menuCanvasPlayerImage = self.menuCanvas.create_image(self.playerX, self.playerY, image = self.menuPlayerImages[self.selectedPlayer], anchor = NW)
			
		
		self.menuSpellBoxes = []
		x = 50
		for i in range (4):
			self.menuSpellBoxes.append(ImageTk.PhotoImage(Image.open("resources/spellBox.png")))
			self.menuCanvas.create_image(x, 260, image = self.menuSpellBoxes[i], anchor = NW)
			x += 110
		
		self.startGamePhoto = Image.open("resources/startGameBox.png")
		self.startGameImage = ImageTk.PhotoImage(self.startGamePhoto )
		self.startGameButton = Button(self.menuCanvas, command = self.level1, image = self.startGameImage, bg = '#cc9e71', bd =  4,\
		highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = "#cc9e71")
		self.startGameButton.place(x = 125, y = 30, width = 250, height = 70)
		
		self.selectPlayerPhoto = Image.open("resources/playerBox.png")
		self.selectPlayerImage = ImageTk.PhotoImage(self.selectPlayerPhoto )
		self.menuCanvas.create_image(175, 130, image = self.selectPlayerImage, anchor = NW)
		
		self.menuLeftPhoto = Image.open("resources/menuLeft.gif")
		self.menuLeftImage = ImageTk.PhotoImage(self.menuLeftPhoto )
		self.menuLeftButton = Button(self.menuCanvas, command = self.menuLeftClick, image = self.menuLeftImage, bg = '#cc9e71', bd =  4,\
		highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = "#cc9e71")
		self.menuLeftButton.place(x = 75, y = 130, width = 70, height = 70)
		
		self.menuRightPhoto = Image.open("resources/menuRight.gif")
		self.menuRightImage = ImageTk.PhotoImage(self.menuRightPhoto )
		self.menuRightButton = Button(self.menuCanvas, command = self.menuRightClick, image = self.menuRightImage, bg = '#cc9e71', bd =  4,\
		highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = "#cc9e71")
		self.menuRightButton.place(x = 355, y = 130, width = 70, height = 70)
		
		self.menuSpellPhotoSize = 60
		self.menuSpellButtonsX = 55
		self.menuSpellImages = []
		
		self.menuSpellImages1 = []
		
		self.menuSpellPhoto10 = Image.open("resources/p1attack0.jpg")
		self.menuSpellPhoto10 = self.menuSpellPhoto10.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto10))
		
		self.menuSpellPhoto11 = Image.open("resources/p1heal0.jpg")
		self.menuSpellPhoto11 = self.menuSpellPhoto11.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto11))
		
		self.menuSpellPhoto12 = Image.open("resources/p1charge0.png")
		self.menuSpellPhoto12 = self.menuSpellPhoto12.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto12))
		
		self.menuSpellPhoto13 = Image.open("resources/p1stun0.jpg")
		self.menuSpellPhoto13 = self.menuSpellPhoto13.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto13))
		
		self.menuSpellImages.append(self.menuSpellImages1)
		
		self.menuSpellImages2 = []
		
		self.menuSpellPhoto20 = Image.open("resources/p2attack0.jpg")
		self.menuSpellPhoto20 = self.menuSpellPhoto20.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto20))
		
		self.menuSpellPhoto21 = Image.open("resources/p2flex0.jpg")
		self.menuSpellPhoto21 = self.menuSpellPhoto21.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto21))
		
		self.menuSpellPhoto22 = Image.open("resources/p2charge0.jpg")
		self.menuSpellPhoto22 = self.menuSpellPhoto22.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto22))
		
		self.menuSpellPhoto23 = Image.open("resources/p2drain0.jpg")
		self.menuSpellPhoto23 = self.menuSpellPhoto23.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
		self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto23))
		
		self.menuSpellImages.append(self.menuSpellImages2)
		
		self.menuSpellButtons = []
		
		
		for k in range (self.numOfPlayers):
			xx = self.menuSpellButtonsX
			tmpmenuSpellButtons = []
			for i in range (4):			
				tmpmenuSpellButtons.append(Button(self.menuCanvas, image = self.menuSpellImages[k][i], bg = 'brown', bd =  0,\
				highlightcolor="brown", highlightbackground="brown", borderwidth=0, activebackground = "#cc9e71"))
				
				xx += self.menuSpellButtonsX*2
			self.menuSpellButtons.append(tmpmenuSpellButtons)
			
			
		self.playerDescrs = [PlayerStrategy1.descr, PlayerStrategy2.descr]
		self.playerSpellDescrs = [PlayerStrategy1.spellDescrs, PlayerStrategy2.spellDescrs]
		self.menuCanvasDescr = self.menuCanvas.create_text(10, 350,  anchor = NW, text = self.playerDescrs[0], font = ("Purisa", 15))
		
		self.selectPlayer()
		self.mainMenu()
	
	def mainMenu(self):
		self.menuCanvas.pack()
		pygame.mixer.music.stop()
		pygame.mixer.music.load("resources/mainMenu.mp3")
		pygame.mixer.music.play(-1)
		
	
	def menuRightClick(self):
		for i in range (4):			
			self.menuSpellButtons[self.selectedPlayer][i].place_forget()
			
		self.selectedPlayer = self.selectedPlayer + 1
		if (self.selectedPlayer == self.numOfPlayers):
			self.selectedPlayer = 0
		
		self.selectPlayer()
		
	def menuLeftClick(self):
		for i in range (4):			
			self.menuSpellButtons[self.selectedPlayer][i].place_forget()
			
		self.selectedPlayer = self.selectedPlayer - 1
		if (self.selectedPlayer == -1):
			self.selectedPlayer = self.numOfPlayers - 1
			
		self.selectPlayer()
		
	
	def selectPlayer(self):
		self.playerX = int(self.maxPlayerX + (1-self.menuPlayerImages[self.selectedPlayer].width()/self.maxPlayerWidth)*self.maxPlayerWidth/2)
		self.playerY = int(self.maxPlayerY + (1-self.menuPlayerImages[self.selectedPlayer].height()/self.maxPlayerHeight)*self.maxPlayerHeight/2)

		self.menuCanvas.itemconfig(self.menuCanvasPlayerImage, image = self.menuPlayerImages[self.selectedPlayer])
		xx = self.menuSpellButtonsX
		for i in range (4):			
			self.menuSpellButtons[self.selectedPlayer][i].place(x = xx, y = 265, width = self.menuSpellPhotoSize, height = self.menuSpellPhotoSize)
			self.menuSpellButtons[self.selectedPlayer][i]['command']=0
			self.menuSpellButtons[self.selectedPlayer][i]['relief']='sunken'
			self.menuSpellButtons[self.selectedPlayer][i].bind("<Enter>", self.hoveredSpell)
			self.menuSpellButtons[self.selectedPlayer][i].bind("<Leave>", self.unhoveredSpell)
			xx += self.menuSpellButtonsX*2
		
		self.menuCanvas.itemconfig(self.menuCanvasDescr, text = self.playerDescrs[self.selectedPlayer])
	
	def hoveredSpell(self, e):
		for i in range (4):
			if e.widget == self.menuSpellButtons[self.selectedPlayer][i]:
				self.menuCanvas.itemconfig(self.menuCanvasDescr, text = self.playerSpellDescrs[self.selectedPlayer][i])
				break
	
	def unhoveredSpell(self, e):
		self.menuCanvas.itemconfig(self.menuCanvasDescr, text = self.playerDescrs[self.selectedPlayer])
			
	
rootWidth = 806
rootHeight = 449
root = Tk()
root.title('Latifis')
root.geometry(""+str(rootWidth)+"x"+str(rootHeight))
root.resizable(0, 0)
root.iconbitmap("resources/icon.ico")

pygame.init()

app = Application(root)
app.startGame()
app.setMenu()
#app.level1()

root.mainloop()