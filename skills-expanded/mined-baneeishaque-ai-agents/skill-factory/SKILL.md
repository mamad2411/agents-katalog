---
name: skill-factory
description: Industrial protocol for automated creation of "Skill-First" AI Agent skills with high fidelity.
category: Meta-Automation
---

# Skill Factory Skill (v1)

This skill automates the creation of new AI Agent Skills following the **agentskills.io** protocol and the
**Industrial Fidelity** mandates.

***

## 1. Preparation: The Fidelity Scan

The Agent MUST ensure that no operational detail is lost during the skill creation process.

1. **Source Discovery**: Identify all user-provided operational logic, dependencies, and constraints from the
   conversation history.
2. **Anti-Loss Validation**: Create a list of "Must-Include" technical specifics. **Summarization is BLOCKED** for
   these items.
3. **Preservation Check**: Ensure existing content is preserved and blended. **Destructive overwriting is FORBIDDEN**.
4. **Script Audit**: Search the target skill directory and workspace for existing automation scripts. **Consolidation
   is MANDATORY**—Utility duplication is a failure of the Industrial standard.

- **Greater-Than-Before**: The skill MUST be more detailed than the prompt that initiated it, including
  extrapolated context where necessary.

***

## 2. Skill Generation Protocol

### 2.0 Layering Decision (Base vs. Composer)

Before creating any new skill, the Agent MUST decide whether the requested capability is:

1. **Atomic** — a single, indivisible workflow with no reusable primitive. Proceed to §2.1 as one skill.
2. **Layerable** — contains a generic primitive (glob assembly, metadata extraction, path normalization, brace
   expansion, list sort+dedupe, etc.) that other domain-specific tasks could reuse. Split into:
    - A **base skill** owning ONLY the primitive, with a stdin / file / argument CLI contract and deterministic output.
      The base skill MUST be domain-agnostic.
    - One or more **composer skills** owning the domain-specific discovery, piping their output into the base skill.

The layering test: *"Could a different domain ever need the same primitive?"* If yes, layering is **MANDATORY** —
inlining the primitive into a single skill is a violation of the SSOT contract.

Reference exemplar: [vscode-search-exclude-glob](../vscode-search-exclude-glob/SKILL.md) (base) +
[vscode-search-exclude-submodules](../vscode-search-exclude-submodules/SKILL.md) (composer).

### 2.1 Directory Structure

- **Creation-time Taxonomy Placement** (mandatory first sub-step): BEFORE choosing
  the target folder, consult the domain taxonomy SSOT
  [`skill-library-domain-grouping` §1.2](../general/skill-library-domain-grouping/SKILL.md#12-sub-groups):
    1. Match the new skill's topic keyword to the taxonomy's leaf group.
    2. Place the new skill in that leaf group (e.g. a new composer over opencode
       session logs goes in the `opencode/` leaf group).
    3. Verify the parent folder's item count stays ≤10 after addition (use
       `directory-tree-audit` if uncertain); propose sub-grouping if it would
       exceed the limit.
    4. Update the domain-grouping skill's §1.1 tree count, §1.2 listing, and a
       `## Changelog` entry IN THE SAME CHANGE — a new skill directory without
       its taxonomy registration is incomplete.
- Create the target folder in `.agents/skills/<skill-name>/` (hyphens required for names).
- Initialize `SKILL.md` (active SSOT), `AGENTS.md` (companion bridge), and — when the skill's metadata
  sections are separated per the library convention — `CHANGELOG.md` (release history) and
  `TRACEABILITY.md` (provenance/session records) as sibling companion files.
- **Metadata-Separation Convention** (library standard, established 2026-08-10): `Changelog` and
  `Traceability` are **information, not instructions** — they MUST live in `CHANGELOG.md` /
  `TRACEABILITY.md` sibling files, with `SKILL.md` retaining pointer-only sections
  (`## Changelog` → `See [CHANGELOG.md](CHANGELOG.md).`). An inline `Changelog` / `Traceability`
  section with body content inside `SKILL.md` is a compliance violation. Enforce/apply via the
  [`skill-doc-metadata-separation`](../markdown/skill-doc-metadata-separation/SKILL.md) composer (which
  delegates all file mutation to the [`markdown-section-to-companion-doc`](../markdown/markdown-section-to-companion-doc/SKILL.md)
  base primitive) — do NOT hand-edit the split.
- For **composer skills**: the composer's script MUST resolve the base script via a relative path anchored to its own
  location (`SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"` then `BASE="$SCRIPT_DIR/../../<base-skill>/scripts/..."`),
  so invocation works regardless of the caller's `cwd`. The composer MUST verify the base script exists and exit
  non-zero with a clear error if it is missing.
- **`scripts/` SANITY CHECK**: Only create `scripts/` when the skill ships executable scripts. A skill with no
  scripts (pure documentation + conventions) MUST NOT have a `scripts/` directory.

### 2.2 SKILL.md Composition

The `SKILL.md` MUST include:

