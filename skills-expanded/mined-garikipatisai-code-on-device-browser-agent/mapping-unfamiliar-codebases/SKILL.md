---
name: mapping-unfamiliar-codebases
description: Use when asked to understand, map, or onboard to an unfamiliar codebase, module, or subsystem end-to-end — before answering architecture questions, before changing code you haven't read, or when a repo/directory is too large to read solo without burning your own context.
---

# Mapping Unfamiliar Codebases

## Overview

Recon cheaply yourself to find the module boundaries, then push essentially *all* substantial file-reading into parallel agents — including the core files, however tempting it is to read those yourself for "first-hand certainty." Reserve your own direct reads for the initial recon and a handful of targeted spot-checks afterward.

Specializes superpowers:dispatching-parallel-agents (general N-problems→N-agents fan-out) for the specific case of building a mental model of code.

## When to Use

An unread directory/subsystem/repo you need to explain, change, or audit end-to-end, with more than ~15 files. **Not for:** a handful of files (just Read them) or a lookup with a known target (grep/Read directly — this builds a model, it doesn't find a symbol).

## The mistake this fixes

The natural move is to self-read the files that feel most load-bearing ("I want first-hand certainty on the core") and only delegate the obviously-large peripheral stuff. That feels rigorous but is strictly worse: reading a 900-line state machine serially is slower than N agents reading it concurrently, and it burns exactly the context you were trying to protect by delegating at all. Nothing stops you from directly verifying the 2-3 most critical claims *after* a delegate reports them — that's cheap. Reading the core yourself *up front*, instead of delegating it too, is not.

## The pattern

1. **Recon cheaply yourself** — `ls`/tree, README, package/manifest, a directory listing of the module. Minutes, not an investigation. Goal: natural module boundaries + a file list per boundary.
2. **Partition into independent domains**, ~5-15 files each. Add a "design docs / history" domain if specs, ADRs, or notably-themed commits exist — the *why* isn't recoverable from source alone.
3. **Dispatch all of them in parallel**, one agent per domain, single message, concurrent. Use `general-purpose`, **not** `Explore` — Explore reads excerpts to *locate* code and will miss content; this needs full reads and open-ended synthesis. Delegate the core domain too — it's exactly the one worth its own dedicated agent, not the one to keep for yourself.
4. **Give every agent the same prompt shape**: shared context, its exact file list (absolute paths), a few focused questions, and a fixed report template so outputs stitch later — Purpose; Key exports (one line each); Data/control flow (what calls in, what it calls out to — name other domains); Invariants/gotchas; Unfinished/limitations. Ask for file:line citations on load-bearing claims and for uncertainty to be flagged, not smoothed over.
5. **Spot-verify, don't re-read wholesale.** Once reports land, directly Read the 1-3 files behind the most safety-critical, surprising, or flagged-uncertain claims. A couple of Reads earns certainty; reading everything yourself first does not.
6. **Synthesize a narrative, don't concatenate.** Trace one concrete flow through every domain in order, then name the 2-4 design principles that recur across domains. State scope explicitly: what you covered, what you left out, and why.

## Common Mistakes

- Using `Explore` for this — built for locating code, not open-ended synthesis; misses content past its read window.
- No fixed report template across agents — reports come back in incompatible shapes and don't stitch.
- Concatenating N reports instead of synthesizing — pushes the integration work onto the reader.
- Skipping design docs/history — misses *why*, not just *what*.
