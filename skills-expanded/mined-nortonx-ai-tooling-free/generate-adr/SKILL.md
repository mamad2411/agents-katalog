---
name: generate-adr
description: "Scaffold an Architecture Decision Record (Nygard format) in docs/adr/ with auto-numbering, status lifecycle, and supersedes cross-linking. Args: <decision title>"
argument-hint: "<decision title>"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`<decision title>`

- Required. About 7 words describing the decision; the interview asks for it (Q1) but you can prefill via the arg.
- **Examples**: `/generate-adr Adopt Lefthook in place of Husky`, `/generate-adr Switch primary database to PostgreSQL`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Generate ADR: $ARGUMENTS

Create an Architecture Decision Record (ADR) in Michael Nygard's canonical 2011 format. ADRs are short, typically one page, and record a single architectural decision: its context, the decision itself, and its consequences. Detect the local ADR convention, interview the user one question at a time, draft an ADR that matches their team's existing style, and write it to disk only after explicit approval.

ADRs document decisions, not aspirations. The user provides the substance; this skill scaffolds structure and enforces brevity. Never pad empty sections with "TBD"; omit them entirely.

## Step 1: Orient

Probe the working directory for an existing ADR location, in this order:

1. `docs/adr/`: Nygard recommendation, the most common convention.
2. `docs/architecture/decisions/`: corporate / monorepo convention.
3. `doc/adr/`: Linux-kernel-style.
4. `adr/` at repo root: rare but valid.

- Exactly one exists: use it.
- Multiple exist: ask which to write to.
- None exist: propose `docs/adr/` and tell the user you will bootstrap it at write-time, including an index README.

List existing ADRs by globbing `<dir>/[0-9][0-9][0-9][0-9]-*.md`. Parse the largest 4-digit prefix; the next ADR number is `max + 1`, zero-padded to 4 digits. Never gap-fill; gaps reflect deleted or rejected drafts and are part of the history.

If at least one ADR exists, read the highest-numbered one as a tone reference so the new ADR matches the team prose style (terseness, header casing, language).

Report in one sentence: detected directory, count of existing ADRs, next number, and the reference ADR (if any).

## Step 2: Interview

Ask each question **one at a time, in order**. Every question ends with this exact footer:

> *Reply with your answer, `skip` to leave this section blank, `stop` to finalize with what we have, `auto` to let me propose a draft from prior answers, or `learn <concept>` if you want me to explain a term first.*

Response handling:
- `stop`: jump to Step 3 with whatever has been gathered. Do not ask remaining questions.
- `skip`: leave the section empty. It will be **omitted** from the file.
- `auto`: draft the section from prior answers and the reference ADR. Show the draft, ask for approval, then continue.
- `learn <concept>`: invoke the `/learn` command on `<concept>`, then re-ask the same question.

**Q1. Decision title.** In about 7 words: what is being decided? Example: "Adopt Lefthook in place of Husky", "Switch primary database to PostgreSQL".

**Q2. Status.** Which lifecycle state applies?
- `Proposed`: under discussion, not yet decided.
- `Accepted`: decided and in effect.
- `Deprecated`: no longer recommended; nothing replaces it.
- `Superseded by ADR-NNNN`: a newer ADR replaces this one.

Today's ISO date (YYYY-MM-DD) will be appended automatically.

**Q3. Supersedes an existing ADR?** Does this ADR replace one already in the directory? Reply with the predecessor 4-digit number (e.g., `0003`) or `no`. If yes, the predecessor `## Status` line will be rewritten to `Superseded by ADR-NNNN, <today>` so future readers do not mistake it for current.

**Q4. Context.** In 3-5 sentences: what situation forces a decision? Describe the constraints, the pain, and any measurable signals: team size, performance numbers, deadlines, compliance asks. Describe the *problem*, not the solution. Avoid marketing language ("robust", "scalable", "best-in-class"); those words do not help future readers.

**Q5. Decision.** State it in one declarative sentence: `We will <do X>.` Add 1-2 sentences of scope or how-to if needed. Do not justify here; justification belongs in Consequences.

