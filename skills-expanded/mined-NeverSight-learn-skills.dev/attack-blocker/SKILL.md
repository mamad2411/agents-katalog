---
name: attack-blocker
description: Resolve project blockers — missing dependencies, build failures, unlinked libraries, missing models, API keys. Uses 5 Whys root-cause analysis and a mandatory resolution sequence. Use when something is blocked or failing to build.
---

**Blockers are problems to solve, not facts to document.** "BLOCKED" means "I have not solved this yet." Attack every blocker with every available tool until it yields. The harder the problem, the more important it is to solve it first.

## 1. Diagnose — 5 Whys

Before any fix, ask "why?" five times to reach the root cause. Write it down. Fix the root cause, not the symptom.

## 2. Mandatory Resolution Sequence

Try each step in order. Stop at the first one that works:

1. **Research** — WebSearch for the library/tool + your platform. Look for package manager support, Homebrew, pre-built binaries, alternatives, official docs.
2. **Package manager** — Add to project config (SPM, npm, pip, cargo, go get, Maven), rebuild.
3. **Homebrew** — `brew install <name>`, link against Homebrew prefix.
4. **Pre-built binary** — Download release from GitHub, add to project.
5. **Compile from source** — `git clone`, build with cmake/make/cargo, link the result.
6. **For downloads (models, weights, binaries)** — Download immediately. "Needs download" is never a legitimate blocker. Use `curl -L`, `huggingface-cli download`, or `wget`.
7. **For API keys** — Register for a free/trial account, get the key, store it.
8. **For dev tools** — Install via brew/pip/npm/gem/cargo.

Only mark BLOCKED after ALL steps have been tried and failed, with specific error output documented.

## 3. Verify

After resolving: rebuild, run tests, confirm the feature works, replace all stub code (`// TODO`, `return ""`, `return nil`) with real implementations.

## Rules

- "It's a C++ library" / "it requires compilation" / "it's hard" are not reasons to give up.
- Never retreat to stubs. If you integrated a dependency, use it.
- Prove the fix works: build passes, tests pass, feature functions.
- You are allowed to install packages, clone repos, download files, register for services, generate keys, modify build configs, and write bridge/FFI code.
