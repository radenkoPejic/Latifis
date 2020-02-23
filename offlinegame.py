from playerstrategies import *
from modestrategies import *
from environmentstrategies import *


class Level():
    def __init__(self, app):
        self.app = app
    
    def setLevel(self):
        pass

#prvi nivo u modu PvE ili HvE
class LevelE1(Level):
    def setLevel(self):
        self.app.players = [None, None]
        self.app.playerStrategy = self.app.playerStrategies[self.app.selectedPlayer]
        
        self.app.enemyStrategy = self.app.enemyStrategies[2]
        
        self.app.firstPlayer = 0
        self.app.gameStrategy.level = 1
        self.app.startGame()
#drugi nivo u modu PvE ili HvE
class LevelE2(Level):
    def setLevel(self):
        self.app.players = [None, None]
        self.app.enemyStrategy = self.app.enemyStrategies[3]

        self.app.gameStrategy.level = 2
        self.app.root.after(self.app.afterTime*3, self.app.playerWinnerGif.pause)
        self.app.root.after(self.app.afterTime*3, self.app.startGame)
        
#prvi nivo u modu HvP        
class LevelP1(Level):
    def setLevel(self):
        self.app.players = [None, None]
        self.app.playerStrategy = self.app.playerStrategies[self.app.selectedPlayer]
        
        self.app.enemyStrategy = self.app.enemyStrategies[1]
        
        self.app.firstPlayer = 0
        self.app.gameStrategy.level = 1
        self.app.startGame()
        
#drugi nivo u modu HvP   
class LevelP2(Level):
    def setLevel(self):
        self.app.players = [None, None]
        
        self.app.enemyStrategy = self.app.enemyStrategies[0]

        self.app.gameStrategy.level = 2
        self.app.root.after(self.app.afterTime*3, self.app.playerWinnerGif.pause)
        self.app.root.after(self.app.afterTime*3, self.app.startGame)
        
        
        
#osnovna klasa za postavljanje strategije igre, cuva nivoe igre
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
        
        
#offline strategija igre u slucaju odabranih PvE, HvE, HvP modova (offline modova)      
class OfflineGameStrategy(GameStrategy):
    def __init__(self, app):
        super().__init__(app)
    
    #resetovanje online igre i postavljanje pocetnog nivoa igre
    def setGame(self):
        self.app.onlineGameStrategy.reset()
        self.levels[0].setLevel()     
        
        
#offline strategija igre u slucaju odabranih PvE, HvE modova          
class OfflineGameStrategyE(OfflineGameStrategy):
    def __init__(self, app):
        super().__init__(app)
        self.levels.append(LevelE1(app))
        self.levels.append(LevelE2(app))
                       
#offline strategija igre u slucaju odabranog HvP moda         
class OfflineGameStrategyP(OfflineGameStrategy):
    def __init__(self, app):
        super().__init__(app)
        self.levels.append(LevelP1(app))
        self.levels.append(LevelP2(app))     
        