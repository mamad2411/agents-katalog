---
name: "frontier-design"
description: "Push creative boundaries with frontier design techniques for AI-generated interfaces"
---

# Claude Design — Frontier Capabilities

## When to activate

- Building interactive experiences that go beyond standard UI — 3D, audio, particle effects, or immersive animation
- Pitch deck or product demo needs live interactive elements rather than static screenshots
- Prototyping voice interfaces or WebGL-based visualizations before committing to a full implementation
- Building marketing landing pages where visual distinction is more important than framework compatibility
- Stakeholder demo requires a shareable URL with motion and interactivity, not just a mockup image

## When NOT to use

- Standard business application UI — use the base claude-design skill and export to Claude Code
- Production-grade 3D experiences where quality must match commercial standards — use Three.js or Unity directly
- When client browser compatibility is a requirement — frontier capabilities require modern browsers (Chrome 110+, Safari 16.4+, Firefox 115+); older enterprise environments will have issues
- When the deliverable is a downloadable video file — animated video exports as a shareable URL only; MP4 download is not supported
- When the project is already in Claude Code and the design direction is locked — iterate in code, not in Claude Design

## Instructions

### 3D Interactive Elements

Claude Design generates interactive 3D elements using WebGL. These are embedded in the exported HTML and work without additional dependencies.

Supported patterns:
- Globe visualizations with drag rotation, scroll zoom, and hover tooltips for data overlays
- Product showcases with orbit controls and material or color switching
- Abstract 3D shapes for hero sections (spheres, tori, morphing blobs)
- Data sculptures — 3D bar charts, scatter plots, network graphs in three dimensions

Prompt pattern:

```
"Generate an interactive 3D globe showing [data]. Include: rotation on drag,
zoom on scroll, tooltip on hover showing [data fields], [color scheme].
Export as interactive HTML."
```

Limitation: complex custom shapes with irregular geometry have rough edges. The capability works best for common 3D primitives and well-known visualization types (globes, product cylinders, abstract spheres). Do not attempt highly detailed meshes — hand those to a Three.js implementation in Claude Code.

### Voice Interfaces

Claude Design generates voice interface wireframes and prototypes. Voice processing is simulated in the prototype — waveform animation, state transitions, and response rendering are real; actual audio capture and processing must be wired in Claude Code using the Web Audio API or a provider SDK.

Supported patterns:
- Hold-to-talk mic button with animated waveform during recording state
- Voice-to-action flows: spoken command triggers a UI transition or result render
- Podcast and interview UIs with playback controls and synchronized transcript display
- Voice search interfaces with animated loading state and result list rendering

Prompt pattern:

```
"Design a voice interface for [use case]. Include: mic button with hold-to-talk
interaction, animated waveform during recording, processing/thinking state,
response display area for [result type]. Color: [palette]."
```

Limitation: all voice states in the prototype are click-triggered simulations. To wire real voice: export the Claude Code bundle, implement `getUserMedia()` or your voice SDK in Claude Code, and map SDK events to the state classes already in the generated HTML.

### WebGL Shaders and Particle Effects

For visually distinctive hero sections and background treatments. These export as self-contained HTML with embedded WebGL; no build step required.

Supported patterns:
- Particle systems: floating nodes, connected network graph, fluid-like motion
- Gradient animations: mesh gradients, aurora effects, animated noise fields
- Interactive particle fields that respond to mouse position and movement
- Geometric shader backgrounds — low-poly, voronoi, wave distortion

Prompt pattern:

```
"Create a hero background with a particle network effect. Approximately 150
particles, connected by lines when within 120px of each other, respond to
mouse movement with a gentle pull force. Color palette: [primary] on [background].
Subtle animation, not distracting."
```

Export: interactive HTML. Hand to Claude Code for production cleanup — replace inline `<script>` with a module, move canvas initialization to a component lifecycle hook, and add a `prefers-reduced-motion` media query check.

### Animated Video Scenes

Multi-scene animated sequences for product walkthroughs, explainer animations, and data stories.

