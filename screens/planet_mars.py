import pygame
import random
import math
import sys
from screens.menu import nave_selecionada

# from settings import WINDOW_RESOLUTION
WINDOW_RESOLUTION = (1000, 600)
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('screens/shot.wav')
collision_sound = pygame.mixer.Sound('screens/som_explosion.wav')
pygame.mixer.music.load('screens/trilhasonora.wav')
pygame.mixer.music.set_volume(1.5)
pygame.mixer.music.play(-1)


class MascaraSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale_factor):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, scale_factor)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, self.rect)


class Explosao(MascaraSprite):
    def __init__(self, x, y):
        explosao_frames = [
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
        super().__init__(explosao_frames[0], (256, 256))
        self.images = [pygame.image.load(frame) for frame in explosao_frames]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect.center = (x, y)
        self.frame = 0
        self.frames_por_segundo = 10
        self.animacao_frames = len(self.images)

    def update(self):
        self.frame += 1
        if self.frame % (self.frames_por_segundo // 2) == 0:
            self.image_index += 1
            if self.image_index >= len(self.images):
                return True  # Indica que a animação deve ser removida
            self.image = self.images[self.image_index]
        return False


def limpar():
    pygame.quit()


class Marte:
    def __init__(self):
        self.nome_da_janela = 'Planeta Marte'
        self.bg_x = 0
        self.player = Player()
        self.inimigos = []
        self.projeteis = []
        self.projeteis_inimigo = []
        self.explosoes = []
        self.game_over = False  # Adiciona a variável de controle do estado Game Over
        self.tempo_espera_explosao = 0
        self.estado_espera_explosao = False
        self.tela_de_vitoria = False

    def criar_inimigo(self, x, y, tipo_de_inigo):
        if tipo_de_inigo == 'normal':
            inimigo = Inimigo(x, y)
        elif tipo_de_inigo == 'special':
            inimigo = InimigoEspecial(x, y)
        else:
            inimigo = NovoInimigo(x, y)
            inimigo.original_y = y
        self.inimigos.append(inimigo)

    def checar_colisao(self):
        for inimigo in self.inimigos[:]:
            if self.player.rect.colliderect(inimigo.rect) and pygame.sprite.collide_mask(self.player, inimigo):
                self.inimigos.remove(inimigo)
                self.player.vida -= 0.1
                self.criar_esplosao(inimigo.rect.centerx, inimigo.rect.centery)
                collision_sound.play()

        for projetil_inimigo in self.projeteis_inimigo[:]:
            if self.player.rect.colliderect(projetil_inimigo.rect) and pygame.sprite.collide_mask(self.player,
                                                                                                  projetil_inimigo):
                self.projeteis_inimigo.remove(projetil_inimigo)
                self.player.vida -= 0.1

        for projetil in self.projeteis[:]:
            for enemy in self.inimigos[:]:
                if projetil.rect.colliderect(enemy.rect) and pygame.sprite.collide_mask(projetil, enemy):
                    if projetil in self.projeteis:
                        self.projeteis.remove(projetil)
                        enemy.vida -= 1
                    if enemy.vida <= 0:
                        self.inimigos.remove(enemy)
                        self.criar_esplosao(enemy.rect.centerx, enemy.rect.centery)
                        collision_sound.play()
                        self.player.pontuacao += 10  # Aumenta a pontuação ao derrotar um inimigo

            if projetil.colidiu:
                self.projeteis.remove(projetil)

    def criar_esplosao(self, x, y):
        explosao = Explosao(x, y)
        self.explosoes.append(explosao)

    def display(self):
        pygame.init()
        window = pygame.display.set_mode(WINDOW_RESOLUTION)
        pygame.display.set_caption(self.nome_da_janela)

        background_image = pygame.image.load('screens/imagensMarte/Marte_2.jpg')
        background_image = pygame.transform.scale(background_image, WINDOW_RESOLUTION)
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not self.tela_de_vitoria:
                if not self.game_over:
                    self.bg_x -= 2
                    if self.bg_x < -background_image.get_width():
                        self.bg_x = 0

                    window.blit(background_image, (self.bg_x, 0))
                    window.blit(background_image, (self.bg_x + background_image.get_width(), 0))

                    self.player.update()
                    self.player.draw(window)

                    for inimigo in self.inimigos:
                        inimigo.update()
                        inimigo.draw(window)

                        if random.randint(0, 100) < 2:
                            inimigo.atirar()

                    for projetil in self.projeteis:
                        projetil.update()
                        projetil.draw(window)

                        if projetil.rect.x >= WINDOW_RESOLUTION[0]:
                            projetil.colidiu = True

                    for projetil_inimigo in self.projeteis_inimigo:
                        projetil_inimigo.update()
                        projetil_inimigo.draw(window)

                        if projetil_inimigo.rect.x <= 0:
                            projetil_inimigo.colidiu = True

                    for explosao in self.explosoes:
                        if explosao.update():
                            self.explosoes.remove(explosao)
                        else:
                            explosao.draw(window)

                    self.player.atualizar_barra_vida(window)
                    self.player.atualizar_pontuacao(window)

                    self.checar_colisao()

                    self.projeteis = [projetil for projetil in self.projeteis if not projetil.colidiu]
                    self.projeteis_inimigo = [projetil_inimigo for projetil_inimigo in self.projeteis_inimigo if
                                              not projetil_inimigo.colidiu]

                    self.inimigos = [inimigo for inimigo in self.inimigos if inimigo.rect.x > -150]

                    if len(self.inimigos) < maximo_de_inimigos and random.randint(0, 100) < 2:
                        x = WINDOW_RESOLUTION[0]
                        y = random.randint(0, WINDOW_RESOLUTION[1] - 150)
                        tipo_de_inimigo = random.choice(['normal', 'special', 'new'])
                        self.criar_inimigo(x, y, tipo_de_inimigo)

                    pygame.display.update()
                    clock.tick(60)

                else:
                    self.exibir_tela_game_over(window)
            else:
                tela_vitoria = TelaVitoria(window)
                tela_vitoria.exibir_tela_vitoria()
                tela_vitoria.processar_eventos()

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
        self.inimigos = []
        self.projeteis = []
        self.projeteis_inimigo = []
        self.explosoes = []
        self.bg_x = 0
        self.tela_de_vitoria = False

    def criar_explosao_do_jogador(self, x, y):
        explosao = Explosao(x, y)
        self.explosoes.append(explosao)


class Player(MascaraSprite):
    def __init__(self):

        super().__init__(nave_selecionada, (50, 50))
        self.rect.center = (WINDOW_RESOLUTION[0] // 2, WINDOW_RESOLUTION[1] - 50)
        self.velocidade_x = 5
        self.esfriar_projetil = 0
        self.vida = 3
        self.pontuacao = 0

    def atirar(self):
        if self.esfriar_projetil <= 0:
            projetil_direita = Projetil(self.rect.centerx + 45, self.rect.centery - 20)
            projetil_esquerda = Projetil(self.rect.centerx + 45, self.rect.centery + 20)

            marte.projeteis.append(projetil_direita)
            marte.projeteis.append(projetil_esquerda)

            self.esfriar_projetil = 30
            shoot_sound.play()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocidade_x
        if keys[pygame.K_RIGHT] and self.rect.x < WINDOW_RESOLUTION[0] - self.rect.width:
            self.rect.x += self.velocidade_x
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocidade_x

        if keys[pygame.K_DOWN] and self.rect.y < WINDOW_RESOLUTION[1] - self.rect.height:
            self.rect.y += self.velocidade_x
        if keys[pygame.K_SPACE]:
            self.atirar()

        if self.esfriar_projetil > 0:
            self.esfriar_projetil -= 1
        if self.vida <= 0:
            marte.criar_explosao_do_jogador(self.rect.centerx, self.rect.centery)
            marte.game_over = True

        if self.pontuacao >= 100:
            marte.tela_de_vitoria = True

    def draw(self, window):

        # window.blit(self.nave_sprite_animado, (self.rect.x, self.rect.y), (self.x_sprite_mover * 192, 0, 192, 192))

        window.blit(self.image, (self.rect.x, self.rect.y))

    def atualizar_barra_vida(self, window):
        pygame.draw.rect(window, (255, 0, 0), (10, 10, self.vida * 30, 20))  # Barra de vida vermelha
        pygame.draw.rect(window, (0, 255, 0), (10, 10, 3 * 30, 20), 2)  # Contorno verde

    def atualizar_pontuacao(self, window):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.pontuacao}", True, (255, 255, 255))
        window.blit(score_text, (WINDOW_RESOLUTION[0] - 150, 10))


class Inimigo(MascaraSprite):
    def __init__(self, x, y):
        super().__init__('screens/Ships/ship_0007.png', (50, 50))
        self.rect.center = (x, y)
        self.velocidade_x = 1
        self.vida = 1
        self.float_offset = 0
        self.posicao_original_y = y
        self.x_sprite_mover = 0

        # Crie uma superfície para a propulsão em formato de tocha de fogo
        self.propulsao_frames = [
            'screens/naves/Ship3/Exhaust/Turbo_flight/Exhaust1/exhaust1.png',
            'screens/naves/Ship3/Exhaust/Turbo_flight/Exhaust1/exhaust2.png',
            'screens/naves/Ship3/Exhaust/Turbo_flight/Exhaust1/exhaust3.png',
            'screens/naves/Ship3/Exhaust/Turbo_flight/Exhaust1/exhaust4.png',
            # Adicione mais caminhos de imagem conforme necessário
        ]
        self.propulsao_index = 0
        self.propulsao_image = pygame.image.load(self.propulsao_frames[self.propulsao_index])
        self.frame_counter = 0

    def update_propulsao(self):
        self.frame_counter += 1
        if self.frame_counter % 5 == 0:  # Altere esse valor para ajustar a velocidade da animação
            self.propulsao_index = (self.propulsao_index + 1) % len(self.propulsao_frames)
            self.propulsao_image = pygame.image.load(self.propulsao_frames[self.propulsao_index])

    def update(self):
        self.rect.x -= self.velocidade_x
        self.rect.y = self.posicao_original_y + math.sin(self.float_offset) * 20
        self.float_offset += 0.1
        self.update_propulsao()  # Chama o método de atualização da propulsão

    def draw(self, window):
        # window.blit(self.image, self.rect)
        window.blit(self.propulsao_image, (self.rect.x + 35, self.rect.y - 5))
        window.blit(self.image, self.rect)

    def atirar(self):
        projetil = ProjetilInimigo(self.rect.centerx, self.rect.centery)
        marte.projeteis_inimigo.append(projetil)


class InimigoEspecial(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('screens/Ships/ship_0008.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 1
        self.vida = 3


class NovoInimigo(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('screens/Ships/ship_0009.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade_x = 1
        self.vida = 1


class Projetil(MascaraSprite):
    def __init__(self, x, y):
        super().__init__('screens/Tiles/tile_0000.png', (16, 16))
        self.rect.center = (x, y)
        self.velocidade_x = 10
        self.colidiu = False

    def update(self):
        self.rect.x += self.velocidade_x


class ProjetilInimigo(Projetil):
    def update(self):
        self.rect.x -= self.velocidade_x


class TelaVitoria:
    def __init__(self, window):
        self.window = window
        self.fonte = pygame.font.Font(None, 50)
        self.fonte_botao = pygame.font.Font(None, 32)

    def exibir_tela_vitoria(self):

        texto_vitoria = self.fonte.render("Missão de destino completa com sucesso", True, (0, 0, 255))
        self.window.blit(texto_vitoria, (WINDOW_RESOLUTION[0] // 2 - 350, WINDOW_RESOLUTION[1] // 2 - 50))

        score_text = self.fonte_botao.render(f"Pontuação: {marte.player.pontuacao}", True, (0, 0, 255))
        self.window.blit(score_text, (WINDOW_RESOLUTION[0] // 2 - 80, WINDOW_RESOLUTION[1] // 2 + 20))

        # Adicione botões para jogar novamente e encerrar o jogo
        pygame.draw.rect(self.window, (0, 255, 0),
                         (WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 80, 200, 50))
        pygame.draw.rect(self.window, (255, 0, 0),
                         (WINDOW_RESOLUTION[0] // 2 - 100, WINDOW_RESOLUTION[1] // 2 + 140, 200, 50))

        play_again_text = self.fonte_botao.render("Jogar Novamente", True, (0, 0, 0))
        quit_text = self.fonte_botao.render("Sair", True, (0, 0, 0))
        self.window.blit(play_again_text, (WINDOW_RESOLUTION[0] // 2 - 95, WINDOW_RESOLUTION[1] // 2 + 95))
        self.window.blit(quit_text, (WINDOW_RESOLUTION[0] // 2 - 30, WINDOW_RESOLUTION[1] // 2 + 155))

        pygame.display.update()

    def processar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (WINDOW_RESOLUTION[0] // 2 - 100) <= mouse_x <= (WINDOW_RESOLUTION[0] // 2 + 100):
                    if (WINDOW_RESOLUTION[1] // 2 + 80) <= mouse_y <= (WINDOW_RESOLUTION[1] // 2 + 130):
                        # Clicou em "Jogar Novamente"
                        marte.reiniciar_jogo()
                    elif (WINDOW_RESOLUTION[1] // 2 + 140) <= mouse_y <= (WINDOW_RESOLUTION[1] // 2 + 190):
                        # Clicou em "Sair"
                        pygame.quit()
                        sys.exit()

maximo_de_inimigos = 30
marte = Marte()
marte.display()
