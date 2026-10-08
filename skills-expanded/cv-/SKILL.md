# Project Rules for Frontend Development

## Code Style
- Use semantic HTML5 elements (nav, section, article, footer, etc.)
- Follow BEM naming convention for CSS classes when appropriate
- Use CSS variables for colors, spacing, and typography
- Write self-documenting code with clear comments
- Keep code clean and readable

## Component Structure
- Each component should be self-contained and reusable
- Components should be in separate files when modular
- Use descriptive class names (e.g., `.hero-section`, not `.div1`)
- Maintain consistent naming patterns across components

## CSS Guidelines
- Mobile-first responsive design approach
- Use CSS Grid for layouts, Flexbox for alignment
- Maintain consistent spacing scale (8px base unit recommended)
- Ensure WCAG AA accessibility standards
- Use CSS custom properties (variables) for theming
- Avoid inline styles; use classes instead

## JavaScript
- Use modern ES6+ syntax
- Add event listeners in DOMContentLoaded
- Comment complex logic
- Keep functions small and focused
- Use descriptive variable and function names

## File Organization
- HTML: index.html (main), components/ (modular pieces if using modules)
- CSS: styles.css (main), styles/components/ (component styles if modular)
- JS: script.js (main), js/components/ (component scripts if modular)
- Keep related files together

## When Creating Components
- Always include responsive design considerations
- Add hover states for interactive elements
- Include accessibility attributes (aria-labels, alt text, semantic HTML)
- Test in multiple browsers
- Ensure proper contrast ratios for text

## Design Principles
- Clean, minimalist design
- High contrast for accessibility
- Consistent spacing and typography
- Smooth animations and transitions
- Performance-conscious (optimize images, minimize CSS/JS)

## Git Practices
- Write clear, descriptive commit messages
- Keep commits atomic (one feature/fix per commit)
- Test before committing
- Use feature branches for major changes
