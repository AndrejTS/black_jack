from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QFont

from random import randrange

import sys


BLACKJACK = (1, 21)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blackjack')
        self.setGeometry(500, 200, 600, 800) 
        self.generalLayout = QGridLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        self.model = BlackjackModel()
        
        self.resultMsg = QLabel('')
        self.resultMsg.setFont(QFont('Arial', 14))
        self.generalLayout.addWidget(self.resultMsg) 

        self.money = QLabel('Money: ' + str(self.model.money))
        self.money.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.money)

        self.bet = QLabel('Bet: ' + str(self.model.bet))
        self.bet.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.bet)

        self.croupiersCards = QLabel('Croupier cards: ')
        self.croupiersCards.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.croupiersCards)

        self.croupiersValue = QLabel('Croupier value: ')
        self.croupiersValue.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.croupiersValue)

        self.playersCards = QLabel('Your cards: ')
        self.playersCards.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.playersCards)

        self.playersValue = QLabel('Your value: ')
        self.playersValue.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.playersValue)

        self.incBetBtn = QPushButton('+')
        self.incBetBtn.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.incBetBtn)

        self.decBetBtn = QPushButton('-')
        self.decBetBtn.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.decBetBtn)

        self.dealBtn = QPushButton('DEAL')
        self.dealBtn.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.dealBtn)

        self.hitBtn = QPushButton('HIT')
        self.hitBtn.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.hitBtn)

        self.standBtn = QPushButton('STAND')
        self.standBtn.setFont(QFont('Arial', 20))
        self.generalLayout.addWidget(self.standBtn)
        
        # Deactivate all buttons, beyond incBetBtn
        self.deactivateButtons()
        self.incBetBtn.setEnabled(True)

        # Connect signals and slots
        self.incBetBtn.clicked.connect(self.incrementBet)
        self.decBetBtn.clicked.connect(self.decrementBet)
        self.dealBtn.clicked.connect(self.initGame)
        self.hitBtn.clicked.connect(self.playerHit)
        self.standBtn.clicked.connect(self.stand)


    def displayBetAndMoney(self):
        self.money.setText('Money: ' + str(self.model.money))
        self.bet.setText('Bet: ' + str(self.model.bet))


    def displayCardsAndValues(self):
        croupiersCards = self.model.cardsToStr(self.model.croupiersCards)
        croupiersValue = self.model.valueToStr(self.model.croupiersValue)
        playersCards = self.model.cardsToStr(self.model.playersCards)
        playersValue = self.model.valueToStr(self.model.playersValue)
        self.croupiersCards.setText('Croupier cards: ' + croupiersCards)
        self.croupiersValue.setText('Croupier value: ' + croupiersValue)
        self.playersCards.setText('Your cards: ' + playersCards)
        self.playersValue.setText('Your value: ' + playersValue)


    def cleanCardsAndValues(self):
        self.croupiersCards.setText('Croupier cards: ')
        self.croupiersValue.setText('Croupier value: ')
        self.playersCards.setText('Your cards: ')
        self.playersValue.setText('Your value: ') 


    def deactivateButtons(self):
        """Deactivate all buttons"""
        self.incBetBtn.setEnabled(False)
        self.decBetBtn.setEnabled(False)
        self.dealBtn.setEnabled(False)
        self.hitBtn.setEnabled(False)
        self.standBtn.setEnabled(False)


    def evaluateGame(self):
        self.model.evaluateGame()
        self.resultMsg.setText(self.model.resultMsg)
        self.displayBetAndMoney()
        self.incBetBtn.setEnabled(True)


    def incrementBet(self):
        if self.model.money == 0:
            self.incBetBtn.setEnabled(False)
            return
        self.resultMsg.setText('')
        self.cleanCardsAndValues()
        self.model.incrementBet()
        self.decBetBtn.setEnabled(True)
        self.dealBtn.setEnabled(True)
        self.displayBetAndMoney()


    def decrementBet(self):
        self.model.decrementBet()
        self.incBetBtn.setEnabled(True)
        if self.model.bet == 0:
            self.decBetBtn.setEnabled(False)
            self.dealBtn.setEnabled(False)
        self.displayBetAndMoney()


    def initGame(self):
        self.model.initGame()
        self.displayCardsAndValues()
        if self.model.playersValue == BLACKJACK:
            self.stand()
        else:
            self.deactivateButtons()
            self.hitBtn.setEnabled(True)
            self.standBtn.setEnabled(True)


    def playerHit(self):
        self.model.playerHit()
        self.displayCardsAndValues()
        if self.model.playersValue > (0, 21):
            self.deactivateButtons()
            self.evaluateGame()
        if self.model.playersValue == (0, 21):
            self.stand()


    def stand(self):
        self.deactivateButtons()
        while self.model.croupiersValue < (0, 17):
            self.model.dealersHit()
            self.displayCardsAndValues()
        self.evaluateGame()


