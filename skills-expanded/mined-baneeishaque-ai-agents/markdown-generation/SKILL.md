---
name: markdown-generation
description: Industrial protocol for generating lint-compliant, high-fidelity markdown documentation.
category: Documentation-Standards
---

# Markdown Generation Skill (v1)

This skill provides a standardized protocol for generating Markdown that complies with the **Industrial standard**
(120-character line limit) and passes `markdownlint-cli2` (markdown linting CLI tool) audits.

*

## 1. Core Syntax Standards

Every generated file MUST adhere to these absolute constraints:

### 1.1 Line Length (MD013)

- **Limit**: 120 characters per line.
- **Exception**: Long URLs and file paths that cannot be broken. Use **Reference-style links** at the bottom of the
  document to resolve length violations for URLs.
- **Wrapping**: Proactively wrap descriptions and YAML blocks to stay under the limit.

### 1.2 Layout & Tables (MD060)

- **Table Alignment**: Use mathematically perfect aligned pipes (`|`).
- **Cell Spacing**: One mandatory space padding on both sides of every pipe (` | content | `).
- **Blank Lines**: Headers, lists, and code blocks MUST be surrounded by blank lines.

### 1.3 Frontmatter

- **Rules/Skills**: Use the triple-dash block (`---`) as defined in [ai-rule-standardization-rules.md](../../../ai-
agent-rules/ai-rule-standardization-rules.md).
- **General Docs**: Use the HTML comment block (`<!-- title: ... -->`) for indexing.

### 1.4 Cross-Reference Links & Anchors

The `markdownlint-cli2` tool validates anchors via **MD051 - Link fragments should be valid**.

- **Anchor Format**: For header `### Step 1 — Deep Change Analysis`, the anchor is `#step-1-deep-change-analysis`
- **Generation Rule**: Convert header to lowercase, replace spaces and `—` (em dash) with dashes (`-`)
- **Verification**: Run `markdownlint-cli2` - it will catch broken anchor errors (MD051)
- **Best Practice**: Always use anchors when linking to headers within skill/rule files

### 1.5 Registry Link Standards (Registry Tables)

In centralized registry files (e.g., `AGENTS.md`, skill indexes), links to internal
repository paths MUST follow these formatting requirements:

- **Backtick Labels**: The link label MUST be the full relative path to the file,
  enclosed in backticks (e.g., `[`.agents/skills/my_skill/SKILL.md`](.agents/skills/my_skill/SKILL.md)`).
- **Consistency**: All links within the same registry table MUST follow this exact
  style for uniform readability and automatic navigation support.

### 1.6 Path Verification

#### Default (CLI-Only)

- **Anchor**: Enforced by MD051 (built-in)
- **File Path**: NOT enforced - run manual verification:
    - `ls -la <path>` to confirm target exists
    - From `skills/<skill>/`: `ls ../<sibling-skill>/SKILL.md`
    - From `skills/<skill>/`: `ls ../../../ai-agent-rules/<rule>.md`

#### With Node.js Custom Rules (If Available)

Install and configure:

```bash
npm install --save-dev markdownlint-rule-relative-links
```

Add to `.markdownlint-cli2.jsonc` (NOT `.markdownlint.jsonc`):

```jsonc
{
    "customRules": ["markdownlint-rule-relative-links"],
    "config": {
        "relative-links": { "root_path": "." }
    }
}
```

Then both anchors AND file paths validated automatically.

### 1.6 Blockquote Metadata Headers

Author-style skill/rule docs carry a metadata blockquote immediately below the
title: consecutive `> **Label:** value` lines such as `> **Skill ID:**`,
`> **Version:**`, `> **Layer:**`, `> **Standard:**`.

- **Problem**: CommonMark renders consecutive blockquote lines as a SINGLE
  paragraph. Without separators the `**Label:**` tokens of the whole header
  block glue into one run on screen (`**Skill ID:** **Version:** 1.0.0 ...`).
- **Canonical rule**: inside a consecutive run of 2+ `> **Label:**` lines, end
  EVERY line except the last with `<br>`. The last line of the run carries no
  `<br>`.
- **Blank `>` separators are FORBIDDEN**: an empty `>` line collapses under
  CommonMark regardless of `<br>` on the neighboring lines.
- **Single header line**: a run of exactly one `> **Label:**` line needs no
  `<br>` (nothing follows it in the same paragraph).

Canonical (renders line-by-line):

```markdown
> **Skill ID:** `demo-skill`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)
```

Collapsed (single paragraph — FORBIDDEN):

```markdown
> **Skill ID:** `demo-skill`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)
```

