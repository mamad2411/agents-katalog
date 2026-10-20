---
title: "HTMX Framework — v1"
description: "HTMX development with modern web patterns and best practices"
globs: ["**/*.html", "**/*.htmx", "**/*.js", "**/*.py", "**/*.go", "**/*.php"]
alwaysApply: false
priority: high
---

# HTMX Development Rules

## Technology Stack
- **Frontend**: HTMX + HTML
- **Backend**: Python (Flask/Django), Go, PHP
- **Styling**: CSS, Tailwind CSS
- **Build Tool**: Vite/Webpack

## Core Principles
- Use progressive enhancement
- Leverage server-side rendering
- Implement proper state management
- Use HTMX attributes effectively

## Project Structure
src/
├─ templates/     # HTML templates
├─ static/        # CSS, JS, images
├─ components/    # Reusable components
├─ utils/         # Utility functions
└─ styles/        # CSS stylesheets

## Coding Standards
- Use semantic HTML elements
- Use kebab-case for CSS classes
- Use descriptive names for HTMX attributes
- Follow accessibility guidelines

## Best Practices
- Use proper HTMX attributes (hx-get, hx-post)
- Implement proper error handling
- Use loading states and indicators
- Optimize for performance

## Common Patterns
- HTMX with Flask/Django
- HTMX with Go (Fiber)
- HTMX with PHP (Laravel)
- Progressive enhancement approach
