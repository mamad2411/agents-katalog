---
name: jetpack-boost-js-deferral
description: Debug and optimize JavaScript deferral and concatenation in Jetpack Boost to improve First Input Delay (FID) and page load times.
---

# Jetpack Boost - JavaScript Deferral and Optimization

This skill focuses on configuring the **Defer Non-Essential JavaScript** and **Concatenate JS** modules in Jetpack Boost.

## When to use this skill
- When debugging JavaScript errors or broken interactivity after enabling JS deferral in Jetpack Boost.
- When configuring JavaScript concatenation.
- When optimizing First Input Delay (FID) or Interaction to Next Paint (INP).

## Guidelines
1. **Deferring JS**: By deferring non-essential JS, the browser can render the page faster. However, scripts that depend on each other or require immediate execution (e.g., some tracking scripts or UI components) might break if deferred improperly.
2. **Troubleshooting Broken Interactivity**: If elements like sliders, menus, or forms stop working, try disabling the "Defer Non-Essential JavaScript" module to isolate the issue. 
3. **Concatenation Issues**: Combining JS files can sometimes cause scope or dependency issues. Disable concatenation if specific plugin scripts fail to execute.
4. **Conflicts**: Ensure no other optimization plugins (like Autoptimize or WP Rocket) are also deferring or concatenating JavaScript simultaneously.
