---
description: Create or harden an agent skill with yao-meta-skill using a short grill plus quickstart
argument-hint: "[skill-name] [workflow/job]"
---
Use the local Yao Meta Skill to turn a repeated workflow into a reusable agent skill.

Yao root: `~/work/yao-meta-skill`

User-provided arguments: `$@`

## Intent

Help me create or improve a skill without making me remember the Yao CLI details. Use a
short grill first, then run `yao.py quickstart` through `uv run` with the collected fields.

Default to Chinese unless I explicitly ask for another language.

## Argument parsing

- If `$1` looks like a slug (`^[a-z0-9][a-z0-9_-]*$`), treat it as the skill name.
- Treat `${@:2}` as the rough workflow/job brief.
- If no valid skill name is provided, infer a short slug from the job and confirm it.
- If no job brief is provided, ask for it first.

## Workflow

1. Confirm `~/work/yao-meta-skill` exists and resolve it to an absolute path at runtime.
2. Read `SKILL.md` from that directory before invoking the CLI.
3. If needed, read `references/intent-dialogue.md` for Yao's intent-capture style.
4. Do a short B+C flow:
   - **C: tiny design grill** — confirm whether this should be a skill at all.
   - **B: semi-automatic command** — once the brief is clear, run `quickstart`.
5. Do not duplicate the whole Yao process in the conversation. Let `yao.py quickstart` own the
   intent confidence gate, reports, and generated package structure.

## Short grill rules

Ask only the minimum missing questions before running the command. Ask one question at a time.
For each question, include:

```text
问题：...
我的建议：...
为什么：...
```

Resolve these fields, using the arguments when possible:

- skill name
- repeated job / workflow
- real inputs people will give the skill
- primary output the skill should hand back
- exclusions or local constraints
- mode / archetype
- output directory

Defaults:

- mode/archetype: `scaffold` for personal or exploratory skills
- mode/archetype: `production` when other people will reuse it soon
- mode/archetype: `library` for shared infrastructure skills
- mode/archetype: `governed` for high-trust, policy-sensitive, or release-critical skills
- output directory: if the current repo has `.pi/skills/`, use its absolute path; otherwise ask

Before creating files, state the resolved command and output directory briefly. Respect the
current Pi workflow guards; in direct Act mode, proceed after the short confirmation.

## Command shape

Run the command from the Yao repo, using absolute paths for output directories:

```bash
cd ~/work/yao-meta-skill && \
uv run python scripts/yao.py quickstart \
  --name "<skill-name>" \
  --job "<repeated job>" \
  --primary-output "<primary output>" \
  --real-input "<real input>" \
  --description "<trigger-oriented description>" \
  --output-dir "<absolute output directory>" \
  --mode "<scaffold|production|library|governed>" \
  --archetype "<scaffold|production|library|governed>" \
  --local-constraint "<constraint>"
```

Only include repeated `--real-input`, `--local-constraint`, `--external-reference`, or
`--user-reference` flags when they are actually known.

## After quickstart

1. Parse the JSON result if present.
2. Summarize the generated skill root and key reports:
   - `reports/skill-interpretation.html`
   - `reports/skill-overview.html`
   - `reports/review-studio.html`
   - `reports/review-viewer.html`
   - `reports/iteration-directions.md`
3. Run the smallest sensible validation, usually:

```bash
cd ~/work/yao-meta-skill && \
uv run python scripts/yao.py validate "<generated-skill-root>"
```

4. If validation fails, report the exact failure and the smallest next fix. Do not guess.
5. End with:
   - created/updated files
   - selected mode/archetype
   - validation result
   - recommended next review action

## Safety and scope

- Do not create a skill for one-off work with no repeated use or reusable output contract.
- Do not fabricate evidence, benchmarks, telemetry, or human review.
- Do not copy private customer content into generated examples unless I explicitly approve it.
- Do not paste raw CLI JSON unless I ask for it; provide a readable summary.
