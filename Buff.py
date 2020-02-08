import random
from PIL import Image, ImageTk

class Buff:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.forTextBox = None
        self.buffSize = 30
        self.buffImage = None
        
    def stillActive(self):
        return True if (self.curr_cooldown > 0) else False
    def castB(self,obj1,obj2=None):
        self.curr_cooldown -= 1
    def restore(self,obj1,obj2=None):
        self.curr_cooldown = self.cooldown
        
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
class HealFullBuff(HealBuff):
    def __init__(self, cooldown, percent):
        self.image = ImageTk.PhotoImage(Image.open("resources/healFullBuff.png"))
        super().__init__(cooldown, percent)
        self.forTextBox = "FullHeal"
    def action(self, c1, c2):
        return (c1.max_health)*self.percent//100
        
class HealCurrBuff(HealBuff):
    def __init__(self, cooldown, percent):
        self.image = ImageTk.PhotoImage(Image.open("resources/healCurrBuff.png"))
        super().__init__(cooldown, percent)
        self.forTextBox = "CurrHeal"
    def action(self, c1, c2):
        return (c1.health)*self.percent//100
        
class HealMissBuff(HealBuff):
    def __init__(self, cooldown, percent):
        self.image = ImageTk.PhotoImage(Image.open("resources/healMissBuff.png"))
        super().__init__(cooldown, percent)
        self.forTextBox = "MissHeal"
    def action(self, c1, c2):
        return (c1.max_health-c1.health)*self.percent//100
        
        
class FlexBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.forTextBox = "Flex"
        self.percent = percent
        self.id = -1
        self.photo = Image.open("resources/flexBuff.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.dodge += self.percent
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.dodge -= self.percent
        
    
        
class ProtectionBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Protect"
        self.id = -1
        self.photo = Image.open("resources/protectionBuff.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.protection += self.percent//100
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.protection -= self.percent//100
		
class WeakenBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Weak"
        self.id = -1
        self.photo = Image.open("resources/weakenBuff.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.weaken += self.percent//100
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.weaken -= self.percent  //100   
		
class StunBuff(Buff):
    def __init__(self, cooldown):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.forTextBox = "Stun"
        self.id = -1 
        self.photo = Image.open("resources/stunBuff.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        if(self.curr_cooldown == (self.cooldown-1)):
            c1.stunned = True
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
        c1.stunned = False
		
class BurnBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Burn" 
        self.photo = Image.open("resources/burnBuff.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        super().castB(c1, c2)
        burn = c1.health*self.percent//100
        self.forTextBox = str(int(-burn))
        c1.health -= burn
        if(c1.health<0):
            c1.health = 0
    def restore(self, c1, c2=None):
        super().restore(c1,c2)
		
class DrainBuff(Buff):
    def __init__(self, cooldown, percent):
        super().__init__(cooldown)
        self.cooldown = cooldown
        self.curr_cooldown = cooldown
        self.percent = percent
        self.forTextBox = "Drain"
        self.photo = Image.open("resources/drainBuff.png")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
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
		
		
        
class EnvironmentBuff(Buff):
    def __init__(self, cooldown):
        super().__init__(cooldown)
		

def addOrReplaceBuff(c, newBuff):    
    for buff in c.buffs:
        if(type(buff)==type(newBuff)):
            c.buffs.remove(buff)
            break
    c.buffs.append(newBuff)
	
#ice 
class IcePlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Ice"
        self.photo = Image.open("resources/icePlus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
        self.casted = False
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.dodge += 0.05
            self.casted = True
#ice
class IceMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Ice"
        self.photo = Image.open("resources/iceMinus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
        self.casted = False		
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.critical -= 0.05
            self.casted = True            


#lava 
class LavaPlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Lava"
        self.photo = Image.open("resources/lavaPlus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
        self.casted = False	
    def castB(self,c1,c2=None):
        if not self.casted:	
            c1.protection += 0.1
            self.casted = True 
#lava 
class LavaMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Lava"
        self.photo = Image.open("resources/lavaMinus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        c1.health -= 0.01*c1.max_health
        if(c1.health<0):
            c1.health = 0


#desert 
class DesertPlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Desert"
        self.photo = Image.open("resources/desertPlus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        c1.energy += 0.1*c1.max_health
        if(c1.energy>c1.max_energy):
            c1.energy = c1.max_energy
#desert 
class DesertMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Desert"
        self.photo = Image.open("resources/desertMinus.png")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
        self.casted = False	
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.weaken += 0.05
            self.casted = True 
		
		
#forest 
class ForestPlus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Forest"
        self.photo = Image.open("resources/forestPlus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
        self.casted = False	
    def castB(self,c1,c2=None):
        if not self.casted:
            c1.critical += 0.1 
            self.casted = True 
#forest
class ForestMinus(EnvironmentBuff):
    def __init__(self):
        super().__init__(1)
        self.forTextBox = "Forest"
        self.photo = Image.open("resources/forestMinus.jpg")
        self.photo = self.photo.resize((self.buffSize, self.buffSize))
        self.image = ImageTk.PhotoImage(self.photo)
    def castB(self,c1,c2=None):
        if(random.random()<0.03):
            addOrReplaceBuff(c1, StunBuff(1))


        