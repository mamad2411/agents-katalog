# C Project System Prompt — Agent Behavior Rules and C Project Entry Point

## Purpose

This file defines the operational rules for AI agents working on C projects. It establishes decision criteria for language standard selection, build system choices, code quality standards, and project layout conventions. Agents MUST follow these rules unless project-specific constraints override them.

## Language Standard Decision Rules

### C17 vs C23

**Decision Rule:** Default to **C17 (C18)** unless ALL of the following conditions are met:
1. The user explicitly requests C23 features
2. The target compiler supports C23 (`__STDC_VERSION__ == 202311L`)
3. The deployment environment has C23 runtime support

```bash
# Always verify compiler C standard support
# GCC 14+ supports C23 draft features
gcc --version | head -1
echo '#if __STDC_VERSION__ < 202311L' | gcc -xc -c - -o /dev/null 2>&1

# Check specific feature support with feature test macros
# C23 adds: nullptr, typeof, bool, true, false as keywords, etc.
```

**C23 Feature Checklist Before Use:**
- [ ] `nullptr` — Only if `__STDC_VERSION__ >= 202311L`
- [ ] `bool`, `true`, `false` keywords — C99+, universally supported
- [ ] `typeof` — GCC extension, NOT standard C23 (use `__typeof__` for portability)
- [ ] `alignas`, `alignof` — C11+, use `<stdalign.h>` for C99
- [ ] `constexpr` — NOT in C23, reserved for future use
- [ ] `#embed` — GCC 13+, Clang 16+, may not be available

**Anti-pattern — Assuming C23 Support:**
```c
// BAD: Assumes C23, breaks on GCC 11, Clang 12, MSVC
#include <std/stdarr.h>  // Does not exist

// GOOD: Explicit version check
#if __STDC_VERSION__ >= 202311L
    #include <std/stdarr.h>
    // Use C23 array views
#else
    #include "custom_array_view.h"  // Fallback
#endif
```

### Standard Library Usage

**Decision Rule:** Prefer **POSIX standard library** for cross-platform Unix/Linux/macOS projects. Note Windows constraints explicitly.

| Feature | POSIX | Windows | Notes |
|---------|-------|---------|-------|
| Threads | `<pthread.h>` | CreateThread | Use abstraction layer |
| Sockets | `<sys/socket.h>` | Winsock (winsock2.h) | Use abstraction layer |
| File ops | `<fcntl.h>`, `<unistd.h>` | `<windows.h>` | Use abstraction layer |
| Shared memory | `<sys/mman.h>` | CreateFileMapping | Use abstraction layer |
| Memory-mapped I/O | `<sys/mman.h>` | CreateFileMapping + MapViewOfFile | Use abstraction layer |

**Minimum Portable Subset for Cross-Platform:**
```c
#include <stdio.h>    // fopen, fprintf, printf, fread, fwrite
#include <stdlib.h>   // malloc, free, exit, atexit, qsort, bsearch
#include <string.h>   // strlen, strcmp, memcpy, memmove, memset
#include <stdint.h>   // int64_t, uint32_t, SIZE_MAX, etc.
#include <stdbool.h>  // bool, true, false (C99+)
#include <stddef.h>   // NULL, size_t, ptrdiff_t, offsetof
#include <assert.h>   // assert, static_assert
#include <limits.h>   // INT_MAX, LONG_MAX, etc.
```

### Diagnostic Levels

**Rule:** Treat warnings as errors for all generated code. Warnings MUST be justified with inline comments or fixed.

```makefile
# GCC/Clang: Treat warnings as errors
CFLAGS += -Wall -Wextra -Wpedantic -Werror

# MSVC
# CFLAGS += /W4 /WX
```

**Common Warnings and Required Actions:**

| Warning | Code Pattern | Required Action |
|---------|-------------|-----------------|
| `-Wconversion` | Implicit type casts | Add explicit casts |
| `-Wsign-conversion` | signed/unsigned mix | Use uintmax_t/intmax_t for mixed arithmetic |
| `-Wshadow` | Variable shadowing | Rename variables |
| `-Wmissing-field-initializers` | Partial struct init | Use designated initializers |
| `-Wold-style-declaration` | Old-style declarations | Use modern declarations |
| `-Wstrict-prototypes` | Missing function prototypes | Always declare function prototypes |

### Code Generation Requirements

**Rule:** ALWAYS produce compilable, warning-free code. Never produce pseudocode.

**Anti-pattern — Pseudocode Generation:**
```c
// BAD: Never do this
// TODO: implement this function
int calculate_something(int x) {
    // do stuff with x
    return result;
}
```

**Correct Approach:**
```c
// GOOD: Always provide a working stub or explicit TODO with implementation
int calculate_something(int x) {
    if (x < 0) {
        return -1;  // Explicit invalid input handling
    }
    // TODO(impl): Add actual calculation when requirements are clarified
    // For now: identity function as placeholder
    return x;
}
```

## Build System Defaults

### Decision Tree

```
Project Type → Build System
─────────────────────────────────────────────────────────
Small single-module       → Plain Makefile
Multi-module (1-10 files) → Makefile with pattern rules
Cross-platform library    → CMake
Kernel / OS development   → Custom Makefile / Kbuild
Embedded (bare-metal)     → Custom Makefile or CMake
Large enterprise          → CMake with submodules
```

### Preferred Toolchain

**Default (Unix-like):** GCC with:
```bash
CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -Werror -std=c17 -O2 -g
LDFLAGS =
```

**Alternative (macOS, BSD):** Clang with compatibility:
```bash
CC = clang
CFLAGS = -Wall -Wextra -Wpedantic -Werror -std=c17 -O2 -g
# Use gcc or cc for portability in scripts
```

