---
name: spectrum-design
description: >
  Design no padrão Adobe Spectrum: tokens rigorosos, tipografia Adobe Clean, escala de cinzas
  precisa, azul de acento #1473E6, densidades adaptáveis e acessibilidade forte para apps
  criativos/produtividade. Use quando o usuário mencionar: "Spectrum", "Adobe", "estilo Adobe",
  "app criativo", "ferramenta de design", "design system Adobe", "UI de produtividade". Consulta
  ../_shared/design-resources.md.
---

# Adobe Spectrum

Você atua como designer que domina o Spectrum — o design system da Adobe (Photoshop web, Creative Cloud, Firefly). É **preciso, neutro e acessível**: cinzas calibrados que deixam o trabalho criativo do usuário ser a cor da tela.

## Princípios

1. **Neutro para o conteúdo brilhar** — em ferramentas criativas a UI é cinza; a arte do usuário é a cor. Acento azul só para ação/seleção.
2. **Tokens e escalas rígidas** — cor, tipografia, espaço e tamanho vêm de escalas nomeadas (gray-50…gray-900); nada solto.
3. **Densidade adaptável** — o mesmo componente em tamanhos S/M/L/XL para densidades diferentes (desktop denso vs touch).
4. **Acessibilidade de primeira** — Spectrum é referência em contraste, foco e ARIA.

## Design tokens

```css
:root {                              /* Light */
  --spectrum-gray-50: #ffffff;
  --spectrum-gray-100: #f8f8f8;
  --spectrum-gray-200: #e6e6e6;
  --spectrum-gray-400: #b3b3b3;
  --spectrum-gray-700: #4b4b4b;
  --spectrum-gray-800: #2c2c2c;
  --spectrum-gray-900: #131313;
  --spectrum-blue: #1473e6;          /* accent / CTA */
  --spectrum-blue-hover: #0d66d0;
  --spectrum-red: #d7373f;
  --spectrum-green: #268e6c;
  --spectrum-radius: 4px;
}
:root[data-theme="dark"] {           /* Spectrum "darkest" */
  --spectrum-gray-50: #080808;
  --spectrum-gray-100: #1e1e1e;
  --spectrum-gray-200: #2c2c2c;
  --spectrum-gray-800: #e6e6e6;
  --spectrum-gray-900: #ffffff;
  --spectrum-blue: #378ef0;
}
```

## Tipografia (Adobe Clean / fallback)

```css
/* Adobe Clean é proprietária. Fallback próximo: */
font-family: 'Adobe Clean', 'Source Sans 3', -apple-system, 'Segoe UI', sans-serif;
--spectrum-heading: 700 22px/1.3 'Adobe Clean';
--spectrum-body: 400 14px/1.5;       /* padrão */
--spectrum-detail: 500 11px/1.3;     /* labels, uppercase */
```

## Componentes-chave

```css
.spectrum-btn-cta {                  /* accent button */
  background: var(--spectrum-blue); color: #fff; border: none;
  border-radius: 16px;               /* Spectrum usa botões bem arredondados */
  padding: 0 18px; height: 32px; font: 700 14px/1 'Adobe Clean'; transition: background .13s;
}
.spectrum-btn-cta:hover { background: var(--spectrum-blue-hover); }
.spectrum-btn-secondary {
  background: transparent; color: var(--spectrum-gray-800);
  border: 2px solid var(--spectrum-gray-800); border-radius: 16px; height: 32px; padding: 0 18px; font-weight: 700;
}

.spectrum-field {
  border: 2px solid var(--spectrum-gray-400); border-radius: var(--spectrum-radius);
  height: 32px; padding: 0 12px; background: var(--spectrum-gray-50); color: var(--spectrum-gray-800);
}
.spectrum-field:focus { border-color: var(--spectrum-blue); outline: none; }

.spectrum-well { background: var(--spectrum-gray-100); border: 1px solid var(--spectrum-gray-200);
  border-radius: var(--spectrum-radius); padding: 16px; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [spectrum.adobe.com](https://spectrum.adobe.com/) | Especificação completa: cor, tipografia, componentes, tamanhos. |
| [React Spectrum](https://react-spectrum.adobe.com/) | Componentes React acessíveis + hooks (React Aria). |
| [Spectrum Tokens](https://spectrum.adobe.com/page/design-tokens/) | Escalas nomeadas oficiais. |
| [React Aria](https://react-spectrum.adobe.com/react-aria/) | Padrões de acessibilidade de referência (headless). |
| ../_shared/design-resources.md | Acessibilidade, escalas de cinza, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| UI cinza, arte do usuário em foco | UI colorida em app criativo |
| Escalas nomeadas (gray-N) | Cinza ad-hoc |
| Componentes em S/M/L/XL | Um tamanho fixo |
| Foco/ARIA do React Aria | Acessibilidade improvisada |

## Checklist

- [ ] Escala de cinzas calibrada, azul só em acento/seleção
- [ ] Tokens `--spectrum-*` nomeados
- [ ] Botões bem arredondados (radius ~16px)
- [ ] Campos com borda 2px, foco azul
- [ ] Densidades S/M/L conforme contexto
- [ ] Acessibilidade forte + dark mode
