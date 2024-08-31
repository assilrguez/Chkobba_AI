import random
from itertools import combinations
from AI_chkobba import AIPlayer #type: ignore

class Card:
    """
    Represents a card in the Chkobba game.

    Attributes:
        rank (str): The rank of the card (e.g., 'A', '2', '3', etc.).
        suit (str): The suit of the card (e.g., '♥', '♦', '♣', '♠').
        value (int): The numeric value of the card, based on its rank.
    """
    def __init__(self, rank:str, suit:str) -> None:
        """Initializes a card with a given rank and suit."""
        self.rank = rank
        self.suit = suit
        self.value = self.get_value()
    
    def get_value(self) -> int:
        """Returns the numeric value of the card based on its rank."""
        values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 'Q': 8, 'J': 9, 'K': 10}
        return values[self.rank]
    
    def __str__(self) -> str:
        """Returns a string representation of the card."""
        return f"({self.rank}{self.suit})"

class Player:
    """
    Represents a player in the Chkobba game.

    Attributes:
        name (str): The name of the player.
        hand (list): The cards currently in the player's hand.
        capture (list): The cards captured by the player.
        chkobba (int): The number of Chkobbas (captures of all table cards).
        score (int): The player's score.
    """
    def __init__(self, name:str) -> None:
        """Initializes a player with a given name and empty hand, capture list, and score."""
        self.card_accepted = False
        self.name = name
        self.hand = []
        self.capture = []
        self.chkobba = 0
        self.score = 0

    def capture_card(self, idx:int, table:list) -> list :
        """
        Handles the logic for capturing cards from the table or playing a card.

        Args:
            idx (int): The index of the card to be played.
            table (list): The list of cards currently on the table.

        Returns:
            list: The list of captured cards.
        """
        captured_cards = []
        played_card = self.hand[idx] 
        # Exact match capture
        for card in table:
            if card.value == played_card.value:
                print(f"{self.name} captured {card} with {played_card}")
                captured_cards.extend([played_card, card])
                self.hand.remove(played_card)
                table.remove(card)
                break  # Only one match needed
        # Sum match capture
        if not captured_cards:
            v_table = [card.value for card in table]
            for r in range(2, len(table) + 1):
                for combo in combinations(v_table, r):
                    cards_combo = []
                    if sum(combo) == played_card.value:
                        for value in combo:
                            c = table[v_table.index(value)]
                            cards_combo.append(c)
                            table.remove(c)
                            v_table.remove(value)
                        captured_cards.extend([played_card, cards_combo])
                        print(f"{self.name} captured", *cards_combo, f"with {played_card}")
                        self.hand.remove(played_card)
                        break
        if not captured_cards:
            print(f"{self.name} threw {played_card}")
            table.append(played_card)
            self.hand.remove(played_card)
        else :
            self.capture.extend(captured_cards)

    def play_turn(self,table:list) -> Card :
        """
        Manages the player's turn to play a card and attempt to capture cards from the table.

        Args:
            table (list): The list of cards currently on the table.
        """
        print("#"*50,"\n"*4,'#'*50)
        print("Press 'Enter' to reveal cards")
        print("#"*50,"\n"*4,'#'*50)
        input()
        print(f"Cards on table :",*table)
        print("your Hand :")
        for i, card in enumerate(self.hand) :
            print(f"{i+1}. {card}")
        try :
            idx = int(input(f"play a card by its index (1..{len(self.hand)}) : ")) - 1
            if ( idx+1 > len(self.hand) or (idx+1)<=0) :
                raise ValueError
        except :
            while ( idx+1 > len(self.hand) or (idx+1)<=0) :
                print("invalid input !, Please pick a valid one .")
                idx = int(input(f"play a card by its index (1..{len(self.hand)}) : ")) - 1
        finally :
            self.capture_card(idx,table)
            if not table :
                self.chkobba += 1

