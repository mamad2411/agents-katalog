---
name: hue-rotate-sprite-identity
description: Create distinct named character variants from a single sprite sheet using CSS hue-rotate + data attributes
category: design
triggers:
  - character variants sprite
  - palette swap
  - hue rotation identity
  - npc color variants
tags:
  - css
  - sprite
  - palette-swap
  - game-ui
version: 1.0.0
---

# Hue-Rotate Sprite Identity

Reuse a single sprite sheet as N distinct "named agents" by applying `filter: hue-rotate(Xdeg)` per-instance. Avoids shipping multiple art assets while still giving each entity a readable identity.

## Pattern

Define agents as data objects with color hue + name:

```js
const AGENTS = {
  BUILDER:   { name: 'Blaze', hue: 30,  role: 'Builder'   },  // orange
  PUBLISHER: { name: 'Cielo', hue: 220, role: 'Publisher' },  // blue
  MERGER:    { name: 'Mira',  hue: 140, role: 'Merger'    },  // green
  EXTRACTOR: { name: 'Echo',  hue: 180, role: 'Analyst'   },  // cyan
  CREATOR:   { name: 'Aria',  hue: 280, role: 'Creator'   },  // violet
};
```

Apply via data attribute so CSS keeps the hue mapping declarative:

```css
.char[data-hue="0"]   { filter: drop-shadow(1px 2px 0 #0006) }
.char[data-hue="30"]  { filter: hue-rotate(30deg)  saturate(1.15) drop-shadow(1px 2px 0 #0006) }
.char[data-hue="140"] { filter: hue-rotate(140deg) saturate(1.2)  drop-shadow(1px 2px 0 #0006) }
.char[data-hue="220"] { filter: hue-rotate(220deg) saturate(1.15) drop-shadow(1px 2px 0 #0006) }
/* ... */
```

```js
function applyIdentity(el, agent) {
  el.setAttribute('data-hue', String(agent.hue));
  // Optionally render a name tag under the sprite
  addNameTag(el, agent.name);
}
```

## Why data-attribute over inline style

- CSS rules are cacheable and debuggable in devtools
- Same hue value = same visual treatment — no drift across elements
- Easy to add global tweaks (e.g. `filter: brightness(.8)` at night) without touching JS

## Ensemble scenes

For multi-agent phases (e.g. three agents working together), render each with its own hue to create a readable team:

```js
for (const agent of profile.agents.slice(0, 3)) {
  const el = document.createElement('div');
  el.className = 'char';
  el.setAttribute('data-hue', agent.hue);
  wrapper.appendChild(el);
}
```

Bumping `saturate()` slightly (`1.1`–`1.2`) compensates for the desaturation that `hue-rotate` introduces.

## Limitations

- Character art with multiple hues (e.g. purple outfit + red hair) gets shifted together — the whole image rotates. Designs with a dominant single hue work best.
- `filter: hue-rotate` is GPU-accelerated but compounding filters (hue + saturate + drop-shadow) can tax mobile GPUs. Limit to 5–10 on-screen characters.
- Drop-shadow inside the filter chain uses the rotated color, which is often desirable (tinted shadow matches tinted character).
