import random

import pygame

import configuracoes
from entidades.personagem import Jogador
from entidades.projetil import Tiro


class Robo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(configuracoes.COR_INIMIGO)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 3
        self.direcao = 1

    def update(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3
        tela = pygame.display.get_surface()
        if self.rect.left <= 0 or self.rect.right >= tela.get_width():
            self.direcao *= -1
        if self.rect.top > tela.get_height():
            self.kill()


def main():
    pygame.init()
    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(configuracoes.TITULO)
    relogio = pygame.time.Clock()
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()
    jogador = Jogador(tela.get_width() // 2, tela.get_height() - 80)
    todos_sprites.add(jogador)
    pontos = 0
    spawn_timer = 0
    rodando = True

    while rodando:
        relogio.tick(configuracoes.FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_SPACE:
                    tiro = Tiro(jogador.rect.centerx, jogador.rect.top)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)

        spawn_timer += 1
        if spawn_timer > 40:
            robo = Robo(random.randint(40, tela.get_width() - 40), -40)
            todos_sprites.add(robo)
            inimigos.add(robo)
            spawn_timer = 0

        pontos += len(pygame.sprite.groupcollide(inimigos, tiros, True, True))
        if pygame.sprite.spritecollide(jogador, inimigos, True):
            jogador.tomar_dano(1)
            if not jogador.vivo:
                rodando = False

        todos_sprites.update()
        tela.fill(configuracoes.BG_COR)
        todos_sprites.draw(tela)
        fonte = pygame.font.Font(None, 30)
        texto = fonte.render(
            f"Vida: {jogador.vida}  |  Pontos: {pontos}",
            True,
            configuracoes.COR_TEXTO,
        )
        tela.blit(texto, (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()