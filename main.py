import json
import random
import time

class card:
    def __init__(self, name, time, text):
        self.type = "Technique"
        self.name = name
        self.time = time
        self.text = text
    def getInformationString(self):
        infoString = self.name + " : " + str(self.time) + "\n" + self.text
        return infoString

class modifierCard(card):
    def __init__(self, name, time, mechanics):
        self.name = name
        self.time = time
        self.type = "modifier"
        self.mechanicNames = ["Move", "Accelerate", "Overshoot", "Ground", "Unground", "Momentum"]
        self.mechanicsIncludeValue = [True, True, True, False, False, True]
        self.mechanicsValues = []
        counter = 0
        for id in mechanics:
            self.mechanicsValues.append(int(mechanics[counter]))
            counter += 1
        # index 0 is Move
        # index 1 is Accelerate
        # index 2 is Overshoot
        # index 3 is Ground
        # index 4 is Unground
        # index 5 is Momentum
    def getInformationString(self):
        infoString = self.name + " : " + str(self.time) + "\n"
        counter = 0
        index = 0
        for id in self.mechanicsValues:
            if id > 0:
                counter += 1
                value = ""
                if (self.mechanicsIncludeValue[index]):
                    value = " " + str(id)
                infoString += str(self.mechanicsValues[index]) + value + ", "
            index += 1
        if counter > 0:
            infoString = infoString[:-2]
        return infoString

class structureCard(card):
    def __init__(self, name, time, strenght, speed, grounded):
        self.name = name
        self.time = time
        self.type = "structure"
        self.strenght = strenght
        self.speed = speed
        self.startGrounded = grounded
    def getInformationString(self):
        infoString = self.name + " : " + str(self.time) + "\n" + str(self.strenght) + "/" + str(self.speed)
        return infoString
class comboCard(card):
    def __init__(self, name, time, text):
        self.name = name
        self.type = "combo"
        self.time = time
        self.text = text
    def getInformationString(self):
        infoString = self.name + " : " + str(self.time) + "\n" + self.text
        return infoString
class dualCard:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2
    def getInformationString(self):
        return "========\n" + self.card1.getInformationString() + "\n--------\n" + self.card2.getInformationString() + "\n========\n"

class player:
    def __init__(self, fileName):
        playerDeckData = open(fileName, "r")
        playerDeckList = []
        self.hand = [[],[]]
        self.fullComboDeck = []
        self.fullDualDeck = []
        for line in playerDeckData:
            playerDeckList.append(line)
        playerComboIndexes = json.loads(playerDeckList[0])
        for id in playerComboIndexes:
            self.fullComboDeck.append(deckData.comboDeck[id])
        playerDualIndexes = json.loads(playerDeckList[1])
        for id in playerDualIndexes:
            self.fullDualDeck.append(deckData.dualDeck[id])
        self.comboDeck = self.fullComboDeck
        self.dualDeck = self.fullDualDeck
    def drawCombo(self, amount):
        for id in range(amount):
            # random.seed(timime())
            selectedCard = random.choice(self.comboDeck)
            self.comboDeck.remove(selectedCard)
            if (len(self.comboDeck) == 0):
                self.comboDeck = self.fullComboDeck
                print("Refueled Combo Deck")
            print(selectedCard.getInformationString())
    def drawDual(self, amount):
        for id in range(amount):
            # random.seed(time.time())
            selectedCard = random.choice(self.dualDeck)
            self.dualDeck.remove(selectedCard)
            if (len(self.dualDeck) == 0):
                self.dualDeck = self.fullDualDeck
                print("Refueled Dual Deck")
            self.hand[0].append(selectedCard.card1)
            self.hand[1].append(selectedCard.card2)
            print(selectedCard.getInformationString())
    def displayHand(self):
        # THIS SYSTEM WILL STOP WORKING WHEN COMBOS ARE INTRODUCED
        handNotation = ["","",""]
        for id in range(len(self.hand[0])):
            handNotation[0] += self.hand[0][id].name[0] + "|"
            handNotation[1] += self.hand[1][id].name[0] + "|"
            handNotation[2] += str(id+1)
            if id < 9:
                handNotation[2] += " "
        print(handNotation[2])
        print(handNotation[0])
        print(handNotation[1])


