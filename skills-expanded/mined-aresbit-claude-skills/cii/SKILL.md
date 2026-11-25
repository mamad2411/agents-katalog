---
name: cii-skill
description: Write, design, or refactor C in the "C Interfaces and Implementations" (CII) style of David Hanson — strict interface/implementation separation, opaque `Module_T` ADTs (`typedef struct T *T` with a hidden struct), checked errors via assert, structured exceptions (`TRY`/`EXCEPT`/`RAISE`), arena/`Mem` allocation, and reusable ADT modules (Except, Mem, Arena, Atom, Table, Set, Seq, Ring, Text, Fmt, AP, MP, Thread, Chan). Use it whenever the user wants to *implement, design, or refactor* C this way: an opaque ADT with a hidden `struct T` and `Module_new`/`Module_free` lifecycle, exception-based (`setjmp`-style `TRY`/`RAISE`) error handling in C, an arena/region allocator, interned strings used as hash-table keys, an arbitrary/multiple-precision integer type, or a paired `.h` interface + `.c` implementation following Hanson's conventions — even if they don't name the book. Do NOT use this skill merely to summarize or explain the book or its chapters (it is for *writing* CII-style code, not describing it), for one-off generic C that isn't CII-structured (e.g. a quick linked-list reverse, a printf format question, a segfault/gdb debugging question), or for ADTs/exceptions/allocators in other languages (Rust, Python, Java, Go).
---

# CII — C Interfaces and Implementations

A discipline and a library for writing reusable C. This skill makes you write C the way David Hanson's book does: every reusable abstraction is an **interface** (a `.h` exposing an opaque type and operations) backed by a separate **implementation** (a `.c`), with errors split cleanly into *checked runtime errors* (`assert`) and *exceptions* (`TRY`/`RAISE`).

The bundled `headers/` directory contains the **authoritative interface headers** for all 20+ CII modules. When using a module, read its header for exact signatures — never guess them. The `references/` files explain semantics, idioms, and gotchas per module group.

## The house style — non-negotiable conventions

These conventions are what make code "CII style." Follow them exactly; consistency is the point of the discipline.

### 1. Interface and implementation are separate files

A module `Foo` is a pair: `foo.h` (the interface — the contract clients see) and `foo.c` (the implementation — hidden). Clients `#include "foo.h"` and link against `foo.o`. The interface exposes the *minimum*: an opaque type and the operations on it. Representation details live only in the `.c`.

### 2. Two-level naming: `Module_operation`

Every exported name is `Module_` + operation, e.g. `Table_get`, `Arena_alloc`. The module name is the namespace C lacks. Exported types are `Module_T`. There are no other globals without the prefix.

### 3. The opaque `T` pointer idiom

Inside an interface, abbreviate the exported type to `T` with a local macro, then undefine it at the end so it doesn't leak:

```c
#ifndef STACK_INCLUDED
#define STACK_INCLUDED
#define T Stack_T
typedef struct T *T;            /* opaque — clients never see the fields */

extern T     Stack_new (void);
extern int   Stack_empty(T stk);
extern void  Stack_push (T stk, void *x);
extern void *Stack_pop  (T stk);
extern void  Stack_free (T *stk);

#undef T
#endif
```

`struct T` is *defined only in the `.c`*. Clients hold `Stack_T` (a pointer) and cannot touch the fields — that is the encapsulation. Use this `#define T … / typedef struct T *T / … / #undef T` pattern for every ADT.

### 4. Lifecycle: `Module_new` constructs, `Module_free(&x)` destroys

Constructors return a fresh `T`. Destructors take the **address** of the variable (`T *`), free the object, and set the client's pointer to `NULL` so use-after-free is caught:

```c
Stack_T s = Stack_new();
...
Stack_free(&s);          /* s is now NULL */
```

### 5. Two error categories — keep them distinct

- **Checked runtime errors** = a client violated the interface contract (passed NULL, an out-of-range index, popped an empty stack). Catch with `assert(e)`. These are *bugs in the caller* and should abort. CII's `assert.h` re-raises `Assert_Failed` (see `references/error-handling.md`) — do **not** include the standard `<assert.h>`.
- **Exceptions** = a runtime situation the client may reasonably handle (out of memory, arithmetic overflow, I/O failure). Raise with `RAISE(e)`, handle with `TRY/EXCEPT`.

Every interface documents which errors it checks and which it raises. Begin each operation in the `.c` with `assert` guards on its arguments.

### 6. Allocation goes through `Mem`/`Arena`, never raw `malloc`

