---
name: compile-skill
description: Use this skill to design and scaffold a new Claude skill from scratch — with explicit step classification (code/inference/hybrid), inference call contracts, and code-first defaults. Trigger when the user wants to author a new skill, build a skill, compile a skill, create a new agent skill, or types "/compile-skill". Distinct from skillify — this is design-from-scratch, not capture-from-session.
---

# Compile Skill

A skill that designs and builds other skills, applying the rules in
`~/.claude/rules/skills.md`. Maximizes code paths, minimizes inference,
declares contracts on every inference call.

The flow is **spec → build**: compose a complete specification with all
file contents inline, then hand it to `build.py` which deterministically
writes the skill, validates it, and smoke-tests its scripts.

## Gotchas

- **Read `~/.claude/rules/skills.md` first.** This skill enforces those
  rules. If they're not in context, load them before proceeding.
- **Save location defaults to the current working directory.** New skill
  goes to `./<skill-name>/`. Do NOT default to `~/.claude/skills/` — that
  is a deliberate change from the global pattern, chosen so the user
  controls placement by where they invoke from.
- **The spec contains everything.** Reference file content, script
  source, eval entries — all inline in the spec JSON. The builder is
  not a stub generator; it is a translator from spec to disk.
- **One inference call per concern.** When decomposing or authoring
  reference files, resist bundling. Each role's reference is its own
  inference call. Each script is its own.
- **The builder follows its own rules.** `build.py` and `validate.py`
  are code-only. No inference creep into them — if you need judgment,
  it belongs upstream in spec composition, not inside the build.
- **Quality is a spec concern, not a build concern.** `build.py`
  guarantees the skill files are written, validate, and the scripts
  run with `--help`. It does NOT guarantee the compiled skill produces
  high-quality output. That's a separate (future) auditor concern.
- **`scaffold.py` is legacy.** It produces a skeleton + script stubs and
  expects the user to hand-author content afterward. Use `build.py` for
  any new compile that has the spec content available upfront.

## Steps

### Step 1: Intake (inference)

Issue a single `AskUserQuestion` call with 3 questions:

1. **What does this skill do?** — one-line user-facing description
2. **What triggers it?** — real user phrases that should activate it
3. **Any tools or MCPs it needs?** — Bash, Read, Notion MCP, etc.

Keep it light. Don't round-by-round. Gather enough to propose a design.

### Step 2: Spec composition (inference)

Compose the complete spec. The spec covers:

- **identity** — name (kebab-case), description (must contain "use this
  skill" or "use when" or "trigger" per the validator)
- **gotchas** — highest-signal failure modes and environment-specific
  facts. Lead with these per skills.md §5.
- **steps** — atomic pipeline steps. Each gets:
  - **n, name, type** (`code` | `inference` | `hybrid`)
  - **rationale** — one sentence on why this type
  - **contract** (inference/hybrid only) — input, output, justification
    for why code can't handle this
  - **script** (code/hybrid only) — relative path, e.g. `scripts/foo.py`
- **files** — every file the skill needs, with `content` inline:
  - References (`references/*.md`) — sub-agent prompts, role files,
    checklists. One concern per file.
  - Scripts (`scripts/*.py`) — full source. Set `kind: "script"` so the
    builder chmods them executable and runs `--help` as a smoke check.
  - Optional: exemplars, bar documents, failure-mode maps, anything
    else that lives in the skill directory.
- **evals.trigger** — `should_trigger` and `should_not_trigger` arrays
  with `prompt` + `rationale`. Aim for 10 each. The most valuable
  should-not-trigger cases are near-misses sharing keywords with the
  trigger.

Apply skills.md §6 throughout: **code-first default**. When in doubt,
code. Write reference files tightly — they live in the body's
progressive-disclosure tier and the orchestrator pays for them on
every invocation.

### Step 3: Approval gate (inference + AskUserQuestion)

Present the proposed design — name, description, step list with types
and rationales, file list with paths and one-line summaries, eval
counts. Issue one `AskUserQuestion`:

- **Approve, revise, or cancel?**

If revise, iterate on Step 2 with the user's feedback. If cancel, exit.

### Step 4: Build (code)

Write the approved spec to a temp file, then run:

```bash
python3 ~/.claude/skills/compile-skill/scripts/build.py \
  --spec /tmp/<skill-name>-spec.json \
  --out ./<skill-name>/
```

`build.py` is deterministic:

- Validates spec structure (kebab-case name, required fields, no
  path traversal in file paths)
- Renders `SKILL.md` from identity + gotchas + steps
- Writes every file in `files[]`; chmods `kind: "script"` files
- Writes `evals/trigger.json` from `evals.trigger`
- Runs `validate.py` on the produced `SKILL.md`
- Runs `--help` on every script as a smoke check
- Returns a JSON report with `all_checks_passed: true|false`

Exit code 0 = built and all checks passed. 1 = built but some check
failed (validator errors or script smoke failure). 2 = spec invalid
or IO error.

Use `--dry-run` to preview the file list without writing.

### Step 5: Report (code)

Surface to the user:

- Path where the skill was saved
- Step count + type breakdown
- Validator result (errors / warnings from `validate.py`)
- Script smoke-check results (which scripts ran `--help` cleanly)
- Next steps: smoke-test the skill on one real input, edit any reference
  files that need iteration, copy to `~/.claude/skills/` if it should
  be globally invocable

## Spec format (v2.0)

```json
{
  "spec_version": "2.0",
  "identity": {
    "name": "kebab-case-name",
    "description": "Use this skill when..."
  },
  "gotchas": ["...", "..."],
  "steps": [
    {
      "n": 1,
      "name": "Step name",
      "type": "code|inference|hybrid",
      "rationale": "Why this type",
      "script": "scripts/foo.py",
      "contract": {
        "input": "schema description",
        "output": "schema description",
        "justification": "why code can't handle this"
      }
    }
  ],
  "files": [
    {"path": "scripts/foo.py", "content": "...", "kind": "script"},
    {"path": "references/role.md", "content": "..."}
  ],
  "evals": {
    "trigger": {
      "should_trigger": [{"prompt": "...", "rationale": "..."}],
      "should_not_trigger": [{"prompt": "...", "rationale": "..."}]
    }
  }
}
```

`script` is only required on code/hybrid steps. `contract` is only
required on inference/hybrid steps. `kind` defaults to `static` if
omitted; set `script` to get `chmod +x` plus `--help` smoke.

## Self-hosted

This skill follows its own rules. Step type breakdown:

| Step | Type |
|------|------|
| 1. Intake | inference |
| 2. Spec composition | inference |
| 3. Approval gate | inference |
| 4. Build | code |
| 5. Report | code |

3 inference, 2 code. **Step 2 (spec composition) is the load-bearing
inference step** — every reference file and every script's source has
to be authored here. Quality of the compiled skill is bounded by the
quality of this step. A future "specifier" skill may take this work
over with explicit quality-target articulation, failure-mode mapping,
and exemplar-grounded reference authoring; for now Step 2 is best
effort by the orchestrator.

## Legacy

`scripts/scaffold.py` produces a skeleton + script stubs and is kept
for backwards compatibility with old specs. Do not use it for new
compiles — it forces a hand-authoring round after scaffolding that
`build.py` makes unnecessary.
