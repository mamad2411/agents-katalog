# AGENTS.md - Guidelines for AI Agents

This document provides guidelines for AI agents working on this codebase.

## Project Overview

This is a C project implementing a notebook/note-taking application. It uses a custom dynamic array implementation with a vtable pattern for type-specific operations. The project uses a macro-based system to generate type-safe containers.

## Build Commands

```bash
make        # Build the project
make run    # Build and run the application
make clean  # Remove build artifacts
make rebuild # Clean and rebuild
make test   # Run all tests
```

**Compiler flags:** `-Wall -Wextra -std=c11 -ggdb -I. -Isrc`

**Output:** Generates `notebook` executable

### Running Tests

The project uses a custom lightweight testing framework:

```bash
make test   # Run all tests
```

Test files are in `tests/` directory:
- `tests/tests.h` - Test framework macros (`TEST()`, `RUN_TEST()`)
- `tests/array.c` - Array module tests (14 tests)
- `tests/string.c` - String module tests (7 tests)

## Core Concepts

### Array System

The project uses a custom generic dynamic array with vtable support:
- `Array` - base container struct with data, size, len, cap, and vtable
- `ArrayVTable` - vtable for type-specific free/copy operations
- `define_array_kind()` - macro to generate type-safe container functions
- `define_full_array_kind()` - macro to generate typedef + functions

### String Type

Built on top of the array system using `define_full_array_kind(String, char, NULL)`.

## Code Style Guidelines

### General

- Use C11 standard (`-std=c11`)
- All source files must compile with `-Wall -Wextra`
- Use tabs for indentation (not spaces)
- Maximum line length: 100 characters (soft limit)

### Naming Conventions

- **Functions/variables:** `snake_case` (e.g., `array_init`, `item_size`)
- **Macros/constants:** `SCREAMING_SNAKE_CASE` (e.g., `DEFAULT_ARRAY_SIZE`)
- **Types/structs:** `PascalCase` (e.g., `Array`, `ArrayVTable`)
- **File names:** `snake_case.c` / `snake_case.h`

### Header Files

- Always use header guards:
  ```c
  #ifndef FILENAME_H
  #define FILENAME_H
  // ...
  #endif
  ```
- Public API goes in `.h` files, implementation in `.c` files
- Include dependencies in this order:
  1. System headers (`<stdio.h>`, etc.)
  2. Local headers (`"array.h"`, etc.)

### Functions

- Use K&R brace style:
  ```c
  bool function_name(int param)
  {
    // ...
  }
  ```
- Return `bool` for functions that indicate success/failure
- Prefer early returns for error conditions
- Check all pointers for NULL before using them

### Error Handling

- Return `false`/`NULL` on failure, `true`/valid pointer on success
- Always validate function parameters at the start
- Use descriptive error patterns:
  ```c
  if (!param)
    return false;
  ```

### Macros

- Use macros for type-safe container operations (see `define_array_kind` pattern)
- Use capitalized names for macro functions (e.g., `array_get_as`)
- Wrap multi-statement macros in `do { ... } while(0)`

### Structs and Types

- Use typedef for structs: `typedef struct name { ... } name;`
- Use vtables for polymorphic behavior
- Prefix member variables with descriptive names

### Comments

- Use C99-style `//` comments (not `/* */` unless for file headers)
- Comment complex logic or non-obvious code
- Document public API functions in headers

### Memory Management

- Follow ownership semantics: allocate in constructor, free in destructor
- Always check `malloc`/`realloc` return values
- Set pointers to NULL after freeing: `free(ptr); ptr = NULL;`

### Code Organization

```
.
├── main.c                 # Entry point
├── Makefile               # Build configuration
├── src/
│   ├── types/
│   │   ├── array/
│   │   │   ├── array.h    # Array implementation and macros
│   │   │   └── array.c
│   │   └── string/
│   │       ├── string.h  # String type (uses array macros)
│   │       └── string.c
│   ├── memo/              # Memo module (TODO)
│   ├── menu/              # Menu module (TODO)
│   └── notebook/          # Notebook module (TODO)
├── tests/
│   ├── tests.h            # Test framework macros
│   ├── array.c            # Array tests (14 tests)
│   └── string.c           # String tests (7 tests)
└── .clangd                # clangd configuration
```

- Group related types in subdirectories under `src/`
- One major type per header/source pair
- Keep headers self-contained when possible

## Common Patterns

### Array Type Definition
```c
typedef struct TypeVTable {
  void (*free)(void *elem);
  void (*copy)(void *dest, const void *src);
} TypeVTable;

define_full_array_kind(Type, type_t, &Type_vtable);
```

### Iteration
```c
Type *item;
foreach (item, &container) {
  // work with item
}
```

## Adding New Features

1. Create header/source pair in appropriate directory
2. Follow naming conventions
3. Add to Makefile if new directory created
4. Test with `make clean && make && make test`
5. Ensure no warnings with `-Wall -Wextra`

## Editor Configuration

For VSCode/Cursor, add to `.vscode/c_cpp_properties.json`:
```json
{
  "configurations": [{
    "compilerPath": "gcc",
    "cStandard": "c11",
    "cppStandard": "c11",
    "intelliSenseMode": "linux-gcc-x64"
  }]
}
```

Format settings:
- Tab size: 4
- Insert spaces: false (use tabs)