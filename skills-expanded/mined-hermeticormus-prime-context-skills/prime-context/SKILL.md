---
name: prime-context
description: Prime project context at the start of a session by reading the project's words, mapping the structure, identifying the stack and key files, summarizing current state from recent git, and producing a compact orientation. Use when opening a project you have not seen this session, switching projects, or resuming after a context clear.
license: MIT
---

# Prime context

A priming protocol for the start of a session. Run it when you open a project you have not seen this session, before doing any work.

**Tradeoff**: priming costs a few reads up front. For a one-line change in a file you already hold, skip it.

## 1. Read the project's own words

Read `README.md` first, then the root manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`).

The declared scripts reveal how the project builds, tests, and runs; the dependencies reveal the stack.

## 2. Map the structure

List the directory tree two to three levels deep, excluding build and dependency directories. Identify where source, tests, and config live, and name the entry points.

## 3. Identify the stack and key files

State the language, framework, package manager, and test runner. Name the three to five files a new contributor would read first.

## 4. Summarize the current state

Read the branch, the last five commits, and the working-tree status. Recent git is the difference between the project's intent and its present.

## 5. Produce a compact orientation

Collapse the above into a short summary: what the project is, the stack, structure and entry points, current state. Keep it tight. The point is a model you carry, not a document you file.

---

See full content at https://github.com/HermeticOrmus/prime-context-skills.
