#!/usr/bin/env python3
"""Gera o cat-banner.svg: a cena pixel com o gato e as estrelas animados.

Rodar de dentro de assets/:

    python3 gerar-banner.py

Precisa de Pillow e do rsvg-convert. O fundo sai de base-model.png, que e a
arte da cena vazia; o gato, o nome, os chips e as estrelas sao desenhados aqui.
"""
import base64
import io
import pathlib

from PIL import Image, ImageDraw, ImageFont

import gato

AQUI = pathlib.Path(__file__).resolve().parent
FONTE = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-ExtraBold.ttf"
W, H = 2170, 725

# ------------------------------------------------------------------ texto


def pixelar(texto, tam, escala, cor):
    """Renderiza pequeno e amplia sem suavizar. O limiar no alfa tira o
    cinza de borda, senao o texto nao fica pixel de verdade."""
    f = ImageFont.truetype(FONTE, tam)
    b = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textbbox((0, 0), texto, font=f)
    w, h = b[2] - b[0] + 2, b[3] - b[1] + 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-b[0] + 1, -b[1] + 1), texto, font=f, fill=cor)
    im.putalpha(im.getchannel("A").point(lambda v: 255 if v > 110 else 0))
    return im.resize((w * escala, h * escala), Image.NEAREST)


# Os icones de tecnologia saem da propria Nerd Font, nao de SVG externo.
# Assim eles recebem o mesmo tratamento de pixel do texto e ficam nitidos;
# rasterizar SVG deixava eles lisos e borrados no meio da arte em pixel.
GLIFO = {
    "java": "\ue738",        # dev-java
    "spring": "\ue8ac",      # dev-spring
    "react": "\ue7ba",       # dev-react
    "typescript": "\ue8ca",  # dev-typescript
    "python": "\ue73c",      # dev-python
}


