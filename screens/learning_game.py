import pygame
from settings import WINDOW_RESOLUTION
from pygame.sprite import Sprite

class Learning_Game(Sprite):
    def __init__(self):
        self.window_name = 'Aprenda a Jogar'

    def display(self):
        display = pygame.display.set_mode(WINDOW_RESOLUTION)
        pygame.display.set_caption(self.window_name)
        return display
    
    def background(self):
        image_background = pygame.image.load('screens\images\menu_&_learning_game_background.jpeg').convert_alpha()
        image_background = pygame.transform.scale(image_background, WINDOW_RESOLUTION)
        return image_background
    
    def button(self, angle):
        image_button_up = pygame.image.load('screens\images\learning_game_button.png').convert_alpha()
        image_button_up = pygame.transform.scale(image_button_up, (50,50))
        image_button_up = pygame.transform.rotate(image_button_up, angle)
        return image_button_up
    
    def ship(self, angle):
        image_ship_yellow = pygame.image.load('screens\images\learning_game_ship_yellow.png').convert_alpha()
        image_ship_yellow = pygame.transform.scale(image_ship_yellow, (50,50))
        image_ship_yellow = pygame.transform.rotate(image_ship_yellow, angle)
        return image_ship_yellow
    
    def arrow(self, angle):
        image_arrow = pygame.image.load('screens\images\learning_game_arrow.png').convert_alpha()
        image_arrow = pygame.transform.scale(image_arrow, (40,40))
        image_arrow = pygame.transform.rotate(image_arrow, angle)
        return image_arrow
   