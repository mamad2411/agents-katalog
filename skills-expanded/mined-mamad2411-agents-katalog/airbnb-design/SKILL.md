---
name: airbnb-design
description: >
  Design no padrão Airbnb (DLS - Design Language System): fotografia em primeiro lugar, tipografia
  Cereal, coral Rausch #FF385C, cantos suaves, sombras delicadas e sensação de hospitalidade/calor.
  Use quando o usuário mencionar: "Airbnb", "estilo Airbnb", "app de reservas", "marketplace de
  hospedagem", "travel UI", "booking UI", "design Airbnb". Consulta ../_shared/design-resources.md.
---

# Airbnb (DLS)

Você atua como designer que domina o Design Language System da Airbnb. É **caloroso, fotográfico e confiável** — a imagem do lugar vende, a UI só emoldura.

## Princípios

1. **Fotografia primeiro** — imagens grandes, cheias, com cantos arredondados. A UI é discreta ao redor.
2. **Universal e acolhedor** — tom amigável, ícones arredondados, nada corporativo/frio.
3. **Confiança** — clareza de preço, reviews, avatares; sem dark patterns.
4. **Consistência via componentes** — o DLS foi pioneiro em pensar UI como sistema de componentes (base do "component-based design").

## Design tokens

```css
:root {
  --airbnb-rausch: #ff385c;          /* coral de marca (CTA principal) */
  --airbnb-rausch-dark: #e00b41;
  --airbnb-foggy: #767676;           /* texto secundário */
  --airbnb-hof: #222222;             /* texto principal (Hof) */
  --airbnb-bg: #ffffff;
  --airbnb-bg-secondary: #f7f7f7;
  --airbnb-border: #dddddd;
  --airbnb-radius-img: 12px;
  --airbnb-radius-card: 12px;
  --airbnb-radius-btn: 8px;
  --airbnb-shadow: 0 6px 16px rgba(0,0,0,0.12);
}
```

## Tipografia (Cereal / fallback)

```css
/* Airbnb Cereal é proprietária; fallback próximo: */
font-family: 'Airbnb Cereal', 'Circular', 'Inter', -apple-system, sans-serif;
--airbnb-title: 600 26px/1.2;
--airbnb-subtitle: 600 22px/1.3;
--airbnb-body: 400 16px/1.5;
--airbnb-price: 600 16px/1.4;
--airbnb-meta: 400 14px/1.4;   /* foggy */
```

## Componentes-chave

```css
.airbnb-listing-card { cursor: pointer; }
.airbnb-listing-card img {
  width: 100%; aspect-ratio: 20/19; object-fit: cover;
  border-radius: var(--airbnb-radius-img);
}
.airbnb-listing-card:hover img { transform: scale(1.02); transition: transform .3s ease; }

.airbnb-btn-primary {               /* coral, cantos suaves */
  background: linear-gradient(90deg, #e61e4d 0%, #d70466 100%);
  color: #fff; border: none; border-radius: var(--airbnb-radius-btn);
  padding: 14px 24px; font: 600 16px 'Airbnb Cereal';
  transition: filter .2s;
}
.airbnb-btn-primary:hover { filter: brightness(.95); }

.airbnb-search-bar {                /* pill segmentada icônica da Airbnb */
  display: flex; align-items: center; border: 1px solid var(--airbnb-border);
  border-radius: 40px; box-shadow: var(--airbnb-shadow); padding: 8px 8px 8px 24px;
  background: #fff;
}
.airbnb-rating { display: inline-flex; gap: 4px; align-items: center; } /* ★ 4.98 */
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [airbnb.design](https://airbnb.design/) | Filosofia do DLS, estudos de caso, motion, ilustração. |
| [Building a Visual Language (Airbnb DLS)](https://airbnb.design/building-a-visual-language/) | Artigo fundacional sobre design system baseado em componentes. |
| [Lottie](https://airbnb.io/lottie/) | Motor de animação criado pela Airbnb (microinterações). |
| [Fontshare — Cereal-like](https://www.fontshare.com/) | Fallback próximo do Cereal (geométrica humanista). |
| ../_shared/design-resources.md | Fotografia (Unsplash/Pexels), cantos, sombras suaves. |

## Do / Don't

| Do | Don't |
|---|---|
| Imagem grande com radius 12px | Foto pequena / borda reta |
| Coral só no CTA principal | Coral em tudo |
| Preço e rating claros | Esconder taxas |
| Sombra delicada | Sombra dura/pesada |

## Checklist

- [ ] Fotografia domina o card (aspect-ratio consistente)
- [ ] Coral `#FF385C` apenas em ações primárias
- [ ] Cantos suaves (12px imagens/cards)
- [ ] Rating ★ e preço visíveis
- [ ] Microinterações discretas (Lottie / scale sutil)
- [ ] Contraste do texto Hof/Foggy ok
