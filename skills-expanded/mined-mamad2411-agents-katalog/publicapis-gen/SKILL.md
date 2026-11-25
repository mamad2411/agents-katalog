# Directory API v1 - Cursor Rules

## General Go Development Guidelines

### Code Quality & Constants
- **NO hardcoded strings in code** - All string literals must be defined as package-local constants
- Use meaningful constant names that clearly express intent
- Group related constants together with clear documentation
- Define constants within the same package where they are used
- Use camelCase for unexported constants (e.g., `errorNotImplemented`)

### Examples of Required Constants Usage
```go
// ❌ BAD - Hardcoded strings
return errors.New("not implemented")
slog.ErrorContext(ctx, "failed to run", "error", err)
if containsOperation(resource.Operations, "Read") {

// ✅ GOOD - Use package-local constants
const (
    errorNotImplemented = "not implemented"
    errorFailedToRun    = "failed to run"
    logKeyError         = "error"
)

return errors.New(errorNotImplemented)
slog.ErrorContext(ctx, errorFailedToRun, logKeyError, err)
if containsOperation(resource.Operations, OperationRead) {
```

### String Categories Requiring Constants
1. **Error Messages**: All error strings must use package-local constants
2. **Log Messages**: All log message keys and values must use package-local constants
3. **CRUD Operations**: "Create", "Read", "Update", "Delete" → use local Operation* constants
4. **Field Types**: "UUID", "String", "Int", "Bool" → define as needed per package
5. **HTTP Methods**: "GET", "POST", etc. → define as needed per package
6. **Content Types**: "application/json" → define as needed per package
7. **Field Modifiers**: "array", "nullable" → define as needed per package

### Exception for Test Files
Test files (files ending in `_test.go`) may contain hardcoded strings for test data, but should still use constants for:
- Repeated test values
- Error messages being tested
- Configuration values

### Adding New Constants
When adding new functionality:
1. Define constants within the same package where they are used
2. Use clear, descriptive names following Go naming conventions
3. Group related constants together in const blocks
4. Use camelCase for unexported constants
5. Add documentation comments for const blocks when needed

### Code Review Checklist
Before submitting code:
- [ ] No hardcoded strings in production code (except test data)
- [ ] All constants defined as package-local constants
- [ ] Constants grouped logically in const blocks
- [ ] Clear and descriptive constant names used
- [ ] Proper camelCase naming for unexported constants

This ensures maintainable, consistent code that's easy to update and internationalize if needed.

## Object-Oriented Design Patterns

### Methods on Structs
- **ALWAYS use methods on structs instead of standalone functions when working with struct data**
- Methods should be attached to the struct they operate on to provide behavior and capabilities
- Use receiver methods to encapsulate logic that belongs to a specific type
- Group related functionality as methods on the appropriate struct

### Method Organization Patterns
The codebase follows these method organization patterns:

#### Validation Methods
- Use boolean methods for validation checks (e.g., `HasCreateOperation()`, `IsNullable()`, `IsArray()`)
- Name validation methods with clear prefixes: `Has*()`, `Is*()`, `Can*()`
- Return simple boolean values for validation checks

#### Utility Methods
- Use methods for derived data and transformations (e.g., `GetPluralName()`, `TagJSON()`)
- Name utility methods with descriptive verbs: `Get*()`, `Create*()`, `Convert*()`
- Methods that generate or transform data should be named with action verbs

#### Factory Methods
- Use standalone factory functions for creating standard instances
- Name factory functions with `Create*()` prefix (e.g., `CreateLimitParam()`, `CreateOffsetParam()`)
- Factory methods should return configured instances of structs

### Examples of Method Usage Patterns
```go
// ✅ GOOD - Methods on structs for validation
func (r Resource) HasCreateOperation() bool {
    return slices.Contains(r.Operations, OperationCreate)
}

func (f Field) IsNullable() bool {
    return slices.Contains(f.Modifiers, ModifierNullable)
}

// ✅ GOOD - Methods for data transformation
func (r Resource) GetCreateBodyParams() []Field {
    // Transform resource fields to body parameters
}

func (f Field) TagJSON() string {
    return camelCase(f.Name)
}

// ✅ GOOD - Factory functions for standard instances
func CreateLimitParam() Field {
    return Field{
        Name:        listLimitParamName,
        Description: listLimitParamDesc,
        Type:        FieldTypeInt,
        Default:     listLimitDefaultValue,
    }
}

// ❌ BAD - Using standalone functions instead of methods
func hasCreateOperation(resource Resource) bool {
    return slices.Contains(resource.Operations, OperationCreate)
}
```