class deckDataHolder:
    def __init__(self):
        try:
            deck = open("carddata.txt", "r")
        except:
            print("Couldnt find carddata.txt")
            return
        deckFileList = []
        for line in deck:
            deckFileList.append(line)
        self.amountOfCards = json.loads(deckFileList[0])[0]
        self.amountOfDuals = json.loads(deckFileList[0])[1]
        self.cardList = []
        self.dualDeck = []
        self.comboDeck = []
        for id in range(self.amountOfCards):
            c_name = deckFileList[id * 4 + 2][2:]
            c_name = c_name[:-1]
            c_time = int(deckFileList[id * 4 + 3])
            if deckFileList[id * 4 + 2][0] == "m":
                c_mechanicsSTR = deckFileList[id * 4 + 4]
                c_mechanicsSTR = c_mechanicsSTR[:-1]
                self.cardList.append(modifierCard(c_name, c_time, json.loads(c_mechanicsSTR)))
            elif deckFileList[id * 4 + 2][0] == "s":
                c_strenght = json.loads(deckFileList[id * 4 + 4])[0]
                c_speed = json.loads(deckFileList[id * 4 + 4])[1]
                c_grounded = json.loads(deckFileList[id * 4 + 4])[2]
                self.cardList.append(structureCard(c_name, c_time, c_strenght, c_speed, c_grounded))
            elif deckFileList[id * 4 + 2][0] == "c":
                c_text = deckFileList[id * 4 + 4]
                self.cardList.append(comboCard(c_name, c_time, c_text))
                self.comboDeck.append(self.cardList[id])
            elif deckFileList[id * 4 + 2][0] == "a":
                c_text = deckFileList[id * 4 + 4]
                self.cardList.append(card(c_name, c_time, c_text))
        for id in range(self.amountOfDuals):
            c_dual = json.loads(deckFileList[(self.amountOfCards) * 4 + 2 + id])
            self.dualDeck.append(dualCard(self.cardList[c_dual[0]], self.cardList[c_dual[1]]))




class gameObject:
    def __init__(self, objectType, direction):
        self.type = " "
        self.modifiers = [[],[]]
        self.direction = None
        self.launchedStructure = None
        self.timer = 0
        self.explode = False
        self.summoning = True
        self.summonType = objectType
        self.grounded = False
        self.strength = 0
        self.summonStrength = 0
        self.launchedStrength = 0
        self.notation = self.type[0]
    def timeAdvance(self, row, lane):
        if launchedStructure != None:
            survivor = game.handleCollision(self.launchedStrength, self.strength)
            if survivor == "incoming":
                self.type = self.launchedStructure
                self.launchedStructure = None
            elif survivor == "defender":
                self.launchedStructure = None
            else:
                self.launchedStructure = None
                self.type = None
                
        if self.timer == game.timer[0]:
            if self.summoning:
                if self.objectType == None:
                    self.summon()
                elif selectedSpace.grounded == False:
                    survivor = game.handleCollision(self.summonStrength, self.strength)
                    if survivor == "incoming":
                        self.type = self.launchedStructure
                        self.launchedStructure = None
                    elif survivor == "defender":
                        self.launchedStructure = None
                    else:
                        self.launchedStructure = None
                        self.type = None
                else:
                    self.launchedStructure = self.type
                    self.type = self.summonType
            if len(modifier[0]) > 0:
                game.handleAttribute(row, lane)



class gameHandler:
    def __init__(self):
        self.gameBoard = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.timer = [0,0,0]
    def applyAttribute(self, player, row, lane, attribute, strength, cardType, timeBeforeActivation = 0):
        selectedSpace = self.gameBoard[row][lane]
        if selectedSpace == None:
            print("There is nothing there.")
            return False
        self.timer[player] += timeBeforeActivation
        selectedSpace.direction = player * -1 + 3
        if selectedSpace.timer < self.timer[0]:
            selectedSpace.timer = self.timer[0]
        selectedSpace.timer += timeBeforeActivation
        
        if attribute == "Momentum":
            for modId in selectedSpace.modifiers[0]:
                if selectedSpace.modifiers[0][modId] == "Move" and selectedSpace.modifiers[1][modId] > 1:
                    attribute = "Move"
            if attribute != "Move":
                return True
        if cardType == "modifier":
            for modId in selectedSpace.modifiers[0]:
                if selectedSpace.modifiers[0][modId] == "Accelerate":
                    strength += selectedSpace.modifiers[1][modId]
        
        for modId in selectedSpace.modifiers[0]:
            if selectedSpace.modifiers[0][modId] == attribute:
                selectedSpace.modifiers[1][modId] += strength

                self.gameBoard[row][lane] = selectedSpace
                return True
        selectedSpace.modifiers[0].append(attribute)
        selectedSpace.modifiers[1].append(strength)

        self.gameBoard[row][lane] = selectedSpace

    def placeStructure(self, player, row, lane, card, timeBeforeActivation = 0):
        selectedSpace = self.gameBoard[row][lane]

        

        if selectedSpace == 0:
            selectedSpace = gameObject(card.name, player * -1 + 3)
            self.gameBoard[row][lane] = selectedSpace
            return False
        else:
            selectedSpace.summonType = card.name
            selectedSpace.summoning = True

        self.timer[player] += timeBeforeActivation
        selectedSpace.direction = player * -1 + 3
        if selectedSpace.timer < self.timer[0]:
            selectedSpace.timer = self.timer[0]
        selectedSpace.timer += timeBeforeActivation

        self.gameBoard[row][lane] = selectedSpace
        return False

    
    def timeAdvance(self):
        for row in range(len(game.gameBoard)):
            for lane in range(len(game.gameBoard)):
                if game.gameBoard[row][lane] != 0:
                    game.gameBoard[row][lane].timeAdvance(row, lane)

        
           
    def playCard(self, player, card, lane):
        row = 1
        if player == 1:
            row = 0
        else:
            row = 2
        if card.type == "modifier" or card.type == "combo":
            for i in card.mechanicsIncludeValue:
                if card.mechanicsIncludeValue[i]:
                    return self.applyAttribute(player, row, lane, card.mechanicNames[i], card.mechanicsValues[i], card.time)
        elif card.type == "structure":
            return self.placeStructure(player, row, lane, card, card.time)
        print(game.gameBoard[row][lane])
        
        
                

        
        




