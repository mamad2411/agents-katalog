---
name: pinterest-design
description: >
  Design no padrão Pinterest: grid masonry de imagens como interface, vermelho de marca #E60023,
  cantos bem arredondados, foco visual e descoberta. Use quando o usuário mencionar: "Pinterest",
  "estilo Pinterest", "grid masonry", "mural de inspiração", "galeria de imagens", "moodboard",
  "descoberta visual", "pins", "design Pinterest". Consulta ../_shared/design-resources.md.
---

# Pinterest

Você atua como designer que domina a linguagem do Pinterest. A interface **é** o grid de imagens: um mural infinito de descoberta visual onde as imagens (pins) fazem todo o trabalho e a UI quase some.

## Princípios

1. **Masonry é a assinatura** — grid de colunas com cards de alturas variáveis (as imagens mantêm proporção). Denso, orgânico, infinito.
2. **Imagem é tudo** — o pin ocupa o card inteiro; texto e ações são discretos e surgem no hover.
3. **Vermelho de marca pontual** — `#E60023` no logo, no botão "Salvar" e em ações-chave. O fundo é branco/limpo para as imagens brilharem.
4. **Cantos bem arredondados** — cards com raio generoso (16px) dão a sensação suave e amigável característica.
5. **Descoberta sem fim** — scroll infinito, related pins, zero fricção para explorar.

## Design tokens

```css
:root {                              /* Light */
  --pin-red: #e60023;                /* marca / salvar */
  --pin-red-hover: #ad081b;
  --pin-bg: #ffffff;
  --pin-bg-alt: #f0f0f0;            /* botão secundário */
  --pin-text: #111111;
  --pin-text-muted: #767676;
  --pin-radius: 16px;
  --pin-gap: 16px;                  /* espaço entre pins */
}
:root[data-theme="dark"] {
  --pin-bg: #111111; --pin-bg-alt: #2a2a2a; --pin-text: #ffffff; --pin-text-muted: #b0b0b0;
}
```

## Tipografia (system)

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
--pin-title: 600 28px/1.2;
--pin-pin-title: 600 16px/1.4;       /* título do pin (discreto) */
--pin-body: 400 14px/1.5;
--pin-meta: 400 12px/1.4;
```

## Componentes-chave

```css
/* Masonry via CSS columns (simples) ou grid com row-span */
.pin-masonry { columns: 5 236px; column-gap: var(--pin-gap); }
@media (max-width: 900px) { .pin-masonry { columns: 3 180px; } }

.pin-card {
  break-inside: avoid; margin-bottom: var(--pin-gap); position: relative;
  border-radius: var(--pin-radius); overflow: hidden; cursor: zoom-in;
}
.pin-card img { width: 100%; display: block; border-radius: var(--pin-radius); }
/* Overlay + botão Salvar surgem no hover */
.pin-card__overlay { position: absolute; inset: 0; background: rgba(0,0,0,.2);
  opacity: 0; transition: opacity .2s; }
.pin-card:hover .pin-card__overlay { opacity: 1; }

.pin-btn-save {
  background: var(--pin-red); color: #fff; border: none; border-radius: 24px;
  padding: 12px 16px; font: 600 15px/1 inherit; transition: background .1s;
}
.pin-btn-save:hover { background: var(--pin-red-hover); }
.pin-btn { background: var(--pin-bg-alt); color: var(--pin-text); border: none;
  border-radius: 24px; padding: 12px 16px; font-weight: 600; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [pinterest.com](https://www.pinterest.com/) | Referência viva: masonry, hover, botão Salvar, cantos. |
| [Pinterest Design (Medium)](https://medium.com/pinterest-design) | Estudos de caso (Gestalt, grid, acessibilidade). |
| [Pinterest Brand](https://business.pinterest.com/brand-guidelines/) | Uso do vermelho e logo. |
| [Codrops Hub](https://tympanus.net/codrops/hub/) | Layouts masonry e transições de imagem. |
| ../_shared/design-resources.md | Imagens (Unsplash/Pexels), grid, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Masonry com imagens em foco | Grid retangular uniforme sem alma |
| Vermelho só em Salvar/marca | Vermelho de fundo |
| Ações no hover | UI poluindo o pin |
| Cantos 16px | Cantos retos |

## Checklist

- [ ] Grid masonry (alturas variáveis, colunas responsivas)
- [ ] Pin = imagem ocupando o card inteiro
- [ ] Vermelho `#E60023` em Salvar/marca; fundo limpo
- [ ] Overlay + ações surgem no hover
- [ ] Cantos arredondados 16px
- [ ] Scroll infinito + dark mode
