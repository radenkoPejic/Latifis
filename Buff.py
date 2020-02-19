import random

class Buff:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.forTextBox = None
        self.buffSize = 30
        self.image = None
    def stillActive(self):
        return True if (self.curr_cooldown > 0) else False
    def castB(self,obj1,obj2=None):
        self.curr_cooldown -= 1
    def restore(self,obj1,obj2=None):
        self.curr_cooldown = self.cooldown
    def description(self):
        pass
        
class HealBuff(Buff):
    def __init__(self, cooldown, percent):
        self.id = 0
        self.percent = percent
        
        super().__init__(cooldown)
    def castB(self, c1, c2):
        super().castB(c1, c2)
        #c1.health += (c1.max_health-c1.health)*self.percent//100
        regenerate = self.action(c1,c2)
        self.forTextBox = str(int(regenerate))
        c1.health += regenerate
        if(c1.health>c1.max_health):
            c1.health = c1.max_health
    def action(self, c1, c2):
        raise NotImplementedError("Subclass must implement abstract method")
    def description(self):
        return self.__class__.__name__ + "\nHealth boosted by " + str(self.percent)
        
class HealFullBuff(HealBuff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown, percent)
        self.image = "resources/healFullBuff.png"
        self.forTextBox = "FullHeal"
    def action(self, c1, c2):
        return (c1.max_health)*self.percent//100
    def description(self):
        return super().description() + "% of maximum health"
        
class HealCurrBuff(HealBuff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown, percent)
        self.image = "resources/healCurrBuff.png"
        self.forTextBox = "CurrHeal"
    def action(self, c1, c2):
        return (c1.health)*self.percent//100
    def description(self):
        return super().description() + "% of current health"
        
class HealMissBuff(HealBuff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown, percent)
        self.image = "resources/healMissBuff.png"
        self.forTextBox = "MissHeal"
    def action(self, c1, c2):
        return (c1.max_health-c1.health)*self.percent//100
    def description(self):
        return super().description() + "% of maximum-current health"
        
        
class FlexBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.forTextBox = "Flex"
        self.percent = percent
        self.id = -1
        self.image = "resources/flexBuff.jpg"
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.dodge += self.percent
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.dodge -= self.percent
    def description(self):
        return self.__class__.__name__ + "\nDodge boosted by " + str(self.percent) + "%"
        
class ProtectionBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Protect"
        self.id = -1
        self.image = "resources/protectionBuff.jpg"
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.protection += self.percent//100
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.protection -= self.percent//100
    def description(self):
        return self.__class__.__name__ + "\nProtection boosted by " + str(self.percent) + "%"
        
class WeakenBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Weak"
        self.id = -1
        self.image = "resources/weakenBuff.jpg"
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.weaken += self.percent//100
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.weaken -= self.percent//100
    def description(self):
        return self.__class__.__name__ + "\nWeaken boosted by " + str(self.percent) + "%"   
        
class StunBuff(Buff):
    def __init__(self, cooldown):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.forTextBox = "Stun"
        self.id = -1 
        self.image = "resources/stunBuff.jpg"
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.stunned = True
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.stunned = False
    def description(self):
        return self.__class__.__name__ + "\nPlayer stunned - unable to cast any spell"
        
class BurnBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Burn"
        self.image = "resources/burnBuff.jpg"
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        burn = c1.health*self.percent//100
        self.forTextBox = str(int(-burn))
        c1.health -= burn
        if(c1.health<0):
            c1.health = 0
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
    def description(self):
        return self.__class__.__name__ + "\nHealth reduced by " + str(self.percent) + "%"   
        
class DrainBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Drain"
        self.image = "resources/drainBuff.png"
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        drain = c1.max_health*self.percent//100
        self.forTextBox = str(int(-drain))
        c1.health -= drain
        if(c1.health<0):
            c1.health = 0
        c2.health += drain
        if(c2.health > c2.max_health):
            c2.health = c2.max_health
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
    def description(self):
        return self.__class__.__name__ + "\n"+ str(self.percent)  + "% of health transferred to other player"       



def addOrReplaceBuff(c, newBuff):   
    for buff in c.buffs:
        if(type(buff)==type(newBuff)):
            c.buffs.remove(buff)
            break
    c.buffs.append(newBuff)     
        
        
        
class EnvironmentBuff(Buff):
    def __init__(self, cooldown):
        super().__init__(cooldown)
    
#ice 
class IcePlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Ice"
        self.image = "resources/icePlus.jpg"
        self.casted = False
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.dodge += 0.05
            self.casted = True
    def description(self):
        return self.__class__.__name__ + "\nDodge boosted by 5%"
#ice
class IceMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Ice"
        self.image = "resources/iceMinus.jpg"
        self.casted = False     
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.critical -= 0.05
            self.casted = True          
    def description(self):
        return self.__class__.__name__ + "\nCritical reduced by 5%"

#lava 
class LavaPlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Lava"
        self.image = "resources/lavaPlus.jpg"
        self.casted = False 
    def castB(self,c1,c2=None):
        if not self.casted: 
            c1.protection += 0.1
            self.casted = True 
    def description(self):
        return self.__class__.__name__ + "\nProtection boosted by 10%"
#lava 
class LavaMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Lava"
        self.image = "resources/lavaMinus.jpg"
    def castB(self,c1,c2=None):
        c1.health -= 0.01*c1.max_health
        if(c1.health<0):
            c1.health = 0
    def description(self):
        return self.__class__.__name__ + "\nHealth reduced by 1% of maximum health"

#desert 
class DesertPlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Desert"
        self.image = "resources/desertPlus.jpg"
    def castB(self,c1,c2=None):
        c1.energy += 0.1*c1.max_health
        if(c1.energy>c1.max_energy):
            c1.energy = c1.max_energy
    def description(self):
        return self.__class__.__name__ + "\nEnergy boosted by 10% of maximum health"
#desert 
class DesertMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Desert"
        self.image = "resources/desertMinus.png"
        self.casted = False 
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.weaken += 0.05
            self.casted = True 
    def description(self):
        return self.__class__.__name__ + "\nWeaken boosted by 5%"           
        
#forest 
class ForestPlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Forest"
        self.image = "resources/forestPlus.jpg"
        self.casted = False 
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.critical += 0.1 
            self.casted = True
    def description(self):
        return self.__class__.__name__ + "\nCritical boosted by 10%"            
#forest
class ForestMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Forest"
        self.image = "resources/forestMinus.jpg"
    def castB(self,c1,c2=None):
        #if(random.random()<0.03):
        if c1.health!=c1.max_health and c2.stunned==False \
        and abs(c1.health/c1.max_health - c2.health/c2.max_health)<0.015:
            addOrReplaceBuff(c1, StunBuff(1))
    def description(self):
        return self.__class__.__name__ + "\n3% chance of adding StunBuff to itself"       

        