class ChkobbaGame:
    """
    Manages the Chkobba game, including players, deck, dealing, and game rounds.

    Attributes:
        players (list): The list of players in the game.
        table_cards (list): The list of cards currently on the table.
    """
    def __init__(self,players:list) -> None:
        """Initializes the game with a list of players and an empty table."""
        self.players = players
        self.table_cards = []

    def create_deck(self) -> list:
        """
        Creates a shuffled deck of 40 cards for the game.

        Returns:
            list: The shuffled deck of cards.
        """
        suits = ['♥', '♦', '♣', '♠']
        ranks = ['A', '2', '3', '4', '5', '6', '7', 'J', 'Q', 'K']
        deck = [Card(rank, suit) for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck
    
    def cut(self,player:Player) -> None:
        """
        Allows a player to cut the deck and choose to keep or discard a card.

        Args:
            player (Player): The player who is cutting the deck.
        """
        idx = int(input("cut the deck in any number (1..40): "))
        card = self.deck[idx]
        print(card)
        card_accepted = input("Do you want to keep it (Y)es/(N)o : ").capitalize()
        player.card_accepted = True if (card_accepted == 'Y' or card_accepted == "Yes") else False
        if player.card_accepted :
            player.hand.append(card)
        else:
            self.table_cards.append(card)
            if player.hand:
                player.hand.remove(card)
        self.deck.remove(card)

    def deal_cards(self):
        """
        Deals cards to players and the table for the current round.
        """
        if self.deal == 1:
            for player in self.players :
                    if not player.card_accepted :
                        player.hand = [self.deck.pop() for _ in range(3)]
                    else :
                        player.hand.extend([self.deck.pop() for _ in range(2)])  
                    # self.ai_hand = [self.deck.pop() for _ in range(3)]
            if len(self.table_cards) == 0: 
                self.table_cards = [self.deck.pop() for _ in range(4)]
            else:
                self.table_cards.extend([self.deck.pop() for _ in range(3)])
        else:
            for player in self.players :
                player.hand = [self.deck.pop() for _ in range(3)]

    def arrange_players(self) -> None:
        """
        Rotates the player order for the next round.
        """
        lst = self.players
        def right_shift(lst):
            return lst[-1:] + lst[:-1]
        self.players = right_shift(lst)

    def evaluate_scores(self):
        """
        Evaluates and updates the scores for each player based on game rules.
        """
        self.statistics_list = []
        for player in self.players :
            El_hayya = (Card('7','♦') in player.capture)
            denari = len([card for card in player.capture if card.suit == '♦']) >  5
            karta = len(player.capture) > 20
            sevens = [card for card in player.capture if card.value == 7]
            sixes = [card for card in player.capture if card.value == 6] 
            bermila = ((len(sevens) > 2 ) or (len(sevens) > 2 and len(sixes) > 2))
            if El_hayya :
                player.score += 1
            if denari :
                player.score += 1
            if karta :
                player.score += 1
            if bermila :
                player.score += 1
            player.score += player.chkobba
            self.statistics_list.append((player.name, El_hayya, bermila, denari, karta))
        
    def show_statistics(self,lst:list) -> None:
        """
        Displays the game statistics for all players.

        Args:
            lst (list): The list of statistics to display.
        """
        print(f"players  | {lst[0][0]}     {lst[1][0]}")
        print(f"EL-Hayya | {lst[0][1]}     | {lst[1][1]}")
        print(f"Bermila  | {lst[0][2]}     | {lst[1][2]}")
        print(f"denery   | {lst[0][3]}     | {lst[1][3]}")
        print(f"karta    | {lst[0][4]}     | {lst[1][4]}")

    def play_round(self) -> None:
        """
        Manages a round of the game, dealing cards and handling player turns.
        """
        self.deal = 1
        self.deck = self.create_deck()
        while self.deck:
            print(f"--- Deal number : {self.deal} ---")
            print(f"{self.players[0].name} plays first !")
            if self.deal == 1 :
                self.cut(self.players[0])
            self.deal_cards()
            while any(player.hand for player in self.players):
                for player in self.players :
                    print(f"{player.name} turn")
                    player.play_turn(self.table_cards)
            self.deal += 1
        self.evaluate_scores()
        self.show_statistics(self.statistics_list)
    def play_ai_round(self) -> None:
        """
        Placeholder function for managing a round with AI players.
        """
        #coming late
        pass

    def reset_round(self) -> None :
        """
        Resets the game state between rounds.
        """
        self.deck = []
        self.table_cards = []
        for player in self.players :
            player.hand = []
            player.chkobba = 0
            player.capture = []
            player.card_accepted = None

    def reset_game(self) -> None:
        """
        Resets the entire game for a fresh start.
        """
        for player in self.players :
            player.score = 0
        print("GAME OVER !!")

    def start_game(self):
        """
        Starts the game loop, alternating rounds until a player reaches the target score.
        """
        round_number = 1
        print("Welcome to Chkobba!")
        print(f"--- Round number : {round_number} ---")
        while all(player.score < 11 for player in self.players) or self.players.score[0] == self.players.score[1]:
            self.play_round()
            self.reset_round()
            self.arrange_players()
        scores = {player.score:player.name for player in self.players}
        print(f"{scores[max(scores)]} wins")
        self.reset_game()
    
    def start_ai_game(self):
        """
        Placeholder function for starting a game with AI opponents.
        """
        #coming late
        pass

def main() -> None :
    """
    Entry point of the game, allowing the user to select a game mode and handle setup.
    """
    try:
        gameMode = int(input("Choose GameMode :\n1. Player VS AI .\n2. Player VS Player .\n> "))
        gameMode = 2 # Force Humans GameMode untill AI GameMode is ready
        if gameMode == 1:
            try:
                player = input("Enter player name : ")
                if player == "AI":
                    raise ValueError
            except :
                print("Player name can't be AI !\nPlease pick an allowed name .")
            players = [Player(player), AIPlayer()]
            game = ChkobbaGame(players)
            game.start_ai_game()
        elif gameMode == 2 :
            player1 = input("Enter player1 name : ")
            player2 = input("Enter player2 name : ")
            players = [Player(player1), Player(player2)]
            game = ChkobbaGame(players)
            game.start_game()
        else :
            raise ValueError
    except ValueError:
        print("please pick (1) for AI game or (2) for humans game")

if __name__ == "__main__":
    main()