---
name: "php-code-review"
description: "Comprehensive PHP code review with security analysis, performance optimization, and PSR-12 compliance checking for PHP7/PHP8 projects"
allowed-tools: ["read", "grep", "glob", "write"]
version: "1.0.0"
---

# PHP Code Review Expert

This skill provides comprehensive PHP code review capabilities, combining automated analysis with expert-level insights for PHP7 and PHP8 development.

## Quick Start

1. **Automated Security Scan**: Use `scripts/php-security-scanner.php` for initial vulnerability detection
2. **Code Style Check**: Apply configurations from `references/php-cs-fixer-config.md`
3. **Manual Review**: Follow the systematic review process outlined below
4. **Report Generation**: Use the structured output format for consistent documentation

## Available Resources

- **Scripts**: `php-security-scanner.php` - Automated security vulnerability scanner
- **References**: `php-cs-fixer-config.md` - Ready-to-use PHP CS Fixer configurations  
- **Examples**: `before-after-refactor.md` - Real-world refactoring examples
- **Templates**: 
  - `review-report-template.md` - Comprehensive review report format
  - `quick-checklist.md` - 30-minute quick review checklist

## Core Review Areas

### 1. Naming Conventions Check

#### Class Naming
- **PSR-4 Compliance**: Class names must match file names
- **CamelCase**: Use PascalCase for class names (e.g., `UserController`)
- **Suffix Patterns**: 
  - Controllers end with `Controller` (e.g., `UserController`)
  - Models end with `Model` or use singular nouns (e.g., `User`)
  - Services end with `Service` (e.g., `EmailService`)

#### Method Naming
- **camelCase**: Methods use camelCase (e.g., `getUserName()`)
- **Verb-Noun Pattern**: Start with action word (e.g., `validateInput()`, `processOrder()`)
- **Boolean Methods**: Use is/has/can prefix (e.g., `isValid()`, `hasPermission()`)

#### Variable Naming
- **camelCase**: Variables use camelCase (e.g., `$userName`)
- **Descriptive**: Use meaningful names (e.g., `$customerEmail` not `$e`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)

#### Database Naming
- **Table Names**: snake_case, plural (e.g., `user_profiles`)
- **Column Names**: snake_case (e.g., `created_at`)
- **Foreign Keys**: `{singular_table}_id` (e.g., `user_id`)

### 2. Syntax Validation (PHP7 vs PHP8)

#### PHP8 Features to Embrace
- **Union Types**: `function process(int|float $value)`
- **Named Arguments**: `createUser(name: 'John', email: 'john@example.com')`
- **Null safe Operator**: `$user?->profile?->avatar`
- **Match Expression**: `match($status) { 1 => 'active', 2 => 'inactive' }`
- **Constructor Property Promotion**: `public function __construct(private string $name)`
- **Null Coalescing Assignment**: `$user['name'] ??= 'Anonymous'`

#### PHP7 Compatibility
- **Typed Properties**: Ensure PHP7.4+ if using typed properties
- **Return Type Declarations**: Check for PHP7.0+ compatibility
- **Array Destructuring**: `["id" => $userId, "name" => $userName] = $user;`

#### Syntax Pitfalls to Avoid
- **Missing Semicolons**: Classic error in PHP
- **Undefined Variables**: Check for `$variable` before use
- **Array Access**: Use `isset($array['key'])` before accessing
- **String Concatenation**: Prefer `"{$variable}"` over `"$variable"`

### 3. Logic Analysis

#### Control Flow Issues
- **Deep Nesting**: Maximum 3 levels, refactor with early returns
- **Complex Conditions**: Break down complex boolean expressions
- **Switch Statements**: Ensure all cases have breaks or returns
- **Loop Performance**: Use `foreach` instead of `for` where possible

#### Error Handling
- **Try-Catch Blocks**: Always catch specific exceptions
- **Error Suppression**: Never use `@` operator
- **Validation**: Validate all inputs before processing
- **Graceful Degradation**: Handle edge cases properly

#### Security Logic
- **Input Sanitization**: Never trust user input
- **SQL Injection**: Use prepared statements exclusively
- **XSS Prevention**: Escape output with `htmlspecialchars()`
- **CSRF Protection**: Implement tokens for state-changing operations
- **File Upload**: Validate file types and sizes strictly

### 4. Performance Optimization

#### Database Queries
- **N+1 Problem**: Use eager loading (e.g., `with('comments')`)
- **Query Optimization**: Add indexes on frequently queried columns
- **Pagination**: Always paginate large datasets
- **Caching**: Cache expensive queries with Redis/Memcached

#### Memory Management
- **Large Arrays**: Process in chunks for large datasets
- **Unnecessary Variables**: Unset large variables after use
- **Generator Functions**: Use `yield` for memory-efficient iteration
- **Object Caching**: Reuse objects instead of recreating

#### Code Efficiency
- **String Operations**: Use `strpos()` instead of `preg_match()` for simple searches
- **Array Functions**: Leverage built-in functions like `array_map()`, `array_filter()`
- **Early Returns**: Reduce nesting and improve readability
- **Lazy Loading**: Load resources only when needed

### 5. Security Vulnerabilities

#### Critical Security Checks
- **SQL Injection**: 
  - ❌ `SELECT * FROM users WHERE id = $_GET['id']`
  - ✅ Use PDO prepared statements
- **XSS Attacks**:
  - ❌ `echo $_POST['username']`
  - ✅ `echo htmlspecialchars($_POST['username'], ENT_QUOTES, 'UTF-8')`
