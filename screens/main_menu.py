import pygame
from settings import WINDOW_RESOLUTION
from pygame.sprite import Sprite

class Main_menu(Sprite):
    def __init__(self):
        self.window_name = 'Menu Principal'

    def display(self):
        pygame.init()
        display = pygame.display.set_mode(WINDOW_RESOLUTION)
        pygame.display.set_caption(self.window_name)
        return display

    def display_refresh(self):
        display = pygame.display.set_mode(WINDOW_RESOLUTION)
        pygame.display.set_caption(self.window_name)
        return display
    
    def background(self):
        image_background = pygame.image.load('screens\images\menu_&_learning_game_background.jpeg').convert_alpha()
        image_background = pygame.transform.scale(image_background, WINDOW_RESOLUTION)
        return image_background
    
    def title(self):
        # Link para fonte https://fontmeme.com/pixel-fonts/
        image_title = pygame.image.load('screens\images\menu_title.png').convert_alpha()
        image_title = pygame.transform.scale(image_title, (624,30))
        return image_title
