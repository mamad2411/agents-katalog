---
alwaysApply: true
description: Overall project instructions
---

# Default Agent Workflow Behavior

## Primary Workflow
When a user provides a prompt, follow this workflow unless explicitly stated otherwise:

1. **Check Product Requirements**: First examine `docs/product/` for relevant PRDs (Product Requirements Documents)
   - Review `docs/product/prd-main.md` for core system requirements
   - Check `docs/product/prd-features/` for specific feature requirements
   - Understand the current product vision and priorities

2. **Identify Current Task**: Look for existing tasks in `docs/tasks/`
   - If tasks exist, prioritize the highest priority or most recent task
   - If multiple tasks exist, ask user which to focus on
   - If no tasks exist, proceed to step 3

3. **Task Consultation**: If no current task exists
   - Present the user with potential next steps based on PRD priorities
   - Suggest tasks that align with the product roadmap
   - Ask for clarification on what the user would like to work on

4. **Task Execution**: When working on a task
   - Break down complex tasks into subtasks
   - Update task status and progress
   - Document any blockers or decisions made

5. **Subtask Management**: At any point during development
   - Add new subtasks to existing tasks as needed
   - Update task dependencies and priorities
   - Ensure subtasks are properly documented

## Architectural Decision Process
When making architectural decisions:

1. **Explain Changes**: First explain the proposed changes to the user
   - Describe the problem being solved
   - Present the proposed solution
   - Highlight trade-offs and alternatives considered

2. **Create ADR**: If the decision is significant, create an Architectural Decision Record
   - Use the template in `docs/templates/adr.md`
   - Document the context, decision, and consequences
   - Place in `docs/technical/decisions/`

3. **Update Architecture**: Update `docs/technical/architecture.md` if needed
   - Add new architectural patterns or components
   - Update technology stack information
   - Document new service boundaries or data flows

# Technical Details

## Project Structure
- **Framework**: T3 Stack with Next.js, TypeScript, Prisma, Tailwind CSS
- **Database**: PostgreSQL with Prisma ORM
- **Testing**: Vitest for unit and integration tests
- **Package Manager**: pnpm
- **Code Quality**: ESLint + Prettier

## Development Patterns
- **Domain Layer**: Domain-driven design with services in `src/server/services/` where each service is a Class that receives it's dependencies and expose an API to be used elsewhere
- **Testing**: Unit tests alongside service files (`*.test.ts`)
- **Type Safety**: Full TypeScript support with Zod for runtime validation

## Code Standards
- **File Naming**: kebab-case for files, PascalCase for components/classes
- **Imports**: Use relative imports for local files, absolute imports for packages
- **Error Handling**: Proper error boundaries and user-friendly error messages
- **Accessibility**: WCAG 2.1 AA compliance for all UI components

## Database Guidelines
- **Schema Changes**: Always create migrations for schema changes
- **Multi-tenancy**: Ensure proper organization-scoped data isolation
- **Performance**: Use appropriate indexes and query optimization
- **Relationships**: Maintain referential integrity with foreign keys

## Security Considerations
- **Authentication**: Magic code email-based authentication
- **Authorization**: Role-based access control (Admin/Member)
- **Data Isolation**: Organization-scoped data access
- **Input Validation**: Zod schemas for all user inputs

## Testing Strategy
- **Unit Tests**: Test individual service methods and components
- **Integration Tests**: Test service interactions and API endpoints
- **Test Coverage**: Aim for high coverage of business logic
- **Mock Strategy**: Use `vitest-mock-extended` for Prisma mocking

## Performance Requirements
- **Page Load**: <2 seconds for all pages
- **Database Queries**: Optimized with proper indexing
- **Bundle Size**: Minimize client-side JavaScript
- **Caching**: Implement appropriate caching strategies

## Documentation Standards
- **Code Comments**: JSDoc for public APIs and complex logic
- **README Updates**: Keep README.md current with setup instructions
- **API Documentation**: Document all endpoints and their schemas
- **Architecture Updates**: Keep technical docs current with implementation

