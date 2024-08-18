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
                infoString += self.mechanicNames[index] + value + ", "
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
        infoString = "========\n" + self.name + " : " + str(self.time) + "\n" + self.text  + "\n========\n"
        return infoString
class dualCard:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2
    def getInformationString(self):
        return "========\n" + self.card1.getInformationString() + "\n--------\n" + self.card2.getInformationString() + "\n========\n"

# Debugging tools

def displayDeck(deck):
    coolstring = ""
    for id in deck:
        coolstring += id.name + ", "
    if len(coolstring) > 2:
        coolstring = coolstring[:-2]
    else:
        coolstring = "empty deck"
    print(coolstring)

# General utility functions

def getListValue(list):
    # Setting one list to another turns it into a reference and can cause issues. Use this instead to set the value of a list.
    newList = []
    for id in list:
        newList.append(id)
    return newList
def selectCardFromHands(playerAtHand):
    temp = 0
    final = -1
    while final != temp:
        print(playerAtHand.getDualHandDisplay())
        print(playerAtHand.getComboHandDisplay())
        try:
            temp = int(input("What index? > "))
            if (temp > (len(playerAtHand.hand[0]) + len(playerAtHand.hand[1])) or temp < 1):
                # Go to Except
                eval (5/0)
            final = temp
        except:
            print("invalid index")
    return final


class player:
    def __init__(self, fileName):
        playerDeckData = open(fileName, "r")
        playerDeckList = []
        self.hand = [[],[]] # First hand is dual, second is combo
        self.comboDeck = []
        self.dualDeck = []
        self.fullComboDeck = []
        self.fullDualDeck = []
        for line in playerDeckData:
            playerDeckList.append(line)
        playerComboIndexes = json.loads(playerDeckList[0])
        for id in playerComboIndexes:
            self.fullComboDeck.append(deckData.comboLibrary[id])
        playerDualIndexes = json.loads(playerDeckList[1])
        for id in playerDualIndexes:
            self.fullDualDeck.append(deckData.dualLibrary[id])
        self.comboDeck = getListValue(self.fullComboDeck)
        u_seed()
        random.shuffle(self.comboDeck)
        self.dualDeck = getListValue(self.fullDualDeck)
        u_seed()
        random.shuffle(self.dualDeck)
    def drawCombo(self, amount):
        for id in range(amount):
            if (len(self.comboDeck) == 0):
                self.comboDeck = getListValue(self.fullComboDeck)
                print("Refueled Combo Deck")
            selectedCard = self.comboDeck[0]
            self.comboDeck.remove(selectedCard)
            self.hand[1].append(selectedCard)
    def drawDual(self, amount):
        for id in range(amount):
            if (len(self.dualDeck) == 0):
                self.dualDeck = getListValue(self.fullDualDeck)
                print("Refueled Dual Deck")
            selectedCard = self.dualDeck[0]
            self.dualDeck.remove(selectedCard)
            self.hand[0].append(selectedCard)
        while len(manager.player1.hand[0]) > 7:
            print(manager.player1.getDualHandDisplay())
            removedCard = int(input("Choose index of card to remove (" + str(len(manager.player1.hand[0]) - 7) +" left) > ")) - 1
            manager.player1.hand[0].remove(manager.player1.hand[0][removedCard])
    def getDualHandDisplay(self):
        infoString = "Dual hand :\n"
        counter = 0
        for id in self.hand[0]:
            counter += 1
            infoString += str(counter) + " : " + id.card1.name + " / " + id.card2.name + "\n"
        return infoString
    def getComboHandDisplay(self):
        infoString = "Combo Hand :\n"
        counter = len(self.hand[0])
        for id in self.hand[1]:
            counter += 1
            infoString += str(counter) + " : " + id.name + "\n"
        return infoString



class gameManager:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.time = 100
        self.listOfCommands = {
            "help" : self.helpCommand,
            "info" : self.infoCommand,
            "play" : self.playCommand,
            "end" : self.endCommand
        }
    def helpCommand(self, player):
        print("Here's a list of available commands:")
        print("help : Gives a list of commands and what they do")
        print("info : Gives all the information of a card in your hand")
        print("play : Play a card in your hand")
        print("end : Ends turn")
        return False
    def infoCommand(self, player):
        index = selectCardFromHands(player)
        if (index > len(player.hand[0])):
            index -= len(player.hand[0])
            print(player.hand[1][index - 1].getInformationString())
        else:
            print(player.hand[0][index - 1].getInformationString())
        return False
    def playCommand(self, player):
        index = selectCardFromHands(player)
        if (index > len(player.hand[0])):
            index -= len(player.hand[0])
            player.hand[1].remove(player.hand[1][index - 1])
        else:
            player.hand[1].remove(player.hand[0][index] - 1)
        return False
    def endCommand(self, player):
        return True


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
        self.dualLibrary = []
        self.comboLibrary = []
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
                self.comboLibrary.append(self.cardList[id])
            elif deckFileList[id * 4 + 2][0] == "a":
                c_text = deckFileList[id * 4 + 4]
                c_text = c_text[:-1]
                self.cardList.append(card(c_name, c_time, c_text))
        for id in range(self.amountOfDuals):
            c_dual = json.loads(deckFileList[(self.amountOfCards) * 4 + 2 + id])
            self.dualLibrary.append(dualCard(self.cardList[c_dual[0]], self.cardList[c_dual[1]]))


def u_seed():
    random.seed(time.time() * random.random())



deckData = deckDataHolder()


#manager = gameManager(player(input("Player 1 deck data file name > ")), player(input("Player 2 deck data file name > ")))
manager = gameManager(player("player1deck.txt"), player("player1deck.txt"))
random.seed(time.time())

while True:

    # Possibly add deck choser at the start here

    # Draw 7:
    manager.player1.drawDual(7)
    manager.player1.drawCombo(4)
    print("Player 1:")
    print(manager.player1.getDualHandDisplay())
    print(manager.player1.getComboHandDisplay())
    endTurn = False
    while endTurn:
        ui = input("Input command > ").lower()
        if (ui in manager.listOfCommands):
            endTurn = manager.listOfCommands[ui](manager.player1)
        else:
            print("No function named as such. Use help for list of functions")


    manager.player2.drawDual(7)
    manager.player2.drawCombo(4)
    print("Player 2:")
    print(manager.player2.getDualHandDisplay())
    print(manager.player2.getComboHandDisplay())
    endTurn = False
    while not endTurn:
        ui = input("Input command > ").lower()
        if (ui in manager.listOfCommands):
            endTurn =  manager.listOfCommands[ui](manager.player2)
        else:
            print("No function named as such. Use help for list of functions")

    # End Turn option
    int(input("end process?"))
