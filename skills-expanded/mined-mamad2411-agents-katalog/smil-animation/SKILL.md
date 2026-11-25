---
name: smil-animation
description: Create self-contained, script-free SVG animations and interactive logic using SMIL 3.0. Use when building interactive icons, ambient backgrounds, or complex transitions without CSS or JS overhead.
# argument-hint: "[animation-type]"
allowed-tools: Read, Grep, Glob
---

# SMIL 3.0 Declarative Animation & Logic

## Purpose
Expert implementation of [SMIL 3.0](https://www.w3.org/TR/SMIL3/) for self-contained, script-free animations and interactive event handling within SVGs. This skill enables complex multi-step logic and synchronization between independent elements that CSS cannot easily handle.

## Invocation
- **Manual**: /smil-animation [animate|transform|motion]
- **Automatic**: Triggered when requests involve "SVG animation", "script-free interaction", or "SVG path morphing".
- **Arguments**: Optional \$0 to specify the primary technique (e.g., motion).

## Prerequisites & Permissions
- Standard workspace read tools (Read, Grep, Glob) for analyzing existing SVGs.
- No special permissions required.

## Workflow
1. **Define the Temporal Logic**:
   - Choose the appropriate element:
     - <animate>: Linear or spline transitions for attributes (radius, color, opacity).
     - <animateTransform>: Spatial changes (rotation, scaling, translation). Use additive="sum" to stack effects.
     - <animateMotion>: Movement along complex bezier paths using <mpath>.
2. **Setup Interactive Event Handling**:
   - Use begin and end attributes to listen to DOM events:
     - Click: begin="elementID.click"
     - Hover: begin="elementID.mouseenter" and end="elementID.mouseleave"
     - Chaining: begin="otherAnimation.end + 2s" for sequencing.
3. **Apply Optimization Techniques**:
   - **Spline Interpolation**: Use calcMode="spline" and keySplines for custom easing curves.
   - **Phase Shifting**: Use prime number durations (e.g., 3.14s, 7.1s) to prevent repetition artifacts in ambient backgrounds.
   - **Path Morphing**: Animate the d attribute (ensure the number of path points remains consistent).

## Examples
### Example 1 — Interactive Icon Transformation
**Command**: User asks for a hamburger menu that turns into an 'X' on click.
**Implementation**:
```xml
<path d="M2,5 L18,5">
  <animate attributeName="d" begin="menu.click" dur="0.2s" fill="freeze" to="M5,5 L15,15" />
</path>
```

### Example 2 — Heartbeat Pulse
**Command**: "Create a heartbeat pulse for this circle."
**Implementation**:
```xml
<circle r="10">
  <animate attributeName="r" values="10;12;10" dur="0.8s" repeatCount="indefinite" />
</circle>
```

## Safety & Guardrails
- **Browser Compatibility**: Note that while widely supported in browsers, some older tools or environments (like certain email clients) may not render SMIL.
- **Complexity**: For extremely heavy animations, suggest performance testing as SMIL runs on the main layout thread of the SVG.
- **Refusal**: Do not use SMIL for security-sensitive logic; it is for presentation and simple interaction only.

## Notes for maintainers
- SMIL 3.0 spec: https://www.w3.org/TR/SMIL3/
- Ensure rotate="auto" is used with animateMotion to align objects to curves.
- Use syncbase values for precise sequencing.