## Git Workflow
- **Branch Naming**: `feature/`, `bugfix/`, `hotfix/` prefixes
- **Commit Messages**: Conventional commits format
- **Pull Requests**: Include tests and documentation updates
- **Code Review**: Ensure all changes follow project standards

## Environment Management
- **Environment Variables**: Use `.env` files for configuration
- **Secrets**: Never commit sensitive data to version control
- **Database**: Use separate databases for development/testing/production
- **Dependencies**: Keep dependencies updated and secure

## Monitoring and Observability
- **Error Tracking**: Implement proper error logging
- **Performance Monitoring**: Track key metrics and user experience
- **Health Checks**: Implement system health endpoints
- **Logging**: Structured logging for debugging and monitoring

# Task Management Guidelines

## Task Creation
- Use the task template in `docs/templates/task.md`
- Assign appropriate priority levels (P0, P1, P2)
- Include acceptance criteria
- Link to relevant PRDs and technical decisions

## Task Updates
- Update progress regularly
- Document any blockers or dependencies
- Add TODOs as needed during development
- Complete TODOs while progressing
- Potentailly write status updates to describe findings and other important notes
- Mark tasks as complete with verification

## Task Prioritization
- P0: Critical path items blocking other work
- P1: High priority features from PRD
- P2: Nice-to-have features and improvements
- Consider dependencies and resource availability

# Communication Guidelines

## User Interaction
- Always explain your reasoning and approach
- Present options when multiple solutions exist
- Ask for clarification when requirements are unclear
- Provide progress updates on long-running tasks

## Decision Documentation
- Document all significant technical decisions
- Explain trade-offs and alternatives considered
- Update relevant documentation after decisions
- Link decisions to specific tasks or features

## Code Review Process
- Review your own code before presenting to user
- Ensure all tests pass and documentation is updated
- Consider edge cases and error scenarios
- Validate against project standards and requirements
# Default Agent Workflow Behavior

## Primary Workflow
When a user provides a prompt, follow this workflow unless explicitly stated otherwise:

1. **Check Product Requirements**: First examine `docs/product/` for relevant PRDs (Product Requirements Documents)
   - Review `docs/product/prd-main.md` for core system requirements
   - Check `docs/product/prd-features/` for specific feature requirements
   - Understand the current product vision and priorities

2. **Identify Current Task**: Look for existing tasks in `docs/tasks/`
   - If tasks exist, prioritize the highest priority or most recent task
   - If multiple tasks exist, ask user which to focus on
   - If no tasks exist, proceed to step 3

3. **Task Consultation**: If no current task exists
   - Present the user with potential next steps based on PRD priorities
   - Suggest tasks that align with the product roadmap
   - Ask for clarification on what the user would like to work on

4. **Task Execution**: When working on a task
   - Break down complex tasks into subtasks
   - Update task status and progress
   - Document any blockers or decisions made

5. **Subtask Management**: At any point during development
   - Add new subtasks to existing tasks as needed
   - Update task dependencies and priorities
   - Ensure subtasks are properly documented

## Architectural Decision Process
When making architectural decisions:

1. **Explain Changes**: First explain the proposed changes to the user
   - Describe the problem being solved
   - Present the proposed solution
   - Highlight trade-offs and alternatives considered

2. **Create ADR**: If the decision is significant, create an Architectural Decision Record
   - Use the template in `docs/templates/adr.md`
   - Document the context, decision, and consequences
   - Place in `docs/technical/decisions/`

3. **Update Architecture**: Update `docs/technical/architecture.md` if needed
   - Add new architectural patterns or components
   - Update technology stack information
   - Document new service boundaries or data flows

# Technical Details

