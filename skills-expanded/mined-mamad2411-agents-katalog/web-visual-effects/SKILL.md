---
name: web-visual-effects
description: Create stunning web visual effects and creative coding experiences using WebGL, WebGPU, shaders, and animation libraries. Use this skill when building GPU-accelerated graphics, scroll-driven animations, particle systems, post-processing effects, glassmorphism, parallax scrolling, or any hardware-accelerated visual experience for the web. Also triggers on "visual effect", "shader", "WebGL", "GLSL", "fragment shader", "particle system", "scroll animation", "parallax", "glassmorphism", "GSAP animation", "post-processing", "bloom effect", "chromatic aberration", "film grain", "liquid distortion", "raymarching", "VFX.js", "PixiJS", "Lottie animation", "smooth scroll", "Lenis", "creative coding", "canvas animation", or any request to build a visually impressive GPU-accelerated web experience.
---

# Web Visual Effects & Creative Coding

Build high-performance, visually stunning web experiences using GPU-accelerated graphics, advanced animation techniques, and creative coding patterns. This skill covers everything from shader-based effects and particle systems to scroll-driven animations and modern UI visual styles.

## Example Prompts

- "Add a liquid distortion hover effect to my hero image."
- "Create a WebGL particle system that reacts to mouse movement."
- "Build a parallax scrolling landing page with smooth scroll."
- "Implement a glassmorphism card component with frosted blur."
- "Add a film grain and vignette post-processing overlay."
- "Create a GSAP scroll-triggered animation sequence."
- "Build a raymarched fractal background in a fragment shader."
- "Add chromatic aberration to my Three.js scene."

---

## 🔧 Project Setup

### CDN Quick Start (no build tools)
```html
<!-- GSAP -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>

<!-- Three.js -->
<script type="importmap">
  { "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170/examples/jsm/"
  }}
</script>

<!-- PixiJS -->
<script src="https://cdn.jsdelivr.net/npm/pixi.js@8/dist/pixi.min.js"></script>

<!-- Lottie -->
<script src="https://cdn.jsdelivr.net/npm/lottie-web@5/build/player/lottie.min.js"></script>

<!-- Lenis Smooth Scroll -->
<script src="https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.min.js"></script>

<!-- VFX.js -->
<script src="https://cdn.jsdelivr.net/npm/vfx-js@1/dist/vfx.min.js"></script>
```

### NPM Installation (framework projects)
```bash
# Animation & scroll
npm install gsap lenis

# 3D / WebGL
npm install three @react-three/fiber @react-three/drei

# 2D engine
npm install pixi.js

# React animation
npm install framer-motion

# Motion design
npm install @theatre/core @theatre/studio

# Lottie
npm install lottie-web

# VFX Effects
npm install vfx-js
```

---

## 🛠 Core Tech Stack

| Technology | Description |
|---|---|
| **WebGL / WebGPU** | Core APIs for hardware-accelerated graphics in the browser. |
| **Three.js** | Industry standard for 3D on the web (Scenes, Cameras, Meshes, Renderers). |
| **React-Three-Fiber (R3F)** | Declarative bridge for using Three.js within React environments. |
| **GSAP (GreenSock)** | Gold standard for high-performance sequencing and timeline-based animations. |
| **Framer Motion** | Declarative animations for React components, layout transitions, and gestures. |
| **VFX-JS** | WebGL-powered effects for standard HTML elements without touching the DOM. Apply displacement, distortion, RGB shift, blur, and transition effects to images, videos, and divs using a unified WebGL canvas overlay. |

---

## 🎨 Visual Techniques & Styles

### Shaders (GLSL)
Custom Vertex and Fragment shaders for liquid distortions, grain, noise, and procedural textures. Write directly in GLSL or use Three.js node materials (TSL) for WebGPU.

### Glassmorphism
Frosted-glass UI effect using `backdrop-filter: blur()` combined with semi-transparent backgrounds and subtle borders.

