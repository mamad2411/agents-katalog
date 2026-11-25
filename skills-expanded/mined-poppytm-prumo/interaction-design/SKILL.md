---
name: interaction-design
description: Human-computer interaction (HCI) engineering, micro-interaction choreography (Trigger-Rule-Feedback-Loop), Fitts's Law target sizing, latency feedback thresholds, and transition curves.
---

# Interaction Design (IxD) Engineering Contract

## 1. Purpose
Define, choreograph, and audit Human-Computer Interaction (IxD) behaviors across digital product interfaces. Enforce ergonomic motor mechanics (Fitts's Law, Hick's Law), micro-interaction physics (Trigger, Rule, Feedback, Loop/Mode), strict cognitive latency budgets, intuitive affordances and signifiers, and accessible gesture/keyboard interaction patterns.

---

## 2. Use When
- Designing state transition animations, gesture controls (swipe, pinch, drag), and micro-interactions.
- Optimizing target acquisition times and touch ergonometrics on mobile and desktop devices.
- Defining feedback choreography for asynchronous actions (loaders, progress bars, success ripples).
- Crafting keyboard interaction shortcuts and accelerator models (`Cmd+K`, single-key hotkeys).

---

## 3. Do Not Use When
- Designing broad information architecture or sitemaps (use `ux-architecture`).
- Conducting statistical qualitative user interviews (use `interaction-research`).
- Writing raw low-level GPU vertex shaders or 3D rendering pipelines (use `shaders` or `rendering-3d`).

---

## 4. Required Context
Before designing interaction specifications, obtain:
1. **Target Modality**: Mouse + Pointer, Multi-touch mobile, Keyboard-only, or Voice/Assistive.
2. **Context of Use**: Desktop professional focus vs mobile on-the-go distraction vs industrial kiosk.
3. **State Transition Matrix**: Complete inventory of states (idle, hovering, active/pressed, loading, settled, error).
4. **Motion Policy**: Strict compliance with `prefers-reduced-motion` overrides.

---

## 5. Procedure

### Step 1: Ergonomic Target Sizing (Fitts's Law)
1. Calculate target acquisition effort using Fitts's Law:
   $$T = a + b \log_2\left(1 + \frac{D}{W}\right)$$
   where $D$ is distance from cursor/thumb and $W$ is target width along the axis of motion.
2. Ensure touch targets maintain a minimum interactive hit area of $44 \times 44\text{ px}$ (or $24 \times 24\text{ px}$ with $\ge 12\text{ px}$ padding per WCAG 2.2 SC 2.5.8).
3. Place high-frequency primary actions in easily reachable screen zones (thumb zone on mobile; screen edges or persistent headers on desktop).

### Step 2: Micro-Interaction Choreography (Dan Saffer Model)
Structure every micro-interaction around the 4-part architecture:
1. **Trigger**: User initiation (click, tap, hover, scroll) or system event (timer, incoming webhook).
2. **Rules**: Execution constraints determining state flow (e.g. "if field is valid, enable button; else disable").
3. **Feedback**: Sensory confirmation within latency thresholds:
   - $<100\text{ ms}$: Instantaneous optical feedback (button depression, focus ring glow).
   - $<1.0\text{ s}$: Retains user cognitive flow (subtle inline spinner).
   - $>1.0\text{ s}$: Disclose determinate progress bar or animated skeleton.
4. **Loops & Modes**: Contextual persistence (e.g. auto-dismiss toast after 4s; toggle repeat mode).

### Step 3: Animation Timing & Easing Curves
1. Configure duration calibrated to spatial distance:
   - Micro-state changes (hover, press, icon flip): $100\text{ ms} - 200\text{ ms}$.
   - Small overlays (tooltips, dropdown menus): $200\text{ ms} - 250\text{ ms}$.
   - Large surface transitions (modals, slide-out drawers, page transitions): $300\text{ ms} - 400\text{ ms}$.
2. Use natural cubic-bezier acceleration curves:
   - **Standard Easing** (`cubic-bezier(0.2, 0.0, 0.0, 1.0)`): Elements already on screen that change position or size.
   - **Deceleration / Entering** (`cubic-bezier(0.0, 0.0, 0.2, 1.0)`): Elements entering the screen.
   - **Acceleration / Exiting** (`cubic-bezier(0.4, 0.0, 1.0, 1.0)`): Elements leaving the screen.

### Step 4: Affordance, Signifiers & Prevention of Slips
1. Provide unambiguous signifiers: interactive elements must not look like static text; static text must not look like clickable pills.
2. Prevent motor slips:
   - Destructive actions require progressive disclosure or typed confirmation.
   - Provide non-blocking Undo windows (toasts with 5-second undo button) rather than intrusive blocking alerts wherever feasible.

### Step 5: Verification & Accessibility Hygiene
1. Guarantee that all pointer interactions have 100% equivalent keyboard shortcuts.
2. Honor `prefers-reduced-motion`: disable spatial translation animations when requested, replacing them with instantaneous cross-fades.

---

## 6. Decision Rules
1. **Never Exceed 400ms Duration**: No functional UI transition should exceed $400\text{ ms}$; sluggish animations frustrate users and degrade perceived performance.
2. **Instant Feedback on Tap**: User input must produce visible feedback within $100\text{ ms}$. Never leave the user wondering if a click registered.
3. **Reversible Actions Prefer Undo Over Confirmation**: Prefer instantaneous action with an Undo window over an interruptive "Are you sure?" modal, except for catastrophic, irreversible data loss.
4. **Respect Motion Preferences**: Never trigger parallax motion or full-screen spins without a user-configured toggle.

---

## 7. Evidence Required
- **Interaction Choreography Matrix**: Detailed specification of trigger, rule, feedback, duration, and easing curve.
- **Latency & Sizing Audit**: Target measurements verifying Fitts's Law minimum hit areas and response times.
- **Keyboard Parity Proof**: Table verifying every gesture/click has an equivalent keyboard mapping.

---

## 8. Output Contract
A production interaction design deliverable must contain:
1. Interaction Design Specification (`templates/interaction-spec.md`).
2. Easing and timing token mappings.
3. State feedback and micro-interaction rules.
4. Accessibility and reduced-motion fallback definitions.

---

## 9. Stop Conditions
- All interactive components define complete state matrices (idle, hover, active, focus, disabled, loading).
- Touch target sizes meet or exceed $44\text{ px}$.
- Animation durations bounded between $100\text{ ms}$ and $400\text{ ms}$.

---

## 10. Escalation Rules
- Escalate to Technical Architecture if device hardware limitations (e.g. low-power mobile CPU) cause jank (<60fps) during transition animations.
- Escalate to Product Management if proposed interaction accelerators conflict with simplicity for novice users.
