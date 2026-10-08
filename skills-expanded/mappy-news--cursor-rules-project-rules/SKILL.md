# mappy.news - Project Rules

## Project Context

This is a location-based news application built with Next.js, Tailwind CSS, and
shadcn/ui. The app displays news articles on an interactive map with filtering
capabilities.

## Code Style Guidelines

### TypeScript

- Use TypeScript for all files
- Prefer interfaces over types for object shapes
- Use strict type checking
- Export types from dedicated `types/` directory

### React/Next.js

- Use Next.js App Router (app directory)
- Prefer server components when possible
- Use client components only when necessary (interactivity, browser APIs)
- Follow React hooks best practices

### Styling

- Use Tailwind CSS utility classes
- Follow shadcn/ui component patterns
- Use CSS Grid and Flexbox for layouts
- Maintain responsive design principles

### File Organization

```
app/              # Next.js app router pages
components/       # Reusable UI components
  ui/            # shadcn/ui components
  map/           # Map-related components
  news/          # News-related components
lib/             # Utilities and database
types/           # TypeScript definitions
data/            # Database and seed data
```

### Database

- Use SQLite with proper schema design
- Include proper indexing for location queries
- Use prepared statements for security

### Best Practices

- Write semantic, accessible HTML
- Include proper error boundaries
- Implement loading states
- Use proper TypeScript types
- Follow Next.js performance best practices
- Test components with representative data

## Development Notes

- Always update progress.md when completing tasks
- Use shadcn/ui components for consistency
- Prioritize performance for map interactions
- Consider mobile-first responsive design