```css
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

### Neumorphism
Soft, extruded UI using dual `box-shadow` to create a raised or pressed appearance.

```css
.neu-element {
  background: #e0e0e0;
  box-shadow: 10px 10px 20px #bebebe,
             -10px -10px 20px #ffffff;
  border-radius: 12px;
}
```

### Post-Processing
Layered screen-space effects applied after the main render pass:
- **Bloom** — Soft glow on bright areas
- **Chromatic Aberration** — RGB channel offset for a lens-like distortion
- **Vignette** — Darkened edges that focus attention toward the center
- **Film Grain** — Subtle noise overlay for a cinematic texture

### Parallax & Scroll Effects
Multi-layered depth scrolling with elements moving at different rates. Includes horizontal "fake" scroll, sticky-based sequences, and scroll-linked animations using the Scroll Timeline API or Intersection Observer.

### Raymarching
GPU-based technique for rendering complex fractal geometries, volumetric light shafts, and signed distance field (SDF) shapes entirely within a fragment shader.

---

## 🚀 Key Libraries & Tools

| Library | Use Case |
|---|---|
| **Drei** | Helper library for R3F — prebuilt shaders, text, environment maps, gizmos. |
| **Lenis** | High-performance smooth scrolling with momentum and easing. |
| **Theatre.js** | Visual timeline editor for professional, keyframe-based motion design. |
| **VFX-JS** | Adding WebGL-powered effects to standard HTML elements. Handles displacement mapping, RGB shift, liquid distortion, glitch effects, and shader-based transitions without manual canvas management. Perfect for interactive hover states and scroll-driven visual effects. |
| **Lottie** | Rendering Adobe After Effects animations exported as JSON. |
| **Spline** | 3D design tool that exports interactive scenes directly to web code. |

---

## 📐 Math & Logic for VFX

### Interpolation
Use `lerp` (linear interpolation) for smooth value transitions between states. Essential for camera movement, color blending, and eased following behaviors.

```javascript
function lerp(start, end, t) {
  return start + (end - start) * t;
}
```

### Noise Functions
Implement Perlin or Simplex noise for organic, natural-looking movement. Layer multiple octaves (fractal Brownian motion) for terrain, clouds, and fluid effects.

### Trigonometry
Use `Math.sin()` and `Math.cos()` for wave motions, circular paths, oscillation, and pulsing effects. Combine with time-based offsets for phased animation.

### Easing Functions
Custom `cubic-bezier` curves or easing equations to add physical "weight" and personality to animations. Avoid linear motion — ease-in-out, elastic, and bounce add life.

---

## � Implementation Workflow

When building a visual effect, follow this sequence:

1. **Identify the technique** — Is this a shader effect, a DOM animation, a scroll-driven sequence, or a particle system? This determines the tech stack.
2. **Choose the minimal toolset** — Don't load Three.js for a CSS-only parallax. Match library weight to effect complexity.
3. **Scaffold the structure** — Set up the canvas/container, animation loop, and resize handler *before* writing the effect logic.
4. **Build the core effect** — Implement the visual with hardcoded values first. Get it working, then parameterize.
5. **Add interactivity** — Mouse tracking, scroll position, device orientation, or audio input.
6. **Optimize** — Profile frame times, reduce draw calls, add GPU detection, and implement `prefers-reduced-motion` fallbacks.
7. **Polish** — Easing, timing, color harmony, and edge-case handling (resize, tab visibility, mobile).

---

## 📝 Common Recipes

### GSAP Scroll-Triggered Animation
```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

gsap.from('.hero-title', {
  y: 100,
  opacity: 0,
  duration: 1.2,
  ease: 'power3.out',
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top 80%',
    end: 'top 20%',
    toggleActions: 'play none none reverse',
  }
});

// Pin + scrub for cinematic sequences
gsap.to('.panels', {
  xPercent: -100 * (panels.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.panels-container',
    pin: true,
    scrub: 1,
    end: () => `+=${document.querySelector('.panels-container').offsetWidth}`,
  }
});
```

### Lenis Smooth Scroll
```javascript
import Lenis from 'lenis';

const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true,
});

// Connect to GSAP ScrollTrigger
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);
```

### Basic Fragment Shader (fullscreen effect)
```html
<canvas id="shader-canvas"></canvas>
<script>
const canvas = document.getElementById('shader-canvas');
const gl = canvas.getContext('webgl2');

const fragSource = `#version 300 es
precision highp float;
uniform float u_time;
uniform vec2 u_resolution;
out vec4 fragColor;

void main() {
  vec2 uv = gl_FragCoord.xy / u_resolution;
  vec3 col = 0.5 + 0.5 * cos(u_time + uv.xyx + vec3(0, 2, 4));
  fragColor = vec4(col, 1.0);
}`;

