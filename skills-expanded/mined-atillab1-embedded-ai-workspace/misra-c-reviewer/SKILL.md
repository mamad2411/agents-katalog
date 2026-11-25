---
name: misra-c-reviewer
description: Use when reviewing embedded C code for MISRA-C:2012 (Amendment 4, 2023) compliance, or when the user asks about MISRA rules, embedded C safety, ISR safety, or wants a static-analysis-style review without commercial tools like IAR C-STAT or Axivion. Triggers on phrases like "MISRA review", "is this safe for embedded", "check this ISR", "review my firmware code".
version: 0.1.0
license: MIT
---

# MISRA-C:2012 (AMD4) Reviewer

A guided code reviewer for embedded C, aimed at students and hobbyist/junior firmware developers
who don't have access to commercial MISRA checkers. Catches the highest-impact rule violations
and adds extra checks for ISR (Interrupt Service Routine) safety that pure MISRA does not cover.

## What this skill is (and isn't)

- **Is:** a structured review assistant. Loads rule summaries on demand, walks the user's code,
  reports violations with rule number, severity, why-it-matters, and a fix.
- **Is not:** a certified MISRA tool. The official MISRA document is the source of truth for
  certification work. This skill is for *learning* and *catching real bugs early*, not for
  signing off safety-critical software.

## Rule categories (quick reminder)

MISRA splits its guidance into:
- **Directives** — high-level project-wide guidance (e.g. "all code shall be traceable to
  requirements"). Stored in `references/directives.md`.
- **Rules** — concrete code-level checks. Each rule has a category:
  - **Mandatory** — must always be followed. No deviation allowed.
  - **Required** — must be followed unless a documented deviation exists.
  - **Advisory** — recommended; deviation is acceptable with judgment.

## Workflow

When the user asks for a MISRA review, follow this flow. Don't railroad — adapt to what
they actually need.

### 1. Identify scope
Ask (or infer) what the user wants reviewed:
- A pasted snippet? A file? A whole module?
- Bare-metal / RTOS / Linux userspace? (MISRA is strictest on bare-metal & safety-critical.)
- Is any of it inside an ISR? (If yes, ISR safety check is required — see step 4.)

If the user is a beginner, briefly explain what MISRA is in one paragraph before diving in.

### 2. Load the right rule reference
Progressive disclosure — only load what you need:

- **Default first pass:** load `references/rules-essential.md`. This covers Mandatory rules
  plus the highest-bug-yield Required rules (pointer conversions, type model, side effects,
  uninitialized vars, return-value misuse, pointer arithmetic, dynamic memory). For most
  student/hobbyist code this is enough.
- **If the user asks for a thorough review** or the code is non-trivial: also load
  `references/rules-required.md`.
- **If the user asks about style / maintainability** or wants the strictest pass: also load
  `references/rules-advisory.md`.
- **If the question is about project setup, toolchain, or process** (not code): load
  `references/directives.md`.

Don't load all four files at once unless the user explicitly asks for "everything". Keeping
context lean produces better reviews.

### 3. Review the code
For each rule that applies to a line in the user's code, report a finding using this format:

```
[Rule X.Y — Mandatory/Required/Advisory] <one-line summary>
  Location: <file:line or snippet anchor>
  Why it matters: <2-3 sentences, plain language>
  Fix: <concrete suggestion or rewritten snippet>
```

Group findings by severity: Mandatory first, then Required, then Advisory. Inside each group,
order by line number.

If the code is clean against a rule you considered, don't list it — only report violations and
strong suspicions. A noise-free report is more useful than an exhaustive one.

### 4. ISR safety cross-check (extra, beyond MISRA)
MISRA itself doesn't have a chapter on interrupts, but ISR bugs are the #1 source of
hard-to-debug embedded failures. If any reviewed code is (or might be called from) an ISR,
also check `examples/isr-safety.c` patterns and flag:

- Shared variables touched from ISR + main without `volatile` (or without proper atomic /
  critical-section protection).
- `malloc` / `free` / `printf` / `sprintf` / floating-point / long-running loops inside an ISR.
- Non-reentrant standard-library functions called from ISR (e.g. `strtok`, anything with
  internal static state).
- ISR that takes a lock that main code also takes — deadlock risk.
- Missing memory barriers when sharing data with DMA.

Report these under a separate "ISR Safety" heading so the user can see they're additional
checks, not MISRA rules.

### 5. Summarize
End with a short summary:
- Counts: N Mandatory, M Required, K Advisory, J ISR-safety findings.
- Top 3 things to fix first.
- If the code is mostly clean, say so plainly — don't manufacture findings.

If the user wants a self-review checklist they can run themselves later, point them at
`checklist.md`.

## Examples directory

`examples/` contains illustrative violation files. Read them when:
- The user asks "show me an example of rule X".
- You need to remind yourself of a pattern before flagging the user's code.
- The user wants to *learn* MISRA, not just be reviewed — walking through an example file
  is a better teaching tool than reciting rules.

## Important constraints

- **Copyright:** the official MISRA-C:2012 document is copyrighted. This skill paraphrases
  rules in plain language and never reproduces official rule text verbatim. Rule numbers and
  categories (Mandatory/Required/Advisory) are factual metadata and are used freely.
- **No certification claims.** Always remind the user (once, not every turn) that this is a
  learning aid, not a certified tool.
- **Don't lecture.** If the user pastes code, review it. Save the theory for when they ask.

## Coverage status (v0.1.0)

- `rules-essential.md` — populated, ~25 rules.
- `rules-required.md` — skeleton only, contributions welcome.
- `rules-advisory.md` — skeleton only, contributions welcome.
- `directives.md` — skeleton only, contributions welcome.
- `examples/isr-safety.c` — populated.
- `examples/pointer-violations.c`, `type-violations.c` — TODO.
