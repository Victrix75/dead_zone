import pygame
import configuracoes


class Tiro(pygame.sprite.Sprite):
	def __init__(self, x, y, direcao):
		super().__init__()
		self.image = pygame.Surface(configuracoes.TAMANHO_TIRO)
		self.image.fill(configuracoes.COR_PROJETIL_JOGADOR)
		self.rect = self.image.get_rect(center=(x, y))
		self.velocidade = configuracoes.VELOCIDADE_TIRO * direcao

	def update(self, dt=1/60):
		self.rect.x += self.velocidade * dt
		tela = pygame.display.get_surface()
		if tela and (self.rect.right < 0 or self.rect.left > tela.get_width()):
			self.kill()
