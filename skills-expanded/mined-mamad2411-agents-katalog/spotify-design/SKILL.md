---
name: spotify-design
description: >
  Design no padrão Spotify (Encore): dark-first, verde de marca #1DB954, tipografia Circular
  bold, capas/imagens como herói, cantos arredondados e alto contraste. Use quando o usuário
  mencionar: "Spotify", "estilo Spotify", "app de música", "player de música", "Encore",
  "streaming UI", "design Spotify". Consulta ../_shared/design-resources.md.
---

# Spotify (Encore)

Você atua como designer que domina a linguagem do Spotify (design system **Encore**). É **dark por padrão**, com a arte (capas, fotos de artista) como protagonista e o verde de marca usado como acento vivo.

## Princípios

1. **Dark-first** — fundo quase preto, conteúdo brilha por cima. Light mode é exceção.
2. **Arte é herói** — capas grandes, imagens edge-to-edge, gradientes derivados da cor dominante da capa.
3. **Verde é acento, não fundo** — `#1DB954` para play/CTA/estado ativo. Nunca preenchendo telas.
4. **Denso mas navegável** — muitas listas; hierarquia por peso tipográfico e espaçamento.

## Design tokens

```css
:root {
  --spotify-green: #1db954;          /* brand / play / active */
  --spotify-green-hover: #1ed760;
  --spotify-black: #121212;          /* base */
  --spotify-elevated: #181818;       /* cards */
  --spotify-elevated-hover: #282828;
  --spotify-highlight: #1a1a1a;
  --spotify-text: #ffffff;
  --spotify-text-subdued: #b3b3b3;   /* metadados, artista */
  --spotify-radius: 8px;
  --spotify-radius-round: 500px;     /* botões pill / avatar */
}
```

## Tipografia (Circular / fallback)

```css
/* Circular é proprietária; fallback próximo: */
font-family: 'Circular', 'Spotify Circular', 'Montserrat', 'Helvetica Neue', sans-serif;
--spotify-title-xl: 900 48px/1 'Circular';   /* nome de playlist/álbum */
--spotify-title: 700 24px/1.2;
--spotify-body: 400 16px/1.5;
--spotify-meta: 400 14px/1.4;                /* text-subdued */
```

## Componentes-chave

```css
.spotify-play-btn {                 /* verde, circular, com scale no hover */
  background: var(--spotify-green); color: #000; border: none;
  width: 56px; height: 56px; border-radius: 50%;
  display: grid; place-items: center; box-shadow: 0 8px 8px rgba(0,0,0,.3);
  transition: transform .12s ease, background .12s ease;
}
.spotify-play-btn:hover { transform: scale(1.06); background: var(--spotify-green-hover); }

.spotify-card {                     /* card de álbum */
  background: var(--spotify-elevated); border-radius: var(--spotify-radius);
  padding: 16px; transition: background .3s ease;
}
.spotify-card:hover { background: var(--spotify-elevated-hover); }

/* Header com gradiente derivado da capa */
.spotify-header { background: linear-gradient(180deg, var(--cover-color, #535353) 0%, var(--spotify-black) 100%); }

.spotify-btn-pill {
  background: transparent; color: #fff; border: 1px solid #7c7c7c;
  border-radius: var(--spotify-radius-round); padding: 8px 32px; font-weight: 700;
}
.spotify-btn-pill:hover { border-color: #fff; transform: scale(1.04); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [spotify.design](https://spotify.design/) | Filosofia de design, estudos de caso, motion. |
| [Encore (Spotify design system)](https://spotify.design/article/reimagining-design-systems-at-spotify) | Como o Encore é estruturado (foundations/web/mobile). |
| [Spotify brand](https://developer.spotify.com/documentation/design) | Uso correto do verde, logo, do/don't de marca. |
| [Fontshare — Montserrat/Circular-like](https://www.fontshare.com/) | Fallback tipográfico próximo do Circular. |
| ../_shared/design-resources.md | Cor dominante de imagem, gradientes, acessibilidade. |

## Do / Don't

| Do | Don't |
|---|---|
| Verde só em play/CTA/ativo | Verde como cor de fundo |
| Capa grande + gradiente dela | Fundo chapado sem arte |
| Dark #121212 | Preto puro #000 (Spotify usa off-black) |
| Text-subdued em metadados | Tudo branco 100% |

## Checklist

- [ ] Fundo off-black `#121212`, não `#000`
- [ ] Verde `#1DB954` apenas como acento
- [ ] Gradiente de header derivado da capa
- [ ] Play button circular com scale no hover
- [ ] Metadados em `--spotify-text-subdued`
- [ ] Contraste ok mesmo no dark