const vertSource = `#version 300 es
in vec4 a_position;
void main() { gl_Position = a_position; }`;

// Compile, link, fullscreen quad, and animate...
</script>
```

### Canvas Particle System Skeleton
```javascript
class Particle {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.vx = (Math.random() - 0.5) * 2;
    this.vy = (Math.random() - 0.5) * 2;
    this.life = 1.0;
    this.decay = 0.003 + Math.random() * 0.008;
    this.size = 2 + Math.random() * 4;
  }

  update() {
    this.x += this.vx;
    this.y += this.vy;
    this.life -= this.decay;
  }

  draw(ctx) {
    ctx.globalAlpha = this.life;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill();
  }
}

const particles = [];

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Spawn new particles (e.g., at mouse position)
  for (let i = 0; i < 3; i++) {
    particles.push(new Particle(mouseX, mouseY));
  }

  // Update and draw
  for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].update();
    particles[i].draw(ctx);
    if (particles[i].life <= 0) particles.splice(i, 1);
  }

  requestAnimationFrame(animate);
}
```

### VFX.js Liquid Distortion on Hover
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .vfx-image {
      width: 600px;
      height: 400px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <img class="vfx-image" src="hero.jpg" alt="Hero">
  <script src="https://cdn.jsdelivr.net/npm/vfx-js@1/dist/vfx.min.js"></script>
  <script>
    // Initialize VFX for the image
    const vfxImage = VFX.add(document.querySelector('.vfx-image'), {
      shader: 'rgbShift',
      overflow: 100  // Extra canvas space for displacement overflow
    });

    // Animate on hover
    vfxImage.uniforms.amount = 0.0;
    
    vfxImage.addEventListener('mouseenter', () => {
      vfxImage.uniforms.amount = 0.5;
      vfxImage.uniforms.angle = Math.random() * Math.PI * 2;
    });
    
    vfxImage.addEventListener('mouseleave', () => {
      vfxImage.uniforms.amount = 0.0;
    });
  </script>
</body>
</html>
```

### VFX.js Displacement Map Effect
```javascript
import VFX from 'vfx-js';

// Add displacement effect using a noise texture
const hero = VFX.add(document.querySelector('.hero-image'), {
  shader: 'displacement',
  overflow: 200,
  map: 'noise-texture.jpg'  // Displacement map (white = max displacement)
});

// Animate displacement strength on scroll
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  hero.uniforms.amount = Math.min(scrollY / 500, 1.0);
});
```

### VFX.js Custom Shader
```javascript
import VFX from 'vfx-js';

// Register a custom shader
VFX.registerShader('waterRipple', {
  uniforms: {
    time: { value: 0.0 },
    amplitude: { value: 0.02 },
    frequency: { value: 10.0 }
  },
  fragmentShader: `
    uniform sampler2D texture;
    uniform vec2 resolution;
    uniform float time;
    uniform float amplitude;
    uniform float frequency;
    varying vec2 vUv;

    void main() {
      vec2 uv = vUv;
      
      // Create ripple distortion
      float dist = length(uv - 0.5);
      float ripple = sin(dist * frequency - time * 3.0) * amplitude;
      
      vec2 offset = normalize(uv - 0.5) * ripple;
      vec2 distortedUv = uv + offset;
      
      gl_FragColor = texture2D(texture, distortedUv);
    }
  `
});

// Apply custom shader
const element = VFX.add(document.querySelector('.water-image'), {
  shader: 'waterRipple'
});

// Animate time uniform
function animate() {
  element.uniforms.time = performance.now() * 0.001;
  requestAnimationFrame(animate);
}
animate();
```

### VFX.js Image Sequence Transition
```javascript
import VFX from 'vfx-js';
import { gsap } from 'gsap';

// Create transition between two images
const container = document.querySelector('.image-container');
const img1 = container.querySelector('.image-1');
const img2 = container.querySelector('.image-2');

const transition = VFX.add(container, {
  shader: 'displacement',
  map: 'displacement-map.jpg',
  overflow: 150
});

// Transition animation
function transitionImages() {
  gsap.timeline()
    .to(transition.uniforms, {
      amount: 1.0,
      duration: 1.2,
      ease: 'power2.inOut'
    })
    .set(img1, { opacity: 0 })
    .set(img2, { opacity: 1 })
    .to(transition.uniforms, {
      amount: 0.0,
      duration: 1.2,
      ease: 'power2.inOut'
    });
}

// Trigger every 5 seconds
setInterval(transitionImages, 5000);
```

