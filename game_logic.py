# Game logic for Ride The Bus

import random
from config import *
from colorama import Fore, Style

class GameState:
    def __init__(self):
        self.round = 1
        self.balance = INITIAL_BALANCE
        self.current_round_cards = []
        self.game_active = True
        self.total_games = 0
        self.wins = 0
        self.losses = 0
        self.current_suit_choice = None  # Store the current suit choice
        self.current_suit_choice = None  # Store the current suit choice
    
    def reset_round(self):
        """Reset the current round cards"""
        self.round = 1
        self.current_round_cards = []
        self.current_suit_choice = None  # Reset the suit choice
        self.current_suit_choice = None  # Reset the suit choice
    
    def format_cards_string(self):
        """Format the current round cards into a readable string"""
        if not self.current_round_cards:
            return "No cards"
            
        card_strings = []
        for card in self.current_round_cards:
            if card['value'] and card['suit']:
                card_strings.append(f"{card['value']} {card['suit']}")
            else:
                card_strings.append("Unknown card")
                
        return ", ".join(card_strings)
    
    def add_card(self, card):
        """Add a card to the current round"""
        if card:
            self.current_round_cards.append(card)
        else:
            print("OCR failed to detect card!")
            self.current_round_cards.append({'value': '?', 'suit': '?', 'numeric_value': None})
    
    def update_balance(self, won):
        """Update balance based on win or loss"""
        cards_str = self.format_cards_string()
        
        if won:
            if self.round == 4:
                self.balance += WIN_AMOUNT
                self.wins += 1
                print(f"{cards_str} --- {Fore.GREEN}Won{Style.RESET_ALL}")
                
                # Display balance with color
                if self.balance > 0:
                    print(f"{Fore.GREEN}Balance: ${self.balance}{Style.RESET_ALL}")
                elif self.balance < 0:
                    print(f"{Fore.RED}Balance: ${self.balance}{Style.RESET_ALL}")
                else:
                    print(f"Balance: ${self.balance}")
                    
                self.reset_round()
                self.total_games += 1
            else:
                # Don't print anything after winning intermediate rounds
                self.round += 1
        else:
            self.balance -= BET_AMOUNT
            self.losses += 1
            print(f"{cards_str} --- {Fore.RED}Lost{Style.RESET_ALL}")
            
            # Display balance with color
            if self.balance > 0:
                print(f"{Fore.GREEN}Balance: ${self.balance}{Style.RESET_ALL}")
            elif self.balance < 0:
                print(f"{Fore.RED}Balance: ${self.balance}{Style.RESET_ALL}")
            else:
                print(f"Balance: ${self.balance}")
                
            self.reset_round()
    
    def determine_round1_winner(self):
        """Determine if we won round 1 (Red or Black)"""
        if not self.current_round_cards:
            return False
        
        card = self.current_round_cards[0]
        if not card['suit']:
            return False
            
        is_red = card['suit'] in RED_SUITS
        
        # We always bet on red
        return is_red
    
    def determine_round2_choice(self):
        """Determine whether to bet higher or lower for round 2"""
        if not self.current_round_cards:
            return "higher"  # Default if no card detected
        
        card1 = self.current_round_cards[0]
        value1 = card1['numeric_value']
        
        # Calculate probabilities for higher (inclusive) and lower (exclusive)
        remaining_cards = CARDS_PER_DECK - 1
        
        # Cards higher than or equal to the current card
        higher_count = sum(1 for v in CARD_VALUES.values() if v >= value1) * 4
        # Remove the one we've seen
        higher_count -= 1
        
        # Cards lower than the current card
        lower_count = sum(1 for v in CARD_VALUES.values() if v < value1) * 4
        
        higher_prob = higher_count / remaining_cards
        lower_prob = lower_count / remaining_cards
        
        if higher_prob > lower_prob:
            return "higher"
        elif lower_prob > higher_prob:
            return "lower"
        else:
            # In case of equal odds, choose randomly
            return random.choice(["higher", "lower"])
    
    def determine_round2_winner(self):
        """Determine if we won round 2 (Higher or Lower)"""
        if len(self.current_round_cards) < 2:
            return False
        
        card1 = self.current_round_cards[0]
        card2 = self.current_round_cards[1]
        
        if card1['numeric_value'] is None or card2['numeric_value'] is None:
            return False
            
        choice = self.determine_round2_choice()
        
        if choice == "higher":
            result = card2['numeric_value'] >= card1['numeric_value']
            return result
        else:
            result = card2['numeric_value'] < card1['numeric_value']
            return result
    
    def determine_round3_choice(self):
        """Determine whether to bet inside or outside for round 3"""
        if len(self.current_round_cards) < 2:
            return "inside"  # Default if not enough cards
        
        card1 = self.current_round_cards[0]
        card2 = self.current_round_cards[1]
        
        # Ensure we have valid numeric values
        if card1['numeric_value'] is None or card2['numeric_value'] is None:
            return "inside"  # Default if missing values
        
        # Ensure lower value is first
        if card1['numeric_value'] > card2['numeric_value']:
            low_card, high_card = card2, card1
        else:
            low_card, high_card = card1, card2
        
        low_val = low_card['numeric_value']
        high_val = high_card['numeric_value']
        
        # Calculate probabilities
        remaining_cards = CARDS_PER_DECK - 2
        
        # Cards inside (inclusive)
        # Inside includes cards equal to boundary cards
        inside_range = list(range(low_val, high_val + 1))
        inside_count = len(inside_range) * 4
        
        # Subtract the two boundary cards we've seen
        inside_count -= 2
        
        # Cards outside (exclusive)
        # Outside excludes boundary cards
        outside_count = remaining_cards - inside_count
        
        inside_prob = inside_count / remaining_cards
        outside_prob = outside_count / remaining_cards
        
        if inside_prob > outside_prob:
            return "inside"
        elif outside_prob > inside_prob:
            return "outside"
        else:
            # In case of equal odds, choose randomly
            return random.choice(["inside", "outside"])
    
    def determine_round3_winner(self):
        """Determine if we won round 3 (Inside or Outside)"""
        if len(self.current_round_cards) < 3:
            return False
        
        card1 = self.current_round_cards[0]
        card2 = self.current_round_cards[1]
        card3 = self.current_round_cards[2]
        
        if any(card['numeric_value'] is None for card in [card1, card2, card3]):
            return False
        
        # Ensure lower value is first
        if card1['numeric_value'] > card2['numeric_value']:
            low_card, high_card = card2, card1
        else:
            low_card, high_card = card1, card2
        
        low_val = low_card['numeric_value']
        high_val = high_card['numeric_value']
        
        choice = self.determine_round3_choice()
        
        if choice == "inside":
            result = low_val <= card3['numeric_value'] <= high_val
            return result
        else:
            result = card3['numeric_value'] < low_val or card3['numeric_value'] > high_val
            return result
    
    def determine_round4_choice(self):
        """Determine which suit to bet on for round 4"""
        if len(self.current_round_cards) < 3:
            return random.choice(SUITS)  # Default if not enough cards
        
        # Only consider the first 3 cards for suit selection
        cards_to_consider = self.current_round_cards[:3]
        
        # Count seen cards by suit
        seen_suits = {}
        for suit in SUITS:
            seen_suits[suit] = 0
        
        for card in cards_to_consider:
            if card['suit']:
                seen_suits[card['suit']] += 1
        
        # Calculate probabilities for each suit
        remaining_cards = CARDS_PER_DECK - 3
        probabilities = {}
        
        for suit in SUITS:
            remaining_suit_cards = CARDS_PER_SUIT - seen_suits[suit]
            probabilities[suit] = remaining_suit_cards / remaining_cards
        
        # Find the suit(s) with the highest probability
        max_prob = max(probabilities.values())
        best_suits = [suit for suit, prob in probabilities.items() if prob == max_prob]
        
        # If multiple suits have the same probability, choose randomly
        chosen_suit = random.choice(best_suits)
        return chosen_suit
    
    def determine_round4_winner(self):
        """Determine if we won round 4 (Suit)"""
        if len(self.current_round_cards) < 4:
            return False
        
        card4 = self.current_round_cards[3]
        
        if not card4['suit']:
            return False
        
        # Use the stored suit choice instead of recalculating
        if self.current_suit_choice:
            chosen_suit = self.current_suit_choice
        else:
            # Fallback to calculation if somehow the choice wasn't stored
            chosen_suit = self.determine_round4_choice()
            
        return card4['suit'] == chosen_suit
    