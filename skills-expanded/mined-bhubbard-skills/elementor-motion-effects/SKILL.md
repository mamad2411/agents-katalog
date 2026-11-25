---
name: elementor-motion-effects
description: Guides creating and managing advanced motion effects, scroll animations, and interactions in Elementor.
---

# Elementor Motion Effects

This skill provides guidance on utilizing Elementor's advanced Motion Effects to create engaging, dynamic, and interactive web experiences.

## Key Concepts

### 1. Scroll Effects
Scroll Effects allow you to animate elements as the user scrolls up or down the page.
- **Vertical & Horizontal Scroll:** Move elements at different speeds relative to the scroll, creating a parallax effect.
- **Transparency:** Fade elements in or out as they enter or leave the viewport.
- **Blur:** Dynamically blur or unblur elements based on scroll position.
- **Rotate & Scale:** Spin or resize elements during scrolling.
- **Viewport Constraints:** Carefully configure the `Viewport` settings (Bottom to Top) to determine exactly when the animation starts and ends.

### 2. Mouse Effects
Add interactivity based on the user's cursor movement.
- **Mouse Track:** Make elements move in relation to the mouse position (either opposite or towards the mouse).
- **3D Tilt:** Create a subtle 3D hovering effect that reacts to cursor positioning over an element.

### 3. Sticky Elements
Keep essential elements visible while scrolling.
- **Sticky Top/Bottom:** Pin headers, call-to-actions, or sidebars to the edge of the screen.
- **Offset & Effects Offset:** Control the exact position and when secondary effects (like shrinking a logo) should trigger.
- **Stay in Column:** Restrict sticky behavior to the element's parent column, preventing it from overlapping other sections.

### 4. Entrance Animations
Standard animations triggered when an element first appears on the screen.
- **Animation Delay:** Stagger animations for a sequential loading effect.

## Best Practices

- **Performance:** Avoid overloading a single page with too many complex animations, as it can degrade rendering performance and drain mobile batteries.
- **Subtlety:** Motion should enhance the user experience, not distract from the content. Keep animations smooth and purposeful.
- **Mobile Responsiveness:** Always test motion effects on mobile devices. Often, it is best to disable complex scroll or hover effects on small screens for better performance and usability.
- **Accessibility:** Ensure that animations do not trigger motion sickness (consider respecting the `prefers-reduced-motion` media query if implementing custom CSS alongside Elementor).
