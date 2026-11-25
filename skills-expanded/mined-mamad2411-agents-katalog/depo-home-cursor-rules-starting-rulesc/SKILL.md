---
description: 
globs: 
alwaysApply: true
---
# Cursor Rules for Spring Boot JWT Authentication Project


## GLOBALS
 - do not implement mocked data ! only for populating example with flyway, no mocked data in the code !
 -  comment the complex code if using complexe composed lines.
 - make sure to keep all the external configurations by profiles, and put the default values in the application.yml
 - we gonna implement a separated frontend later with react, so dont bother with the front now but keep in mind it will came later so make sure to prepare for that with the configs

## General Guidelines
- Follow a consistent coding style throughout the project
- Use meaningful variable and method names
- Add appropriate comments for complex logic
- Implement proper exception handling
- Write clean, maintainable code

## Development Workflow
- DO NOT automatically run the application or tests after code generation
- Let the developer manually start the server
- Commit code in logical chunks
- Focus on one feature at a time

## Data Handling
- DO NOT use mocked data under any circumstances
- Implement proper database access with JPA/Hibernate
- Use prepared statements or parameterized queries
- Validate all input data
- Handle edge cases properly

## Security Requirements
- Implement proper JWT validation for every protected endpoint
- Store passwords using BCryptPasswordEncoder only
- Include proper authorization checks in controllers and services
- Use Principal from SecurityContext to get current user
- Implement proper CORS configuration
- Validate all input to prevent injection attacks
- Do not expose sensitive information in responses

## Code Structure
- Keep controllers thin, move business logic to services
- Separate concerns properly (controller, service, repository)
- Use DTOs for request/response handling
- Use proper entity mapping for database operations

## Database
- Use Flyway migrations for all schema changes
- Configure different Flyway behavior for dev vs prod profiles
- Use proper indexing for performance
- Implement proper relationships between entities

## Docker
- Create separate docker-compose files as requested
- Configure proper networking between containers
- Use environment variables for configuration
- Set up proper volume mapping for data persistence

## Testing
- DO NOT implement unit tests at this stage
- We will add them later

## Documentation
- Document all endpoints in Swagger
- Add proper descriptions for all API parameters
- Include examples where appropriate
- Document configuration options in README.md

## Frontend Considerations
- Backend should expose proper CORS headers
- JWT should be easily consumable by React frontend
- Return appropriate HTTP status codes
- Use consistent response formats

## Error Handling
- Return meaningful error messages
- Use appropriate HTTP status codes
- Implement global exception handling
- Log errors properly but don't expose sensitive information

## Performance
- Implement pagination for list endpoints
- Use proper JPA fetching strategies
- Avoid N+1 query problems

## Specific Project Rules
- Handle agent access filtering in the service layer, not in controllers
- Always check user roles before returning data
- Configure Flyway to clean database in dev profile only
- Preserve data in production profile
- Implement JWT with proper expiration and security



