from abc import ABC, abstractmethod
import pygame
import configuracoes
from sprites import (
    carregar_sprites_jogador,
    carregar_sprites_morte_jogador,
    carregar_sprite_powerup_cooldown,
    carregar_sprite_tiro,
    carregar_sprite_dano,
)


class Personagem(pygame.sprite.Sprite, ABC):

    def __init__(self,
                 x,
                 y,
                 largura,
                 altura,
                 vida):
        super().__init__()
        self.largura,self.altura = largura,altura
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, largura, altura)
        # A hitbox menor deixa a colisão mais justa sem reduzir o sprite.
        margem = configuracoes.MARGEM_COLISAO_JOGADOR
        self.hitbox = self.rect.inflate(-margem, -margem)
        self.maximo_vidas = vida
        self.vidas = vida
        self.vida = vida
        self.vivo = True
        self.contato_dano = 1
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.image.fill(configuracoes.COR_JOGADOR)

    @abstractmethod
    def update(self, *args,**kwargs):
        pass

    def tomar_dano(self,dano,contra_ataque=(0,0)):
        if not self.vivo:
            return
        self.vida -= dano
        self.vidas = self.vida
        # Ativa o timer de exibição do sprite de dano (se suportado pelo personagem)
        if hasattr(self, "_DANO_MOSTRAR"):
            self._dano_timer = self._DANO_MOSTRAR
        else:
            self._dano_timer = 20
        if self.vida <=0:
            self.vida = 0
            self.vivo=False

    def aplicar_gravidade(self):
        self.vel.y = min(
            self.vel.y + configuracoes.GRAVIDADE,
            configuracoes.VEL_QUEDA_LIVRE
        )

    def atualizar_hitbox(self):
        """Mantém a hitbox reduzida centralizada no sprite."""
        self.hitbox.center = self.rect.center

    def mover_colidir_x(self,blocos):
        parede = 0
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        for tile in blocos:
            if self.rect.colliderect(tile):
                if self.vel.x > 0:
                    self.rect.right = tile.left
                    parede = 1
                elif self.vel.x <0:
                    self.rect.left = tile.right
                    parede = -1
                self.pos.x = self.rect.x
        return parede

    def mover_colidir_y(self,blocos):
        no_chao = False
        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)
        for tile in blocos:
            if self.rect.colliderect(tile):
                if self.vel.y > 0:
                    self.rect.bottom = tile.top
                    no_chao = True
                elif self.vel.y <0:
                    self.rect.top = tile.bottom
                self.vel.y = 0
                self.pos.y = self.rect.y
        return no_chao

    def desenhar(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))


class Jogador(Personagem):
    def __init__(self, x, y):
        super().__init__(x, y, configuracoes.TAMANHO_JOGADOR, configuracoes.TAMANHO_JOGADOR, 10)
        self.direcao = "direita"
        self._esta_se_movendo = False
        self.numero_sprite = 1
        self._contador_animacao = 0
        self.chao_y = None
        self.esta_no_chao = False
        tamanho = (configuracoes.TAMANHO_JOGADOR, configuracoes.TAMANHO_JOGADOR)
        self.sprites = carregar_sprites_jogador(tamanho)
        self.sprites_morte = carregar_sprites_morte_jogador(tamanho)
        self.sprite_powerup_cooldown = carregar_sprite_powerup_cooldown()
        self.sprites_tiro = carregar_sprite_tiro("Jogador", tamanho)
        self.sprites_dano = carregar_sprite_dano("Jogador", tamanho)
        self._atualizar_imagem()
        self.cooldown_tiro = 0
        self.cooldown_tiro_max = configuracoes.COOLDOWN_TIRO
        self.cooldown_reduzido_ativo = False
        self.indicador_cooldown_timer = 0.0
        self._dano_timer = 0
        self._DANO_MOSTRAR = 20

    def pular(self):
        if not self.esta_no_chao:
            return False
        self.vel.y = configuracoes.FORCA_PULO_JOGADOR
        self.esta_no_chao = False
        return True

    def reduzir_cooldown_tiro(self):
        cooldown_minimo = max(1, (configuracoes.COOLDOWN_TIRO + 4) // 5)
        self.cooldown_tiro_max = max(
            cooldown_minimo,
            int(self.cooldown_tiro_max * 0.85),
        )
        self.cooldown_tiro = min(self.cooldown_tiro, self.cooldown_tiro_max)
        self.cooldown_reduzido_ativo = True
        self.indicador_cooldown_timer = 2.5

    def desenhar_powerup_cooldown(self, surface):
        if self.indicador_cooldown_timer <= 0:
            return
        indicador_rect = self.sprite_powerup_cooldown.get_rect(
            midbottom=(self.rect.centerx, self.rect.top - 4)
        )
        surface.blit(self.sprite_powerup_cooldown, indicador_rect)

    def _atualizar_imagem(self):
        direcao = "direita" if not self._esta_se_movendo else self.direcao
        imagens = self.sprites.get(direcao, [])
        if imagens:
            indice = 0 if not self._esta_se_movendo else (self.numero_sprite - 1) % len(imagens)
            self.image = imagens[indice]

    def update(self, dt=1/60):
        self.indicador_cooldown_timer = max(
            0.0, self.indicador_cooldown_timer - dt
        )
        teclas = pygame.key.get_pressed()
        self.vel.x = 0

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.vel.x = -configuracoes.VELOCIDADE_JOGADOR
            self.direcao = "esquerda"
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.vel.x = configuracoes.VELOCIDADE_JOGADOR
            self.direcao = "direita"

        if not self.esta_no_chao:
            self.vel.y = min(self.vel.y + configuracoes.GRAVIDADE, configuracoes.VEL_QUEDA_LIVRE)

        self._esta_se_movendo = self.vel.x != 0 or self.vel.y != 0
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt * 60

        if self.chao_y is not None:
            if self.rect.bottom >= self.chao_y and self.vel.y >= 0:
                self.rect.bottom = self.chao_y
                self.vel.y = 0
                self.esta_no_chao = True
            else:
                self.esta_no_chao = False

        tela = pygame.display.get_surface()
        if tela:
            self.rect.clamp_ip(tela.get_rect())
        self.atualizar_hitbox()

        if self._esta_se_movendo:
            self._contador_animacao += 1
            if self._contador_animacao >= 8:
                self.numero_sprite += 1
                self._contador_animacao = 0
        else:
            self.numero_sprite = 1
            self._contador_animacao = 0

        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        if self._dano_timer > 0:
            self._dano_timer -= 1

        if self._dano_timer > 0:
            dano_img = self.sprites_dano.get(self.direcao) if self.sprites_dano else None
            if dano_img:
                self.image = dano_img
            else:
                self._atualizar_imagem()
            return

        if self.cooldown_tiro > 0:
            tiro_img = self.sprites_tiro.get(self.direcao) if self.sprites_tiro else None
            if tiro_img:
                self.image = tiro_img
            else:
                self._atualizar_imagem()
            return

        self._atualizar_imagem()