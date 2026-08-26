import glob
import os
import re

from assets import IMAGES_DIR, load_image


def carregar_sprites(classe, tamanho=None):
    """Carrega arquivos no formato Classe,direcao,numero.ext."""
    sprites = {"esquerda": [], "direita": []}
    for direcao in sprites:
        arquivos = _encontrar_arquivos(classe, direcao)
        sprites[direcao] = [
            load_image(arquivo, tamanho)
            for arquivo in arquivos
        ]
    return sprites


def _encontrar_arquivos(classe, direcao):
    diretorios = [
        IMAGES_DIR,
        os.path.join(os.path.dirname(__file__), "entidades", "front", "sprites", classe),
    ]
    arquivos = []
    for diretorio in diretorios:
        arquivos.extend(glob.glob(os.path.join(diretorio, "*")))
    arquivos = [
        arquivo for arquivo in arquivos
        if _nome_corresponde(os.path.basename(arquivo), classe, direcao)
    ]
    return sorted(set(arquivos), key=_numero_do_arquivo)


def _nome_corresponde(nome_com_extensao, classe, direcao):
    nome = os.path.splitext(nome_com_extensao)[0]
    return nome == f"{classe},{direcao},{_numero_do_nome(nome)}" or bool(
        re.fullmatch(fr"{re.escape(classe)}{direcao}\d+", nome)
    )


def _numero_do_nome(nome):
    try:
        return int(nome.rsplit(",", 1)[1])
    except (IndexError, ValueError):
        return -1


def _numero_do_arquivo(caminho):
    nome = os.path.splitext(os.path.basename(caminho))[0]
    legado = re.fullmatch(r".+(?:esquerda|direita)(\d+)", nome)
    if legado:
        return int(legado.group(1))
    try:
        return int(nome.rsplit(",", 1)[1])
    except (IndexError, ValueError):
        return 0


def carregar_sprites_jogador(tamanho=None):
    return carregar_sprites("Jogador", tamanho)


def carregar_sprite_tiro(classe, tamanho=None):
    """Procura por imagens de tiro em subdiretórios ou com sufixo 'tiro'.
    Ex: Jogador,direita,tiro.png ou pasta tiro/Jogador,direita,1.png
    Retorna um dict {'esquerda': Surface|None, 'direita': Surface|None}.
    """
    sprites = {"esquerda": None, "direita": None}
    
    # Procura em subdiretório tiro
    tiro_dir = os.path.join(os.path.dirname(__file__), "entidades", "front", "sprites", classe, "tiro")
    if os.path.exists(tiro_dir):
        for direcao in sprites:
            arquivos = _encontrar_arquivos(f"{classe}/tiro", direcao)
            if arquivos:
                sprites[direcao] = load_image(arquivos[0], tamanho)
    
    # Se não encontrou em subdiretório, procura com sufixo
    if sprites["esquerda"] is None or sprites["direita"] is None:
        diretorios = [
            IMAGES_DIR,
            os.path.join(os.path.dirname(__file__), "entidades", "front", "sprites"),
        ]
        arquivos = []
        for diretorio in diretorios:
            if os.path.exists(diretorio):
                arquivos.extend(glob.glob(os.path.join(diretorio, "**", "*"), recursive=True))

        for arquivo in arquivos:
            nome = os.path.splitext(os.path.basename(arquivo))[0]
            partes = [p.strip().lower() for p in nome.split(",")]
            if len(partes) >= 3 and partes[-1] == "tiro" and partes[0] == classe.lower():
                direcao = partes[1]
                if direcao in sprites and sprites[direcao] is None:
                    try:
                        sprites[direcao] = load_image(arquivo, tamanho)
                    except:
                        pass
    
    # Criar sprite fallback se não encontrou
    if tamanho and (sprites["esquerda"] is None or sprites["direita"] is None):
        import pygame
        fallback = pygame.Surface(tamanho, pygame.SRCALPHA)
        fallback.fill((120, 240, 180, 200))  # Verde claro semi-transparente
        if sprites["esquerda"] is None:
            sprites["esquerda"] = fallback
        if sprites["direita"] is None:
            sprites["direita"] = fallback.copy()

    return sprites


def carregar_sprite_dano(classe, tamanho=None):
    """Procura por imagens de dano em subdiretórios ou com sufixo 'dano'.
    Ex: Jogador,direita,dano.png ou pasta dano/Jogador,direita,1.png
    Retorna um dict {'esquerda': Surface|None, 'direita': Surface|None}.
    """
    sprites = {"esquerda": None, "direita": None}
    
    # Procura em subdiretório dano
    dano_dir = os.path.join(os.path.dirname(__file__), "entidades", "front", "sprites", classe, "dano")
    if os.path.exists(dano_dir):
        for direcao in sprites:
            arquivos = _encontrar_arquivos(f"{classe}/dano", direcao)
            if arquivos:
                sprites[direcao] = load_image(arquivos[0], tamanho)
    
    # Se não encontrou em subdiretório, procura com sufixo
    if sprites["esquerda"] is None or sprites["direita"] is None:
        diretorios = [
            IMAGES_DIR,
            os.path.join(os.path.dirname(__file__), "entidades", "front", "sprites"),
        ]
        arquivos = []
        for diretorio in diretorios:
            if os.path.exists(diretorio):
                arquivos.extend(glob.glob(os.path.join(diretorio, "**", "*"), recursive=True))

        for arquivo in arquivos:
            nome = os.path.splitext(os.path.basename(arquivo))[0]
            partes = [p.strip().lower() for p in nome.split(",")]
            if len(partes) >= 3 and partes[-1] == "dano" and partes[0] == classe.lower():
                direcao = partes[1]
                if direcao in sprites and sprites[direcao] is None:
                    try:
                        sprites[direcao] = load_image(arquivo, tamanho)
                    except:
                        pass
    
    # Criar sprite fallback se não encontrou
    if tamanho and (sprites["esquerda"] is None or sprites["direita"] is None):
        import pygame
        fallback = pygame.Surface(tamanho, pygame.SRCALPHA)
        fallback.fill((200, 70, 70, 200))  # Vermelho escuro semi-transparente
        if sprites["esquerda"] is None:
            sprites["esquerda"] = fallback
        if sprites["direita"] is None:
            sprites["direita"] = fallback.copy()

    return sprites