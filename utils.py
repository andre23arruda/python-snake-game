import random, os

BLOCK_SIZE = 40
WIDTH = 600
ZERO = 0
WINDOW_SIZE = (600, 600)
BACKGROUND_COLOR = (110, 110, 5)
START_POSITION = 240

def get_random_number(reference_number: int):
    random_number = random.randint(BLOCK_SIZE, WIDTH - BLOCK_SIZE)
    remainder_value = random_number % BLOCK_SIZE
    return random_number - remainder_value

local_path = os.path.dirname(__file__)
