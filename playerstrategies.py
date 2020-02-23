from DeepMalis import *
from Enemy import *
from playergifs1 import *
from playergifs2 import *
from enemygifs1 import *
from enemygifs2 import *
from Buff import *
import textwrap


class PEStrategy:
    #infinite energija
    enemyMaxEnergy = 20000

    def __init__(self, tag, explorationFactor):
        #tag koji sluzi za naziv .h5 fajla u player modu
        self.tag = tag
        #faktor istrazivanja u player modu
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
    
    #dohvatanje tipa igraca (player, enemy)
    def getTypeOfPlayer(self):
        pass
    
    #kraj prikaza igraca
    def stop(self):
        pass
    
    #opis za prikaz spellova igraca u glavnom meniju
    def getPlayerSpellDescrs(self, player, boxWidth = 83):
        descrs = []
        for spell in player.spells:
            descr = spell.description()
            nameEnd = descr.find("\n")
            name = descr[:nameEnd]
            descr = descr[nameEnd+1:]
            descr = descr.replace("\n", ", ")
            descr = textwrap.fill(text = descr, width = boxWidth)
            descr = name + "\n" + descr
            descrs.append(descr)
        return descrs
    
    #opis za prikaz podataka igraca u glavnom meniju 
    def getPlayerDescr(self, player, boxWidth = 83):
        name = self.getPlayerName() + "\n"
        
        environment = textwrap.fill(text = self.getEnvironmentDescr(), width = boxWidth) + "\n"
        
        attributes = ""
        attributes += "Maximum health: " + str(player.max_health) +", Maximum energy: "
        if player.max_energy != PEStrategy.enemyMaxEnergy: 
            attributes +=  str(player.max_energy)
        else: attributes += "infinite"
        attributes += ", Critical: " + str(int(player.critical*100)) +"%"
        attributes += ", Dodge: " + str(int(player.dodge*100)) +"%"
        attributes += ", Weaken: " + str(int(player.weaken*100)) +"%"
        attributes += ", Protection: " + str(int(player.protection*100)) +"%"
        attributes = textwrap.fill(text = attributes, width = boxWidth)
        
        descr = name + environment + attributes
        return descr
    
    #dohvatanje plus i minus environment tagova
    def getEnvironmentTags(self):
        pass
    
    #opis pozitivnih i negativnih okruzenja igraca radi prikaza u glavnom meniju
    def getEnvironmentDescr(self):
        environmentPlusTags, environmentMinusTags = self.getEnvironmentTags()
        descr = ""
        n = len(environmentPlusTags)
        if n>0:
            descr += "Positive Environments: "
            for i in range(n):
                descr += environmentPlusTags[i] + ", "
 
        n = len(environmentMinusTags)
        if n>0:
            descr += "Negative Environments: "
            for i in range(n-1):
                descr += environmentMinusTags[i] + ", "
            descr += environmentMinusTags[n-1]
        
        return descr

#osnovna klasa strategije za playera Charizard Y        
class PEStrategy1(PEStrategy):
    playerName = "Charizard Y"
    environmentPlusTags = ["Lava", "Desert"]
    environmentMinusTags = ["Ice","Forest"]
    maxHealth = 1000
    maxEnergy = 1000
    
    def getEnvironmentTags(self):
        return PEStrategy1.environmentPlusTags, PEStrategy1.environmentMinusTags
    
    def getPlayerName(self):
        return PEStrategy1.playerName
    
#osnovna klasa strategije za playera Charizard X          
class PEStrategy2(PEStrategy):
    playerName = "Charizard X"
    environmentPlusTags = ["Forest"]
    environmentMinusTags = ["Lava"]
    maxHealth = 1000
    maxEnergy = 1000
    
    def getEnvironmentTags(self):
        return PEStrategy2.environmentPlusTags, PEStrategy2.environmentMinusTags
    
    def getPlayerName(self):
        return PEStrategy2.playerName
        
#osnovna klasa strategije za enemya Enemy 1  
class PEStrategy3(PEStrategy):
    playerName = "Enemy 1"
    environmentPlusTags = ["Lava"]
    environmentMinusTags = ["Ice"]
    maxHealth = 2000
    maxEnergy = PEStrategy.enemyMaxEnergy
    
    def getEnvironmentTags(self):
        return PEStrategy3.environmentPlusTags, PEStrategy3.environmentMinusTags
    
    def getPlayerName(self):
        return PEStrategy3.playerName
        
#osnovna klasa strategije za enemya Enemy 2          
class PEStrategy4(PEStrategy):
    playerName = "Enemy 2"
    environmentPlusTags = ["Ice"]
    environmentMinusTags = ["Lava", "Desert"]
    maxHealth = 1000
    maxEnergy = PEStrategy.enemyMaxEnergy
    
    def getEnvironmentTags(self):
        return PEStrategy4.environmentPlusTags, PEStrategy4.environmentMinusTags
    
    def getPlayerName(self):
        return PEStrategy4.playerName
        
        
