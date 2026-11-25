---
name: backend
description: Backend developer skill for Java 17, TEJ, RestExpress, Kafka, Gradle, PostgreSQL
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

# Backend Developer Skill

Java/TEJ backend implementation with modern patterns and frameworks.

## Technical Stack

- **Language**: Java 17+
- **Frameworks**: TEJ, RestExpress, Spring Data JPA
- **Database**: PostgreSQL with Flyway migrations
- **Messaging**: Kafka with proper patterns
- **Testing**: JUnit 5, Mockito, TestContainers
- **Build**: Gradle with convention plugins

## Capabilities

- Implement features from approved designs
- RPI workflow (Refactor-Partner-Implement)
- Kafka producer/consumer implementation
- Repository pattern and JPA entities
- RESTful API implementation
- Unit and integration testing

## Process Flow

1. Receive approved design (G3)
2. Analyze acceptance criteria
3. Implement production code
4. Write unit tests (>80% coverage)
5. Submit PR for code review (G5)

## Key Patterns

- ApplicationServiceException hierarchy
- Singleton Kafka producers
- Try-with-resources resource management
- Parameterized SQL queries (no concatenation)
- SLF4J logging exclusively

## Skill Triggers

Use this skill when:
- Story ready for implementation
- Design approved (G3 complete)
- Developer needs implementation guidance
- Code generation needed

## Quality Standards

- Code follows team conventions
- Test coverage >= 80%
- No hardcoded secrets or configs
- Memory leak prevention
- Performance validated
