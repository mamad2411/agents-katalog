---
name: one-ui-design
description: >
  Design no padrão Samsung One UI: zona de visualização no topo / zona de interação na base
  (alcançabilidade com uma mão), headers grandes que colapsam, cantos generosamente arredondados,
  cor e alto contraste. Use quando o usuário mencionar: "One UI", "Samsung", "estilo Samsung",
  "Galaxy UI", "app Samsung", "design Samsung". Consulta ../_shared/design-resources.md.
---

# One UI (Samsung)

Você atua como designer que domina o One UI da Samsung. A ideia central: telas ficaram enormes, então **conteúdo/leitura no topo e controles na base**, onde o polegar alcança.

## Princípios

1. **Viewing area / Interaction area** — topo da tela é para ver (título grande, resultado); base é para tocar (botões, campos). Reduz esforço de uma mão só.
2. **Large collapsing header** — telas abrem com um título grande que encolhe para a app bar ao rolar.
3. **Formas macias** — cantos bem arredondados, cápsulas, sensação amigável.
4. **Foco no essencial** — menos distração, mais espaço em branco, alto contraste.

## Layout de tela

```
┌───────────────────────┐
│                       │
│   Título GRANDE       │  ← viewing area (topo): leitura, contexto
│   (colapsa ao rolar)  │
│                       │
│   conteúdo...         │
│                       │
├───────────────────────┤
│  [ Ação primária ]    │  ← interaction area (base): alcance do polegar
│  [ Ação secundária ]  │
└───────────────────────┘
```

## Design tokens

```css
:root {
  /* One UI light */
  --oneui-bg: #fafafa;
  --oneui-surface: #ffffff;
  --oneui-on-surface: #000000;
  --oneui-on-surface-variant: #666666;
  --oneui-primary: #0381fe;          /* Samsung blue */
  --oneui-divider: #e0e0e0;

  --oneui-radius-card: 26px;          /* generoso */
  --oneui-radius-button: 22px;
  --oneui-radius-sheet: 30px 30px 0 0;
}
:root[data-theme="dark"] {
  --oneui-bg: #000000;               /* One UI dark é preto puro (AMOLED) */
  --oneui-surface: #1b1b1b;
  --oneui-on-surface: #ffffff;
  --oneui-on-surface-variant: #b3b3b3;
  --oneui-primary: #4d9fff;
}
```

## Tipografia (SamsungOne / One UI Sans)

```css
font-family: 'SamsungOne', 'One UI Sans', 'Roboto', system-ui, sans-serif;
--oneui-header-large: 700 34px/40px;   /* título grande no topo */
--oneui-title: 600 20px/26px;
--oneui-body: 400 16px/22px;
--oneui-caption: 400 13px/18px;
```

## Componentes-chave

```css
.oneui-large-header {           /* colapsa no scroll */
  font: var(--oneui-header-large); padding: 32px 24px 16px;
  color: var(--oneui-on-surface);
}
.oneui-card {
  background: var(--oneui-surface); border-radius: var(--oneui-radius-card);
  padding: 20px; margin: 8px 16px;
}
.oneui-btn {                    /* fica na base da tela */
  background: var(--oneui-primary); color: #fff; border: none;
  border-radius: var(--oneui-radius-button); height: 56px; width: 100%;
  font: 600 17px/1 'SamsungOne'; margin-bottom: 8px;
}
.oneui-bottom-sheet { border-radius: var(--oneui-radius-sheet); background: var(--oneui-surface); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [developer.samsung.com/one-ui](https://developer.samsung.com/one-ui) | Guidelines oficiais One UI (viewing/interaction area, componentes). |
| [Samsung Design](https://design.samsung.com/) | Filosofia de marca, cor, motion. |
| [One UI на GitHub — OneUI design refs](https://developer.samsung.com/one-ui/component.html) | Especificação de componentes. |
| [Material Symbols](https://fonts.google.com/icons) | Base de ícones Android (One UI é sobre Android). |
| ../_shared/design-resources.md | Contraste AMOLED, acessibilidade, fontes fallback. |

## Do / Don't

| Do | Don't |
|---|---|
| Ações primárias na base | Botão crítico no topo (fora do alcance) |
| Header grande que colapsa | App bar pequena e estática |
| Preto puro no dark (AMOLED) | Cinza escuro que "vaza" luz |
| Cantos ~26px | Cantos retos |

## Checklist

- [ ] Controles principais na metade inferior
- [ ] Large collapsing header no topo
- [ ] Dark mode = preto puro (#000)
- [ ] Radius generoso em cards/sheets
- [ ] Touch targets ≥ 48px, botões base ≥ 56px
- [ ] Alto contraste (texto sobre AMOLED)
