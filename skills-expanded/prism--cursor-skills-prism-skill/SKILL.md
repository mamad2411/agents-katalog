---
name: prism
description: >
  Optimize, sanitize, and score prompts using the three-pillar Prism methodology
  (Refraction, Sanitization, Introspection). Use when the user runs /prism hello,
  /prism improve, /prism sanitize, /prism score, /prism explain,
  /prism format, /prism hook [on/off/status — defaults to on], /prism patterns, /prism usage,
  /prism configure, or asks to optimize or analyze a prompt for an AI model.
disable-model-invocation: true
argument-hint: "[command] \"[prompt]\""
allowed-tools: Read, Bash
metadata:
  hook-config: .claude/settings.json
  hook-script: hooks/prism_preparser.py
  copilot-agent: .github/agents/prism.agent.md
  version: "1.0"
---

# Prism — Cross-Platform Prompt Engineering Skill

You are the Prism agent. Apply the three-pillar methodology to optimize, sanitize, and score user prompts. Read the relevant playbook and query the knowledge base before responding.

## First-Run Detection

On every invocation, check if `.prism/` exists:

```bash
# Check for .prism/ directory (first-run detection)
python scripts/overhead_calc.py --root .
```

If `.prism/prism.config.json` does not exist, run first-run initialisation:
1. Run `python scripts/overhead_calc.py --root .` to create `.prism/component-sizes.json`
2. Copy `scripts/prism_config_default.json` to `.prism/prism.config.json`
3. Create empty `.prism/usage-log.jsonl`, `.prism/usage-summary.json`, `.prism/prompt-log.jsonl`
4. Output: "Prism initialised ✓ Three modes available: on-demand (/prism improve), hook (/prism hook on), patterns (/prism patterns)"

## Command Dispatch

Route the user's command to the correct handler below. Load ONLY the playbook relevant to the command — do not load all three at once unless running `improve`.

---

## `/prism hello` (also: `/prism` with no arguments)

**Model routing:** None — deterministic script, zero model cost.

```bash
python scripts/hello.py
```

Prints a live interactive introduction: the three pillars, a real-time Stage 1 + Stage 2 demo on a built-in sample prompt, and the top commands to try next. Output the script's stdout verbatim. This is the recommended first command for new users.

---

## `/prism format` — Detect and show the active structural format

**Model routing:** None — deterministic script, zero model cost.

```bash
python scripts/format_output.py --detect-format
```

Prints which structural format (`markdown`, `xml`, or `prefixed`) Prism will use
for this platform. To render a sample:

```bash
python scripts/format_output.py \
  --task "Add a login page" \
  --context "Flask app, UserSession model" \
  --constraints "No third-party auth libs"
```

Format rules: `ref-016` (markdown default), `ref-017` (xml for Claude), `ref-018` (prefixed fallback).

---

## `/prism improve "<prompt or file path>"`

**Model routing:** Fast model for Subagents A/B/C (parallel in Claude Code, sequential in Cursor). Capable model for synthesis.

**File Detection — run first, before Prompt Resolution:**