### VFX.js Mouse-Reactive Distortion
```javascript
import VFX from 'vfx-js';

const image = VFX.add(document.querySelector('.interactive-image'), {
  shader: 'rgbShift',
  overflow: 100
});

let mouseX = 0, mouseY = 0;
let targetX = 0, targetY = 0;

// Track mouse position
image.addEventListener('mousemove', (e) => {
  const rect = e.target.getBoundingClientRect();
  targetX = (e.clientX - rect.left) / rect.width - 0.5;
  targetY = (e.clientY - rect.top) / rect.height - 0.5;
});

image.addEventListener('mouseleave', () => {
  targetX = 0;
  targetY = 0;
});

// Smooth interpolation
function animate() {
  mouseX += (targetX - mouseX) * 0.1;
  mouseY += (targetY - mouseY) * 0.1;
  
  // Map mouse position to effect parameters
  image.uniforms.amount = Math.sqrt(mouseX * mouseX + mouseY * mouseY) * 0.8;
  image.uniforms.angle = Math.atan2(mouseY, mouseX);
  
  requestAnimationFrame(animate);
}
animate();
```

### VFX.js Multi-Effect Layer
```javascript
import VFX from 'vfx-js';

// Layer multiple effects on the same element
const element = document.querySelector('.multi-effect');

// Effect 1: Base RGB shift
const layer1 = VFX.add(element, {
  shader: 'rgbShift',
  overflow: 50
});

// Effect 2: Film grain overlay
const layer2 = VFX.add(element, {
  shader: 'noise',
  overflow: 0
});

// Sync both effects
function animate() {
  const time = performance.now() * 0.001;
  
  // Pulsing RGB shift
  layer1.uniforms.amount = 0.3 + Math.sin(time) * 0.2;
  
  // Animated grain
  layer2.uniforms.time = time;
  layer2.uniforms.amount = 0.15;
  
  requestAnimationFrame(animate);
}
animate();
```

### VFX.js Glitch Effect
```javascript
import VFX from 'vfx-js';

const glitchElement = VFX.add(document.querySelector('.glitch-img'), {
  shader: 'glitch',
  overflow: 80
});

// Trigger random glitch bursts
function triggerGlitch() {
  const intensity = Math.random() * 0.8 + 0.2;
  const duration = 100 + Math.random() * 200;
  
  glitchElement.uniforms.amount = intensity;
  glitchElement.uniforms.seed = Math.random();
  
  setTimeout(() => {
    glitchElement.uniforms.amount = 0;
  }, duration);
  
  // Next glitch in 2-6 seconds
  setTimeout(triggerGlitch, 2000 + Math.random() * 4000);
}

triggerGlitch();
```

### Three.js Post-Processing Pipeline
```javascript
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { FilmPass } from 'three/addons/postprocessing/FilmPass.js';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));

// Bloom
const bloom = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  0.8,  // strength
  0.4,  // radius
  0.85  // threshold
);
composer.addPass(bloom);

// Film grain + scanlines
const film = new FilmPass(0.25, false);
composer.addPass(film);

// In animation loop: composer.render() instead of renderer.render()
```

---

## 🐛 Debugging & Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Animation stutters / drops frames | Layout thrashing; animating `width`, `top`, `left` | Animate only `transform` and `opacity`. Use `will-change` sparingly. |
| WebGL context lost | Too many active canvases or GPU memory exhaustion | Listen for `webglcontextlost` event; reduce texture sizes; dispose unused resources. |
| `backdrop-filter` not working | Missing vendor prefix or stacking context issue | Add `-webkit-backdrop-filter`. Ensure no ancestor has `overflow: hidden` clipping the blur. |
| Scroll animation fires too early/late | Incorrect ScrollTrigger `start`/`end` values | Use `markers: true` in dev to visualize trigger points. |
| Shader won't compile | GLSL syntax error or precision mismatch | Check `gl.getShaderInfoLog(shader)` for line-level errors. Ensure `precision highp float;` is declared. |
| Particles lag on mobile | Too many particles for device GPU | Detect device with `navigator.hardwareConcurrency` or viewport width; scale particle count down. |
| Lenis scroll conflicts with modals | Smooth scroll intercepts all wheel events | Call `lenis.stop()` when opening modals; `lenis.start()` when closing. |
| GSAP animations not reversing on scroll-back | Wrong `toggleActions` configuration | Use `toggleActions: 'play none none reverse'` or `scrub: true` for bidirectional. |
| VFX.js element not displaying | VFX canvas not positioned correctly or overflow too small | Increase `overflow` parameter (e.g., `overflow: 100`). Ensure parent has `position: relative`. |
| VFX.js effects appear pixelated | Canvas resolution doesn't match device pixel ratio | VFX.js auto-detects DPR. Check if CSS is scaling the element; use native size when possible. |
| VFX.js performance drops on mobile | Too many VFX instances or complex shaders | Limit VFX to hero sections only. Disable on mobile with `if (window.innerWidth > 768)` check. |
| VFX.js displacement not visible | Displacement map is uniform (all same color) | Use high-contrast displacement maps. White = max displacement, black = no displacement. |

