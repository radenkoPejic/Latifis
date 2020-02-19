import Spell
from myQueue import myQueue

class rootPlayer:
    def step(self, enemy):
        pass
        
class Malis(rootPlayer):
    def __init__(self, health, damage, energy, tag, exploration_factor=1):
        self.health = health
        self.max_health = health
        self.energy = energy
        self.max_energy = energy
        self.damage = damage
        self.dead = False
        self.dodge = 0.2
        self.weaken = 0
        self.protection = 0
        self.stunned = False
        self.critical = 0.1
        self.playerCurrTurn = 0
        self.spells = []
        self.buffs = []
        self.spells.append(Spell.Attack(0,100,50))
        #self.spells.append(Spell.Heal(2,200,200))
        self.spells.append(Spell.Long_MissHeal(6,300,20,4))
        self.spells.append(Spell.Charge(0,0,600))
        self.spells.append(Spell.Stun(7,200,3))
        ###Player
        self.tag = tag
        self.exp_factor = exploration_factor
        self.exploration_rate = exploration_factor
        #self.exploration_rate = 1.0 # Initial exploration rate
        self.exploration_delta = 1.0 / 100 # Shift from exploration to explotation
        ###Agent
        self.epsilon = 0.95#0.9
        #od 50F3 do 55F3 self.alpha = 0.9
        self.alpha = 0.9
        self.prev_state = [100,100,0] #state-[playerHealth%,enemyHealth%]
        self.state = [100,100,0]
        self.queue = myQueue(3)
        ###
    def selfState(self):
        return 100*self.health//self.max_health
        
    def engState(self):
        return 100*self.energy//self.max_energy
        
    def refil(self):
        self.health = self.max_health
        self.energy = self.max_energy
        
    def available_spell(self):
        sol = []
        for spell in self.spells:
            if(spell.castable(self) == True):
                sol.append(spell)
        return sol
        
    def take_action(self, action, e):
        self.spells[action].cast(self,e)
        for carolija in self.spells:
            carolija.reduceCooldown()
        return [self.selfState(), e.selfState()]

    def reward(self, winner, state, turnNum):
        #if winner is 'Malis':
        #    R = 1
        #elif winner is None:
        """
        deltaPrev = self.prev_state[0]-self.prev_state[1]
        deltaState = state[0]-state[1]
        R = (-10)*((deltaState-deltaPrev)/100)
        """
        #R = ((self.prev_state[1]-state[1])/100)
        #else:
        #    R = -1
        
        #R = self.queue.calc()
        #deltaPrev = self.prev_state[0]-self.prev_state[1]
        #deltaState = state[0]-state[1]
        #R = np.sign(deltaState-deltaPrev)*abs((deltaState)*(deltaState-deltaPrev))
        #R = state[0]-state[1]
        #return R    
        if winner is 'Malis':
            #R = max(-0.001,1+10*(200-turnNum)/200)
            #R = exp(10*(1-turnNum/250))
            R = 1
        elif winner is None:
            #R =  (1-turnNum/250)
            #R = 0
            """
            deltaPrev = self.prev_state[0]-self.prev_state[1]
            deltaState = state[0]-state[1]
            R = ((deltaState-deltaPrev)/100)
            """
            R = self.queue.calc2()
        #elif state[0]-state[1]>0.5:
        #    R = 0.5
        else:
            R = -1
        return R  
        
    def isDead(self):
        return self.health<=0
    