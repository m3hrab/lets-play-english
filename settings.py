import pygame
# Screen Settings settings
WIDTH = 960
HEIGHT = 540
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (150, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
HEADER_COLOR = "#93c808"
QUESTION_COLOR = "#000000"
HOVER_COLOR = "#f7b0cd"
CORRECT_COLOR = (102, 255, 102)     
WRONG_COLOR = (255, 102, 102)       
SUBTITLE_COLOR = RED#"#3b82c6"

# Font sizes 
FONT_LARGE_SIZE = 36
FONT_MEDIUM_SIZE = 24
FONT_SMALL_SIZE = 18

# Game constants
FEEDBACK_DURATION = 30  # 2 seconds at 60 FPS

# Sound 
SOUND_ON = True
# Load sound files
pygame.mixer.init()
CLICK_SOUND = pygame.mixer.Sound("assets/sounds/click.mp3")
CORRECT_SOUND = pygame.mixer.Sound("assets/sounds/correct.mp3")
WRONG_SOUND = pygame.mixer.Sound("assets/sounds/incorrect.mp3")

CLICK_SOUND.set_volume(0.5)  # Set volume to 50%
CORRECT_SOUND.set_volume(0.5)  # Set volume to 50%
WRONG_SOUND.set_volume(0.5)  # Set volume to 50%


