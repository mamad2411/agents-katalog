---
name: "Clean Code Checker"
description: "A skill that helps check and optimize code according to Clean Code principles step by step, supporting JavaScript, TypeScript, and Python."
---

# Clean Code Checker

This skill provides comprehensive code analysis and optimization based on Clean Code principles. It examines code systematically, checking each Clean Code criterion individually and providing specific optimization suggestions.

## When to Use

This skill should be used when:
- Reviewing existing code for quality improvements
- Optimizing new code to meet Clean Code standards
- Refactoring code to improve readability and maintainability
- Learning and applying Clean Code principles
- Preparing code for production deployment

## Usage

### Process Overview

1. **Analyze Code Structure**: Examine the provided code to identify language (JS/TS/Python) and overall structure
2. **Systematic Check**: Apply Clean Code criteria one by one
3. **Generate Suggestions**: Provide specific, actionable recommendations for each issue found
4. **Apply Optimizations**: Implement approved improvements step by step

### Available Scripts

#### `scripts/analyze_code.py`
Execute to analyze code for Clean Code violations:
```bash
python scripts/analyze_code.py --file <path> --language <js|ts|python>
```

#### `scripts/refactor_code.py`
Execute to apply approved Clean Code optimizations:
```bash
python scripts/refactor_code.py --file <path> --language <js|ts|python> --rules <rule-list>
```

### Clean Code Criteria

The skill checks the following criteria systematically:

#### 1. Naming Conventions
- Variables, functions, and classes have clear, descriptive names
- Consistent naming conventions (camelCase for JS/TS, snake_case for Python)
- Avoid single-letter variables except in loops
- Use pronounceable names

#### 2. Function Design
- Functions should be small (under 20 lines)
- Single responsibility principle
- Clear parameter list (prefer 3 or fewer parameters)
- No side effects

#### 3. Comments
- Comments explain why, not what
- Remove dead code and commented-out code
- Ensure comments are accurate and up-to-date

#### 4. Code Formatting
- Consistent indentation and spacing
- Proper line length (under 80-100 characters)
- Consistent brace style and quotes

#### 5. Error Handling
- Use appropriate exception types
- Provide meaningful error messages
- Avoid empty catch blocks

#### 6. Code Duplication
- Identify duplicate code patterns
- Extract common functionality to reusable functions
- Use composition over inheritance where appropriate

#### 7. Complexity Control
- Reduce nesting levels
- Control cyclomatic complexity
- Use guard clauses to simplify logic

#### 8. Testability
- Make code easy to test
- Avoid static variables in functions
- Use dependency injection where appropriate

#### 9. Design Patterns
- Apply appropriate design patterns
- Avoid over-engineering
- Balance flexibility and simplicity

#### 10. Magic Numbers and Hardcoding
- Eliminate magic numbers
- Use constants or configuration
- Externalize environment-specific values

### Workflow

1. **Initial Analysis**: Use `analyze_code.py` to get comprehensive violations report
2. **Prioritize Issues**: Focus on high-impact violations first
3. **Apply Fixes**: Use `refactor_code.py` to implement approved changes
4. **Verify Results**: Re-analyze code to confirm improvements

### Language-Specific Considerations

#### JavaScript/TypeScript
- Use const/let appropriately
- Prefer arrow functions for simple functions
- Use template literals for string concatenation
- Follow ESLint rules where applicable

#### Python
- Follow PEP 8 style guidelines
- Use descriptive function and variable names
- Prefer list comprehensions for simple operations
- Use context managers for resource management

## Examples

### Example 1: Basic Code Review
```
User: "Check this JavaScript code for Clean Code violations"
→ Run analysis → Generate suggestions → Apply fixes
```

### Example 2: Function Optimization
```
User: "Optimize this complex function to be more readable"
→ Identify complexity issues → Simplify logic → Apply guard clauses
```

### Example 3: Refactoring for Testability
```
User: "Make this code more testable"
→ Extract dependencies → Remove static coupling → Add interfaces
```