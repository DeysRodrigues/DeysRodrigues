"""Sprite do gatinho: so a cabeca, apoiada rente a mesa, com o rabinho ao lado.

O desenho e um mapa de letras, um caractere por pixel:

    .  vazio        #  corpo        p  rosa da orelha e da bochecha
    e  olho         s  brilho       n  focinho          m  boca

Mexer no bicho e mexer nessas letras. Cada linha precisa de 16 caracteres.
"""

CABECA = [
    ".#............#.",
    ".#p..........p#.",
    ".#pp........pp#.",
    ".##############.",
    "################",
    "################",
    "###se######se###",
    "###ee######ee###",
    "###ee######ee###",
    "################",
    "#pp####nn####pp#",
    "######m##m######",
    ".######mm######.",
    "..############..",
    "...##########...",
]
for _i, _l in enumerate(CABECA):
    assert len(_l) == 16, f"linha {_i} tem {len(_l)} caracteres, precisa de 16"

ALTURA = len(CABECA)

# Rabinho: caminho de 2 pixels de espessura, subindo pela direita da cabeca e
# virando pra dentro no topo. As coordenadas seguem a mesma grade da cabeca.
RABO = [
    (17, 14), (18, 13), (19, 12), (20, 11),
    (21, 10), (21, 9), (21, 8), (20, 7), (19, 6), (18, 6),
]

COR = {
    "#": "#d75dd2",
    "p": "#fb81be",
    "e": "#2b1240",
    "s": "#ffffff",
    "n": "#e96fc8",
    "m": "#2b1240",
}

OLHO = {"e", "s"}   # o que pisca separado


def pixels(linhas_visiveis=None):
    """Devolve (coluna, linha, cor, parte) de cada pixel.

    `parte` e "rabo", "olho" ou "cabeca", que e como o banner separa o que
    anima junto. `linhas_visiveis` corta a cabeca por baixo, para o caso de
    ela ficar parcialmente escondida pela mesa.
    """
    ate = ALTURA if linhas_visiveis is None else linhas_visiveis
    fora = []

    for x, y in RABO:
        if y < ate:
            for dx in (0, 1):
                fora.append((x + dx, y, COR["#"], "rabo"))

    for y, linha in enumerate(CABECA[:ate]):
        for x, c in enumerate(linha):
            if c != ".":
                fora.append((x, y, COR[c], "olho" if c in OLHO else "cabeca"))

    return fora
