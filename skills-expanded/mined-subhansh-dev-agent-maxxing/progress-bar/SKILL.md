---
name: progress-bar
description: Generate progress bars with animations, gradients, and multi-step indicators.
---

# Progress Bar Component

```css
.progress {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-light));
  border-radius: 3px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  animation: progressShimmer 1.5s infinite;
}

@keyframes progressShimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-lg { height: 10px; border-radius: 5px; }
.progress-sm { height: 3px; border-radius: 2px; }

/* Multi-step */
.progress-steps {
  display: flex;
  gap: 4px;
}

.progress-step {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 2px;
}

.progress-step.complete {
  background: var(--accent);
}

.progress-step.current {
  background: linear-gradient(90deg, var(--accent), rgba(255,255,255,0.3));
}
```

Rules:
- Animate width changes with 0.3s ease
- Show shimmer effect on indeterminate progress
- Multi-step: show completed, current, and remaining
