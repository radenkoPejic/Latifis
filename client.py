from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os
import threading
from DeepMalis import *
import jsonpickle

sem = threading.Semaphore()
pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-57b6337c-3f6d-4727-b5ec-3d9ccb6d737e'
pnconfig.subscribe_key = 'sub-c-26f8560a-4e3c-11ea-94fd-ea35a5fcc55f'
pnconfig.ssl = True
pubnub = PubNub(pnconfig)
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        global player1
        global player2
        print ("from device 1: ")
        print (message.message)
        if message.message[0] == 1:
            player2 = jsonpickle.decode((message.message[1]))
        else:
            player2 = jsonpickle.decode((message.message[1]))
            player1 = jsonpickle.decode((message.message[2]))
            action = message.message[3]
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("chan-1").execute()
## publish a message

time.sleep(10)
def initPlayers():
    global player1
    global player2
    player1 = DeepMalis3(1000,50,1000, tag='Novi11100', exploration_factor=0.05)
    player2 = None  
    state = [100, 100]
    winner = None
    turn = 'X'
    player_turn = player1
    player1.buffs = []
    player1.queue.reset()
initPlayers()    
def prepare(player):    
    newA = jsonpickle.encode(player)
    newA = str(newA)
    #newA.replace("\","\"")
    print("a :"+newA)
    newA = newA.replace("\"","\\\"")
    return newA
#slanje igraca i inicijalizacija komunikacije
pubnub.publish().channel("chan-1").message([1,prepare(player1)]).pn_async(my_publish_callback)
def doBuffsPlayer():
    i = 0
    while i < len(player1.buffs):
        if(player1.buffs[i].curr_cooldown>0):
            player1.buffs[i].castB(player1,player2)
            i+=1
        else:
            player1.buffs[i].restore(player1,player2)
            del(player1.buffs[i])
while True:
    global player2
    if player2 != None:
        break
while True:
    #global player1
    #global player2 
    sem.acquire()
    doBuffsPlayer()
    print(type(player1))
    print(type(player2))
    print("Player: ")
    print(player2)
    action = player1.get_next_action(player1.prev_state)
    print('Player: '+str(action))
    state = player1.take_action(action[0], player2)
    print(state)
    pubnub.publish().channel("chan-1").message([2,prepare(player1),prepare(player2),action]).pn_async(my_publish_callback)
    sem.release()
    if player1.health <= 0 or player2.health <=0:
        break
    time.sleep(10.25)