**Enforcement**: the base primitive
`scripts/join-blockquote-header.py` owns this transform (idempotent
`--check`/`--apply`/`--diff`). The composer
[`skill-factory`](../skill-factory/SKILL.md) `scripts/audit-normalize-skill-headers.py`
walks the whole library against it.

### 1.7 Cross-Repository / Submodule Isolation Links

When a repository is consumed both as a standalone Git repository AND as a
submodule inside one or more parent repositories (e.g., `ai-agent-rules`
standing alone on GitHub while also being embedded in `ai-suite`), link
directionality is **asymmetric** and MUST be enforced as follows:

- **Inbound (parent → submodule)**: Files in the parent repository MAY
  reference files inside the submodule using ordinary workspace-relative
  paths (e.g., `ai-agent-rules/git-submodule-rules.md`,
  `../../../ai-agent-rules/git-submodule-rules.md` from a skill three levels
  deep). These resolve correctly because the submodule is checked out under a
  known relative path within the parent working tree.

- **Outbound (submodule → parent or sibling repo)**: Files inside the
  submodule MUST NOT use relative paths that traverse above the submodule's
  own repository root (e.g., `../.agents/...`, `../../other-repo/...`). Such
  paths resolve only inside the parent checkout and **silently break** the
  moment the submodule is consumed standalone (cloned directly, browsed on
  its own GitHub page, packaged for distribution, or vendored elsewhere).
  This is a one-way containment rule:

    > *A submodule has its own existence. It MUST NOT depend on the
    > existence, layout, or checkout location of any parent that happens to
    > embed it.*

- **Required outbound form — Hosted VCS Permalink (SHA-pinned)**: When a
  file inside the submodule genuinely needs to reference content in a parent
  or sibling repository, the link MUST be an absolute hosted-VCS URL pinned
  to a commit SHA (never `main` / `master`):

    ```markdown
    [Skill Name](https://github.com/<org>/<parent-repo>/blob/<full-40-char-sha>/<path>/SKILL.md)
    ```

    Branch-tip URLs (`/blob/main/`, `/blob/master/`) are FORBIDDEN here for
    the same link-rot reason given in §4.2.1.

- **Preferred host — upstream, not a fork**: The `<org>` segment of an
  outbound permalink MUST point at the **canonical upstream** of the
  referenced repository, NOT at a personal or short-lived fork. Forks may be
  deleted, renamed, or made private at any time, which silently breaks every
  permalink pointing at them. The upstream is identified as the repository
  whose `parent` field (`gh repo view --json parent` or the GitHub UI's
  *"forked from"* breadcrumb) is empty — i.e., the root of the fork network.
  If only a fork is currently writable but the upstream exists, the
  permalink MUST still target the upstream; push the referenced commit
  upstream first, or use the upstream's pre-existing SHA. Author choice MAY
  override this default only when the upstream is unreachable (deleted,
  private, or 404) — see `git-submodule-dead-upstream-audit` for the
  diagnostic procedure.

- **Preferred alternative — migrate or duplicate the SSOT**: Before adding an
  outbound permalink, the agent MUST first consider whether the referenced
  content belongs inside the submodule itself. A persistent outbound
  permalink is a code smell suggesting the SSOT is in the wrong repository.

- **Audit signal**: Any occurrence of the regex
  `\]\(\.\.\/(?!\.\.\/)[^)]*\)` (or deeper `../../`) inside a tracked file of
  a submodule is a violation of this section unless the traversal stays
  inside the submodule's own tree. CI / pre-commit hooks SHOULD flag such
  links.

### 1.8 Section Dividers (Industrial Standard)

- **Marker**: Use three asterisks (`***`) for all horizontal rules.
- **Rule Compliance**: This ensures compliance with `markdownlint` rule MD035
  and provides a consistent visual weight.
- **Forbidden**: Do NOT use hyphens (`---`) or underscores (`___`) for dividers.

### 1.9 Layout & Alignment

- **Centered Blocks**: Use `<div align="center">` followed by a blank line to
  center-align branding elements.
- **Lint Compliance**: Avoid inline suppression (`MD033`). Instead, use the
  project-level `.markdownlint.jsonc` configuration to globally allow the
  `div` element for layout purposes.
- **Closing Tags**: Always ensure a matching `</div>` closing tag is present.
- **Empirical Spacing**: Maintain a blank line between the HTML markers and
  markdown content.

*Example:*

```markdown
<div align="center">

![Badge](url)

*Caption text*

</div>
```

*

## 2. Verification Workflow

Before finalizing ANY markdown file, the agent MUST:

1. **Config Initialization**: If the project lacks a `.markdownlint.jsonc` file, the agent
   MUST initialize it using rules from the reference config (`../../../.markdownlint.jsonc`
   relative to this skill file), incorporating the `MD013` 120-character line length exception.
