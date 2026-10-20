# Copilot Instructions: Improve Codebase Architecture
Description: A systematic approach to refactoring and improving codebase architecture by identifying and deepening shallow modules, improving locality and leverage, and establishing clear seams and interfaces.

# Improve Codebase Architecture Skill

## Overview
This skill enables you to systematically improve codebase architecture by identifying and refactoring shallow modules into deep modules with clear interfaces. The process increases locality (changes concentrate in one place) and leverage (more capability per interface). Learn the core concepts in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Codebase Exploration**
   - Have AI scan the codebase to identify architectural issues
   - Look for shallow modules, duplicate implementations, and poor interfaces
   - Document findings (see [Practical Guide](references/practical_guide.md) for patterns)

2. **Candidate Selection**
   - Review identified candidates with strategic perspective
   - Prioritize based on impact and effort
   - Example: Choose duplicate implementations first

3. **Solution Design**
   - For each candidate:
     a. Define a clear module interface
     b. Consolidate implementations
     c. Improve locality by co-locating related code
   - Use AI to propose designs (examples in [Code Examples](references/code_examples.md))

4. **Grilling Session**
   - Engage in Q&A with AI to refine the solution
   - Address edge cases and implementation details
   - Make strategic decisions about interface design

5. **Implementation**
   - Create GitHub issues for AFK agents to implement
   - Or implement changes directly with AI assistance

6. **Testing**
   - Write tests at module seams
   - Verify interface contracts
   - Ensure adapters work in all contexts

## Best Practices
1. **Regular Execution**: Run this skill every few days in active codebases
2. **Strategic Oversight**: You must make the high-level decisions
3. **Deep Over Shallow**: Always prefer modules that hide complexity
4. **Clear Interfaces**: Document interface contracts thoroughly

## Common Pitfalls
1. **Over-automation**: Trying to run this fully AFK (requires human judgment)
2. **Interface Bleed**: Letting implementation details leak into interfaces
3. **Premature Optimization**: Deepening modules that don't need it
4. **Testing Neglect**: Forgetting to establish tests at seams

## Validation
1. **Metrics**: Count of shallow → deep module conversions
2. **Testing**: Verify modules can be tested in isolation
3. **Change Impact**: Measure how changes affect other parts of system
4. **Leverage**: Assess capability gained per interface unit

Remember: The AI is your tactical partner, but you must provide strategic direction. Combine this skill with testing practices for maximum impact on legacy codebases.

## Reference Guides

### Code Examples

# Code Examples for Architecture Improvement

## Identifying a Shallow Module
```typescript
// Bad: Shallow module with complex interface
class UserManager {
  constructor(dbConnection: Connection, logger: Logger, config: Config) {
    // ...
  }
  
  async createUser(
    email: string, 
    password: string, 
    profileData: object,
    options?: {validateEmail?: boolean, sendWelcome?: boolean}
  ): Promise<User> {
    // Complex validation logic
    // Email sending logic
    // Database operations
    // Logging
  }
}
```

## Refactored Deep Module
```typescript
// Good: Deep module with simple interface
class UserManager {
  async createUser(request: CreateUserRequest): Promise<User> {
    // All complex logic hidden inside
  }
}

interface CreateUserRequest {
  email: string;
  password: string;
  profile?: ProfileData;
}
```

## Adapter Example
```typescript
// Clock interface
interface Clock {
  now(): Date;
}

// Production adapter
class SystemClock implements Clock {
  now() { return new Date(); }
}

// Test adapter
class FakeClock implements Clock {
  constructor(private fixedDate: Date) {}
  now() { return this.fixedDate; }
}
```

## AI Prompt Template
```
Explore the codebase architecture and identify:
1. Modules with complex interfaces but little implementation (shallow)
2. Concepts with duplicate implementations
3. Areas where related code is scattered (low locality)

For each candidate found:
- Describe the current architecture
- Explain why it's problematic
- Propose a deeper module design with:
  * A simplified interface
  * Consolidated implementation
  * Improved locality

Engage in a grilling session to refine the solution before implementation.
```

These examples demonstrate the transformation from problematic shallow modules to improved deep modules with clear interfaces and proper separation of concerns.

### Core Concepts

# Core Concepts of Codebase Architecture Improvement

## Modules
A module is a unit of functionality in your application. It could be:
- A set of React components forming a page
- Functions responsible for authentication
- A logging system (console, file, or third-party service)

## Interfaces
An interface is everything a caller must know to use a module correctly, including:
- Method signatures
- Documentation
- Usage patterns

## Deep vs Shallow Modules
- **Deep modules**: Hide complex implementation behind simple interfaces (ideal)
  - Example: TanStack Query hides complex caching logic behind simple hooks
- **Shallow modules**: Have complex interfaces with little implementation (problematic)

## Seams and Adapters
- **Seams**: Points where modules interact through interfaces
  - Ideal locations for testing (mocks, stubs)
- **Adapters**: Concrete implementations that satisfy interface requirements
  - Example: Real clock vs test fake clock both implementing clock interface

## Key Benefits
1. **Locality**: Changes and fixes concentrate in one place (deep modules)
2. **Leverage**: More capability per unit of interface learned

## Architectural Principles
1. Prefer deep modules over shallow ones
2. Identify and clearly define module interfaces
3. Establish clear seams between modules
4. Use adapters to satisfy interface requirements in different contexts

These concepts form the foundation for systematically improving codebase architecture. The goal is to increase maintainability by creating modules with high locality and leverage.

### Practical Guide

# Practical Guide to Improving Codebase Architecture

## Step 1: Codebase Exploration
Begin by having your AI assistant explore the codebase to identify:
- Shallow modules (complex interfaces with little implementation)
- Poorly defined interfaces
- Duplicate implementations of the same concept
- Areas with low locality (related code scattered)

## Step 2: Candidate Identification
Look for these common patterns:
1. **Duplicate implementations**: Same concept implemented in multiple places
   - Example: Frontend and backend both implementing business rules
2. **Overexposed modules**: Too many implementation details in interfaces
3. **Tight coupling**: Modules with many direct dependencies

## Step 3: Deepening Modules
For each candidate:
1. Define a clear interface that hides implementation details
2. Consolidate duplicate implementations
3. Move related functionality into the module to improve locality

## Step 4: Establishing Seams
1. Identify natural boundaries between modules
2. Define clear interfaces at these boundaries
3. Implement adapters for different contexts (e.g., testing vs production)

## Step 5: Testing Strategy
1. Write tests at module seams
2. Use mocks/stubs to test modules in isolation
3. Verify interface contracts are maintained

## Working with AI
1. Use the AI to explore and identify candidates
2. Engage in a "grilling session" to refine solutions
3. Have the AI propose module shapes and interfaces
4. Make strategic decisions about what to implement

Remember: The AI is tactical, you provide strategic direction. Run this process regularly (every few days) in fast-moving codebases.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[How To De-Slop A Codebase Ruined By AI (with one skill)](https://www.youtube.com/watch?v=3MP8D-mdheA)** by AI Coding