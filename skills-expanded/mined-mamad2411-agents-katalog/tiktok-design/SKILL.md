---
name: tiktok-design
description: >
  Design no padrão TikTok: vídeo vertical full-screen imersivo, dark absoluto, acentos cyan #25F4EE
  e vermelho #FE2C55, UI sobreposta mínima e energia jovem. Use quando o usuário mencionar: "TikTok",
  "estilo TikTok", "vídeo vertical", "feed de vídeo full screen", "shorts", "reels", "for you page",
  "app de vídeo curto", "design TikTok". Consulta ../_shared/design-resources.md.
---

# TikTok

Você atua como designer que domina a linguagem do TikTok. A interface é **o vídeo em tela cheia**: imersão total, UI sobreposta mínima e flutuante, fundo preto absoluto e acentos vibrantes. Energia, velocidade e foco no conteúdo.

## Princípios

1. **Vídeo full-screen imersivo** — o vídeo vertical ocupa 100% da tela; a UI flutua por cima, translúcida e discreta, sem molduras.
2. **Preto absoluto** — fundo `#000` para o vídeo dominar e os acentos brilharem.
3. **Acentos cyan + vermelho** — `#25F4EE` (cyan) e `#FE2C55` (vermelho/rosa) da marca, com o efeito "glitch/chromatic" característico. Usados em CTA, curtir, branding.
4. **Interação lateral** — coluna de ações à direita (curtir, comentar, compartilhar, áudio girando); info do criador embaixo. Padrão consagrado de vídeo vertical.
5. **Energia jovem** — motion rápido, texto bold, feedback tátil, cultura de trends.

## Design tokens

```css
:root {                              /* dark absoluto (padrão) */
  --tt-bg: #000000;
  --tt-surface: #121212;
  --tt-text: #ffffff;
  --tt-text-muted: rgba(255,255,255,.75);
  --tt-cyan: #25f4ee;                /* acento marca */
  --tt-red: #fe2c55;                /* CTA / curtir / marca */
  --tt-border: rgba(255,255,255,.12);
  --tt-radius: 8px;
}
:root[data-theme="light"] {         /* light existe mas é secundário */
  --tt-bg: #ffffff; --tt-surface: #f1f1f2; --tt-text: #161823;
  --tt-text-muted: rgba(22,24,35,.75); --tt-border: rgba(22,24,35,.12);
}
```

## Tipografia (Proxima Nova / TikTok Sans / fallback)

```css
/* TikTok usa 'Proxima Nova' / 'TikTok Sans'. Fallback próximo: */
font-family: 'TikTok Sans', 'Proxima Nova', -apple-system, 'Helvetica Neue', sans-serif;
--tt-title: 700 18px/1.3;
--tt-username: 600 17px/1.3;
--tt-body: 400 15px/1.4;
--tt-action-count: 600 13px/1.2;     /* contador sob cada ação */
```

## Componentes-chave

```css
.tt-video-stage { position: relative; width: 100%; height: 100dvh; background: #000; overflow: hidden; }
.tt-video { width: 100%; height: 100%; object-fit: cover; }
/* Gradiente sutil embaixo p/ legibilidade da UI sobre o vídeo */
.tt-scrim { position: absolute; inset: auto 0 0 0; height: 40%;
  background: linear-gradient(0deg, rgba(0,0,0,.5), transparent); }

/* Coluna de ações à direita */
.tt-actions { position: absolute; right: 8px; bottom: 90px; display: flex; flex-direction: column;
  gap: 20px; align-items: center; color: #fff; }
.tt-action { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.tt-action--like.active svg { fill: var(--tt-red); }

.tt-btn-primary {                    /* CTA vermelho (ex: Seguir/Login) */
  background: var(--tt-red); color: #fff; border: none; border-radius: var(--tt-radius);
  height: 44px; padding: 0 20px; font: 600 15px/1 'TikTok Sans'; transition: filter .1s;
}
.tt-btn-primary:hover { filter: brightness(1.05); }
/* Efeito chromatic/glitch da marca */
.tt-glitch { text-shadow: 2px 0 var(--tt-red), -2px 0 var(--tt-cyan); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [tiktok.com](https://www.tiktok.com/) | Referência viva: vídeo full-screen, coluna de ações, scrim. |
| [TikTok Brand](https://www.tiktok.com/business/en/brand-guidelines) | Uso de cyan/vermelho, efeito chromatic, logo. |
| [TikTok Design (blog)](https://newsroom.tiktok.com/) | Padrões de produto. |
| [Codrops Hub](https://tympanus.net/codrops/hub/) | Efeitos glitch/chromatic e transições de vídeo. |
| ../_shared/design-resources.md | Dark absoluto, scrim, motion, acessibilidade sobre vídeo. |

## Do / Don't

| Do | Don't |
|---|---|
| Vídeo full-screen, UI flutuante mínima | Molduras/cromo ao redor do vídeo |
| Preto absoluto `#000` | Cinza escuro que apaga o vídeo |
| Cyan + vermelho como acento/glitch | Encher a tela de cor |
| Coluna de ações à direita | Ações espalhadas sem padrão |

## Checklist

- [ ] Vídeo vertical 100% da tela, UI sobreposta translúcida
- [ ] Fundo preto absoluto `#000`
- [ ] Acentos `#25F4EE` (cyan) + `#FE2C55` (vermelho), efeito chromatic na marca
- [ ] Coluna de ações à direita + info do criador embaixo
- [ ] Scrim de gradiente para legibilidade da UI sobre o vídeo
- [ ] Motion rápido; light mode secundário
