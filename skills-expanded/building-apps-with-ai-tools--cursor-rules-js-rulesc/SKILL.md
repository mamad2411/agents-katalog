---
description: JavaScript coding standards and best practices
globs: **/*.js
alwaysApply: false
---

# JavaScript Coding Standards

## Code Style
- Use 2-space indentation
- Use single quotes for strings
- Always use semicolons
- Maximum line length: 80 characters
- Use meaningful variable and function names

## Modern JavaScript Features
- Use `const` for variables that won't be reassigned
- Use `let` for variables that will be reassigned
- Avoid `var` entirely
- Use arrow functions for short, simple functions
- Use template literals for string interpolation
- Use destructuring for object and array assignment

## Error Handling
- Always wrap async operations in try/catch blocks
- Provide meaningful error messages
- Log errors appropriately (console.error for debugging)
- Handle edge cases gracefully

## DOM Manipulation
- Use `querySelector` and `querySelectorAll` instead of older DOM APIs
- Cache DOM elements when used multiple times
- Use event delegation for dynamic elements
- Avoid inline event handlers in HTML

## Performance
- Minimize DOM queries
- Use `requestAnimationFrame` for animations
- Debounce or throttle event handlers when appropriate
- Use efficient data structures and algorithms

## Example Code

```javascript
'use strict';

// Good: Modern JavaScript with proper error handling
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const userData = await response.json();
    return userData;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    return null;
  }
}

// Good: Event delegation and modern DOM manipulation
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('#user-list');
  
  container.addEventListener('click', (e) => {
    if (e.target.matches('.user-item')) {
      const userId = e.target.dataset.userId;
      handleUserClick(userId);
    }
  });
});
```

