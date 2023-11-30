import sys
import pygame
import random
import math
from screens.menu import nave_selecionada

WINDOW_RESOLUTION = (1000, 600)
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('screens/shot.wav')
collision_sound = pygame.mixer.Sound('screens/som_explosion.wav')
pygame.mixer.music.load('screens/trilhasonora.wav')
pygame.mixer.music.set_volume(1.5)
pygame.mixer.music.play(-1)


class MaskedSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale_factor):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale_factor)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, self.rect)


class Explosion(MaskedSprite):
    def __init__(self, x, y):
        explosion_frames = [
            'screens/Explosion/Explosion1.png',
            'screens/Explosion/Explosion2.png',
            'screens/Explosion/Explosion3.png',
            'screens/Explosion/Explosion4.png',
            'screens/Explosion/Explosion5.png',
            'screens/Explosion/Explosion6.png',
            'screens/Explosion/Explosion7.png',
            'screens/Explosion/Explosion8.png',
            'screens/Explosion/Explosion9.png',
            'screens/Explosion/Explosion10.png',
            # Adicione mais caminhos de imagem conforme necessário
        ]
        super().__init__(explosion_frames[0], (256, 256))
        self.images = [pygame.image.load(frame) for frame in explosion_frames]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect.center = (x, y)
        self.frame = 0
        self.frames_per_second = 10
        self.animation_frames = len(self.images)

    def update(self):
        self.frame += 1
        if self.frame % (self.frames_per_second // 2) == 0:
            self.image_index += 1
            if self.image_index >= len(self.images):
                return True  # Indica que a animação deve ser removida
            self.image = self.images[self.image_index]
        return False


def cleanup():
    pygame.quit()


class Earth:
    def __init__(self):
        self.window_name = 'Terra'
        self.bg_x = 0
        self.player = Player()
        self.enemies = []
        self.projectiles = []
        self.enemy_projectiles = []
        self.explosions = []
        self.game_over = False
        self.NEXT_LEVEL_SCORE = 50  # Defina a pontuação necessária para passar de fase
        self.next_level_unlocked = False
        self.next_level_reached = False

    def create_enemy(self, x, y, enemy_type):
        if enemy_type == 'normal':
            enemy = Enemy(x, y)
        elif enemy_type == 'special':
            enemy = SpecialEnemy(x, y)
        else:
            enemy = NewEnemy(x, y)
            enemy.original_y = y
        self.enemies.append(enemy)

    def check_collisions(self):
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect) and pygame.sprite.collide_mask(self.player, enemy):
                self.enemies.remove(enemy)
                self.player.life -= 0.1
                self.create_explosion(enemy.rect.centerx, enemy.rect.centery)
                collision_sound.play()

        for enemy_projectile in self.enemy_projectiles[:]:
            if self.player.rect.colliderect(enemy_projectile.rect) and pygame.sprite.collide_mask(self.player,
                                                                                                  enemy_projectile):
                self.enemy_projectiles.remove(enemy_projectile)
                self.player.life -= 0.1
                collision_sound.play()

        for projectile in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect) and pygame.sprite.collide_mask(projectile, enemy):
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                        enemy.life -= 1
                    if enemy.life <= 0:
                        self.enemies.remove(enemy)
                        self.create_explosion(enemy.rect.centerx, enemy.rect.centery)
                        collision_sound.play()
                        self.player.score += 10  # Aumenta a pontuação ao derrotar um inimigo

            if projectile.collided:
                self.projectiles.remove(projectile)

    def create_explosion(self, x, y):
        explosion = Explosion(x, y)
        self.explosions.append(explosion)

    def display(self):
        pygame.init()
        window = pygame.display.set_mode(WINDOW_RESOLUTION)
        pygame.display.set_caption(self.window_name)

        background_image = pygame.image.load('screens/backgroud_terra.jpeg')
        background_image = pygame.transform.scale(background_image, WINDOW_RESOLUTION)

        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not self.next_level_reached:
                if not self.game_over:
                    self.bg_x -= 2
                    if self.bg_x < -background_image.get_width():
                        self.bg_x = 0

                    window.blit(background_image, (self.bg_x, 0))
                    window.blit(background_image, (self.bg_x + background_image.get_width(), 0))

                    self.player.update()
                    self.player.draw(window)

                    for enemy in self.enemies:
                        enemy.update()
                        enemy.draw(window)

                        if random.randint(0, 100) < 2:
                            enemy.shoot()

                    for projectile in self.projectiles:
                        projectile.update()
                        projectile.draw(window)

                        if projectile.rect.x >= WINDOW_RESOLUTION[0]:
                            projectile.collided = True

                    for enemy_projectile in self.enemy_projectiles:
                        enemy_projectile.update()
                        enemy_projectile.draw(window)

                        if enemy_projectile.rect.x <= 0:
                            enemy_projectile.collided = True

                    for explosion in self.explosions:
                        if explosion.update():
                            self.explosions.remove(explosion)
                        else:
                            explosion.draw(window)

                    # linhas para renderizar a barra de vida e a pontuação
                    self.check_collisions()
                    self.player.update_life_bar(window)
                    self.player.update_score(window)

                    self.check_collisions()

                    self.projectiles = [projectile for projectile in self.projectiles if not projectile.collided]
                    self.enemy_projectiles = [enemy_projectile for enemy_projectile in self.enemy_projectiles if
                                              not enemy_projectile.collided]

                    self.enemies = [enemy for enemy in self.enemies if enemy.rect.x > -150]

                    if len(self.enemies) < MAX_ENEMIES and random.randint(0, 100) < 2:
                        x = WINDOW_RESOLUTION[0]
                        y = random.randint(0, WINDOW_RESOLUTION[1] - 150)
                        enemy_type = random.choice(['normal', 'special', 'new'])
                        self.create_enemy(x, y, enemy_type)
                    if not self.game_over and self.next_level_unlocked:
                        self.display_next_level_screen(window)
                        self.next_level_unlocked = False
                    # Verifica se o jogador atingiu a pontuação necessária para passar de fase
                    if self.player.score >= self.NEXT_LEVEL_SCORE and not self.next_level_reached:
                        self.next_level_reached = True
                        self.next_level_unlocked = True

                    pygame.display.update()
                    clock.tick(60)
                else:
                    self.exibir_tela_game_over(window)
            else:
                self.display_next_level_screen(window)
        pygame.quit()
        sys.exit()

    def exibir_tela_game_over(self, window):
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, (0, 0, 255))
        window.blit(game_over_text, (WINDOW_RESOLUTION[0] // 2 - 150, WINDOW_RESOLUTION[1] // 2 - 50))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.player.pontuacao}", True, (0, 0, 255))
        window.blit(score_text, (WINDOW_RESOLUTION[0] // 2 - 70, WINDOW_RESOLUTION[1] // 2 + 20))

        # Adicione botões para jogar novamente e encerrar o jogo
        pygame.draw.rect(window, (0, 255, 0),
                         (WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 80, 200, 50))
        pygame.draw.rect(window, (255, 0, 0),
                         (WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 140, 200, 50))

        font = pygame.font.Font(None, 36)
        play_again_text = font.render("Play Again", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))
        window.blit(play_again_text, (WINDOW_RESOLUTION[0] // 2 - 60, WINDOW_RESOLUTION[1] // 2 + 95))
        window.blit(quit_text, (WINDOW_RESOLUTION[0] // 2 - 30, WINDOW_RESOLUTION[1] // 2 + 155))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (WINDOW_RESOLUTION[0] // 2 - 100) <= mouse_x <= (WINDOW_RESOLUTION[0] // 2 + 100):
                    if (WINDOW_RESOLUTION[1] // 2 + 80) <= mouse_y <= (WINDOW_RESOLUTION[1] // 2 + 130):
                        # Clicou em "Play Again"
                        self.reiniciar_jogo()
                    elif (WINDOW_RESOLUTION[1] // 2 + 140) <= mouse_y <= (WINDOW_RESOLUTION[1] // 2 + 190):
                        # Clicou em "Quit"
                        pygame.quit()
                        sys.exit()

    def reiniciar_jogo(self):
        # Reinicializa as variáveis de jogo para recomeçar
        self.game_over = False
        self.player = Player()
        self.enemies = []
        self.projectiles = []
        self.enemy_projectiles = []
        self.explosions = []
        self.bg_x = 0
        self.next_level_reached = False
        self.next_level_unlocked = False

    def display_next_level_screen(self, window):
        pygame.mixer.music.pause()  # Pausa a música de fundo
        font = pygame.font.Font(None, 74)
        congrats_text = font.render("Parabéns, você passou de fase!", True, (0, 0, 255))
        window.blit(congrats_text, (WINDOW_RESOLUTION[0] // 2 - 300, WINDOW_RESOLUTION[1] // 2 - 50))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, (0, 0, 255))
        window.blit(score_text, (WINDOW_RESOLUTION[0] // 2 - 70, WINDOW_RESOLUTION[1] // 2 + 20))

        # Adicione botões para jogar a próxima fase e sair do jogo
        pygame.draw.rect(window, (0, 255, 0),
                         (WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 80, 200, 50))
        pygame.draw.rect(window, (255, 0, 0),
                         (WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 140, 200, 50))

        font = pygame.font.Font(None, 36)
        next_level_text = font.render("Próxima Fase", True, (0, 0, 0))
        quit_text = font.render("Quit", True, (0, 0, 0))
        window.blit(next_level_text, (WINDOW_RESOLUTION[0] // 2 - 60, WINDOW_RESOLUTION[1] // 2 + 95))
        window.blit(quit_text, (WINDOW_RESOLUTION[0] // 2 - 30, WINDOW_RESOLUTION[1] // 2 + 155))

        pygame.display.update()

        # Aguarde o jogador fazer uma escolha
        choice_made = False
        while not choice_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Retificando as coordenadas do botão
                    button_next_level = pygame.Rect(WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 80,
                                                    200, 50)
                    button_quit = pygame.Rect(WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 140, 200, 50)
                    if button_next_level.collidepoint(mouse_x, mouse_y):
                        # Clicou em "Próxima Fase"
                        choice_made = True
                        from screens.galaxy import Galaxy

                    elif button_quit.collidepoint(mouse_x, mouse_y):
                        # Clicou em "Quit"
                        pygame.quit()
                        sys.exit()


class Player(MaskedSprite):
    def __init__(self):
        super().__init__(nave_selecionada, (50, 50))
        self.pontuacao = 0
        self.rect.center = (WINDOW_RESOLUTION[0] // 2, WINDOW_RESOLUTION[1] - 50)
        self.speed_x = 5
        self.projectile_cooldown = 0
        self.life = 3
        self.score = 0
        self.rotacao = 0
        self.progelil = Projectile

    def shoot(self):
        if self.projectile_cooldown <= 0:
            projectile = Projectile(self.rect.centerx, self.rect.centery)
            earth.projectiles.append(projectile)
            self.projectile_cooldown = 30
            shoot_sound.play()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT] and self.rect.x < WINDOW_RESOLUTION[0] - self.rect.width:
            self.rect.x += self.speed_x
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed_x
        if keys[pygame.K_DOWN] and self.rect.y < WINDOW_RESOLUTION[1] - self.rect.height:
            self.rect.y += self.speed_x
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_w]:
            if self.rotacao == 0:
                self.rotacao += 90
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 90

            if self.rotacao == 180:
                self.rotacao -= 270
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 90
            if self.rotacao == 270:
                self.rotacao -= 90
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 90
        if keys[pygame.K_a]:
            if self.rotacao == 0:
                self.rotacao += 180
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 180
            if self.rotacao == 90:
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 180
            if self.rotacao == 270:

                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 180
        if keys[pygame.K_s]:
            if self.rotacao == 0:
                self.rotacao += 270
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 270
            if self.rotacao == 90:
                self.rotacao += 90
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 270
            if self.rotacao == 180:
                self.rotacao -= 90
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 270
        if keys[pygame.K_d]:
            if self.rotacao == 270:
                self.rotacao -= 180
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 0
            if self.rotacao == 180:

                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 0
            if self.rotacao == 90:
                self.rotacao -= 180
                self.image = pygame.transform.rotate(self.image, self.rotacao)
                self.rotacao = 0

        '''self.image = pygame.transform.rotate(self.image, self.rotacao)'''


        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        if self.life <= 0:
            earth.game_over = True

    def draw(self, window):
        window.blit(self.image, self.rect)

    def update_life_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (10, 10, self.life * 30, 20))  # Barra de vida vermelha
        pygame.draw.rect(window, (0, 255, 0), (10, 10, 3 * 30, 20), 2)  # Contorno verde

    def update_score(self, window):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        window.blit(score_text, (WINDOW_RESOLUTION[0] - 150, 10))


class Enemy(MaskedSprite):
    def __init__(self, x, y):
        super().__init__('screens\imageTerra\monster_blue.gif', (60, 60))
        self.rect.center = (x, y)
        self.speed_x = 1
        self.life = 1
        self.float_offset = 0
        self.original_y = y

    def update(self):
        self.rect.x -= self.speed_x
        self.rect.y = self.original_y + math.sin(self.float_offset) * 20
        self.float_offset += 0.1

    def draw(self, window):
        window.blit(self.image, self.rect)

    def shoot(self):
        projectile = EnemyProjectile(self.rect.centerx, self.rect.centery)
        earth.enemy_projectiles.append(projectile)


class SpecialEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('screens\imageTerra\monster_yellow.gif')
        self.image = pygame.transform.scale(self.image, (65, 65))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 1
        self.life = 3


class NewEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('screens\imageTerra\monster_blue.gif')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 1
        self.life = 1


class Projectile(MaskedSprite):
    def __init__(self, x, y):
        super().__init__('screens\imageTerra\_tile_0003.png', (20, 20))
        self.rect.center = (x, y)
        self.speed_x = 10
        self.collided = False

    def update(self):
        self.rect.x += self.speed_x


class EnemyProjectile(Projectile):
    def update(self):
        self.rect.x -= self.speed_x



MAX_ENEMIES = 10
earth = Earth()
earth.display()