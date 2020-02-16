import random
import os
from pathlib import Path
import keras.layers as Kl
import keras.models as Km
from Player import Malis
import Spell 
import numpy as np

class DeepMalis(Malis):

    def __init__(self, health, damage, energy, tag, exploration_factor=1):
        super().__init__(health, damage, energy, tag, exploration_factor)
        self.value_model = self.load_model()

    @staticmethod
    def state2array(state):
        index = int(state[0]*100+state[1])
        return np.array([index])
    def get_next_action(self, state):
        if random.random() > self.exploration_rate: # Explore (gamble) or exploit (greedy)
            return self.greedy_action(state)
        else:
            return self.random_action()

    def greedy_action(self, state):
        actions = self.calc_value(state)
        #print(actions)
        acts = actions
        for i in range(len(self.spells)):
            if(not self.spells[i].castable(self)):
                actions[0,i] = -999999 
        #print('=================Greedy '+str(np.argmax(actions)))
        return np.argmax(actions), np.argmax(actions)==np.argmax(acts)

    def random_action(self):
        available_spells = self.available_spell()
        randomSpell = random.choice(available_spells)
        for i in range(len(self.spells)):
            if(randomSpell == self.spells[i]):
                #print('=================Random '+str(i))
                return i, True
        print('=================Random omasio -1')
        return -1
    
    def update(self, state, winner, turnNum, action):
        # Train our model with new data
        self.train(state, winner, turnNum, action)

        # Finally shift our exploration_rate toward zero (less gambling)
        if self.exploration_rate > 0:
            self.exploration_rate -= self.exploration_delta
    
    def train(self, state, winner, turnNum, action, done):
        self.queue.put(state)
        if done:
            v_s = self.calc_value(self.prev_state)
            print(v_s)
            R = self.reward(winner, state, turnNum)
            v_s_tag = self.calc_value(state) #if winner is None else np.zeros((1,4))
            v_s[0,action] = (1-self.alpha)*v_s[0,action]+self.alpha*(R+self.epsilon*np.max(v_s_tag))#R + self.epsilon*np.amax(v_s_tag)#v_s_tag[0,action]#
            X_train = self.state2array(self.prev_state)
            target = v_s
            if target is not None:
                self.value_model.fit(X_train, target, epochs=10, verbose=0)
            self.prev_state = state

    def load_model(self):
        s = 'model_values' + self.tag + '.h5'
        model_file = Path(s)
        if model_file.is_file():
            model = Km.load_model(s, compile = False)
            print('load model: ' + s)
        else:
            print('new model')
            model = Km.Sequential()
            model.add(Kl.Dense(16, activation='relu', input_dim=(1)))
            model.add(Kl.Dense(16, activation='relu'))
            model.add(Kl.Dense(4, activation='linear'))
            model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'])

        model.summary()
        return model

    def calc_value(self, state):
        return self.value_model.predict(self.state2array(state))
    
    def save_values(self, c):
        s = 'model_values' + self.tag + c + '.h5'
        try:
            os.remove(s)
        except:
            pass
        self.value_model.save(s)
        
        
        
        
class DeepMalis2(DeepMalis):

    def __init__(self, health, damage, energy, tag, exploration_factor=1):
        super().__init__(health, damage, energy, tag, exploration_factor)
        self.spells = []
        self.spells.append(Spell.BurnAttack(1,150,60))
        self.spells.append(Spell.Long_FullHeal(6,300,10,4)) #promena
        self.spells.append(Spell.Charge(0,0,400))
        self.spells.append(Spell.Stun(7,200,3))
        
class DeepMalis3(DeepMalis):

    def __init__(self, health, damage, energy, tag, exploration_factor=1):
        super().__init__(health, damage, energy, tag, exploration_factor)
        self.spells = []
        self.spells.append(Spell.WeakenAttack(2,100,60))#2,100,60
        self.spells.append(Spell.Flexible(3,300,30,2))
        self.spells.append(Spell.ProtectionCharge(0,0,400))
        self.spells.append(Spell.DrainAttack(5,400,100))#5,400,100