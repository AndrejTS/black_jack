from random import randrange
from time import sleep


class BlackJack:
    def __init__(self, deposit=1000, number_of_decks=1): 
        card_deck = [(2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), ('J', 'S'), ('Q', 'S'), ('K', 'S'), ('A', 'S'), 
                    (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), ('J', 'D'), ('Q', 'D'), ('K', 'D'), ('A', 'D'), 
                    (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'C'), 
                    (2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), ('J', 'H'), ('Q', 'H'), ('K', 'H'), ('A', 'H')]
        self.all_cards = card_deck * number_of_decks
        self.money = deposit


    def deal_cards(self):
        cards = []
        for _ in range(2):
            cards.append(self.all_cards.pop(randrange(len(self.all_cards))))
        return cards


    def deal_one_card(self):
        card = self.all_cards.pop(randrange(len(self.all_cards)))
        return card


    def value_of_cards(self, cards):
        value = 0
        for card in cards:
            if type(card[0]) == int:
                value += card[0]
            elif card[0] in 'JQK':
                value += 10
            ###
        return value


    def cards_to_str(self, cards):
        result = ""
        for i in cards:
            result += str(i[0]) + i[1] + ' '
        return result 


    def print_cards_and_values(self, player, players_value, croupier, croupier_value):
        print(f"Croupier's cards: {self.cards_to_str(croupier)}   (value: {croupier_value})")
        print(f"Your cards: {self.cards_to_str(player)}   (value: {players_value})")


    def play(self):
        while True:
            print()
            print("Your money: " + str(self.money))
            bet = input("Your bet: ")
            print()
            players_cards = self.deal_cards()
            croupiers_cards = self.deal_cards()
            players_value = self.value_of_cards(players_cards)
            croupier_value = self.value_of_cards(croupiers_cards)

            self.print_cards_and_values(players_cards, players_value, croupiers_cards, croupier_value)

            while True:
                decision = input("Next card? (y/n) ")
                print()
                if decision == "y":
                    players_cards.append(self.deal_one_card())
                    players_value = self.value_of_cards(players_cards)
                    self.print_cards_and_values(players_cards, players_value, croupiers_cards, croupier_value)
                    if players_value > 21:
                        break
                if decision == "n":
                    while croupier_value < 17:
                        croupiers_cards.append(self.deal_one_card())
                        croupier_value = self.value_of_cards(croupiers_cards)
                        self.print_cards_and_values(players_cards, players_value, croupiers_cards, croupier_value)
                        print()
                        if croupier_value < 17:
                            sleep(5)
                    break
            if players_value > 21:
                print()
                print("You lose")
                self.money -= int(bet)
            else:
                if croupier_value > 21:
                    print()
                    print("You win")
                    self.money += int(bet)
                elif players_value > croupier_value:
                    print()
                    print("You win")
                    self.money += int(bet)
                elif players_value == croupier_value:
                    print()
                    print("Tie")
                else:
                    print()
                    print("You lose")
                    self.money -= int(bet)


f = BlackJack()
f.play()
