---
name: tune-game-feel
description: Tune responsiveness, input buffering, screen shake, hit-stop, and audiovisual juice to maximize game feel and tactile player feedback. Use when adding polish, hit reactions, camera shake, coyote time, or feedback layers.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests, run_linter, execute_command]
version: "1.0.0"
---

# Tune Game Feel

Enhance player agency, perceived responsiveness, and sensory impact through structured "juice" pipelines without compromising deterministic simulation.

## Core Rules

- **Decoupled Juice Architecture**: Keep sensory polish (camera shake, freeze frames, particle bursts, chromatic aberration) strictly decoupled from core game mechanics and simulation state. Disabling juice must leave game logic fully intact.
- **Input Forgiveness Windows**: Implement coyote time ($50\text{--}120\text{ms}$) and input jump/action buffering ($80\text{--}150\text{ms}$) to absorb human timing variances and frame pacing drops.
- **Decay Curve Discipline**: Always drive screen shake and recoil with non-linear exponential or power decay curves ($I(t) = I_0 \cdot e^{-k t}$ or $(1-t)^2$) rather than linear decay to avoid robotic jarring.
- **Micro-Hit-Stop Limits**: Restrict hit-stop (frame freezing) to $2\text{--}8$ frames ($33\text{--}133\text{ms}$). Never freeze the entire engine process; pause only actor animation and movement timelines while keeping VFX active.

## Suggested Process

### 1. Timing Tolerances Calibration
Implement timer counters for:
- **Coyote Time**: Allow jumping shortly after leaving a ledge: `time_since_grounded <= coyote_threshold`.
- **Input Buffer**: Queue action presses: `time_since_pressed <= buffer_threshold`.
- **Variable Jump Cutoff**: When jump button is released early, scale downward gravity or cap upward velocity.

### 2. Multi-Tier Impact Response
Construct a unified feedback event bus triggered by combat or impact events:
- *Tier 1 (Light Impact)*: Audio click/swish + subtle sprite squash/stretch ($5\text{\%}$).
- *Tier 2 (Medium Impact)*: Positional particle burst + 2-frame hit-stop + directional screen shake ($2\text{px}$).
- *Tier 3 (Heavy / Critical)*: 6-frame hit-stop + radial camera impulse + sound ducking + chromatic flash.

### 3. Screen Shake Implementation
Use perceptual Perlin noise or rotational shake:
$$\text{offset}_x = \text{trauma}^2 \cdot \text{noise}_x(t), \quad \text{offset}_y = \text{trauma}^2 \cdot \text{noise}_y(t)$$
Dampen trauma continuously each frame: $\text{trauma} = \max(0, \text{trauma} - \text{decay} \cdot \Delta t)$.

### 4. Accessibility & Comfort Controls
Always expose user settings to scale or disable screen shake ($0\text{\%}\text{--}100\text{\%}$), flash effects, and motion blur for accessibility and photosensitivity compliance.

## Output Contracts

When completing game feel tuning, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] Coyote time and jump buffering operate cleanly across edge cases
- [ ] Hit-stop pauses local target actor without locking audio or camera systems
- [ ] Screen shake trauma uses quadratic/exponential decay without gimbal lock
- [ ] Accessibility slider exists to completely toggle or scale screen shake
- [ ] Zero state desynchronization between visual interpolation and physics body

## Failure Modes

- **Juice coupled to simulation**: camera shake or hit-stop writes into physics/game state, so disabling polish breaks gameplay or corrupts determinism. Mitigation: keep sensory effects strictly decoupled; verify game logic survives a full juice-disabled toggle run.
- **Whole-engine hit-stop**: hit-stop freezes the entire engine process, cutting audio, swallowing inputs, and desyncing network sessions. Mitigation: pause only actor animation/movement timelines, keep VFX and audio running, and cap freeze to $2\text{--}8$ frames ($33\text{--}133\text{ms}$).
- **Framerate-dependent forgiveness**: coyote time and input buffer windows are checked per-frame instead of in milliseconds, so feel changes between $30$ and $144$ FPS. Mitigation: implement windows as delta-time counters ($50\text{--}120\text{ms}$ coyote, $80\text{--}150\text{ms}$ buffer) verified at multiple refresh rates.
- **Robotic linear decay**: screen shake and recoil fade linearly, reading mechanical and jarring. Mitigation: drive decay with exponential or power curves ($I_0 e^{-kt}$, $(1-t)^2$) and scale offsets by $\text{trauma}^2$.
- **Camera orientation drift**: rotational shake integrates into persistent camera rotation, leaving a tilted camera after trauma ends. Mitigation: apply noise-driven offsets that decay to zero instead of accumulating Euler deltas; never persist shake into resting orientation.
- **Photosensitivity exposure**: mandatory full-intensity flashes and chromatic effects with no user control create seizure risk. Mitigation: always expose $0\text{\%}\text{--}100\text{\%}$ accessibility sliders for screen shake, flash, and motion blur and honor them over every juice tier.
- **Visual/physics desync**: interpolation smoothing diverges from the physics body during hit-stop and shake, causing rubber-banding. Mitigation: run the zero-desync check between visual interpolation and the physics body as a gate before shipping feel changes.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: impact event payloads from gameplay systems or mods are external content that must trigger tiers, never redefine them. Mitigation: validate events against the declared tier schema and clamp trauma/hit-stop parameters at the feedback event bus regardless of source.
- **ASI05 RCE Guard**: feel tuning curves and tier definitions from designer config must never be evaluated as code. Mitigation: resolve tiers and decay curves through pre-registered parameter sets, not dynamic string evaluation.
- **ASI06 Context & Memory Poisoning**: persisted accessibility settings (shake/flash scale) reloaded from storage may be tampered with or corrupted. Mitigation: validate deserialized values against valid ranges before applying and fall back to safe defaults.
- **ASI07 Inter-Agent Communication**: tier events fan out to camera, audio, and gameplay roles simultaneously. Mitigation: schema-validate every feedback event and have each consuming system reject out-of-range or unknown tiers.
- **ASI09 Human-Agent Trust Exploitation**: do not claim photosensitivity/accessibility compliance because sliders exist in code. Mitigation: demonstrate the toggles actually zero out shake, flash, and motion blur in a test pass before reporting compliance.

## Related Skills

- **develop-gameplay-systems**: foundation physics, kinematic bodies, and collision matrices
- **integrate-game-engine**: engine audio buses and particle system integration