---

## �📋 Best Practices

- **Performance**: Always use `requestAnimationFrame` for render and animation loops. Never use `setInterval` or `setTimeout` for frame-driven updates.
- **Accessibility**: Respect `prefers-reduced-motion` media queries. Provide reduced or static alternatives for users who disable motion.
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
- **Responsive VFX**: Scale particle counts, resolution, and effect complexity based on device DPI, viewport size, and GPU capabilities. Use `navigator.gpu` or `WEBGL_debug_renderer_info` for GPU detection.
- **Memory Cleanup**: Properly dispose of geometries, materials, textures, and render targets in Three.js to prevent memory leaks. Call `.dispose()` on resources when removing objects from scenes.
- **Progressive Enhancement**: Layer effects on top of functional baselines. The page should work without WebGL; effects enhance, not gatekeep.
- **Frame Budget**: Target 16ms per frame (60fps). Profile with browser DevTools Performance panel. Offload heavy computation to Web Workers or GPU compute shaders.
- **VFX.js Optimization**: Only apply VFX to elements that need it (hero images, CTAs). Remove VFX instances with `.remove()` when elements leave the DOM. Use the `overflow` parameter conservatively — larger values = more GPU memory.
- **Displacement Maps**: Use grayscale images for displacement maps. Resolution should match or exceed the target element. Pre-compress displacement maps — they don't need to be high quality, just high contrast.

---

## ⚠️ Safety & Guardrails

- **Refuse seizure-inducing effects**: Never create rapidly flashing content (>3 flashes/second). This violates WCAG 2.3.1 and can cause photosensitive seizures.
- **Always provide motion fallbacks**: Every animation must have a `prefers-reduced-motion` alternative. No exceptions.
- **Warn about mobile performance**: If an effect requires heavy GPU usage (raymarching, >1000 particles, complex shaders), explicitly note that it may not perform well on mobile and provide a simpler fallback strategy.
- **Don't hide content behind effects**: Visual effects should enhance, never gatekeep. Core content must be accessible if WebGL fails, JS is disabled, or the effect is reduced.
- **Respect battery life**: Avoid infinite high-FPS animation loops on content that's not in view. Use Intersection Observer to pause off-screen effects.
- **Warn about bundle size**: Flag when adding large libraries (Three.js ~150KB gzipped, GSAP ~25KB) and suggest tree-shaking or lighter alternatives when possible.

---

## 📚 Resources & Documentation

| Resource | URL |
|---|---|
| Three.js Docs | https://threejs.org/docs/ |
| Three.js Examples | https://threejs.org/examples/ |
| GSAP Docs | https://gsap.com/docs/v3/ |
| GSAP ScrollTrigger | https://gsap.com/docs/v3/Plugins/ScrollTrigger/ |
| Shader Tutorial (Book of Shaders) | https://thebookofshaders.com/ |
| WebGL Fundamentals | https://webglfundamentals.org/ |
| PixiJS Docs | https://pixijs.com/docs |
| Framer Motion Docs | https://motion.dev/docs |
| Lenis Docs | https://lenis.darkroom.engineering/ |
| Theatre.js Docs | https://www.theatrejs.com/docs |
| Lottie Web | https://airbnb.io/lottie/ |
| MDN Web Animations API | https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API |
| CSS Scroll-Driven Animations | https://scroll-driven-animations.style/ |
| VFX.js GitHub | https://github.com/vfx-js/vfx |
| VFX.js Examples | https://vfx-js.github.io/ |

### Version & Compatibility Notes