1. **YAML Frontmatter**: name, description, category. Skill names MUST use lowercase letters, numbers, and hyphens.
   The frontmatter block (`---` ... `---`) MUST be the FIRST content in the file (line 1 column 1, no BOM, no
   preceding blank lines, **no preceding HTML comments**); any preceding character makes the agentskills.io lint
   validator emit `Skill must provide a name` even when the YAML is otherwise valid. When a workspace tradition
   uses a namespaced Skill ID containing slashes or underscores (e.g., `dgs_ice/foo_bar`), that form is FORBIDDEN
   in `name:` (validator enforces `^[a-z0-9-]+$`) — put the hyphenated single-segment form in `name:` and keep
   the namespaced form in the body under `> **Skill ID:** ...` where it is not lint-validated.
   The `> **Label:**` metadata header blockquote below the title MUST follow the §1.6 blockquote convention of
   **[`markdown-generation`](../markdown-generation/SKILL.md#16-blockquote-metadata-headers)** — every line of a
   2+-line run ends with `<br>` except the last; blank `>` separators are FORBIDDEN. The library-wide composer
   `scripts/audit-normalize-skill-headers.py` (this skill) enforces the rule via the base primitive.
   The `name:` MUST also satisfy the **Skill-Name Precision Mandate** ([`ai-rule-standardization-rules.md` §Skill Naming](../../../ai-agent-rules/ai-rule-standardization-rules.md)) — every distinguishing constraint of the skill's scope (filetype, transport, mode, exclusion) MUST appear in the name; generic names that omit a qualifying constraint silently collide with future variants and mislead callers. A longer precise name is always preferable to a shorter ambiguous one.
2. **Environment & Dependencies**: Mandated verification logic (`which`, version checks).
3. **Operational Logic**: The EXACT steps provided by the user (**Zero Omission**).
4. **SSOT Compliance**: The skill MUST NOT duplicate technical standards
   defined in the central rule repository. Instead, it MUST link to the
   authoritative rule files using relative links (e.g., to the atomic
   commit rules or commit message rules).
5. **Traceability Section**: Links to permanent conversation logs. All such logs MUST be sanitised through the
   **[Redaction & Portability Skill](../redaction-portability/SKILL.md)** before being committed — see §3 of this
   document for the mandatory audit checklist.
   AI-agent session identifiers are machine-local and MUST NOT appear in committed artifacts — reference the
   session by date and topic. References to local-only planning documents (gitignored `docs/`) MUST NOT
   appear in committed artifacts either — replace them with self-contained explanations or links to
   public repository content.
6. **Separate-File Convention (MANDATORY)**: the `Traceability` section — like `Changelog` — is information,
   not instructions, and MUST be authored directly in a sibling `TRACEABILITY.md` (respectively `CHANGELOG.md`)
   companion file, with `SKILL.md` carrying only the pointer section (`## Traceability` → `See
   [TRACEABILITY.md](TRACEABILITY.md).`) per §2.1. Do NOT draft an inline `## Traceability` / `## Changelog`
   body inside `SKILL.md`; if an existing skill has one, split it with the
   [`skill-doc-metadata-separation`](../markdown/skill-doc-metadata-separation/SKILL.md) composer.

**No-Parallel-Rule-File Mandate**: When the Factory produces a new skill, it MUST NOT also produce a parallel
rule file (`ai-agent-rules/<topic>-rules.md`) covering the same procedure. Rule / instruction files are
vendor-locked (`.cursor/rules/*.mdc`, `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`,
`.windsurfrules`, etc.); the `agentskills.io` standard is the open, multi-vendor-portable alternative.
Authoring a sibling rule re-introduces the vendor lock the skill was created to escape and splits the SSOT.
An `AGENTS.md` Permanent Operating Reminder (one-line bullet pointing at the skill) is permitted and
encouraged; a full parallel rule file is FORBIDDEN. Authoritative rationale:
[`ai-rule-standardization-rules.md` §2 Skill-First Architecture](../../../ai-agent-rules/ai-rule-standardization-rules.md)
and [`rule-to-skill-industrialization` §0](../rule-to-skill-industrialization/SKILL.md).

### 2.2.1 Script Authoring Mandates

**No-Embedded-Script Mandate**: Script source code MUST NOT be embedded inside `SKILL.md`, `AGENTS.md`, or any other
markdown document. Markdown MUST link to the separate file under `scripts/` via a **relative** path
(e.g., `[scripts/foo.ps1](scripts/foo.ps1)`) and MAY include a short fenced invocation example (one-liner).
Embedding the full script body is FORBIDDEN — it breaks syntax highlighting, debugging, standalone execution, and
the SSOT contract. See [AI Rule Standardization Rules — No-Embedded-Script Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md).

**Tier Decomposition Mandate**: Before drafting the `SKILL.md` body, walk every step of the user-provided procedure
and classify each as Tier A (deterministic) or Tier C (judgement) per
[`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md). Every Tier-A step MUST
be extracted into a script under `scripts/` and invoked from prose via a one-liner. Prose MUST NOT carry multi-line
bash recipes, Python heredocs, regex-laden `sed`/`awk` chains, or step-by-step file-mutation walkthroughs — those
belong in a script. A skill whose prose still embeds deterministic mechanics has skipped the decomposition step and
fails the Factory's industrial standard.

When the skill ships executable scripts under `scripts/`, every script MUST obey the **Universal Script Mandates** in §2.2.1.1 (all scripts, all tiers) and, when Tier 2 (PowerShell) is selected, additionally obey the **Tier-2 (PowerShell) Craftsmanship Mandates** in §2.2.1.2.

#### 2.2.1.1 Universal Script Mandates

Apply to every script regardless of language tier.

1. **Language Selection (SSOT-Delegated)**: The script's language MUST be chosen per the four-tier framework in
   **[Scripting Language Selection Rules](../../../ai-agent-rules/scripting-language-selection-rules.md)** — that
   document is the SSOT. Do NOT inline the framework here. In one line: **Tier 1 (Python 3.12+) is the default for
   new scripts**; Tier 2 (PowerShell 7+ / `pwsh`) is reserved for scripts whose body IS shell glue; Tier 3 (C / Go /
   Rust / Zig) is reserved for measured CPU-bound bottlenecks; Tier 4 (Java / C# / Node / PHP) is reserved for
   ecosystem-mandated cases. The **older "PowerShell-First" default is RETIRED** for new scripts (see Scripting
   Language Selection Rules §intro). Selection MUST be made BEFORE drafting the script and MUST be documented in
   the script's header (`.NOTES` block for `.ps1`, module docstring for `.py`) with a one-line citation of the
   §3–§5 tier rule that applies. **Tier-1 (Python) craftsmanship details** (byte-safe I/O, `argparse`, `ruff`,
   `pytest`, PEP 723 / `uv`, mise-equivalence) are SSOT-owned by Scripting Language Selection Rules §2.3.
   **Tier-2 (PowerShell) craftsmanship details** (comment-based help, `pwsh-preview` → `pwsh` fallback,
   `Common-Utils.ps1` dot-source, `Write-Message` guard, strict-mode hygiene) — §2.2.1.2 below — remain
   mandatory whenever Tier 2 is selected; they DO NOT apply to Tier-1 (Python) scripts.
2. **Bash Extension Mandate**: When Bash is selected (a Tier-2 borderline case requiring documented justification —
   usually because the host lacks `pwsh`), the file MUST use the `.bash` extension — never `.sh` — per
   [Bash Scripting Rules §Naming](../../../ai-agent-rules/bash-scripting-rules.md) and the
   [GitHub Actions Workflow Rules](../../../ai-agent-rules/github-actions-workflow-rules.md) standalone-script
   mandate.
3. **Tier-Violation Remediation**: When a Factory audit on an EXISTING skill discovers a script that picked the
   wrong language tier per
   [`scripting-language-selection-rules`](../../../ai-agent-rules/scripting-language-selection-rules.md)
   (typically a `.bash` / `.sh` wrapping a `python3 - <<PY` heredoc, or a shell script doing JSON / regex work),
   DELEGATE the port to [`script-language-tier-port`](../script-language-tier-port/SKILL.md) as its own atomic
   refactor commit — do NOT inline the port mechanics here.
4. **Plan-Time Tier Declaration**: Any planning artifact (per
   [`ai-agent-planning-rules`](../../../ai-agent-rules/ai-agent-planning-rules.md))
   that proposes NEW scripts MUST surface, in the plan body, a per-script
   table listing (a) the Tier-1 (Python) evaluation, (b) the chosen tier,
   (c) the `scripting-language-selection-rules` §3–§5 citation, and (d) —
   if the chosen tier is NOT Tier-1 — the explicit deviation reason. This
   surfaces wrong-tier picks at plan-review time, where they cost a plan
   revision, instead of post-implementation, where they cost a
   [`script-language-tier-port`](../script-language-tier-port/SKILL.md)
   refactor commit.
5. **Recursive Submodule Bootstrap**: Any documentation that instructs the user to clone or initialize the
   `powershell-scripts` submodule (or any other submodule) MUST use the recursive form
   (`git submodule update --init --recursive <path>` or `git clone --recurse-submodules <url>`).
6. **Template Extraction Mandate** (companion to No-Embedded-Script Mandate): When a script writes
   file content (YAML, markdown, .gitignore, config stanzas, etc.), that content MUST be kept in a
   separate `.template` file under `scripts/` and read at runtime via a path anchored on the script's
   own location (`Path(__file__).parent / "<name>.template"` in Python;
   `Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "<name>.template"` in PowerShell).
   Embedding file-content strings in scripts is FORBIDDEN because it: (a) breaks syntax highlighting
   and linting of the template format, (b) duplicates SSOT — the truth lives both in the string
   literal and the generated file, (c) prevents editors from applying format-specific tooling,
   (d) makes content changes require touching the script file.  For automated remediation of existing
   scripts that violate this mandate, use
   [`script-template-extraction`](../script-template-extraction/SKILL.md).
7. **Documentation Invocation Convention** — Skill docs MUST use simplified
   invocation forms (`python3`, `node`, `ruby`, `php`, `pwsh`). Never embed
   fragile path-resolution commands like
   `PY=~/.local/share/mise/installs/python/$(ls … | sort … | tail -1)/bin/python`
   in documentation code blocks. The companion runtime resolution logic is
   documented in
   [`mise-tool-management §3.3`](../mise-tool-management/SKILL.md#33-runtime-tool-resolution).
   Use `scripts/verify-doc-invocations.py` to audit for violations.

#### 2.2.1.2 Tier-2 (PowerShell) Craftsmanship Mandates

Apply **only when the script's selected tier is Tier 2 (PowerShell)**. Tier-1 (Python) scripts are exempt — Python craftsmanship is SSOT-owned by [Scripting Language Selection Rules §2.3](../../../ai-agent-rules/scripting-language-selection-rules.md).

1. **Documentation Headers**: Comment-based help with `.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`, `.NOTES`
   sections — see the [Script Management Rules](../../../ai-agent-rules/script-management-rules.md).
2. **Execution**: Documented invocations MUST use `pwsh-preview` (preferred) with `pwsh` as fallback.
3. **Common-Utils Dot-Source**: Scripts MUST dot-source `Common-Utils.ps1` from the
   [`powershell-scripts`](../../../ai-agent-rules/powershell-scripts/) submodule of `ai-agent-rules` for shared
   helpers (`Write-Message`, etc.) unless an explicit exemption is justified in the script's `.NOTES` block.
4. **Portable Anchored Paths**: All sibling-artifact lookups (the dot-source above, base-skill scripts under the
   Layered Composition Mandate, config files) MUST be resolved through paths anchored on the script's own location
   via `Split-Path -Parent $MyInvocation.MyCommand.Path` + `Join-Path` — NEVER `$PWD`-relative or hard-coded.
5. **Write-Message Safeguard**: Every `Write-Message` call MUST be guarded with
   `if (-not [string]::IsNullOrWhiteSpace($Message)) { ... }`.
6. **Strict Mode Hygiene**: Scripts SHOULD declare `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`.
   When reading `$LASTEXITCODE` after invoking another script, guard with
   `Test-Path Variable:LASTEXITCODE` to avoid strict-mode failures on first invocation.

### 2.2.2 Script Delivery & Preservation Mandates

Scripts are **first-class deliverables** of a skill — not disposable session artifacts:

1. **Ship It (Delivery Mandate)**: Any automation script developed during a skill session MUST be committed inside
   the skill's `scripts/` directory as part of the skill's canonical form. "The script helped during the session"
   is sufficient and mandatory justification to ship it permanently. Leaving scripts uncommitted is a failure of
   the Industrial standard.
2. **Never Silent Drop (Preservation Mandate)**: Existing scripts in a skill's `scripts/` directory MUST NOT be
   deleted, emptied, or replaced without an explicit user instruction. During skill refactors (e.g., extracting a
   base layer), the original script MUST be migrated or superseded explicitly — not silently removed.
3. **Supersession Documentation**: If a script is superseded by a higher-layer composer (3-layer stack refactor),
   the SKILL.md MUST document: (a) which script replaces it, (b) the new invocation path, and (c) the rationale —
   so no operational knowledge is lost even when the old file is intentionally removed.
4. **Commit Inclusion**: The skill's scripts MUST appear in the same commit as the skill's `SKILL.md` — never
   deferred to a follow-up commit. An uncommitted script that exists only in the working tree is NOT part of the
   skill.

### 2.3 AGENTS.md (Companion Bridge) Composition

Every skill folder MUST contain an `AGENTS.md` file alongside `SKILL.md`. The file is a **passive bridge** that exposes the skill to *non-skill-aware* agent runtimes — clients that auto-load `AGENTS.md` by filename convention (e.g., Codex CLI, some Cursor profiles, some Continue.dev configurations) but do not parse `agentskills.io` YAML frontmatter or the `.agents/skills/<name>/SKILL.md` directory contract. The bridge ensures those agents discover the skill exists and know to read `SKILL.md` for the operational details, instead of silently missing the skill.

#### 2.3.1 Disambiguation — Per-Skill Bridge vs. Root-Level Architecture

Three root-level files share the `AGENTS` prefix:

| File | Role | Maintained by |
| --- | --- | --- |
| `<repo-root>/AGENTS.md` | Permanent Operating Reminders (all AI tools) | Manual |
| `<repo-root>/AGENTS-legacy.md` | Skills table for legacy / non-skill-aware runtimes | §2.4 Registration (row inserted via `agents-md-stage-row.py --target AGENTS-legacy.md`) |
| `<repo-root>/AGENTS-github-copilot.md` | GitHub Copilot-specific instructions (delta only) | Manual |
| **Per-skill bridge** `.agents/skills/<skill>/AGENTS.md` | Companion bridge for one skill | THIS subsection (§2.3) |

They are NOT the same artifact and MUST NOT be conflated. The per-skill bridge does not list other skills; the root-level files each serve their distinct roles. A failure to distinguish them has been observed where an author put per-skill bridge content into the root registry (or vice versa).

#### 2.3.2 Required Sections (Template)

The per-skill `AGENTS.md` MUST contain the following sections in this order:

1. **`# <Skill Display Name> — Companion Bridge`** (level-1 heading; the literal suffix `— Companion Bridge` lets reviewers grep for bridges across the tree).
2. **`## Purpose`** (1–3 sentences). State that this file is the bridge for non-skill-aware runtimes and that the operational SSOT lives in [`SKILL.md`](SKILL.md).
3. **`## When This Skill Applies`** (1 short paragraph or 3–5 bullets). Plain-language trigger conditions, paraphrased from `SKILL.md`'s `## Description` and `## When to Apply` sections — NOT copy-pasted.
4. **`## Operational Procedure`** (1 sentence + the link). A single sentence directing the agent to `SKILL.md` for the procedure: *"Read [`SKILL.md`](SKILL.md) for the full operational procedure, including all mandates, scripts, and verification steps. Do NOT execute any step without first loading `SKILL.md` — this bridge is intentionally non-actionable."*
5. **`## Cross-References`** (optional bullet list). Relative links to closely-related skills and rule files. Use §5.6 (Cross-Reference Link Discipline) — proper relative markdown links, not bare code spans.

#### 2.3.3 Frontmatter Prohibition

The per-skill `AGENTS.md` MUST NOT carry YAML frontmatter (no leading triple-dash block). Frontmatter is the discriminator that distinguishes `SKILL.md` (skill-aware runtime metadata) from the bridge file. Adding frontmatter to `AGENTS.md` causes some runtimes to mis-classify it as a second skill registration and emit duplicate-name lint errors.

#### 2.3.4 Forbidden Content

The per-skill `AGENTS.md` MUST NOT contain:

1. **Embedded scripts** (covered by §2.2.1 No-Embedded-Script Mandate — applies to ALL markdown in the skill, including the bridge).
2. **Duplicated rule content** from `SKILL.md` or from `ai-agent-rules/*.md`. The bridge paraphrases trigger conditions; operational mandates are not restated.
3. **Step-by-step procedures**. Any reader looking for the procedure MUST be sent to `SKILL.md`. The bridge is intentionally non-actionable so divergence between the two files is impossible.
4. **Long verbatim quotes** from `SKILL.md`. If the bridge starts copying paragraphs from `SKILL.md`, the bridge has overstepped its role and will drift on the next `SKILL.md` edit.

#### 2.3.5 Size Guidance

A correctly-scoped per-skill `AGENTS.md` is typically **40–120 lines** (Purpose + When + Operational pointer + Cross-References). Sub-40 lines suggests missing sections (e.g., no When-This-Applies); over-120 lines suggests content duplication that should be deleted and replaced with a pointer to `SKILL.md`. The size is a smell test, not a hard cap.

#### 2.3.6 Audience Clarification

The bridge serves **two audiences**:

1. **Non-skill-aware agent runtimes** that auto-load `AGENTS.md` by filename convention. The bridge ensures these runtimes discover the skill and know to load `SKILL.md` for operational details.
2. **Human reviewers** browsing the skill folder who haven't yet opened `SKILL.md`. The bridge gives them a one-minute orientation before they commit to reading the full SSOT.

It is NOT for skill-aware runtimes — those load `SKILL.md` directly via the `agentskills.io` discovery contract and ignore the bridge.

#### 2.3.7 Audit Step

A bridge audit row is added to §3 Post-Drafting Checklist verifying that `<skill>/AGENTS.md` exists, has no frontmatter, contains the five required sections from §2.3.2, and is within the 40–120 line size guidance from §2.3.5. A skill with no bridge file is INCOMPLETE and MUST NOT be marked done.

### 2.4 Registration

- Update the `AGENTS-legacy.md` skills table to register the new skill with its absolute path and description.
    Use the shared registration helper instead of hand-editing the table:

    ```bash
    python3 .agents/skills/git-hunk-staging-primitives/scripts/agents-md-stage-row.py \
        --target AGENTS-legacy.md \
        --mode worktree \
        --row "| Skill Name | [\`.agents/skills/<skill-name>/SKILL.md\`](.agents/skills/<skill-name>/SKILL.md) | One-line description |"
    ```

    `--mode worktree` reads the working-tree `AGENTS-legacy.md`, inserts the row at the alphabetically correct position,
    and writes the result back to the working tree for normal `git add` review. The default `--mode staged`
    is reserved for the Atomic Commit Construction §2f Interleaving Mandate when `AGENTS-legacy.md` already carries
    unrelated pending hunks.
- **Alphabetical Order Mandate**: The `AGENTS-legacy.md` skills table MUST remain sorted alphabetically (case-insensitive)
  by the **Skill** column. New entries MUST be inserted at the correct sorted position \u2014 NEVER appended to the end.
  After insertion, the Agent MUST visually verify that the row above and below the new entry maintain the sort order.
- For layered pairs: register **both** the base and the composer in the same change at their respective sorted
  positions, with the composer's row explicitly noting *"Composer — feeds X into the base Y skill"* so the dependency
  is visible at the index level.
- Registration is the LAST registration step: the §2.1 taxonomy-placement update (domain-grouping tree + changelog)
  MUST be completed before the `AGENTS-legacy.md` row is added, so the index never advertises a skill the taxonomy
  does not yet register.

***

## 3. Post-Drafting Checklist

Every skill generated via the Factory MUST automatically undergo the final verification:

- **Portability, Redaction & PII Audit (MANDATORY — SSOT delegation)**: Every file produced by the Factory MUST be
  put through the full **[Redaction & Portability Skill](../redaction-portability/SKILL.md)** protocol before the
  skill is considered complete. The Factory MUST NOT inline its own redaction rules — the redaction skill is the SSOT.
  Specifically, the Factory MUST execute, in order:
    1. **Tier Classification** (Redaction §1): Walk every string in every generated artifact (`SKILL.md`,
       `AGENTS.md`, every `docs/conversations/*.md`, every `docs/cases/*.md`, every script header) and classify
       each candidate string as Tier A (identity/credentials), Tier B (machine/org topology), or Tier C
       (public/universal).
    2. **Canonical Placeholder Substitution** (Redaction §2): Replace every Tier-A and Tier-B match with the
       canonical placeholder vocabulary (`<workspace-root>`, `<user-home>`, `<toolbase>`, `<author>`, `<user>`,
       `<corp-proxy-host>`, `<corp-domain>`, `<internal-vcs>`, `<ticket-system>`, `<customer>`,
       `<product-codename>`, etc.). Ad-hoc placeholder invention is FORBIDDEN — extend Redaction §2 first.
    3. **Path Handling** (Redaction §3): All absolute Windows / POSIX paths are converted to workspace-relative,
       user-home-relative (`~`), or placeholder form. Angle-bracket placeholders in `[text](target)` link targets
       are converted to inline-code symbolic references per Redaction §3.3 to avoid broken navigation.
    4. **Identity Handling** (Redaction §4): Author trailers, reviewer names, OS usernames, and email addresses are
       redacted. Commit SHAs are preserved.
    5. **Network & Org Handling** (Redaction §5): Internal proxy hosts, internal domains, internal repository URLs,
       ticket IDs, customer names, and product codenames are redacted; the `nonProxyHosts` and analogous wildcards
       use `<corp-domain>` / `<corp-cloud-domain>` placeholders.
    6. **File Naming Hygiene** (Redaction §6): Conversation and case-study filenames MUST encode topics, never
       organization or identity strings.
    7. **Verification Scan** (Redaction §8 Step 4): Re-run the regex inventory scans for absolute paths, emails,
       IPv4, and internal hostnames. The terminal output MUST be empty (or contain only Tier-C universally-true
       matches) before the audit passes.
    8. **Encoding Sanity Check** (Redaction §8 Step 5): Scan for mojibake markers (`Ã`, `â€`, `Â`, `ï¿½`) that
       redaction edits frequently introduce, and fix them before considering the audit complete.
    9. **Directory Depth Audit**: Verify the correct directory depth (e.g., `../../../` from a 3-level deep skill).
   10. **Repository Independence Audit** (Redaction §1.0 + §1.4): When the new skill mentions ANY other repository
       (whether by Markdown link or by prose), run the Pre-Commit Checklist from Redaction §1.4 and apply the
       Standalone-Clone Test from §1.0 — "if I clone ONLY the enclosing repo into a fresh empty directory, does
       every relative link resolve and does every prose reference still make sense?" Reject any relative-path link
       whose target escapes the enclosing repo (count `../` segments) regardless of how it resolves on the author's
       disk. Multi-root VS Code layouts are inadmissible defences. The Worked Example in Redaction §1.5
       (a public-skill ↔ org-private-skill pair) is the reference pattern.
- **Prohibited Behavior**: The Factory MUST NOT publish a skill that has not passed the Redaction & Portability audit.
  Half-redacted strings (e.g., `<corp-proxy-host>.<real-corp>.com`) and over-redacted public identifiers
  (e.g., redacting `Apache Commons`, `Eclipse`, `Maven Central`) are both audit failures per Redaction §10.
- **Contextual Hosting**: Documentation (logs, artifacts) MUST reside in the component's `docs/` folder.
- **Fidelity Check**: Verify that no technical details from the source conversation were summarized or lost.
- **Markdown Audit**: Run the
  **[Markdown Lint Workflow](../general/markdown-lint-workflow/SKILL.md)**
  3-step pipeline (Step 1: `markdownlint-cli2 --fix`, Step 2: companion scripts
  in execution order, Step 3: manual fix + audit) to ensure 100% lint compliance.
  The agent MUST re-read every generated/edited markdown file and fix any stray
  tool-output tags (`</content>`, `<parameter ...>`), duplicated lines, broken or
  multi-line links, unclosed fences, and embedded absolute paths BEFORE presenting
  the artifact.
  Linting MUST be performed by invoking the **`markdownlint-cli2`** binary directly
  (e.g., `markdownlint-cli2 --fix <path>` then `markdownlint-cli2 <path>`); using `npx markdownlint-cli2` is
  **FORBIDDEN** per
  **[Markdown Generation Rules §5](../../../ai-agent-rules/markdown-generation-rules.md#5-validation-rules-markdownlint-cli2)**.
  Recommended fix-script execution order is documented in
  **[Markdown Lint Workflow §2.1](../general/markdown-lint-workflow/SKILL.md#21-execution-order)**.
- **Bridge Audit**: Confirm `<skill-dir>/AGENTS.md` exists, carries NO YAML frontmatter (no leading `---` block), contains the five required sections from §2.3.2 (`# <Skill> — Companion Bridge` / `## Purpose` / `## When This Skill Applies` / `## Operational Procedure` / `## Cross-References`), and is within the 40–120 line size guidance from §2.3.5. A skill with no bridge file is INCOMPLETE.
- **Metadata-Separation Audit**: Run the
  [`skill-doc-metadata-separation`](../markdown/skill-doc-metadata-separation/SKILL.md)
  composer in `--check` mode over the authored skill (and, for library-wide changes, over the whole
  library) and confirm it exits 0 — no inline `Changelog` / `Traceability` sections remain in any
  `SKILL.md`; every skill carries `CHANGELOG.md` / `TRACEABILITY.md` beside `SKILL.md` with pointer-only
  sections in the SSOT.

  ```bash
  python3 .agents/skills/markdown/skill-doc-metadata-separation/scripts/separate-skill-doc-metadata.py \
    --target .agents/skills/<skill-name> --check
  ```

- **Header Blockquote Audit** (mandatory for every authored/edited skill doc): Run the
  composer `scripts/audit-normalize-skill-headers.py` and confirm it exits 0 —
  every `> **Label:**` header run in the library must render line-by-line
  (`<br>` on all but the last line, §2.2). The composer shells out to the base
  primitive `markdown-generation/scripts/join-blockquote-header.py`; do NOT
  reimplement the transform inline.

  ```bash
  python3 .agents/skills/skill-factory/scripts/audit-normalize-skill-headers.py --check
  ```

- **Registration Audit**: Confirm the new skill row was inserted into the `AGENTS-legacy.md` skills table at the correct
  alphabetical (case-insensitive) position by the **Skill** column, NOT appended to the end. Spot-check the rows
  immediately above and below to verify the sort order holds.
- **Organization Audit**: Confirm the new skill's placement obeys the domain taxonomy in
  [`skill-library-domain-grouping` §1](../general/skill-library-domain-grouping/SKILL.md#1-domain-taxonomy).
  The parent folder MUST have ≤10 items; if the addition would exceed the threshold, the agent
  MUST propose a sub-grouping before adding.
- **Invocation Audit**: Run `scripts/verify-doc-invocations.py` to confirm no fragile invocation
  patterns are present in any `**/SKILL.md` file (mandate #7). The script MUST exit 0 before
  the skill is considered complete.
- **Composition Audit** (when layering applies):
    1. **No Inlining**: Confirm the composer script does NOT reimplement the base primitive — it MUST shell out to
       the base script.
    2. **End-to-End Pipeline Validation**: Execute the composer against a real input and confirm the output matches
       the base skill's expected format (deterministic, sorted, deduped, correctly framed).
    3. **Bidirectional Discoverability**: Confirm the base skill lists the new composer in its
       `## Composition by Higher-Level Skills` table, and the composer links back to the base in its
       `## Composition Rationale` and `## Related Skills` sections.
    4. **Cross-Reference Integrity**: Run the
       [`skill-cross-reference-audit`](../general/skill-cross-reference-audit/SKILL.md)
       base script to detect: (a) skill names duplicated in both Composition and
       Related Skills sections, (b) missing AGENTS.md, (c) missing YAML frontmatter,
       (d) empty Related Skills sections, (e) missing Related Skills in skills that
       have Composition sections. Resolve all reported issues before declaring the
       skill complete.

       ```bash
       python3 .agents/skills/general/skill-cross-reference-audit/scripts/audit-cross-refs.py
       ```

- **Script Authoring Audit** (when scripts are shipped):
    1. **Cross-Version Smoke Test**: Execute the script with `pwsh-preview` (and, where feasible, `pwsh`) on a real
       input and confirm exit code 0 on the success path and exit code 1 with a `Write-Message`-rendered diagnostic on
       the failure path.
    2. **Pipeline Cleanliness**: Capture the script's stdout into a variable (`$out = & ./script.ps1 ...`) and confirm
       it contains exactly the expected payload — no diagnostic noise leaking onto the success stream.
    3. **Common-Utils Dependency**: Confirm the documented `git submodule update --init --recursive` snippet for the
       `powershell-scripts` submodule appears in the skill's Environment & Dependencies section.
    4. **Path Portability**: Run the script from at least two different working directories (e.g., the repo root and
       `/tmp`) to prove the `$MyInvocation`-anchored relative paths still resolve.

## 4. Bash-Authoring Hygiene During Skill Creation

Skill authoring itself frequently mutates many files via bash. The same patterns that freeze the VS Code renderer during normal agent work also freeze it during skill-authoring sessions. Before any bash invocation a Factory author MUST satisfy:

1. **One command per call.** No `;` / `&&` chaining unless required by a pipe.
2. **One path argument per call.** Iterate at the agent level, not in shell.
3. **No bash `grep -r` / `find` for searches.** Use the in-process `grep` / `glob` tools with `head_limit`.
4. **Heredoc body ≤ ~50 lines.** Split into multiple `cat >> file <<EOF` appends; for surgical insertions use Python `pathlib.Path.read_text() / write_text()` instead of `sed -i`.
5. **Bound every call's output.** Redirect unknowns to `scratch/` per [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md).

The ten recurring freeze patterns, the eleven-item per-call self-audit checklist, and the post-freeze recovery protocol are owned by [`ide-renderer-freeze-prevention`](../ide-renderer-freeze-prevention/SKILL.md) — Factory authors enforce its §5 checklist on every bash call made during skill creation but do not re-document the patterns locally (SSOT).

## 5. Skill-Doc Editing Discipline

Eight independent invariants govern in-place edits to existing skill docs (`SKILL.md`, `AGENTS.md`) so that one author's mutation does not leave broken references, duplicated sections, misplaced subsections, off-topic bloat, broken cross-reference links, too-narrow top-level headings, formatting drift, or numbering gaps for the next author to clean up.

### 5.1 Post-Rename Cross-Reference Sweep

Whenever a skill-authoring task renames anything that other artifacts may reference:

- A heading anchor or section number (e.g., `§3c` → `§3b`)
- A skill folder or skill identifier (e.g., `git-submodule-selective-init` → `git-submodule-selective-init-no-lfs`)
- A file path, symbol name, or canonical placeholder

…the renamer MUST, **before reporting the task done**, sweep the entire affected tree for the OLD form and update every inbound hit in the same operation. The mechanics are Tier-A (per [`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md)) and are owned by the dedicated script — INVOKE the script, do NOT re-derive the sweep ad-hoc:

```bash
# 1. Dry-run preview (exit 1 if hits found, 0 if clean)
.agents/skills/skill-factory/scripts/post-rename-sweep.py --old "<OLD>" --new "<NEW>"

# 2. Review the per-file hit listing; if all hits are legitimate inbound refs:
.agents/skills/skill-factory/scripts/post-rename-sweep.py --old "<OLD>" --new "<NEW>" --apply

# 3. Verify zero residual hits (exit 0 == clean):
.agents/skills/skill-factory/scripts/post-rename-sweep.py --old "<OLD>" --new "<NEW>"
```

The script auto-discovers repo root, applies safe default scopes (skill `.md`, skill `scripts/`, `ai-agent-rules/`, root `AGENTS.md`, `memories/repo/`), uses LITERAL string replacement only (no regex — per §5.1 a rename is always a literal-form change), and skips `.git/`, `node_modules/`, `__pycache__/`, `.venv/` unconditionally. Custom scope can be passed via repeatable `--scope <GLOB>`. The script is the SSOT for the sweep mechanics — do NOT fall back to bash `grep -r` (violates [`ide-renderer-freeze-prevention`](../ide-renderer-freeze-prevention/SKILL.md) §3 Pattern 2) or to inline Python re-implementation (violates [`script-over-instruction-decomposition`](../script-over-instruction-decomposition/SKILL.md) Consumer Discipline).

A rename is a refactor; every inbound reference is part of the refactor's scope. Stopping at the renamed file is an incomplete refactor and the user has to catch it.

**Insertion-induced renumbering counts.** "Rename" here includes any change that shifts the section's identifier, even when the heading TEXT is untouched. Specifically:

1. **Insertion before**: adding a new `## N.` before an existing section bumps that section (and all successors) to `## (N+1).`. The displaced section has been renumbered — every inbound `§N` reference (whether self-referential within the same skill or cross-skill) becomes dangling and MUST be updated in the same edit.
2. **Deletion before**: removing a `## N.` shifts successors down by one. Same sweep obligation.
3. **Promotion / demotion**: moving `### N.M` up to `## (N+1).` or vice versa changes the citation form (`§N.M` ↔ `§(N+1)`). Same sweep obligation.

These no-text-change renumbers are the most-missed class because the diff looks small ("just inserted a new section, nothing else changed"). The cross-reference impact is identical to a text-rename. Apply §5.4 verification (`grep -n '^## \|^### ' <file>`) AND the inbound-sweep above on every numbered insertion / deletion / promotion.

**Self-referential references count too.** A `§N` citation inside the same skill that points to a now-renumbered sibling section is just as dangling as a cross-skill `§N`. Include the same file in the sweep target list — do not assume "the heading's just two screens above, I'd have noticed."

**Historical example**: in [`git-submodule-dead-upstream-audit`](../git-submodule-dead-upstream-audit/SKILL.md), an inbound reference *"The `curl` invocations in §2 follow…"* in §1 became dangling because the curl-introducing section is actually §3 (Upstream Reachability Probe) and §4 (Fork / Mirror Discovery) — not §2 (Pre-Audit Discovery, which uses only `git`). Whether the slip originated from an early-draft renumber or a typo, §5.4's verification step (numbering audit) combined with this §5.1 inbound-sweep would have caught it before the doc shipped.

### 5.2 Cross-Reference Append Discipline

When adding an inbound back-link section (e.g., `## Composition by Higher-Level Skills`) to a target skill:

1. First check whether the target already has that section (`grep -n "<section heading>" target/SKILL.md`).
2. If it does → append a **row to the existing table / bullet to the existing list**.
3. If it does NOT → create the section.

Never create a second heading of the same name. The skill-factory's "one section per topic" invariant must be preserved.

(Persisted as `permanent_discipline.post-rename-cross-reference-sweep`.)

### 5.2.1 Composition-Table Membership & Description Discipline

The `## Composition by Higher-Level Skills` table on a base skill is NOT a catalog of "skills that mention this one" — it is the **inbound composition graph**. Three failure modes have been observed when authors append rows carelessly:

1. **Unrelated skills listed**: a skill that neither composes nor consumes the base is added because its topic sounded adjacent. PROHIBITED — the table loses signal and downstream readers compose the wrong primitive.
2. **Merely related skills listed**: a sibling skill that shares a topic but does NOT invoke / depend on / extend the base is added. PROHIBITED in this table — such skills belong in the base's `## Related Skills` section instead. The Composition table is reserved for true composers (callers that pipe through the base's public contract) and consumers (skills that hard-depend on the base's output shape).
3. **Generic / non-contextual descriptions**: a true composer is listed but its description is a paraphrase of the composer's own one-liner ("does X with Y"). PROHIBITED — the description MUST state HOW the composer uses the base: which base section/script it invokes, what it pipes in, what it gets out, and (if applicable) at which stage of its own workflow.

**Acceptance criteria** for any new row in `## Composition by Higher-Level Skills`:

- [ ] The candidate skill ACTUALLY invokes the base skill (via script shell-out, explicit `§N` reference, or hard dependency on the base's output contract). If it merely shares a topic → move to `## Related Skills` instead.
- [ ] The description names the **specific composition mechanism** — which section/script of the base is invoked, with what input, producing what output, at what stage of the composer's flow.
- [ ] The description is NOT a copy of the composer's own description; it is written from the BASE skill's perspective ("Composer X feeds inputs A into §N of this skill; consumes output B at its Step M").

**Verification**: before declaring a Composition table edit done, open each newly-added row's composer and confirm a literal reference to the base skill exists (script include, `§N` citation, or relative link to the base SKILL.md). If no such reference exists, the row is misplaced — move it to `## Related Skills` or delete it.

(Persisted as `permanent_discipline.composition-table-membership-and-description-discipline`.)

### 5.2.2 Composition Rationale Section Discipline

The `## Composition Rationale` section sits in the skill's front-matter zone (before `## 1.`) and answers a question the reader has on first arrival: **"why does this skill exist as a separate atomic unit, and how does it fit into the larger graph of skills?"** It is NOT a duplicate of `## Description` (which states what the skill does) and NOT a duplicate of `## Related Skills` (a flat list of adjacents). It is the **justification for atomicity + the upstream/downstream wiring statement**.

#### Purpose by skill role

- **Base skill** (owns a generic primitive consumed by others): Composition Rationale explains why the primitive was extracted as its own skill (typically: "multiple composers reuse it; inlining would split the SSOT") and names the known composer(s) that depend on its public contract. It MUST link to each composer.
- **Composer skill** (calls one or more base skills via their public CLI / section contracts): Composition Rationale names every base skill it composes, the EXACT mechanism of composition (which script / section / CLI flag), and the domain-specific value the composer adds on top of the bases. It MUST link to each base.
- **Standalone skill** (neither base nor composer): a one-paragraph statement of why the procedure is atomic and self-contained. Short. No table.

#### How a composer's Composition Rationale differs from a base's

| Aspect | Base skill | Composer skill |
| --- | --- | --- |
| Direction of wiring | Downstream (lists who depends on me) | Upstream (lists what I depend on) |
| Mandatory link targets | Every known composer | Every base skill composed |
| Typical mechanism phrasing | "Composers shell out to `scripts/<base>.sh` and consume its stdout JSON contract" | "Pipes `<input-discovery-output>` into `<base>/scripts/<x>` via `$(dirname "$0")/../../<base>/scripts/<x>`" |
| What it justifies | Why the primitive was extracted (SSOT) | Why the composer adds value beyond the base (domain knowledge, multi-base orchestration) |
| Failure mode if missing | Composers re-implement the primitive (inline-duplication) | Base is invoked redundantly or the wrong base is chosen |

#### Quick decision rule (which section does a cross-skill link belong in?)

```
Is the OTHER skill INVOKED by this skill (script call / CLI / hard contract dep)?
├── YES → ## Composition Rationale (and the base lists me back under ## Composition by Higher-Level Skills)
└── NO  → Is it topic-adjacent (same domain area but no invocation)?
          ├── YES → ## Related Skills (one-line bullet, no mechanism prose)
          └── NO  → Do NOT link it. Topic vagueness is not a reason to cross-link.
```

#### Example: a composer's Composition Rationale (maximum-detail template)

For a hypothetical `git-submodule-selective-init-no-lfs` skill that composes two bases — `git-submodule-selective-init` (the generic selective-init primitive) and `git-lfs-skip-smudge-env` (sets `GIT_LFS_SKIP_SMUDGE=1` in a scoped subshell) — the Composition Rationale would read:

```markdown
## Composition Rationale

This skill is a composer: it does NOT re-implement selective submodule init logic, nor does it re-implement the LFS skip-smudge environment manipulation. It orchestrates two atomic base skills:

1. **[`git-lfs-skip-smudge-env`](../git-lfs-skip-smudge-env/SKILL.md)** — invoked FIRST. The composer sources its `scripts/enter-skip-smudge.sh` via `source "$(dirname "$0")/../../git-lfs-skip-smudge-env/scripts/enter-skip-smudge.sh"` to export `GIT_LFS_SKIP_SMUDGE=1` for the current shell. This ensures any subsequent `git submodule update` invocation will fetch submodule trees without triggering LFS smudge filters (saves bandwidth + disk on repos with multi-GB LFS objects the caller does not need).
2. **[`git-submodule-selective-init`](../git-submodule-selective-init/SKILL.md)** — invoked SECOND. The composer shells out to its `scripts/init-selected-submodules.sh <path-glob>...` passing the user-supplied submodule path globs. The base script's stdout (one initialized submodule path per line) is consumed by this composer to confirm the selection matched and to surface progress.

The composer's domain-specific value-add over either base alone: a single CLI surface that guarantees the LFS-skip environment is active BEFORE the submodule update runs (ordering is critical — setting the env after the update is a no-op). Inlining either base would duplicate logic that other composers (`git-submodule-selective-init-shallow`, `git-lfs-mirror-skip-blobs`) also consume.

Bidirectional discoverability: both bases list this composer in their respective `## Composition by Higher-Level Skills` tables.
```

And the corresponding base-side entry (on `git-submodule-selective-init/SKILL.md`):

```markdown
## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`git-submodule-selective-init-no-lfs`](../git-submodule-selective-init-no-lfs/SKILL.md) | Calls `scripts/init-selected-submodules.sh <glob>...` AFTER sourcing `git-lfs-skip-smudge-env`'s env-setter; consumes the one-path-per-line stdout to surface progress to the user. |
| [`git-submodule-selective-init-shallow`](../git-submodule-selective-init-shallow/SKILL.md) | Calls `scripts/init-selected-submodules.sh <glob>...` with `GIT_SUBMODULE_DEPTH=1` pre-exported; relies on the base's exit code only (does not parse stdout). |
```

Note how each composer-table row names the EXACT script invoked, the input contract, the output contract consumed, and any ordering / env constraints. Generic descriptions like "uses selective init for the no-LFS variant" are FORBIDDEN per §5.2.1.

(Persisted as `permanent_discipline.composition-rationale-section-discipline`.)

### 5.3 Subsection Insertion Position

When adding a new numbered subsection (e.g., `### 4.7`, `#### 3b`) to an existing skill, insert it at the **correct logical position by section number** — between the existing predecessor and successor — **never append at file end**.

The default `cat >> file <<EOF` heredoc pattern is fast but appends at end-of-file; for mid-file insertions use Python `pathlib.Path.read_text() / write_text()` with a string-anchor replacement instead:

```python
import pathlib
p = pathlib.Path("path/to/SKILL.md")
s = p.read_text(encoding="utf-8")
target = "\n***\n\n## 5. Next Section"   # the successor
new_block = "\n### 4.7 New Subsection\n\nBody…\n\n***\n"
p.write_text(s.replace(target, new_block + "\n## 5. Next Section", 1), encoding="utf-8")
```

**Verification step** (mandatory before declaring the insert done):

```bash
grep -n '^##\|^### [0-9]' path/to/SKILL.md
```

Read the output and confirm that within each parent section the numbering is **monotone** (4.1, 4.2, …, 4.7, then ## 5.). A subsection that appears after the parent's terminator (`## 5.`, `## 6.`) is misplaced — relocate it.

(Persisted as `permanent_discipline.insert-subsection-at-logical-position`.)

### 5.4 Numbered-Section Scheme Consistency

When the target document uses a numbered section scheme (`## 1.`, `## 2.`, `## 3.`, …), any new section MUST follow the scheme:

- Number it as the next sequential top-level (`## N.`) — or
- Demote it to a sub-section of an existing parent (`### N.M`).

NEVER append an unnumbered `## Heading` into a numbered document. Equally: if inserting **between** existing numbered sections, **renumber all successors** in the same edit.

**Front-matter exemption.** Sections that appear BEFORE `## 1.` (typically `## Description`, `## Composition Rationale`, `## Related Skills`, `## Source Rules`) are exempt — those follow the repo's pre-Step-1 convention.

**Verification step** (mandatory before declaring the insert done):

```bash
grep -n '^##\|^### ' path/to/SKILL.md
```

Read the output and confirm:

1. Numbering is **monotone** across all `## N.` headings.
2. Every `### N.M` lives between its parent `## N.` and the next `## (N+1).`.
3. No unnumbered `## Heading` appears after `## 1.`.

(Persisted as `permanent_discipline.numbered-section-scheme-consistency`.)

**Indent-continuity check (pointer).** Every skill-doc edit that inserts
or rewrites list items, code-fence contents, or table rows MUST verify
that the new content's continuation-line indent exactly matches unmodified
sibling lines. Delegate detection and repair to the
[`list-indent-consistency`](../general/list-indent-consistency/SKILL.md)
base skill. Accept only after re-verifying that surrounding and added lines
agree.

### 5.5 Section-Home Discipline (Don't Bloat Tangential Skills)

Before adding a section of more than ~10 lines to an existing skill doc, the author MUST first answer: **"Is this section's topic within this skill's declared scope (Description + Composition Rationale)?"**

Three failure modes have been observed when authors append sections carelessly:

1. **Topic-mismatch bloat**: a large body of guidance is dropped into a skill whose scope it does not belong to, merely because the *task* that surfaced the guidance happened to touch that skill (e.g., adding a multi-paragraph "Bash-Authoring Hygiene" section to [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) just because the author was *using* scratch redirection while authoring bash). PROHIBITED — readers of the host skill encounter off-topic content, and the true SSOT skill never gets the addition.
2. **Duplicate-SSOT drift**: the guidance is added to skill A even though skill B already owns it. PROHIBITED — future edits diverge between the two copies.
3. **No-SSOT-yet sprawl**: the guidance is genuinely new and has no owning skill, so the author parks it in the nearest neighbour. PROHIBITED — create a new dedicated skill (via the Factory's normal flow) or extend the most-related EXISTING owner; do not park.

**Acceptance criteria** before adding a section larger than ~10 lines to an existing skill:

- [ ] The section's topic is explicitly named in the host skill's `## Description` OR `## Composition Rationale`. If not → STOP, find/create the correct owner.
- [ ] No other skill already owns the topic (verify with the `grep` tool on a 2–3 word topic phrase across `.agents/skills/**/SKILL.md`). If another skill owns it → add there; in the host, leave at most a one-line delegation pointer with relative link to the SSOT.
- [ ] If genuinely new and no owner exists → invoke the Factory's new-skill flow (`## 1. When to Apply`) rather than parking.

**Thin-pointer template** for the host skill when delegating: a single sentence of the form *"For <topic>, see [<owner-skill>](../<owner-skill>/SKILL.md) — that skill is the SSOT."* A one-line pointer is the maximum permitted footprint of a tangential topic on a host skill.

**Historical example**: an earlier authoring session embedded a multi-paragraph Bash-Authoring Hygiene section into [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) because the author was using scratch redirection while writing the bash. The correct home was this skill's §4 (which delegates the freeze catalogue to [`ide-renderer-freeze-prevention`](../ide-renderer-freeze-prevention/SKILL.md) as the SSOT). The section was later relocated and only the SSOT pointer remained in scratch.

(Persisted as `permanent_discipline.section-home-discipline`.)

### 5.6 Cross-Reference Link Discipline

Every **first-mention** (within a given section / subsection) of any of the following inside a skill doc MUST be rendered as a proper relative markdown link, not as a bare backtick code span:

- A sibling skill folder → `[`<skill-name>`](../<skill-name>/SKILL.md)`
- A rule doc → `[`<rule-name>.md`](../../../ai-agent-rules/<rule-name>.md)` (path depth adjusts to the host file's location)
- A memory file → `[`<memory>.md`](../../../memories/repo/<memory>.md)`
- Any other in-repo path the reader may want to navigate to

Subsequent re-mentions within the same section/subsection MAY use a bare backtick code span (`` `name` ``) for readability — but the FIRST mention sets the navigability anchor for that section.

**Rationale**: a skill doc is read as a hypertext, not a manuscript. A bare `` `repo-scratch-output-capture` `` looks identical to a linked one in the source but is dead text in the rendered view — readers cannot navigate to the referenced skill and authors of inbound links lose discoverability of their target.

**Forbidden patterns** (must be fixed when found):

1. A skill name mentioned in prose as a bare code span when the host skill is not itself the named skill.
2. A relative path written as `\`../foo/SKILL.md\`` (code span containing a path) without being wrapped as a link.
3. A `§N` citation that names a foreign skill without linking to that skill's SKILL.md.

**Verification step** (mandatory before declaring a skill-doc edit done):

```bash
grep -nE '`[a-z][a-z0-9_./-]+`' path/to/SKILL.md
```

Read every hit and ask: is the backticked token a skill folder, rule doc, memory file, or repo path? If YES and the same line does NOT contain the surrounding `[…](…)` link syntax → convert to a proper relative link. Acceptable bare-code-span backticked tokens: shell commands, code identifiers (function/variable/class names), file extensions, CLI flags, sentinel strings.

(Persisted as `permanent_discipline.cross-reference-link-discipline`.)

### 5.7 Heading Scope Discipline (Choose a Parent That Hosts Siblings)

Before naming a new top-level section (`## N. <Heading>`) in a skill doc, the author MUST ask: *"Is this a single atomic concern, or is it one of multiple related concerns that share a theme?"*

If **multiple related concerns** are foreseeable → choose a parent heading whose scope is **broad enough to host current and future siblings**, and place the immediate concern as a `### N.1` subsection under it. Do NOT promote the first specific concern to top-level — doing so forces later authors to either (a) cram unrelated concerns under a too-narrow heading, or (b) renumber the whole document when a sibling arrives.

**Decision test** (apply before writing the heading):

1. Can you imagine writing one or more sibling `### N.M` sections on the same theme within the next 1–3 authoring sessions? → **YES** → the parent (theme) is the correct top-level; the concern is `### N.1`.
2. Is this section genuinely atomic and stands alone with no foreseeable siblings on the same theme? → **YES** → a specific top-level is fine.
3. If unsure → prefer the broader parent. A parent with only one subsection is cheap to maintain; a misplaced top-level is expensive to restructure later (every cross-reference to `§N` breaks under renumbering).

**Forbidden patterns**:

1. **Premature specificity**: making `## N. <Specific Concern>` when 2+ sibling concerns on the same theme are visible at authoring time.
2. **Retroactive umbrella-stuffing**: when a sibling concern arises later, cramming it under a too-narrow existing top-level instead of restructuring to the correct parent. PROHIBITED — restructure to the correct parent and renumber inbound references per §5.1.

**Historical example**: §5 was originally planned as `## N. Post-Rename Cross-Reference Sweep`. The author noticed that "post-rename sweep" is one of several skill-doc-editing concerns (also: cross-reference append, composition-table membership, subsection insertion, numbered-section consistency, section-home discipline, cross-reference link discipline, heading scope itself). The correct shape was `## 5. Skill-Doc Editing Discipline` with `### 5.1 Post-Rename Cross-Reference Sweep` as one of N subsections — which is what 5.1 through 5.7 now reflects.

(Persisted as `permanent_discipline.heading-scope-discipline`.)

### 5.8 Style-Consistency Discipline (Match the Surrounding Document)

Before adding or editing any block in an existing skill doc, the author MUST sample the surrounding 20–50 lines AND the document's overall conventions, and ensure the new content matches the dominant local pattern across **all** of the following axes:

| Axis | Examples of variants to choose between |
| --- | --- |
| List marker | `-` vs `*` vs `1.` (numbered) |
| List indentation depth | 2-space vs 4-space continuation |
| Blank lines around headings | 0, 1, or 2 blank lines above/below `##` / `###` |
| Blank lines between list items | none vs one (compact vs loose lists) |
| Blank lines around fenced code | always one above + one below vs flush |
| Bold / italic markers | `**bold**` vs `__bold__`; `*italic*` vs `_italic_` |
| Code-span vs link for skill/file names | governed by §5.6 (Cross-Reference Link Discipline) |
| Horizontal-rule pattern | `***` vs `---` vs none; frequency between sections |
| Step / mandate prefix | `1.`, `**1.**`, `### N.M`, `**Mandate Name**:` |
| Table header alignment | `:---` vs `---` vs `---:` |
| Heading capitalization | Title Case vs Sentence case |

**Mandates**:

1. **Sample before write.** Read at least the immediate predecessor + successor sibling sections of the insertion point. Match their dominant style. If conflicting styles already coexist locally, match the nearest sibling at the same nesting depth.
2. **Do not introduce a second marker style.** If the document uses `-` for bullets throughout, do NOT introduce a `*` bullet block. If parent sections use `**Mandate Name**:` prefix, do NOT introduce a bare numbered list inside a new sibling sub-section.
3. **Preserve indentation depth.** If continuation lines under a list item use 4 spaces in the surrounding document, the new content's continuation lines MUST also use 4 spaces — not 2.
4. **Preserve blank-line spacing.** Count blank lines above/below the nearest sibling heading and reproduce the same count for the new heading.

For automated detection and repair of continuation-line indent drift, use
the [`list-indent-consistency`](../general/list-indent-consistency/SKILL.md)
base skill.

**Verification step** (mandatory before declaring the edit done):

```bash
git --no-pager diff -U0 path/to/SKILL.md | head -200
```

Visually scan the diff for style drift vs surrounding lines: do the inserted bullets use the same marker as the file's existing bullets? Same indentation? Same blank-line padding around headings? If any axis drifts → fix in the same edit, not later.

**Historical example**: an insertion of "Script Authoring Mandates" subsections into `skill-factory/SKILL.md` introduced styling that diverged from the surrounding numbered-mandate format (mixed marker styles, inconsistent blank-line padding around headings, and `**Mandate Name**:` prefix used in some siblings but bare numbered list in others). The content was correct; the formatting drift forced a follow-up cleanup edit. The fix would have been free if the §5.8 verification step had been run on the original edit.

(Persisted as `permanent_discipline.style-consistency-discipline`.)

***

## 6. Skill Enrichment Workflow

This section bridges the editing disciplines (§5) with the commit
workflow. Use it when enriching an existing skill (adding content,
fixing cross-references, updating style) rather than creating a new
one from scratch.

### 6.1 Gap Analysis

Before editing, identify what is missing or needs improvement:

1. Read the target skill's SKILL.md deeply — understand its structure,
   sections, style, and cross-references.
2. Compare against related skills — are there patterns or conventions
   in sibling skills that the target lacks?
3. Check the
   [`pre-commit-verification-protocol`](../general/pre-commit-verification-protocol/SKILL.md)
   and [`skill-cross-reference-audit`](../general/skill-cross-reference-audit/SKILL.md)
   — do any flagged issues apply to this skill?
4. Define the specific gap (new section, missing cross-ref, style fix,
   content update).

### 6.2 Read & Pattern-Match Phase

1. Sample the surrounding 20–50 lines of the insertion point per §5.8
   (Style-Consistency Discipline).
2. Identify the dominant local patterns:
   - List marker (`-` vs `*` vs `1.`)
   - Blank-line spacing around headings
   - Bold/italic markers
   - Code-span vs link for skill names (§5.6)
3. Match the new content to these patterns before writing.

### 6.3 Edit Phase

1. Apply the editing disciplines from §5 as applicable:
   - §5.1 — Post-Rename Cross-Reference Sweep (if renaming a section)
   - §5.2 — Cross-Reference Append (if adding a new skill to Related Skills)
   - §5.3 — Composition Table Membership (if the skill has a Composition table)
   - §5.4 — Subsection Insertion (if adding a subsection into an existing section)
   - §5.5 — Numbered-Section Consistency (if adding a new numbered section)
   - §5.6 — Cross-Reference Link Discipline (every skill/doc name gets a link on first mention)
   - §5.7 — Heading Scope Discipline (choose a broad-enough parent for foreseeable siblings)
   - §5.8 — Style-Consistency Discipline (match surrounding document patterns)
2. Write the new content matching the identified patterns.
3. Update AGENTS.md bridge if the skill's description or category
   changed.

### 6.4 Verification Phase

Run the
[`pre-commit-verification-protocol`](../general/pre-commit-verification-protocol/SKILL.md):

1. Cross-reference audit:

   ```bash
   python3 .agents/skills/general/skill-cross-reference-audit/scripts/audit-cross-refs.py
   ```

2. Markdown lint:

   ```bash
   markdownlint-cli2 .agents/skills/<skill-path>/SKILL.md
   ```

3. Visual smoke test:

   ```bash
   git diff -U0 .agents/skills/<skill-path>/SKILL.md | head -200
   ```

Fix any issues before staging.

### 6.5 Stage & Commit Phase

Follow the
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
protocol:

1. Stage the edited files.
2. For AGENTS.md with multi-session rows, use the
   [`opencode-agents-md-manager`](../opencode-agents-md-manager/SKILL.md)
   composer to isolate current-session rows.
3. Write a descriptive commit message following conventional commits:
   `feat(skill): <change-description>` or `fix(skill): <change-description>`.
4. Present the commit-preview and await user authorization per §2e.

### 6.6 Post-Commit Verification

After the commit is executed:

```bash
git log --oneline -3
git status
```

Confirm the commit landed correctly and no unintended files were
included.

### 6.7 Relationship to Other Workflows

- For **creating a new skill from scratch**, use §1 (Skill Creation
  Checklist) + §3 (Post-Drafting Checklist).
- For **editing an existing skill**, use this §6 workflow.
- For **batch execution across multiple skills**, use
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  §2g (batch-by-batch authorization).

***

## Related Skills

- [`markdown-generation`](../markdown-generation/SKILL.md) — base primitive
  `scripts/join-blockquote-header.py` is shelled out to by this skill's
  `scripts/audit-normalize-skill-headers.py` (the §3 Header Blockquote Audit).
- [`skill-doc-metadata-separation`](../markdown/skill-doc-metadata-separation/SKILL.md) — composer enforcing
  the §2.1 / §2.2 item 5 separate-file convention for `Changelog` / `Traceability`; its `--check`
  mode is the §3 Metadata-Separation Audit.
- [`markdown-section-to-companion-doc`](../markdown/markdown-section-to-companion-doc/SKILL.md) — base
  primitive (section → companion-file split) that the metadata-separation composer delegates all
  file mutation to.
- [`human-scanable-organization`](../general/human-scanable-organization/SKILL.md) — the 8±2
  human-scanability principle and grouping methodology that determines when and how to
  sub-group a skill folder.
- [`skill-library-domain-grouping`](../general/skill-library-domain-grouping/SKILL.md) — the
  project-specific domain taxonomy that governs where every new skill belongs. Consulted at
  §2.1 creation time (mandatory taxonomy placement before folder selection) AND enforced
  by the Post-Drafting Checklist (§3).
- [`skill-cross-reference-audit`](../general/skill-cross-reference-audit/SKILL.md) — automated
  audit consumed by §3 Composition Audit step; run after any skill modification to verify
  cross-reference integrity, missing bridges, and missing frontmatter.
