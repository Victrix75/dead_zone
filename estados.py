import pygame

# Estados principais do jogo para separar as telas e a lógica.
ESTADO_MENU = "menu"
ESTADO_FASE_1 = "fase_1"
ESTADO_SAIR = "sair"


class Botao:
    """Botão simples reutilizável para menus e telas de início."""

    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_texto, fonte):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.fonte = fonte

    def desenhar(self, tela):
        # Fundo do botão.
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=12)

        # Borda para destacar o botão na tela.
        pygame.draw.rect(tela, (255, 255, 255), self.rect, 2, border_radius=12)

        # Texto centralizado dentro do botão.
        texto_superficie = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_superficie.get_rect(center=self.rect.center)
        tela.blit(texto_superficie, texto_rect)

    def clique(self, posicao):
        # Verifica se o clique do mouse está dentro do botão.
        return self.rect.collidepoint(posicao)