### Method Design Guidelines
1. **Attach methods to the struct they primarily operate on**
2. **Use clear, descriptive method names that indicate their purpose**
3. **Validation methods should return boolean values**
4. **Utility methods should return the transformed data**
5. **Factory functions should create and return configured instances**
6. **Keep method signatures simple and focused**
7. **Use consistent naming patterns across similar methods**

### Method Categories
- **Validation Methods**: Check properties or capabilities (`Has*()`, `Is*()`, `Can*()`)
- **Accessor Methods**: Get or compute derived values (`Get*()`, `Tag*()`)
- **Factory Methods**: Create standard instances (`Create*()`)
- **Transformation Methods**: Convert or generate data from struct fields
- **Helper Methods**: Provide utility functionality specific to the struct

### Code Organization Checklist
Before adding new functionality:
- [ ] Consider if logic belongs as a method on an existing struct
- [ ] Use appropriate naming patterns for the method type
- [ ] Group related methods together in the source file
- [ ] Add factory functions for commonly created instances
- [ ] Prefer methods over standalone functions when working with struct data
- [ ] Use consistent patterns with existing similar methods

## Go Code Formatting Rules

### Automatic Formatting
- **ALWAYS run `gofmt -s -w .` after making any Go code changes**
- All Go code MUST follow standard Go formatting conventions
- Use Go's standard formatting (gofmt) - no custom formatting rules
- Ensure proper import organization and grouping

### Formatting Requirements
- Use tabs for indentation (Go standard)
- Keep line lengths reasonable (prefer under 100 characters when possible)
- Follow Go's standard comment formatting
- Use proper spacing around operators and after commas
- Organize imports in standard groups: standard library, third party, local

### Before Committing
- [ ] Run `gofmt -s -w .` to format all Go files
- [ ] Verify no linting errors with proper formatting
- [ ] Check that all string literals use package-local constants
- [ ] Ensure consistent code style throughout

### Cursor-Specific Instructions
When editing Go code:
1. **IMMEDIATELY** after any Go code modification, run gofmt formatting
2. Follow the repository's constant usage rules (no hardcoded strings)
3. Maintain consistent indentation and spacing
4. Keep import statements properly organized
5. Ensure all functions and types have proper documentation comments

## Performance and Idiomatic Go Code

### Efficient Slice Operations
- **ALWAYS use slice unpacking instead of loops when appending entire slices**
- Replace loops that append individual elements with `append(slice, otherSlice...)`
- This improves performance and follows Go best practices

### Examples of Efficient Slice Operations
```go
// ❌ BAD - Inefficient loop that staticcheck will flag (S1011)
for _, item := range sourceSlice {
    targetSlice = append(targetSlice, item)
}

// ✅ GOOD - Use slice unpacking
targetSlice = append(targetSlice, sourceSlice...)
```

### Staticcheck Rules to Follow
- **S1011**: Replace loops with slice unpacking when possible
- Always run `staticcheck` before committing to catch performance issues
- Use `go vet` to identify common Go mistakes

### Performance Checklist
Before submitting code:
- [ ] No loops that can be replaced with slice unpacking (`...`)
- [ ] Run `staticcheck ./...` and fix all issues
- [ ] Run `go vet ./...` and address warnings
- [ ] Use efficient Go idioms for common operations

## Testing Best Practices

### Test File Organization and Structure
- **ONE test file per source file** - Follow one-to-one mapping (e.g., `specification.go` → `specification_test.go`)
- **Group tests by method/function** - Each method should have its own main test function
- **Use subtests for edge cases** - Organize edge cases as subtests within the main test function
- **NO separate test files for methods or edge cases** - All tests for a source file belong in one test file

### Test File Naming and Organization Rules
```go
// ✅ GOOD - Proper test organization in specification_test.go
func TestService_IsObject(t *testing.T) {
    // Main test logic here
    
    t.Run("edge cases", func(t *testing.T) {
        t.Run("empty collections", func(t *testing.T) {
            // Edge case test logic
        })
        
        t.Run("nil collections", func(t *testing.T) {
            // Another edge case test logic
        })
    })
}

func TestField_IsArray(t *testing.T) {
    // Main test logic here
    
    t.Run("edge cases", func(t *testing.T) {
        t.Run("multiple modifiers", func(t *testing.T) {
            // Edge case test logic
        })
    })
}
```

