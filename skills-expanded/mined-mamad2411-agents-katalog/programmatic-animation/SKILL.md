---
name: programmatic-animation
description: Advanced Framer Motion and cinematic React animation guidelines.
---

# Programmatic UI Animation (Framer Motion)

## Cinematic Principles
- **Spring Physics**: Use physics-based springs instead of linear generic timings. E.g., `transition={{ type: "spring", stiffness: 300, damping: 30 }}`.
- **Orchestration**: Leverage `staggerChildren` and `delayChildren` to create sequential loading reveals across dashboards to simulate high processing power.
- **Performance**: Animate only compositing CSS properties (`transform`, `opacity`). Never animate `width`, `height`, or `margin` directly unless using Layout Animations (`<motion.div layout>`).

## Agentic Interface Triggers
- Tie visual animations to WebSocket events. If an agent emits a `CRITICAL` alert, use a `<motion.div>` overlay with a pulsing red `boxShadow` to represent the system state changing visually.
