from DeepMalis import *
from Enemy import *
from tkinter import *

class Igra():
	def __init__(self, player, enemy):
		self.player1 = player
		self.player2 = enemy
		self.init_game()
		
	def doBuffsPlayer(self):
		i = 0
		while i < len(self.player1.buffs):
			if(self.player1.buffs[i].curr_cooldown>0):
				self.player1.buffs[i].castB(self.player1,self.player2)
				i+=1
			else:
				self.player1.buffs[i].restore(self.player1,self.player2)
				del(self.player1.buffs[i])
				
	def doBuffsEnemy(self):
		i = 0
		while i < len(self.player2.buffs):
			if(self.player2.buffs[i].curr_cooldown>0):
				self.player2.buffs[i].castB(self.player2,self.player1)
				i+=1
			else:
				self.player2.buffs[i].restore(self.player2,self.player1)
				del(self.player2.buffs[i])
		
	def game_winner(self):
		if(self.player1.isDead()==True):
			self.winner = "Enemy"
		if(self.player2.isDead()==True):
			self.winner = "Malis"
		return self.winner

	def init_game(self):
		self.state = [100, 100]
		self.winner = None
		self.turn = 'X'
		self.player_turn = self.player1
		self.player1.buffs = []
		self.player2.buffs = []

	def main(self, episodes):
		self.player1.exploration_delta = 1.0/episodes
		sum = 0
		won = 0
		for episode in range(episodes):
			i = 0
			potez = 0
			self.winner = None
			self.player1.refil()
			self.player2.refil()
			self.init_game()
			while self.winner is None:
				i+=1
				print('Potez: '+str(i))
				if(potez == 0):
					self.doBuffsPlayer()
					action = self.player1.get_next_action(self.player1.prev_state)
					state = self.player1.take_action(action, self.player2)
					print('State: '+str(state[0])+' '+str(state[1]))
					self.player1.train(state, self.winner, i, action)
				else:
					self.doBuffsEnemy()
					self.player2.step(self.player1)
				potez = 1-potez
				self.game_winner()
			print('Gotova jedna-----------------------------------------------------------------')
			if self.winner == 'Malis':
				won += 1
			print('Dobijene: '+str(won)+' ukupno: '+str(episode))
			sum += i
			if self.player1.exploration_rate > 0:
				self.player1.exploration_rate -= self.player1.exploration_delta
			if episode%100 == 0:
				self.player1.save_values(str(episode))
		print(won)
		print(sum//episodes)
		print(sum)
		
	def play_game(self):
		self.init_game()
		potez = 0
		i = 0
		while self.winner is None:
			i += 1
			if(potez == 0):
				self.doBuffsPlayer()
				action = self.player1.get_next_action(self.player1.prev_state)
				print('Player: '+str(action))
				state = self.player1.take_action(action, self.player2)
				print(state)
			else:
				self.doBuffsEnemy()
				action = self.player2.step(self.player1)
				print('Enemy: '+str(action))
			potez = 1-potez
			self.game_winner()
		print(self.winner+str(i))
	def checkEF(self, episodes, Ef, dEf):
		#ef = 1.0
		#deltaEf = 0.1
		ef = Ef
		deltaEf = dEf
		while(ef >= 0.0):
			sum = 0
			won = 0
			print(ef)
			for episode in range(episodes):
				i = 0
				potez = 0
				self.winner = None
				self.player1.refil()
				self.player2.refil()
				self.init_game()
				self.player1.exploration_rate = ef
				while self.winner is None:
					i+=1
					if(potez == 0):
						self.doBuffsPlayer()
						action = self.player1.get_next_action(self.player1.prev_state)
						state = self.player1.take_action(action, self.player2)
					else:
						self.doBuffsEnemy()
						self.player2.step(self.player1)
					potez = 1-potez
					self.game_winner()
				if self.winner == 'Malis':
					won += 1
				sum += i
				if self.player1.exploration_rate > 0:
					self.player1.exploration_rate -= self.player1.exploration_delta
			print(ef)
			print(won)
			print(sum//episodes)
			print(sum)
			print("---")
			ef -= deltaEf
def check_player():
	game = Igra(#DeepMalis2(1000,50,1000, tag='Novi5100', exploration_factor=0.5), #Novi6dobar
				DeepMalis3(1000,50,1000, tag='Novi9i210001', exploration_factor=1.0),
				#Enemy2(1000,12,200000, tag='Enemy2', exploration_factor=1))
				Enemy(2000,12,200000, tag='Enemy', exploration_factor=1))
	
	game.main(101)
	#game.checkEF(100, 1, 1)
	#game.play_game()

####Za pokretanje odkomentarisati ovo ispod
#root = Tk()
#check_player()