---
name: skill-selector
description: >-
  Selects and runs skills from installed skills based on user input: categorize
  requirements, map multiple requirement points to one or more skills (not
  limited to a single skill), fall back to find-skill / skills discovery when
  none fit, and perform a quick security check before use. Invoke via
  "/skill-selector" or when the user asks which skill to use, recommends a
  skill, or wants the agent to auto-pick skills for a task. Always use this skill
  when skill selection or recommendation is requested.
---

# Skill Selector

Selects and runs skills from installed skills based on user input. **Decompose and categorize** the user’s requirements first; **one task may need several skills** (each requirement point can map to its best skill). When multiple skills match a single point, list the top 5 with score and a brief conclusion for the user to choose from, then run the chosen skill(s). If nothing in the catalog fits, **use discovery** (`find-skill` / `npx skills find`) to locate and install a skill, then re-evaluate. **Before relying on a skill**, do a lightweight **security review** (see **4c**); do not execute if the review fails.

## Invocation

- **Slash command**: User invokes this skill by typing **`/skill-selector`** (or the platform equivalent for running a skill by name).
- This skill must be installed by the user; at run time the user enters the skill name (e.g. `/skill-selector`) to execute it.

## When to Use

- User explicitly asks which skill to use, or to recommend a skill.
- User describes a task and wants the agent to auto-pick and run the best matching skill.
- User invokes `/skill-selector` (or equivalent).

## Data Source

Read **available_skills** (or the equivalent list) from the current context. Each entry has `name`, `description`, and `fullPath`. Use only this information for matching and scoring; do not assume skills that are not listed.

## Execution Flow

### 0. Categorize Requirements (before scoring)

- Break the user’s request into **distinct requirement points** (e.g. “edit PDF”, “write marketing copy”, “set up A/B test”).
- For **each** point, independently pick the best matching skill(s) from **available_skills**. **Do not limit the overall answer to a single skill** when several points need different domains.
- Execution order: respect dependencies (e.g. product context before copy); otherwise follow user priority or a logical order.
- Output a short **plan**: requirement point → candidate skill(s) → whether user confirmation is needed for that point.

### 1. Understand User Intent

- **Explicit selection**: User asks to pick or recommend a skill → use the task description they give (or ask for it) as the match target **per requirement point** (see step 0).
- **Implicit selection**: User gives a task and wants "the best skill" to run it → use that task description as the match target, still **split into points** when the task is multi-faceted.

If the user only says "pick a skill" with no task, briefly ask: "What task or scenario do you want to accomplish?" then match against their reply.

### 2. Score Each Skill (0–100)

For each entry in **available_skills**, for **each requirement point** (when multiple points exist):

- Score relevance of its **description** (and name if needed) to that point’s match target.
- Consider: keyword/domain match, task type match, how well "when to use" in the description aligns with user intent; higher score for better fit.
- Score low (e.g. 0–30) for skills that are clearly irrelevant.

You do not need to output every score; use them internally to rank. When several points each need a different winner, you may output **one recommendation block per point** (or a compact table: point → top skill → score).

### 3. Decide and Output

Apply **Case A / B per requirement point** when the user has multiple points; for a single-point task, one pass is enough.

**Case A: Single clear winner (for that point)**

- Condition: Top score ≥ 80 and gap to second place ≥ 20.
- Action: State the recommendation concisely, then **list the selected skill by name** (see below), then proceed to "Run the selected skill(s)."

**Case B: Multiple close candidates (for that point)**

- Condition: Case A does not apply (e.g. top two scores are close, or top score < 80).
- Action:
  - List the **top 5** (by score, highest first). Each line: **Rank | skill name | score | one-line conclusion** (why it fits or does not).
  - Say: "Please choose which skill to use (e.g. reply with the number or skill name)."
  - After the user chooses, **list the selected skill by name** (see below), then proceed to "Run the selected skill(s)."

**Listing the selected skill(s)**

- As soon as a skill is chosen (either automatically or by user), output a clear line:
  - **Selected skill: \<skill name\>** (one line per chosen skill; if multiple points, prefix with the requirement point or use **Selected skills:** with a comma-separated list).
- Substitute the exact skill name from the list (e.g. **Selected skill: pdf**). Do this before reading or executing the skill.

### 4. Run the Selected Skill(s)

- After the user has chosen (or the single winner per point is chosen):
  - Use the **Read** tool to load each selected skill's SKILL file (its `fullPath`, usually `SKILL.md`).
  - Follow each skill's instructions for its **corresponding requirement point** (or the combined task if one skill covers all points).
- If the user only wanted a recommendation and not execution, stop after the recommendation or list; do not read or run another skill.

### 4b. When No Installed Skill Fits

- Say clearly that the current **available_skills** list has no strong match for one or more requirement points.
- **Discovery fallback**: run **`find-skill`** if available in the environment, or use the Skills CLI to search, e.g. **`npx skills find <keywords>`** (see [skills CLI](https://skills.sh/docs/cli)), identify a candidate repo/skill, then **`npx skills add <owner/repo>`** (or `--skill <name>` when needed) so it becomes available.
- After install, **re-run** categorization and scoring against the updated skill list for the unresolved point(s).
- If discovery still yields nothing appropriate, suggest manual search on [skills.sh](https://skills.sh) or rephrasing the task.

### 4c. Security Review

Before **first use** of a skill in this session (especially newly discovered or newly installed skills), do a **lightweight security check**:

- Prefer skills from **known sources**; for GitHub repos, skim README, file list, and obvious scripts for red flags (unexpected network exfiltration, shelling out to risky commands, obfuscated payloads, credential harvesting).
- If **anything looks unsafe**, do **not** execute that skill; warn the user and suggest removal or audit.
- If **no security issues** are found (or the skill is already vetted and unchanged in this session), proceed with execution. **Do not** create or maintain a separate review log file unless the user or project explicitly requires it.

## Output Format

- **Single recommendation (one requirement point)**: Short recommendation + reason (1–2 sentences), then **Selected skill: \<name\>**, then run it (after **4c** security review when executing).
- **Multiple requirement points**: Short plan: point → skill name → score (or “user to choose”); then **Selected skill(s):** as above for each point, then run in order (after **4c** for each skill when executing).
- **Multiple candidates (one point)**: Table or numbered list, each line: **Rank | name | score | one-line conclusion**; then prompt for choice. After choice: **Selected skill: \<name\>**, then run it.

Keep analysis brief; avoid long paragraphs.

## Top-5 List Example

```
Top 5 matching skills — please choose one (reply with number or skill name):

1 | pdf          | 92 | Strong match for "extract tables from PDF"; description covers PDF handling
2 | docx         | 65 | Handles documents but focused on Word; weaker for PDF
3 | xlsx         | 45 | Tables can be exported to Excel; not the primary use case
4 | copywriting  | 20 | Focused on copy; not relevant to extraction
5 | form-cro     | 15 | Form conversion; not relevant to this task
```

## Notes

- Only choose from the installed/available skill list in the current context (e.g. agent_skills) **unless** you are in the discovery path (step 4b); do not invent skill *names* without a real install source.
- **Multi-skill tasks** are normal: one skill per requirement point is preferred when domains differ; avoid forcing a single skill to cover unrelated concerns.
- If no skill fits after categorization, follow **4b** (find-skill / `npx skills find` + install) before giving up.
- Always complete **4c** before executing a skill, especially for newly installed or untrusted sources.
