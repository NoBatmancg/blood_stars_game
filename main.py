from screens.main_menu import Main_menu
from screens.menu import main
from screens.learning_game import Learning_Game
from utils import calculate_screen_center, button_learning_game, button_return
from settings import WINDOW_RESOLUTION
import pygame

run = True

menu_ = Main_menu()
menu_display = menu_.display()
menu_open = True

learning_game = Learning_Game()
learning_game_open = True

while run:
    for event in pygame.event.get():

        if menu_open:
            menu_display = menu_.display_refresh()
            menu_display.blit(menu_.background(), (0,0))
            menu_display.blit(menu_.title(), calculate_screen_center(WINDOW_RESOLUTION, menu_.title()))
            menu_display.blit(button_learning_game(), (10,10))
            learning_game_open = True
            menu_open = False
            
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
            if event.key == pygame.K_ESCAPE:  # Verifica se a tecla pressionada foi o "ESC"
                run = False
            elif learning_game_open == True:
                main()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique do botão esquerdo do mouse
                        if x > 9 and x < 46 and y > 9 and y < 46:  # Defina as coordenadas do botão de transição
                            menu_open = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN: # Verifica o clique do mouse
            if event.button == 1:  # Clique do botão esquerdo do mouse
                x, y = event.pos
                print(f'Posicao do clique {x},{y}')  # Posição do clique

                if x > 9 and x < 46 and y > 9 and y < 46:  # Defina as coordenadas do botão de transição
                    if learning_game_open:
                        learning_game_display = learning_game.display()
                        learning_game_display.blit(learning_game.background(), (0,0)) # Imagem de fundo

                        learning_game_display.blit(button_return(), (10,10)) # Imagem/botão de retorno

                        learning_game_display.blit(learning_game.ship(360), (120,300)) # Imagem nave
                        learning_game_display.blit(learning_game.arrow(90), (166,305)) # Imagem seta
                        learning_game_display.blit(learning_game.arrow(90), (210,305)) # Imagem seta
                        learning_game_display.blit(learning_game.button(90), (160,350)) # imagem botão
                        
                        learning_game_display.blit(learning_game.ship(360), (360,215)) # Imagem nave
                        learning_game_display.blit(learning_game.arrow(360), (365,305)) # Imagem seta
                        learning_game_display.blit(learning_game.arrow(360), (365,270)) # Imagem seta
                        learning_game_display.blit(learning_game.button(360), (360,350)) # imagem botão

                        learning_game_display.blit(learning_game.ship(360), (515,300)) # Imagem nave
                        learning_game_display.blit(learning_game.arrow(180), (520,215)) # Imagem seta
                        learning_game_display.blit(learning_game.arrow(180), (520,260)) # Imagem seta
                        learning_game_display.blit(learning_game.button(180), (515,350)) # imagem botão

                        learning_game_display.blit(learning_game.ship(360), (780,300)) # Imagem nave
                        learning_game_display.blit(learning_game.arrow(270), (745,305)) # Imagem seta
                        learning_game_display.blit(learning_game.arrow(270), (700,305)) # Imagem seta
                        learning_game_display.blit(learning_game.button(270), (740,350))

                        learning_game_open = False
                    else:
                        menu_open = True

    pygame.display.update()