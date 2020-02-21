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
    
    #postavljanje vrste igraca
    def setPlayer(self, app):
        pass
    
    #postavljanje gif za igraca
    def setPlayerGif(self, app):
        pass
    
    #postavljanje gifova za spellove igraca
    def setPlayerSpellGifs(self, app):
        pass
    
    #postavljanje gifa za dodge igraca
    def setPlayerDodgeGif(self, app):
        pass
    
    #postavljanje environment buffova za igraca
    def setEnvironmentBuff(self, tag, player):
        pass
        
    def getTypeOfPlayer(self):
        pass
    
    #kraj prikaza igraca
    def stop(self):
        pass
        
        
class PlayerStrategy1(PlayerStrategy): #Charizard Y - narandzasti
    #opis za prikaz u meniju
    descr = "Charizard Y\nPositive environments: Lava, Desert\nNegative environments: Ice, Forest"
    spellDescrs = ["BurnAttack\nDamage: 60, Critical: 10%, Energy: 150, Cooldown: 0\nAdditional effect: 70% chance of adding BurnBuff to enemy's buff list if spell\nis not dodged",
    "LongMissHeal\nHeal: 10% of maximum-current health, Energy: 300, Cooldown: 6, Duration: 4\nAdditional effect: Adds FullBuff to players' buff list",
    "Charge\nBonus: 400, Energy: 0, Cooldown: 0",
    "Stun\nDuration: 3, Energy: 200, Cooldown: 7\nAdditional effect: Adds StunBuff to enemy's buff list if spell is not dodged"
    ]
    
    def setPlayer(self, app, toLoad = True, toSet = False):
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = 1000
        app.playerEnergy = app.playerStartEnergy = 1000
        app.players[0] = DeepMalis2(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor)
        if toLoad == True:
            app.players[0].load_model()
            
    def setPlayerWinnerGif(self, app):
        app.playerWinnerGif = PlayerWinnerGif1(app.root, app.endGameCanvas, 0, 0, app)
        
    def setPlayerTexts(self, app):
        app.createTexts(app.playerTexts, 183, 194)
        app.criticalImages.append(app.backgroundCanvas.create_image(133, 132, image = app.criticalImage, anchor = NW, state = "hidden"))

    def setPlayerGif(self, app):
        app.playerGif = PlayerGif1(app.root, app.backgroundCanvas, 240, 320, app.afterTime, app)
        
    def setPlayerSpellGifs(self, app):
        app.playerSpellGifs.append(PlayerAttackGif1(app.root, app.backgroundCanvas, 270, 303, app.afterTime, app, 0))
        app.playerSpellGifs.append(PlayerHealGif1(app.root, app.backgroundCanvas, 235, 330, app))
        app.playerSpellGifs.append(PlayerChargeGif1(app.root, app.backgroundCanvas, 145, 290, app))
        app.playerSpellGifs.append(PlayerStunGif1(app.root,app.backgroundCanvas, 620, 380, app.afterTime, app))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(PlayerDodgeGif1(app.root, app.backgroundCanvas, 255, 350, app))
    
    #postavljanje slika u kucicama za spellove playera
    def setPlayerSpellImages(self, app):
        self.attackPhoto = Image.open("resources/p1attack.jpg")
        self.attackPhoto = self.attackPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.attackPhoto))
        
        self.healPhoto = Image.open("resources/p1heal.jpg")
        self.healPhoto = self.healPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.healPhoto))
        
        self.chargePhoto = Image.open("resources/p1charge.png")
        self.chargePhoto = self.chargePhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.chargePhoto))

        self.stunPhoto = Image.open("resources/p1stun.jpg")
        self.stunPhoto = self.stunPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.stunPhoto))
            
    def setEnvironmentBuff(self, tag, player):
        if (tag == "lava"):
            player.buffs.append(LavaPlus())
        if (tag == "desert"):
            player.buffs.append(DesertPlus())
        elif (tag == "ice"):
            player.buffs.append(IceMinus())
        elif (tag == "forest"):
            player.buffs.append(ForestMinus())
    
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()
        
        
class PlayerStrategy2(PlayerStrategy): #Charizard X - sivo-plavi
    #opis za prikaz u meniju
    descr = "Charizard X\nPositive environments: Forest\nNegative environments: Lava"
    spellDescrs = ["WeakenAttack\nDamage: 60, Critical: 10%, Energy: 100,Cooldown: 2\nAdditional effect: 70% chance of adding WeakenBuff to enemy's buff list if spell\nis not dodged",
    "Flexible\nDodge: boosted by 30% of current dodge, Energy: 300, Cooldown: 3, Duration: 2\nAdditional effect: Adds FlexBuff to players' buff list",
    "ProtectionCharge\nBonus: 400, Energy: 0, Cooldown: 0\nAdditional effect: 70% chance of adding ProtectionBuff to players' buff list",
    "DrainAttack\nDamage: 100, Energy: 400, Cooldown: 5\nAdditional effect: 90% chance of adding DrainBuff to enemy's buff list if spell\nis not dodged"
    ]
    
    def setPlayer(self, app, toLoad = True, toSet = True):
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = 1000
        app.playerEnergy = app.playerStartEnergy = 1000
        app.players[0] = DeepMalis3(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor)
        if toLoad == True:
            app.players[0].load_model()
    
    def setPlayerWinnerGif(self, app):
        app.playerWinnerGif = PlayerWinnerGif2(app.root, app.endGameCanvas, 0, 0, app)
        
    def setPlayerTexts(self, app):
        app.createTexts(app.playerTexts, 183, 194)
        app.criticalImages.append(app.backgroundCanvas.create_image(133, 132, image = app.criticalImage, anchor = NW, state = "hidden"))
    
    def setPlayerGif(self, app):
        app.playerGif = PlayerGif2(app.root, app.backgroundCanvas, 240, 350, app.afterTime, app)
           
    def setPlayerSpellGifs(self, app):
        app.playerSpellGifs.append(PlayerAttackGif2(app.root, app.backgroundCanvas, 270, 313, app.afterTime, app, 0))
        app.playerSpellGifs.append(PlayerFlexGif2(app.root, app.backgroundCanvas, 255, 360, app))
        app.playerSpellGifs.append(PlayerChargeGif2(app.root, app.backgroundCanvas, 245, 350, app))
        app.playerSpellGifs.append(PlayerDrainGif2(app.root,app.backgroundCanvas, 630, 330, app.afterTime, app, 3))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(PlayerDodgeGif2(app.root, app.backgroundCanvas, 250, 350, app))
        
    #postavljanje slika u kucicama za spellove playera
    def setPlayerSpellImages(self, app):
        self.attackPhoto = Image.open("resources/p2attack.jpg")
        self.attackPhoto = self.attackPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.attackPhoto))

        self.healPhoto = Image.open("resources/p2flex.jpg")
        self.healPhoto = self.healPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.healPhoto))
        
        self.chargePhoto = Image.open("resources/p2charge.jpg")
        self.chargePhoto = self.chargePhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.chargePhoto))
        
        self.stunPhoto = Image.open("resources/p2drain.jpg")
        self.stunPhoto = self.stunPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.stunPhoto))
            
    def setEnvironmentBuff(self, tag, player):
        if (tag == "forest"):
            player.buffs.append(ForestPlus())
        elif (tag == "lava"):
            player.buffs.append(LavaMinus())
    
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()
        
