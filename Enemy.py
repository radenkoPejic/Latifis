from Spell import *
from Player import rootPlayer
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class Enemy(rootPlayer):
    def __init__(self, health, damage, energy,tag='Enemy', exploration_factor=1):
        self.health = health
        self.max_health = health
        self.energy = energy
        self.max_energy = energy
        self.damage = damage
        self.dead = False;
        self.dodge = 0.2
        self.weaken = 0
        self.protection = 0
        self.stunned = False
        self.critical = 0.05
        self.spells = []
        self.buffs = []
        self.spells.append(Attack(0,0,70))
        self.spells.append(EnergyAttack(5,0,250))
        self.spells.append(BurnAttack(7,0,100))
        self.spells.append(WeakenAttack(6,0,150))
        self.alwaysCastableSpellIndex = 0
        ###
        self.tag = tag
        self.exp_factor = exploration_factor
        
    def refil(self):
        self.health = self.max_health
        self.energy = self.max_energy
    
    #Obican step koriscen za treniranje    
    def step(self,p):
        spellID = 0
        self.spells[spellID].cast(self,p)
        return spellID
    
    #neophodno zbog pozivanja stepFuzzy f-je
    def initFuzzy(self,p):
        playerHealth = ctrl.Antecedent(np.arange(0, p.max_health+1, 1), 'playerHealth')
        playerEnergy = ctrl.Antecedent(np.arange(0, p.max_energy+1, 1), 'playerEnergy')
        health = ctrl.Antecedent(np.arange(0, self.max_health+1, 1), 'health')
        
        spellToPlay = ctrl.Consequent(np.array([0,1,2,3]), 'spellToPlay')
        
        playerHealth.automf(3)
        playerEnergy.automf(3)
        health.automf(3)
        
        spellToPlay['att'] = fuzz.trimf(spellToPlay.universe, [0, 0, 1])
        spellToPlay['eng'] = fuzz.trimf(spellToPlay.universe, [0, 1, 2])
        spellToPlay['burn'] = fuzz.trimf(spellToPlay.universe, [1, 2, 3])
        spellToPlay['weak'] = fuzz.trimf(spellToPlay.universe, [2, 3, 3])
        
        rules = []
        rules.append(ctrl.Rule(playerHealth['average'] & health['average'], spellToPlay['att']))
        rules.append(ctrl.Rule(health['poor'] | playerEnergy['good'], spellToPlay['eng']))
        rules.append(ctrl.Rule(playerHealth['poor'] | playerEnergy['poor'], spellToPlay['burn']))
        rules.append(ctrl.Rule(playerHealth['good'] & health['good'], spellToPlay['weak']))
        rules.append(ctrl.Rule(playerHealth['good'] & health['average'] , spellToPlay['weak']))
                
        tipping_ctrl = ctrl.ControlSystem(rules)
        
        self.tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        #spellToPlay.view()
    
    #potez fuzzy igraca
    def stepFuzzy(self,p):
        self.tipping.input['playerHealth'] = p.health
        self.tipping.input['playerEnergy'] = p.energy
        self.tipping.input['health'] = self.health
        
        self.tipping.compute()
        
        spellToCast = self.tipping.output['spellToPlay']
        
        sol = []
        for i in range(4):
            if(self.spells[i].castable(self)):
                sol.append(abs(spellToCast-i))
            else:
                sol.append(444)
        spellID = np.argmin(sol)
        #print(sol)
        self.spells[spellID].cast(self,p)
        for carolija in self.spells:
            carolija.reduceCooldown()
        return spellID
        
    def selfState(self):
        return 100*self.health//self.max_health
    def engState(self):
        return 100*self.energy//self.max_energy
    def isDead(self):
        return self.health<=0
        
class Enemy2(Enemy):
    def __init__(self, health, damage, energy,tag='Enemy2', exploration_factor=1):
        super().__init__(health, damage, energy, tag, exploration_factor=1)
        self.dodge = 0.35
        self.weaken = 0
        self.protection = 0.03
        self.stunned = False
        self.critical = 0.35
        self.spells = []
        self.buffs = []
        self.spells.append(Attack(0,0,50))
        self.spells.append(Long_FullHeal(9,0,10,2))
        self.spells.append(Rewind(12,0,3))
        self.spells.append(WeakenAttack(7,0,100))
        self.alwaysCastableSpellIndex = 0
        #self.spells.append(Stun(7,0,4))
        
    #Obican step koriscen za treniranje     
    def step(self,p):
        for spell in self.spells:
            spell.reduceCooldown()
        #castedSpell = self.spells[0]
        spellID = 0
        if(not self.spells[1].underCooldown()):
            if(random.random()<0.65):
                spellID = 1
                #castedSpell = self.spells[1]
        self.spells[spellID].cast(self,p)
        return spellID
    
    #neophodno zbog pozivanja stepFuzzy f-je    
    def initFuzzy(self,p):
        playerHealth = ctrl.Antecedent(np.arange(0, p.max_health+1, 1), 'playerHealth')
        playerEnergy = ctrl.Antecedent(np.arange(0, p.max_energy+1, 1), 'playerEnergy')
        health = ctrl.Antecedent(np.arange(0, self.max_health+1, 1), 'health')

        spellToPlay = ctrl.Consequent(np.array([0,1,2,3]), 'spellToPlay')
        
        playerHealth.automf(3)
        playerEnergy.automf(3)
        health.automf(3)
        
        spellToPlay['att'] = fuzz.trimf(spellToPlay.universe, [0, 0, 1])
        spellToPlay['heal'] = fuzz.trimf(spellToPlay.universe, [0, 1, 2])
        spellToPlay['rew'] = fuzz.trimf(spellToPlay.universe, [1, 2, 3])
        spellToPlay['weak'] = fuzz.trimf(spellToPlay.universe, [2, 3, 3])
        
        rules = []
        rules.append(ctrl.Rule(playerHealth['average'] & health['average'], spellToPlay['att']))
        rules.append(ctrl.Rule(health['poor'] | health['average'], spellToPlay['heal']))
        rules.append(ctrl.Rule(health['poor'] | playerEnergy['average'], spellToPlay['rew']))
        rules.append(ctrl.Rule(health['good'] | health['average'], spellToPlay['weak']))
        rules.append(ctrl.Rule(playerHealth['poor'] , spellToPlay['weak']))
        
        tipping_ctrl = ctrl.ControlSystem(rules)
        
        self.tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        #spellToPlay.view()