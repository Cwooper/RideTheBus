# Configuration settings for the Ride The Bus bot

import os

# Directory settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "Pictures")

# Tesseract settings
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update with your path

# Card coordinates
CARD_TOP_LEFT = (1176, 532)
CARD_TOP_RIGHT = (1386, 821)

# OCR Region (value detection)
OCR_TOP_LEFT = (1175, 546)
OCR_BOTTOM_RIGHT = (1208, 579)

# Suit Region
SUIT_TOP_LEFT = (1176, 547)
SUIT_BOTTOM_RIGHT = (1208, 613)

# Button coordinates
READY_BUTTON = (1280, 935)
RED_HIGHER_INSIDE_HEARTS_BUTTON = (1280, 1024)
BLACK_LOWER_OUTSIDE_CLUBS_BUTTON = (1280, 1085)
DIAMONDS_BUTTON = (1280, 1143)
SPADES_BUTTON = (1280, 1207)

# Game state detection
OPTION_AVAILABLE_PIXEL = (1408, 1028)
OPTION_AVAILABLE_COLOR1 = (135, 50, 50)
OPTION_AVAILABLE_COLOR2 = (121, 42, 42)
COLOR_TOLERANCE = 20  # RGB tolerance for color matching

# Timeouts and retries
CARD_WAIT_TIME = 1.5  # Fixed seconds to wait for card to appear
MAX_OPTION_WAIT_TIME = 15  # Maximum seconds to wait for options to be available
MAX_READY_ATTEMPTS = 20  # Maximum number of attempts to click Ready button
CHECK_INTERVAL = 0.1  # Time between checks when polling for state changes

# Card values (2-10, J, Q, K, A)
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# Game settings
INITIAL_BALANCE = 0  # Starting balance
BET_AMOUNT = 500  # Amount lost on a loss
WIN_AMOUNT = 10000  # Amount won on completing all rounds

# Card counting
CARDS_PER_DECK = 52
CARDS_PER_SUIT = 13

# Suits
SUITS = ["Diamonds", "Hearts", "Clubs", "Spades"]
RED_SUITS = ["Diamonds", "Hearts"]
BLACK_SUITS = ["Clubs", "Spades"]
