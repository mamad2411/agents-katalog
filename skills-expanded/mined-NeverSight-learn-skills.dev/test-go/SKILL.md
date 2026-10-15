---
name: test-go
description: Generate Go unit tests by analyzing source file flow and ensuring 80%+ coverage.
---

# Go Test Skill

Generate unit tests by analyzing the source file's functions, branches, and logic flow.

## Commands

| Command | Description |
|---------|-------------|
| `/test-go create <path>` | Create tests for a file, folder, or module |
| `/test-go update <path>` | Update existing tests |

`<path>` can be:
- A file: `user.go` or `#File`
- A folder: `internal/usecase/` or `#Folder`
- A module/package name: `auth`, `user`

**Tip**: Use Kiro's `#File` or `#Folder` context to quickly reference paths.

## Workflow

### Step 1: Analyze Source File

Read the source file and identify:
- All exported functions/methods
- All code branches (if/else, switch, for loops)
- All error return paths
- All dependencies (interfaces) that need mocking
- All possible panic scenarios

### Step 2: Create Test Plan

For each function/method found:
1. List all execution paths
2. Identify inputs that trigger each path
3. Determine expected outputs for each path
4. Note edge cases (nil, empty, zero, boundary)

### Step 3: Generate Tests

Create table-driven tests that cover every path identified in Step 2.

## Coverage Target: 80%+

Every test file must cover:
- All exported functions
- All if/else branches
- All switch cases
- All error return statements
- All loop conditions

## Consistent Pattern

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name    string
        input   InputType
        want    OutputType
        wantErr bool
    }{
        // Test cases for each execution path
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := FunctionName(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Naming Convention

- Test file: `[source-file]_test.go` (same directory)
- Test function: `Test[FunctionName]`
- Test case name: Describes the scenario being tested

## Mocking

Use interfaces for dependencies and create mock implementations:
```go
type mockDep struct {
    funcName func(args) (result, error)
}
```

## Running Tests

```bash
go test ./...                           # Run all
go test -cover ./...                    # With coverage
go test -coverprofile=coverage.out ./...  # Generate report
```
