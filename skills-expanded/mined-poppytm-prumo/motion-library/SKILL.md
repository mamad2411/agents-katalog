# Motion Design Library & Animation System

## 1. Purpose
This skill establishes a formal, robust motion design library and animation system. It ensures that UI motion is meaningful, performant, accessible, and consistently applied using semantic motion tokens, standard duration conventions, and spring physics for natural, velocity-aware interactions.

## 2. Use When
- Developing UI components that require interaction feedback (hover, focus, active states).
- Implementing page or view transitions.
- Choreographing complex, multi-element layout changes.
- Defining a design system's semantic motion tokens.
- Auditing existing animations for performance or accessibility.

## 3. Do Not Use When
- Animating non-composite properties (like `width`, `height`, `top`, `left`, `margin`, `padding`) which trigger layout recalculations, unless strictly required and performance tested.
- Implementing structural logic entirely dependent on animation timing (events must not rely solely on animation end callbacks without fallbacks).
- Designing functional UI that requires >1000ms animation durations, as this degrades perceived performance.

## 4. Required Context
- Understanding of the target platform's rendering engine and compositor behavior.
- Access to the design system's base tokens.
- Clear interaction requirements and user flows.

## 5. Procedure
1. **Define Motion Token Vocabulary:** Establish semantic tokens for durations (micro, small, medium, large), easing curves (productive, expressive), and spring configurations (bouncy, gentle, stiff).
2. **Create Reusable Motion Primitives:** Build abstracted components or utilities for standard patterns (e.g., `fadeIn`, `slideIn`, `scaleIn`, `collapse`, `expand`).
3. **Implement Spring-Based Interactions:** Apply spring physics (mass-spring-damper model) for gesture-driven UI to ensure interruptibility and natural momentum.
4. **Define Choreography Rules:** Establish rules for staggered entrances, cascading exits, and coordinated multi-element sequences to avoid overwhelming the user.
5. **Implement Reduced-Motion Alternatives:** Wrap all animations in checks for `@media (prefers-reduced-motion: reduce)`. Replace spatial motion with opacity crossfades or instant state changes. Never remove interaction feedback entirely.
6. **Performance-Test:** Ensure a consistent 60fps target. Animate only `transform` and `opacity`. Use `will-change` sparingly.
7. **Document:** Provide interactive examples and integration guidelines for the motion library.

## 6. Decision Rules
- **Properties:** Restrict animations to `transform` and `opacity` whenever possible to enable GPU hardware acceleration.
- **Duration:** Never exceed 1000ms for functional UI animations. Use Micro (50-100ms) for feedback, Small (100-200ms) for state changes, Medium (200-400ms) for transitions, Large (400-700ms) for page/route changes.
- **Physics vs. Easing:** Use spring physics for interactive/gesture-driven elements; use cubic-bezier easing for simple, non-interactive state changes or predefined choreography.
- **Accessibility:** Respect `prefers-reduced-motion` without exception.

## 7. Evidence Required
- Code implementation must reference semantic motion tokens, not hardcoded values.
- Lighthouse or Chrome DevTools performance profiles demonstrating 60fps during animations without main-thread blocking.
- A functional test verifying that animations degrade gracefully when `prefers-reduced-motion` is active.

## 8. Output Contract
- A complete set of semantic motion tokens.
- A library of reusable motion primitives and choreographies.
- Verified accessibility support for reduced motion.

## 9. Stop Conditions
- Motion tokens are fully integrated and documented.
- All core interaction primitives perform at 60fps.
- Reduced motion paths have been validated for all animated components.

## 10. Escalation Rules
- Escalate if hardware acceleration cannot be achieved for critical animations.
- Escalate if business requirements demand complex layout animations that consistently drop frames.
