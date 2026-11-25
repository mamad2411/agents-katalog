---
name: algorithmic-art
description: Create generative algorithmic art using p5.js. Use when user wants to create generative art, algorithmic art, creative coding, p5.js sketches, procedural art, or visual art through code. The skill produces self-contained interactive HTML artifacts with seeded randomness and parameter controls.
---

# Algorithmic Art Generation Skill

A framework for creating generative art using p5.js in two phases: computational philosophy, then visual expression.

## Core Process

### Phase 1: Algorithmic Philosophy

Create a computational aesthetic movement (4-6 paragraphs) describing how beauty emerges through:
- Mathematical relationships and noise functions
- Particle behaviors and field dynamics
- Emergent complexity from simple rules
- Seeded variation enabling reproducibility

The philosophy must emphasize "meticulously crafted algorithm" and expert-level computational artistry.

### Phase 2: p5.js Implementation

Express the philosophy through interactive HTML artifacts using a viewer template as foundation. Keep fixed UI elements while replacing the algorithm and parameters.

## Key Technical Requirements

### Seeded Randomness
All work must use consistent seeds for reproducibility, following the "Art Blocks pattern" of deterministic generation:
```javascript
// Use p5.js random seed
randomSeed(seed);
noiseSeed(seed);
```

### Parameter Design
Create tunable controls that emerge naturally from the algorithmic philosophy rather than predetermined pattern types.

### Single Artifact Structure
Self-contained HTML files embedding p5.js (via CDN), all algorithms inline, no external dependencies.

## Fixed vs. Variable Elements

**Always Maintain**:
- Anthropic branding (Poppins/Lora fonts, light theme)
- Sidebar structure (Seed controls, Parameters, optional Colors, Actions)
- Seed navigation (Previous/Next/Random/Jump functionality)

**Always Customize**:
- The p5.js algorithm itself
- Parameter definitions and ranges
- UI controls matching the art's needs
- Visual implementation expressing the philosophy

## Essential Principle

"The algorithm flows from the philosophy, not from a menu of options." Each work should feel like it emerged through countless iterations by someone at the absolute top of their field in computational aesthetics.

## Artifact Template Structure

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Lora:ital@0;1&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
  <style>
    /* Anthropic brand: light theme, Poppins headings, Lora body */
    :root {
      --dark: #141413;
      --light: #faf9f5;
      --accent: #d97757;
    }
  </style>
</head>
<body>
  <!-- Sidebar: seed controls + algorithm parameters -->
  <!-- Canvas: p5.js sketch -->
  <script>
    let seed = Math.floor(Math.random() * 10000);

    function setup() {
      // Initialize canvas
      randomSeed(seed);
      noiseSeed(seed);
    }

    function draw() {
      // Algorithm expressed from philosophy
    }
  </script>
</body>
</html>
```
