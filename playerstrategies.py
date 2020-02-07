from DeepMalis import *
from Enemy import *
from playergifs1 import *
from playergifs2 import *
from enemygifs1 import *
from enemygifs2 import *
from Buff import *

class PlayerStrategy:
	def __init__(self, tag, explorationFactor):
		self.tag = tag
		self.explorationFactor = explorationFactor
		
	def setPlayer(self, app):
		pass
	
	def setPlayerGif(self, app):
		pass
		
	def setPlayerSpellGifs(self, app):
		pass
	
	def setPlayerDodgeGif(self, app):
		pass
	
	def setEnvironmentBuff(self, tag, player):
		pass

class PlayerStrategy1(PlayerStrategy):
	descr = "Charizard Y\nPositive environments: Lava, Desert\nNegative environments: Ice, Forest"
	spellDescrs = ["BurnAttack\nDamage: 60, Critical: 10%, Energy: 150, Cooldown: 0\nAdditional effect: 70% chance of adding BurnBuff to enemy's buff list if spell\nis not dodged",
	"LongFullHeal\nHeal: 10% of max health, Energy: 300, Cooldown: 6, Duration: 4\nAdditional effect: Adds FullBuff to players' buff list",
	"Charge\nBonus: 400, Energy: 0, Cooldown: 0",
	"Stun, Duration: 3, Energy: 200, Cooldown: 7\nAdditional effect: Adds StunBuff to enemy's buff list if spell is not dodged"
	]
	
	def setPlayer(self, app):
		app.players.append(DeepMalis2(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor))
		
	def setPlayerTexts(self, app):
		app.playerText = app.backgroundCanvas.create_text(183, 194, anchor = NW, font = ("Purisa", 20, "bold"), text = "")
		app.criticalImages.append(app.backgroundCanvas.create_image(133, 132, image = app.criticalImage, anchor = NW, state = "hidden"))

	def setPlayerGif(self, app):
		app.playerGif = PlayerGif1(app.root, app.backgroundCanvas, 240, 320, app.afterTime, app)
		
	def setPlayerSpellGifs(self, app):
		app.playerSpellGifs.append(PlayerAttackGif1(app.root, app.backgroundCanvas, 270, 303, app.afterTime, app, 0))
		app.playerSpellGifs.append(PlayerHealGif1(app.root, app.backgroundCanvas, 235, 330))
		app.playerSpellGifs.append(PlayerChargeGif1(app.root, app.backgroundCanvas, 145, 290))
		app.playerSpellGifs.append(PlayerStunGif1(app.root,app.backgroundCanvas, 620, 380, app.afterTime))
	
	def setPlayerDodgeGif(self, app):
		app.dodgeGifs.append(PlayerDodgeGif1(app.root, app.backgroundCanvas, 255, 350))
		
	def setPlayerSpells(self, app):
	
		app.spells = app.players[0].spells
		self.attackPhoto0 = Image.open("resources/p1attack0.jpg")
		self.attackPhoto0 = self.attackPhoto0.resize((50, 50))
		app.spellImages0.append(ImageTk.PhotoImage(self.attackPhoto0))
		self.attackPhoto1 = Image.open("resources/p1attack1.jpg")
		self.attackPhoto1 = self.attackPhoto1.resize((52, 52))
		app.spellImages0.append(ImageTk.PhotoImage(self.attackPhoto1))
		self.attackPhoto2 = Image.open("resources/p1attack2.jpg")
		self.attackPhoto2 = self.attackPhoto1.resize((50, 50))
		app.spellImages0.append(ImageTk.PhotoImage(self.attackPhoto2))
		app.spellImages.append(app.spellImages0)
		
		
		self.healPhoto0 = Image.open("resources/p1heal0.jpg")
		self.healPhoto0 = self.healPhoto0.resize((50, 50))
		app.spellImages1.append(ImageTk.PhotoImage(self.healPhoto0))
		self.healPhoto1 = Image.open("resources/p1heal1.jpg")
		self.healPhoto1 = self.healPhoto1.resize((52, 52))
		app.spellImages1.append(ImageTk.PhotoImage(self.healPhoto1))
		self.healPhoto2 = Image.open("resources/p1heal2.jpg")
		self.healPhoto2 = self.healPhoto2.resize((50, 50))
		app.spellImages1.append(ImageTk.PhotoImage(self.healPhoto2))
		app.spellImages.append(app.spellImages1)
		
		
		self.chargePhoto0 = Image.open("resources/p1charge0.png")
		self.chargePhoto0 = self.chargePhoto0.resize((50, 50))
		app.spellImages2.append(ImageTk.PhotoImage(self.chargePhoto0))
		self.chargePhoto1 = Image.open("resources/p1charge1.png")
		self.chargePhoto1 = self.chargePhoto1.resize((52, 52))
		app.spellImages2.append(ImageTk.PhotoImage(self.chargePhoto1))
		self.chargePhoto2 = Image.open("resources/p1charge2.png")
		self.chargePhoto2 = self.chargePhoto1.resize((50, 50))
		app.spellImages2.append(ImageTk.PhotoImage(self.chargePhoto2))
		app.spellImages.append(app.spellImages2)
				
		
		self.stunPhoto0 = Image.open("resources/p1stun0.jpg")
		self.stunPhoto0 = self.stunPhoto0.resize((50, 50))
		app.spellImages3.append(ImageTk.PhotoImage(self.stunPhoto0))
		self.stunPhoto1 = Image.open("resources/p1stun1.jpg")
		self.stunPhoto1 = self.stunPhoto1.resize((52, 52))
		app.spellImages3.append(ImageTk.PhotoImage(self.stunPhoto1))
		self.stunPhoto2 = Image.open("resources/p1stun2.jpg")
		self.stunPhoto2 = self.stunPhoto2.resize((50, 50))
		app.spellImages3.append(ImageTk.PhotoImage(self.stunPhoto2))
		app.spellImages.append(app.spellImages3)
		
	def setEnvironmentBuff(self, tag, player):
		if (tag == "lava"):
			player.buffs.append(LavaPlus())
		if (tag == "desert"):
			player.buffs.append(DesertPlus())
		elif (tag == "ice"):
			player.buffs.append(IceMinus())
		elif (tag == "forest"):
			player.buffs.append(ForestMinus())
	
	def stop(self, app):
		app.playerGif.stop()
		for gif in app.playerSpellGifs:
			gif.stop()
		app.dodgeGifs[0].stop()
		
		