class PlayerStrategy3(PlayerStrategy): #Enemy 1 - tamni, flipovan
    #opis za prikaz u meniju
    
    def setPlayer(self, app, toLoad = True, toSet = False):
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = 2000
        app.playerEnergy = app.playerStartEnergy = 20000
        app.players[0] = Enemy(app.playerStartHealth,12,app.playerStartEnergy, self.tag, self.explorationFactor)
            
    def setPlayerWinnerGif(self, app):
        app.playerWinnerGif = PlayerWinnerGif1(app.root, app.endGameCanvas, 0, 0, app)
        
    def setPlayerTexts(self, app):
        app.createTexts(app.playerTexts, app.rootWidth - 420, 95, NE)
        app.criticalImages.append(app.backgroundCanvas.create_image(app.rootWidth - 450, 45, image = app.criticalImage, anchor = NE, state = "hidden"))
    
    def setPlayerGif(self, app):
        app.playerGif = EnemyGif1(app.root, app.backgroundCanvas, 800, 342, app, 0)
        
    def setPlayerSpellGifs(self, app):
        app.playerSpellGifs.append(EnemyAttackGif1(app.root, app.backgroundCanvas, 453, 232, app.afterTime, app, 0, 0))
        app.playerSpellGifs.append(EnemyEnergyAttackGif1(app.root, app.backgroundCanvas, 373, 342, app.afterTime, app, 1, 0))
        app.playerSpellGifs.append(EnemyBurnAttackGif1(app.root, app.backgroundCanvas, 553, 442, app.afterTime, app, 2, 0))
        app.playerSpellGifs.append(EnemyWeakenAttackGif1(app.root, app.backgroundCanvas, 373, 342, app.afterTime, app, 3, 0))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(EnemyDodgeGif1(app.root, app.backgroundCanvas, 680, 350, app, 0))
    
    #postavljanje slika u kucicama za spellove playera
    def setPlayerSpellImages(self, app):
        self.attackPhoto = Image.open("resources/e1attack.jpg")
        self.attackPhoto = self.attackPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.attackPhoto))
        
        self.healPhoto = Image.open("resources/e1energy.jpg")
        self.healPhoto = self.healPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.healPhoto))
        
        self.chargePhoto = Image.open("resources/e1burn.jpg")
        self.chargePhoto = self.chargePhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.chargePhoto))

        self.stunPhoto = Image.open("resources/e1weaken.jpg")
        self.stunPhoto = self.stunPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.stunPhoto))
            
    def setEnvironmentBuff(self, tag, player):
        if (tag == "lava"):
            player.buffs.append(LavaPlus())
        elif (tag == "ice"):
            player.buffs.append(IceMinus())
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()
        
        
class PlayerStrategy4(PlayerStrategy): #Enemy 2 - plavi, flipovan
    #opis za prikaz u meniju
    
    def setPlayer(self, app, toLoad = True, toSet = False):
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = 1000
        app.playerEnergy = app.playerStartEnergy = 20000
        app.players[0] = Enemy2(app.playerStartHealth,12,app.playerStartEnergy, self.tag, self.explorationFactor)
            
    def setPlayerWinnerGif(self, app):
        app.playerWinnerGif = PlayerWinnerGif1(app.root, app.endGameCanvas, 0, 0, app)
        
    def setPlayerTexts(self, app):
        app.createTexts(app.playerTexts, app.rootWidth - 420, 95, NE)
        app.criticalImages.append(app.backgroundCanvas.create_image(app.rootWidth - 450, 45, image = app.criticalImage, anchor = NE, state = "hidden"))
    
    def setPlayerGif(self, app):
        app.playerGif = EnemyGif2(app.root, app.backgroundCanvas, 800, 342, app, 0)
        
    def setPlayerSpellGifs(self, app):
        app.playerSpellGifs.append(EnemyAttackGif2(app.root, app.backgroundCanvas, 583, 392, app, 0, 0))
        app.playerSpellGifs.append(EnemyHealGif2(app.root, app.backgroundCanvas, 750, 457, app, 0))
        app.playerSpellGifs.append(EnemyRewindGif2(app.root, app.backgroundCanvas, 750, 400, app, 0))
        app.playerSpellGifs.append(EnemyWeakenAttackGif2(app.root, app.backgroundCanvas, 530, 407, app.afterTime, app, 3, 0))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(EnemyDodgeGif2(app.root, app.backgroundCanvas, 680, 350, app, 0))
    
    #postavljanje slika u kucicama za spellove playera
    def setPlayerSpellImages(self, app):
        self.attackPhoto = Image.open("resources/e2attack.jpg")
        self.attackPhoto = self.attackPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.attackPhoto))
        
        self.healPhoto = Image.open("resources/e2heal.jpg")
        self.healPhoto = self.healPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.healPhoto))
        
        self.chargePhoto = Image.open("resources/e2rewind.jpg")
        self.chargePhoto = self.chargePhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.chargePhoto))

        self.stunPhoto = Image.open("resources/e2weaken.jpg")
        self.stunPhoto = self.stunPhoto.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.stunPhoto))
            
    def setEnvironmentBuff(self, tag, player):
        if (tag == "ice"):
            player.buffs.append(IcePlus())
        elif (tag == "lava"):
            player.buffs.append(LavaMinus())
        elif (tag == "desert"):
            player.buffs.append(DesertMinus())
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()        
        

