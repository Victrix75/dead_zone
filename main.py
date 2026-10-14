import random
from pathlib import Path

import pygame

import configuracoes
from cenario import Cenario
from entidades.personagem import Jogador
from entidades.projetil import Tiro
from inimigos import ZumbiBasico, ZumbiForte
from estados import (
    Botao,
    ESTADO_GAME_OVER,
    ESTADO_MENU,
    ESTADO_FASE_1,
    ESTADO_SAIR,
)


def carregar_audio():
    """Carrega as músicas e efeitos do diretório de sons."""
    pasta_sons = Path(__file__).parent / "sounds"
    musicas = {
        ESTADO_MENU: (pasta_sons / "musica_menu_EpicZOMBIEsoundtrack.mp3", 0.65),
        ESTADO_FASE_1: (pasta_sons / "jogo_rodando_Deadspace.mp3", 0.3),
        ESTADO_GAME_OVER: (pasta_sons / "tela_game_over_theplague.mp3", 0.65),
    }
    efeitos = {
        "jogador_tiro": pygame.mixer.Sound(pasta_sons / "jogador_tiro.mp3"),
        "zumbi_ataque": pygame.mixer.Sound(pasta_sons / "zumbibasicoataque.mp3"),
    }
    for efeito in efeitos.values():
        efeito.set_volume(0.65)
    return musicas, efeitos


def atualizar_musica(estado, musicas, estado_musica):
    """Inicia em loop a música correspondente quando o estado muda."""
    if estado == estado_musica:
        return estado_musica

    faixa = musicas.get(estado)
    if faixa is None:
        pygame.mixer.music.stop()
        return None

    caminho, volume = faixa
    pygame.mixer.music.stop()
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    return estado


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


def formatar_tempo(segundos):
    """Converte os segundos da partida para o formato minutos:segundos."""
    minutos = int(segundos) // 60
    segundos_restantes = int(segundos) % 60
    return f"{minutos:02d}:{segundos_restantes:02d}"


