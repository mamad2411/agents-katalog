---
description:
globs:
alwaysApply: true
---

# AI Rules for Techno Ambassador

Techno Ambassador is a platform bringing together all event cycles and events related to techno music. The main purpose of the product is to enable users to check event ratings and provide ratings and comments on completed events. The system integrates event location data retrieved from Facebook using AI technology, and administrators have the ability to approve or supplement this data. The platform also enables monitoring of user activities through integration with analytical tools.

## Tech Stack

- Astro 5
- TypeScript 5
- Vue 3
- Tailwind 4
- PrimeVue

## Project Structure

When introducing changes to the project, always follow the directory structure below:

- `./src` - source code
- `./src/layouts` - Astro layouts
- `./src/pages` - Astro pages
- `./src/pages/api` - API endpoints
- `./src/features/feature-1` - feature client-side components written in Astro (static) and Vue (dynamic)
- `./src/shared/components` - reusable client-side components written in Astro (static) and Vue (dynamic)
- `./src/assets` - static internal assets
- `./public` - public assets

When modifying the directory structure, always update this section.

## Coding practices

### Guidelines for clean code

- Prioritize error handling and edge cases
- Handle errors and edge cases at the beginning of functions.
- Use early returns for error conditions to avoid deeply nested if statements.
- Place the happy path last in the function for improved readability.
- Avoid unnecessary else statements; use if-return pattern instead.
- Use guard clauses to handle preconditions and invalid states early.
- Implement proper error logging and user-friendly error messages.
- Consider using custom error types or error factories for consistent error handling.
- Do not add short comments to the code! Only add comments when it is necessary!
