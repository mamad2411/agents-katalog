---
name: perflab-view-transitions
description: Guidance on the View Transitions (Experimental) module. Use when configuring or troubleshooting the SPA-like page transition animations.
---

# Performance Lab: View Transitions (Experimental)

This module utilizes the new CSS View Transitions API to create seamless, animated transitions between page loads, making a standard multi-page WordPress site feel like a Single Page Application (SPA).

## Browser Support
The View Transitions API is relatively new. Browsers that do not support it will simply fall back to standard page loads without the animation.

## Customizing Transitions
By default, the plugin applies a subtle cross-fade. Theme developers can customize these animations using the `::view-transition-*` CSS pseudo-elements to create complex slide, scale, or morph effects.

## Conflicts
Since View Transitions "freeze" the visual state of the DOM, they can sometimes cause visual glitches with complex JavaScript animations or sticky headers that shift positions during load.
