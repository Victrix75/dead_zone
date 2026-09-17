import pygame

import configuracoes
from sprites import carregar_sprite_inimigo_estado, carregar_sprites_inimigo


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura=70, altura=70, velocidade=45, vida=1, cor=None):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.vida = vida
        self.tempo_ataque = 0.0
        self.bloqueado = False
        self.tempo_animacao = 0.0
        self.tempo_sprite_especial = 0.0
        self.sprite_especial = None
        self.direcao = "esquerda"
        self.cor = cor or configuracoes.COR_INIMIGO
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, self.cor, (0, 0, largura, altura), border_radius=6)
        self.rect = self.image.get_rect(topleft=(x, y))

    def atualizar_sprite(self):
        """Atualiza o frame atual sem alterar o retângulo de colisão."""
        if self.tempo_sprite_especial > 0 and self.sprite_especial:
            self.image = self.sprite_especial[self.direcao]
            return
        imagens = self.sprites.get(self.direcao, [])
        if imagens:
            indice = int(self.tempo_animacao * 8) % len(imagens)
            self.image = imagens[indice]

    def configurar_sprites(self, sprites):
        """Recebe os sprites carregados e mantém o fallback colorido existente."""
        self.sprites = sprites
        self.atualizar_sprite()

    def update(self, dt=1/60):
        if not self.bloqueado:
            self.rect.x -= self.velocidade * dt
        self.tempo_ataque = max(0.0, self.tempo_ataque - dt)
        self.tempo_sprite_especial = max(0.0, self.tempo_sprite_especial - dt)
        self.tempo_animacao += dt if not self.bloqueado else 0
        self.atualizar_sprite()
        tela = pygame.display.get_surface()
        if tela and self.rect.right < 0:
            self.kill()

    def tomar_dano(self, dano):
        self.vida -= dano
        if self.sprites_dano:
            self.sprite_especial = self.sprites_dano
            self.tempo_sprite_especial = 0.2
        if self.vida <= 0:
            self.kill()

    def pode_atacar(self):
        if self.tempo_ataque > 0:
            return False
        self.tempo_ataque = configuracoes.COOLDOWN_ATAQUE_INIMIGO
        self.sprite_especial = self.sprites_ataque
        self.tempo_sprite_especial = 0.25
        return True


class ZumbiBasico(Inimigo):
    def __init__(self, x, y):
        tamanho = configuracoes.TAMANHO_INIMIGO
        super().__init__(
            x=x,
            y=y - tamanho,
            largura=tamanho,
            altura=tamanho,
            velocidade=45,
            vida=1,
            cor=configuracoes.COR_INIMIGO,
        )
        tamanho_sprite = (tamanho, tamanho)
        self.configurar_sprites(carregar_sprites_inimigo(tamanho_sprite))
        self.sprites_ataque = carregar_sprite_inimigo_estado("zumbiataque.png", tamanho_sprite)
        self.sprites_dano = carregar_sprite_inimigo_estado("zumbidano.png", tamanho_sprite)

    def update(self, dt=1/60):
        super().update(dt)
