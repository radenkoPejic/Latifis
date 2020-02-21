from offlinegame import *
from math import floor
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os
import jsonpickle

                
class MySubscribeCallback(SubscribeCallback):
    def __init__(self, app):
        self.app = app

    def presence(self, pubnub, presence):
        pass
        
    def status(self, pubnub, status):
        print(status)
        
    def message(self, pubnub, message):
        print("message.message[0]="+str(message.message[0]))
        
        if message.message[0] == 0:
            print(self.app.onlineGameStrategy.coinSent)
            print(message.message[1])
            if self.app.onlineGameStrategy.coinSent == False:
                self.app.onlineGameStrategy.enemyCoin = message.message[1]
            self.app.onlineGameStrategy.coinSent = False
            self.app.onlineGameStrategy.checkConnection()
        
        elif message.message[0] == 1:
            message.message[1] = message.message[1].replace("\\\"","\"")
            player2 = jsonpickle.decode(message.message[1])
            selectedPlayer2 = message.message[2]
            print("SELECTED PLAYER:", end ="")
            print(selectedPlayer2)
            coin = message.message[3]
            print(coin)
            if coin ==  self.app.onlineGameStrategy.enemyCoin:
                self.app.onlineGameStrategy.startOnlineGame(player2, selectedPlayer2)
                
        elif message.message[0] == 2:
            if self.app.side == 1:
                message.message[1] = message.message[1].replace("\\\"","\"")
                self.app.onlineGameStrategy.newPlayers[1] = jsonpickle.decode(message.message[1])
                self.app.onlineGameStrategy.received[0] = True
                self.app.onlineGameStrategy.checkReceived()
            
        elif message.message[0] == 3:
            if self.app.side == 1:
                message.message[1] = message.message[1].replace("\\\"","\"")
                self.app.onlineGameStrategy.newPlayers[0] = jsonpickle.decode(message.message[1])
                self.app.onlineGameStrategy.received[1] = True
                self.app.onlineGameStrategy.checkReceived()
                
        elif message.message[0] == 4:
            if self.app.side == 1:
                self.app.onlineGameStrategy.app.playerActionIndex = int(message.message[1])
                self.app.onlineGameStrategy.received[2] = True
                self.app.onlineGameStrategy.checkReceived()
              

    

class OnlineGameStrategy(GameStrategy):
    def __init__(self, app):
        super().__init__(app)
        self.reset()
        
    def reset(self):
        self.start()
        self.enemyCoin = -1
    
    def start(self):
        self.app.playerFirst = -1
        self.app.players = []
        self.newPlayers = [None, None]
        self.received = [False, False, False]
        self.coinSent = False
        self.playerCoin = -1
        
    def connection_callback(self, envelope, status):
    # Check whether request successfully completed or not
        if not status.is_error():
            self.coinSent = True
            pass
    
    def my_publish_callback(self, envelope, status):
    # Check whether request successfully completed or not
        if not status.is_error():
            pass  
            
    def prepare(self, player): 
        newA = jsonpickle.encode(player)
        newA = str(newA)
        newA = newA.replace("\'","\"")
        newA = newA.replace("\"","\\\"")
        return newA
        
    #odabir igraca za online igru
    def setGame(self):
        self.start()
        self.app.players = [None, None]
        self.app.playerStrategy = self.app.playerStrategies[self.app.selectedPlayer]
        
        self.app.playerStrategy.setPlayer(self.app, False, True)
        
        self.connectOnline()
        
    #konekcija sa protivnikom i slanje random broja za odabir ko igra prvi i koja je pozadina
    def connectOnline(self):
        self.playerCoin = random.random()
        self.app.pubnub.publish().channel("chan-1").message([0,self.playerCoin]).pn_async(self.connection_callback)
        
    #provera da li su se protivnici konektovali i da li je odredjeno ko igra prvi    
    def checkConnection(self):
        print("coins")
        print(self.playerCoin, self.enemyCoin)
        if self.playerCoin != -1 and self.enemyCoin != -1:
            if self.playerCoin < self.enemyCoin:
                self.app.firstPlayer = 0
                self.sendPlayer()
            elif self.playerCoin > self.enemyCoin:
                self.app.firstPlayer = 1
                self.sendPlayer()
            else: #ako nesto nije uspelo ili su se pogodila dva ista randoma pokusavamo ponovo
                self.playerCoin = self.enemyCoin = -1
                self.connectOnline()
    
    #slanje igraca online protivniku i postavljanje environmenta
    def sendPlayer(self):
        if self.app.firstPlayer == 0:
            pom = min(0.49, self.playerCoin)
        else:
            pom = min(0.49, self.enemyCoin)
        
        randEnvironment = floor(pom * 8)
        self.app.selectEnvironment(randEnvironment)
        self.app.pubnub.publish().channel("chan-1").message([1,self.prepare(self.app.players[0]), self.app.selectedPlayer, self.playerCoin]).pn_async(self.my_publish_callback)
  
  
  
    #pokretanje online igre
    def startOnlineGame(self, player2, selectedPlayer2):
        self.app.enemyStrategy = self.app.enemyStrategies[selectedPlayer2]
        self.app.enemyStrategy.addPlayer2(self.app, player2)
        self.level = 1
        print("START ONLINE GAME")
        self.app.startGame()
        
    
    #provera da li su stigle sve poruke od online protivnika
    def checkReceived(self):
        if self.received[0]==True and self.received[1]==True and self.received[2]==True:
            self.received[0] = self.received[1] = self.received[2] = False
            self.app.playerPlayed[1] = 1
            self.app.players[0] = self.newPlayers[0]
            self.app.players[1] = self.newPlayers[1]
            self.app.game.setPlayers(self.app.players)
            self.app.run()
            

    #slanje broja akcije i novih stanja nakon odigranog poteza
    def updateGameStatus(self):
        self.app.pubnub.publish().channel("chan-1").message([4,str(self.app.playerActionIndex)]).pn_async(self.my_publish_callback)
        self.app.pubnub.publish().channel("chan-1").message([2,self.prepare(self.app.players[0])]).pn_async(self.my_publish_callback)
        self.app.pubnub.publish().channel("chan-1").message([3,self.prepare(self.app.players[1])]).pn_async(self.my_publish_callback)
    