deckData = deckDataHolder()
# for id in deckData.dualDeck:
    # print(id.getInformationString())
# for id in deckData.comboDeck:
    # print(id.getInformationString())

player1 = player("player1deck.txt")
player2 = player("player2deck.txt")

random.seed(time.time())
game = gameHandler()
cardSelected = 0
cardSideSelected = 0
laneSelected = 0
playerSelected = 0
hands = [[],[]]
boardString = ""
timeFlag = True
stackFlag = False

while True:
    # Possibly add deck choser at the start here

    # Draw 7:
    player1.drawDual(7)
    player2.drawDual(7)

    
    
    # If hand > 7, choose X cards to remove
    while len(player1.hand[0]) > 7:
        player1.displayHand()
        
        removedCard = int(input("PLAYER 1: Choose id of card to remove")) - 1
        player1.hand[0].remove(player1.hand[0][removedCard])
        player1.hand[1].remove(player1.hand[1][removedCard])

    while len(player2.hand[0]) > 7:
        player2.displayHand()
        
        removedCard = int(input("PLAYER 2: Choose id of card to remove")) - 1
        player2.hand[0].remove(player2.hand[0][removedCard])
        player2.hand[1].remove(player2.hand[1][removedCard])
    # For future BoredYoshi: Add game logistics here
    timeFlag = True

    while timeFlag:
        hands[0] = player1.hand
        hands[1] = player2.hand
        timeFlag = True

        #print(hands[0][0][0])
        #print(hands[0][1][0])
    
        print("Player 1:")
        player1.displayHand()
        
        print("")
        for i in range(len(game.gameBoard)):
            for j in range(len(game.gameBoard[i])):
                try:
                    if game.gameBoard[i][j] == 0:
                        boardString += "- "
                except:
                    boardString += game.gameBoard[i][j].notation + " "
            if i == 1:
                boardString += "    Time: " + str(game.timer[0])
            print(boardString)
            boardString = ""
        print("")
                    
        print("Player 2:")
        player2.displayHand()
    
        stackFlag = True
        playerSelected = int(input("Which player will play? (3 to skip 5 time, 4 to skip to next important event)"))
        
        while stackFlag:
            if playerSelected == 3:
                stackFlag = False
                game.timer[0] += 5
                game.timeAdvance()
                if game.timer[0] > 100:
                    game.timer[0] -= 100
                    timeFlag = False
            for i in range(2):
                if game.timer[i+1] < game.timer[0]:
                    game.timer[i+1] = game.timer[0]
            if playerSelected == 4:
                stackFlag = False
                if game.timer[1] > game.timer[2]:
                    game.timer[0] = game.timer[2]
                else:
                    game.timer[0] = game.timer[1]
                game.timeAdvance()
                if game.timer[0] > 100:
                    game.timer[0] -= 100
                    timeFlag = False

            if playerSelected < 3:
                cardSelected = int(input("Choose id of card to play"))
                cardSideSelected = int(input("Choose which side of card to play (top/bottom) (1/2)"))
                laneSelected = int(input("Choose lane to play in"))
    
                print(hands[playerSelected - 1][cardSideSelected - 1][cardSelected - 1].type)
                stackFlag = game.playCard(playerSelected,hands[playerSelected - 1][cardSideSelected - 1][cardSelected - 1],laneSelected)
            if stackFlag:
                if input("Continue playing cards? (Y/N)") == "N":
                    stackFlag = False
        
        
        