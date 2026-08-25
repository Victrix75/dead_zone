from abc import ABC,abstractmethod
import pygame
import configuracoes

class Personagem(pygame.sprint.Sprite,ABC):

    def __init__(self,
                 x,
                 y,
                 largura,
                 altura,
                 vida):
        super().__init__()
        self.largura,self.altura = largura,altura
        self.pos = pygame.Vector(x,y)
        self.vel = pygame.Vector(0,0)
        self.rect = pygame.Rect(x,y,largura,altura)
        self.maximo_vidas = vida
        self.vidas = vida
        self.vivo = True
        self.contato_dano = 1
        self.imagem=None

    @abstractmethod
    def update(self, *args,**kwargs):
        pass

    def tomar_dano(self,dano,contra_ataque=(0,0)):
        if not self.vivo:
            return
        self.vida -=dano
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

    def desenhar(self, surface,camera):
        surface.blit(self.image,
                     camera.apply(self.rect))

        
                