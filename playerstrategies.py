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
    
    #kraj prikaza igraca
    def stop(self):
        pass
        
        
class PlayerStrategy1(PlayerStrategy): #Charizard Y - narandzasti
    #opis za prikaz u meniju
    descr = "Charizard Y\nPositive environments: Lava, Desert\nNegative environments: Ice, Forest"
    spellDescrs = ["BurnAttack\nDamage: 60, Critical: 10%, Energy: 150, Cooldown: 0\nAdditional effect: 70% chance of adding BurnBuff to enemy's buff list if spell\nis not dodged",
    "LongFullHeal\nHeal: 10% of max health, Energy: 300, Cooldown: 6, Duration: 4\nAdditional effect: Adds FullBuff to players' buff list",
    "Charge\nBonus: 400, Energy: 0, Cooldown: 0",
    "Stun\nDuration: 3, Energy: 200, Cooldown: 7\nAdditional effect: Adds StunBuff to enemy's buff list if spell is not dodged"
    ]
    
    def setPlayer(self, app):
        app.players.append(DeepMalis2(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor))
        
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
        self.attackPhoto0 = Image.open("resources/p1attack0.jpg")
        self.attackPhoto0 = self.attackPhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.attackPhoto0))
        
        self.healPhoto0 = Image.open("resources/p1heal0.jpg")
        self.healPhoto0 = self.healPhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.healPhoto0))
        
        self.chargePhoto0 = Image.open("resources/p1charge0.png")
        self.chargePhoto0 = self.chargePhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.chargePhoto0))

        self.stunPhoto0 = Image.open("resources/p1stun0.jpg")
        self.stunPhoto0 = self.stunPhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.stunPhoto0))
            
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
        
        
class PlayerStrategy2(PlayerStrategy): #Charizard X - sivo-plavi
    #opis za prikaz u meniju
    descr = "Charizard X\nPositive environments: Forest\nNegative environments: Lava"
    spellDescrs = ["WeakenAttack\nDamage: 60, Critical: 10%, Energy: 100,Cooldown: 2\nAdditional effect: 70% chance of adding WeakenBuff to enemy's buff list if spell\nis not dodged",
    "Flexible\nDodge: boosted by 30% of current dodge, Energy: 300, Cooldown: 3, Duration: 2\nAdditional effect: Adds FlexBuff to players' buff list",
    "ProtectionCharge\nBonus: 400, Energy: 0, Cooldown: 0\nAdditional effect: 70% chance of adding ProtectionBuff to players' buff list",
    "DrainAttack\nDamage: 100, Energy: 400, Cooldown: 5\nAdditional effect: 90% chance of adding DrainBuff to enemy's buff list if spell\nis not dodged"
    ]
    
    def setPlayer(self, app):
        app.players.append(DeepMalis3(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor))
        
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
        self.attackPhoto0 = Image.open("resources/p2attack0.jpg")
        self.attackPhoto0 = self.attackPhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.attackPhoto0))

        self.healPhoto0 = Image.open("resources/p2flex0.jpg")
        self.healPhoto0 = self.healPhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.healPhoto0))
        
        self.chargePhoto0 = Image.open("resources/p2charge0.jpg")
        self.chargePhoto0 = self.chargePhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.chargePhoto0))
        
        self.stunPhoto0 = Image.open("resources/p2drain0.jpg")
        self.stunPhoto0 = self.stunPhoto0.resize((50, 50))
        app.spellImages.append(ImageTk.PhotoImage(self.stunPhoto0))
            
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
        

class EnemyStrategy1(PlayerStrategy): #Enemy1 - tamni
    
    def setPlayer(self, app):
        app.players.append(Enemy(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor))
        
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
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        
        
class EnemyStrategy2(PlayerStrategy): #Enemy2 - plavi
    
    def setPlayer(self, app):
        app.players.append(Enemy2(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor))
      
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
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()