class PlayerStrategy2(PlayerStrategy):
	descr = "Charizard X\nPositive environments: Forest\nNegative environments: Lava"
	spellDescrs = ["WeakenAttack\nDamage: 60, Critical: 10, Energy: 100,Cooldown: 2\nAdditional effect: 70% chance of adding WeakenBuff to enemy's buff list if spell\nis not dodged",
	"Flexible\nDodge: boosted by 30% of current dodge, Energy: 300, Cooldown: 3, Duration: 2\nAdditional effect: Adds FlexBuff to players' buff list",
	"ProtectionCharge\nBonus: 400, Energy: 0, Cooldown: 0\nAdditional effect: 70% chance of adding ProtectionBuff to players' buff list",
	"DrainAttack\nDamage: 100, Energy: 400, Cooldown: 5\nAdditional effect: 90% chance of adding DrainBuff to enemy's buff list if spell\nis not dodged"
	]
	
	def setPlayer(self, app):
		app.players.append(DeepMalis3(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor))
		
	def setPlayerTexts(self, app):
		app.playerText = app.backgroundCanvas.create_text(183, 194, anchor = NW, font = ("Purisa", 20, "bold"), text = "")
		app.criticalImages.append(app.backgroundCanvas.create_image(133, 132, image = app.criticalImage, anchor = NW, state = "hidden"))

	
	def setPlayerGif(self, app):
		app.playerGif = PlayerGif2(app.root, app.backgroundCanvas, 240, 350, app.afterTime, app)
		
		
	def setPlayerSpellGifs(self, app):
		app.playerSpellGifs.append(PlayerAttackGif2(app.root, app.backgroundCanvas, 270, 303, app.afterTime, app, 0))
		app.playerSpellGifs.append(PlayerFlexGif2(app.root, app.backgroundCanvas, 255, 360))
		app.playerSpellGifs.append(PlayerChargeGif2(app.root, app.backgroundCanvas, 245, 350))
		app.playerSpellGifs.append(PlayerDrainGif2(app.root,app.backgroundCanvas, 630, 330, app.afterTime))
	
	def setPlayerDodgeGif(self, app):
		app.dodgeGifs.append(PlayerDodgeGif2(app.root, app.backgroundCanvas, 250, 350))
		
	def setPlayerSpells(self, app):
	
		app.spells = app.players[0].spells
		self.attackPhoto0 = Image.open("resources/p2attack0.jpg")
		self.attackPhoto0 = self.attackPhoto0.resize((50, 50))
		app.spellImages0.append(ImageTk.PhotoImage(self.attackPhoto0))
		self.attackPhoto1 = Image.open("resources/p2attack1.jpg")
		self.attackPhoto1 = self.attackPhoto1.resize((52, 52))
		app.spellImages0.append(ImageTk.PhotoImage(self.attackPhoto1))
		self.attackPhoto2 = Image.open("resources/p2attack2.jpg")
		self.attackPhoto2 = self.attackPhoto2.resize((50, 50))
		app.spellImages0.append(ImageTk.PhotoImage(self.attackPhoto2))
		app.spellImages.append(app.spellImages0)
		
		
		self.healPhoto0 = Image.open("resources/p2flex0.jpg")
		self.healPhoto0 = self.healPhoto0.resize((50, 50))
		app.spellImages1.append(ImageTk.PhotoImage(self.healPhoto0))
		self.healPhoto1 = Image.open("resources/p2flex1.jpg")
		self.healPhoto1 = self.healPhoto1.resize((52, 52))
		app.spellImages1.append(ImageTk.PhotoImage(self.healPhoto1))
		self.healPhoto2 = Image.open("resources/p2flex2.jpg")
		self.healPhoto2 = self.healPhoto2.resize((50, 50))
		app.spellImages1.append(ImageTk.PhotoImage(self.healPhoto2))
		app.spellImages.append(app.spellImages1)
		
		
		self.chargePhoto0 = Image.open("resources/p2charge0.jpg")
		self.chargePhoto0 = self.chargePhoto0.resize((50, 50))
		app.spellImages2.append(ImageTk.PhotoImage(self.chargePhoto0))
		self.chargePhoto1 = Image.open("resources/p2charge1.jpg")
		self.chargePhoto1 = self.chargePhoto1.resize((52, 52))
		app.spellImages2.append(ImageTk.PhotoImage(self.chargePhoto1))
		self.chargePhoto2 = Image.open("resources/p2charge2.jpg")
		self.chargePhoto2 = self.chargePhoto2.resize((50, 50))
		app.spellImages2.append(ImageTk.PhotoImage(self.chargePhoto2))
		app.spellImages.append(app.spellImages2)
				
		
		self.stunPhoto0 = Image.open("resources/p2drain0.jpg")
		self.stunPhoto0 = self.stunPhoto0.resize((50, 50))
		app.spellImages3.append(ImageTk.PhotoImage(self.stunPhoto0))
		self.stunPhoto1 = Image.open("resources/p2drain1.jpg")
		self.stunPhoto1 = self.stunPhoto1.resize((52, 52))
		app.spellImages3.append(ImageTk.PhotoImage(self.stunPhoto1))
		self.stunPhoto2 = Image.open("resources/p2drain2.jpg")
		self.stunPhoto2 = self.stunPhoto2.resize((50, 50))
		app.spellImages3.append(ImageTk.PhotoImage(self.stunPhoto2))
		app.spellImages.append(app.spellImages3)
		
	def setEnvironmentBuff(self, tag, player):
		if (tag == "forest"):
			player.buffs.append(ForestPlus())
		elif (tag == "lava"):
			player.buffs.append(LavaMinus())
	
	def stop(self, app):
		app.playerGif.stop()
		for gif in app.playerSpellGifs:
			gif.stop()
		app.dodgeGifs[0].stop()
		

