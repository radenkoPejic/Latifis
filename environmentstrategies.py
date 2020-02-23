from playerstrategies import *

#osnovna klasa za dodavanje environment plus i minus buffova igracima na osnovu environmenta
class EnvironmentStrategy():
    def setEnvironment(self, app):
        pass
        

class LavaStrategy():
    tag = "Lava"
    
    def setEnvironment(self, app):
        environmentPlusTags, environmentMinusTags = app.playerStrategy.getEnvironmentTags()
        if LavaStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[0], LavaPlus())
        if LavaStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[0], LavaMinus())
            
        environmentPlusTags, environmentMinusTags = app.enemyStrategy.getEnvironmentTags()
        if LavaStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[1], LavaPlus())
        if LavaStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[1], LavaMinus())            

class IceStrategy():
    tag = "Ice"
    
    def setEnvironment(self, app):
        environmentPlusTags, environmentMinusTags = app.playerStrategy.getEnvironmentTags()
        if IceStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[0], IcePlus())
        if IceStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[0], IceMinus())

        environmentPlusTags, environmentMinusTags = app.enemyStrategy.getEnvironmentTags()
        if IceStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[1], IcePlus())
        if IceStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[1], IceMinus())        
         
                
class DesertStrategy():
    tag = "Desert"
    
    def setEnvironment(self, app):
        environmentPlusTags, environmentMinusTags = app.playerStrategy.getEnvironmentTags()
        if DesertStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[0], DesertPlus())
        if DesertStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[0], DesertMinus())
            
        environmentPlusTags, environmentMinusTags = app.enemyStrategy.getEnvironmentTags()
        if DesertStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[1], DesertPlus())
        if DesertStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[1], DesertMinus())            
                       

class ForestStrategy():
    tag = "Forest"
    
    def setEnvironment(self, app):
        environmentPlusTags, environmentMinusTags = app.playerStrategy.getEnvironmentTags()
        if ForestStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[0], ForestPlus())
        if ForestStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[0], ForestMinus())
                  
        environmentPlusTags, environmentMinusTags = app.enemyStrategy.getEnvironmentTags()
        if ForestStrategy.tag in environmentPlusTags:
            Buff.addOrReplaceBuff(app.players[1], ForestPlus())
        if ForestStrategy.tag in environmentMinusTags:
            Buff.addOrReplaceBuff(app.players[1], ForestMinus())    

