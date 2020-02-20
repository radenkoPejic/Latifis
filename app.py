from tkinter import ttk
from igra import Igra
from onlinegame import *
from math import ceil
import pygame
import os
        


class Application():

    def __init__(self, root, pubnub):
        self.root = root        
        self.root.title("Latifis")
        self.rootWidth = 806
        self.rootHeight = 449
        self.root.geometry(""+str(self.rootWidth)+"x"+str(self.rootHeight))
        self.root.resizable(0, 0)
        self.root.iconbitmap("resources/icon.ico")
        
        self.pubnub = pubnub
        self.pubnub.add_listener(MySubscribeCallback(self))
        self.pubnub.subscribe().channels("chan-1").execute()
        
        self.backgroundCanvas = None
        self.backgroundPhoto = None
        self.backgroundImage = None
        
        self.style = None
        self.playerHealth = 0
        self.playerStartHealth = 0
        self.playerEnergy = 0
        self.playerStartEnergy = 0

        self.enemyHealth = 0
        self.enemyStartHealth = 0
        self.enemyEnergy = 0
        self.enemyStartEnergy = 0
        
        self.playerStatusCanvas = None
        self.playerStatusPhoto = None
        self.playerStatusImage = None
        self.playerHealthText = None
        self.playerEnergyText = None
        
        self.playerHealthBar = None
        self.playerEnergyBar = None

        self.playerTexts = []
        
        self.enemyStatusCanvas = None
        self.enemyStatusPhoto = None
        self.enemyStatusImage = None
        self.enemyHealthText = None
        self.enemyEnergyText = None
        
        self.enemyHealthBar = None
        self.enemyEnergyBar = None

        self.enemyTexts = []
        
        self.turnCanvas = None
        self.turnPhoto = None
        self.turnImage = None
        self.turnText = None
        
        self.spellCanvas = None
        self.spellCanvasPhoto = None
        self.spellCanvasImage = None
        self.spellCanvasText = None
        
    
        self.spellCanvasButtons = []
        self.lightBrown = "#cc9e71"
        self.darkBrown = "#522e0a"
        
        
        self.afterTime = 1500
        self.switchTime = 500
        self.checkTime = 10000
        self.side = 0
        
        self.potez = None
        self.cooldowns = []
        self.castables = []
        self.playerActionIndex = None
        
        self.spellImages = []
        self.spellHoverLabels = []
        
        self.looserImage = ImageTk.PhotoImage(Image.open("resources/looser.jpg"))
        self.buffImage = ImageTk.PhotoImage(Image.open("resources/transparent.png"))
        
        self.criticalImage = ImageTk.PhotoImage(Image.open("resources/criticalhit.png"))
        self.criticalImages = []

        self.playerBuffImages = []
        self.playerBuffPhotos = [self.buffImage, self.buffImage, self.buffImage, self.buffImage, self.buffImage, self.buffImage]
        self.playerBuffTexts = []
        
        self.enemyBuffImages = []
        self.enemyBuffPhotos = [self.buffImage, self.buffImage, self.buffImage, self.buffImage, self.buffImage, self.buffImage]
        self.enemyBuffTexts = []
        
        self.firstPlayer = 0
        self.players = []
        self.newPlayers = [None, None]
        self.playerStrategy = None
        self.enemyStrategy = None

        self.dodgeGifs = []
        
        self.playerSpellGifs = []
        
        self.playerSpellGifs = []
        self.playerGif = None

        self.enemySpellGifs = []
        self.enemyGif = None
        
        self.environment = -1
        self.environmentTags = ["forest", "desert", "lava", "ice"]
        self.environmentTextColors = ["black", "black", "white", "black"]
        
        self.playerWinnerGif = None
        self.endGameCanvas = None
        
        self.endGameSound = pygame.mixer.Sound("resources/endgame.wav")
        
        self.menuCanvas = None
        
        self.game = None
                
        self.musicVolume = 100
        self.playerModes = []
        self.modeStrategies = [None, None] 
        self.playerPlayed = []
        
        self.onlineGameStrategy = OnlineGameStrategy(self)
        self.gameStrategy = None
        
        self.clockAfter = None


    #prikaz buffova, maksimalne duzine liste 6, ako je kraca dopunjuje se prikaz skrivenom difolt slikom
    def showPlayerBuffs(self):
        for i in range (len(self.playerBuffImages)):
            
            if i < len(self.players[0].buffs):
                photo = Image.open(self.players[0].buffs[i].image)
                size = self.players[0].buffs[i].buffSize
                photo = photo.resize((size, size))
                self.playerBuffPhotos[i] = ImageTk.PhotoImage(photo)
                self.playerStatusCanvas.itemconfig(self.playerBuffImages[i], image = self.playerBuffPhotos[i], state = "normal")
                txt = ""
                if self.players[0].buffs[i].forTextBox != None: 
                    txt = self.players[0].buffs[i].forTextBox.center(7)
                self.playerStatusCanvas.itemconfig(self.playerBuffTexts[i], text = txt)
            else:
                self.playerBuffPhotos[i] = self.buffImage
                self.playerStatusCanvas.itemconfig(self.playerBuffImages[i], image = self.playerBuffPhotos[i], state = "hidden")
                self.playerStatusCanvas.itemconfig(self.playerBuffTexts[i], text = "")
            
            
        for txt in self.enemyBuffTexts:
            self.enemyStatusCanvas.itemconfig(txt, text = "")
    
    def showEnemyBuffs(self):
        for i in range (len(self.enemyBuffImages)):
            if i < len(self.players[1].buffs):
                photo = Image.open(self.players[1].buffs[i].image)
                size = self.players[1].buffs[i].buffSize
                photo = photo.resize((size, size))
                self.enemyBuffPhotos[i] = ImageTk.PhotoImage(photo)
                self.enemyStatusCanvas.itemconfig(self.enemyBuffImages[i], image = self.enemyBuffPhotos[i], state = "normal")
                txt = ""
                if self.players[1].buffs[i].forTextBox != None: 
                    txt = self.players[1].buffs[i].forTextBox.center(7)
                self.enemyStatusCanvas.itemconfig(self.enemyBuffTexts[i], text = txt)
            else:
                self.enemyBuffPhotos[i] = self.buffImage
                self.enemyStatusCanvas.itemconfig(self.enemyBuffImages[i], image = self.enemyBuffPhotos[i], state = "hidden")
                self.enemyStatusCanvas.itemconfig(self.enemyBuffTexts[i], text = "")
            
            
        for txt in self.playerBuffTexts:
            self.playerStatusCanvas.itemconfig(txt, text = "")
            
    #apdejt svih progres barova, zaokruzivanje na prvi veci (ceil)    
    def updateStatus(self):
        self.playerHealthBar["value"] = 100*self.players[0].health/self.players[0].max_health
        self.playerEnergyBar["value"] = 100*self.players[0].energy/self.players[0].max_energy
        self.playerHealthBar.update()
        self.playerEnergyBar.update()
        self.playerStatusCanvas.itemconfig(self.playerHealthText, text = "Health "+str(ceil(self.players[0].health)))
        self.playerStatusCanvas.itemconfig(self.playerEnergyText, text = "Energy "+str(ceil(self.players[0].energy)))
        
        self.enemyHealthBar["value"] = 100*self.players[1].health/self.players[1].max_health
        if self.players[1].max_energy == 20000:
            self.enemyEnergyBar["value"] = 100
        else:
            self.enemyEnergyBar["value"] = 100*self.players[1].energy/self.players[1].max_energy
        self.enemyHealthBar.update()
        self.enemyEnergyBar.update()
        self.enemyStatusCanvas.itemconfig(self.enemyHealthText, text = "Health "+str(ceil(self.players[1].health)))
        if self.players[1].max_energy != 20000:
            self.enemyStatusCanvas.itemconfig(self.enemyEnergyText, text = "Energy "+str(ceil(self.players[1].energy)))
    
    def createTexts(self, texts, x, y, anch = NW):
        texts.clear()
        texts.append(self.backgroundCanvas.create_text(x-1, y-1, anchor = anch, font = ("Purisa", 20, "bold"), text = ""))
        texts.append(self.backgroundCanvas.create_text(x-1, y+1, anchor = anch, font = ("Purisa", 20, "bold"), text = ""))
        texts.append(self.backgroundCanvas.create_text(x+1, y-1, anchor = anch, font = ("Purisa", 20, "bold"), text = ""))
        texts.append(self.backgroundCanvas.create_text(x+1, y+1, anchor = anch, font = ("Purisa", 20, "bold"), text = ""))
        texts.append(self.backgroundCanvas.create_text(x, y, anchor = anch, font = ("Purisa", 20, "bold"), text = ""))       
    
    def showText(self, texts, ispis, color = "white"):
        environmentColor = self.environmentTextColors[self.environment]
        for i in range (len(texts)-1):
            self.backgroundCanvas.itemconfig(texts[i], text = ispis, fill = environmentColor)
        self.backgroundCanvas.itemconfig(texts[len(texts)-1], text = ispis, fill = color)
        

    def run(self):
        
        if self.game.winner is None:
            turn = self.potez//2 + 1
            
            #odlucivanje ko je na redu
            side = self.potez % 2
            if self.firstPlayer == 1:
                side = 1 - side
            
            #pulsiranje u kriticnim momentima za prvog igraca pred poraz
            if self.players[0].health < 150:
                self.pulseSound.play()
            
            
            #dolazak na potez - jos nije odluceno sta se igra
            if self.playerPlayed[side]==0:
                                    
                
                #ispis koji je igrac na potezu uz zaustavljanje protivnickih gifova
                #primena buffova na trenutnog igraca i prikazivanje stanja buffova za oba
                if side == 0:
                    self.turnCanvas.itemconfig(self.turnText, text = "Player's turn " + str(turn))
                    self.enemyGif.pause()
                    self.enemySpellGifs[self.playerActionIndex].pause()
                    self.game.doBuffsPlayer()
                    self.showEnemyBuffs()  
                    self.showPlayerBuffs()
                       
                else:
                    self.turnCanvas.itemconfig(self.turnText, text = "Enemy's turn " + str(turn))
                    self.playerGif.pause()
                    self.playerSpellGifs[self.playerActionIndex].pause()
                    self.game.doBuffsEnemy()
                    self.showPlayerBuffs()
                    self.showEnemyBuffs()    
                    
                
                #skrivanje svih prikaza za damage i pauziranje dodge gifa trenutnog igraca
                self.showText(self.playerTexts, "")
                self.showText(self.enemyTexts, "")
                self.backgroundCanvas.itemconfig(self.criticalImages[side], state = "hidden")
                self.dodgeGifs[side].pause()
                
                
                #ako je igrac kompjuterski nema cekanja na odabir spella klikom misa
                if self.playerModes[side] == "player" or self.playerModes[side] == "enemy":
                    self.playerPlayed[side] = 1
                    
                elif self.playerModes[0] == "human" and side == 0:
                    #ako je igrac stunovan preskace potez ali mu stavljamo da je odigrao neki uvek moguci
                    #potez(charge je obicno uvek castable) kako bi se igracev gif prikazao u odredjenoj brzini
                    if self.players[0].stunned == True:
                        self.playerPlayed[0] = 1
                        self.playerActionIndex = 2
                    else:
                        #ako je prvi igrac covek cupka u mestu
                        self.playerGif.wait()
                        #saljemo brojeve za ispis clocku na glup nacin jer radi root.after 
                        #gleda satnja promenljivih u momentu kada prodje aftertime
                        pomPotez = self.potez
                        #mora malo kasnije da bi se video prikaz
                        self.root.after(200, lambda: self.updateClok(pomPotez, 10)) 
                        self.root.after(1*1000, lambda: self.updateClok(pomPotez, 9)) 
                        self.root.after(2*1000, lambda: self.updateClok(pomPotez, 8)) 
                        self.root.after(3*1000, lambda: self.updateClok(pomPotez, 7)) 
                        self.root.after(4*1000, lambda: self.updateClok(pomPotez, 6)) 
                        self.root.after(5*1000, lambda: self.updateClok(pomPotez, 5)) 
                        self.root.after(6*1000, lambda: self.updateClok(pomPotez, 4)) 
                        self.root.after(7*1000, lambda: self.updateClok(pomPotez, 3)) 
                        self.root.after(8*1000, lambda: self.updateClok(pomPotez, 2)) 
                        self.root.after(9*1000, lambda: self.updateClok(pomPotez, 1)) 
                        #pamtimo da bi smo opozvali check ako je covek na vreme odigrao potez
                        self.clockAfter = self.root.after(self.checkTime, lambda: self.checkTimeToPlay(pomPotez))
                    

                
                #pamtimo cooldownove pre odigravanja poteza zbog prikaza u kucicama
                self.cooldowns = []
                self.castables = []
                for i in range (len(self.players[0].spells)):
                    self.cooldowns.append(self.players[0].spells[i].curr_cooldown)
                    self.castables.append(self.players[0].spells[i].castable(self.players[0]))
                
                #pamtimo buffove pre odigravanja poteza zbog prikaza u status barovima
                self.playerBuffDescrs = []
                self.enemyBuffDescrs = []
                for i in range (len(self.players[0].buffs)):
                    self.playerBuffDescrs.append(self.players[0].buffs[i].description())
                for i in range (len(self.players[1].buffs)):
                    self.enemyBuffDescrs.append(self.players[1].buffs[i].description())
                #apdejt prikaza ako je misom hoverovan neki od buffova a nije bilo motiona
                self.checkHoverBuffs()           
                               
                #apdejt svih kucica za spell
                for ix in range (len(self.spellCanvasButtons)):
                    if self.castables[ix] == True:
                        self.spellCanvasButtons[ix]["state"] = "normal"
                        self.spellCanvasButtons[ix]["text"] = ""
                        self.spellCanvasButtons[ix]["bg"] = self.lightBrown
                    else:
                        self.spellCanvasButtons[ix]["state"] = "disabled"
                        if self.cooldowns[ix]>0:
                            self.spellCanvasButtons[ix]["text"] = str(self.cooldowns[ix])
                        else:
                            self.spellCanvasButtons[ix]["text"] = ""
                        self.spellCanvasButtons[ix]["bg"] = self.lightBrown
                                
               
                #drugog igraca gasimo i preuzimamo potez
                self.playerPlayed[1-side] = 0
                
                #apdejt stanja na status barova 
                self.updateStatus()
                
                #provera da neko nije izgubio zbog dejstva buffova
                if self.game.game_winner() != None:
                    self.root.after(self.afterTime+self.switchTime, self.run)
                    return
            
            
            #promena strane nakon prelaznog dela i preuzimanja poteza
            self.side = side
        
        
            #igranje poteza - izvrsavanje odabranog spella
            if self.playerPlayed[self.side]==1:
                self.potez += 1
                
                self.root.after(200, lambda: self.spellCanvas.itemconfig(self.playerClockText, text = ""))
                
                #dohvatanje odigranog spella ako je uopste odigran
                spell = self.modeStrategies[self.side].playSpell()
            
            
                #slanje poruke ka online protivniku
                if self.side == 0 and self.playerModes[1]=="online":
                    self.onlineGameStrategy.updateGameStatus()
               
                if self.playerActionIndex > -1:
                    #apdejt poteza i pokretanje gifova izazvanih spellom
                    if self.side == 0:  
                        self.playerGif.setSpell(spell)
                        self.playerGif.goOn()
                        if not self.players[0].stunned:
                            self.playerSpellGifs[self.playerActionIndex].goOn()
                        
                    else:
                        self.enemyGif.setSpell(spell)
                        self.enemyGif.goOn()
                        if not self.players[1].stunned:
                            self.enemySpellGifs[self.playerActionIndex].goOn() 
                                    
                    #oznacavanje kucice odigranog spella
                    if self.side==0 and self.players[0].stunned == False:
                        self.spellCanvasButtons[self.playerActionIndex]["state"] = "normal"
                        self.spellCanvasButtons[self.playerActionIndex]["text"] = ""
                        self.spellCanvasButtons[self.playerActionIndex]["bg"] = "yellow"

                #provera kraja igre 
                self.game.game_winner()

                #kraj poteza i prelazak na sledeci potez
                self.root.after(self.afterTime+self.switchTime, self.run)
                
                
        #ako je pobedio prvi igrac prikazuje se winnergif preko celog ekrana i prelazi se na sledeci nivo ako postoji       
        elif self.game.winner == "Malis":
            self.updateStatus()
            self.turnCanvas.itemconfig(self.turnText, text = "     Player won")
            self.stopGame()
            self.root.after(2*self.afterTime, self.playerWinnerGif.goOn)
            #fadeout za background muziku
            pygame.mixer.music.fadeout(2*self.afterTime)
            self.gameStrategy.nextLevel()
            
            
        #ako je pobedio drugi igrac prikazu je se looserimage preko celog ekrana i sledi povratak u glavni meni    
        else:
            self.updateStatus()
            self.turnCanvas.itemconfig(self.turnText, text = "     Enemy won")
            self.stopGame()
            #fadeout za background muziku
            pygame.mixer.music.fadeout(2*self.afterTime)
            self.gameStrategy.endOfGame()
            
    
    #zaustavljanje gifova igraca
    #moze se doraditi - skloniti prikaze helti ili jos necega?
    def stopGame(self):
        app.playerStrategy.stop(self)
        app.enemyStrategy.stop(self)
    
    
    def backToMenu(self):
        self.onlineGameStrategy.reset()
        self.gameStrategy = None
        self.root.after(self.afterTime*3, self.hideLoser)
        self.root.after(self.afterTime*3, self.playerWinnerGif.pause)
        self.root.after(self.afterTime*3, self.mainMenu)
    
    def mainMenu(self):
        self.menuCanvas.pack()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resources/mainMenu.mp3")
        pygame.mixer.music.set_volume(self.musicVolume/100)
        pygame.mixer.music.play(-1)
    
    #prikaz looser slike i pustanje end game zvuka
    def showLoser(self):
        self.endGameCanvas.pack()
        self.endGameCanvas.itemconfig(self.looserImageCanvas, state="normal")
        self.endGameSound.play()
    
    #sakrivanje prikaza looser slike
    def hideLoser(self):
        self.endGameCanvas.itemconfig(self.looserImageCanvas, state="hidden")
        
    #pokretanje aplikacije - postavljanje prikaza aplikacije
    def startApp(self):
        self.potez = 0
        self.environment = -1
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("yellow.Horizontal.TProgressbar", troughcolor="white", bordercolor="white", background="yellow")
        self.style.configure("red.Horizontal.TProgressbar", troughcolor="white", bordercolor="white", background="red")
    
        self.backgroundCanvas = Canvas(self.root, bd=0, highlightthickness=0, relief="ridge")
        self.backgroundCanvas.place(x = 0, y = 0, width = self.rootWidth, height = self.rootHeight)

        self.backgroundPhoto = Image.open("resources/background1.jpg")
        self.backgroundPhoto = self.backgroundPhoto.resize((self.rootWidth, self.rootHeight))
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundPhoto)
        self.backgroundCanvas.create_image(0, 0, image = self.backgroundImage, anchor = NW)
        
        statusCanvasX = 20
        statusCanvasWidth = 250
        self.playerStatusCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief="ridge")
        self.playerStatusCanvas.place(width = statusCanvasWidth, height = 100, x = statusCanvasX, y = 2)
        self.playerStatusPhoto = Image.open("resources/box.png")
        self.playerStatusPhoto = self.playerStatusPhoto.resize((250, 100))
        self.playerStatusImage = ImageTk.PhotoImage(self.playerStatusPhoto)
        self.playerStatusCanvas.create_image(0, 0, image = self.playerStatusImage, anchor = NW)
        barTextX = 10
        self.playerHealthText = self.playerStatusCanvas.create_text(barTextX, 10, anchor = NW, text = "Health "+str(self.playerHealth), fill = "white")
        self.playerEnergyText = self.playerStatusCanvas.create_text(barTextX, 31, anchor = NW, text = "Energy "+str(self.playerEnergy), fill = "white")

        barX = 95
        barWidth = 120
        self.playerHealthBar = ttk.Progressbar(self.playerStatusCanvas, style = "red.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.playerHealthBar.place(width = barWidth, height = 15, x = barX, y = 10)
        self.playerEnergyBar = ttk.Progressbar(self.playerStatusCanvas, style = "yellow.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.playerEnergyBar.place(width = barWidth, height = 15, x = 95, y = 31)

        
        self.enemyStatusCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief="ridge")
        self.enemyStatusCanvas.place(width = 250, height = 100, x = self.rootWidth - statusCanvasX - statusCanvasWidth, y = 2)
        self.enemyStatusPhoto = Image.open("resources/box.png")
        self.enemyStatusPhoto = self.playerStatusPhoto.resize((250, 100))
        self.enemyStatusImage = ImageTk.PhotoImage(self.enemyStatusPhoto)
        self.enemyStatusCanvas.create_image(0, 0, image = self.enemyStatusImage, anchor = NW)
        self.enemyHealthText = self.enemyStatusCanvas.create_text(statusCanvasWidth - barTextX, 10, anchor = NE, text = "Health "+str(self.enemyHealth), fill = "white")
        self.enemyEnergyText = self.enemyStatusCanvas.create_text(statusCanvasWidth - barTextX, 31, anchor = NE, text = "Energy infinite", fill = "white")

        self.enemyHealthBar = ttk.Progressbar(self.enemyStatusCanvas, style = "red.Horizontal.TProgressbar",orient="horizontal", mode="determinate")
        self.enemyHealthBar.place(width = barWidth, height = 15, x = statusCanvasWidth - barWidth - barX, y = 10)
        self.enemyEnergyBar = ttk.Progressbar(self.enemyStatusCanvas, style = "yellow.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.enemyEnergyBar.place(width = barWidth, height = 15, x = statusCanvasWidth - barWidth - barX, y = 31)
        

        self.turnCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief="ridge")
        self.turnCanvas.place(width= 200, height = 50, x = self.rootWidth/2 - 200/2 , y = 7)
        self.turnPhoto = Image.open("resources/turn.jpg")
        self.turnPhoto= self.turnPhoto.resize((200, 50))
        self.turnImage = ImageTk.PhotoImage(self.turnPhoto)
        self.turnCanvas.create_image(0, 0, image = self.turnImage, anchor = NW)
        self.turnText = self.turnCanvas.create_text(12, 12, anchor = NW, text = "", font = ("Purisa", 17))
        
        spellCanvasWidth = 400
        spellCanvasX = self.rootWidth/2 - spellCanvasWidth/2
        self.spellCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief="ridge")
        self.spellCanvas.place(width = spellCanvasWidth, height = 75, x = spellCanvasX, y = 350)
        self.spellCanvasPhoto = Image.open("resources/box.png")
        self.spellCanvasPhoto = self.spellCanvasPhoto.resize((spellCanvasWidth, 75))
        self.spellCanvasImage = ImageTk.PhotoImage(self.spellCanvasPhoto)
        self.spellCanvas.create_image(0, 0, image = self.spellCanvasImage, anchor = NW)
        self.spellCanvasText = self.spellCanvas.create_text(73, 22, anchor = NW, text = "Spells:", font = ("Purisa", 17), fill = "white")
        
        self.playerClockPhoto = Image.open("resources/clock.png")
        self.playerClockPhoto = self.playerClockPhoto.resize((40, 60))
        self.playerClockImage = ImageTk.PhotoImage(self.playerClockPhoto)
        self.spellCanvas.create_image(15, 6, image = self.playerClockImage, anchor = NW)
        
        self.playerClockText = self.spellCanvas.create_text(35, 36, anchor = CENTER, text = "", font = ("Purisa", 25, "bold"), fill = "red")
        
        self.playerBuffImages = []
        self.playerBuffTexts = []
        self.playerBuffHoverLabels = []
        self.playerBuffHoverLabelsPlaces = []

        for x in range (5, 230, 40):
            self.playerBuffImages.append(self.playerStatusCanvas.create_image(x, 55, image=self.buffImage, anchor = NW))
            self.playerStatusCanvas.itemconfig(self.playerBuffImages[len(self.playerBuffImages)-1], state="hidden")
            self.playerBuffTexts.append(self.playerStatusCanvas.create_text(x, 86, anchor = NW, text = "", font = ("Purisa", 8), fill = "white"))
            self.playerStatusCanvas.bind("<Motion>", self.hoverBuffsPlayer)
            self.playerStatusCanvas.bind("<Leave>", self.unhoverBuffs)
            self.playerBuffHoverLabels.append(Label(self.backgroundCanvas, text = "", anchor = NW, justify = LEFT, fg = "white", bg = self.lightBrown))
            self.playerBuffHoverLabelsPlaces.append(x + statusCanvasX)
            

        self.enemyBuffImages = []
        self.enemyBuffTexts = []
        self.enemyBuffHoverLabels = []
        self.enemyBuffHoverLabelsPlaces = []


        for x in range (245, 20, -40):
            self.enemyBuffImages.append(self.enemyStatusCanvas.create_image(x, 55, image=self.buffImage, anchor = NE))
            self.enemyStatusCanvas.itemconfig(self.enemyBuffImages[len(self.enemyBuffImages)-1], state="hidden")
            self.enemyBuffTexts.append(self.enemyStatusCanvas.create_text(x, 86, anchor = NE, text = "", font = ("Purisa", 8), fill = "white"))
            self.enemyStatusCanvas.bind("<Motion>", self.hoverBuffsEnemy)
            self.enemyStatusCanvas.bind("<Leave>", self.unhoverBuffs)
            self.enemyBuffHoverLabels.append(Label(self.backgroundCanvas, text = "", anchor = NW, justify = LEFT, fg = "white", bg = self.lightBrown))
            self.enemyBuffHoverLabelsPlaces.append(x + self.rootWidth - statusCanvasX - statusCanvasWidth)        
        
        
        self.spellHoverLabels = []
        self.spellHoverLabelsPlaces = []        
        self.spellCanvasButtons = []    
            
        i = 0
        
        for X in range (120, 290, 55):
            self.spellCanvasButtons.append(Button(self.spellCanvas, text = "", font = ("Purisa", 25, "bold"), compound = CENTER,\
            bg = self.lightBrown, bd = 2.5, disabledforeground = "red", activebackground = self.lightBrown))
            self.spellCanvasButtons[i].place(x = X + 40, y = 12, width = 50, height = 50)
            self.spellCanvasButtons[i].bind("<Enter>", self.hoverCanvasSpell)
            self.spellCanvasButtons[i].bind("<Leave>", self.unhoverCanvasSpell)
            self.spellCanvasButtons[i].bind("<Button-1>", self.selectSpell)
    
            self.spellHoverLabels.append(Label(self.backgroundCanvas, text = "", anchor = SW, justify = LEFT, fg = "white", bg = self.lightBrown))
            self.spellHoverLabelsPlaces.append(X + spellCanvasX + 40)
            i+=1
            
            
        self.pulseSound = pygame.mixer.Sound("resources/pulse.wav")
    
        self.menuCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief="ridge", width = self.rootWidth, height = self.rootHeight)
        self.endGameCanvas = Canvas(self.backgroundCanvas, bd=0, highlightthickness=0, relief="ridge", width = self.rootWidth, height = self.rootHeight)
        self.looserImageCanvas = self.endGameCanvas.create_image(0, 0, image=self.looserImage, anchor = NW)
        self.endGameCanvas.pack_forget()
            
        app.setMenu()
    
    #postavljanje prikaza glavnog menija
    def setMenu(self):
        self.menuCanvas.pack()
        self.menuCanvasPhoto = Image.open("resources/mainMenu.png")
        self.menuCanvasPhoto = self.menuCanvasPhoto.resize((self.rootWidth, self.rootHeight))
        self.menuCanvasImage = ImageTk.PhotoImage(self.menuCanvasPhoto)
        self.menuCanvas.create_image(0, 0, image = self.menuCanvasImage, anchor = NW)
        
        self.maxPlayerWidth = 280
        self.maxPlayerHeight = 320
        self.maxPlayerX = 515
        self.maxPlayerY = 10
        
        self.selectedPlayer = 0
        self.numOfPlayers = 2
        
        self.menuPlayerImages = []
        
        self.menuPlayerPhoto1 = Image.open("resources/player1.png")
        self.menuPlayerImages.append(ImageTk.PhotoImage(self.menuPlayerPhoto1))
        
        self.menuPlayerPhoto2 = Image.open("resources/player2.png")
        self.menuPlayerImages.append(ImageTk.PhotoImage(self.menuPlayerPhoto2))
        
        self.playerX = int(self.maxPlayerX + (1-self.menuPlayerImages[self.selectedPlayer].width()/self.maxPlayerWidth)*self.maxPlayerWidth/2)
        self.playerY = int(self.maxPlayerY + (1-self.menuPlayerImages[self.selectedPlayer].height()/self.maxPlayerHeight)*self.maxPlayerHeight/2)

        self.menuCanvasPlayerImage = self.menuCanvas.create_image(self.playerX, self.playerY, image = self.menuPlayerImages[self.selectedPlayer], anchor = NW)
            
        
        self.menuSpellBoxes = []
        x = 50
        for i in range (4):
            self.menuSpellBoxes.append(ImageTk.PhotoImage(Image.open("resources/spellBox.png")))
            self.menuCanvas.create_image(x, 260, image = self.menuSpellBoxes[i], anchor = NW)
            x += 110
            
        
        self.menuScaler = Scale(self.menuCanvas, command = self.setMusicVolume, from_=100, to=0, bd = 1,  bg = self.darkBrown, highlightbackground = self.lightBrown, \
        font = ("Purisa", 10, "bold"), fg = self.lightBrown, sliderlength = 50, troughcolor = self.lightBrown, activebackground = self.darkBrown)
        self.menuScaler.place(x = 20, y = 20, width = 48, height = 150)
        self.menuScaler.set(self.musicVolume)
        
        
        self.menuSpeakerPhoto = Image.open("resources/speaker.jpg")
        self.menuSpeakerImage = ImageTk.PhotoImage(self.menuSpeakerPhoto)
        self.menuCanvas.create_image(20, 180, image = self.menuSpeakerImage, anchor = NW)   
        
        self.selectedMode = 0
        self.menuModeImages = []
        
        self.menuModePhoto1 = Image.open("resources/modepve.png")
        self.menuModePhoto1 = self.menuModePhoto1.resize((180, 60))
        self.menuModeImages.append(ImageTk.PhotoImage(self.menuModePhoto1))
        
        self.menuModePhoto2 = Image.open("resources/modehve.png")
        self.menuModePhoto2 = self.menuModePhoto2.resize((180, 60))
        self.menuModeImages.append(ImageTk.PhotoImage(self.menuModePhoto2))
        
        self.menuModePhoto3 = Image.open("resources/modehvp.png")
        self.menuModePhoto3 = self.menuModePhoto3.resize((180, 60))
        self.menuModeImages.append(ImageTk.PhotoImage(self.menuModePhoto3))
        
        self.menuModePhoto4 = Image.open("resources/modehvh.png")
        self.menuModePhoto4 = self.menuModePhoto4.resize((180, 60))
        self.menuModeImages.append(ImageTk.PhotoImage(self.menuModePhoto4))
        
        self.numOfModes = len(self.menuModeImages)
        
        self.menuModeImage = self.menuCanvas.create_image(185, 20, image = self.menuModeImages[0], anchor = NW)

        self.menuLeftPhoto = Image.open("resources/menuLeft.gif")
        self.menuLeftImage = ImageTk.PhotoImage(self.menuLeftPhoto )
        self.menuLeftButton1 = Button(self.menuCanvas, command = self.menuLeftModeClick, image = self.menuLeftImage, bg = self.lightBrown, bd =  4,\
        highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = self.lightBrown)
        self.menuLeftButton1.place(x = 105, y = 20, width = 60, height = 60)
        
        self.menuRightPhoto = Image.open("resources/menuRight.gif")
        self.menuRightImage = ImageTk.PhotoImage(self.menuRightPhoto )
        self.menuRightButton1 = Button(self.menuCanvas, command = self.menuRightModeClick, image = self.menuRightImage, bg = self.lightBrown, bd =  4,\
        highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = self.lightBrown)
        self.menuRightButton1.place(x = 385, y = 20, width = 60, height = 60)
        
        
        
        self.selectPlayerPhoto = Image.open("resources/playerBox.png")
        self.selectPlayerImage = ImageTk.PhotoImage(self.selectPlayerPhoto )
        self.menuCanvas.create_image(210, 95, image = self.selectPlayerImage, anchor = NW)
        
        self.menuLeftButton2 = Button(self.menuCanvas, command = self.menuLeftPlayerClick, image = self.menuLeftImage, bg = self.lightBrown, bd =  4,\
        highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = self.lightBrown)
        self.menuLeftButton2.place(x = 105, y = 95, width = 60, height = 60)

        self.menuRightButton2 = Button(self.menuCanvas, command = self.menuRightPlayerClick, image = self.menuRightImage, bg = self.lightBrown, bd =  4,\
        highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = self.lightBrown)
        self.menuRightButton2.place(x = 385, y = 95, width = 60, height = 60)
            
        
        self.startGamePhoto = Image.open("resources/startGameBox.png")
        self.startGameImage = ImageTk.PhotoImage(self.startGamePhoto )
        self.startGameButton = Button(self.menuCanvas, command = self.setGame, image = self.startGameImage, bg = self.lightBrown, bd =  4,\
        highlightcolor="brown", highlightbackground="brown", borderwidth=4, activebackground = self.lightBrown)
        self.startGameButton.place(x = 165, y = 170, width = 220, height = 60)
        
        
        self.menuSpellPhotoSize = 60
        self.menuSpellButtonsX = 55
        self.menuSpellImages = []
        
        self.menuSpellImages1 = []
        
        self.menuSpellPhoto10 = Image.open("resources/p1attack.jpg")
        self.menuSpellPhoto10 = self.menuSpellPhoto10.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto10))
        
        self.menuSpellPhoto11 = Image.open("resources/p1heal.jpg")
        self.menuSpellPhoto11 = self.menuSpellPhoto11.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto11))
        
        self.menuSpellPhoto12 = Image.open("resources/p1charge.png")
        self.menuSpellPhoto12 = self.menuSpellPhoto12.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto12))
        
        self.menuSpellPhoto13 = Image.open("resources/p1stun.jpg")
        self.menuSpellPhoto13 = self.menuSpellPhoto13.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages1.append(ImageTk.PhotoImage(self.menuSpellPhoto13))
        
        self.menuSpellImages.append(self.menuSpellImages1)
        
        self.menuSpellImages2 = []
        
        self.menuSpellPhoto20 = Image.open("resources/p2attack.jpg")
        self.menuSpellPhoto20 = self.menuSpellPhoto20.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto20))
        
        self.menuSpellPhoto21 = Image.open("resources/p2flex.jpg")
        self.menuSpellPhoto21 = self.menuSpellPhoto21.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto21))
        
        self.menuSpellPhoto22 = Image.open("resources/p2charge.jpg")
        self.menuSpellPhoto22 = self.menuSpellPhoto22.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto22))
        
        self.menuSpellPhoto23 = Image.open("resources/p2drain.jpg")
        self.menuSpellPhoto23 = self.menuSpellPhoto23.resize((self.menuSpellPhotoSize, self.menuSpellPhotoSize))
        self.menuSpellImages2.append(ImageTk.PhotoImage(self.menuSpellPhoto23))
        
        self.menuSpellImages.append(self.menuSpellImages2)
        
        self.menuSpellButtons = []
        
        
        for k in range (self.numOfPlayers):
            xx = self.menuSpellButtonsX
            tmpmenuSpellButtons = []
            for i in range (4):         
                tmpmenuSpellButtons.append(Button(self.menuCanvas, image = self.menuSpellImages[k][i], bg = "brown", bd =  0,\
                highlightcolor="brown", highlightbackground="brown", borderwidth=0, activebackground = self.lightBrown))
                
                xx += self.menuSpellButtonsX*2
            self.menuSpellButtons.append(tmpmenuSpellButtons)
            
            
        self.playerDescrs = [PlayerStrategy1.descr, PlayerStrategy2.descr]
        self.playerSpellDescrs = [PlayerStrategy1.spellDescrs, PlayerStrategy2.spellDescrs]
        self.menuCanvasDescr = self.menuCanvas.create_text(10, 350,  anchor = NW, text = self.playerDescrs[0], font = ("Purisa", 15))
        
        self.selectPlayer()
        self.mainMenu()
    
    
    #glavna zajednicka podesavanja za sve modove i nivoie i pokretanje borbe 
    def startGame(self):
        self.playerActionIndex = 0
        self.potez = 0
        
        #modovi
        if self.selectedMode == 0:
            self.playerModes = ["player", "enemy"]
            self.modeStrategies = [PlayerModeStrategy(self), EnemyModeStrategy(self)]
        elif self.selectedMode == 1:
            self.playerModes = ["human", "enemy"]
            self.modeStrategies = [HumanModeStrategy(self), EnemyModeStrategy(self)]
        elif self.selectedMode == 2:
            self.playerModes = ["human", "player"]
            self.modeStrategies = [HumanModeStrategy(self), PlayerModeStrategy(self)]
        elif self.selectedMode == 3:
            self.playerModes = ["human", "online"]
            self.modeStrategies = [HumanModeStrategy(self), OnlineModeStrategy(self)]
        
        
        self.playerPlayed = [0, 0]
    
        self.backgroundCanvas.delete("all")
    
        if self.playerModes[1] != "online":
            self.selectEnvironment()
        self.backgroundCanvas.create_image(0, 0, image = self.backgroundImage, anchor = NW)
        
        self.playerEnergyBar["maximum"] = 100
        self.playerHealthBar["maximum"] = 100
        self.enemyHealthBar["maximum"] = 100
        self.enemyEnergyBar["maximum"] = 100
        
        self.criticalImages = []
        
        self.spellImages = []
        
        self.cooldowns = [0, 0, 0, 0]
        self.playerBuffDescrs = []
        self.enemyBuffDescrs = []
        
        self.playerStrategy.setPlayerTexts(self)
        self.enemyStrategy.setPlayerTexts(self)
        
            
        self.dodgeGifs = []
        self.playerSpellGifs = []
        self.enemySpellGifs = []
        
        if self.selectedMode < 2:
            self.players = []
            self.playerStrategy.setPlayer(self)
            self.enemyStrategy.setPlayer(self)
            

        self.playerStrategy.setPlayerSpellImages(self)
        
        
        for i in range (len(self.spellCanvasButtons)):
            self.spellCanvasButtons[i]["image"] = self.spellImages[i]
            if self.playerModes[0]=="human":
                self.spellCanvasButtons[i]["activebackground"] = "yellow"
            self.spellHoverLabels[i]["text"] = self.players[0].spells[i].description()
              
        
        self.playerStrategy.setPlayerGif(self)
        self.enemyStrategy.setPlayerGif(self)
        
        self.playerStrategy.setPlayerDodgeGif(self)
        self.enemyStrategy.setPlayerDodgeGif(self)
        
        self.playerStrategy.setPlayerSpellGifs(self)
        self.enemyStrategy.setPlayerSpellGifs(self)
            
        
        self.game = Igra(self.players[0], self.players[1])
        if self.playerModes[1] == "enemy":
            self.players[1].initFuzzy(self.players[0])
        
        #dodavanje environment buffova igracima
        self.playerStrategy.setEnvironmentBuff(self.environmentTags[self.environment], self.players[0])
        self.enemyStrategy.setEnvironmentBuff(self.environmentTags[self.environment], self.players[1])
        
        
        self.menuCanvas.pack_forget()
        #sve je spremno za pocetak borbe
        self.root.after(3, self.run)
        
        
    def selectEnvironment(self, randEnvironment = -1):
        if randEnvironment == -1:
            while True:
                randEnvironment = random.randint(0, 3)
                if randEnvironment != self.environment:
                    break
                
        self.environment = randEnvironment
        self.backgroundPhoto = Image.open("resources/background" + str(randEnvironment+1)+".jpg")
        self.backgroundPhoto = self.backgroundPhoto.resize((self.rootWidth, self.rootHeight))
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundPhoto)
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resources/background" + str(randEnvironment+1)+".mp3") 
        pygame.mixer.music.set_volume(self.musicVolume/100)
        pygame.mixer.music.play(-1)

    
    #aktivira se na klik dugmeta start game i sluzi da se zapocne igra, ali se prvo moraju postaviti svi uslovi za igru
    def setGame(self):
        if self.selectedMode < 2:
            self.gameStrategy = OfflineGameStrategyE(self)
        elif self.selectedMode == 2:
            self.gameStrategy = OfflineGameStrategyP(self)
        elif self.selectedMode == 3:
            self.gameStrategy = self.onlineGameStrategy
        self.gameStrategy.setGame()    
    
    def setMusicVolume(self, volume):
        self.musicVolume = int(volume)
        pygame.mixer.music.set_volume(self.musicVolume/100)
        self.pulseSound.set_volume(self.musicVolume/100)
        self.endGameSound.set_volume(self.musicVolume/100)
    
    def menuLeftPlayerClick(self):
        for i in range (4):         
            self.menuSpellButtons[self.selectedPlayer][i].place_forget()
            
        self.selectedPlayer -= 1
        if (self.selectedPlayer == -1):
            self.selectedPlayer = self.numOfPlayers - 1
            
        self.selectPlayer()
    
    def menuRightPlayerClick(self):
        for i in range (4):         
            self.menuSpellButtons[self.selectedPlayer][i].place_forget()
            
        self.selectedPlayer += 1
        if (self.selectedPlayer == self.numOfPlayers):
            self.selectedPlayer = 0
        
        self.selectPlayer()

    def selectPlayer(self):
        self.playerX = int(self.maxPlayerX + (1-self.menuPlayerImages[self.selectedPlayer].width()/self.maxPlayerWidth)*self.maxPlayerWidth/2)
        self.playerY = int(self.maxPlayerY + (1-self.menuPlayerImages[self.selectedPlayer].height()/self.maxPlayerHeight)*self.maxPlayerHeight/2)

        self.menuCanvas.itemconfig(self.menuCanvasPlayerImage, image = self.menuPlayerImages[self.selectedPlayer])
        xx = self.menuSpellButtonsX
        for i in range (4):         
            self.menuSpellButtons[self.selectedPlayer][i].place(x = xx, y = 265, width = self.menuSpellPhotoSize, height = self.menuSpellPhotoSize)
            self.menuSpellButtons[self.selectedPlayer][i]["command"]=0
            self.menuSpellButtons[self.selectedPlayer][i]["relief"]="sunken"
            self.menuSpellButtons[self.selectedPlayer][i].bind("<Enter>", self.hoverMenuSpell)
            self.menuSpellButtons[self.selectedPlayer][i].bind("<Leave>", self.unhoverMenuSpell)
            xx += self.menuSpellButtonsX*2
        
        self.menuCanvas.itemconfig(self.menuCanvasDescr, text = self.playerDescrs[self.selectedPlayer])
    
    
    def menuLeftModeClick(self):
        self.selectedMode -= 1
        if self.selectedMode == -1:
            self.selectedMode = self.numOfModes - 1
        
        self.selectMode()
    
    def menuRightModeClick(self):
        self.selectedMode += 1
        if self.selectedMode == self.numOfModes:
            self.selectedMode = 0
        
        self.selectMode()
        
    def selectMode(self):
        self.menuCanvas.itemconfig(self.menuModeImage, image = self.menuModeImages[self.selectedMode])
    
    
    def hoverMenuSpell(self, e):
        for i in range (4):
            if e.widget == self.menuSpellButtons[self.selectedPlayer][i]:
                self.menuCanvas.itemconfig(self.menuCanvasDescr, text = self.playerSpellDescrs[self.selectedPlayer][i])
                break
    
    def unhoverMenuSpell(self, e):
        self.menuCanvas.itemconfig(self.menuCanvasDescr, text = self.playerDescrs[self.selectedPlayer])
            
    def hoverCanvasSpell(self, e):
        if self.playerPlayed[self.side] == 0 and self.playerModes[self.side] == "human" and e.widget["state"]!="disabled": 
            e.widget["bg"] = "yellow"
        for i in range (len(self.spellHoverLabels)):
            if e.widget == self.spellCanvasButtons[i]:
                self.spellHoverLabels[i].place(x = self.spellHoverLabelsPlaces[i], y = 360, anchor = SW)
                break
            
    def unhoverCanvasSpell(self,e):
        if self.playerPlayed[self.side] == 0 and self.playerModes[self.side] == "human":
            e.widget["bg"] = self.lightBrown
        for i in range (len(self.spellHoverLabels)):
            if e.widget == self.spellCanvasButtons[i]:
                self.spellHoverLabels[i].place_forget()
                break
    
    def hoverBuffsPlayer(self, e):
        for i in range (len(self.playerBuffImages)):
            x1, y1 = e.widget.coords(self.playerBuffImages[i])
            x2, y2 = x1 + 30, y1 + 30
            if e.x >= x1 and e.x <x2 and e.y >= y1 and e.y < y2 and i<len(self.playerBuffDescrs):
                self.playerBuffHoverLabels[i].place(x = self.playerBuffHoverLabelsPlaces[i], y = 100, anchor = NW)
                self.playerBuffHoverLabels[i]["text"] = self.playerBuffDescrs[i]
            else: self.playerBuffHoverLabels[i].place_forget()
    
    def hoverBuffsEnemy(self, e):
        for i in range (len(self.enemyBuffImages)):
            x2, y1 = e.widget.coords(self.enemyBuffImages[i])
            x1, y2 = x2 - 30, y1 + 30
            if e.x >= x1 and e.x <x2 and e.y >= y1 and e.y < y2 and i<len(self.enemyBuffDescrs):
                self.enemyBuffHoverLabels[i].place(x = self.enemyBuffHoverLabelsPlaces[i], y = 100, anchor = NE)
                self.enemyBuffHoverLabels[i]["text"] = self.enemyBuffDescrs[i]
            else: self.enemyBuffHoverLabels[i].place_forget()
                
    def unhoverBuffs(self, e):
        for i in range (len(self.playerBuffHoverLabels)):
            self.playerBuffHoverLabels[i].place_forget()
        for i in range (len(self.enemyBuffHoverLabels)):
            self.enemyBuffHoverLabels[i].place_forget()
    
    def checkHoverBuffs(self):
        x = self.root.winfo_pointerx()-self.playerStatusCanvas.winfo_rootx()
        y = self.root.winfo_pointery()-self.playerStatusCanvas.winfo_rooty()
    
        for i in range (len(self.playerBuffHoverLabels)):
            x1, y1 = self.playerStatusCanvas.coords(self.playerBuffImages[i])
            x2, y2 = x1 + 30, y1 + 30
            if x >= x1 and x <x2 and y >= y1 and y < y2 and i<len(self.playerBuffDescrs):
                self.playerBuffHoverLabels[i].place(x = self.playerBuffHoverLabelsPlaces[i], y = 100, anchor = NW)
                self.playerBuffHoverLabels[i]["text"] = self.playerBuffDescrs[i]
            else: self.playerBuffHoverLabels[i].place_forget()
            
        x = self.root.winfo_pointerx()-self.enemyStatusCanvas.winfo_rootx()
        y = self.root.winfo_pointery()-self.enemyStatusCanvas.winfo_rooty()
        
        for i in range (len(self.enemyBuffImages)):
            x2, y1 = self.enemyStatusCanvas.coords(self.enemyBuffImages[i])
            x1, y2 = x2 - 30, y1 + 30
            if x >= x1 and x <x2 and y >= y1 and y < y2 and i<len(self.enemyBuffDescrs):
                self.enemyBuffHoverLabels[i].place(x = self.enemyBuffHoverLabelsPlaces[i], y = 100, anchor = NE)
                self.enemyBuffHoverLabels[i]["text"] = self.enemyBuffDescrs[i]
            else: self.enemyBuffHoverLabels[i].place_forget()
    
    def selectSpell(self, e):
        if e.widget["state"]!="disabled" and self.side == 0 and self.playerPlayed[0] == 0 and self.playerModes[0] == "human" and self.players[0].stunned == False:
            self.playerPlayed[0] = 1
            self.playerActionIndex = self.spellCanvasButtons.index(e.widget)
            self.root.after_cancel(self.clockAfter)
            self.run()
            
    def checkTimeToPlay(self, potez):
        print("CHECKING "+str(potez))
        if self.potez == potez and self.side == 0 and self.playerPlayed[0] == 0:
            self.playerPlayed[0] = 1
            print("SKIPPING MOVE")
            self.spellCanvas.itemconfig(self.playerClockText, text = "0")
            self.playerActionIndex = -1
            self.run()
    
    def updateClok(self, potez, number):
        if self.potez == potez and self.side == 0 and self.playerPlayed[0] == 0:
            self.spellCanvas.itemconfig(self.playerClockText, text = str(number))
    
    
def doExit():
    os._exit(0)
    
    
#main
root = Tk()
root.protocol("WM_DELETE_WINDOW", doExit)

pygame.init()

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-57b6337c-3f6d-4727-b5ec-3d9ccb6d737e"
pnconfig.subscribe_key = "sub-c-26f8560a-4e3c-11ea-94fd-ea35a5fcc55f"
pnconfig.ssl = True
pubnub = PubNub(pnconfig)

app = Application(root, pubnub)


app.startApp()

root.mainloop()