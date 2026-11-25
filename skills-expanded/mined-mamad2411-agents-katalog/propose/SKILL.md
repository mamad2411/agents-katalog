---
name: propose-skill
description: Analyze session patterns and propose new skills. Use when Claude notices repeating workflows, when the skill-creation nudge fires, or when the user says "formalize this", "make this a skill", or "propose a skill". Reads session context to identify recurring tool sequences, command patterns, or file editing flows that could be automated.
disable-model-invocation: true
---

# Propose Skill

> **Best with the `multiplai-context` plugin.** Steps below read that plugin's runtime artifacts (`.multiplai/diary/` and `.multiplai/learnings/`). Without it, rely on the current conversation context alone.

Detect repeating patterns in the current session and draft a skill proposal.

---

## Step 1: Gather Session Context

Read these sources to understand what's been happening:

1. Today's `.multiplai/diary/` entry — session summaries and key actions
2. Recent `.multiplai/learnings/` files — patterns and observations from recent sessions
3. The current conversation context (already available)

Focus on: Which tool sequences recur? Which bash commands repeat? Which file types get edited in the same order? What workflows span multiple steps?

### Optional: `--from-session` — extract from a real trajectory

Diary entries and learnings are *summaries*. They record that a workflow
happened, not the exact commands, flag values, and dead ends it went through —
so a skill drafted from them reads plausibly and then fails on first use,
because the details it needed were the ones summarization dropped.

When the user says "make a skill out of what we just did", or passes
`--from-session [<id-prefix>]`, read the raw transcript instead:

```
ls -t "$CLAUDE_CONFIG_DIR/projects/$(pwd | tr '/' '-')"/*.jsonl | head -5
```

The newest file is the current session. Read the transcript and pull out the
**actual trajectory**: every tool call in order, with its real arguments, and
the result that made the next step necessary.

Then split what you found into two piles — this is the whole point of the mode:

| | **Stable step** | **Judgment point** |
|---|---|---|
| Looks like | Same command, same flags, every time | The decision that *chose* the command |
| Example | `uv run collect_costs.py && costs_report.py --by skill` | Which `--by` dimension answers the question being asked |
| Goes in the skill as | A literal command to run | A criterion for deciding, never a hardcoded answer |

**The rule:** a step is stable only if you saw it done the *same way* for a
*different input*. One occurrence is an anecdote — writing it into the skill as
a fixed step bakes this session's specifics into every future run. If you only
have one trajectory, write the step as a judgment point with the observed case
named as an example.

Record the dead ends too. The command that failed, and why, is often the most
valuable line in the skill — it is the part that cannot be reconstructed from
the successful path alone.

---

## Step 2: Identify the Pattern

Look for:
- **Tool chains**: Same sequence of Read → Edit → Bash happening repeatedly
- **File templates**: Same structure being created for different inputs
- **Multi-step workflows**: Procedures with 3+ steps that follow a consistent order
- **Domain knowledge**: Information that gets re-explained or re-discovered

Skip patterns that:
- Are already covered by an existing skill (check `$CLAUDE_CONFIG_DIR/skills/`)
- Are too simple to warrant a skill (single command, one-step action)
- Are one-off procedures unlikely to recur

---

## Step 3: Draft the SKILL.md

Follow the format from `skill-creator/SKILL.md`:

```yaml
---
name: skill-name
description: Clear description including when to use and trigger phrases.
---
```

Body should include:
- Step-by-step workflow (imperative form)
- Any scripts that should be bundled (propose them, don't write yet)
- Reference files needed
- Expected inputs and outputs

**Keep it under 200 lines.** Concise > comprehensive.

---

## Step 4: Present for Approval

Show the draft to the user with:

```
I noticed a repeating pattern: [describe the pattern in 1-2 sentences]

Here's a skill proposal:

[draft SKILL.md content]

Target path: $CLAUDE_CONFIG_DIR/skills/{name}/SKILL.md

Should I create this skill? (yes / modify / no)
```

**NEVER write the skill file without explicit "yes" from the user.**

---

## Step 5: Write to a Draft Location

If approved, write the skill to a **draft** directory first — not to
`$CLAUDE_CONFIG_DIR/skills/`:

1. Create `/tmp/skill-draft/{name}/SKILL.md` with the approved content
2. If scripts were proposed, create them in `/tmp/skill-draft/{name}/scripts/`

Nothing is installed yet. Step 6 decides whether it gets to be.

---

## Step 6: Promotion Gate — run it, don't vouch for it

A skill that is written is not a skill that works. Until this gate existed, the
first time anyone found out a bundled script had a bad import or a `--help`
that raised was mid-task, days later, with the authoring context gone. Saying
"the script looks correct" is not evidence; running it is.

**Run the deterministic half:**

```
uv run --script "${CLAUDE_PLUGIN_ROOT}/skills/skill-creator/scripts/promote_skill.py" /tmp/skill-draft/{name}
```

It checks frontmatter (required keys, known `model`/`effort` values) and
executes every bundled entry point with `--help`, expecting exit 0.

- **Exit 0** → proceed to step 7.
- **Exit 1** → fix what it reports and re-run. Do **not** install a skill that
  fails the gate, and do not report it as ready. If a failure is genuinely not
  fixable, say so explicitly and let the user decide — don't quietly install.
- **`[warn]` lines** → not blocking, but read them. A "could not import X"
  warning means the script has an undeclared dependency and will fail on any
  machine that hasn't pre-installed it; add PEP 723 inline metadata.

**Then judge the half a script can't.** `promote_skill.py` deliberately makes no
judgment about whether the skill is a *good idea*. You do, before installing:

- **Does it duplicate an existing skill?** List the installed skills and check.
  Two skills with overlapping descriptions means neither routes reliably.
- **Is the description a real trigger?** It is the only thing routing sees.
  "Helps with data" routes on nothing.
- **Would a plain instruction in CLAUDE.md do the job?** If the workflow is
  three sentences with no scripts and no branching, it probably would.

If any of those is a "no", go back to step 3 rather than installing.

---

## Step 7: Install

Only after step 6 passes:

1. Move `/tmp/skill-draft/{name}/` to `$CLAUDE_CONFIG_DIR/skills/{name}/`
2. Add a trigger line to CLAUDE.md under "Skill Triggers" if the pattern needs
   explicit routing
3. Report what the gate actually checked — not "created and validated" when only
   frontmatter was checked

---

## Guidelines

- One skill per pattern. Don't bundle unrelated workflows.
- Match existing skill conventions — look at 2-3 existing skills for style.
- Prefer high-freedom instructions over rigid scripts unless the workflow is fragile.
- The description field is the primary trigger — make it comprehensive with exact phrases.