## Project Structure
- **Framework**: T3 Stack with Next.js, TypeScript, Prisma, Tailwind CSS
- **Database**: PostgreSQL with Prisma ORM
- **Testing**: Vitest for unit and integration tests
- **Package Manager**: pnpm
- **Code Quality**: ESLint + Prettier

## Development Patterns
- **Domain Layer**: Domain-driven design with services in `src/server/services/` where each service is a Class that receives it's dependencies and expose an API to be used elsewhere
- **Testing**: Unit tests alongside service files (`*.test.ts`)
- **Type Safety**: Full TypeScript support with Zod for runtime validation

## Code Standards
- **File Naming**: kebab-case for files, PascalCase for components/classes
- **Imports**: Use relative imports for local files, absolute imports for packages
- **Error Handling**: Proper error boundaries and user-friendly error messages
- **Accessibility**: WCAG 2.1 AA compliance for all UI components

## Database Guidelines
- **Schema Changes**: Always create migrations for schema changes
- **Multi-tenancy**: Ensure proper organization-scoped data isolation
- **Performance**: Use appropriate indexes and query optimization
- **Relationships**: Maintain referential integrity with foreign keys

## Security Considerations
- **Authentication**: Magic code email-based authentication
- **Authorization**: Role-based access control (Admin/Member)
- **Data Isolation**: Organization-scoped data access
- **Input Validation**: Zod schemas for all user inputs

## Testing Strategy
- **Unit Tests**: Test individual service methods and components
- **Integration Tests**: Test service interactions and API endpoints
- **Test Coverage**: Aim for high coverage of business logic
- **Mock Strategy**: Use `vitest-mock-extended` for Prisma mocking

## Performance Requirements
- **Page Load**: <2 seconds for all pages
- **Database Queries**: Optimized with proper indexing
- **Bundle Size**: Minimize client-side JavaScript
- **Caching**: Implement appropriate caching strategies

## Documentation Standards
- **Code Comments**: JSDoc for public APIs and complex logic
- **README Updates**: Keep README.md current with setup instructions
- **API Documentation**: Document all endpoints and their schemas
- **Architecture Updates**: Keep technical docs current with implementation

## Git Workflow
- **Branch Naming**: `feature/`, `bugfix/`, `hotfix/` prefixes
- **Commit Messages**: Conventional commits format
- **Pull Requests**: Include tests and documentation updates
- **Code Review**: Ensure all changes follow project standards

## Environment Management
- **Environment Variables**: Use `.env` files for configuration
- **Secrets**: Never commit sensitive data to version control
- **Database**: Use separate databases for development/testing/production
- **Dependencies**: Keep dependencies updated and secure

## Monitoring and Observability
- **Error Tracking**: Implement proper error logging
- **Performance Monitoring**: Track key metrics and user experience
- **Health Checks**: Implement system health endpoints
- **Logging**: Structured logging for debugging and monitoring

# Task Management Guidelines

## Task Creation
- Use the task template in `docs/templates/task.md`
- Assign appropriate priority levels (P0, P1, P2)
- Include acceptance criteria
- Link to relevant PRDs and technical decisions

## Task Updates
- Update progress regularly
- Document any blockers or dependencies
- Add TODOs as needed during development
- Complete TODOs while progressing
- Potentailly write status updates to describe findings and other important notes
- Mark tasks as complete with verification

## Task Prioritization
- P0: Critical path items blocking other work
- P1: High priority features from PRD
- P2: Nice-to-have features and improvements
- Consider dependencies and resource availability

# Communication Guidelines

## User Interaction
- Always explain your reasoning and approach
- Present options when multiple solutions exist
- Ask for clarification when requirements are unclear
- Provide progress updates on long-running tasks

## Decision Documentation
- Document all significant technical decisions
- Explain trade-offs and alternatives considered
- Update relevant documentation after decisions
- Link decisions to specific tasks or features

## Code Review Process
- Review your own code before presenting to user
- Ensure all tests pass and documentation is updated
- Consider edge cases and error scenarios
- Validate against project standards and requirements
