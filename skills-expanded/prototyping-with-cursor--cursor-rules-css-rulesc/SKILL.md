---
description: Adding a new CSS file and global styles
globs: *.css
alwaysApply: false
---
# Global CSS
1. Never add anything to the global CSS file unless prompted to.
2. All CSS should be in the prototype's folder.
3. Do not use :root outside of the globals.css file.

# Prototype CSS
Avoid referencing other prototype's CSS unless explictly prompted.

# CSS Modules
1. Never use bare HTML element selectors (like div, pre, code) in CSS Modules files.
2. Always use a local class name for selectors (starting with a dot).
3. For styling HTML elements, create a specific class name that describes its purpose (e.g., .preBlock instead of pre).
4. Nested selectors must include at least one local class name (e.g., .bookInfo h2 is valid because it includes .bookInfo).
5. When targeting elements inside a component, prefer creating new class names over nesting selectors.