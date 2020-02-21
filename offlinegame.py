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
        self.app.players = [None, None]
        self.app.playerStrategy = self.app.playerStrategies[self.app.selectedPlayer]
        
        self.app.enemyStrategy = self.app.enemyStrategies[2]
        
        self.app.firstPlayer = 0
        self.app.gameStrategy.level = 1
        self.app.startGame()

class LevelE2(Level):
    def setLevel(self):
        self.app.players = [None, None]
        self.app.enemyStrategy = self.app.enemyStrategies[3]

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
        self.app.players = [None, None]
        self.app.playerStrategy = self.app.playerStrategies[self.app.selectedPlayer]
        
        self.app.enemyStrategy = self.app.enemyStrategies[1]
        
        self.app.firstPlayer = 0
        self.app.gameStrategy.level = 1
        self.app.startGame()

class LevelP2(Level):
    def setLevel(self):
        self.app.players = [None, None]
        
        self.app.enemyStrategy = self.app.enemyStrategies[0]

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
        