### Test Organization Guidelines
1. **Main test function naming**: `Test<StructName>_<MethodName>` for methods, `Test<FunctionName>` for functions
2. **Group tests by struct/type** using comment headers (e.g., `// ============================================================================`)
3. **Test happy path first** in the main test function body
4. **Add edge cases as subtests** using `t.Run("edge cases", func(t *testing.T) {...})`
5. **Use descriptive subtest names** that explain the scenario being tested

### File Structure Example
```go
package specification

import (
    "testing"
    "github.com/stretchr/testify/assert"
)

// ============================================================================
// Service Tests
// ============================================================================

func TestService_IsObject(t *testing.T) {
    // Main happy path test
    
    t.Run("edge cases", func(t *testing.T) {
        t.Run("case sensitivity", func(t *testing.T) {
            // Specific edge case
        })
    })
}

// ============================================================================
// Field Tests  
// ============================================================================

func TestField_IsArray(t *testing.T) {
    // Main happy path test
    
    t.Run("edge cases", func(t *testing.T) {
        t.Run("nil modifiers", func(t *testing.T) {
            // Specific edge case
        })
    })
}

// ============================================================================
// Factory Function Tests
// ============================================================================

func TestCreateLimitParam(t *testing.T) {
    // Main happy path test
    
    t.Run("consistency", func(t *testing.T) {
        // Edge case or consistency check
    })
}
```

### Test Organization Checklist
Before organizing tests:
- [ ] One test file per source file (no separate method or edge case files)
- [ ] Tests grouped by struct/type with clear comment headers
- [ ] Main test functions named after the method/function being tested
- [ ] Happy path tested in main function body
- [ ] Edge cases organized as subtests within main test function
- [ ] Descriptive subtest names that explain the scenario
- [ ] Related tests grouped together in logical sections

### Test Readability and Assertions
- **ALWAYS assert specific values rather than just checking existence**
- Tests should be self-documenting and easy to understand at a glance
- Use explicit assertions that show expected vs actual values
- Avoid generic assertions like `assert.NotNil()` when you can assert the specific expected value

### Examples of Clear Value Assertions
```go
// ❌ BAD - Vague assertions that don't show expected values
assert.NotNil(t, user)
assert.NotEmpty(t, user.Name)
assert.True(t, len(users) > 0)
assert.NoError(t, err)

// ✅ GOOD - Explicit value assertions
assert.Equal(t, "john.doe@example.com", user.Email)
assert.Equal(t, "John Doe", user.Name)
assert.Equal(t, 3, len(users))
assert.Nil(t, err, "Expected no error when creating valid user")
```

### Test Structure Guidelines
- **Arrange-Act-Assert pattern**: Clearly separate test setup, execution, and verification
- Use descriptive variable names that explain what they represent
- Set up test data with explicit, meaningful values
- Group related assertions together with clear comments

### Test Data Best Practices
```go
// ✅ GOOD - Explicit test data setup
func TestCreateUser(t *testing.T) {
    // Arrange
    expectedEmail := "test.user@example.com"
    expectedName := "Test User"
    expectedRole := "admin"
    
    userRequest := CreateUserRequest{
        Email: expectedEmail,
        Name:  expectedName,
        Role:  expectedRole,
    }
    
    // Act
    user, err := userService.CreateUser(userRequest)
    
    // Assert
    assert.Nil(t, err, "Expected no error when creating user with valid data")
    assert.Equal(t, expectedEmail, user.Email, "User email should match request")
    assert.Equal(t, expectedName, user.Name, "User name should match request")
    assert.Equal(t, expectedRole, user.Role, "User role should match request")
    assert.NotEmpty(t, user.ID, "User should have generated ID")
    assert.False(t, user.CreatedAt.IsZero(), "User should have creation timestamp")
}
```

### Test Naming Conventions
- Main test function should be named after the method being tested: `TestMethodName`
- Use sub-tests with `t.Run()` for different scenarios and edge cases
- Sub-test names should be descriptive and explain the scenario and expected outcome
- Group related test cases under the same main test function

