---
name: 6-free-dev-tools
description: Six free developer productivity tools — GitIngest (repo→AI context), GitDiagram (repo→architecture diagram), repomix (pack repo for LLM), transform.tools (code/data format converter), pglite (in-browser Postgres), and DevToys (offline Swiss Army knife for developers). Use when building LLM coding workflows, doing codebase analysis, or outfitting a dev environment. Source: @swblessed carousel.
---

# 6 Free Developer Tools

Six free tools that fill real gaps in developer workflows.

---

## 01. GitIngest — Turn Any Repo into AI-Ready Context

**URL**: gitingest.com

**What it does**: Takes any GitHub repo and produces a single text dump optimised for pasting into an LLM context window.

**How to use**: Replace `github.com/owner/repo` with `gitingest.com/owner/repo` in the browser — or use the CLI.

```bash
pip install gitingest
gitingest https://github.com/owner/repo
```

**Output**: One file with repo structure + all file contents, formatted to minimise token waste.

**Best for**: Asking an LLM to explain, audit, or extend an unfamiliar codebase.

---

## 02. GitDiagram — Repo to Architecture Diagram

**URL**: gitdiagram.com

**What it does**: Analyses a GitHub repository and generates an interactive architecture diagram showing how components connect.

**How to use**: Enter any public repo URL — the diagram renders in seconds.

**Output**: Clickable component graph — click a node to jump to the relevant file.

**Best for**: Onboarding to a new codebase, creating architecture documentation, understanding dependency flows.

---

## 03. repomix — Pack a Repo for LLM Input

**Repo**: github.com/yamadashy/repomix

**What it does**: Packs an entire codebase into a single XML/Markdown/plain-text file for LLM consumption. Like GitIngest but local, configurable, and respects `.gitignore`.

```bash
npx repomix
# generates repomix-output.txt with the full repo
```

**Best for**: Feeding a local repo into Claude or GPT-4 without a GitHub URL.

---

## 04. transform.tools — Code & Data Format Converter

**URL**: transform.tools

**What it does**: Converts between 40+ code and data formats in the browser — no install, no account.

**Supported conversions (sample)**:
- JSON ↔ TypeScript types
- JSON ↔ Zod schema
- JSON ↔ YAML / TOML / CSV
- GraphQL ↔ TypeScript
- SVG → React component (JSX)
- CSS ↔ JS-in-CSS (styled-components)
- HTML → JSX / Pug

**Best for**: Generating TypeScript interfaces from an API response JSON, converting config files between formats.

---

## 05. pglite — Postgres in the Browser (WASM)

**Repo**: github.com/electric-sql/pglite

**What it does**: Full Postgres running in the browser via WebAssembly — no server, no Docker, persistent storage via IndexedDB or OPFS.

```typescript
import { PGlite } from '@electric-sql/pglite';
const db = new PGlite();
await db.exec('CREATE TABLE users (id serial, name text)');
const result = await db.query('SELECT * FROM users');
```

**Best for**: Local-first apps, browser-based SQL demos, offline data tools, testing without a real DB server.

---

## 06. DevToys — Offline Developer Swiss Army Knife

**URL**: devtoys.app (Windows, macOS, Linux)

**What it does**: 30+ offline developer utilities in one desktop app — no internet required, no data leaves the machine.

**Built-in tools**:
- JSON ↔ YAML converter and formatter
- Regex tester with match highlighting
- JWT decoder (header + payload)
- Base64 encode/decode
- Text diff (side-by-side)
- Hash generator (MD5, SHA-1, SHA-256, SHA-512)
- URL encode/decode
- Unix timestamp converter
- Lorem Ipsum generator
- Color picker / converter (HEX ↔ RGB ↔ HSL)

**Best for**: Security-conscious environments where pasting tokens/JWTs into online tools is not allowed.

---

## Quick-reference table

| Tool | Where | Best for |
|---|---|---|
| GitIngest | gitingest.com | Repo → LLM context dump |
| GitDiagram | gitdiagram.com | Repo → architecture diagram |
| repomix | npm/npx | Local repo → LLM input file |
| transform.tools | transform.tools | Format conversions (JSON→TypeScript etc.) |
| pglite | npm | Postgres in the browser (WASM) |
| DevToys | devtoys.app | Offline dev utilities (JWT, Base64, diff) |

Source: @swblessed