class BlackjackModel:
    def __init__(self, deposit=1000, numberOfDecks=5): 
        deck = Deck()
        self.allCards = deck.cardDeck * numberOfDecks
        self.money = deposit
        self.bet = 0
        self.resultMsg = None


    def incrementBet(self):
        self.money -= 50
        self.bet += 50


    def decrementBet(self):
        self.money += 50
        self.bet -= 50


    def initGame(self):
        self.playersCards = self.dealCard(2)
        self.croupiersCards = self.dealCard(2)
        self.playersValue = self.valueOfCards(self.playersCards)
        self.croupiersValue = self.valueOfCards(self.croupiersCards)


    def playerHit(self):
        self.playersCards += self.dealCard(1)
        self.playersValue = self.valueOfCards(self.playersCards)


    def dealersHit(self):
        self.croupiersCards += self.dealCard(1)
        self.croupiersValue = self.valueOfCards(self.croupiersCards)


    def evaluateGame(self):
        if self.playersValue == BLACKJACK:
            if self.croupiersValue == BLACKJACK:
                print("Tie")
                self.money += self.bet
                self.resultMsg = 'Tie'
            else:
                print("You win (3:2)")
                self.money += int(self.bet * 2.5)
                self.resultMsg = 'You win!'
        elif self.croupiersValue == BLACKJACK:
            print("You lose")
            self.resultMsg = 'You lose!'
        elif self.playersValue > (0, 21):
            print("BUSTED, You lose")
            self.resultMsg = 'BUSTED, You lose'
        elif self.croupiersValue > (0, 21):
            print("You win")
            self.money += self.bet * 2
            self.resultMsg = 'You win!'
        elif self.playersValue > self.croupiersValue:
            print("You win")
            self.money += self.bet * 2
            self.resultMsg = 'You win!'
        elif self.playersValue == self.croupiersValue:
            print("Tie")
            self.money += self.bet
            self.resultMsg = 'Tie'
        else:
            print("You lose")
            self.resultMsg = 'You lose!'

        self.bet = 0


    def dealCard(self, quantity):
        cards = []
        for _ in range(quantity):
            cards.append(self.allCards.pop(randrange(len(self.allCards))))
        return cards


    def cardsToStr(self, cards):
        result = ""
        for i in cards:
            result += str(i[0]) + i[1] + ' '
        return result 


    def valueOfCards(self, cards):
        values = [c[0] for c in cards]
        totalValue = 0
        for v in values:
            if type(v) == int: # cards from 2 to 10
                totalValue += v
            elif v in 'JQK':
                totalValue += 10
            else: # Ace
                totalValue += 11
        
        # Ace can be 1 or 11
        # if player is over 21, subtract 10 for one ace
        if totalValue > 21 and 'A' in values:
            numberOfAces = values.count('A')
            for _ in range(numberOfAces):
                totalValue -= 10
                if totalValue <= 21:
                    break

        # check blackjack
        if len(cards) == 2 and totalValue == 21:
            return (1, 21)
        else:
            return (0, totalValue)


    def valueToStr(self, value):
        if value == BLACKJACK:
            return 'Blackjack'
        return str(value[1])


class Deck:
    """Class for creating deck of cards"""
    def __init__(self):
        self.cardDeck = []
        listOfValues = []
        # append number values 
        for i in range(2,11): 
            listOfValues.append(i)
        # append high values
        highCards = ['J', 'Q', 'K', 'A']
        for i in highCards:
            listOfValues.append(i)
        # create one deck (52 cards)
        colors = ['♠', '♦', '♣', '♥']
        for color in colors:
            for value in listOfValues:
                self.cardDeck.append((value, color))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
