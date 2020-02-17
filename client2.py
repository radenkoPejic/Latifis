from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os
from DeepMalis import *
from Player import *
import jsonpickle


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
        print(status)
    def message(self, pubnub, message):
        global player1
        global player2
        global received
        global tmpModel
        global action
        print("message.message[0]="+str(message.message[0]))
        if message.message[0] == 1:
            message.message[1] = message.message[1].replace("\\\"","\"")
            player2 = jsonpickle.decode(message.message[1])
        elif message.message[0] == 2:
            message.message[1] = message.message[1].replace("\\\"","\"")
            player2 = jsonpickle.decode(message.message[1])
            received[0] = True
        elif message.message[0] == 3:
            message.message[1] = message.message[1].replace("\\\"","\"")
            tmpModel = player1.value_model
            player1 = jsonpickle.decode(message.message[1])
            player1.value_model = tmpModel
            received[1] = True
        elif message.message[0] == 4:
            action = message.message[1]
            print(type(action))
            received[2] = True

player1 = DeepMalis3(1000,50,1000, tag="dm3vsdm21000vse11000", exploration_factor=10.05)
#player1.load_model()
player2 = None 
received = [False, False, False]
action = ""
tmpModel = None
            
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels("chan-1").execute()

## publish a message

time.sleep(15)

state = [100, 100]
winner = None
turn = 'X'
player_turn = player1
player1.buffs = []
player1.queue.reset()  

def prepare(player):   
    global tmpModel
    tmpModel = player.value_model
    player.value_model = None
    newA = jsonpickle.encode(player)
    player.value_model = tmpModel
    newA = str(newA)
    #newA.replace("\","\"")
    newA = newA.replace("\'","\"")
    newA = newA.replace("\"","\\\"")
    #print("a :"+newA)
    return newA
    
#slanje igraca i inicijalizacija komunikacije
pubnub.publish().channel("chan-1").message([5,prepare(player1)]).pn_async(my_publish_callback)
def doBuffsPlayer():
    global player1
    i = 0
    while i < len(player1.buffs):
        if(player1.buffs[i].curr_cooldown>0):
            player1.buffs[i].castB(player1,player2)
            i+=1
        else:
            player1.buffs[i].restore(player1,player2)
            del(player1.buffs[i])

while True:
    if player2 != None:
        break
cnt = 0       
print("Protivnik stigao")
while True:
    if received[0] == False or received[1] == False or received[2] == False:
        continue
    received[0]=received[1]=received[2]=False
    cnt+=1
    print("\nPotez " + str(cnt) +" primljeno:")
    print('Action: ', end="")
    print(action)
    print([player1.selfState(), player2.selfState()])
    doBuffsPlayer()
    print(type(player1))
    print(type(player2))
    action = player1.get_next_action(player1.prev_state)
    state = player1.take_action(action[0], player2)
    print("Poslato:")
    print('Action: '+str(action))
    print(state)
  
    if player1.health <= 0 or player2.health <=0:
        break
    time.sleep(2)    
    pubnub.publish().channel("chan-1").message([8,str(action[0])]).pn_async(my_publish_callback)
    pubnub.publish().channel("chan-1").message([6,prepare(player1)]).pn_async(my_publish_callback)
    pubnub.publish().channel("chan-1").message([7,prepare(player2)]).pn_async(my_publish_callback)