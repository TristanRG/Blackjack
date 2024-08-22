from project import Card, Deck, Player, Dealer, game_results, check_funds, display_game_rules
from unittest.mock import patch
from io import StringIO

#Tests the calculate_total() function, which calculates the point value of the hand.
def test_calculate_total():
    player = Player()
    player.add_card(Card("Ace", "Hearts"))
    player.add_card(Card("King", "Diamonds"))
    assert player.calculate_total() == 21

    player.add_card(Card("8", "Clubs"))
    assert player.calculate_total() == 19

#Tests the deal_card() function, which deals a card and then removes that specific card from the deck, changing the deck value from 52 to 51.
def test_deal_card():
    deck = Deck()
    card = deck.deal_card()
    assert isinstance(card, Card)
    assert len(deck.cards) == 51

#Tests the deck_creation() function, which creates a full deck of 52 cards.
def test_deck_creation():
    deck = Deck()
    assert len(deck.cards) == 52

#Tests the first_card_value() function, which calculates the value of the dealer's first card only, in this case an Ace has the value of 11
def test_first_card_value():
    dealer = Dealer()
    dealer.add_card(Card("Ace", "Spades"))
    dealer.add_card(Card("9", "Hearts"))

    assert dealer.first_card_value() == 11

#Tests the game_results() function, which tells the the outcome of the game based on the point values
def test_game_results():
    assert game_results(20, 18, 1000, 100) == 1100  # Player wins
    assert game_results(18, 20, 1000, 100) == 900   # Dealer wins
    assert game_results(20, 20, 1000, 100) == 1000  # Tie
    assert game_results(20, 22, 1000, 100) == 1100  # Dealer busts

#Tests whether the user has enough funds to continue
def test_check_funds():
    assert check_funds(100) == True  # Positive deposit
    assert check_funds(0) == False   # Zero deposit
    assert check_funds(-50) == False # Negative deposit

#Tests whether the game rules are displayede correctly
def test_display_game_rules():
    expected_output = (
        "Game Rules:\n"
        "1. Place your bet: Before the cards are dealt, you must place a bet.\n"
        "2. Receive your cards: Once all bets have been placed, the dealer will deal two cards to each player, face up.\n"
        "3. Decide to double, hit or stand: After receiving your two cards, you can choose to 'double' your bet and receive an additional card, 'hit' and receive additional cards, or 'stand' and keep your current hand.\n"
        "4. Dealer’s turn: After all players have had their turn, the dealer will reveal their face-down card and hit or stand according to predetermined rules.\n"
        "5. Determine the winner: If neither the player nor the dealer busts, the person with the highest hand value wins.\n"
    )

    # Mock print and capture output
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        display_game_rules()
        output = mock_stdout.getvalue()

    assert output == expected_output