### Examples of Good Test Structure
```go
func TestCreateUser(t *testing.T) {
    // Test the happy path first
    expectedEmail := "test.user@example.com"
    expectedName := "Test User"
    expectedRole := "admin"
    
    userRequest := CreateUserRequest{
        Email: expectedEmail,
        Name:  expectedName,
        Role:  expectedRole,
    }
    
    user, err := userService.CreateUser(userRequest)
    
    assert.Nil(t, err, "Expected no error when creating user with valid data")
    assert.Equal(t, expectedEmail, user.Email, "User email should match request")
    assert.Equal(t, expectedName, user.Name, "User name should match request")
    assert.Equal(t, expectedRole, user.Role, "User role should match request")
    assert.NotEmpty(t, user.ID, "User should have generated ID")
    assert.False(t, user.CreatedAt.IsZero(), "User should have creation timestamp")
    
    // Sub-tests for edge cases and error conditions
    t.Run("email must be unique", func(t *testing.T) {
        duplicateRequest := CreateUserRequest{
            Email: expectedEmail, // Same email as above
            Name:  "Another User",
            Role:  "user",
        }
        
        _, err := userService.CreateUser(duplicateRequest)
        assert.EqualError(t, err, "user with email 'test.user@example.com' already exists")
    })
    
    t.Run("invalid email format returns validation error", func(t *testing.T) {
        invalidRequest := CreateUserRequest{
            Email: "invalid-email",
            Name:  "Test User",
            Role:  "user",
        }
        
        _, err := userService.CreateUser(invalidRequest)
        assert.Contains(t, err.Error(), "invalid email format")
    })
    
    t.Run("empty name returns validation error", func(t *testing.T) {
        emptyNameRequest := CreateUserRequest{
            Email: "another@example.com",
            Name:  "",
            Role:  "user",
        }
        
        _, err := userService.CreateUser(emptyNameRequest)
        assert.Contains(t, err.Error(), "name is required")
    })
}
```

### Assertion Message Guidelines
- Include context in assertion messages to help debugging
- Explain what the test is verifying
- Use clear, descriptive language

### Table-Driven Tests
When using table-driven tests, make test cases self-explanatory:
```go
func TestValidateEmail(t *testing.T) {
    testCases := []struct {
        name          string
        email         string
        expectedValid bool
        expectedError string
    }{
        {
            name:          "valid email with standard format",
            email:         "user@example.com",
            expectedValid: true,
            expectedError: "",
        },
        {
            name:          "invalid email missing at symbol",
            email:         "userexample.com",
            expectedValid: false,
            expectedError: "invalid email format",
        },
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            valid, err := ValidateEmail(tc.email)
            
            assert.Equal(t, tc.expectedValid, valid, 
                "Email validation result should match expected for: %s", tc.email)
                
            if tc.expectedError != "" {
                assert.Contains(t, err.Error(), tc.expectedError,
                    "Error message should contain expected text for: %s", tc.email)
            } else {
                assert.Nil(t, err, "Expected no error for valid email: %s", tc.email)
            }
        })
    }
}
```

### Testing Checklist
Before submitting test code:
- [ ] **One test file per source file** (follow one-to-one mapping)
- [ ] **Tests organized by method/function** with proper naming (`Test<StructName>_<MethodName>`)
- [ ] **Edge cases as subtests** within main test functions
- [ ] **Clear section headers** to group tests by struct/type
- [ ] All assertions check specific expected values
- [ ] Main test function named after the method being tested
- [ ] Sub-tests with descriptive names for different scenarios
- [ ] Test data uses meaningful, explicit values
- [ ] Assertion messages provide helpful context for debugging
- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] Edge cases and error conditions are tested with specific assertions
- [ ] No generic assertions like `assert.True()` where specific values can be checked
- [ ] Happy path tested first, then edge cases in sub-tests

### Error Testing Best Practices
When testing error conditions:
```go
// ❌ BAD - Generic error checking
assert.Error(t, err)

// ✅ GOOD - Specific error validation
assert.EqualError(t, err, "user with email 'test@example.com' already exists")
// OR
assert.Contains(t, err.Error(), "already exists")
assert.IsType(t, &ValidationError{}, err)
```

## Build Artifacts and Binary Files

### Binary File Management
- **NEVER commit binary files or build artifacts to the repository**
- Build artifacts include but are not limited to:
  - Compiled Go binaries (e.g., `publicapis-gen`, executable files)
  - Coverage files (`coverage.out`, `coverage.html`) - these are temporary test artifacts
  - Any files generated by `go build` or similar build commands
- Always clean up build artifacts after testing or building

### Build Process
- Use `go build .` for local development and testing only
- Binaries should be built in CI/CD pipelines for releases
- If you accidentally commit a binary file, remove it immediately

### File Exclusions
Files that should NEVER be committed:
- Any executable files without extensions (typically Go binaries)
- `.exe` files (Windows binaries)
- Coverage output files (`*.out`, `coverage.html`)
- Temporary build files and artifacts