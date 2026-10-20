---
name: matterjs-physics
description: "Implement 2D physics interactions with Matter.js — Engine/World setup, Render/Runner configuration, adding bodies and constraints, mouse interaction, and SPA cleanup patterns."
metadata:
  openclaw:
    emoji: "⚛️"
    source: "https://github.com/MengTo/Skills"
---

# Matter.js — 2D Physics Skill

## When to use
- Interactive 2D physics: falling objects, drag interactions, physics-based UI elements
- Canvas-based simulations and games
- Fun, playful UI moments with real physics

## Minimal setup
```html
<script>
  const { Engine, Render, Runner, Bodies, Composite } = Matter;
  const engine = Engine.create();
  const render = Render.create({
    element: document.body, engine,
    options: { width: 800, height: 600, wireframes: false }
  });
  Runner.run(Runner.create(), engine);
  Render.run(render);
  const ground = Bodies.rectangle(400, 610, 810, 60, { isStatic: true });
  const box = Bodies.rectangle(400, 200, 80, 80);
  Composite.add(engine.world, [ground, box]);
</script>
```

## Mouse interaction
```js
const { Mouse, MouseConstraint } = Matter;
const mouse = Mouse.create(render.canvas);
const mc = MouseConstraint.create(engine, { mouse });
Composite.add(engine.world, mc);
render.mouse = mouse;
```

## Common patterns
- `Composite.add(engine.world, [...])` to add bodies
- `render.options.wireframes = false` for solid rendering
- `Runner.run(runner, engine)` for a simple loop

## Cleanup (SPA)
- `Runner.stop(runner)` — stop simulation
- Remove render canvas from DOM
- Clear engine and world references

## Tips for AI Agents
- Ask about viewport size and scaling for the canvas.
- Confirm rendering approach (Matter.Render vs custom renderer).
- Check if mouse/touch drag interaction is needed.
