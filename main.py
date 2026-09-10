import pygame

import configuracoes
from cenario import Cenario
from entidades.personagem import Jogador
from entidades.projetil import Tiro
from inimigos import ZumbiBasico
from estados import Botao, ESTADO_MENU, ESTADO_FASE_1, ESTADO_SAIR


def criar_menu(tela):
    """Cria os botões do menu inicial com as opções de jogar e sair."""
    fonte_titulo = pygame.font.Font(None, 72)
    fonte_botao = pygame.font.Font(None, 42)

    titulo = fonte_titulo.render(configuracoes.TITULO, True, configuracoes.COR_TEXTO)
    titulo_rect = titulo.get_rect(center=(tela.get_width() // 2, 140))

    largura_botao = 220
    altura_botao = 60
    centro_x = tela.get_width() // 2
    centro_y = tela.get_height() // 2

    botoes = {
        "jogar": Botao(
            centro_x - largura_botao // 2,
            centro_y - 20,
            largura_botao,
            altura_botao,
            "Play",
            (40, 180, 110),
            configuracoes.COR_TEXTO,
            fonte_botao,
        ),
        "sair": Botao(
            centro_x - largura_botao // 2,
            centro_y + 70,
            largura_botao,
            altura_botao,
            "Sair",
            (180, 60, 60),
            configuracoes.COR_TEXTO,
            fonte_botao,
        ),
    }

    return titulo, titulo_rect, botoes


def estado_menu(tela, eventos):
    """Renderiza e controla a tela inicial do jogo."""
    titulo, titulo_rect, botoes = criar_menu(tela)
    tela.fill(configuracoes.BG_COR)
    tela.blit(titulo, titulo_rect)

    for botao in botoes.values():
        botao.desenhar(tela)

    pygame.display.flip()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return ESTADO_SAIR
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = pygame.mouse.get_pos()
            if botoes["jogar"].clique(pos):
                return ESTADO_FASE_1
            if botoes["sair"].clique(pos):
                return ESTADO_SAIR

    return ESTADO_MENU


def criar_fase_1(tela):
    """Cria os grupos e objetos da fase 1 apenas uma vez."""
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    tiros = pygame.sprite.Group()

    linha_chao = tela.get_height() - 80
    jogador = Jogador(tela.get_width() // 2, linha_chao - 90)
    cenario = Cenario(tela)
    todos_sprites.add(jogador)

    return {
        "todos_sprites": todos_sprites,
        "inimigos": inimigos,
        "tiros": tiros,
        "jogador": jogador,
        "cenario": cenario,
        "pontos": 0,
        "spawn_timer": 0,
        "spawn_intervalo": 120,
        "linha_inimigo": linha_chao,
    }


def estado_fase_1(tela, eventos, dt, fase):
    """Atualiza a fase 1 um único frame por chamada, mantendo o ciclo estável."""
    jogador = fase["jogador"]
    todos_sprites = fase["todos_sprites"]
    inimigos = fase["inimigos"]
    tiros = fase["tiros"]
    cenario = fase["cenario"]

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return ESTADO_SAIR, None
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return ESTADO_MENU, None
            elif evento.key == pygame.K_SPACE:
                if jogador.cooldown_tiro <= 0:
                    direcao_tiro = 1 if jogador.direcao == "direita" else -1
                    tiro = Tiro(
                        jogador.rect.centerx + direcao_tiro * jogador.rect.width // 2,
                        jogador.rect.centery,
                        direcao_tiro,
                    )
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                    jogador.cooldown_tiro = configuracoes.COOLDOWN_TIRO

    fase["spawn_timer"] += dt * configuracoes.FPS
    if fase["spawn_timer"] >= fase["spawn_intervalo"]:
        robo = ZumbiBasico(
            tela.get_width() + 40,
            fase["linha_inimigo"],
        )
        todos_sprites.add(robo)
        inimigos.add(robo)
        fase["spawn_timer"] = 0

    fase["pontos"] += len(pygame.sprite.groupcollide(inimigos, tiros, True, True))
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        jogador.tomar_dano(1)
        if not jogador.vivo:
            return ESTADO_MENU, None

    todos_sprites.update(dt)
    cenario.desenhar()
    todos_sprites.draw(tela)

    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(
        f"Vida: {jogador.vida}  |  Pontos: {fase['pontos']}",
        True,
        configuracoes.COR_TEXTO,
    )
    tela.blit(texto, (10, 10))
    pygame.display.flip()

    return ESTADO_FASE_1, fase


def main():
    """Ponto de entrada do jogo: controla os estados e o fluxo principal."""
    pygame.init()
    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(configuracoes.TITULO)
    relogio = pygame.time.Clock()

    estado_atual = ESTADO_MENU
    eventos = []
    fase_1 = None
    rodando = True

    while rodando:
        dt = relogio.tick(configuracoes.FPS) / 1000.0
        eventos = pygame.event.get()

        if estado_atual == ESTADO_MENU:
            estado_atual = estado_menu(tela, eventos)
        elif estado_atual == ESTADO_FASE_1:
            if fase_1 is None:
                fase_1 = criar_fase_1(tela)
            estado_atual, fase_1 = estado_fase_1(tela, eventos, dt, fase_1)
        elif estado_atual == ESTADO_SAIR:
            rodando = False

    pygame.quit()


if __name__ == "__main__":
    main()