class PlayerStrategy1(PEStrategy1): #Charizard Y - narandzasti
    
    def setPlayer(self, app, toLoad = True, toSet = False):
        #ako je vec setovan u online modu ne setuje se opet
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = PEStrategy1.maxHealth
        app.playerEnergy = app.playerStartEnergy = PEStrategy1.maxEnergy
        app.players[0] = DeepMalis2(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor)
        #ako je u human modu ne ucitava se model
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

    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()
        
        
class PlayerStrategy2(PEStrategy2): #Charizard X - sivo-plavi

    def setPlayer(self, app, toLoad = True, toSet = True):
        #ako je vec setovan u online modu ne setuje se opet
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = PEStrategy2.maxHealth
        app.playerEnergy = app.playerStartEnergy = PEStrategy2.maxEnergy
        app.players[0] = DeepMalis3(app.playerStartHealth,50,app.playerStartEnergy, self.tag, self.explorationFactor)
        #ako je u human modu ne ucitava se model
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
        
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()
        
        
class PlayerStrategy3(PEStrategy3): #Enemy 1 - tamni, flipovan
    
    def setPlayer(self, app, toLoad = True, toSet = False):
        #ako je vec setovan u online modu ne setuje se opet        
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = PEStrategy3.maxHealth
        app.playerEnergy = app.playerStartEnergy = PEStrategy3.maxEnergy
        app.players[0] = Enemy(app.playerStartHealth,12,app.playerStartEnergy, self.tag, self.explorationFactor)
            
    def setPlayerWinnerGif(self, app):
        app.playerWinnerGif = PlayerWinnerGif(app.root, app.endGameCanvas, 0, 0, app)
        
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
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()
        
        
class PlayerStrategy4(PEStrategy4): #Enemy 2 - plavi, flipovan
    
    def setPlayer(self, app, toLoad = True, toSet = False):
        #ako je vec setovan u online modu ne setuje se opet
        if toSet == False: return
        app.playerHealth = app.playerStartHealth = PEStrategy4.maxHealth
        app.playerEnergy = app.playerStartEnergy = PEStrategy4.maxEnergy
        app.players[0] = Enemy2(app.playerStartHealth,12,app.playerStartEnergy, self.tag, self.explorationFactor)
            
    def setPlayerWinnerGif(self, app):
        app.playerWinnerGif = PlayerWinnerGif(app.root, app.endGameCanvas, 0, 0, app)
        
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
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.playerGif.stop()
        for gif in app.playerSpellGifs:
            gif.stop()
        app.dodgeGifs[0].stop()        
        

class EnemyStrategy1(PEStrategy1): #Charizard Y - narandzasti, flipovan 
            
    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        #ako je u nekom od offline modova kreira se u trenutnoj aplikaciji i ucitava se model
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = PEStrategy1.maxHealth
            app.enemyEnergy = app.enemyStartEnergy = PEStrategy1.maxEnergy
            app.players[1] = DeepMalis2(app.enemyStartHealth,50,app.enemyStartEnergy, self.tag, self.explorationFactor)
            app.players[1].load_model()
        else: #ako je u online modu ocitavamo podatke sa primljenog protivnickog igraca
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
        
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        

class EnemyStrategy2(PEStrategy2): #Charizard X - sivo-plavi, flipovan

    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        #ako je u nekom od offline modova kreira se u trenutnoj aplikaciji i ucitava se model
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = PEStrategy2.maxHealth
            app.enemyEnergy = app.enemyStartEnergy = PEStrategy2.maxEnergy
            app.players[1] = DeepMalis3(app.enemyStartHealth,50,app.enemyStartEnergy, self.tag, self.explorationFactor)
            app.players[1].load_model()
        else: #ako je u online modu ocitavamo podatke sa primljenog protivnickog igraca
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
    
    def getTypeOfPlayer(self):
        return "player"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()        
        

class EnemyStrategy3(PEStrategy3): #Enemy 1 - tamni

    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):   
        #ako je u nekom od offline modova kreira se u trenutnoj aplikaciji
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = PEStrategy3.maxHealth
            app.enemyEnergy = app.enemyStartEnergy = PEStrategy3.maxEnergy
            app.players[1] = Enemy(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor)
        else: #ako je u online modu ocitavamo podatke sa primljenog protivnickog igraca
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
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        
        
class EnemyStrategy4(PEStrategy4): #Enemy 2 - plavi

    def addPlayer2(self, app, player2):
        app.players[1] = player2
    
    def setPlayer(self, app, offline = True):
        #ako je u nekom od offline modova kreira se u trenutnoj aplikaciji
        if offline == True:
            app.enemyHealth = app.enemyStartHealth = PEStrategy4.maxHealth
            app.enemyEnergy = app.enemyStartEnergy = PEStrategy4.maxEnergy
            app.players[1] = Enemy2(app.enemyStartHealth,12,app.enemyStartEnergy, self.tag, self.explorationFactor)
        else: #ako je u online modu ocitavamo podatke sa primljenog protivnickog igraca
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
            
    def getTypeOfPlayer(self):
        return "enemy"
    
    def stop(self, app):
        app.enemyGif.stop()
        for gif in app.enemySpellGifs:
            gif.stop()
        app.dodgeGifs[1].stop()
        

