# AgentCare Development Instructions

## When working on agent classes:
- Always extend the base Agent class
- Implement proper error handling with try/catch
- Use dependency injection for tool access
- Add logging for all agent actions
- Include performance metrics collection

## When working on API endpoints:
- Use express-validator for input validation
- Implement proper HTTP status codes
- Add comprehensive error responses
- Include rate limiting middleware
- Document with OpenAPI/Swagger annotations

## When working on database operations:
- Use parameterized queries to prevent SQL injection
- Implement proper transaction handling
- Add database connection pooling
- Include proper indexing strategies
- Use migrations for schema changes

## When working on frontend components:
- Use TypeScript with strict mode
- Implement proper state management
- Add loading states and error boundaries
- Include accessibility attributes
- Write component tests with React Testing Library

## Multi-Agent System Patterns:
1. **Supervisor Pattern**: Central coordinator delegates tasks
2. **Chain of Responsibility**: Pass requests through agent chain
3. **Observer Pattern**: Agents notify each other of state changes
4. **Strategy Pattern**: Different agents for different appointment types

## Error Handling Strategy:
- Agent coordination errors should gracefully fallback
- API errors should return user-friendly messages
- Database errors should be logged but not exposed
- Frontend errors should show helpful recovery options

## Performance Considerations:
- Implement agent response caching
- Use database connection pooling
- Add CDN for static assets
- Implement lazy loading for components
- Use service workers for offline functionality