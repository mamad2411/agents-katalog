---
name: vericontext
description: >-
  Guides AI agents to follow VeriContext citation/claim rules when writing or
  editing documents (README, AGENTS.md, plans, etc.), and to verify with
  verify workspace that every claim is still current.
  When installed as a plugin, hooks enforce (1) a reminder while writing
  documents, and (2) automatic batch verification at the end of each turn.
  When only the skill is installed standalone, neither hook exists — the
  agent must follow this document's rules on its own, and can only add the
  optional git hook (commit/push blocking) on top.
  NOT for: modifying code itself, writing tests, build work.
---

## Phase 1 — Identify What to Reference (Detect & Plan)

Before writing or editing a document, first identify the code and structure it will reference.

### 1.1 Reference Type Classification

| Reference Type | VeriContext Tool | Token Format |
|-----------|-----------------|-----------|
| Code line range | `vericontext cite` (specify line range) | `[[vctx:<path>#L<start>-L<end>@<hash8>]]` |
| File mention (role, code, existence) | `vericontext cite` (whole file: L1 to last line) | `[[vctx:<path>#L1-L<last>@<hash8>]]` |
| Directory existence | `vericontext claim --kind exists-dir` | `[​[vctx-exists-dir:<path>/]]` |
| File/directory absence confirmation | `vericontext claim --kind missing` | `[[vctx-missing:<path>]]` |

> **Mentioning a file always requires hashing it.** Whatever level you mention a file at — role, code, or existence — hash the whole file with `vericontext cite`. Do not use the `exists-file` claim.

### 1.2 Behavior Rules

1. **Referencing code lines requires citing that range.** To write "this function does X," first cite the function's line range with `vericontext cite`, then insert the token into the document.
2. **Mentioning a file always requires hashing the whole file.** Whatever level you mention a file at — describing its role, showing code, or noting its existence — cite the whole file from L1 to the last line with `vericontext cite`. **Do not use the `exists-file` claim.**
3. **Mentioning a directory requires creating a claim with `vericontext claim --kind exists-dir`.** To write "the src/ directory contains...", create an exists-dir claim.
4. **Even if you read the code with an external tool (read_file, etc.)**, call `vericontext cite` before describing it in the document, to obtain the citation token.
5. Place citation/claim tokens inside an **HTML comment (`<!-- ... -->`)**, or inline right after the related text.

## Phase 2 — Generate & Embed Citation/Claim

### 2.1 CLI Usage (common across agent environments)

**Generating a citation:**
```bash
vericontext cite --root <project-root> --path <file> --start-line <N> --end-line <M> --json
```

Example response:
```json
{ "ok": true, "citation": "[​[vctx:src/cli.ts#L30-L36@1625cd2a]]", "sha256_full": "1625cd2a..." }
```

**Generating a structure claim:**
```bash
vericontext claim --root <project-root> --kind exists-dir --path src/ --json
```

Example response:
```json
{ "ok": true, "claim": "[​[vctx-exists-dir:src/]]", "kind": "exists-dir", "normalized_path": "src/" }
```

### 2.2 Insertion Patterns

**Pattern A — inline (used in tables, code maps):**

