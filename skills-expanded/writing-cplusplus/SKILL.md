---
name: writing-cplusplus
description: Guidance for writing, reading, updating, building, and testing C++ code for the 64-bit RISC OS build environment. Use whenever Codex works on RISC OS C++ command projects, `cc/` sources, C++ headers in `h/`, `riscos64-c++`, `riscos-project --type c++command`, `${C++LIB}`, or C++ interop with C and RISC OS APIs.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-project:*) Bash(riscos-amu:*) Bash(riscos-build-run:*)
---

# Guidance for writing C++ code for RISC OS.

## Scope

Use this skill for C++ in the RISC OS cross-compilation environment. C++ is
currently supported only for 64-bit RISC OS builds.

Current caveats:

* Exceptions are not supported. Do not use `throw`, `catch`, or code paths that
  depend on exception unwinding.
* RTTI does not work. Do not use `typeid` or `dynamic_cast`.
* Templates are not tested. Avoid template-heavy designs unless the user has
  explicitly accepted the risk.
* C++ modules are not tested.

Prefer simple, explicit C++ using ordinary functions, classes, constructors,
destructors, references, and C-compatible interfaces where practical.

## Project Structure

Use the RISC OS source filename conventions:

* C++ sources live in `cc/` and have no host extension, for example `cc/main`.
* C and C++ headers live in `h/` and have no host extension, for example
  `h/countlib`.
* Include headers using their C/C++ names, for example `#include "countlib.h"`.
* Makefiles are named `Makefile,fe1`.
* The version include is usually `VersionNum`.

Do not create source files such as `cc/main.cpp` or headers such as
`h/countlib.h` unless the existing project already uses that convention.

Create a new C++ command skeleton with:

```sh
riscos-project create --type c++command --name <Name> --skeleton
```

The skeleton should build before it is extended.

## Build And Test

Build C++ command projects for 64-bit RISC OS:

```sh
riscos-amu BUILD64=1
```

Run the resulting absolute with `riscos-build-run --64`:

```sh
riscos-build-run --64 aif64/<Name>,ff8 --command <Name>
```

`riscos-build-run` creates a temporary RISC OS filing system and copies listed
files into its root. If the host file is `aif64/Testing,ff8`, run it as
`Testing`, not `aif64.Testing`.

For direct compiler use:

```sh
riscos64-c++ -c -o o.name cc.name
riscos64-link o.name -lsupc++ C:c++64.o.libc++-64 -o name,ff8
riscos-build-run --64 name,ff8 --command name
```

When using the RISC OS makefile system, put the C++ runtime in `LIBS`:

```make
LIBS       = ${CLIB} ${C++LIB}
```

List objects using `o.` names and let the build system vary them for 64-bit
builds:

```make
OBJS       = o.main \
            o.worker
```

## C++ Style

Match the surrounding project style first. For new C++ code:

* Use 4-space indentation.
* Put braces at the start of lines when that matches nearby RISC OS C/C++ code;
  otherwise follow the local C++ style already present.
* Do not leave trailing spaces.
* Keep `main` small and move reusable logic into separate functions or classes.
* Avoid magic numbers and strings; use named constants.
* Use `static` for file-local helper functions.
* Use `const` for values and references that should not be changed.
* Use RAII for simple ownership, but avoid constructors that need to report
  failure by throwing. Prefer explicit `init`, `open`, or `create` methods for
  operations that can fail.
* Avoid threads and re-entrancy assumptions. RISC OS is single-threaded.

Do not add broad abstractions just because C++ makes them possible. RISC OS is
memory constrained; keep interfaces small and predictable.

## Includes And Types

Common includes:

```cpp
#include <stdint.h>
#include <stdlib.h>
#include <iostream>
#include "kernel.h"
#include "swis.h"
```

Use fixed-width types at RISC OS and C ABI boundaries:

```cpp
int32_t value;
uint32_t flags;
uintptr_t address;
```

Use `uintptr_t` when converting pointers to integers. Be careful with
`_kernel_swi_regs`: 64-bit RISC OS headers may still represent SWI register
fields as 32-bit values.

## C And RISC OS Interop

Use `extern "C"` for functions compiled as C or exported to C:

```cpp
extern "C" int c_scale(int value, int multiplier);
```

For headers included from both C and C++:

```c
#ifdef __cplusplus
extern "C" {
#endif

int c_scale(int value, int multiplier);

#ifdef __cplusplus
}
#endif
```

Do not expose C++ classes, references, overloaded functions, exceptions, or
standard library types through C-callable interfaces.

RISC OS APIs often use C strings or control-terminated strings. Use C
zero-terminated strings for normal C/C++ interfaces, and control-terminated
strings only when the RISC OS API documents that convention.

## Comments

Retain existing comments where they remain correct. Add comments to explain
intent, not mechanical operations.

Use the project's existing file prologue style for new C++ source files:

```cpp
/*******************************************************************
 * File:        name
 * Purpose:     Description
 * Author:      AUTHOR
 ******************************************************************/
```

Do not use the bordered C function prologue format from the C skill for every
C++ member function unless the local C++ project already does so.

## Common Failures

If a build tries to produce or run 32-bit output, check that `BUILD64=1` and
`riscos-build-run --64` are both present.

If linking fails with missing C++ runtime symbols, check that `${C++LIB}` is in
`LIBS` for makefile builds, or that direct links include `-lsupc++` and the
C++ library object.

If code fails around exceptions, RTTI, templates, or modules, remove or isolate
that feature before chasing unrelated build issues.
