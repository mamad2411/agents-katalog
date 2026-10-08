---
description: 
globs: 
alwaysApply: true
---
# General Development Guidelines

Our project is a mobile-first web app that prioritizes precision, simplicity, and reliability.

## Core Principles

1. Execute exactly what is requested - no more, no less
2. Implement the simplest solution that fulfills all requirements
3. Minimize code complexity and line count while meeting specifications
4. Never add functionality or features that weren't explicitly requested
5. No spaghetti code - use helper, util, component files
6. Use context7 mcp tool for specific libraries refs.

## Code Standards

- Avoid using `any` type - it creates build issues in Vercel
- Never use underscores to fix unused variable linter warnings
- Use shadcn components via `npx shadcn@latest add ComponentName`
- File size limit: Alert when exceeding 500 lines

## Project Maintenance

- Update ROADMAP.md after implementing new features
- Add strategic and precise logging only where critical - avoid overwhelming the code

## Development Workflow

- Development server is always running - no need for `npm run dev` commands
- When asked questions, analyze first before making code changes
- Start with core solutions before handling edge cases
- Test thoroughly after significant changes
- Focus on root causes rather than symptoms

## Mobile-First Development

- Prioritize mobile user experience
- Ensure responsive design across all components
- Test thoroughly on mobile devices and viewports

Remember: Your value comes from precision and reliability. When in doubt, ask yourself: "Am I adding any functionality or complexity that wasn't explicitly requested?"