from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    
    dictionary = open(dictionaryloc, "r").readlines()
    for i in range(len(dictionary)):
        dictionary[i] = dictionary[i].strip()
    return dictionary

      
    
def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    turntext = open(turntextloc, "r").readlines()
    for i in range(len(turntext)):
        turntext[i] = turntext[i].strip()
    return turntext

        
def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    finalroundtext = open(finalRoundTextLoc, "r").readlines()
    for i in range(len(finalroundtext)):
        finalroundtext[i] = finalroundtext[i].strip()
    return finalroundtext

def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location
    # read round status from file and store in roundstatus variable with string.format
    roundstatus = open(roundstatusloc, "r").readlines()
    for i in range(len(roundstatus)):
        roundstatus[i] = roundstatus[i].strip()
    return roundstatus
    

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location 
    wheellist = open(wheeltextloc, "r").readlines()
    for i in range(len(wheellist)):
        wheellist[i] = wheellist[i].strip()
    return wheellist
    
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    # store in players dictionary
    for i in range(len(players)):
        players[i]["name"] = input("Enter player name: ")
    return players


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary

    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    #choose random word from dictionary
    #make a list of the word with underscores instead of letters.
    roundWord = random.choice(dictionary)
    roundUnderscoreWord = list(roundWord)
    for i in range(len(roundUnderscoreWord)):
        roundUnderscoreWord[i] = "_"

    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    # Return the starting player number (random)
    # Use getWord function to retrieve the word and the underscore word (blankWord)

    for i in range(len(players)):
        players[i]["roundtotal"] = 0
    
    initPlayer = random.randint(0,len(players)-1)
    roundWord, blankWord = getWord()


    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global wheelChoice

    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right. 

    wheelChoice = random.choice(wheellist)
    print("{} spins the wheel and gets a {}".format(players[playerNum]["name"], wheelChoice))
    if wheelChoice == "bankrupt":
        players[playerNum]["roundtotal"] = 0
        print("{} is bankrupt and loses this round".format(players[playerNum]["name"]))
        stillinTurn = False
    elif wheelChoice == "loose":
        print("{} loses this round".format(players[playerNum]["name"]))
        stillinTurn = False
    else:
        # players[playerNum]["roundtotal"] += int(wheelChoice)
        print("{} has {} in the bank".format(players[playerNum]["name"], players[playerNum]["roundtotal"]))
        print(*blankWord)
        goodGuess, count = guessletter(input("Guess a letter: "), playerNum)
        if goodGuess:
            print("{} has found {} letter(s) in the word".format(players[playerNum]["name"], count))
            players[playerNum]["roundtotal"] += count * int(wheelChoice)
            wofTurn(playerNum)
        else: 
            stillinTurn = False
        
    return stillinTurn


def guessletter(letter, playerNum, handleVowel=False): 
    global players
    global blankWord
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    # if not, return goodGuess = false and count = 0

    goodGuess = False
    count = 0
    if letter in vowels and not handleVowel:
        print("{} is a vowel {} loses this round".format(letter, players[playerNum]["name"]))
        return goodGuess, count
        
    if letter in roundWord:
        for i in range(len(roundWord)):
            if roundWord[i] == letter:
                blankWord[i] = letter
                count += 1
                goodGuess = True
        print(*blankWord)
    else:
        print("{} is not in the word".format(letter))
        goodGuess = False
        count = 0
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True

    if players[playerNum]["roundtotal"] >= 250:
        letter = input("Choose a vowel: ")
        players[playerNum]["roundtotal"] -= 250
        if letter in vowels:
            goodGuess, count = guessletter(letter, playerNum, True)
            if goodGuess:
                players[playerNum]["roundtotal"] += count * int(wheelChoice)
                wofRound()
            else:
                print("{} is not in the word".format(letter))
                return False
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  

    wordguess = input("Guess the word: ")
    if wordguess == roundWord:
        for i in range(len(roundWord)):
            blankWord[i] = roundWord[i]
        
        return False
    else:
        print("{} is not the word".format(wordguess))
        return True
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 

    print("{}'s turn".format(players[playerNum]["name"]))
    print("{} has {} in the bank".format(players[playerNum]["name"], players[playerNum]["roundtotal"]))
    print("{}".format(*turntext))
    print(*blankWord)

    choice = input("Would you like to (s)pin the wheel, (b)uy a vowel, or (g)uess the word?: ")
    
    while choice.upper() != "S" and choice.upper() != "B" and choice.upper() != "G":
        choice = input("Invalid choice.\nPlease choose (s)pin the wheel, (b)uy a vowel, or (g)uess the word: ")
    
    stillinTurn = True
    while stillinTurn:
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option") 
            stillinTurn = False
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
    # print("in round")
    playerNum = initPlayer
    while roundstatus:
        # print("in while")
        while playerNum < len(players):
            stillinTurn = wofTurn(playerNum)
            if not stillinTurn:
                playerNum += 1
        if playerNum == len(players):
                playerNum = 0
            
        # if not stillinTurn:
        #     break
        # initPlayer = playerNum
    
    # print("out of wild")
    
    print("{}".format(roundstatus))
    print("{}".format(*blankWord))
    print('kk')


def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won

    # for player in players:
    #     if player["gametotal"] > amount:
    #         amount = player["gametotal"]
    #         winplayer = player["name"]
    #         print("{} is playing".format(winplayer))
    #         print("{}".format(finalroundtext))
    #     wofFreeLetters = ['R','S','T','L','N','E']
    #     for letter in wofFreeLetters:
    #         guessletter(letter, players.index(player))
    #     print("{}".format(blankWord))
    #     consonants = input("Choose 3 consonants: ")
    #     vowels = input("Choose 1 vowel: ")
    #     guessletter(consonants, players.index(player))
    #     guessletter(vowels, players.index(player))
    #     print("{}".format(blankWord))
    #     wordguess = input("Guess the word: ")
    #     if wordguess == roundWord:
    #         players[players.index(player)]["gametotal"] += finalprize
    #         print("{} won {}".format(players[players.index(player)]["name"], finalprize))
    #         break
    #     else:
    #         print("{} is not the word".format(wordguess))
    #         break
        
            



def main():
    gameSetup()    

    while True:
        wofRound()
        wofFinalRound()
        if input("Play again? (y/n): ").upper() == "N":
            break
        else:
            gameSetup()

if __name__ == "__main__":
    main()
    
    
