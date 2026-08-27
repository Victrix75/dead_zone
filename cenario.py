import pygame
import os

# Caminho para a pasta onde estão guardadas as imagens do jogo
ASSETS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "cenario",
)


class Cenario:
    def __init__(self, tela):
        self.tela = tela
        self.frame = 0
        self.frames = []
        self.carregar_frames()

    def carregar_frames(self):
        # Obtém a largura e altura atuais da tela
        largura_tela = self.tela.get_width()
        altura_tela = self.tela.get_height()

        # Lista com os nomes exatos das duas imagens do fundo
        arquivos_cenario = ["cenario0.png"]

        for nome_arquivo in arquivos_cenario:
            caminho = os.path.join(ASSETS, nome_arquivo)

            if os.path.exists(caminho):
                # Carrega a imagem
                img = pygame.image.load(caminho).convert()

                # Redimensiona a imagem para cobrir toda a tela
                img = pygame.transform.scale(
                    img, 
                    (largura_tela, altura_tela)
                )

                self.frames.append(img)

    def atualizar_animacao(self):
        # Incrementa o contador de quadros para a animação
        self.frame += 1

    def desenhar(self):
        if len(self.frames) > 0:
            # Alterna a imagem a cada 10 quadros para a animação não ser rápida demais
            # O operador % garante que o índice fica entre 0 e (quantidade de imagens - 1)
            indice = (self.frame // 10) % len(self.frames)
            
            # Desenha a imagem de fundo a partir do canto superior esquerdo (0, 0)
            self.tela.blit(self.frames[indice], (0, 0))

            # Atualiza a contagem para o próximo ciclo
            self.atualizar_animacao()