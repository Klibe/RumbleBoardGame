import json
import random
import time

class card:
    def __init__(self, name, time, text):
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
                infoString += str(self.mechanicsValues[index]) + str(value) + ", "
            index += 1
        if counter > 0:
            infoString = infoString[:-2]
        return infoString

class structureCard(card):
    def __init__(self, name, time, strenght, speed, grounded):
        self.name = name
        self.time = time
        self.strenght = strenght
        self.speed = speed
        self.startGrounded = grounded
    def getInformationString(self):
        infoString = self.name + " : " + str(self.time) + "\n" + str(self.strenght) + "/" + str(self.speed)
        return infoString
class comboCard(card):
    def __init__(self, name, time, text):
        self.name = name
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
        random.seed(time.time() * random.random())
        random.shuffle(self.comboDeck)
        random.seed(time.time() * random.random())
        random.shuffle(self.dualDeck)
    def drawCombo(self, amount):
        for id in range(amount):
            if (len(self.comboDeck) == 0):
                self.comboDeck = self.fullComboDeck
                print("Refueled Combo Deck")
            selectedCard = self.comboDeck[0]
            self.comboDeck.remove(selectedCard)
            print(selectedCard.getInformationString())
    def drawDual(self, amount):
        for id in range(amount):
            if (len(self.dualDeck) == 0):
                self.dualDeck = self.fullDualDeck
                print("Refueled Dual Deck")
            selectedCard = self.dualDeck[0]
            self.dualDeck.remove(selectedCard)
            print(selectedCard.getInformationString())


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






deckData = deckDataHolder()
for id in deckData.dualDeck:
    print(id.getInformationString())
for id in deckData.comboDeck:
    print(id.getInformationString())

player1 = player(input("Player one deck file name > "))
player2 = player(input("Player two deck file name > "))

while True:
    playerID = int(input("Which player draws? > "))
    deckType = input("Which deck (c/d)? > ")
    amountdrawn = int(input("How many cards to draw? > "))
    if (playerID == 1):
        if (deckType == "c"):
            player1.drawCombo(amountdrawn)
        else:
            player1.drawDual(amountdrawn)
    else:
        if (deckType == "c"):
            player2.drawCombo(amountdrawn)
        else:
            player2.drawDual(amountdrawn)