**Cross-compilation (embedded):**
```bash
CC = $(TARGET)-gcc
CFLAGS = --target=$(TARGET) -mcpu=$(CPU) -Os
SYSROOT = $(TOOLCHAIN)/$(TARGET)/sysroot
CFLAGS += --sysroot=$(SYSROOT)
```

### Build Output Requirements

**Rule:** Always produce `compile_commands.json` for IDE support.

```bash
# GCC/Clang with Bear (build command wrapper)
bear -- make

# CMake (automatic)
cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
```

### Build System Templates

**Makefile for single-module project:**
```makefile
# Makefile for single-module C project
CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wpedantic -Werror -std=c17 -O2 -g
LDFLAGS ?=

TARGET = myapp
SRC = main.c
OBJ = $(SRC:.c=.o)

.PHONY: all clean run test

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $@ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) $(OBJ)

test: $(TARGET)
	./$(TARGET) --test

# Include dependencies
-include $(OBJ:.o=.d)

%.d: %.c
	$(CC) $(CFLAGS) -MM $< > $@
```

**CMakeLists.txt for multi-module project:**
```cmake
cmake_minimum_required(VERSION 3.16)
project(myapp C)

set(CMAKE_C_STANDARD 17)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Warning flags
add_compile_options(
    -Wall -Wextra -Wpedantic -Werror
    $<$<C_COMPILER_ID:MSVC>: /W4 /WX>
)

# Enable AddressSanitizer for debugging
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
if(ENABLE_ASAN)
    add_compile_options(-fsanitize=address -g)
    add_link_options(-fsanitize=address)
endif()

# Source groups
file(GLOB_RECURSE SOURCES "src/*.c")
file(GLOB_RECURSE HEADERS "include/*.h")

add_executable(myapp ${SOURCES} ${HEADERS})
target_include_directories(myapp PUBLIC "${CMAKE_SOURCE_DIR}/include")

# Testing
enable_testing()
find_package(CMocka REQUIRED)
add_subdirectory(tests)
```

## Header/Source Layout Rules

### Rule 1: One Header Per Module

Each logical module gets exactly one `.h` file. Private declarations stay in the `.c` file.

```
module_name/
├── module_name.h       # Public API
├── module_name.c       # Implementation
├── module_name_private.h  # Optional: semi-private, for internal use
└── module_name_test.c  # Optional: unit tests
```

### Rule 2: Include Guards or #pragma once

**Preferred: #pragma once** (simpler, widely supported)

```c
#pragma once

#include <stddef.h>  // For size_t
#include <stdbool.h>

// Public types
typedef struct ModuleConfig ModuleConfig;

// Public API
ModuleConfig* module_create(void);
void module_destroy(ModuleConfig* config);
int module_process(const ModuleConfig* config, const char* input, char* output, size_t output_size);
```

**Alternative: Include Guards** (required for pre-C23 compilers with identical base names)

```c
#ifndef MODULE_NAME_H
#define MODULE_NAME_H

/* same content */

#endif /* MODULE_NAME_H */
```

### Rule 3: Self-Contained Headers

Every header must compile standalone without prior declarations.

```c
// BAD: forward declaration needed
typedef struct Foo Foo;  // Opaque type
Foo* create_foo(void);

// GOOD: All types defined before use
typedef struct Foo {
    int value;
    char* name;
} Foo;

Foo* create_foo(void);
```

### Rule 4: Include Order

Headers must be self-contained. Include in this order:
1. Corresponding implementation header (e.g., `foo.h` in `foo.c`)
2. Public API headers of dependencies
3. Standard library headers
4. System headers

```c
// foo.c
#include "foo.h"          // 1. Corresponding header first
#include "bar.h"          // 2. Dependency public headers
#include <stdlib.h>       // 3. Standard library
#include <string.h>
#include <assert.h>
```

### Rule 5: Minimal Header Dependencies

Public headers should not include headers they don't directly use.

```c
// BAD: module.h includes string.h but doesn't use it
#include <stddef.h>
#include <string.h>  // Not needed here

// GOOD: Only include what the header actually uses
#include <stddef.h>  // Only needed for size_t
```

## Checklist

- [ ] C17 is the default standard; C23 requires explicit request and compiler verification
- [ ] All generated code compiles with `-Wall -Wextra -Wpedantic -Werror`
- [ ] No pseudocode or TODO stubs without at least a working placeholder
- [ ] `compile_commands.json` is generated for IDE support
- [ ] One header per module with `#pragma once`
- [ ] Self-contained headers that compile without prior declarations
- [ ] Standard library usage is documented for portability
- [ ] Windows constraints are explicitly noted
- [ ] POSIX functions are abstracted for cross-platform projects

## Example Prompt Snippets

**Starting a new C project:**
```
Create a new C project called "csvtool" in /projects/csvtool/
- Multi-module layout with separate modules for parsing, validation, output
- Use CMake as build system
- Generate compile_commands.json
- Include unit tests with cmocka
```

**Adding a new module:**
```
Add a new module "lexer" to the existing C project at /projects/mylang/
- Follow existing header/source layout conventions
- Create lexer.h and lexer.c
- Include proper include guards
- Add a unit test file lexer_test.c
```

**Cross-compiling for embedded:**
```
Add cross-compilation support to /projects/firmware/
- Target: ARM Cortex-M4, thumb mode
- Toolchain: arm-none-eabi-gcc
- No dynamic allocation (embedded target)
- Produce a .elf and .bin file
```

**Compiler feature detection:**
```
Check if the current compiler supports C23 nullptr
- Print __STDC_VERSION__ and __GNUC__ versions
- Provide a portable fallback if nullptr is not available
- Use #if __STDC_VERSION__ >= 202311L conditional
```
