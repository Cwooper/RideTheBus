# Main program for Ride The Bus bot

import time
from datetime import datetime
import sys
from colorama import init
from card_detection import identify_card, capture_screen, save_debug_image
from game_logic import GameState
from ui_interaction import *
from utils import setup_logging
from config import *

def main():
    """Main program loop"""
    # Initialize colorama for cross-platform color support
    init()
    
    # Setup
    print("Starting Ride The Bus bot...")
    time.sleep(3)
    
    game_state = GameState()
    print(f"Initial balance: ${game_state.balance}")
    
    try:
        # Main game loop
        while True:
            
            # Click Ready button until options are available
            attempts = 0
            max_attempts = 20
            while not is_option_available() and attempts < max_attempts:
                click_ready()  # This already includes a 1-second cooldown
                attempts += 1
                # Short wait before checking again
                time.sleep(0.2)
            
            if attempts >= max_attempts:
                print("Failed to detect options after maximum attempts")
                continue
            
            # Round 1: Red or Black
            if game_state.round == 1:
                # Always choose red
                click_red()
                
                # Wait 1.5 seconds for card to appear
                wait_for_card_to_appear()
                
                # Capture screen
                screen = capture_screen()
                
                # Identify the card
                card = identify_card(screen)
                game_state.add_card(card)
                
                if not card:
                    print("Failed to identify card in round 1")
                    game_state.update_balance(False)  # Assume loss if card detection fails
                    continue
                
                # Determine if we won
                won = game_state.determine_round1_winner()
                game_state.update_balance(won)
                
                if not won:
                    continue  # Start over if we lost
            
            # Wait for next round options
            if not wait_for_option_available(timeout=15):
                print("Options for round 2 not detected, restarting")
                game_state.reset_round()
                continue
            
            # Round 2: Higher or Lower
            if game_state.round == 2:
                # Determine best choice
                choice = game_state.determine_round2_choice()
                
                # Make the choice
                if choice == "higher":
                    click_higher()
                else:
                    click_lower()
                
                # Wait 1.5 seconds for card to appear
                wait_for_card_to_appear()
                
                # Capture screen
                screen = capture_screen()
                
                # Identify the card
                card = identify_card(screen)
                game_state.add_card(card)
                
                if not card:
                    print("Failed to identify card in round 2")
                    game_state.update_balance(False)  # Assume loss if card detection fails
                    continue
                
                # Determine if we won
                won = game_state.determine_round2_winner()
                game_state.update_balance(won)
                
                if not won:
                    continue  # Start over if we lost
            
            # Wait for next round options
            if not wait_for_option_available(timeout=15):
                print("Options for round 3 not detected, restarting")
                game_state.reset_round()
                continue
            
            # Round 3: Inside or Outside
            if game_state.round == 3:
                # Determine best choice
                choice = game_state.determine_round3_choice()
                
                # Make the choice
                if choice == "inside":
                    click_inside()
                else:
                    click_outside()
                
                # Wait 1.5 seconds for card to appear
                wait_for_card_to_appear()
                
                # Capture screen
                screen = capture_screen()
                
                # Identify the card
                card = identify_card(screen)
                game_state.add_card(card)
                
                if not card:
                    print("Failed to identify card in round 3")
                    game_state.update_balance(False)  # Assume loss if card detection fails
                    continue
                
                # Determine if we won
                won = game_state.determine_round3_winner()
                game_state.update_balance(won)
                
                if not won:
                    continue  # Start over if we lost
            
            # Wait for next round options
            if not wait_for_option_available(timeout=15):
                print("Options for round 4 not detected, restarting")
                game_state.reset_round()
                continue
            
            # Round 4: Suit
            if game_state.round == 4:
                # Determine best choice
                suit = game_state.determine_round4_choice()
                game_state.current_suit_choice = suit  # Store the choice
                
                # Make the choice
                click_suit(suit)
                
                # Wait 1.5 seconds for card to appear
                wait_for_card_to_appear()
                
                # Capture screen
                screen = capture_screen()
                
                # Identify the card
                card = identify_card(screen)
                game_state.add_card(card)
                
                if not card:
                    print("Failed to identify card in round 4")
                    game_state.update_balance(False)  # Assume loss if card detection fails
                    continue
                
                # Determine if we won
                won = game_state.determine_round4_winner()
                game_state.update_balance(won)
                
                # Always start over after round 4
                game_state.total_games += 1
                continue
            
            # No sleep between iterations - the program will naturally
            # move to the next iteration without artificial delay
    
    except KeyboardInterrupt:
        print("Bot stopped by user")
        print(f"Final balance: ${game_state.balance}")
        print(f"Games played: {game_state.total_games}")
        print(f"Wins: {game_state.wins}, Losses: {game_state.losses}")
    except Exception as e:
        print(f"Unhandled exception: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        print("Bot shutting down")

if __name__ == "__main__":
    main()
    