# Card detection functionality

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os
import mss
import mss.tools
from datetime import datetime
from config import *

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def capture_screen():
    """Capture the current screen using mss"""
    with mss.mss() as sct:
        # Use the entire screen
        monitor = sct.monitors[1]
        screen = np.array(sct.grab(monitor))
        # Convert BGRA to BGR (remove alpha channel)
        return screen[:, :, :3]

def save_debug_image(image, filename="debug_card"):
    """Save an image for debugging purposes"""
    debug_dir = "debug_images"
    os.makedirs(debug_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(debug_dir, f"{filename}_{timestamp}.png")
    
    cv2.imwrite(filepath, image)
    # print(f"Saved debug image: {filepath}")
    return filepath

def crop_ocr_region(screen):
    """Crop the OCR region (card value) from the screen using exact coordinates"""
    x1, y1 = OCR_TOP_LEFT
    x2, y2 = OCR_BOTTOM_RIGHT
    return screen[y1:y2, x1:x2]

def crop_suit_region(screen):
    """Crop the suit region from the screen using exact coordinates"""
    x1, y1 = SUIT_TOP_LEFT
    x2, y2 = SUIT_BOTTOM_RIGHT
    return screen[y1:y2, x1:x2]

def detect_card_value(screen):
    """Extract the card value using OCR with exact coordinates"""
    # Crop the OCR region
    ocr_region = crop_ocr_region(screen)
    
    # Convert to grayscale for OCR
    gray = cv2.cvtColor(ocr_region, cv2.COLOR_BGR2GRAY)
    
    # Apply binary threshold for better text extraction
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Use Tesseract to extract text
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=23456789JQKAjqka10'
    text = pytesseract.image_to_string(thresh, config=custom_config).strip()
    
    # Clean up text and map to card value
    text = text.upper().replace(' ', '')
    
    # Handle OCR errors and map to values
    if '1' in text or '0' in text:
        return '10'
    elif any(val in text for val in CARD_VALUES.keys()):
        for val in CARD_VALUES.keys():
            if val in text:
                return val
    
    # Save debug images only on failure
    save_debug_image(ocr_region, "ocr_fail_region")
    save_debug_image(thresh, "ocr_fail_processed")
    
    print(f"Warning: Could not detect card value. OCR text: '{text}'")
    return None

def load_suit_templates():
    """Load the suit template images"""
    templates = {}
    for suit in SUITS:
        template_path = os.path.join(TEMPLATE_DIR, f"{suit}.png")
        if os.path.exists(template_path):
            templates[suit] = cv2.imread(template_path)
        else:
            print(f"Warning: Template for {suit} not found at {template_path}")
    return templates

def detect_card_suit(screen, templates):
    """Detect the card suit using template matching with exact coordinates"""
    # Crop the suit region
    suit_region = crop_suit_region(screen)
    
    # Save the suit region for debugging
    # save_debug_image(suit_region, "suit_region")
    
    best_match = None
    best_score = -1
    
    for suit, template in templates.items():
        # Try different scales of the template for better matching
        for scale in [0.7, 0.85, 1.0, 1.15, 1.3]:
            # Resize the template
            width = int(template.shape[1] * scale)
            height = int(template.shape[0] * scale)
            
            # Skip if the template is too large for the region
            if width > suit_region.shape[1] or height > suit_region.shape[0]:
                continue
                
            resized_template = cv2.resize(template, (width, height), interpolation=cv2.INTER_AREA)
            
            try:
                # Use the template as-is for matching (no preprocessing)
                result = cv2.matchTemplate(suit_region, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)
                
                if max_val > best_score:
                    best_score = max_val
                    best_match = suit
            except Exception as e:
                print(f"Error matching template for {suit} at scale {scale}: {str(e)}")
    
    # Check if match is confident enough
    if best_score > 0.5:  # Lowered threshold for better detection
        return best_match
    
    # Save debug image on failure
    # save_debug_image(suit_region, "suit_fail_region")
    
    print(f"Warning: Could not detect card suit. Best match: {best_match} with score {best_score}")
    return None

def identify_card(screen=None):
    """Identify the card on screen (both value and suit)"""
    if screen is None:
        screen = capture_screen()
    
    # Detect value
    value = detect_card_value(screen)
    # if value:
    #     print(f"Successfully detected card value: {value}")
    
    # Detect suit
    templates = load_suit_templates()
    suit = detect_card_suit(screen, templates)
    # if suit:
    #     print(f"Successfully detected card suit: {suit}")
    
    if value and suit:
        return {'value': value, 'suit': suit, 'numeric_value': CARD_VALUES.get(value)}
    elif value:
        print(f"Partial card detection: Value {value} detected but suit unknown")
        return {'value': value, 'suit': None, 'numeric_value': CARD_VALUES.get(value)}
    elif suit:
        print(f"Partial card detection: Suit {suit} detected but value unknown")
        return {'value': None, 'suit': suit, 'numeric_value': None}
    
    print("Failed to identify card")
    return None
