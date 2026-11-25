---
name: concept-diagrams
# Como esta skill aparece para o usuario na lista do 'o que sei fazer'.
# Mora aqui, e nao no motor: o que a skill e e como ela se apresenta
# mudam juntos.
vitrine:
  grupo: 'Visuais'
  rotulo: 'fluxo/jornada em SVG'
description: "Generate minimal SVG educational/process diagrams."
version: 1.0.0
author: Sentury
license: MIT
platforms: [linux, macos, windows]
tags: [diagrams, svg, visualization, educational]
category: creative
---

# Concept Diagrams Skill

Duas opções dentro de `executar_python` (NÃO use import/open/curl/write_file — o sandbox bloqueia). O diagrama é **renderizado inline (imagem)** E fica **baixável** ao mesmo tempo.

## 1) `save_svg(filename, svg_completo)` — RICO e LIVRE (PREFIRA ESTE)

Você escreve o **SVG inteiro** — qualquer forma, ícone, gradiente, cor, legenda, layout. É onde mora a riqueza: **capriche** e **varie o desenho conforme o conteúdo** (não repita o mesmo diagrama). Sempre `<svg ...viewBox="0 0 L A">...</svg>`, sem `<script>`/`onclick`, texto legível (cor clara em fundo escuro).

```python
svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 470" font-family="Segoe UI, system-ui, sans-serif">
  <defs><filter id="s"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/></filter></defs>
  <rect width="900" height="470" fill="#0f172a"/>
  <text x="450" y="48" fill="#e2e8f0" font-size="24" font-weight="700" text-anchor="middle">Por que o site ficou lento</text>
  <!-- efeito central -->
  <rect x="360" y="90" width="180" height="72" rx="16" fill="#450a0a" stroke="#ef4444" stroke-width="2" filter="url(#s)"/>
  <text x="450" y="133" fill="#fecaca" font-size="17" font-weight="700" text-anchor="middle">Página em 6,2 s</text>
  <!-- causas (desenhe cards coloridos por severidade, setas curvas, ícones, sub-causas) -->
  <rect x="70" y="270" width="200" height="72" rx="16" fill="#422006" stroke="#eab308" stroke-width="2" filter="url(#s)"/>
  <text x="170" y="313" fill="#fde68a" font-size="15" font-weight="600" text-anchor="middle">Consulta sem índice</text>
  <path d="M170,270 C170,200 350,180 400,162" fill="none" stroke="#64748b" stroke-width="2.5"/>
  <!-- ...adicione as demais causas e conexões... -->
</svg>"""
resultado = save_svg("causa_raiz_lentidao", svg)
```

Desenhe de acordo com o caso: causa-raiz (efeito + causas + sub-causas), jornada (etapas em fluxo), funil (blocos que estreitam), comparativo (barras), espinha de peixe. Use paleta, títulos e formas variadas — **evite o mesmo layout sempre**.

## 2) `save_svg_diagram(filename, boxes, arrows, layout, title)` — RÁPIDO (estruturado)

Quando quiser algo pronto sem desenhar. layout ∈ `flow`/`tree`/`star`/`funnel`; boxes com `color` (red/yellow/green/blue/purple/gray) e `level` (0,1,2…), SEM x/y.

```python
boxes = [{"id":"lento","text":"Página em 6,2 s","color":"red","level":0},
         {"id":"indice","text":"Consulta sem índice","color":"yellow","level":1},
         {"id":"imagens","text":"Imagens sem compressão","color":"yellow","level":1}]
arrows = [{"from":"indice","to":"lento"},{"from":"imagens","to":"lento"}]
resultado = save_svg_diagram("causa_raiz", boxes, arrows, layout="tree", title="Por que o site ficou lento")
```

Só afirme que gerou se `resultado` confirmar sucesso. Para um diagrama editável, use `save_excalidraw` dentro do `executar_python` (gera um `.excalidraw`, que abre no excalidraw.com).