| CLI entry point | `src/cli.ts` | <!-- [​[vctx:src/cli.ts#L30-L36@1625cd2a]] --> |

**Pattern B — end of section (used after explanatory paragraphs):**

Verification logic operates atomically per claim. If even one fails, the overall result becomes `ok: false`.
<!-- [​[vctx:src/verify/workspace.ts#L41-L86@bf6e3670]] -->

**Pattern C — structure declaration (used in project structure descriptions):**

├── src/          # production logic
<!-- [​[vctx-exists-dir:src/]] -->
├── tests/        # unit + e2e tests
<!-- [​[vctx-exists-dir:tests/]] -->
<!-- [​[vctx:package.json#L1-L<last>@<hash8>]] — hashing is required whenever a file is mentioned -->

### 2.3 Absolute Prohibitions

- Do not type citation tokens by hand. Always generate them with the tool.
- Do not guess hash values or copy previous ones.
- Do not create citations for files that do not exist.
- Do not use the `exists-file` claim when mentioning a file. Always generate a whole-file hash with `vericontext cite`.
- Do not assert "this file exists/doesn't exist" without a citation/claim.

### 2.4 Do Not Put Live Citations in Documents That Get Distributed

The rules so far are for **documents that stay inside a single project**. If a
document leaves that project and gets copied into someone else's repository, the
rule flips.

**Which documents this applies to:** skill definitions (`SKILL.md`), their
`references/`, documents bundled into distribution packages, documents that ship
inside plugin payloads, templates — in short, any document that gets installed into
another project and becomes a target of `verify` there.

**Why it flips:** a citation is a claim that "this path in this repository holds this
content." Once that document is copied into someone else's project, that path doesn't
exist there, so the claim **becomes false and fails verification**. The user sees the
failure not in a document they wrote, but **in a file we shipped them**, and reasonably
concludes the tool is broken. The tool's own distributed artifact ends up committing
the very failure the tool exists to prevent.

**How to write examples instead:** when showing token syntax as an example in a
distributed document, do not use real paths and hashes. Use one of the following:

1. **Placeholders** — write `<...>` as in `[[vctx:<path>#L<start>-L<end>@<hash8>]]`.
   The parser does not recognize this as a valid token, so it never becomes a claim
   anywhere.
2. **Zero-width space escape** — if you must show an example with a real-looking
   path, insert U+200B between the opening brackets, writing it as
   `[​[vctx:src/cli.ts#L1-L10@a1b2c3d4]]`. This has no effect on rendering, and
   the scanner does not see it as a token.

> **Test question:** if this document were copied into someone else's repository,
> would the citation written here still be true? If not, it's an example, so escape
> it.

## Phase 3 — Verify & Enforce

### 3.1 3-Layer Enforcement Structure

This table shows the full picture when installed as a **plugin**. Layers 1–2 run
via hooks the plugin registers; if only the skill is installed standalone (e.g. via
`npx skills add`), these two hooks **do not exist** — the agent must follow the
rules below on its own.

| Layer | Timing | Mechanism | Delivery | Enforcement Level |
|-------|------|----------|-----------|-----------|
| **Layer 1** | While writing documents | PreToolUse hook — reminds of citation rules on .md edit/create | Plugin only | Soft (guidance) |
| **Layer 2** | At end of turn | Stop hook auto-runs verify workspace --all | Plugin only | **Hard (gate)** |
| **Layer 3** | At commit/push | git pre-commit / pre-push hook — verifies all project .md files | Install directly per 3.6, either way (opt-in) | Hard (opt-in) |

Layers 1–2 nudge the agent toward good habits; Layer 3 blocks mechanically.
**If only the skill is installed, there are no Layers 1–2, so the agent must uphold
the Phase 1–3 rules and run the commands in 3.2 on its own.**

### 3.2 Verification Timing

Run verification at the following points:

1. **When a task is complete** — verify the changed documents once one logical unit of work is done
2. **When wrapping up a plan** — verify every claim contained in the plan document
3. **At commit/push time** — if the git hook is installed, all project .md files are verified automatically (opt-in hard gate, see 3.6). If it isn't installed, the agent must still verify manually at this point.

> **Note:** Do not verify immediately after every code edit. Batch-verify once a task is done.

**Layer 2 — how to verify when a task is complete:**

Verify an individual document:
```bash
vericontext verify workspace --root <project-root> --in-path <document.md> --json
```

Batch-verify the whole project:
```bash
vericontext verify workspace --root <project-root> --all --json
```

### 3.3 Interpreting Verification Results

**Success:**
```json
{ "ok": true, "total": 3, "ok_count": 3, "fail_count": 0, "results": [...] }
```

**Failure:**
```json
{ "ok": false, "total": N, "ok_count": M, "fail_count": N-M,
  "results": [{ "claim": "<token>", "ok": false, "reason": "hash_mismatch|missing|range_invalid" }] }
```

### 3.4 Response Procedure on Failure

1. `hash_mismatch` → re-read the file's current line range, generate a new citation with `vericontext cite`, and replace it.
2. `missing` / `not_file` / `not_dir` → check whether the file/directory was moved or deleted, then either fix the document content or remove the claim.
3. `range_invalid` → if the file has shrunk, re-cite with the correct range.
4. **After resolving every failure, run verification again.** Repeat until `ok: true`.

### 3.5 Verification Pass Criteria

- `ok: true` — safe to commit or submit the plan
- `ok: false` — **commit/submission blocked**. Every failed claim must be fixed.

> **Principle: Fail Closed.** Skipping verification, or committing while it's failing, is a violation of this skill.

### 3.6 Git Hook Installation

The git hook is **optional**. If the plugin is installed, Layer 2 (the Stop hook)
already verifies at the end of every turn, so the commit gate is an extra net meant
to catch documents a human edited by hand. **If only the skill is installed, there
are no Layers 1–2, so this git hook becomes the only automatic verification
mechanism** — installing it is recommended.

`git-hooks/` lives inside this skill directory, and its location depends on how
you installed — use whichever of the two cases below applies to you.

**If you cloned this repository (vericontext) to work on it:**

```bash
HOOKS_DIR="$(git config core.hooksPath || echo .git/hooks)"
cp skills/vericontext/git-hooks/vctx-verify-docs skills/vericontext/git-hooks/pre-commit "$HOOKS_DIR/"
chmod +x "$HOOKS_DIR/vctx-verify-docs" "$HOOKS_DIR/pre-commit"
```

**If you installed only the skill into another project via `npx skills add`:**

The skill is installed at a different path depending on the agent/scope
(`.claude/skills/vericontext/`, `~/.codex/skills/vericontext/`, etc.). So you don't
need to know the exact path, locate `git-hooks/` relative to the location of this
very `SKILL.md` file you're reading right now — `git-hooks/` always sits in the
same directory as this `SKILL.md`:

```bash
SKILL_DIR="$(cd "$(dirname "<actual path to this SKILL.md file>")" && pwd)"
HOOKS_DIR="$(git config core.hooksPath || echo .git/hooks)"
cp "$SKILL_DIR/git-hooks/vctx-verify-docs" "$SKILL_DIR/git-hooks/pre-commit" "$HOOKS_DIR/"
chmod +x "$HOOKS_DIR/vctx-verify-docs" "$HOOKS_DIR/pre-commit"
```

> Substitute `<actual path to this SKILL.md file>` with the value the agent
> reading this document already knows — the actual file path this skill was
> loaded from.

> `pre-commit` is a thin shim that calls `vctx-verify-docs` in the same directory,
> so **copy both files together**. To also use `pre-push`, add it the same way.

> In repos where `core.hooksPath` is set (husky, lefthook, etc.), files written to
> `.git/hooks` are **completely ignored** by git. Check the actual hooks directory
> first, as shown above. If a `pre-commit` already exists, don't overwrite it —
> add a call to it instead.

## Phase 4 — Per-Agent Setup Guide

### Claude Code
- Loads automatically when installed as a plugin (includes the Layer 1–2 hooks).
- When only the skill is installed (`npx skills add`), it's installed at `.claude/skills/vericontext/` and loads automatically, but there are no hooks.

### Codex (OpenAI)
- Run the CLI (`vericontext cite`, `vericontext claim`, `vericontext verify workspace`) via the Bash/shell tool.
- This skill's core rules are summarized in AGENTS.md, which Codex reads automatically.

### OpenCode
- Uses the same CLI + AGENTS.md approach as Codex.

### Antigravity / Other
- In environments where only CLI execution is available, run `vericontext verify workspace --root . --all --json` to batch-verify all documents in the project.
- Copy the core rules from Phases 1–3 into INSTRUCTIONS.md or the system prompt.

## Reference File Index

| File | Read When |
|------|-----------|
| `references/citation-format-guide.md` | When you need the exact citation/claim syntax |
| `references/verification-playbook.md` | When you need concrete steps to resolve a verification failure |
| `references/cross-agent-setup.md` | When setting up VeriContext in a new agent environment |

## Critical Rules

1. **Mentioning a file always requires generating a whole-file hash with `vericontext cite`.** Role description, code, existence — regardless of level. The `exists-file` claim is prohibited.
2. **Referencing code lines requires citing that range with `vericontext cite`.** No exceptions.
3. **Mentioning a directory requires using `vericontext claim --kind exists-dir`.**
4. **Run `vericontext verify workspace` when a task is complete.** Not after every code edit — verify once a task is done. With the plugin, the Stop hook runs it automatically; with only the skill installed, the agent must run it manually.
5. **If the git hook is installed, verify the whole directory before commit/push.** Commit/push is blocked unless the result is `ok: true`. The git hook is opt-in (see 3.6), so this gate does not apply unless it's installed.
6. **Do not hand-write citation tokens.** Always generate them with the tool.
7. **When you modify code, also update citations in documents that reference it, once the task is complete.**
8. **Do not ignore verification failures.** Fail closed — failures must always be fixed.
9. **Do not put live citations in documents that get copied to other projects.** This covers the skill, its references, documents bundled into distribution packages or plugin payloads, and templates. Write examples as placeholders (`<path>`) or with the zero-width space escape — see 2.4. Test question: if this document were sitting in someone else's repository, would this citation still be true?
