---
description: 
globs: 
alwaysApply: true
---
**Important!**

# Project Overview
- This project uses Nuxt 3.15, Vue 3.5, Vuetify, TypeScript and Firebase.
- Use ES imports, not require()
- Do not import new libraries without approval

# Vue 3 Best Practices

## Component Design
- First block <script setup> is placed, then block <template>
- All component files should be named in PascalCase
- Avoid using inline styles in Vue components
- Use Composition API with <script setup>
- Keep components small and focused
- Extract reusable logic into composables
- Use props and emits for component communication
- Leverage computed properties for derived state
- Follow progressive enhancement
- Ensure accessibility

## Performance
- Use v-show for frequent toggles
- Use v-once for static content
- Use shallowRef when possible
- Keep watchers targeted and efficient

## State Management
- Use provide/inject for deep prop passing in tighly coupled components
- Keep state close to where it's used
- Use reactive refs consistently

## Code Organization
- Group related files in feature directories
- Keep business logic in composables
- Maintain clear component hierarchy

## TypeScript
- Define prop types explicitly
- Use interfaces for complex objects
- Leverage type inference when possible
- Use strict type checking

## Security
- Sanitize user inputs
- Validate props
- Don't use v-html
- Implement proper CORS policies