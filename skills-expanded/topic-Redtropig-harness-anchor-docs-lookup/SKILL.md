---
name: docs-lookup
description: Use when looking up unfamiliar tools, APIs, errors, library behavior. Context7 → WebSearch → calibrated uncertainty fallback chain. Don't guess.
---

# Docs Lookup (with fallback)

When you need authoritative information about an unfamiliar **tool / API / error message / library behavior**, follow this fallback chain. Each step has explicit success and failure criteria so the agent never silently degrades to guessing.

```
Step 1: Structured docs MCP   (Context7; or Microsoft Learn for .NET/Azure/Windows/MSVC)
   ↓ (unavailable / no match / wrong content / tool error)
Step 2: WebSearch     (broader web, recent ecosystem changes)
   ↓ (unavailable / no useful results / paywalled)
Step 3: Calibrated uncertainty (tell user what you tried + what's needed)
```

**You do not skip steps.** If Step 1 fails, you go to Step 2. If Step 2 fails, you go to Step 3. You do NOT retry Step 1 with the same query hoping for a different answer.

---

## Step 1: Structured docs MCP — Context7, or a first-party MCP for its ecosystem

**When it's the right tool**: API references, configuration options, well-known libraries (React, CMake, Clang, etc.), version-specific behavior.

**Two-call usage** (typical Context7 / Microsoft Docs MCP shapes):

```
1. resolve-library-id(library_name)            → canonical id, e.g. /llvm/clang
2. get-library-docs(id, topic="<question>")    → structured snippet + citation URL
```

(Tool names vary by harness: `mcp__Context7__*`, `mcp__plugin_context7_context7__*`, `mcp__73bcda44-…__query-docs`, etc. Use whatever resolves to "Context7" in your tool inventory.)

**First-party ecosystem docs MCP — prefer it over Context7 when the topic matches.** Context7 is the general default for libraries, but if the question is about a specific vendor ecosystem **and** that vendor's docs MCP is in your inventory, it is higher-signal (first-party). The prime example: **Microsoft Learn** (`microsoft_docs_search` → `microsoft_docs_fetch`; `microsoft_code_sample_search` for snippets) for **.NET / Azure / Windows / MSVC / Win32** topics — including MSVC compiler errors and Windows-SDK headers in C/C++ work. Same two-call shape (search → fetch) and the same failure-mode handling below; if it is absent or returns nothing useful, fall through to Context7 → WebSearch as normal. *(General principle — prefer the first-party MCP for its ecosystem; not a hard dependency.)*

**Context7 "doesn't work" — what to watch for**:

| Failure mode | Signal | Action |
|---|---|---|
| MCP server not connected | Context7 tools absent from your tool inventory | Go to Step 2 |
| Library not indexed | `resolve-library-id` returns `[]` or "no match" | Go to Step 2 |
| Returned wrong library | Excerpt mentions a different product than asked | Re-query with a more specific name **once**, then Step 2 |
| Returned irrelevant snippet | Snippet doesn't mention your error / option / API | Reformulate `topic` **once**, then Step 2 |
| Tool errors out | Non-zero / "error:" reply | Step 2 (don't retry the same call) |
| Returns very old version | Stated version is older than your project's | Useful as baseline; confirm with WebSearch for recent changes |

**Do not** retry the same query multiple times — Context7 is deterministic for a given input. One retry with a refined query is allowed; further iteration is the agent thrashing.

---

## Step 2: WebSearch (fallback)

**When it's the right tool**:
- Context7 unavailable or returned nothing useful
- Question is about a **recent** change (release notes, CVEs, ecosystem shifts)
- The exact error string is likely indexed by search engines (compiler errors, framework stack traces)
- The library is small / non-indexed in Context7

**Query construction rules**:

| Goal | Pattern |
|---|---|
| Exact-error lookup | `"<paste error string in quotes>"` + tool name |
| Tool config option | `<tool> <option-name> documentation` |
| Recent ecosystem | `<library> <feature> 2026` |
| Comparison | `<lib-A> vs <lib-B> <year>` |

**Source quality (descending trust)**:
1. Official docs (linked from the tool's homepage)
2. Stack Overflow answer with accepted check + multiple upvotes
3. GitHub issue with maintainer reply
4. Reputable engineering blog (Anthropic, OpenAI, Cloudflare, etc.)
5. Random blog posts — only when corroborated by 1-4

**WebSearch "doesn't work"**:

| Failure mode | Signal | Action |
|---|---|---|
| Tool not available | WebSearch absent from tool inventory | Skip to Step 3 |
| Returns paywall / login walls | Excerpts mention sign-up / 403 | Try one more query variant, then Step 3 |
| All hits are AI-generated junk | Suspiciously polished, no concrete details, no source | Step 3 — don't trust |
| No results | Empty / "no results found" | Reformulate **once**, then Step 3 |

---

## Step 3: Calibrated uncertainty (terminal fallback)

When external lookup fails, **do not guess**. State explicitly what you tried and what you'd need:

> "I looked up `<topic>` via Context7 (not loaded / returned no match for `<query>`) and WebSearch (no useful results / returned only AI-generated content). I am uncertain about `<specific question>`. To proceed I would need: `<the specific input from you, e.g. output of \`cmake --version\`, or a link to the right docs, or permission to try option X cautiously>`."

This earns user trust. Guessing destroys it. The terminal fallback exists because pretending to know is the highest-cost agent failure mode.

---

## Reporting what you looked up

When you DO find an answer, **cite the source**:

> "Per Context7 (`clang-tidy v18 docs`): `bugprone-easily-swappable-parameters` flags adjacent params of the same type that could be confused at call sites. Tuning option: `MinimumLength` (default 2)."

> "Per WebSearch (Stack Overflow answer with 47 upvotes, accepted Aug 2025): the fix is `set(CMAKE_POLICY_DEFAULT_CMP0148 NEW)` before `find_package(Python)`."

The citation makes your claim falsifiable — the user can verify. **Unsourced confidence is worse than sourced uncertainty.**

---

## When NOT to invoke docs-lookup

- The answer is in the project's own docs (use `project-indexing` to find local files first)
- The question is about the user's intent (ask them directly)
- You already have high-confidence evidence from a prior lookup this session (don't re-look-up the same thing)
- The question is project-internal architecture (read the code; don't search the web)

## Related

- `self-correction-loop` — when a tool error needs context, this skill is the lookup step
- `anti-hallucination-gates` — the citation from this skill becomes part of evidence
- `project-indexing` — for **internal** lookups (when info is in your repo, not on the web)
- All `cpp-*` skills — domain entry points; they delegate the lookup procedure here
