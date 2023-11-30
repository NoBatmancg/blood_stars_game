import pygame

def calculate_screen_center(screen_resolution, image):
    tela_largura, tela_altura = screen_resolution
    
    x = (tela_largura - image.get_width()) // 2
    y = (tela_altura - image.get_height()) // 2
    
    return (x,y)

def button_learning_game():
        image_learning_game = pygame.image.load('screens\images\learning_game.png').convert_alpha()
        image_learning_game = pygame.transform.scale(image_learning_game, (35,35))
        return image_learning_game

def button_return():
        image_learning_game = pygame.image.load('screens\images\\return.png').convert_alpha()
        image_learning_game = pygame.transform.scale(image_learning_game, (35,35))
        return image_learning_game