class EnemyStrategy3(PlayerStrategy): #Charizard Y - narandzasti, flipovan 
    
    def setPlayer(self, app):
        app.players.append(DeepMalis2(app.enemyStartHealth,50,app.enemyStartEnergy, self.tag, self.explorationFactor))
        
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
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        

class EnemyStrategy4(PlayerStrategy): #Charizard X - sivo-plavi, flipovan

    def setPlayer(self, app):
        app.players.append(DeepMalis3(app.enemyStartHealth,50,app.enemyStartEnergy, self.tag, self.explorationFactor))
        
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
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()


class Level():
    def __init__(self, app):
        self.app = app
    
    def level(self):
        pass

class OfflineLevel1(Level):
    def level(self):
        self.app.menuCanvas.pack_forget()
        self.app.playerHealth = self.app.playerStartHealth = 1000
        self.app.playerEnergy = self.app.playerStartEnergy = 1000
        self.app.enemyHealth = self.app.enemyStartHealth = 2000
        self.app.enemyEnergy = self.app.enemyStartEnergy = 20000
        
        if (self.app.selectedPlayer == 0):
            self.app.playerStrategy = PlayerStrategy1("Novi11100", 0.05)
            self.app.playerWinnerGif = PlayerWinnerGif1(self.app.root, self.app.endGameCanvas, 0, 0, self.app)
        else:
            self.app.playerStrategy = PlayerStrategy2("dm3vsdm21000vse11000", 0.05)
            self.app.playerWinnerGif = PlayerWinnerGif2(self.app.root, self.app.endGameCanvas, 0, 0, self.app)
        
        self.app.enemyStrategy = EnemyStrategy1("Enemy1", 1)
        
        self.app.level = 1
        self.app.startLevel()

class OfflineLevel2(Level):
    def level(self):
        self.app.playerHealth = self.app.playerStartHealth = 1000
        self.app.playerEnergy = self.app.playerStartEnergy = 1000
        self.app.enemyHealth = self.app.enemyStartHealth = 1000
        self.app.enemyEnergy = self.app.enemyStartEnergy = 20000
        
        self.app.enemyStrategy = EnemyStrategy2("Enemy2", 1)

        self.app.level = 2
        self.app.root.after(self.app.afterTime*3, self.app.playerWinnerGif.pause)
        self.app.root.after(self.app.afterTime*3, self.app.startLevel)

class OnlineLevel1(Level):
    def level(self):
        self.app.menuCanvas.pack_forget()
        self.app.playerHealth = self.app.playerStartHealth = 1000
        self.app.playerEnergy = self.app.playerStartEnergy = 1000
        self.app.enemyHealth = self.app.enemyStartHealth = 1000
        self.app.enemyEnergy = self.app.enemyStartEnergy = 1000
        
        if (self.app.selectedPlayer == 0):
            self.app.playerStrategy = PlayerStrategy1("Novi11100", 0.05)
            self.app.playerWinnerGif = PlayerWinnerGif1(self.app.root, self.app.endGameCanvas, 0, 0, self.app)
        else:
            self.app.playerStrategy = PlayerStrategy2("dm3vsdm21000vse11000", 0.05)
            self.app.playerWinnerGif = PlayerWinnerGif2(self.app.root, self.app.endGameCanvas, 0, 0, self.app)
        
        if random.random()<0.5:
            self.app.enemyStrategy = EnemyStrategy3("Novi11100", 0.05)
        else:
            self.app.enemyStrategy = EnemyStrategy4("dm3vsdm21000vse11000", 0.05)
        
        self.app.selectedMode += 2
        self.app.level = 1
        self.app.startLevel()

class OfflineLevelStrategy():
    def __init__(self, app):
        app.levels = []
        app.levels.append(OfflineLevel1(app))
        app.levels.append(OfflineLevel2(app))
      
class OnlineLevelStrategy():
    def __init__(self, app):
        app.levels = []
        app.levels.append(OnlineLevel1(app))  