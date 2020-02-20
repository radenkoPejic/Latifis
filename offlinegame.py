from playerstrategies import *
from playergifs1 import *
from playergifs2 import *


class Level():
    def __init__(self, app):
        self.app = app
    
    def setLevel(self):
        pass

class LevelE1(Level):
    def setLevel(self):
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
        
        self.app.gameStrategy.level = 1
        self.app.startGame()

class LevelE2(Level):
    def setLevel(self):
        self.app.playerHealth = self.app.playerStartHealth = 1000
        self.app.playerEnergy = self.app.playerStartEnergy = 1000
        self.app.enemyHealth = self.app.enemyStartHealth = 1000
        self.app.enemyEnergy = self.app.enemyStartEnergy = 20000
        
        self.app.enemyStrategy = EnemyStrategy2("Enemy2", 1)

        self.app.gameStrategy.level = 2
        self.app.root.after(self.app.afterTime*3, self.app.playerWinnerGif.pause)
        self.app.root.after(self.app.afterTime*3, self.app.startGame)
        

class GameStrategy():
    def __init__(self, app):
        self.app = app
        self.levels = []
        self.level = 0
    
    def setGame(self):
        pass
    
    def nextLevel(self):
        if self.level < len(self.levels): #prelazak na sledeci nivo
            self.app.root.after(2*self.app.afterTime, self.levels[self.level].setLevel)
        else: #povratak u glavni meni nakon svih nivoa
            self.app.root.after(2*self.app.afterTime, self.app.backToMenu)
            
    def endOfGame(self):
        self.app.root.after(2*self.app.afterTime, self.app.showLoser)
            #povratak u glavni meni
        self.app.root.after(2*self.app.afterTime, self.app.backToMenu)
        
        
class OfflineGameStrategyE(GameStrategy):
    def __init__(self, app):
        super().__init__(app)
        self.levels.append(LevelE1(app))
        self.levels.append(LevelE2(app))
        
    def setGame(self):
        self.levels[0].setLevel()
        
        
class LevelP1(Level):
    def setLevel(self):
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
            
        self.app.players = []
        self.app.playerStrategy.setPlayer(self.app)
        self.app.enemyStrategy = EnemyStrategy3(self.app, DeepMalis2(self.app.enemyStartHealth,50,self.app.enemyStartEnergy, "Novi11100", 0.05))
        self.app.players[1].load_model()
        
        self.app.gameStrategy.level = 1
        self.app.startGame()

class LevelP2(Level):
    def setLevel(self):
        self.app.playerHealth = self.app.playerStartHealth = 1000
        self.app.playerEnergy = self.app.playerStartEnergy = 1000
        self.app.enemyHealth = self.app.enemyStartHealth = 1000
        self.app.enemyEnergy = self.app.enemyStartEnergy = 1000
        
        self.app.players = []
        self.app.playerStrategy.setPlayer(self.app)
        self.app.enemyStrategy = EnemyStrategy4(self.app, DeepMalis3(self.app.enemyStartHealth,50,self.app.enemyStartEnergy, "dm3vsdm21000vse11000", 0.05))
        self.app.players[1].load_model()

        self.app.gameStrategy.level = 2
        self.app.root.after(self.app.afterTime*3, self.app.playerWinnerGif.pause)
        self.app.root.after(self.app.afterTime*3, self.app.startGame)
                
               
        
class OfflineGameStrategyP(GameStrategy):
    def __init__(self, app):
        super().__init__(app)
        self.levels.append(LevelP1(app))
        self.levels.append(LevelP2(app))
        
    def setGame(self):
        self.levels[0].setLevel()        
        
