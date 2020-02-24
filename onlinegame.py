from offlinegame import *
from math import floor
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os
import jsonpickle


#klasa ciji se objekat pretplacuje na kanal radi osluskivanja poruka                
class MySubscribeCallback(SubscribeCallback):
    def __init__(self, app):
        self.app = app

    def presence(self, pubnub, presence):
        pass
        
    def status(self, pubnub, status):
        print(status)
        
    def message(self, pubnub, message):
        print("message.message[0]="+str(message.message[0]))
        
        #poruka 0 - oznacava inicijalnu poruku za uspostavljanje igre 
        if message.message[0] == 0:
            print(self.app.onlineGameStrategy.coinSent)
            print(message.message[1])
            #ako je online igra u toku ne reaguje se na tudju poruku za uspostavljanje igre
            if self.app.onlineGameStrategy.gameStarted == True: return
            #ako je stigla poruka od protivnika pamtimo njegov coin
            if self.app.onlineGameStrategy.coinSent == False:
                self.app.onlineGameStrategy.enemyCoin = message.message[1]
            self.app.onlineGameStrategy.coinSent = False
            #proveravamo konekciju
            self.app.onlineGameStrategy.checkConnection()
        
        #poruka 1 - oznacava drugu poruku za uspostavljanje igre
        elif message.message[0] == 1:
            message.message[1] = message.message[1].replace("\\\"","\"")
            #prihvatamo protivnickog igraca
            player2 = jsonpickle.decode(message.message[1])
            selectedPlayer2 = message.message[2]
            coin = message.message[3]
            print(coin)
            #ako smo zeleli da igramo online igru (i ako ne igramo neku offline igru)
            #i ako smo prihvatili coin od protivnika sa kojim smo razmenili coine u poruci 0
            #krecemo u postavljanje online igre i njeno startovanje
            if self.app.onlineGameStrategy.playerCoin != -1 and coin ==  self.app.onlineGameStrategy.enemyCoin:  
                print("SELECTED PLAYER:", end ="")
                print(selectedPlayer2)
                self.app.onlineGameStrategy.startOnlineGame(player2, selectedPlayer2)

                
        elif message.message[0] < 5:
            #ako je protivnik na potezu i ako je to protivnik sa kojim igramo 
            if self.app.side == 1 and str(self.app.onlineGameStrategy.enemyCoin)==message.message[1]:
                #poruka 2 - prihvatamo novi objekat protivnickog igraca sa apdejtovanim podacima 
                if message.message[0] == 2:
                    message.message[2] = message.message[2].replace("\\\"","\"")
                    self.app.onlineGameStrategy.newPlayers[1] = jsonpickle.decode(message.message[2])
                    self.app.onlineGameStrategy.received[0] = True
                    self.app.onlineGameStrategy.checkReceived()
                #poruka 3 - prihvatamo novi objekat prvog igraca sa apdejtovanim podacima     
                elif message.message[0] == 3:
                    message.message[2] = message.message[2].replace("\\\"","\"")
                    self.app.onlineGameStrategy.newPlayers[0] = jsonpickle.decode(message.message[2])
                    self.app.onlineGameStrategy.received[1] = True
                    self.app.onlineGameStrategy.checkReceived()
                #poruka 4 - prihvatamo indeks odigranog spella protivnickog igraca 
                elif message.message[0] == 4:
                    self.app.onlineGameStrategy.app.playerActionIndex = int(message.message[2])
                    self.app.onlineGameStrategy.received[2] = True
                    self.app.onlineGameStrategy.checkReceived()
              

#klasa za online strategiju igre
#pravimo samo jedan njen objekat na pocetku kreiranja aplikacije
class OnlineGameStrategy(GameStrategy):

    def __init__(self, app):
        super().__init__(app)
        self.reset()
    
    #resetovanje svih podataka pri kreiranju aplikacije ili pri pocetku offline igre ili na kraju online igre
    def reset(self):
        self.start()
        self.enemyCoin = -1
    
    #resetovanje svih podataka sem protivnickog coina (koji moramo upamtiti ako je neko neko poslao poruku 0)
    #zove se na klik misem pri odabranom online modu
    def start(self):
        self.app.playerFirst = -1
        self.app.players = []
        self.newPlayers = [None, None]
        self.received = [False, False, False]
        self.coinSent = False
        self.gameStarted = False
        self.randEnvironment = -1
        self.playerCoin = -1
    
    #callback pri uspostavljanju igre i slanju poruke 0 
    #kako bismo znali da li smo posiljalac ili primalac u tom trenutku
    def connection_callback(self, envelope, status):
    # Check whether request successfully completed or not
        if not status.is_error():
            self.coinSent = True
            pass
    #prazan standardni callback
    def my_publish_callback(self, envelope, status):
    # Check whether request successfully completed or not
        if not status.is_error():
            pass  
    #pripremanje - enkodovanje i serijalizacija objekta igraca pre slanja preko pubnuba    
    def prepare(self, player): 
        newA = jsonpickle.encode(player)
        newA = str(newA)
        newA = newA.replace("\'","\"")
        newA = newA.replace("\"","\\\"")
        return newA
        
    #odabir svog igraca za online igru
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
        
        self.randEnvironment = floor(pom * 8)
        self.app.pubnub.publish().channel("chan-1").message([1,self.prepare(self.app.players[0]), self.app.selectedPlayer, self.playerCoin]).pn_async(self.my_publish_callback)

  
    #pokretanje online igre
    def startOnlineGame(self, player2, selectedPlayer2):
        self.app.enemyStrategy = self.app.enemyStrategies[selectedPlayer2]
        self.app.enemyStrategy.addPlayer2(self.app, player2)
        self.level = 1
        print("START ONLINE GAME")
        self.gameStarted = True
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
        self.app.pubnub.publish().channel("chan-1").message([4, str(self.playerCoin), str(self.app.playerActionIndex)]).pn_async(self.my_publish_callback)
        self.app.pubnub.publish().channel("chan-1").message([2, str(self.playerCoin), self.prepare(self.app.players[0])]).pn_async(self.my_publish_callback)
        self.app.pubnub.publish().channel("chan-1").message([3, str(self.playerCoin), self.prepare(self.app.players[1])]).pn_async(self.my_publish_callback)
    