class EnemyStrategy1(PlayerStrategy): #Charizard Y - narandzasti, flipovan 
            
    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = 1000
            app.enemyEnergy = app.enemyStartEnergy = 1000
            app.players[1] = DeepMalis2(app.enemyStartHealth,50,app.enemyStartHealth, self.tag, self.explorationFactor)
            app.players[1].load_model()
        else:
            print(app.players)
            app.enemyHealth = app.enemyStartHealth = app.players[1].max_health
            app.enemyEnergy = app.enemyStartEnergy = app.players[1].max_energy
            
    
    def setPlayerTexts(self, app):
        app.createTexts(app.enemyTexts, app.rootWidth - 183, 194, NE)
        app.criticalImages.append(app.backgroundCanvas.create_image(app.rootWidth - 133, 132, image = app.criticalImage, anchor = NE, state = "hidden"))
        
    def setPlayerGif(self, app):
        app.enemyGif = PlayerGif1(app.root, app.backgroundCanvas, 240, 320, app.afterTime, app, 1)
        
    def setPlayerSpellGifs(self, app):
        app.enemySpellGifs.append(PlayerAttackGif1(app.root, app.backgroundCanvas, 270, 303, app.afterTime, app, 0, 1))
        app.enemySpellGifs.append(PlayerHealGif1(app.root, app.backgroundCanvas, 235, 330, app, 1))
        app.enemySpellGifs.append(PlayerChargeGif1(app.root, app.backgroundCanvas, 145, 290, app, 1))
        app.enemySpellGifs.append(PlayerStunGif1(app.root,app.backgroundCanvas, 620, 380, app.afterTime, app, 1))
    
    def setPlayerDodgeGif(self, app):    
        app.dodgeGifs.append(PlayerDodgeGif1(app.root, app.backgroundCanvas, 255, 350, app, 1))
        
    def setEnvironmentBuff(self, tag, player):
        if (tag == "lava"):
            player.buffs.append(LavaPlus())
        if (tag == "desert"):
            player.buffs.append(DesertPlus())
        elif (tag == "ice"):
            player.buffs.append(IceMinus())
        elif (tag == "forest"):
            player.buffs.append(ForestMinus())
            
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        