**Q6. Consequences.** List concrete +/- outcomes. Format: lines starting with `+` for gains, `-` for costs, one per line. Be honest about the downsides: an ADR with only `+` bullets is a sales pitch, not a decision record. `auto` proposes a starter list grounded in Q4 + Q5; you confirm or edit.

**Q7. Alternatives considered.** List rejected options, each with a one-line reason. Format: `- <option>: <why rejected>`. `skip` is acceptable for decisions with no serious alternatives, but flag this; most non-trivial decisions had at least one alternative worth recording.

## Step 3: Assemble

Compose the ADR in-memory using exactly this template:

```markdown
# ADR-NNNN: <Title from Q1>

## Status
<Q2 status>, <today, YYYY-MM-DD>

## Context
<Q4 prose>

## Decision
<Q5 prose>

## Consequences
+ <gain>
+ <gain>
- <cost>
- <cost>

## Alternatives considered
- <option>: <why rejected>
- <option>: <why rejected>
```

Filename: `<dir>/NNNN-<kebab-case-title>.md`. Sanitize the title: lowercase, strip punctuation, replace spaces with hyphens, collapse repeats.

**Formatting rules:**
- Section order is fixed: Status -> Context -> Decision -> Consequences -> Alternatives considered. Never reorder.
- Omit sections that were `skip`ped; never substitute "N/A", "(none)", or "TBD".
- No emojis. No horizontal rules (`---`). No intro prose above the `# ADR-NNNN:` title. No trailing summary.
- No sub-headings beyond H2. ADRs are meant to be scannable on one screen; extra hierarchy buries the decision.
- Bold/italic only for emphasis on a single key term, never on whole sentences.

If the rendered ADR exceeds ~80 lines, warn the user that the decision may be too big for a single ADR and worth splitting. Offer to write it anyway.

Show the full rendered markdown and ask:

> *Write to `<target-path>`? Reply `yes`, `edit <section>` to revise (status / context / decision / consequences / alternatives), or `stop` to abort without writing.*

On `edit <section>`, re-ask the corresponding question, regenerate the preview, ask again.

## Step 4: Write

On `yes`:

1. **Create the directory** using the runtime file/directory creation tool or platform command if it does not exist.
2. **Write the new ADR file** with the runtime file writing tool.
3. **If Q3 named a predecessor**: read that file, replace its `## Status` line with `Superseded by ADR-NNNN, <today>`, and save back. Without this step, the predecessor still appears `Accepted` and future readers will trust stale guidance.
4. **Maintain the index README** at `<dir>/README.md`:
   - If it exists with a table of ADRs, append a row.
   - If it does not exist (bootstrap case), create it from this template:
     ```markdown
     # Architecture Decision Records

     | # | Title | Status | Date |
     |---|-------|--------|------|
     | [ADR-0001](0001-<slug>.md) | <Title> | <Status> | <Date> |
     ```
   - Sort rows by ADR number ascending. When a predecessor status changes, update its row too.
5. **Confirm in one line**: written path, plus (if applicable) "updated ADR-NNNN status" and "index updated".

On `stop`: one-line confirmation that no file was written. Do not retry unless asked.

## Guardrails

- Never invent context, alternatives, metrics, or stakeholders that are not grounded in user answers. When uncertain, ask or `skip`: do not guess.
- Never overwrite an existing ADR file. If `NNNN-<slug>.md` already exists, increment to the next free number and inform the user.
- Do not mention this skill, the interview process, or `$ARGUMENTS` inside the generated ADR.
- Do not auto-touch the repo `CLAUDE.md` or top-level `README.md`. An ADR documents itself; mixing it into project-memory files creates noise.
- ADRs are historical records. Once accepted and committed, content should be immutable; only the status transitions (Accepted -> Deprecated, Accepted -> Superseded). Do not offer to "fix" the content of past ADRs.
- If the user asks a question about Claude Code itself rather than ADR content, point them to `/help`.