def rgba(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def icone(nome, cor, tam=46):
    """Desenha o glifo no tamanho final, com suavizacao normal.

    Aqui nao se usa o pixelar(): o limiar no alfa come os tracos finos desses
    logos e o resultado fica pior que o original.
    """
    g = GLIFO[nome]
    f = ImageFont.truetype(FONTE, tam)
    b = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textbbox((0, 0), g, font=f)
    w, h = max(b[2] - b[0] + 2, 2), max(b[3] - b[1] + 2, 2)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((-b[0] + 1, -b[1] + 1), g, font=f, fill=rgba(cor))
    return im


# --------------------------------------------------- camada estatica
base = Image.open(AQUI / "base-model.png").convert("RGBA")
assert base.size == (W, H), base.size

# A arte tem mais de cem mil cores por causa dos degrades. Fechar a paleta
# aqui, antes de desenhar chip e texto, corta o peso do arquivo sem estragar
# as cores de destaque, que sao pintadas depois.
tela = base.convert("RGB").quantize(colors=140, method=Image.MEDIANCUT,
                                    dither=Image.NONE).convert("RGBA")

NOME = "Deys Rodrigues"
TAGLINE = "full stack developer"
tela.alpha_composite(pixelar(NOME, 19, 6, (168, 85, 199, 255)), (835, 195))
tela.alpha_composite(pixelar(NOME, 19, 6, (255, 255, 255, 255)), (828, 186))
tela.alpha_composite(pixelar(TAGLINE, 13, 4, (214, 176, 240, 255)), (832, 322))

CHIPS = [("java", "java", "#f0a04b"),
         ("spring", "spring", "#6DB33F"),
         ("react", "react", "#61DAFB"),
         ("typescript", "typescript", "#3178C6"),
         ("python", "python", "#f7c948")]
CY, CH, ICO = 404, 70, 52
PAD_X, GAP_IL, GAP_CHIP = 10, 8, 10

d = ImageDraw.Draw(tela)
x = 830
for arquivo, rotulo, cor in CHIPS:
    lab = pixelar(rotulo, 14, 2, (240, 230, 250, 255))
    largura = PAD_X * 2 + ICO + GAP_IL + lab.width
    d.rounded_rectangle([x, CY, x + largura, CY + CH], radius=12,
                        fill=(30, 16, 56, 235), outline=cor, width=3)
    ic = icone(arquivo, cor)
    tela.alpha_composite(ic, (x + PAD_X + (ICO - ic.width) // 2,
                              CY + (CH - ic.height) // 2))
    tela.alpha_composite(lab, (x + PAD_X + ICO + GAP_IL, CY + (CH - lab.height) // 2))
    x += largura + GAP_CHIP

LY, X0, X1 = 648, 60, W - 60
CORES = [(251, 129, 190), (215, 93, 210), (160, 32, 240),
         (106, 13, 173), (55, 97, 216), (30, 144, 255)]


def degrade(t):
    t = max(0.0, min(1.0, t)) * (len(CORES) - 1)
    i = min(int(t), len(CORES) - 2)
    f, a, b = t - i, CORES[i], CORES[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3))


for px in range(X0, X1):
    d.rectangle([px, LY, px + 1, LY + 7], fill=degrade((px - X0) / (X1 - X0)))

HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
for hx, cor in ((X0 - 42, (251, 129, 190)), (X1 + 8, (30, 144, 255))):
    for yy, linha in enumerate(HEART):
        for xx, c in enumerate(linha):
            if c == "#":
                d.rectangle([hx + xx * 7, LY - 14 + yy * 7,
                             hx + xx * 7 + 6, LY - 14 + yy * 7 + 6], fill=cor)

buf = io.BytesIO()
tela.convert("RGB").quantize(colors=256, method=Image.MEDIANCUT,
                             dither=Image.NONE).save(buf, format="PNG", optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()

# ------------------------------------------------------- gato e estrelas
# A cabeca fica apoiada rente a mesa: o queixo encosta na linha do tampo.
MESA = 542          # y da beirada da mesa, medido na propria arte
P, CX = 15, 330
topo = MESA - gato.ALTURA * P

cabeca, olhos, rabo = [], [], []
for x, y, cor, parte in gato.pixels():
    r = (f'<rect x="{CX + x*P}" y="{topo + y*P}" width="{P}" height="{P}" '
         f'fill="{cor}"/>')
    {"rabo": rabo, "olho": olhos, "cabeca": cabeca}[parte].append(r)

# pivo do rabo: onde ele encosta na cabeca
PX, PY = CX + 18 * P, topo + 14 * P

SPARK = [".#.", "###", ".#."]
ESTRELAS = [(1290, 120, 9, "#ff7ad9", 0.0), (1178, 214, 7, "#63e0ff", 0.7),
            (1520, 180, 8, "#c78bff", 1.4), (1610, 300, 6, "#ff7ad9", 2.1),
            (1100, 330, 7, "#63e0ff", 0.4), (1690, 96, 6, "#ffffff", 1.8),
            (760, 250, 7, "#c78bff", 1.1), (1420, 92, 6, "#63e0ff", 2.6),
            (2010, 250, 7, "#ff7ad9", 0.9)]
estrelas = []
for ex, ey, p, cor, atraso in ESTRELAS:
    pix = "".join(f'<rect x="{ex+x*p}" y="{ey+y*p}" width="{p}" height="{p}" fill="{cor}"/>'
                  for y, l in enumerate(SPARK) for x, c in enumerate(l) if c == "#")
    estrelas.append(f'<g opacity="0.25">{pix}<animate attributeName="opacity" '
                    f'values="0.2;1;0.2" dur="3.2s" begin="{atraso}s" '
                    f'repeatCount="indefinite"/></g>')

nl = "\n"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="Deys Rodrigues, desenvolvedora full stack">

  <image x="0" y="0" width="{W}" height="{H}"
         xlink:href="data:image/png;base64,{b64}"/>

{nl.join("  " + e for e in estrelas)}

  <g>
    <animateTransform attributeName="transform" type="translate"
                      values="0 0; 0 5; 0 0" dur="3.6s" repeatCount="indefinite"/>

    <g>
      <animateTransform attributeName="transform" type="rotate"
                        values="0 {PX} {PY}; -13 {PX} {PY}; 0 {PX} {PY}; 9 {PX} {PY}; 0 {PX} {PY}"
                        dur="2.6s" repeatCount="indefinite"/>
{nl.join("      " + r for r in rabo)}
    </g>

{nl.join("    " + r for r in cabeca)}

    <g>
      <animate attributeName="opacity" values="1;1;1;0;1"
               keyTimes="0;0.9;0.945;0.965;1" dur="4.2s" repeatCount="indefinite"/>
{nl.join("      " + o for o in olhos)}
    </g>
  </g>
</svg>
"""

saida = AQUI / "cat-banner.svg"
saida.write_text(svg)
print(f"{saida.name}: {len(svg)/1024:.0f} KB  (fundo {len(buf.getvalue())/1024:.0f} KB)")
print(f"gato: cabeca {16*P}x{gato.ALTURA*P}px, queixo em y={MESA}")