- **File Inclusion**:
  - ❌ `include($_GET['file'])`
  - ✅ Whitelist allowed files, use absolute paths
- **Command Injection**:
  - ❌ `shell_exec($_GET['command'])`
  - ✅ Use `escapeshellarg()` and validate inputs

#### Authentication & Authorization
- **Password Security**: Use `password_hash()` and `password_verify()`
- **Session Management**: Regenerate session IDs, set secure session parameters
- **Access Control**: Implement role-based access control (RBAC)
- **API Security**: Validate API tokens on every request

### 6. Code Quality Metrics

#### Cyclomatic Complexity
- **Target**: Maximum 10 per method
- **Refactoring**: Break down complex methods
- **Testing**: Ensure each branch has test coverage

#### Code Reusability
- **DRY Principle**: Don't Repeat Yourself
- **Single Responsibility**: Each method/class has one purpose
- **Composition over Inheritance**: Favor composition for flexibility

#### Documentation
- **PHPDoc**: Document all public methods and classes
- **Type Declarations**: Use strong typing where possible
- **Inline Comments**: Explain complex business logic
- **README**: Keep project documentation updated

## Review Process

### Step 1: Automated Scanning (If the environment exists)
1. **Syntax Check**: `php -l filename.php`
2. **Code Standards**: Run PHP_CodeSniffer with PSR-12
3. **Static Analysis**: Use PHPStan or Psalm
4. **Security Scan**: Run security checkers

### Step 2: Manual Review
1. **Readability**: Is the code easy to understand?
2. **Maintainability**: Can future developers easily modify this?
3. **Performance**: Are there obvious bottlenecks?
4. **Security**: Are there potential vulnerabilities?

### Step 3: Testing
1. **Unit Tests**: Ensure adequate coverage (80%+)
2. **Integration Tests**: Test component interactions
3. **Performance Tests**: Benchmark critical paths

## Common Code Smells

### Red Flags
- **Long Methods**: > 50 lines
- **Large Classes**: > 500 lines
- **Too Many Parameters**: > 4 parameters
- **Duplicate Code**: Same logic in multiple places
- **Dead Code**: Unused variables, methods, or classes
- **Magic Numbers**: Hardcoded values without explanation
- **Inconsistent Formatting**: Mixing styles

### Refactoring Patterns
- **Extract Method**: Break down complex methods
- **Extract Class**: Separate responsibilities
- **Replace Magic Numbers**: Use named constants
- **Introduce Parameter Object**: Group related parameters
- **Encapsulate Collection**: Control collection access

## PHP7 vs PHP8 Compatibility Checklist

### PHP8+ Features (Use When Available)
- [ ] Union Types: `function foo(int|float $bar)`
- [ ] Named Arguments: `array_fill(start_index: 0, count: 100, value: 50)`
- [ ] Match Expression: More concise than switch
- [ ] Null safe Operator: `$country = $session?->user?->getAddress()?->country`
- [ ] Constructor Property Promotion: `public function __construct(private string $name)`
- [ ] Attributes: `#[Route('/users')]`, `#[ORM\Entity]`

### PHP7.4+ Features
- [ ] Typed Properties: `private string $name;`
- [ ] Arrow Functions: `$ids = array_map(fn(Post $post) => $post->id, $posts)`
- [ ] Null Coalescing Assignment: `$array['key'] ??= 'default'`
- [ ] Spread Operator in Arrays: `$merged = [...$array1, ...$array2]`

### Backward Compatibility
- [ ] Check PHP version requirements
- [ ] Avoid features not in target PHP version
- [ ] Use polyfills for newer functions if needed
- [ ] Test on minimum supported PHP version

## Best Practices Summary

### Do
- ✓ Use meaningful variable and method names
- ✓ Write self-documenting code
- ✓ Keep methods small and focused
- ✓ Use type declarations
- ✓ Write tests for critical logic
- ✓ Handle errors gracefully
- ✓ Validate all inputs
- ✓ Use dependency injection
- ✓ Follow PSR standards
- ✓ Document complex business logic

### Don't
- ✗ Use global variables
- ✗ Suppress errors with `@`
- ✗ Trust user input without validation
- ✗ Mix business logic with presentation
- ✗ Create god classes that do everything
- ✗ Use magic methods excessively
- ✗ Ignore performance implications
- ✗ Skip error handling
- ✗ Hardcode configuration values
- ✗ Leave debug code in production

## Review Output Format

When reviewing code, use the standardized templates:

### For Comprehensive Reviews
Use `templates/review-report-template.md` which provides:
- Executive summary with key findings
- Categorized issues (Critical/Standards/Improvements)
- Security and performance assessments
- PHP compatibility analysis
- Actionable recommendations with timelines

### For Quick Reviews
Use `templates/quick-checklist.md` for:
- 30-minute focused review process
- Essential security and quality checks
- Pull request reviews
- Pre-deployment validation

### Custom Format
For specific needs, provide feedback in this structure:

```markdown
## Code Review: [filename]

### Summary
[Overall assessment]

### Critical Issues (Must Fix)
- [ ] [Issue description and suggested fix]

### Standards Violations (Should Fix)
- [ ] [Issue and recommended solution]

### Improvements (Nice to Have)
- [ ] [Suggestion for better code quality]

### Performance Impact
- [Analysis of performance implications]

### Security Assessment
- [Security vulnerabilities found]

### PHP Compatibility
- [PHP version compatibility issues]
```

## References

- See `references/php-cs-fixer-config.md` for automated code style configuration
- See `examples/before-after-refactor.md` for refactoring examples
- Use `scripts/php-security-scanner.php` for automated security scanning