- **Evolving specs**: The Web Animations API, Scroll Timeline API, and View Transitions API are actively evolving — check browser support before recommending for production.
- **Three.js versioning**: Three.js has breaking changes between minor versions. Pin CDN imports to specific versions (e.g., `@0.170`).
- **GSAP licensing**: GSAP is now a Webflow product and all plugins (ScrollTrigger, ScrollSmoother, SplitText, MorphSVG, DrawSVG, Flip, Observer, InertiaPlugin) are free. Register plugins before use: `gsap.registerPlugin(ScrollTrigger)`.
- **WebGPU maturity**: WebGPU is stable in Chrome/Edge but still emerging in Firefox/Safari. Always include a WebGL fallback when using WebGPU features.

---

## Related Skills

### threejs-3d-webgpu
The Three.js 3D pipeline skill — scene graphs, cameras, geometries, materials, PBR lighting, model loading, and TSL/WebGPU compute. web-visual-effects often *uses* Three.js (post-processing, particles, shaders), but the full 3D scene workflow lives there.

**Use threejs-3d-webgpu instead when:** the project is primarily a 3D scene with objects, cameras, and lighting rather than a screen-space visual effect layered on top of a web page.

### gsap
Professional JavaScript animation — tweens, timelines, Flip, Observer, SplitText, and MorphSVG. GSAP is the most-used animation library in this skill's recipes.

**Use alongside this skill when:** the visual effect involves sequenced timelines, text reveals, layout transitions, or any animation that benefits from GSAP's easing and synchronisation model.

### gsap-scrolltrigger
Scroll-driven animations using GSAP ScrollTrigger — pinning, scrubbing, snap points, parallax, and horizontal scrolling. Many web-visual-effects recipes are scroll-triggered.

**Use alongside this skill when:** the effect is tied to scroll position, sections need to pin during animation, or the page tells a story as the user scrolls.

### animation-specialist
Broad motion design expertise: easing theory, spring dynamics, CSS animations, Web Animations API, SVG morphing, and GSAP timelines. Useful when the right animation approach hasn't been decided or when the effect spans multiple techniques.

**Use instead of this skill when:** the user needs help choosing between CSS, GSAP, SVG animation, or p5 for a visual goal — and the answer isn't clearly GPU-accelerated or WebGL-based.

### css-design
Expert CSS including `@keyframes`, transitions, `animation-timeline`, scroll-driven CSS animations, and `prefers-reduced-motion`. CSS handles glassmorphism, neumorphism, basic parallax, and simple entrance animations without any JavaScript.

**Use instead of this skill when:** the visual effect can be achieved with `backdrop-filter`, CSS transforms, or the native `scroll()` / `view()` animation-timeline — no JavaScript or canvas required.

### physics
Numerical integration, spring systems, rigid bodies, soft bodies (PBD), and SPH fluids — framed as time-stepped simulation loops. GPU particle systems and physically-based animations benefit from understanding the underlying simulation math.

**Use alongside this skill when:** the particle system needs realistic force-based behaviour (gravity, drag, attraction, collisions) rather than pure procedural noise-driven motion.

### trigonometry
Sin/cos/atan2, circular motion, oscillation, polar coordinates, and wave functions. Nearly every shader and animation loop in this skill uses trig.

**Use alongside this skill when:** a shader or animation involves wave-based motion, radial patterns, circular orbits, or any periodic behaviour driven by `sin(time)`.

### p5js-creative-coding
Generative and creative coding using p5.js — 2D canvas drawing, Perlin noise, interactive sketches, and particle systems without a 3D scene graph or WebGL pipeline.

**Use instead of this skill when:** the user wants to prototype a generative or interactive canvas experience quickly without setting up WebGL, Three.js, or a build pipeline.

### svg-graphics
Scalable SVG graphics, SMIL animation, CSS SVG transforms, path morphing, and accessible diagrams. SVG animations are the right choice when the effect is icon-scale, needs to be inline in HTML, or must work in contexts where canvas/WebGL isn't available.

**Use instead of this skill when:** the animation is an icon, illustration, or diagram that should scale infinitely and doesn't need GPU acceleration.

### frontend-design
Creative direction and full interface implementation — layout, typography, colour systems, and component design as a unified whole.

**Use before this skill when:** the visual effects need to sit inside a polished web page and the overall design direction (colour palette, typography, layout) hasn't been established yet.