class EnemyStrategy1(PlayerStrategy):
	
	def setPlayer(self, app):
		app.players.append(Enemy(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor))
		
	def setPlayerTexts(self, app):
		app.enemyText = app.backgroundCanvas.create_text(420, 95, anchor = NW, font = ("Purisa", 20, "bold"), text = "")
		app.criticalImages.append(app.backgroundCanvas.create_image(450, 45, image = app.criticalImage, anchor = NW, state = "hidden"))
		
	
	def setPlayerGif(self, app):
		app.enemyGif = EnemyGif1(app.root, app.backgroundCanvas, 800, 342, app.players,\
						app.enemySpellGifs, app.playerText, app.enemyText, app.dodgeGifs, app.criticalImages)
		
		
	def setPlayerSpellGifs(self, app):
		app.enemySpellGifs.append(EnemyAttackGif1(app.root, app.backgroundCanvas, 453, 232, app.afterTime, app, 0))
		app.enemySpellGifs.append(EnemyEnergyAttackGif1(app.root, app.backgroundCanvas, 373, 342, app.afterTime, app, 1))
		app.enemySpellGifs.append(EnemyBurnAttackGif1(app.root, app.backgroundCanvas, 553, 442, app.afterTime, app, 2))
		app.enemySpellGifs.append(EnemyWeakenAttackGif1(app.root, app.backgroundCanvas, 373, 342, app.afterTime, app, 3))
	
	def setPlayerDodgeGif(self, app):
		app.dodgeGifs.append(EnemyDodgeGif1(app.root, app.backgroundCanvas, 680, 350))
	
	def setEnvironmentBuff(self, tag, player):
		if (tag == "lava"):
			player.buffs.append(LavaPlus())
		elif (tag == "ice"):
			player.buffs.append(IceMinus())
	
	def stop(self, app):
		app.enemyGif.stop()
		for gif in app.enemySpellGifs:
			gif.stop()
		app.dodgeGifs[1].stop()
		
