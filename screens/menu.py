import pygame
import sys
import os

nave_selecionada = ""

def draw_menu(screen, white, selected_ship, ship_images):
    screen.fill(white)

    for i, image in enumerate(ship_images):
        x = (i + 1) * (screen_width // 5) - image.get_width() // 2
        y = screen_height // 2 - image.get_height() // 2
        screen.blit(image, (x, y))

        if selected_ship == i:
            pygame.draw.rect(screen, (255, 0, 0), (x - 5, y - 5, image.get_width() + 10, image.get_height() + 10), 2)

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (0, 0, 0))
    global start_rect
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height - 50))
    pygame.draw.rect(screen, (0, 255, 0),
                     (start_rect.x - 5, start_rect.y - 5, start_rect.width + 10, start_rect.height + 10), 2)
    screen.blit(start_text, start_rect)

    pygame.display.flip()

def load_ship_images():
    ship_paths = [
        "screens/Ships/ship_0000.png",
        "screens/Ships/ship_0001.png",
        "screens/Ships/ship_0002.png",
        "screens/Ships/ship_0003.png"
    ]
    ship_images = [pygame.image.load(path) for path in ship_paths]
    return ship_images, ship_paths

def main():
    global nave_selecionada, selected_ship, screen_width, screen_height

    pygame.init()

    screen_width = 1000
    screen_height = 600
    selected_ship = None

    white = (200, 255, 255)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu de Seleção de Nave")

    ship_images, ship_paths = load_ship_images()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    if selected_ship is not None:
                        print("Você escolheu a nave", selected_ship + 1)
                        print("Caminho da nave selecionada:", nave_selecionada)
                        # Restante do código para iniciar o jogo ou realizar outras ações
                        from screens.planet_earth import Earth
                        running = False
                else:
                    for i, image in enumerate(ship_images):
                        x = (i + 1) * (screen_width // 5) - image.get_width() // 2
                        y = screen_height // 2 - image.get_height() // 2
                        rect = pygame.Rect(x - 5, y - 5, image.get_width() + 10, image.get_height() + 10)
                        if rect.collidepoint(event.pos):
                            nave_selecionada = ship_paths[i]
                            selected_ship = i

        draw_menu(screen, white, selected_ship, ship_images)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
