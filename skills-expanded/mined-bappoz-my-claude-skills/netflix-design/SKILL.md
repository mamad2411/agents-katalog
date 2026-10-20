---
name: netflix-design
description: >
  Design no padrão Netflix: dark cinematográfico, a arte (thumbnails/billboards) como interface,
  vermelho de marca #E50914, tipografia Netflix Sans, linhas de cards com preview no hover e foco
  em descoberta de conteúdo. Use quando o usuário mencionar: "Netflix", "estilo Netflix", "app de
  streaming", "catálogo de vídeo", "carrossel de filmes", "OTT UI", "design Netflix". Consulta
  ../_shared/design-resources.md.
---

# Netflix

Você atua como designer que domina a linguagem do Netflix. Princípio máximo: **o conteúdo é a interface**. A arte de capa vende; a UI apenas emoldura e some.

## Princípios

1. **Arte é a UI** — billboards e thumbnails ocupam a tela; texto e cromo são mínimos.
2. **Dark cinematográfico** — fundo quase preto para a arte brilhar, como uma sala de cinema.
3. **Descoberta por linhas** — conteúdo organizado em "rows" temáticas roláveis horizontalmente; hover expande com preview.
4. **Vermelho é acento de ação** — `#E50914` em play/CTA/logo, nunca como fundo.
5. **Personalização visível** — "porque você assistiu", continue assistindo; a home é diferente para cada um.

## Design tokens

```css
:root {
  --nflx-red: #e50914;               /* brand / play */
  --nflx-red-hover: #f6121d;
  --nflx-black: #141414;             /* base (não #000 puro) */
  --nflx-elevated: #181818;          /* cards */
  --nflx-text: #ffffff;
  --nflx-text-secondary: #b3b3b3;
  --nflx-radius: 4px;                /* thumbnails têm cantos discretos */
  --nflx-scrim: linear-gradient(0deg, rgba(20,20,20,1) 0%, transparent 60%);
}
```

## Tipografia (Netflix Sans / fallback)

```css
/* Netflix Sans é proprietária. Fallback próximo: */
font-family: 'Netflix Sans', 'Helvetica Neue', Roboto, sans-serif;
--nflx-billboard-title: 700 clamp(28px, 5vw, 64px)/1.1;   /* título sobre o billboard */
--nflx-row-title: 700 20px/1.3;      /* "Em alta agora" */
--nflx-body: 400 15px/1.5;
```

## Componentes-chave

```css
/* Billboard: arte full-bleed + scrim para legibilidade do texto */
.nflx-billboard { position: relative; aspect-ratio: 16/9; background-size: cover; }
.nflx-billboard::after { content:''; position:absolute; inset:0; background: var(--nflx-scrim); }

/* Linha de cards com scroll horizontal */
.nflx-row { display: flex; gap: 6px; overflow-x: auto; scroll-snap-type: x mandatory; }
.nflx-card {
  flex: 0 0 auto; width: 240px; aspect-ratio: 16/9; border-radius: var(--nflx-radius);
  background-size: cover; scroll-snap-align: start; transition: transform .3s ease;
}
.nflx-card:hover { transform: scale(1.12); z-index: 2; }   /* preview expande */

.nflx-btn-play {
  background: #fff; color: #000; border: none; border-radius: var(--nflx-radius);
  padding: 8px 24px; font-weight: 700; display: inline-flex; gap: 8px; align-items: center;
}
.nflx-btn-info { background: rgba(109,109,110,.7); color: #fff; border: none; border-radius: var(--nflx-radius); padding: 8px 24px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [netflix.com](https://www.netflix.com/) | Referência viva: billboard, rows, hover preview, scrim. |
| [Netflix Design (Medium)](https://netflixtechblog.com/) | Artigos de UI/personalização/performance. |
| [Netflix Brand Site](https://brand.netflix.com/) | Uso do vermelho, logo, tipografia. |
| [Codrops Hub](https://tympanus.net/codrops/hub/) | Carrosséis, hover 3D e transições cinematográficas. |
| ../_shared/design-resources.md | Imagens/arte, gradientes-scrim, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Arte full-bleed + scrim | Card pequeno com muito texto |
| Vermelho só em ação | Vermelho de fundo |
| Fundo `#141414` | Preto puro `#000` |
| Hover que expande preview | Hover só com sombra |

## Checklist

- [ ] Thumbnails/billboards dominam a tela
- [ ] Scrim de gradiente sob texto sobre arte
- [ ] Vermelho `#E50914` apenas em ação/marca
- [ ] Rows com scroll horizontal + snap
- [ ] Hover expande o card (preview)
- [ ] Fundo off-black `#141414`
