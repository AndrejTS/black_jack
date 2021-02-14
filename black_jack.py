from random import randrange
from time import sleep


class Deck:
    def __init__(self):
        self.card_deck = []

        list_of_values = []
        # append number values 
        for i in range(2,11): 
            list_of_values.append(i)

        # append high values
        high_cards = ['J', 'Q', 'K', 'A']
        for i in high_cards:
            list_of_values.append(i)

        # create one deck (52 cards)
        colors = ['S', 'D', 'C', 'H']
        for color in colors:
            for value in list_of_values:
                self.card_deck.append((value, color))


class BlackJack:
    def __init__(self, deposit=1000, number_of_decks=1): 
        deck = Deck()
        self.all_cards = deck.card_deck * number_of_decks
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
        values = [c[0] for c in cards] # pouze hodnoty, barvy nejsou podstatne
        total_value = 0
        for v in values:
            if type(v) == int: # karty 2 - 10
                total_value += v
            elif v in 'JQK':
                total_value += 10
            else: # Ace
                total_value += 11
        
        # eso muze byt 1 nebo 11
        if total_value > 21 and 'A' in values:
            number_of_aces = values.count('A')
            for _ in range(number_of_aces):
                total_value -= 10
                if total_value <= 21:
                    break

        # check blackjack
        if len(cards) == 2 and total_value == 21:
            total_value = 'Blackjack'

        return total_value


    def cards_to_str(self, cards):
        result = ""
        for i in cards:
            result += str(i[0]) + i[1] + ' '
        return result 


    def print_status(self, player, players_value, croupier, croupier_value):
        print(f"Croupier's cards: {self.cards_to_str(croupier)}   (value: {croupier_value})")
        print(f"Your cards: {self.cards_to_str(player)}   (value: {players_value})")


    def play_game(self):
        while True:
            print()
            print("Your money: " + str(self.money))
            bet = input("Your bet: ")
            print()
            players_cards = self.deal_cards()
            croupiers_cards = self.deal_cards()
            players_value = self.value_of_cards(players_cards)
            croupier_value = self.value_of_cards(croupiers_cards)

            self.print_status(players_cards, players_value, croupiers_cards, croupier_value)


            # the player can draw more cards to improve his hand
            while True:
                decision = input("Next card? (y/n) ")
                print()
                if decision == "y":
                    players_cards.append(self.deal_one_card())
                    players_value = self.value_of_cards(players_cards)
                    self.print_status(players_cards, players_value, croupiers_cards, croupier_value)
                    if players_value > 21: # busted
                        break
                if decision == "n":
                    break

            # if player isn't busted, it is the dealer's turn
            if players_value <= 21:
                while croupier_value < 17: # dealer must draw
                    croupiers_cards.append(self.deal_one_card())
                    croupier_value = self.value_of_cards(croupiers_cards)
                    self.print_status(players_cards, players_value, croupiers_cards, croupier_value)
                    print()
                    if croupier_value < 17:
                        sleep(6)

            #evaluation
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


