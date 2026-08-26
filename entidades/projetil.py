import pygame
import configuracoes


class Tiro(pygame.sprite.Sprite):
	def __init__(self, x, y, direcao):
		super().__init__()
		self.image = pygame.Surface((16, 8))
		self.image.fill(configuracoes.COR_PROJETIL_JOGADOR)
		self.rect = self.image.get_rect(center=(x, y))
		self.velocidade = configuracoes.VELOCIDADE_TIRO * direcao

	def update(self):
		self.rect.x += self.velocidade
		tela = pygame.display.get_surface()
		if self.rect.right < 0 or self.rect.left > tela.get_width():
			self.kill()