Supported patterns:
- Product walkthrough: annotated UI with spotlight animations and step-by-step reveals
- Explainer sequences: icon animations, text reveals, slide transitions
- Data story animations: charts and graphs that build over time with synchronized narration text

Export path: shareable URL only. To capture as video, use a screen recorder (QuickTime, OBS, or Loom) pointed at the shared URL. To embed in a website, use an iframe from the shared URL. MP4 download is not available — do not promise it to clients.

Prompt pattern:

```
"Create a 4-scene animated walkthrough of [product]. Scene 1: [description].
Scene 2: [description]. Scene 3: [description]. Scene 4: [description].
Transitions: slide in from right. Duration: approximately 8 seconds per scene.
Brand colors: [hex values]."
```

### Full Interactive Experiences

Combinations of multiple frontier elements in a single prototype. These are experimental — expect more iteration cycles than single-capability outputs.

Viable combinations:
- Voice input + 3D visualization response (speak a query, 3D chart updates)
- WebGL background + live data binding (particle density driven by a number input)
- Animated video sections + inline interactive controls

Prompt strategy for combined experiences: build each capability separately, validate it, then request the combination. Attempting a full combined experience in a single prompt increases the chance of structural errors in the output.

### Export Strategy for Frontier Designs

| Deliverable | Export path | When to use |
|---|---|---|
| Interactive HTML | Download from Claude Design | Browser demos, direct deploy, iframe embed |
| Claude Code handoff | Export bundle | Production implementation with real APIs |
| Screen recording | Record shared URL | Animated video capture, client presentation |
| Shared URL | Copy from Claude Design | Stakeholder review, async feedback |

When exporting interactive HTML for production use, pass the file to Claude Code with this prompt:

```
"Clean up this Claude Design HTML export for production. Extract inline styles
to a CSS file, move inline scripts to a module, add prefers-reduced-motion
support, and ensure it passes WCAG 2.1 AA contrast checks."
```

### Current Maturity

Stable and reliable:
- Interactive 3D globes and standard product showcase orbits
- Particle network and floating-dot effects
- Voice UI wireframes with simulated state transitions
- CSS and JS-based animated transitions and reveals

Rough edges — expect iteration:
- Complex physics simulations (cloth, fluid, rigid body stacking)
- Custom GLSL shader code beyond common noise patterns
- Real-time external data binding in the exported HTML

Not supported:
- Downloading animated sequences as MP4 or GIF
- Complex multiplayer or real-time collaborative interactions
- WebXR or AR/VR experiences

## Example

Solo founder building a SaaS product demo for an investor meeting. Needs: animated hero, product screenshot carousel with depth, and a voice search prototype — all shareable as a URL.

Step 1 — Build each element separately:

```
Prompt 1 (hero):
"Create a hero section with a particle network background. ~120 particles,
connected within 100px, mouse-responsive. Headline: 'Search your codebase
with voice.' CTA button: 'Try the demo'. Primary: #5B21B6, background: #0F0A1E."

Prompt 2 (carousel):
"Build a product screenshot carousel with 3 slides. Each slide tilts in 3D
on hover (15deg X rotation, subtle shadow depth). Transition: fade + scale.
Use placeholder screenshots. Same brand colors as the hero."

Prompt 3 (voice prototype):
"Design a voice search interface. Hold-to-talk mic button centered on screen.
Animated waveform rings during recording state. 'Processing...' spinner.
Results list fades in below. Simulate: 3-second recording, 1-second processing,
then show 4 mock results."
```

Step 2 — Combine into a single page:

```
"Combine the hero, carousel, and voice interface into a single-page layout.
Order: hero (full viewport), carousel section (centered, 80vw), voice interface
(full viewport, dark background). Add smooth scroll between sections."
```

Step 3 — Export decision:

The demo stays in Claude Design as a shareable URL for the investor meeting. After the meeting, export the Claude Code bundle and wire the voice prototype to the actual search API using the Web Speech API in Claude Code. The particle hero and 3D carousel port directly — no real-API dependency.