2. **Sync Check**: Ensure `.vscode/settings.json` contains `"markdownlint.configFile": ".markdownlint.jsonc"` to
   synchronize the IDE extension with the project's Industrial standard.
3. **Run Markdown Lint Workflow**: Execute the full
   **[Markdown Lint Workflow](../general/markdown-lint-workflow/SKILL.md)** 3-step pipeline
   on the file:
   - Step 1: `markdownlint-cli2 --fix`
   - Step 2: Companion scripts in execution order
   - Step 3: Manual fix + final `markdownlint-cli2` audit
4. **Fidelity Verification**: Ensure the "Fidelity Mandate" (no loss of user technical specifics) is upheld during
   formatting.

*

## 3. Lint Fix Protocol

Companion scripts and the full 3-step lint fix pipeline have moved to
**[Markdown Lint Workflow](../general/markdown-lint-workflow/SKILL.md)**.

This skill delegates all lint-fix operations there. See that skill for:

- The 7 companion scripts (with descriptions and usage)
- Required execution order (table separators → fence language → wrap long
  lines → ...)
- Known `markdownlint-cli2 --fix` caveats (MD040 fence corruption)
- The convenience pipeline script `fix-markdown-pipeline.py`

*

## 4. Related Rules & References

- **SSOT**: [markdown-generation-rules.md](../../../ai-agent-rules/markdown-generation-rules.md)
- **Formatting Protocol**: [ai-rule-standardization-rules.md](../../../ai-agent-rules/ai-rule-standardization-rules.md)
- **Error Patterns & Case Studies**: [markdown-generation-error-patterns.md](./markdown-generation-error-patterns.md)
- **Lint Fix Pipeline**: [markdown-lint-workflow](../general/markdown-lint-workflow/SKILL.md)

*

## 5. CI Integration

### 5.1 Pipeline Script

When automating lint fixing in a CI pipeline or pre-commit hook, use the
convenience pipeline script from
**[Markdown Lint Workflow](../general/markdown-lint-workflow/SKILL.md#3-convenience-pipeline-script)**:

```bash
python3 .agents/skills/general/markdown-lint-workflow/scripts/fix-markdown-pipeline.py \
  file.md
```

This runs `markdownlint-cli2 --fix`, then all companion scripts in execution
order, then a final audit — all in one invocation. For individual companion
script usage, see the
[Markdown Lint Workflow skill](../general/markdown-lint-workflow/SKILL.md#2-companion-scripts).

### 5.2 YAML Frontmatter Validation

YAML frontmatter `description` values that contain colons followed by
YAML-reserved tokens (e.g., `resetMocks: true`) cause downstream parsers
(VS Code preview, `markdownlint-cli2`) to misinterpret the colon as a new
YAML key opening.

**Rule:** If a `description` value contains any colon (`:`) that is not
trailing whitespace or a URL scheme (`https://`), wrap the entire value in
double quotes (`"..."`). Bare unquoted descriptions containing internal
colons are FORBIDDEN.

Correct:

```yaml
---
description: "Repository-specific composer that uses the generic ai-suite skill for debugging missing toolbar features"
---
```

Incorrect:

```yaml
---
description: Repository-specific composer that uses the generic ai-suite skill for debugging missing toolbar features
---
```

The difference is invisible in most Markdown renderers but causes silent
YAML parse failures in editor preview panes and schema validators.

### 5.3 Lint Gate

Every skill authored via the Skill Factory (`skill-factory`) MUST pass the
full Verification Workflow (§2) including the
**[Markdown Lint Workflow](../general/markdown-lint-workflow/SKILL.md)** 3-step
pipeline before it is considered complete. The factory's Post-Drafting
Checklist (§3) is the SSOT for the gating criteria.

## 6. Companion Scripts

| Script | Location | Purpose |
| --- | --- | --- |
| `scripts/join-blockquote-header.py` | Base (generic markdown primitive) | Normalize metadata-header blockquote runs (`> **Label:**` lines) to the §1.6 canonical form: `<br>` on every run line except the last. Idempotent `--check`/`--apply`/`--diff`; CRLF/LF and trailing-newline preserved; stdin or file input. Consumed by the `skill-factory` composer. |

## Composition by Higher-Level Skills

| Composer | Consumes |
| --- | --- |
| [`skill-factory`](../skill-factory/SKILL.md) | `scripts/join-blockquote-header.py` via `scripts/audit-normalize-skill-headers.py` (library-wide header audit + apply) |

## Related Skills

- [`markdown-lint-workflow`](../general/markdown-lint-workflow/SKILL.md) — the
  3-step lint fix pipeline this skill delegates to (§3)
