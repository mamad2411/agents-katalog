---
name: lang-html
description: HTML5 semantic architecture, WCAG 2.1 AA/AAA accessibility by construction, zero inline scripting, strict CSP compliance, and safe DOM boundaries.
---

# HTML5 Semantic Architecture & Accessibility Contract

## 1. Semantic Structure & Document Hierarchy
- Treat HTML as a semantic document/interface language, never merely visual markup.
- Prohibit \`<div>\` and \`<span>\` soup when semantic elements exist (\`<main>\`, \`<nav>\`, \`<article>\`, \`<section>\`, \`<header>\`, \`<footer>\`, \`<aside>\`).
- Enforce strict heading hierarchy (\`<h1>\` through \`<h6>\`) without skipping levels. Only one \`<h1>\` per document or main view.

## 2. Accessibility by Construction (WCAG 2.1 AA/AAA)
- Never use ARIA roles to override or mimic native elements (e.g. \`<div role="button">\` is prohibited; use \`<button>\`).
- All interactive elements must be focusable via Tab, support Enter/Space key actuation, and preserve visible focus rings.
- All \`<img>\` elements must possess an explicit \`alt\` attribute (descriptive text or \`alt=""\` for decorative assets).
- Form inputs must be explicitly associated with a \`<label>\` using matching \`id\` and \`for\` attributes.

## 3. Security & Injection Boundaries
- Prohibit inline event handlers (\`onclick\`, \`onerror\`) and inline \`<script>\` or \`<style>\` tags.
- Prohibit \`javascript:\` pseudo-protocols in \`href\` or \`src\` attributes.
- Prohibit raw \`innerHTML\` or \`dangerouslySetInnerHTML\` without registered sanitizer.\n