class EnemyStrategy2(PlayerStrategy): #Charizard X - sivo-plavi, flipovan

    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        print(offline)
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = 1000
            app.enemyEnergy = app.enemyStartEnergy = 1000
            app.players[1] = DeepMalis3(app.enemyStartHealth,50,app.enemyStartHealth, self.tag, self.explorationFactor)
            app.players[1].load_model()
        else:
            app.enemyHealth = app.enemyStartHealth = app.players[1].max_health
            app.enemyEnergy = app.enemyStartEnergy = app.players[1].max_energy
        
    def setPlayerTexts(self, app):
        app.createTexts(app.enemyTexts, app.rootWidth - 183, 194, NE)
        app.criticalImages.append(app.backgroundCanvas.create_image(app.rootWidth - 133, 132, image = app.criticalImage, anchor = NE, state = "hidden"))
    
    def setPlayerGif(self, app):
        app.enemyGif = PlayerGif2(app.root, app.backgroundCanvas, 240, 350, app.afterTime, app, 1)
             
    def setPlayerSpellGifs(self, app):
        app.enemySpellGifs.append(PlayerAttackGif2(app.root, app.backgroundCanvas, 270, 313, app.afterTime, app, len(app.enemySpellGifs), 1))
        app.enemySpellGifs.append(PlayerFlexGif2(app.root, app.backgroundCanvas, 255, 360, app, 1))
        app.enemySpellGifs.append(PlayerChargeGif2(app.root, app.backgroundCanvas, 245, 350, app, 1))
        app.enemySpellGifs.append(PlayerDrainGif2(app.root,app.backgroundCanvas, 630, 330, app.afterTime, app, len(app.enemySpellGifs), 1))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(PlayerDodgeGif2(app.root, app.backgroundCanvas, 250, 350, app, 1))
        
    def setEnvironmentBuff(self, tag, player):
        if (tag == "forest"):
            player.buffs.append(ForestPlus())
        elif (tag == "lava"):
            player.buffs.append(LavaMinus())
    
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()        
        

