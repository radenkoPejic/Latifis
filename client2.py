from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os
import threading
from DeepMalis import *
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
        print ("from device 1: ")
        print (message.message)
        if message.message[0] == 1:
            player2 = message.message[1]
            player1.kreni = True
        else:
            player1 = message.message[1]
            player2 = message.message[2]
            action = message.message[3]
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("chan-1").execute()
## publish a message

time.sleep(15.25)
player1 = DeepMalis2(1000,50,1000, tag='Novi11100', exploration_factor=0.05)
player2 = None       
state = [100, 100]
winner = None
turn = 'X'
player_turn = player1
player1.buffs = []
player1.queue.reset()
pubnub.publish().channel("chan-1").message([1,player1]).pn_async(my_publish_callback)
def doBuffsPlayer():
    i = 0
    while i < len(player1.buffs):
        if(player1.buffs[i].curr_cooldown>0):
            player1.buffs[i].castB(player1,player2)
            i+=1
        else:
            player1.buffs[i].restore(player1,player2)
            del(player1.buffs[i])
            
            
while player2==None:
    time.sleep(1)
while True:
    sem.acquire()
    doBuffsPlayer()
    action = player1.get_next_action(player1.prev_state)
    print('Player: '+str(action))
    state = player1.take_action(action[0], player2)
    print(state)
    pubnub.publish().channel("chan-1").message([2,player1,player2,action]).pn_async(my_publish_callback)
    sem.release()
    time.sleep(10.25)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    