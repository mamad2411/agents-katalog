---
name: vtj-debug-panel
description: Configures Tweakpane debug panels for 3D components. Use when adding debug controls, monitoring component state, or adjusting parameters in real-time via the #debug interface.
---

# vite-threejs Debug Panel (Tweakpane)

## Overview

Creates real-time parameter adjustment panels using Tweakpane. Activated via `#debug` URL hash.

**Core principles:**
- Every tunable parameter gets a control
- Colors must use `view: 'color'`
- Group panels hierarchically (max 3 levels)

## Quick Start

```javascript
constructor() {
  this.experience = new Experience()
  this.debug = this.experience.debug
  
  this.params = { intensity: 1.0, color: '#ffffff' }
  
  if (this.debug.active) {
    this.debugInit()
  }
}

debugInit() {
  this.debugFolder = this.debug.ui.addFolder({
    title: 'Component Name',
    expanded: false,
  })
  
  this.debugFolder.addBinding(this.params, 'intensity', {
    min: 0, max: 10, step: 0.1,
  })
}
```

## When to Use

- Creating new 3D components
- Adding ShaderMaterial uniform controls
- Monitoring runtime state
- Adding action buttons

## Control Types

| Type | Key Config |
|------|------------|
| Number | `min`, `max`, `step` |
| Color | `view: 'color'` (required) |
| 3D Point | `view: 'point3d'` |
| Boolean | No extra config |
| Select | `options: { label: value }` |
| Button | `addButton({ title })` |

**Detailed examples:** See [references/controls.md](references/controls.md)

## ShaderMaterial Integration

All ShaderMaterial uniforms must have debug controls:

```javascript
folder.addBinding(this.params, 'color', { view: 'color' })
  .on('change', (ev) => {
    this.material.uniforms.uColor.value.set(ev.value)
  })
```

**Full patterns:** See [references/shader-debug.md](references/shader-debug.md)

## Common Mistakes

- ❌ Colors without `view: 'color'`
- ❌ Direct `this.debug.ui` extraction
- ❌ Calling `debugInit()` without checking `debug.active`
- ❌ Nesting deeper than 3 levels
- ❌ All panels expanded by default

**Complete error catalog:** See [references/common-mistakes.md](references/common-mistakes.md)

## Quick Reference

| Need | Code |
|------|------|
| Access debug | `this.debug = this.experience.debug` |
| Check active | `if (this.debug.active)` |
| Create folder | `this.debug.ui.addFolder({ title })` |
| Bind parameter | `folder.addBinding(params, 'key', options)` |
| Handle change | `.on('change', callback)` |
| Method name | `debugInit()` |

**Advanced patterns:** See [references/advanced-patterns.md](references/advanced-patterns.md)