def estado_game_over(tela, eventos, pontos, tempo):
    """Renderiza a tela de derrota e controla suas opções."""
    fonte_titulo = pygame.font.Font(None, 84)
    fonte_pontos = pygame.font.Font(None, 42)
    fonte_botao = pygame.font.Font(None, 36)

    tela.fill((35, 12, 18))

    titulo = fonte_titulo.render("GAME OVER", True, (220, 60, 70))
    titulo_rect = titulo.get_rect(center=(tela.get_width() // 2, 170))
    tela.blit(titulo, titulo_rect)

    resultado = fonte_pontos.render(
        f"Pontuação: {pontos}  |  Tempo: {formatar_tempo(tempo)}",
        True,
        configuracoes.COR_TEXTO,
    )
    resultado_rect = resultado.get_rect(center=(tela.get_width() // 2, 270))
    tela.blit(resultado, resultado_rect)

    largura_botao = 260
    altura_botao = 58
    centro_x = tela.get_width() // 2
    inicio_botoes = tela.get_height() // 2 + 80
    botoes = {
        "reiniciar": Botao(
            centro_x - largura_botao // 2,
            inicio_botoes,
            largura_botao,
            altura_botao,
            "Jogar novamente",
            (40, 180, 110),
            configuracoes.COR_TEXTO,
            fonte_botao,
        ),
        "menu": Botao(
            centro_x - largura_botao // 2,
            inicio_botoes + 80,
            largura_botao,
            altura_botao,
            "Menu principal",
            (80, 90, 110),
            configuracoes.COR_TEXTO,
            fonte_botao,
        ),
    }

    for botao in botoes.values():
        botao.desenhar(tela)

    pygame.display.flip()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return ESTADO_SAIR
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return ESTADO_MENU
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos
            if botoes["reiniciar"].clique(pos):
                return ESTADO_FASE_1
            if botoes["menu"].clique(pos):
                return ESTADO_MENU

    return ESTADO_GAME_OVER


def criar_fase_1(tela):
    """Cria os grupos e objetos da fase 1 apenas uma vez."""
    todos_sprites = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    corpos_zumbis = pygame.sprite.Group()
    tiros = pygame.sprite.Group()

    linha_chao = tela.get_height() - 80
    jogador = Jogador(
        tela.get_width() // 2,
        linha_chao - configuracoes.TAMANHO_JOGADOR,
    )
    jogador.chao_y = linha_chao
    jogador.esta_no_chao = True
    cenario = Cenario(tela)
    todos_sprites.add(jogador)

    return {
        "todos_sprites": todos_sprites,
        "inimigos": inimigos,
        "corpos_zumbis": corpos_zumbis,
        "tiros": tiros,
        "jogador": jogador,
        "cenario": cenario,
        "pontos": 0,
        "tempo": 0.0,
        "spawn_timer": 0,
        "spawn_intervalo": random.randint(210, 360),
        "zumbi_forte_apareceu": False,
        "morte_timer": None,
        "linha_inimigo": linha_chao,
    }


def criar_zumbi_pela_lateral(tela, linha_inimigo, classe_zumbi):
    """Cria um zumbi numa borda, virado para o centro da tela."""
    lado = random.choice(("esquerda", "direita"))
    direcao = "direita" if lado == "esquerda" else "esquerda"
    tamanho = configuracoes.TAMANHO_INIMIGO
    if classe_zumbi is ZumbiForte:
        tamanho = int(tamanho * 1.35)
    x = -tamanho - 40 if lado == "esquerda" else tela.get_width() + 40
    return classe_zumbi(x, linha_inimigo, direcao)


def estado_animacao_morte(tela, eventos, dt, fase):
    """Mostra a pose sem sangue e depois com sangue antes do game over."""
    if any(evento.type == pygame.QUIT for evento in eventos):
        return ESTADO_SAIR, fase

    fase["morte_timer"] += dt
    indice_sprite = 0 if fase["morte_timer"] < 1.0 else 1
    fase["jogador"].image = fase["jogador"].sprites_morte[indice_sprite]
    fase["cenario"].desenhar()
    fase["todos_sprites"].draw(tela)
    pygame.display.flip()

    if fase["morte_timer"] >= 2.0:
        return ESTADO_GAME_OVER, fase
    return ESTADO_FASE_1, fase


def estado_fase_1(tela, eventos, dt, fase, efeitos):
    """Atualiza a fase 1 um único frame por chamada, mantendo o ciclo estável."""
    jogador = fase["jogador"]
    todos_sprites = fase["todos_sprites"]
    inimigos = fase["inimigos"]
    corpos_zumbis = fase["corpos_zumbis"]
    tiros = fase["tiros"]
    cenario = fase["cenario"]
    if fase["morte_timer"] is not None:
        return estado_animacao_morte(tela, eventos, dt, fase)

    fase["tempo"] += dt
    etapas_aceleracao = max(0, int((fase["tempo"] - 20) // 4) + 1)
    multiplicador_velocidade = min(1 + etapas_aceleracao * 0.20, 3.0)

    for evento in eventos:
        if evento.type == pygame.QUIT:
            return ESTADO_SAIR, None
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return ESTADO_MENU, None
            elif evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                jogador.pular()
            elif evento.key == pygame.K_f:
                if jogador.cooldown_tiro <= 0:
                    direcao_tiro = 1 if jogador.direcao == "direita" else -1
                    tiro = Tiro(
                        jogador.rect.centerx + direcao_tiro * jogador.rect.width // 2,
                        jogador.rect.centery,
                        direcao_tiro,
                    )
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                    jogador.cooldown_tiro = jogador.cooldown_tiro_max
                    efeitos["jogador_tiro"].play()
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if jogador.cooldown_tiro <= 0:
                direcao_tiro = 1 if jogador.direcao == "direita" else -1
                tiro = Tiro(
                    jogador.rect.centerx + direcao_tiro * jogador.rect.width // 2,
                    jogador.rect.centery,
                    direcao_tiro,
                )
                todos_sprites.add(tiro)
                tiros.add(tiro)
                jogador.cooldown_tiro = jogador.cooldown_tiro_max
                efeitos["jogador_tiro"].play()

    fase["spawn_timer"] += dt * configuracoes.FPS
    if fase["tempo"] >= 15 and not fase["zumbi_forte_apareceu"]:
        forte = criar_zumbi_pela_lateral(
            tela, fase["linha_inimigo"], ZumbiForte
        )
        todos_sprites.add(forte)
        inimigos.add(forte)
        fase["zumbi_forte_apareceu"] = True

    if fase["spawn_timer"] >= fase["spawn_intervalo"]:
        classe_zumbi = (
            ZumbiForte
            if fase["tempo"] >= 15 and random.random() < 0.25
            else ZumbiBasico
        )
        robo = criar_zumbi_pela_lateral(
            tela, fase["linha_inimigo"], classe_zumbi
        )
        todos_sprites.add(robo)
        inimigos.add(robo)
        fase["spawn_timer"] = 0
        fator_intervalo = 0.75 ** etapas_aceleracao
        fase["spawn_intervalo"] = max(
            configuracoes.FPS // 2,
            int(random.randint(210, 360) * fator_intervalo),
        )

    acertos = pygame.sprite.groupcollide(inimigos, tiros, False, True)
    for inimigo, tiros_acertados in acertos.items():
        for _ in tiros_acertados:
            inimigo.tomar_dano(1)
        if inimigo.morrendo:
            inimigos.remove(inimigo)
            corpos_zumbis.add(inimigo)
            fase["pontos"] += 1
            if random.random() < 0.09:
                jogador.reduzir_cooldown_tiro()

    for inimigo in inimigos:
        inimigo.multiplicador_velocidade = multiplicador_velocidade
        inimigo.bloqueado = (
            inimigo.rect.left <= jogador.rect.right
            and inimigo.rect.right >= jogador.rect.left
        )

    todos_sprites.update(dt)

    inimigos_em_contato = [
        inimigo
        for inimigo in inimigos
        if jogador.hitbox.colliderect(inimigo.rect)
    ]
    contato_esquerda = any(
        inimigo.rect.centerx < jogador.hitbox.centerx
        for inimigo in inimigos_em_contato
    )
    contato_direita = any(
        inimigo.rect.centerx > jogador.hitbox.centerx
        for inimigo in inimigos_em_contato
    )
    cercado = contato_esquerda and contato_direita

    # Evita que a correção de colisão alterne o jogador entre dois lados.
    for inimigo in inimigos:
        if cercado or not jogador.hitbox.colliderect(inimigo.rect):
            continue
        if jogador.vel.x > 0:
            jogador.hitbox.right = inimigo.rect.left
        elif jogador.vel.x < 0:
            jogador.hitbox.left = inimigo.rect.right
        elif jogador.vel.x == 0:
            continue
        elif jogador.hitbox.centerx < inimigo.rect.centerx:
            jogador.hitbox.right = inimigo.rect.left
        else:
            jogador.hitbox.left = inimigo.rect.right
        jogador.rect.center = jogador.hitbox.center
        jogador.pos.x = jogador.rect.x
        jogador.atualizar_hitbox()

    # Uma margem de 1 pixel permite atacar no instante em que o zumbi encosta.
    # O ataque acontece quando os sprites visuais encostam.
    area_ataque = jogador.rect.inflate(2, 0)
    inimigos_atacando = [
        inimigo
        for inimigo in inimigos
        if area_ataque.colliderect(inimigo.rect)
    ]
    for inimigo in inimigos_atacando:
        if inimigo.pode_atacar():
            efeitos["zumbi_ataque"].play()
            jogador.tomar_dano(inimigo.dano_ataque)
            if not jogador.vivo:
                fase["morte_timer"] = 0.0
                break

    if fase["morte_timer"] is not None:
        return estado_animacao_morte(tela, eventos, dt, fase)

    inimigos_ordenados = sorted(inimigos, key=lambda inimigo: inimigo.rect.left)
    for anterior, atual in zip(inimigos_ordenados, inimigos_ordenados[1:]):
        distancia_minima = anterior.rect.width + 10
        if atual.rect.left < anterior.rect.right + 10:
            atual.rect.left = anterior.rect.left + distancia_minima

    cenario.desenhar()
    todos_sprites.draw(tela)
    jogador.desenhar_powerup_cooldown(tela)

    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(
        f"Vida: {jogador.vida}  |  Pontos: {fase['pontos']}  |  Tempo: {formatar_tempo(fase['tempo'])}",
        True,
        configuracoes.COR_TEXTO,
    )
    tela.blit(texto, (10, 10))
    pygame.display.flip()

    return ESTADO_FASE_1, fase


def main():
    """Ponto de entrada do jogo: controla os estados e o fluxo principal."""
    pygame.init()
    musicas, efeitos = carregar_audio()
    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(configuracoes.TITULO)
    relogio = pygame.time.Clock()

    estado_atual = ESTADO_MENU
    eventos = []
    fase_1 = None
    rodando = True
    estado_musica = None

    while rodando:
        dt = relogio.tick(configuracoes.FPS) / 1000.0
        eventos = pygame.event.get()
        estado_musica = atualizar_musica(estado_atual, musicas, estado_musica)

        if estado_atual == ESTADO_MENU:
            proximo_estado = estado_menu(tela, eventos)
            if proximo_estado == ESTADO_FASE_1:
                fase_1 = None
            estado_atual = proximo_estado
        elif estado_atual == ESTADO_FASE_1:
            if fase_1 is None:
                fase_1 = criar_fase_1(tela)
            estado_atual, fase_1 = estado_fase_1(
                tela, eventos, dt, fase_1, efeitos
            )
        elif estado_atual == ESTADO_GAME_OVER:
            proximo_estado = estado_game_over(
                tela,
                eventos,
                fase_1["pontos"],
                fase_1["tempo"],
            )
            if proximo_estado == ESTADO_FASE_1:
                fase_1 = None
            estado_atual = proximo_estado
        elif estado_atual == ESTADO_SAIR:
            rodando = False

    pygame.quit()


if __name__ == "__main__":
    main()