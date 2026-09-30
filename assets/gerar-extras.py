#!/usr/bin/env python3
"""Gato pequeno e divisor de secao, mesma linguagem visual do banner."""
import pathlib

GATO = [
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
    "....########....",
]
COR = {"#": "#d75dd2", "p": "#fb81be", "e": "#2b1240",
       "s": "#ffffff", "n": "#e96fc8", "m": "#2b1240"}
OUT = pathlib.Path("/home/deys/Projetos/personal-projects/refactor-plan/profile-assets")
OUT.mkdir(parents=True, exist_ok=True)
nl = chr(10)

# ---------------------------------------------------------------- gato pequeno
P = 5
W, H = 16 * P, 15 * P
corpo, olhos = [], []
for y, linha in enumerate(GATO):
    for x, c in enumerate(linha):
        if c == ".":
            continue
        r = (f'<rect x="{x * P}" y="{y * P}" width="{P}" height="{P}" '
             f'fill="{COR[c]}"/>')
        (olhos if c in ("e", "s") else corpo).append(r)

cat = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}" role="img" aria-label="gatinho">
  <g>
    <animateTransform attributeName="transform" type="translate"
                      values="0 0; 0 2; 0 0" dur="3.6s" repeatCount="indefinite"/>
{nl.join("    " + r for r in corpo)}
    <g>
      <animate attributeName="opacity" values="1;1;1;0;1"
               keyTimes="0;0.9;0.945;0.965;1" dur="4.2s" repeatCount="indefinite"/>
{nl.join("      " + r for r in olhos)}
    </g>
  </g>
</svg>
"""
(OUT / "cat.svg").write_text(cat)

# -------------------------------------------------------------------- divisor
HEART = [".#.#.", "#####", "#####", ".###.", "..#.."]
CORES = ["#a020f0", "#b23ae6", "#c54bdc", "#d75dd2",
         "#e96fc8", "#fb81be", "#e96fc8", "#d75dd2",
         "#c54bdc", "#b23ae6", "#a020f0", "#6a0dad",
         "#4a47c2", "#3761d8", "#2b6fea", "#1e90ff"]
DP, DW, DH = 3, 900, 22
espaco = DW // len(CORES)
pecas = []
for i, cor in enumerate(CORES):
    ox = i * espaco + (espaco - 5 * DP) // 2
    oy = 2 if i % 2 == 0 else 5
    for y, linha in enumerate(HEART):
        for x, c in enumerate(linha):
            if c == "#":
                pecas.append(
                    f'<rect x="{ox + x * DP}" y="{oy + y * DP}" width="{DP}" '
                    f'height="{DP}" fill="{cor}" opacity="0.9"/>')

div = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{DW}" height="{DH}"
     viewBox="0 0 {DW} {DH}" role="img" aria-label="divisor">
{nl.join("  " + p for p in pecas)}
</svg>
"""
(OUT / "divider.svg").write_text(div)

for f in ("cat.svg", "divider.svg"):
    print(f"{OUT / f} ({(OUT / f).stat().st_size} bytes)")
