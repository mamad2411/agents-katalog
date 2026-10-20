---
title: "Qwik Framework — v1"
description: "Qwik.js development with TypeScript and Vite best practices"
globs: ["**/*.tsx", "**/*.ts", "src/**/*.tsx", "src/**/*.ts"]
alwaysApply: false
priority: high
---

# Qwik Development Rules

## Technology Stack
- **Framework**: Qwik
- **Language**: TypeScript
- **Build Tool**: Vite
- **Package Manager**: npm/yarn/pnpm

## Core Principles
- Use Qwik's resumability approach
- Leverage fine-grained lazy loading
- Implement proper hydration strategies
- Use Qwik's built-in optimizations

## Project Structure
src/
├─ routes/        # Qwik routing
├─ components/    # Reusable components
├─ hooks/         # Custom Qwik hooks
├─ utils/         # Utility functions
└─ types/         # TypeScript definitions

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for components
- Use kebab-case for CSS classes
- Use descriptive names for props and state

## Best Practices
- Use $() for reactive values
- Implement proper lazy loading
- Use Qwik's built-in state management
- Optimize for resumability

## Common Patterns
- Qwik components with proper exports
- State management with useStore
- Routing with Qwik routing
- Proper cleanup and resource management