class EnemyStrategy2(PlayerStrategy):
	
	def setPlayer(self, app):
		app.players.append(Enemy2(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor))
		
		
	def setPlayerTexts(self, app):
		app.enemyText = app.backgroundCanvas.create_text(420, 95, anchor = NW, font = ("Purisa", 20, "bold"), text = "")
		app.criticalImages.append(app.backgroundCanvas.create_image(450, 45, image = app.criticalImage, anchor = NW, state = "hidden"))
		
	
	def setPlayerGif(self, app):
		app.enemyGif = EnemyGif2(app.root, app.backgroundCanvas, 800, 342, app.players,\
						app.enemySpellGifs, app.playerText, app.enemyText, app.dodgeGifs, app.criticalImages)
		
		
	def setPlayerSpellGifs(self, app):
		app.enemySpellGifs.append(EnemyAttackGif2(app.root, app.backgroundCanvas, 583, 392))
		app.enemySpellGifs.append(EnemyHealGif2(app.root, app.backgroundCanvas, 750, 457))
		app.enemySpellGifs.append(EnemyRewindGif2(app.root, app.backgroundCanvas, 750, 400))
		app.enemySpellGifs.append(EnemyWeakenAttackGif2(app.root, app.backgroundCanvas, 530, 407, app.afterTime, app, 3))
	
	def setPlayerDodgeGif(self, app):
		app.dodgeGifs.append(EnemyDodgeGif2(app.root, app.backgroundCanvas, 680, 350))
	
	def setEnvironmentBuff(self, tag, player):
		if (tag == "ice"):
			player.buffs.append(IcePlus())
		elif (tag == "lava"):
			player.buffs.append(LavaMinus())
		elif (tag == "desert"):
			player.buffs.append(DesertMinus())
	
	def stop(self, app):
		app.enemyGif.stop()
		for gif in app.enemySpellGifs:
			gif.stop()
		app.dodgeGifs[1].stop()