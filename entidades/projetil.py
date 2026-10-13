import pygame
import configuracoes


class Tiro(pygame.sprite.Sprite):
	def __init__(self, x, y, direcao):
		super().__init__()
		largura, altura = configuracoes.TAMANHO_TIRO
		self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
		pygame.draw.rect(self.image, (28, 29, 31), (0, 2, 12, 6), border_radius=3)
		pygame.draw.rect(self.image, (255, 209, 70), (5, 1, 7, 8), border_radius=2)
		pygame.draw.circle(self.image, (255, 240, 180), (12, 5), 3)
		pygame.draw.circle(self.image, (12, 12, 12), (12, 5), 1)
		pygame.draw.rect(self.image, (200, 200, 200), (10, 2, 4, 6), border_radius=2)
		self.rect = self.image.get_rect(center=(x, y))
		self.velocidade = configuracoes.VELOCIDADE_TIRO * direcao

	def update(self, dt=1/60):
		self.rect.x += self.velocidade * dt
		tela = pygame.display.get_surface()
		if tela and (self.rect.right < 0 or self.rect.left > tela.get_width()):
			self.kill()
