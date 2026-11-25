---
name: design-tokens-dtcg
description: Como definir design tokens en el formato W3C DTCG (Design Tokens Community Group) en dev-team - estructura tokens.json ($type, $value, alias), capas primitivo/semantico/componente, modos claro/oscuro, tokens de motion, validacion y generacion de CSS variables / Tailwind con Style Dictionary o script Node. Cargala al crear o mantener tokens.json y DESIGN.md.
---

# Design tokens DTCG (dev-team)

## 1. Formato (W3C DTCG)
```json
{
  "color": {
    "$type": "color",
    "neutral": { "50": { "$value": "#f7f6f3" }, "950": { "$value": "#15161a" } },
    "brand":   { "600": { "$value": "#1f5fbf", "$description": "Acento unico" } },
    "text":    { "primary": { "$value": "{color.neutral.950}" },
                 "muted":   { "$value": "#5b6472" } },
    "surface": { "base": { "$value": "#ffffff" }, "raised": { "$value": "{color.neutral.50}" } },
    "status":  { "success": { "$value": "#1f7a4d" }, "error": { "$value": "#b42318" } }
  },
  "font": {
    "family": { "$type": "fontFamily",
      "display": { "$value": ["Fraunces", "Georgia", "serif"] },
      "text":    { "$value": ["Geist", "system-ui", "sans-serif"] } },
    "size": { "$type": "dimension",
      "sm": { "$value": "14px" }, "md": { "$value": "16px" }, "xl": { "$value": "24px" } },
    "weight": { "$type": "fontWeight", "regular": { "$value": 400 }, "semibold": { "$value": 600 } }
  },
  "space": { "$type": "dimension", "1": { "$value": "4px" }, "2": { "$value": "8px" }, "4": { "$value": "16px" } },
  "radius": { "$type": "dimension", "sm": { "$value": "6px" }, "md": { "$value": "10px" } },
  "shadow": { "$type": "shadow",
    "raised": { "$value": { "color": "#00000014", "offsetX": "0px", "offsetY": "2px", "blur": "8px", "spread": "0px" } } },
  "motion": {
    "duration": { "$type": "duration", "fast": { "$value": "150ms" }, "base": { "$value": "220ms" } },
    "ease":     { "$type": "cubicBezier", "out": { "$value": [0.2, 0.8, 0.2, 1] } }
  },
  "component": {
    "button": { "primary": {
      "bg":   { "$type": "color", "$value": "{color.brand.600}" },
      "text": { "$type": "color", "$value": "#ffffff" } } }
  }
}
```
Reglas: `$type` heredable por grupo; alias `{ruta.al.token}`; `$description` cuando la
intencion no es obvia; nombres semanticos en minusculas con puntos; nada de valores
duplicados (alias, no copia).

## 2. Capas
1. **Primitivos** (`color.neutral.500`, `space.4`): la paleta cruda. Nunca se usan en UI.
2. **Semanticos** (`color.text.primary`, `color.surface.raised`): lo que usa la UI.
3. **Componente** (`component.button.primary.bg`): solo cuando un componente necesita
   desviarse; apuntan a semanticos.

## 3. Modos (claro/oscuro, marcas, densidad)
Conjuntos por modo con la misma estructura semantica: `tokens.light.json` /
`tokens.dark.json` (o `$extensions.modes`). El oscuro se DISEÑA (elevacion por tono),
no se invierte. Los primitivos son compartidos; los semanticos cambian.

## 4. Generacion (una sola fuente)
- Con Style Dictionary (`npm i -D style-dictionary`): transforms `css/variables`
  (`:root{--color-text-primary:...}`) y `js/es6` para Tailwind (`theme.extend`).
- Sin dependencias: `scripts/build-tokens.mjs` que recorre `tokens.json`, resuelve alias
  y emite `tokens.css` (+ `[data-theme="dark"]`) y `tailwind.tokens.js`. Nunca editar
  los generados a mano.

## 5. Validacion
JSON valido · todo alias resuelve · sin tokens huerfanos (busca su uso en el prototipo) ·
contraste de pares texto/superficie calculado · `$type` correcto (`color`, `dimension`,
`fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `shadow`, `number`).

## 6. Puente con herramientas
Figma Variables ↔ DTCG (import/export via MCP o plugins Tokens Studio) · Pencil y Penpot
leen JSON de tokens · `DESIGN.md` documenta los semanticos con su intencion para que los
agentes no inventen valores.
