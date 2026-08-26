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
    """Procura por imagens de tiro nomeadas com o sufixo 'tiro'.
    Ex: Jogador,direita,tiro.png ou Jogador,esquerda,tiro.png
    Retorna um dict {'esquerda': Surface|None, 'direita': Surface|None}.
    """
    sprites = {"esquerda": None, "direita": None}
    diretorios = [
        IMAGES_DIR,
        os.path.join(os.path.dirname(__file__), "entidades", "front", "sprites"),
    ]
    arquivos = []
    for diretorio in diretorios:
        arquivos.extend(glob.glob(os.path.join(diretorio, "*")))

    for arquivo in arquivos:
        nome = os.path.splitext(os.path.basename(arquivo))[0]
        partes = [p.strip().lower() for p in nome.split(",")]
        if len(partes) >= 3 and partes[-1] == "tiro" and partes[0] == classe.lower():
            direcao = partes[1]
            if direcao in sprites and sprites[direcao] is None:
                sprites[direcao] = load_image(arquivo, tamanho)

    return sprites