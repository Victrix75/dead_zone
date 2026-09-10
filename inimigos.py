import pygame

import configuracoes


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura=70, altura=70, velocidade=45, vida=1, cor=None):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.vida = vida
        self.cor = cor or configuracoes.COR_INIMIGO
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, self.cor, (0, 0, largura, altura), border_radius=6)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt=1/60):
        self.rect.x -= self.velocidade * dt
        tela = pygame.display.get_surface()
        if tela and self.rect.right < 0:
            self.kill()

    def tomar_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.kill()


class ZumbiBasico(Inimigo):
    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y - 70,
            largura=70,
            altura=70,
            velocidade=45,
            vida=1,
            cor=configuracoes.COR_INIMIGO,
        )

    def update(self, dt=1/60):
        super().update(dt)