class EnemyStrategy3(PlayerStrategy): #Enemy1 - tamni

    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = 2000
            app.enemyEnergy = app.enemyStartEnergy = 20000
            app.players[1] = Enemy(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor)
        else:
            app.enemyHealth = app.enemyStartHealth = app.players[1].max_health
            app.enemyEnergy = app.enemyStartEnergy = app.players[1].max_energy
        
    def setPlayerTexts(self, app):
        app.createTexts(app.enemyTexts, 420, 95)
        app.criticalImages.append(app.backgroundCanvas.create_image(450, 45, image = app.criticalImage, anchor = NW, state = "hidden"))
    
    def setPlayerGif(self, app):
        app.enemyGif = EnemyGif1(app.root, app.backgroundCanvas, 800, 342, app)
            
    def setPlayerSpellGifs(self, app):
        app.enemySpellGifs.append(EnemyAttackGif1(app.root, app.backgroundCanvas, 453, 232, app.afterTime, app, 0))
        app.enemySpellGifs.append(EnemyEnergyAttackGif1(app.root, app.backgroundCanvas, 373, 342, app.afterTime, app, 1))
        app.enemySpellGifs.append(EnemyBurnAttackGif1(app.root, app.backgroundCanvas, 553, 442, app.afterTime, app, 2))
        app.enemySpellGifs.append(EnemyWeakenAttackGif1(app.root, app.backgroundCanvas, 373, 342, app.afterTime, app, 3))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(EnemyDodgeGif1(app.root, app.backgroundCanvas, 680, 350, app))
    
    def setEnvironmentBuff(self, tag, player):
        if (tag == "lava"):
            player.buffs.append(LavaPlus())
        elif (tag == "ice"):
            player.buffs.append(IceMinus())
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        
        
class EnemyStrategy4(PlayerStrategy): #Enemy2 - plavi

    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = 1000
            app.enemyEnergy = app.enemyStartEnergy = 20000
            app.players[1] = Enemy2(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor)
        else:
            app.enemyHealth = app.enemyStartHealth = app.players[1].max_health
            app.enemyEnergy = app.enemyStartEnergy = app.players[1].max_energy
      
    def setPlayerTexts(self, app):
        app.createTexts(app.enemyTexts, 420, 95)
        app.criticalImages.append(app.backgroundCanvas.create_image(450, 45, image = app.criticalImage, anchor = NW, state = "hidden"))     
    
    def setPlayerGif(self, app):
        app.enemyGif = EnemyGif2(app.root, app.backgroundCanvas, 800, 342, app)       
        
    def setPlayerSpellGifs(self, app):
        app.enemySpellGifs.append(EnemyAttackGif2(app.root, app.backgroundCanvas, 583, 392, app, 0))
        app.enemySpellGifs.append(EnemyHealGif2(app.root, app.backgroundCanvas, 750, 457, app))
        app.enemySpellGifs.append(EnemyRewindGif2(app.root, app.backgroundCanvas, 750, 400, app))
        app.enemySpellGifs.append(EnemyWeakenAttackGif2(app.root, app.backgroundCanvas, 530, 407, app.afterTime, app, 3))
    
    def setPlayerDodgeGif(self, app):
        app.dodgeGifs.append(EnemyDodgeGif2(app.root, app.backgroundCanvas, 680, 350, app))
    
    def setEnvironmentBuff(self, tag, player):
        if (tag == "ice"):
            player.buffs.append(IcePlus())
        elif (tag == "lava"):
            player.buffs.append(LavaMinus())
        elif (tag == "desert"):
            player.buffs.append(DesertMinus())
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()





class ModeStrategy():
    def __init__(self, app):
        self.app = app
        
    def playSpell(self):
        pass
        
        
class PlayerModeStrategy(ModeStrategy):
    def playSpell(self):
        self.app.playerActionIndex = self.app.players[self.app.side].step(self.app.players[1-self.app.side])
        return self.app.players[self.app.side].spells[self.app.playerActionIndex]
  
class EnemyModeStrategy(ModeStrategy):
    def playSpell(self):
        self.app.playerActionIndex = self.app.players[self.app.side].stepFuzzy(self.app.players[1-self.app.side])
        return self.app.players[self.app.side].spells[self.app.playerActionIndex]
  
class HumanModeStrategy(ModeStrategy):
    def playSpell(self):
        #zaustavljanje cupkanja
        if self.app.side == 0:
            self.app.playerGif.pause()  
        else: self.app.enemyGif.pause()
        
        #ako nije stigao da odigra potez smanjujemo cooldownove i vracamo None
        if self.app.playerActionIndex == -1:
            for carolija in self.app.players[self.app.side].spells:
                carolija.reduceCooldown()
            return None
        #odigravamo potez
        else:
            self.app.players[self.app.side].take_action(self.app.playerActionIndex, self.app.players[1-self.app.side])
            return self.app.players[self.app.side].spells[self.app.playerActionIndex]
        
class OnlineModeStrategy(ModeStrategy):
    def playSpell(self):
        if self.app.playerActionIndex == -1: return None
        return self.app.players[self.app.side].spells[self.app.playerActionIndex]
    