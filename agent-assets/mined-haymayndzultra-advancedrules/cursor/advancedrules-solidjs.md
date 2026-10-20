---
title: "SolidJS with TypeScript — v1"
description: "SolidJS development with TypeScript best practices and patterns"
globs: ["**/*.tsx", "**/*.ts", "src/**/*.tsx", "src/**/*.ts"]
alwaysApply: false
priority: high
---

# SolidJS Development Rules

## Technology Stack
- **Framework**: SolidJS
- **Language**: TypeScript
- **Build Tool**: Vite
- **Package Manager**: npm/yarn/pnpm

## Core Principles
- Use reactive primitives (createSignal, createEffect)
- Prefer fine-grained reactivity over coarse-grained
- Leverage SolidJS's compilation approach
- Use proper component composition

## Project Structure
src/
├─ components/     # Reusable UI components
├─ pages/         # Page components
├─ stores/        # State management
├─ utils/         # Utility functions
└─ types/         # TypeScript definitions

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for components
- Use kebab-case for CSS classes
- Use descriptive names for props and state

## Best Practices
- Create small, focused components
- Use createMemo for expensive computations
- Implement proper error boundaries
- Use lazy loading for code splitting

## Common Patterns
- Custom stores with createStore
- Reactive props with createMemo
- Component composition over inheritance
- Proper cleanup in createEffect