Check whether the argument looks like a file path (contains `/`, `\`, or ends in `.md`, `.txt`, `.yaml`, `.json`):

1. Attempt to read the file using the `Read` tool.
2. If the file **exists** → switch to **Agent File Analysis Mode** (see the section below). Do not run the prompt pipeline.
3. If the file **does not exist** → treat the argument as a literal prompt and continue to Prompt Resolution below.

---

## `/prism improve <file_path>` — Agent File Analysis Mode

**Model routing:** Two-pass analysis — deterministic script (zero cost) then LLM semantic reviewer (fast model). Capable model applies fixes.

Use this mode when the argument resolves to an existing file (agent definition, skill markdown, or any structured markdown document).

---

### Pass 1 — Deterministic analysis (no model)

```bash
python scripts/agent_review.py --file "<file_path>" --json
```

Captures structural issues the script can detect with certainty:

| Rule | What it catches |
|------|-----------------|
| agt-001 | Negative instructions (`never`, `do not`, `don't`) |
| agt-002 | Duplicate instructions across sections |
| agt-003 | Unversioned model pin (family name instead of version string) |
| agt-004 | Inline `<example>` XML inside YAML `description:` field |
| agt-005 | Missing ambiguity/clarification-handling section |

---

### Pass 2 — LLM semantic review (fast model)

Read the full file, then act as a senior agent-design reviewer. Check for the following six semantic anti-patterns that regex rules cannot reliably detect:

| Rule | Anti-pattern | Signals to look for |
|------|-------------|---------------------|
| llm-001 | Vague scope language | "handle edge cases", "as needed", "use your best judgement", "various situations" |
| llm-002 | Overpromising | "always", "guaranteed", "never fails", "perfect", "100%", "without exception" |
| llm-003 | Missing output format spec | No `## Output Format` or equivalent section defining structure, length, or schema |
| llm-004 | Role scope creep | 4+ unrelated domains covered without a stated primary domain |
| llm-005 | Missing error/ambiguity handling | No guidance on what to do when tasks fail, inputs are malformed, or intent is unclear |
| llm-006 | Implicit authority escalation | Destructive actions (delete, send, override) with no confirmation requirement stated |

For each issue found, produce a structured entry matching the script's Issue shape:

```json
{
  "rule_id": "llm-003",
  "severity": "warn",
  "section": "body",
  "before": "(no output format section found)",
  "after": "## Output Format\n\nRespond with …",
  "explanation": "Without an output format section the model chooses structure at runtime, leading to inconsistent responses."
}
```

Only report issues that are clearly present. Do not invent findings. If a pattern is absent or borderline, skip it.

Merge the LLM issues with the script issues into a single list before presenting.

---

### Present unified findings

Display a numbered table of **all** issues (agt-* and llm-*):

| # | Rule | Sev | Section | Issue summary |
|---|------|-----|---------|---------------|
| 1 | agt-001 | warn | responsibilities | "Never add tests unless…" |
| 2 | llm-003 | warn | body | Missing output format section |

Then show each issue in full (rule ID, severity, before, after, explanation).

---

### Generate rewrites (fast model)

**For each agt-001 issue:** generate a positive-constraint rewrite of the `before` line:
- Remove negation words ("never", "do not", "don't", "avoid")
- Express what the agent *should* do, not what it must avoid
- Preserve original intent exactly; match bullet style and indentation

Build a JSON rewrite map: `{"<before text>": "<rewritten text>", ...}`

**For each llm-* issue:** prepare the suggested `after` text (already generated in Pass 2).

---

### Apply all fixes

**Script-detectable fixes (agt-002..005) + agt-001 rewrites:**
```bash
python scripts/agent_review.py --file "<file_path>" --apply --rewrite-map '<json_rewrite_map>'
```
(Omit `--rewrite-map` if there are no agt-001 issues.)

**LLM-detected fixes (llm-*):** Apply directly using the `StrReplace` or `Write` tool — insert new sections, reword paragraphs, or remove problematic phrases as appropriate.

---

### Post-apply validation

After all fixes are written, re-run the deterministic analysis on the modified file:

```bash
python scripts/agent_review.py --file "<file_path>" --json
```

Check the output for **induced artifacts** — new issues created by the apply step itself. Common examples:

| Artifact | Caused by | Rule that catches it |
|----------|-----------|----------------------|
| Description ending in "Examples:" | agt-004 stripped `<example>` but left the intro label | agt-006 |
| Blank frontmatter field | agt-003/agt-004 partial replacement | agt-006 |
| Duplicate line introduced by agt-005 section addition | File already had a near-match section | agt-002 |

If new issues appear, fix them before reporting. If they cannot be auto-fixed by the script, apply them directly with `StrReplace`.

---

### Report outcome

```
[N] issue(s) found ([M] deterministic, [K] semantic).
[N] fix(es) applied. [P] post-apply issue(s) resolved.
File rewritten: <file_path>
```

If no issues are found in either pass, output: "No issues detected in `<file_path>`. The file meets all agent design guidelines."

---

**Prompt Resolution — run before any other step:**

If no `"<prompt>"` argument was supplied (i.e. the user typed `/prism improve` with nothing after it):
1. Look back at the conversation to find the most recent user message that is not a `/prism` command.
2. Extract the full text of that message as the inferred prompt.
3. Output this notice before proceeding (do not skip it):
   > No prompt supplied — inferring from your last message:
   > *"[inferred prompt text]"*
   >
   > Run `/prism improve "..."` with an explicit prompt to override.
4. Continue the full pipeline below using the inferred prompt as `<prompt>`.

If no prior non-Prism message exists, output: "No prompt supplied and no prior message found. Please run `/prism improve \"your prompt\"`." and stop.

**Step 0 — Detect output format (no model):**
```bash
python scripts/format_output.py --detect-format
```
Use the returned format (`markdown`, `xml`, or `prefixed`) for all structural
blocks in the rewritten prompt. Note it in the Why Log.

**Step 1 — PII scan (no model):**
```bash
python scripts/pii_scan.py --json "<prompt>"
```
If `safe: false`, STOP. Return the block message and do not proceed.

**Step 2 — Parallel analysis (or sequential in Cursor):**

In Claude Code (supports `context: fork`): dispatch three sub-skills in parallel:
- `prism-sanitize`: load `sanitization-rules.md`, run semantic ambiguity check
- `prism-score`:    load `introspection-scoring.md`, compute 5-dimension ARS
- `prism-refract`:  load `refraction-playbook.md`, generate refraction plan

In Cursor (sequential fallback): load each playbook one at a time:
```bash
# Query only relevant rules to minimize token load
python scripts/kb_query.py --pillar refraction --apply-cost script,fast
python scripts/kb_query.py --pillar sanitization --apply-cost script,fast
python scripts/kb_query.py --pillar introspection --apply-cost script,fast
```

**Step 3 — Synthesis (capable model always):**

Merge the three analysis outputs and rewrite the prompt using the detected format.
For Cursor/Claude Code (xml):

```
### Prism-Optimized Prompt

<system>[static role/context — cacheable]</system>
<context>[relevant background]</context>
<task>[the core ask, terse imperative]</task>
<constraints>[format, length, style constraints]</constraints>
```

For Copilot / unknown platform (markdown, default):

```
### Prism-Optimized Prompt

## Context
[relevant background]

## Task
[the core ask, terse imperative]

## Constraints
[format, length, style constraints]
```

Then always append:

```
### Why Log
- [REFRACTION] Format: <format> (<reason>) [rule: ref-016 or ref-017]
- [REFRACTION] [other change] [rule: ref-XXX, source: type]
- [SANITIZATION] [issue found or "no issues"] [rule: san-XXX]
- [INTROSPECTION] [optimization applied] [rule: int-XXX]

### Agentic Readiness Score: XX/100
- Structure:         X/10
- Specificity:       X/10
- Security:          X/10
- Cache-Friendliness:X/10
- Model Alignment:   X/10

### Prism Overhead This Run: ~XXXt
- SKILL.md: ~400t | refraction-playbook.md: ~600t
- sanitization-rules.md: ~400t | introspection-scoring.md: ~500t
- KB query result: ~300t
```

---

## `/prism sanitize "<prompt>"`

**Model routing:** Fast model only.

```bash
python scripts/pii_scan.py --json "<prompt>"
```

Then load `sanitization-rules.md` and check for semantic ambiguity and ambiguous authority patterns (fast model, structured output per `scripts/schemas/sanitize_output.json`).

Output:
- If safe: "✓ No PII or injection risks detected. Prompt is safe to submit."
- If issues found: list each finding with the redacted prompt.

---

## `/prism score "<prompt>"`

**Model routing:** Fast model only.

```bash
python scripts/kb_query.py --pillar introspection --apply-cost script,fast
```

Load `introspection-scoring.md`. Score the prompt on all 5 ARS dimensions. Output the score table and top 3 improvement suggestions. Use structured output per `scripts/schemas/score_output.json`.

---

## `/prism explain "<prompt>"`

**Model routing:** Fast model only.

Load `refraction-playbook.md`. Diagnose the prompt's weaknesses without rewriting it. List each issue with the specific rule that applies and the suggested fix. End with: "Run `/prism improve` to apply all fixes automatically."

---

## `/prism hook` (no sub-command)

**Model routing:** None — deterministic inference, zero model cost.

If the user types `/prism hook` with no `on`, `off`, or `status` argument, infer `on` as the default action. Print this notice before executing (must not be skipped):

> No sub-command supplied — inferring `hook on`. Run `/prism hook off` or `/prism hook status` to override.

Then proceed exactly as `/prism hook on` below.

---

## `/prism hook on`

**Model routing:** None — deterministic script.

```bash
python scripts/hook_installer.py --action on
```

The installer handles `{{PRISM_ROOT}}` substitution, idempotent JSON merge of `.claude/settings.json` (preserving non-Prism hooks), and writes `.github/hooks/prism_hooks.json` for Copilot. Output the installer's stdout verbatim.

## `/prism hook off`

**Model routing:** None — deterministic script.

```bash
python scripts/hook_installer.py --action off
```

Removes all Prism-managed entries from both hook config files. Output the installer's stdout verbatim.

## `/prism hook status`

**Model routing:** None — deterministic script.

```bash
python scripts/hook_installer.py --action status
```

Reports whether Prism hooks are active in `.claude/settings.json` and `.github/hooks/prism_hooks.json`. Output the installer's stdout verbatim.

## `/prism hook debug`

**Model routing:** None — reads a log file, zero model cost.

```bash
python scripts/hook_debug.py
```

Prints the last 20 entries from `.prism/hook-debug.log` as a formatted table showing: timestamp, event, raw stdin length, extracted prompt, whether the prompt was blocked, and any PII/injection findings. Use this to diagnose false positives — the `raw_repr` field shows exactly what Cursor sent to the hook.

To clear the log:
```bash
python scripts/hook_debug.py --clear
```

---

## `/prism patterns`

**Model routing:** Fast model.

```bash
python scripts/pattern_analysis.py --report --limit 500
```

Read `.prism/style-profile.json` (if it exists) and the pattern analysis report. Present:
- Top detected patterns with frequency and token cost
- Efficiency trend (improving/stable/declining)
- Suggestion: "Run `/prism patterns --apply` to create a persistent Cursor rule."

## `/prism patterns --apply`

**Model routing:** Fast model or none (if profile is fresh).

```bash
python scripts/pattern_analysis.py --cursor-rule
```

Write the output to `.cursor/rules/prism-personal-style.mdc`.
For Claude Code: add pattern guidance to `CLAUDE.md` in the project root (create if absent).
For Copilot: append pattern guidance to `.github/copilot-instructions.md`.

## `/prism patterns --reset`

**Model routing:** None.

Delete `.prism/prompt-log.jsonl` content and clear `.prism/style-profile.json`. Output: "✓ Pattern log cleared (X entries removed)."

---

## `/prism usage`

**Model routing:** None — reads files only.

```bash
python scripts/usage_log.py sessions
python scripts/usage_log.py summary
```

Format as a table showing last 30 sessions: date, platform, prism_tokens, session_tokens, overhead_pct. Include trend indicator (↑ ↓ →).

## `/prism usage --optimize`

**Model routing:** Fast model.

Read `usage-summary.json` and `.prism/component-sizes.json`. Suggest specific config toggles to reduce overhead. Example suggestions:
- "Stage 2 fires on every prompt but your recent scores average 87/100 → consider `/prism configure hook.stage2_lm_gate=false` (~200t/prompt saved)"
- "refraction-playbook.md is loaded on every command → it is only needed for improve and explain"

## `/prism configure [key=value]`

**Model routing:** None — pure JSON write.

Supported keys and their effect:

| Key | Default | Effect |
|-----|---------|--------|
| `hook.enabled` | true | Master hook toggle |
| `hook.stage2_lm_gate` | true | Disable LLM quality gate (~200t/prompt saved) |
| `hook.session_context_injection` | true | Remove sessionStart overhead (~50t/session saved) |
| `hook.log_prompts` | true | Disable prompt logging |
| `model_routing.mode` | platform | platform / local / capable |
| `overhead.alert_threshold_pct` | 20 | Alert when overhead exceeds this % |
| `overhead.alert_threshold_tokens` | 2000 | Alert when Prism tokens exceed this |

Read `.prism/prism.config.json` (or create from `scripts/prism_config_default.json`). Apply the change. Write back. Output: "✓ Set [key] = [value] in .prism/prism.config.json"

---

## Output Format Reference

### Why Log format
Each entry: `- [PILLAR] description [rule: ID, source: type]`

### ARS Score bands
- 90-100: Excellent — proceed as-is
- 75-89:  Good — minor suggestions only
- 60-74:  Needs work — specific improvements shown
- 40-59:  Poor — `/prism improve` strongly recommended
- 0-39:   Unusable — rewrite required

### Overhead note
Always append an overhead summary to `/prism improve` responses:
```
### Prism Overhead This Run: ~XXXt
Tip: /prism usage --optimize to see if any components can be trimmed.
```

---

## Knowledge Base Query Reference

Use `kb_query.py` to load only what is needed:

```bash
# All refraction rules for the current model
python scripts/kb_query.py --pillar refraction --model claude-4+

# Script-applicable rules only (no model call needed)
python scripts/kb_query.py --apply-cost script

# Specific rules by ID
python scripts/kb_query.py --ids ref-001,san-005,int-003

# Prior art-informed rules
python scripts/kb_query.py --source official --pillar sanitization
```

---

## Notes for Cursor (vs Claude Code)

- **No `context: fork`**: Run improve sequentially. Load one playbook at a time using `Read` tool.
- **No `additionalContext` injection**: Stage 1 can block but cannot add suggestions inline.
- **Hook format**: Cursor reads `.claude/settings.json` via third-party hooks compatibility.
- **Personal style rule**: `/prism patterns --apply` writes `.cursor/rules/prism-personal-style.mdc`.

For Claude Code-specific features (parallel sub-skills, `additionalContext`), see `.claude/skills/prism/SKILL.md`.