Use the `Mem` macros — `NEW(p)`, `NEW0(p)`, `ALLOC`, `CALLOC`, `RESIZE`, `FREE(p)` — which carry `__FILE__`/`__LINE__` and raise `Mem_Failed` on exhaustion (so you never check a NULL return). For region/phase allocation where you free everything at once, use `Arena`. See `references/memory.md`.

### 7. Generic containers store `void *`; clients supply `cmp`/`hash`

CII containers are not type-parametric — they hold `void *` and you pass comparison/hash functions (often using `Atom`s as keys so pointer identity == equality). Iteration uses the **apply/closure** idiom: `Module_map(t, apply, cl)` calls `apply(..., cl)` per element, where `cl` is an opaque client pointer threading state through.

## Module catalog — route to the right reference

Read the reference file for the group you need, then the specific header in `headers/` for exact signatures.

| Module(s) | Purpose | Reference |
|-----------|---------|-----------|
| `Except`, `assert` | Structured exceptions; checked-error assertions | `references/error-handling.md` |
| `Mem`, `Arena` | Production allocator; arena (region) allocator | `references/memory.md` |
| `Atom` | Immutable interned strings (pointer identity == equality) | `references/atom.md` |
| `List`, `Stack`, `Table`, `Set`, `Array`, `Seq`, `Ring`, `Bit` | Core containers & data structures | `references/containers.md` |
| `Fmt`, `Str`, `Text` | Type-safe formatting; non-destructive string ops; immutable text | `references/strings.md` |
| `AP`, `MP`, `Arith` | Arbitrary-precision & fixed-precision integer arithmetic | `references/arithmetic.md` |
| `Thread`, `Chan` | User-level threads; synchronous channels | `references/concurrency.md` |

For the design philosophy itself (how to *invent* a good interface, import/export granularity, when to expose representation) read `references/design-principles.md`.

## Writing a new CII-style module

When the user asks for a new module, **scaffold the pair first**, then fill it in. The bundled generator writes an idiomatic `.h`/`.c` skeleton (opaque `T`, the `#define T … #undef T` idiom, `Module_new`/`Module_free`, assert guards, `Mem` allocation) so you start in the right shape:

```bash
python scripts/new_module.py Stack --hint --ops "push,pop"   # → stack.h + stack.c
python scripts/new_module.py Node --transparent              # public struct, like List_T
```

Flags: `--hint` (constructor takes an `int hint`), `--transparent` (expose the representation), `--ops a,b,c` (stub extra operations), `--out DIR`, `--force`. Then define `struct T`, give each operation its real signature + documented checked-errors/exceptions, and fill in the bodies.

The shape it produces (and that you should match if writing by hand):

`foo.h` (interface):
```c
#ifndef FOO_INCLUDED
#define FOO_INCLUDED
#define T Foo_T
typedef struct T *T;

extern T    Foo_new (void);
extern void Foo_free(T *foo);
/* ... operations, each documenting its checked errors & exceptions ... */

#undef T
#endif
```

`foo.c` (implementation):
```c
#include <stddef.h>
#include "assert.h"
#include "mem.h"
#include "foo.h"
#define T Foo_T
struct T {              /* the hidden representation */
    ...
};

T Foo_new(void) {
    T foo;
    NEW(foo);           /* raises Mem_Failed on exhaustion */
    ...
    return foo;
}

void Foo_free(T *foo) {
    assert(foo && *foo);   /* checked runtime error: NULL handle */
    FREE(*foo);            /* sets *foo = NULL */
}
```

Notes that keep it idiomatic:
- Include order: standard headers, then `assert.h`/`mem.h`, then own interface last. Re-`#define T` at the top of the `.c` and the `struct T` definition makes the representation concrete.
- Guard every public function's arguments with `assert` first.
- Constructors that need a size hint take an `int hint` (advisory only). Destructors always take `T *`.
- Provide `Foo_free`, not `Foo_dispose`, unless mirroring `Arena_dispose` (whole-arena teardown).

## Worked examples and deep dives

The translated book chapters live at `/home/ares/yyscode/cii-code/docs/ch*.md` (Chinese, with line-by-line annotated source and modern-C notes). The original Hanson source is at `/home/ares/yyscode/cii-code/code/`. Point the user there for full implementations, algorithm analysis, or exercises; cite the relevant chapter when explaining *why* an interface is shaped the way it is.

When writing example client code, prefer small, complete, compilable programs. A typical CII program links the modules it uses: `cc main.c table.c atom.c mem.c arena.c except.c -o main`.
