import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "cenario")


class Cenario:
    def __init__(self, tela):
        self.tela = tela
        self.frame = 0
        self.frames = []
        self.carregar_frames()

    def carregar_frames(self):
        largura_tela = self.tela.get_width()
        altura_tela = self.tela.get_height()

        arquivos_cenario = ["cenario0.webp", "cenario0.png"]

        for nome_arquivo in arquivos_cenario:
            caminho = os.path.join(ASSETS, nome_arquivo)
            if os.path.exists(caminho):
                img = pygame.image.load(caminho)
                if img.get_alpha() is None:
                    img = img.convert()
                else:
                    img = img.convert_alpha()

                img = pygame.transform.scale(img, (largura_tela, altura_tela))
                self.frames.append(img)

        if not self.frames:
            self.frames.append(pygame.Surface((largura_tela, altura_tela)))
            self.frames[0].fill((22, 20, 38))

    def atualizar_animacao(self):
        self.frame += 1

    def desenhar(self):
        if len(self.frames) > 0:
            indice = (self.frame // 10) % len(self.frames)
            self.tela.blit(self.frames[indice], (0, 0))
            self.atualizar_animacao()