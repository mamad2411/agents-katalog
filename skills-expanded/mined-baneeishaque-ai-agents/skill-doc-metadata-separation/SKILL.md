---
name: skill-doc-metadata-separation
description: Composer — audit and split skill-doc metadata sections (Changelog, Traceability, ...) out of SKILL.md into CHANGELOG.md / TRACEABILITY.md companion files, library-wide or per-skill, by delegating all file mutation to the markdown-section-to-companion-doc base primitive.
category: Meta-Automation
---

# Skill Doc Metadata Separation Skill (v1) — Composer

> **Skill ID:** `skill-doc-metadata-separation`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Composer (per [`skill-factory` §2.0 Layering Decision](../../skill-factory/SKILL.md))

This is the **composer skill** of a 2-layer section-separation stack. It owns the skill-doc domain: which
sections are metadata, what the companion files are called, and the audit → plan → split → re-audit
lifecycle. All actual file mutation is delegated to the base primitive
[`markdown-section-to-companion-doc`](../markdown-section-to-companion-doc/SKILL.md).

***

## 1. When to Apply

Use when a skill's `SKILL.md` carries **information, not instructions** as inline `##` sections — most
commonly `Changelog` and `Traceability` — and those sections should live in sibling companion files
(`CHANGELOG.md`, `TRACEABILITY.md`) with the source keeping a pointer paragraph.

Apply to a **single skill** or the **whole library** in one pass:

```bash
# single skill directory
python3 .agents/skills/skill-doc-metadata-separation/scripts/separate-skill-doc-metadata.py \
  --target .agents/skills/<skill-name> --check

# whole library (recursive sweep)
python3 .agents/skills/skill-doc-metadata-separation/scripts/separate-skill-doc-metadata.py \
  --target .agents/skills --check
```

Do NOT use this skill to reorganize instruction content, merge documents, or reformat markdown — it
moves metadata sections only.

***

## 2. Workflow

1. **Audit** (`--check`): every `SKILL.md` under `--target` is probed via the base primitive for each
   configured section. Inline sections (body content beyond a pointer) are violations; absent or
   pointer-only sections are compliant. Exit 0 = clean, 1 = violations listed.
2. **Human judgement gate** (MANDATORY, not scriptable): for every violation, decide whether the section
   is *information* (changelog entries, provenance tables, session records) — split it — or
   *instructions* (operational mandates, verification steps) — leave it inline. The script never makes
   this call.
3. **Plan** (`--dry-run`): print the exact companion files, titles, and source replacement for every
   section that passed the gate. Review before mutating.
4. **Split** (`--split`): run the base primitive for each approved section, then **re-audit** and report.
   Exit 0 only when the re-audit is clean.
5. **Verify layout**: each split skill now carries `CHANGELOG.md` / `TRACEABILITY.md` beside `SKILL.md`,
   and `SKILL.md` ends with pointer sections (`## Changelog` → `See [CHANGELOG.md](CHANGELOG.md).`).

### Default Section Vocabulary

| Section | Companion file | Pointer | Nature |
| :--- | :--- | :--- | :--- |
| `Changelog` | `CHANGELOG.md` | `See [CHANGELOG.md](CHANGELOG.md).` | Information (release history) |
| `Traceability` | `TRACEABILITY.md` | `See [TRACEABILITY.md](TRACEABILITY.md).` | Information (provenance) |

`--sections` overrides the comma-separated vocabulary; `--pointer SECTION=TEXT` (repeatable) overrides
the pointer paragraph per section (the companion-name mapping `Changelog → CHANGELOG.md`,
`Traceability → TRACEABILITY.md` is canonical at the composer level and not overridable).

***

## 3. CLI Contract

Located at [`scripts/separate-skill-doc-metadata.py`](./scripts/separate-skill-doc-metadata.py).

```bash
python3 separate-skill-doc-metadata.py --target DIR (--check | --dry-run | --split)
                                       [--sections Changelog,Traceability]
                                       [--pointer SECTION=TEXT ...]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--target` | ✅ | A skill directory (contains `SKILL.md` → single-skill mode) or a library root (→ recursive sweep of every `SKILL.md` below it) |
| `--check` | ✅* | List inline sections; exit 1 if any |
| `--dry-run` | ✅* | Print the split plan; write nothing |
| `--split` | ✅* | Split all inline sections, then re-audit; exit 1 if any split fails or re-audit is dirty |
| `--sections` | ❌ | Comma-separated section vocabulary (default: `Changelog,Traceability`) |
| `--pointer` | ❌ | Override the pointer paragraph for a section, repeatable, `SECTION=TEXT` (defaults: `Changelog` → `See [CHANGELOG.md](CHANGELOG.md).`, `Traceability` → `See [TRACEABILITY.md](TRACEABILITY.md).`) |

*Exactly one mode flag is required.

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Compliant (check / dry-run) or all splits succeeded with a clean re-audit |
| 1 | Violations found (check), or base script missing / base failure / dirty re-audit (split) |
| 2 | Usage error |

### Base Resolution

The base primitive is resolved relative to this script's own location —
`Path(__file__).resolve().parent.parent.parent / "markdown-section-to-companion-doc/scripts/split-section.py"` —
so invocation works from any `cwd`. If the base is missing, the composer exits 1 with a clear error
(skill-factory §2.1 mandate).

***

## 4. Design Notes

- **Base owns bytes, composer owns domain**: every file mutation is delegated to
  `split-section.py`; this script never edits markdown directly. The composer only aggregates
  check results, maps sections to companion names, and sequences base invocations.
- **Idempotent re-runs**: the base treats already-external sections as no-ops, so re-running
  `--split` after a partial run is safe.
- **`SKILL.md`-only sweep**: companion bridges (`AGENTS.md`) are never scanned — metadata sections
  live in `SKILL.md` only.
- **Deterministic output**: `--check` violation lines are greppable; `--split` echoes every base
  invocation result before the re-audit verdict.

***

## 5. Related Skills

- [markdown-section-to-companion-doc](../markdown-section-to-companion-doc/SKILL.md) — the base
  primitive this composer delegates all file mutation to.
- [skill-factory](../../skill-factory/SKILL.md) — §2.1 directory layout (including the
  `CHANGELOG.md` / `TRACEABILITY.md` companion-file convention this skill enforces) and §2.2.1 script
  authoring mandates.
- [markdown-generation](../../markdown-generation/SKILL.md) — §1.6 blockquote metadata headers and §3
  lint-compliance for the generated companion files.

## Traceability

See [TRACEABILITY.md](TRACEABILITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
