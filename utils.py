# Utility functions

import time
import logging
import os
from datetime import datetime
import cv2


def setup_logging():
    """Set up logging with timestamp"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"ride_the_bus_{timestamp}.log")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )

    logger = logging.getLogger()
    logger.info(f"Logging started at {timestamp}")

    return logger


def log_game_state(game_state):
    """Log the current game state"""
    logging.info(f"Round: {game_state.round}, Balance: ${game_state.balance}")
    if game_state.current_round_cards:
        for i, card in enumerate(game_state.current_round_cards):
            if card and card["value"] and card["suit"]:
                logging.info(f"Card {i+1}: {card['value']} of {card['suit']}")
            else:
                logging.info(f"Card {i+1}: Detection incomplete")


def save_debug_image(image, prefix="debug"):
    """Save an image for debugging purposes"""
    debug_dir = "debug_images"
    os.makedirs(debug_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(debug_dir, f"{prefix}_{timestamp}.png")

    cv2.imwrite(filename, image)
    logging.info(f"Saved debug image: {filename}")

    return filename


def safe_execute(func, *args, max_retries=3, **kwargs):
    """Execute a function with error handling and retries"""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error executing {func.__name__}: {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                time.sleep(1)
            else:
                logging.error(f"Failed after {max_retries} attempts")
                return None


def timing_decorator(func):
    """Decorator to measure execution time"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.debug(
            f"{func.__name__} took {end_time - start_time:.2f} seconds to execute"
        )
        return result

    return wrapper
