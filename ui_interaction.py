# UI interaction functions

import pyautogui
import time
import numpy as np
import cv2
import mss
from config import *

def click_button(position):
    """Click at the specified position"""
    x, y = position
    pyautogui.click(x, y)

def click_ready():
    """Click the ready button"""
    click_button(READY_BUTTON)

def click_red():
    """Click the Red button (same as Higher/Inside/Hearts)"""
    click_button(RED_HIGHER_INSIDE_HEARTS_BUTTON)

def click_black():
    """Click the Black button (same as Lower/Outside/Clubs)"""
    click_button(BLACK_LOWER_OUTSIDE_CLUBS_BUTTON)

def click_diamonds():
    """Click the Diamonds button"""
    click_button(DIAMONDS_BUTTON)

def click_spades():
    """Click the Spades button"""
    click_button(SPADES_BUTTON)

def click_higher():
    """Click the Higher button (same as Red/Inside/Hearts)"""
    click_button(RED_HIGHER_INSIDE_HEARTS_BUTTON)

def click_lower():
    """Click the Lower button (same as Black/Outside/Clubs)"""
    click_button(BLACK_LOWER_OUTSIDE_CLUBS_BUTTON)

def click_inside():
    """Click the Inside button (same as Red/Higher/Hearts)"""
    click_button(RED_HIGHER_INSIDE_HEARTS_BUTTON)

def click_outside():
    """Click the Outside button (same as Black/Lower/Clubs)"""
    click_button(BLACK_LOWER_OUTSIDE_CLUBS_BUTTON)

def click_hearts():
    """Click the Hearts button (same as Red/Higher/Inside)"""
    click_button(RED_HIGHER_INSIDE_HEARTS_BUTTON)

def click_clubs():
    """Click the Clubs button (same as Black/Lower/Outside)"""
    click_button(BLACK_LOWER_OUTSIDE_CLUBS_BUTTON)

def click_suit(suit):
    """Click the button for the specified suit"""
    if suit == "Hearts":
        click_hearts()
    elif suit == "Diamonds":
        click_diamonds()
    elif suit == "Clubs":
        click_clubs()
    elif suit == "Spades":
        click_spades()
    else:
        print(f"Unknown suit: {suit}")

def get_pixel_color(x, y, screen=None):
    """Get the RGB color of a pixel on screen"""
    if screen is None:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screen = np.array(sct.grab(monitor))
    
    # Get the pixel color (BGR format)
    pixel_color = screen[y, x, :3]
    
    # Convert to RGB
    r, g, b = pixel_color[2], pixel_color[1], pixel_color[0]
    return (r, g, b)

def color_matches(color1, color2, tolerance=COLOR_TOLERANCE):
    """Check if two colors match within a tolerance"""
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

def is_option_available(screen=None):
    """Check if the next option is available by checking the pixel color"""
    x, y = OPTION_AVAILABLE_PIXEL
    pixel_color = get_pixel_color(x, y, screen)
    
    # Check if the color matches either of the two target colors
    return (color_matches(pixel_color, OPTION_AVAILABLE_COLOR1) or
            color_matches(pixel_color, OPTION_AVAILABLE_COLOR2))

def wait_for_option_available(timeout=15, check_interval=0.1):
    """Wait until options are available or timeout is reached"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if is_option_available():
            return True
        time.sleep(check_interval)
    
    return False

def wait_for_card_to_appear():
    """Wait a fixed 1.5 seconds for the card to appear"""
    time.sleep(1.5)
    return True

def capture_screen():
    """Capture the current screen using MSS"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen = np.array(sct.grab(monitor))
        # Convert BGRA to BGR (remove alpha channel)
        return screen[:, :, :3]
    