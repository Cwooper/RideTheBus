# Ride The Bus OCR Bot

An automated bot that plays the casino-style "Ride The Bus" card game in Schedule I using computer vision and OCR.

Note: This bot only currently works on display 0 with a 1440p game and monitor.

## Game Rules

The game "Ride The Bus" consists of four rounds, each with different rules:

1. **Round 1: Red or Black (2x cashout)**
   - Player guesses if the card will be red (Hearts/Diamonds) or black (Clubs/Spades)
   - Bot strategy: Always bet on Red

2. **Round 2: Higher or Lower (3x cashout)**
   - Player guesses if the next card will be higher or lower than the current card
   - Higher is inclusive (includes cards of equal value)
   - Lower is exclusive (does not include cards of equal value)
   - Bot strategy: Choose option with best probability based on the current card

3. **Round 3: Inside or Outside (4x cashout)**
   - Player guesses if the next card will be inside or outside the range of the two cards shown
   - Inside is inclusive (includes cards of equal value as either boundary card)
   - Outside is exclusive (does not include cards of the same value as boundary cards)
   - Bot strategy: Calculate odds and choose best option

4. **Round 4: Suit (20x cashout)**
   - Player guesses which suit the next card will be
   - Bot strategy: Calculate odds for each suit based on previously seen cards and choose the suit with the highest probability
   - If multiple suits have equal (highest) probability, randomly choose among them

Notes:

- Each round is played with a fresh deck
- Ace is the highest card value
- Player can optionally cash out after each round

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/Cwooper/RideTheBus.git
    cd RideTheBus
    ```

2. Install requirements:

    ```bash
    pip install -r requirements.txt
    ```

3. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Add the Tesseract installation directory to your PATH
   - Edit config.py to point to your Tesseract executable

## Project Structure

```sh
RideTheBus/
├── main.py              # Main program loop
├── card_detection.py    # Card recognition functions
├── game_logic.py        # Decision-making logic
├── ui_interaction.py    # Mouse/keyboard control
├── config.py            # Configuration settings
├── utils.py             # Helper functions
├── requirements.txt     # Package dependencies
├── README.md            # This file
└── Pictures/            # Template images for suit detection
    ├── Diamond.png
    ├── Club.png
    ├── Spades.png
    └── Heart.png
```

## How It Works

### Card Detection

The bot uses a combination of:

1. Template matching with OpenCV to identify card suits
2. Tesseract OCR to read card values (2-10, J, Q, K, A)

### Decision Logic

The bot makes decisions based on probability calculations:

1. **Round 1**: Always bets on Red
2. **Round 2**:
   - Calculates probability of higher/lower based on the first card
   - Accounts for higher being inclusive and lower being exclusive
3. **Round 3**:
   - Calculates probability of inside/outside based on the first two cards
   - Accounts for inside being inclusive and outside being exclusive
4. **Round 4**:
   - Tracks all cards seen in previous rounds
   - Calculates probability for each suit based on remaining cards
   - Chooses the suit with highest probability (randomly breaks ties)

### Usage

1. Configure the pixel positions in config.py:
   - Set the coordinates for card corners
   - Define regions for buttons and win/loss indicators

2. Run the bot:

    ```bash
    python main.py
    ```

3. The terminal will display:
   - Current game state
   - Card detections
   - Probability calculations
   - Decision making process
   - Win/loss tracking

Press Ctrl+C to stop the bot at any time.
