---
description: 
globs: *.vue
alwaysApply: false
---
## Frontend

### VueUse

- Prefer VueUse specialized functions over generic implementations for better performance
- Trust automatic cleanup - VueUse handles side-effects disposal when components unmount
- Use manual cleanup handlers only when disposing resources before component unmounting
- Pass reactive refs as arguments instead of static values to maintain reactivity
- Leverage built-in debouncing and throttling instead of manual implementations

