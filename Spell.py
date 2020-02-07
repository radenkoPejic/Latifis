import random
import Buff

class Spell:
    def __init__(self, cooldown, energy):
        self.cooldown = cooldown
        self.curr_cooldown = 0
        self.energy = energy
        self.id = -1
    def ID(self):
        return self.id;
    def underCooldown(self):
        return self.curr_cooldown!=0
    def reduceCooldown(self):
        if(self.curr_cooldown>0):
            self.curr_cooldown -= 1
    def castable(self, c):
        return (not self.underCooldown()) and (c.energy - self.energy >= 0)
    def cast(self,obj1,obj2=None):
        raise NotImplementedError("Subclass must implement abstract method")
    def cast2(self,obj1,obj2=None):
        raise NotImplementedError("Subclass must implement abstract method")
    def addOrReplaceBuff(self, c, newBuff):    
        for buff in c.buffs:
            if(type(buff)==type(newBuff)):
                #c.buffs.remove(buff)
                buff.curr_cooldown = newBuff.cooldown
                return 
        c.buffs.append(newBuff)
        
class AttackSpell(Spell):
    def __init__(self, cooldown, energy):
        super().__init__(cooldown, energy)
class DefenseSpell(Spell):
    def __init__(self, cooldown, energy):
        super().__init__(cooldown, energy)

        
class Attack(AttackSpell):
    def __init__(self, cooldown, energy, damage):
        self.id = 0
        self.damage = damage
        self.dodged = False
        self.criticalHit = False
        self.damageDone = 0
        self.color = "red"
        super().__init__(cooldown, energy)
        
    def addBuffs(self, c1, c2):
        pass
    def cast(self, c1, c2):
        if(self.castable(c1)):
            if(c1.stunned == False):
                self.curr_cooldown = self.cooldown
                c1.energy -= self.energy
                if(random.random()>c2.dodge):
                    self.dodged = False
                    self.addBuffs(c1,c2)
                    dmg = (1-c1.weaken)*(1-c2.protection)*self.damage*(1+0.1*(2*random.random()-1))
                    if(random.random()<c1.critical):
                        dmg *= 3
                        self.criticalHit = True
                    else:
                        self.criticalHit = False
                    self.damageDone = dmg
                    c2.health -= dmg
                    if(c2.health<=0):
                        c2.health = 0
                        c2.dead = True
                else:
                    self.dodged = True
        else:
            raise Exception()
            
    def cast2(self, c1, c2):
        if(self.castable(c1)):
            if(c1.stunned == False):
                #if(random.random()>c2.dodge):
                    c2.health -= c1.damage*(1+0.1*(2*random.random()-1))
                    if(c2.health<=0):
                        c2.health = 0
        else:
            raise Exception()

class EnergyAttack(AttackSpell):
    def __init__(self, cooldown, energy, damage):
        self.damage = damage
        self.dodged = False
        self.criticalHit = False
        self.damageDone = 0
        self.color = "yellow"
        super().__init__(cooldown, energy)
        self.id = 15
        
    def addBuffs(self, c1, c2):
        pass
    def cast(self, c1, c2):
        if(self.castable(c1)):
            if(c1.stunned == False):
                self.curr_cooldown = self.cooldown
                c1.energy -= self.energy
                if(random.random()>c2.dodge):
                    self.dodged = False
                    self.addBuffs(c1,c2)
                    #dmg = (1-c1.weaken)*(1-c2.protection)*self.damage*(1+0.1*(2*random.random()-1))
                    dmg = self.damage*(1+0.1*(2*random.random()-1))
                    if(random.random()<c1.critical):
                        dmg *= 3
                        self.criticalHit = True
                    else:
                        self.criticalHit = False
                    self.damageDone = dmg
                    c2.energy -= dmg
                    if(c2.energy<=0):
                        c2.energy = 0
                        #c2.dead = True
                else:
                    self.dodged = True
        else:
            print('puca ovde')
            raise Exception()

class BurnAttack(Attack):
    def addBuffs(self, c1, c2):
        if(random.random()<0.70):
            self.addOrReplaceBuff(c2, Buff.BurnBuff(3,3))
            #c2.buffs.append(Buff.BurnBuff(3,3))
class WeakenAttack(Attack):
    def addBuffs(self, c1, c2):
        if(random.random()<0.70):
            self.addOrReplaceBuff(c2, Buff.WeakenBuff(2, 40))		
            #c2.buffs.append(Buff.WeakenBuff(2,40))
