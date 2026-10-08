# C Learning Project Collaboration Guide

This directory is for learning C for combinatorial-mathematics verification. When modifying or adding code, prioritize clarity, verifiability, and learning value over elaborate software architecture.

## Scope

- Programs in this repository primarily support mathematical computation: binomial coefficients, Catalan numbers, sets and graphs, combinatorial enumeration, backtracking search, and verification of mathematical identities.
- Introduce dynamic memory, structs, file I/O, bit operations, GMP, benchmarking, assertions, GDB, and Makefiles gradually and only when useful.
- Do not proactively introduce assembly, inline assembly, system-call wrappers, operating-system APIs, linked-list frameworks, or design patterns unrelated to mathematical verification.
- Do not add learning progress, personal information, or out-of-scope goals to source code or documentation unless the user explicitly requests it.

## Learning and Coding Guidance

- Teach the user how to develop each program step by step instead of providing a complete solution directly.
- Explain the relevant C concepts, the core idea of the algorithm, and the expected edge cases; then ask the user to write or revise the code.
- Give hints, pseudocode, or a small example when needed, but do not replace the user’s work with a finished program unless they explicitly ask for the full solution.
- Review the user’s code and point out specific improvements, design choices, and bug risks without writing the final program for them.

## Code Principles

- Each exercise should illustrate one main idea where possible. Put new programs in clearly named directories, such as `week2/` or a topic-specific directory.
- When creating a new exercise file, follow the same pattern as week1: keep each program self-contained in one `.c` file, use filenames in the format `[YYYY.MM.DD] short.c`, where the date is followed by a short description of no more than six letters, such as `[2026.08.31] hh.c`; begin with `#include <stdio.h>` when standard input/output is used, and use `int main(void)` with `return 0;` on success.
- Favor clear variable names, straightforward control flow, and small, focused functions over compact tricks or over-engineering.
- Add a short comment only when it explains the exercise or a non-obvious decision; do not comment every line.
- Use C11 by default. Code should compile cleanly with GCC using `gcc -std=c11 -Wall -Wextra -Wpedantic`.
- Use `int main(void)`. Give functions explicit parameter and return types; avoid implicit conversions and uninitialized variables.
- Keep names simple and direct. Prefer `size_t` for counts and indexes. Use a clearly wider type, or GMP when necessary, for intermediate results that may overflow.
- Check errors and boundaries for input, file operations, memory allocation, and numeric operations.
- Follow “the allocator frees” for dynamic memory. Store `malloc`/`realloc` results in a temporary pointer first, update the original pointer only after a successful allocation, and never use a pointer after freeing it.
- Provide paired `init_*` / `free_*` functions for structs that own resources. Callers should not need to guess ownership rules.
- Favor correctness and readability in mathematical enumeration code before optimizing it, and optimize only when benchmark data is available.

## Verification and Debugging

- Do not compile programs yourself. Ask the user to run the compiler and share any warnings or errors.
- After modifying C files, guide the user to compile affected programs locally and help them fix any newly introduced warnings, but never perform the compilation on their behalf.
- Add small, manually checkable test cases to mathematical programs. Output should include sufficient parameters to reproduce a result.
- Use `assert` for internal invariants, such as increasing elements in a combination, no duplicates in a permutation, or a count bounded by a known result.
- For heap-memory code, prefer AddressSanitizer with `-fsanitize=address,undefined -g`; use Valgrind for leak checks when available.
- Debug through source code, call stacks, and variable values. Do not introduce or depend on assembly-level debugging for this project.
- Performance comparisons must report compiler options, input size, and running time. Do not draw conclusions from a single run alone.

## Mathematical Computing Conventions

- Before bit-mask enumeration, check the type width. Never shift by a count equal to or greater than the width of the type.
- Use GMP `mpz_t` for exact results beyond 64-bit integer range, and ensure every `mpz_init*` has a matching `mpz_clear` or `mpz_clears`.
- Cross-check combinatorial formulas and enumeration results with an independent method whenever possible, such as small brute-force cases, symmetry identities, or known counts.
- For large output, prefer summary counts, configurable input sizes, and optional file output. Do not make massive terminal output the default.

## Project Evolution

- Do not create a general-purpose library too early during the single-file exercise stage.
- Split code into `.c` and `.h` files and add a minimal Makefile only once a verification program has separate enumeration, checking, and output responsibilities.
- Ask for approval before adding any dependency. GMP is an expected dependency in this learning plan; when using it, document the required `-lgmp` compiler flag.
