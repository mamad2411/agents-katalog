# Project Intelligence: Boids Simulation

## Development Patterns

### 1. Component Structure

- Use atomic design principles
- Follow Svelte 5 runes syntax
- Maintain strict TypeScript types
- Keep components small and focused

### 2. State Management

- Prefer component-scoped state
- Use Svelte runes for reactivity
- Avoid global stores
- Implement unidirectional data flow
- Use the Event Bus (event-bus.ts) to communicate between Phaser and Svelte

### 3. Testing Approach

- Write tests alongside features
- Use Vitest for unit testing
- Follow testing pyramid principles
- Maintain high test coverage
- Do not test Svelte components or UI

## Project Preferences

### 1. Code Style

- Use 2-space indentation
- Follow Prettier formatting
- Use ESLint for linting
- Maintain consistent naming

### 2. Documentation

- Keep documentation up-to-date
- Use Markdown for docs
- Maintain clear commit messages
- Document architectural decisions

### 3. Performance

- Optimize critical paths
- Monitor frame rates
- Profile memory usage
- Implement performance budgets

## Workflow Patterns

### 1. Development Process

- Use feature branches
- Perform code reviews
- Maintain CI/CD pipeline
- Follow semantic versioning

### 2. Error Handling

- Implement graceful degradation
- Use error boundaries
- Maintain error logging
- Provide user feedback

### 3. Maintenance

- Regularly update dependencies
- Address technical debt
- Monitor performance
- Maintain documentation

## Key Insights

### 1. Architecture

- Event-driven design
- Modular components
- Clear separation of concerns
- Performance-first approach

### 2. UI Patterns

- Responsive design
- Theme support
- Accessibility focus
- Consistent component library

### 3. Simulation

- Physics-based movement
- Spatial partitioning
- Behavior composition
- Performance optimization