class DrainAttack(Attack):
    def addBuffs(self, c1, c2):
        if(random.random()<0.9):
            self.addOrReplaceBuff(c2, Buff.DrainBuff(2,7))
            #c2.buffs.append(Buff.DrainBuff(2,7))               
class Heal(DefenseSpell):
    def __init__(self, cooldown, energy, health):
        self.id = 1
        self.health = health
        self.color = "green"
        super().__init__(cooldown, energy)
    def cast(self, c1, c2=None):
        if(self.castable(c1)):
            if(c1.stunned == False):
                self.curr_cooldown = self.cooldown
                c1.energy -= self.energy
                c1.health += self.health*(1+0.05*(2*random.random()-1))
                if(c1.health>c1.max_health):
                    c1.health = c1.max_health
        else:
            raise Exception()
    def cast2(self, c1, c2=None):
        if self.castable(c1):
            c1.health += self.health*(1+0.05*(2*random.random()-1))
            if(c1.health>c1.max_health):
                c1.health = c1.max_health
        else:
            raise Exception()

             
class Charge(DefenseSpell):
    def __init__(self, cooldown, energy, bonus):
        self.id = 2
        self.bonus = bonus
        self.color = "yellow"
        super().__init__(cooldown, energy)
    def addBuffs(self, c1, c2):
        pass
    def cast(self, c1, c2=None):
        if(self.castable(c1)):
            self.curr_cooldown = self.cooldown
            self.addBuffs(c1, c2)
            c1.energy += self.bonus
            if(c1.energy>c1.max_energy):
                c1.energy = c1.max_energy
        else:
            raise Exception()
    def cast2(self, c1, c2=None):
        if(self.castable(c1)):
            c1.energy += self.bonus
        else:
            raise Exception()
class ProtectionCharge(Charge):
    def addBuffs(self, c1, c2):
        if(random.random()<0.70):
            self.addOrReplaceBuff(c1, Buff.ProtectionBuff(1,20))
            #c1.buffs.append(Buff.ProtectionBuff(1,20))           
        
class BuffsSpell(Spell):
    def __init__(self, cooldown, energy, percent, duration):
        self.id = 3
        #self.buff = Buff.HealBuff(duration, percent)
        self.addBuff(duration, percent)
        super().__init__(cooldown, energy)
    def cast(self, c1, c2=None):
        if(self.castable(c1)):
            self.curr_cooldown = self.cooldown
            c1.energy -= self.energy
            #c1.buffs.append(self.buff)
            self.addOrReplaceBuff(c1, self.buff)
        else:
            raise Exception()
    def cast2(self, c1, c2=None):
        pass      
    def addBuff(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Long_FullHeal(BuffsSpell):
    def addBuff(self,duration, percent):
        self.buff = Buff.HealFullBuff(duration, percent)
class Long_CurrHeal(BuffsSpell):
    def addBuff(self,duration, percent):
        self.buff = Buff.HealCurrBuff(duration, percent)
class Long_MissHeal(BuffsSpell):
    def addBuff(self,duration, percent):
        self.buff = Buff.HealMissBuff(duration, percent)
class Flexible(BuffsSpell):
    def addBuff(self, duration, percent):
        self.buff = Buff.FlexBuff(duration, percent)
class Protection(BuffsSpell):
    def addBuff(self, duration, percent):
        self.buff = Buff.ProtectionBuff(duration, percent)
class Weaken(BuffsSpell):
    def addBuff(self, duration, percent):
        self.buff = Buff.WeakenBuff(duration, percent)
class Stun(Spell):
    def __init__(self, cooldown, energy, duration):
        self.addBuff(duration)
        super().__init__(cooldown, energy)
    def cast(self, c1, c2=None):
        if(self.castable(c1)):
            self.curr_cooldown = self.cooldown
            c1.energy -= self.energy
            if random.random() > c2.dodge:
                #c2.buffs.append(self.buff)
                self.addOrReplaceBuff(c2, self.buff)
                self.dodged = False
            else:
                self.dodged = True	
			
        else:
            raise Exception()
    def cast2(self, c1, c2=None):
        pass      
    def addBuff(self, duration):
        self.buff = Buff.StunBuff(duration)
		
class Rewind(Spell):
    def __init__(self, cooldown, energy, duration):
        super().__init__(cooldown, energy)
        self.duration = duration
        self.id = 16
    def cast(self, c1, c2=None):
        if(self.castable(c1)):
            self.curr_cooldown = self.cooldown
            c1.energy -= self.energy
            for spell in c1.spells:
                spell.curr_cooldown -= self.duration
                if(spell.curr_cooldown<0):
                    spell.curr_cooldown = 0
        else:
            raise Exception()
