from enum import Enum,auto
import pygame
import configuracoes

class Habilidade(Enum):
    TIRO = auto()

NOME_HABILIDADE = {
    Habilidade.TIRO: "Tiro",
}
HABILIDADE_HOTKEY = {
    Habilidade.TIRO: "F",
}

class PowerUp(pygame.sprite.Sprite):

    def __init__(self,x,y,habilidade:Habilidade):
        super().__init__()
        self.habilidade = habilidade
        tamanho = configuracoes.TILE_SIZE
        self.image = None 
        self.rect = self.image.get_rect(
            topleft=(x,y))
        self._t=0

    def update(self):
        self._t +=1
        if (self._t // 15) % 2 == 0:
            self.rect.y += -1
        else:
            self.rect.y += 1

    def desenhar(self, surface, camera):
        surface.blit(self.image, 
                     camera.apply(self.rect))
        