
assignment
Atividade Mini Jogo
Max Miller da Silveira
•
Ontem (editado: 09:02)
100 pontos
Com base na mecânica do arquivo jogo_tiro elabore uma proposta de jogo.


Grupo 1
Luiz Carlos Lima Medeiros
Shara Jayane da Silva
Samuel Santos Lopes
Felipe Eduardo Medeiros Pinheiro
Emilly Yasmim Alves Araujo
Weslley Albert Alves Dantas
Sara Isabel Rocha da Costa

Grupo 2
Sofia Sabina Azevêdo Nóbrega
Renan Rodrigo Medeiros Dantas
Iam Italo da Silva
Manoel Vitor do Nascimento Brito
Cezar Augusto da Nóbrega Calixto
Matheus Najan da Conceição Silva

Grupo 3
Juan Oliveira Fonseca
Kalyne Dutra de Medeiros
Ytalo Kauã Diniz da Silva
Adaylton José Rodrigues Borges
Reylton de Lira Tavares
Anthony Rafael Ferreira da Silva
Nataniel de Medeiros Lucena dos Santos

Grupo 4
José Ferreira dos Santos Neto
Anthony Gabryel Macedo da Silva
Rafael Araújo Brito
Gustavo Medeiros de Lucena
Ana Allyce da Silva Albino
Gabriel Medeiros Soares

Grupo 5
Maria Clara Silva Pereira
Nathália Mariana de Araújo Silva
Davi Araujo Bezerra
Larissa Danielly Santos Nóbrega
Lays Eduarda Araújo Silva
Pablo Lorran Pereira Gomes

Grupo 6
Júlio César Brito Santos
Pedro Lázaro de Aráujo Dantas
Vinícius Morais de Araújo
Rafael Victor Cabral de Azevêdo
Maria Luiza Santos Lopes
Ana Élida Nascimento de Souza

Definam os papeis de cada um:

Líder: Organiza o cronograma, integra o código de todos, resolve conflitos de merge, garante que o jogo final rode sem erros.

Desenvolvedores: Implementa as melhorias na mecânica principal como  novos tipos de tiro, padrões de inimigos, sistema de pontuação, condições de vitória/derrota. Cria itens colecionáveis, upgrades de arma, sistema de vidas/energia, ondas de dificuldade crescente (waves).

Artes: Cria ou edita sprites do jogador, inimigos, projéteis, explosões e cenário; cuida da identidade visual do jogo.

Artes e Desenvolvimento: Implementa menu inicial, HUD (vida, pontuação, fase), tela de game over, telas de transição.

Artes e Testes: Adiciona sons de tiro, explosão, música de fundo; testa o jogo em busca de bugs, balanceamento de dificuldade e dá feedback contínuo ao grupo.

Implementações obrigatórias: 
  — dificuldade crescente: aumentar velocidade e frequência de spawn conforme o tempo/pontuação — hoje o jogador pode metralhar sem limite; adicionar um temporizador entre tiros — itens que caem dos inimigos destruídos: tiro triplo, escudo, vida extra, tiro mais rápido
jogo_tiro.py
Texto

1 comentário para a turma

Ytalo Kauã Diniz da Silva • Ontem
Max, você disse que a gente ia escolher os grupos, e a maioria da sala já estava com os grupos formados.

Adicionar comentário para a turma...

Seus trabalhos
Atribuído
Comentários particulares
import pygame
import random

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Robot Defense - Template")

FPS = 60
clock = pygame.time.Clock()


# CLASSE BASE
class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image.fill((0, 255, 0))  # verde
        self.vida = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))


# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image.fill((255, 255, 0))  # amarelo

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))  # vermelho

    def atualizar_posicao(self):
        raise NotImplementedError


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()


todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

pontos = 0
spawn_timer = 0

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)

    # timer de entrada dos inimigos
    spawn_timer += 1
    if spawn_timer > 40:
        robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
        todos_sprites.add(robo)
        inimigos.add(robo)
        spawn_timer = 0

    # colisão tiro x robô
    colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)
    pontos += len(colisao)

    # colisão robô x jogador
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        jogador.vida -= 1
        if jogador.vida <= 0:
            print("GAME OVER!")
            rodando = False

    # atualizar
    todos_sprites.update()

    # desenhar
    TELA.fill((20, 20, 20))
    todos_sprites.draw(TELA)

    #Painel de pontos e vida
    font = pygame.font.SysFont(None, 30)
    texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
    TELA.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
