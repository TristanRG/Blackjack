import random
import sys

#Main class for the cards
class Card:
    def __init__(self, rank, suit):
        #Each card has a rank and a suit
        self._rank = rank
        self._suit = suit

    #Defines the value of each card based on their rank and handles the logic for aces
    def value(self):
        if self._rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self._rank == 'Ace':
            return 11
        else:
            return int(self._rank)

    #String representation
    def __str__(self):
        return f"{self._rank} of {self._suit}"

    #Displaying the representation
    def __repr__(self):
        return self.__str__()

#Handles the creation of the deck,shuffling and dealing the cards
class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    #Creates the deck of cards
    @staticmethod
    def create_deck():
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = []

        #Creates a card for each combination of rank and suit
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                deck.append(card)

        #We shuffle the deck 3 times to replicate a normal shuffle
        for _ in range(3):
            random.shuffle(deck)
        return deck

    #Deals the card at the top of the deck
    def deal_card(self):
        return self.cards.pop()

#Base class for the player and dealer, also manages their hand
class Participant:
    def __init__(self):
        self.hand = []

    #Adds a card to the participant's hand
    def add_card(self, card):
        self.hand.append(card)

    #Calculates the total point value of the participant's hand
    def calculate_total(self):
        total = 0
        aces = 0
        for card in self.hand:
            total += card.value()
            if card._rank == 'Ace':
                aces += 1

        #Adjusts the value of the ace if there is one
        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

#Player class, derived from participant
class Player(Participant):
    #Show the player's hand
    def show_hand(self):
        print(f"Your current hand is: {', '.join(str(card) for card in self.hand)}")

#Dealer class, derived from participant
class Dealer(Participant):
    #Show the dealer's first card
    def show_dealer_first_card(self):
        print(f"Dealer's first card is: {self.hand[0]}")

    #Reveal the dealer's full hand
    def reveal_full_hand(self):
        print(f"Dealer's current hand is: {', '.join(str(card) for card in self.hand)}")

    #Calculates the value of the first card for the dealer
    def first_card_value(self):
        return self.hand[0].value()

#Main function of the program
def main():
    menu() #starts the game loop

#Menu function that handles the user interaction
def menu():
    try:
        deposit = int(input("How much would you like to deposit? "))
    except ValueError:
        print("Make sure you provide a number.")
        return

    #Check if the initial deposit is valid
    if not check_funds(deposit):
            sys.exit("You have insufficient funds to make a bet. You're out.")

    while True:
        print(f"\nYour current balance is {deposit}")
        print("1. Make a bet.")
        print("2. Learn the basics")
        print("3. Exit")
        option = int(input("Choose an option: "))
        if option == 1:
            #Starts the betting process
            while True:
                try:
                    bet = int(input("How much would you like to bet? "))
                except ValueError:
                    print("Bet must be a number.")
                    continue
                if bet > deposit:
                    print("Your bet cannot be higher than your current deposit")
                    continue
                elif bet < 1:
                    print("Provide a higher bid")
                    continue

                #Calls the game_starts method and updates the deposit
                deposit = game_starts(bet, deposit)
                break

        #Display the game rules
        elif option == 2:
            display_game_rules()
            continue

        #Exit the game
        elif option == 3:
            sys.exit(0)

        else:
            print("Invalid option")
            continue

#Function that starts the interactive game of blackjack
def game_starts(bet, deposit):
    #We initialize the deck, player and dealer
    deck = Deck()
    player = Player()
    dealer = Dealer()

    #Both the player and dealer draw 2 cards
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    #Show the player's hand and the dealer's first card and their points
    player.show_hand()
    dealer.show_dealer_first_card()
    player_points = player.calculate_total()
    dealer_points = dealer.calculate_total()
    print(f"You currently have {player_points} points")
    print(f"The dealer currently has {dealer.first_card_value()} points")

    #Gives the player the option to double, hit or stand
    while True:
        print("\n1. Would you like to double down and draw a card? ")
        print("2. Would you like to hit? ")
        print("3. Would you like to stand? ")
        choice = int(input("Choose: "))

        if choice == 1:
            #Player chooses to double down
            if bet * 2 > deposit:
                print("You have insufficient funds to double down.")
                continue
            else:
                bet *= 2
                player.add_card(deck.deal_card())
                player_points = player.calculate_total()
                player.show_hand()
                print(f"You currently have {player_points} points")
                if player_points > 21:
                    print("You went over 21. You lose.")
                    return deposit - bet
                break

        elif choice == 2:
            #Player chooses to hit
            while True:
                player.add_card(deck.deal_card())
                player_points = player.calculate_total()
                player.show_hand()
                print(f"You currently have {player_points} points")
                if player_points > 21:
                    print("You went over 21. You lose.")
                    deposit -= bet
                    return deposit
                #Automatically stans if the player reaches the score of 21
                elif player_points == 21:
                    break
                print("1. Would you like to hit again?")
                print("2. Would you like to stand?")
                choice = int(input("Choose: "))
                if choice == 1:
                    continue
                elif choice == 2:
                    break
                else:
                    print("Invalid choice")
            break

        #Player chooses to sit
        elif choice == 3:
            break

        else:
            print("Invalid option")
            continue

    if player_points > 21:
        print("You went over 21. You lose.")
        return

    #Dealer's turn starts
    dealer.reveal_full_hand()
    #While the dealer's points are under 17 he must keep hitting
    while dealer_points < 17:
        dealer.add_card(deck.deal_card())
        dealer_points = dealer.calculate_total()
        dealer.reveal_full_hand()
        print(f"The dealer currently has {dealer_points} points")

    #Use the game_results function to determine the result and update the deposit
    deposit = game_results(player_points, dealer_points, deposit, bet)
    return deposit

#Gives the outcome of the game and returns the winnings/losses based on it
def game_results(player_points, dealer_points, deposit, bet):

    if dealer_points > 21:
        print(f"Dealer went over 21. You win {bet}$")
        deposit += bet

    elif dealer_points > player_points:
        print(f"Dealer has {dealer_points} and you have {player_points}. You lost {bet}")
        deposit -= bet

    elif player_points > dealer_points:
        print(f"Your score {player_points} is higher than the dealer's points {dealer_points}. You win {bet}$")
        deposit += bet

    else:
        print(f"It's a tie. You're getting your {bet} back")

    return deposit

#Checks whether the deposit is lesser or equal to 0
def check_funds(deposit):
    if deposit <= 0:
        return False
    return True

#Display the game rules
def display_game_rules():
        print("Game Rules:\n"
                  "1. Place your bet: Before the cards are dealt, you must place a bet.\n"
                  "2. Receive your cards: Once all bets have been placed, the dealer will deal two cards to each player, face up.\n"
                  "3. Decide to double, hit or stand: After receiving your two cards, you can choose to 'double' your bet and receive an additional card, 'hit' and receive additional cards, or 'stand' and keep your current hand.\n"
                  "4. Dealer’s turn: After all players have had their turn, the dealer will reveal their face-down card and hit or stand according to predetermined rules.\n"
                  "5. Determine the winner: If neither the player nor the dealer busts, the person with the highest hand value wins.")

if __name__ == "__main__":
    main()
