# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal learning and reference repository for systems programming, algorithms, and computer science fundamentals. It is **not a single unified application** — each subdirectory is an independent, self-contained unit.

## Directory Structure

- `code/` — Personal C++ exercises (OOP, templates, inheritance, memory management)
- `code_book/` — Textbook implementations organized by book/topic:
  - `APUE/` — Advanced Programming in the UNIX Environment
  - `TCPL/` — The C Programming Language
  - `c++_primer/`, `c++template/`, `effectiveC++/`, `inside_cpp_object_model/` — C++ deep dives
  - `csapp/` — Computer Systems: A Programmer's Perspective
  - `labuladong/`, `leecode/` — Algorithm practice
  - `Design_Patterns/`, `Generic_Programming_STL/` — Software design
  - `AssemblyLanguage/`, `kernel/` — Low-level systems
- `go/` — Go implementations of algorithms and LeetCode problems
- `ai/` — CUDA and ML-related experiments
- `md/` — Technical notes (AI, CUDA, Linux, ELF, performance, interview prep)
- `template/` — C++ file header template
- `env/` — Personal environment config (bashrc, gitconfig, vimrc)

## Building Individual Programs

There is no single root-level build system. Each exercise compiles independently.

**C/C++ single file:**
```sh
gcc -Wall -g -o out file.c
g++ -std=c++11 -Wall -g -o out file.cpp
```

**Using the TEMPLATE Makefile pattern:**
```makefile
CC=gcc -Wall -c -g
LD=gcc
```

**APUE programs** use their own `Makefile` under `code_book/APUE/master/`.

**Go programs:**
```sh
go run file.go
go build ./...
go test ./...
```

**Thinking C++ chapters** have `runall.sh` scripts to build all examples in a chapter directory.

## Languages

- **C++** — Primary language (systems programming, templates, STL, OOP)
- **C** — UNIX/systems programming (APUE, TCPL)
- **Go** — Algorithm and interview problem solutions
- **Assembly** — x86 learning exercises
- **Python** — Minimal (ML experiments in `ai/`)

## Code Style / Conventions

- C++ files use the header guard pattern: `#ifndef FOO_H / #define FOO_H / #endif`
- File headers include author (Jimmy Han), date, and version comments
- No external package managers or dependency files — all code is self-contained
- `.gitignore` excludes build artifacts: `*.exe`, `*.o`, `*.a`, `go/bin/*`, `go/pkg/*`
