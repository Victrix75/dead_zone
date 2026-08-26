from abc import ABC, abstractmethod
import pygame
import configuracoes
from sprites import carregar_sprites_jogador, carregar_sprite_tiro, carregar_sprite_dano


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
        super().__init__(x, y, 88, 88, 5)
        self.direcao = "direita"
        self._esta_se_movendo = False
        self.numero_sprite = 1
        self._contador_animacao = 0
        self.sprites = carregar_sprites_jogador((88, 88))
        self.sprites_tiro = carregar_sprite_tiro("Jogador", (88, 88))
        self.sprites_dano = carregar_sprite_dano("Jogador", (88, 88))
        self._atualizar_imagem()
        self.cooldown_tiro = 0
        self._dano_timer = 0
        self._DANO_MOSTRAR = 20

    def _atualizar_imagem(self):
        direcao = "direita" if not self._esta_se_movendo else self.direcao
        imagens = self.sprites.get(direcao, [])
        if imagens:
            indice = 0 if not self._esta_se_movendo else (self.numero_sprite - 1) % len(imagens)
            self.image = imagens[indice]

    def update(self):
        teclas = pygame.key.get_pressed()
        self.vel.x = 0
        self.vel.y = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.vel.x = -configuracoes.VELOCIDADE_JOGADOR
            self.direcao = "esquerda"
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.vel.x = configuracoes.VELOCIDADE_JOGADOR
            self.direcao = "direita"
        self._esta_se_movendo = self.vel.length_squared() > 0
        self.rect.x += round(self.vel.x)
        self.rect.y += round(self.vel.y)
        tela = pygame.display.get_surface()
        self.rect.clamp_ip(tela.get_rect())
        if self._esta_se_movendo:
            self._contador_animacao += 1
            if self._contador_animacao >= 8:
                self.numero_sprite += 1
                self._contador_animacao = 0
        else:
            self.numero_sprite = 1
            self._contador_animacao = 0
        # Decrementar cooldown do tiro
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        # Decrementar timer de dano
        if self._dano_timer > 0:
            self._dano_timer -= 1

        # Prioridade: dano > tiro > animação normal
        if self._dano_timer > 0:
            dano_img = self.sprites_dano.get(self.direcao) if self.sprites_dano else None
            if dano_img:
                self.image = dano_img
            else:
                # Fallback: usar animação normal ou imagem vermelha/alterada
                self._atualizar_imagem()
            return

        if self.cooldown_tiro > 0:
            tiro_img = self.sprites_tiro.get(self.direcao) if self.sprites_tiro else None
            if tiro_img:
                self.image = tiro_img
            else:
                # Fallback: usar animação normal
                self._atualizar_imagem()
            return

        self._atualizar_imagem()