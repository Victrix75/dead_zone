import pygame
import configuracoes


class Tiro(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.Surface((8, 16))
		self.image.fill(configuracoes.COR_PROJETIL_JOGADOR)
		self.rect = self.image.get_rect(midbottom=(x, y))

	def update(self):
		self.rect.y -= configuracoes.VELOCIDADE_TIRO
		if self.rect.bottom < 0:
			self.kill()
