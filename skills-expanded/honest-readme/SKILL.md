---
name: honest-readme
description: >-
  Write READMEs and project docs that describe what the thing is and how to run
  it, without marketing fluff or badge spam. Use this WHENEVER you create or edit
  a README, a repo description, a docs landing page, or a package summary.
  Superlatives ("blazingly fast", "production-ready", "powerful", "seamless"),
  rows of decorative badges, emoji-prefixed headings, and a "Features" list of
  vague adjectives are the tell that a model or a template wrote it. Replace them
  with a plain one-line description, a real install and usage example, and claims
  that are specific and true. Pair with no-filler-phrases for the prose.
---

# Honest README

A README exists to answer three questions fast: what is this, how do I run it,
and how do I use it. Most AI-written or template READMEs bury those under a hero
of badges, a tagline like "Blazingly fast, production-ready, developer-first
toolkit", and a "Features" list where every bullet is an adjective. That styling
reads as generated, and worse, it tells the reader nothing.

The rule: every line earns its place by informing the reader. If a sentence would
be just as true of a hundred other projects, cut it or make it specific.

## Cut these

- **Superlatives and hype:** "blazingly fast", "lightning-fast", "powerful",
  "robust", "seamless", "elegant", "production-ready", "battle-tested",
  "enterprise-grade", "next-generation". Either show the claim (a benchmark
  number, a real constraint) or drop it.
- **Badge spam:** a wall of shields.io badges for every CI, coverage, license,
  downloads, and "made with love". Keep at most the few a maintainer actually
  checks (build status, version, license). Decorative badges go.
- **Emoji-prefixed headings:** `## 🚀 Features`, `## ✨ Installation`. Plain
  headings. (If you want an icon in a hosted doc, see `prefer-icons`.)
- **Vague feature lists:** "Fast. Simple. Flexible. Modern." A reader cannot act
  on these. Replace with what the thing actually does.
- **Filler intros:** "In today's fast-paced world of software development...".
  Start with what the project is.

## Write these instead

- **One plain sentence up top** that says what it is and who it is for: "A CLI
  that converts Figma frames to React components." No tagline gymnastics.
- **A real install line** people can copy: `npm install x`, `pip install x`.
- **A minimal usage example** that actually runs, with real-looking input and
  output, not pseudo-code.
- **Specific, true claims.** Not "highly configurable" but "configured through a
  single `config.toml`; see the options below."
- **Requirements and limits** if they matter: supported versions, platforms, the
  one thing it deliberately does not do.

## Before and after

Before:
```
# ⚡ TurboParse

> 🚀 A blazingly fast, production-ready, developer-first parsing toolkit.

[badge][badge][badge][badge][badge]

## ✨ Features
- Fast
- Simple
- Flexible
- Modern
```

After:
```
# TurboParse

Parses large CSV files into typed records, streaming, without loading the whole
file into memory.

## Install
npm install turboparse

## Usage
... a short example that runs ...
```

## Before you deliver

Read the README top to bottom as a stranger. For each line ask: does this tell me
something specific and true, or is it decoration? Cut every adjective you cannot
back up, every badge a maintainer would not check, and every emoji on a heading.
What remains should let someone install and use the thing in under a minute.

For the sentence-level fluff inside the prose, pair this with `no-filler-phrases`,
`no-em-dashes`, and `no-fancy-ascii`.
