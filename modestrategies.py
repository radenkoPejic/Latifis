from playerstrategies import *

#osnovna klasa za odredjivanje moda oba igraca
class ModeStrategy():
    def setPlayerModes(self, app):
        pass
#PvE mod igre(offline) - prvi igrac je ili player ili enemy, drugi igrac je enemy
class ModePvEStrategy(ModeStrategy):
    def setPlayerModes(self, app):
        app.playerModes = [app.playerStrategy.getTypeOfPlayer(), app.enemyStrategy.getTypeOfPlayer()]        
#HvE mod igre(offline) - prvi igrac je human, drugi igrac je enemy       
class ModeHvEStrategy(ModeStrategy):
    def setPlayerModes(self, app):
        app.playerModes = ["human", app.enemyStrategy.getTypeOfPlayer()]
#HvP mod igre(offline) - prvi igrac je human, drugi igrac je player         
class ModeHvPStrategy(ModeStrategy):
    def setPlayerModes(self, app):
        app.playerModes = ["human", app.enemyStrategy.getTypeOfPlayer()]
#HvH mod igre(online) - prvi igrac je human, drugi igrac je human      
class ModeHvHStrategy(ModeStrategy):
    def setPlayerModes(self, app):
        app.playerModes = ["human", "online"]
        
        
#osnovna klasa za odredjivanje odigravanja poteza vezanog za moda igraca
class PEModeStrategy():
    def __init__(self, app):
        self.app = app
        
    def playSpell(self):
        pass
        
        
class PlayerModeStrategy(PEModeStrategy):
    def playSpell(self):
        self.app.playerActionIndex = self.app.players[self.app.side].step(self.app.players[1-self.app.side])
        return self.app.players[self.app.side].spells[self.app.playerActionIndex]
  
class EnemyModeStrategy(PEModeStrategy):
    def playSpell(self):
        self.app.playerActionIndex = self.app.players[self.app.side].stepFuzzy(self.app.players[1-self.app.side])
        return self.app.players[self.app.side].spells[self.app.playerActionIndex]
  
class HumanModeStrategy(PEModeStrategy):
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
        
class OnlineModeStrategy(PEModeStrategy):
    def playSpell(self):
        if self.app.playerActionIndex == -1: return None
        return self.app.players[self.app.side].spells[self.app.playerActionIndex]