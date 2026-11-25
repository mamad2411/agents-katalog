---
name: bundle-skills
description: Use this skill when the user wants to create, update, or plan a skill bundle CSV for the skillless project, especially prompts like "/bundle-skills frontend", "bundle skills for python", "make a react skill pack", "merge these skills into a list", or "find skills and create a category". This skill guides the agent through clarifying the bundle concept, splitting it into useful subgroups, using find-skills/skills.sh metadata, checking install counts and security audit risk, comparing against existing lists/*.csv files, asking whether to merge or create a new bundle, and producing alphabetically sorted CSV rows.
---

# Bundle Skills

This project stores skill bundles as CSV files under `lists/`. A bundle is a category file consumed by the `skillless`
CLI.

Use this workflow to help a user turn a loose request like `/bundle-skills frontend` into a reviewed, safe, sorted CSV
bundle.

## Repository conventions

- Bundle files live in `lists/<category>.csv`.
- CSV header is always:
  ```csv
  repo,skill_name,agents
  ```
- `repo` is a GitHub `owner/repo` or supported URL.
- `skill_name` is the skill to install. Empty means “install all skills from that repo”; use this only when
  intentionally bundling the whole repo.
- `agents` is space-separated, commonly `opencode claude-code codex`.
- Sort final CSV rows by `repo` alphabetically, then by `skill_name` for stable diffs.
- Verify the bundle with `./skillless list` and, when safe, `./skillless -n pack <category>`.

## Workflow

### 1. Interpret the user’s bundle idea

Extract the raw requested domain from the prompt.

Examples:

- `/bundle-skills frontend` → broad frontend bundle.
- `/bundle-skills react testing` → React-focused testing bundle.
- `/bundle-skills backend node` → Node/backend bundle.

Rewrite the idea into a generic intent and split it into subgroups. For broad topics, do not treat the first word as a
single bucket.

Example split for `frontend`:

- Core frontend engineering
- Frameworks such as React, Next.js, Vue, Angular, Svelte
- Styling and CSS systems such as Tailwind, design systems, animation
- Testing and browser automation
- Accessibility, UX, and performance

Keep the split practical. The goal is a useful bundle, not exhaustive taxonomy.

### 2. Confirm scope before searching deeply

Ask the user to confirm the interpreted idea and fill missing decisions that affect the search.

Ask only what matters. Typical questions:

- Bundle name: should this become `lists/<name>.csv`?
- Framework focus: generic, React/Next.js, Vue, Angular, backend-specific, etc.?
- Target agents: default to `opencode claude-code codex` unless the user wants fewer.
- Merge policy: if a related CSV already exists, should the final result merge into it or create a new bundle?

Recommended confirmation format:

```text
I read this bundle as: <generic summary>.
I would split it into: <subgroups>.
Proposed CSV: lists/<name>.csv.
Target agents: opencode claude-code codex.

Confirm, or tell me what to narrow/change.
```

Do not edit CSV files until the user confirms the plan.

### 3. Discover candidate skills

Use the local `find-skills` workflow first. Search each subgroup separately so broad requests do not miss
framework-specific skills.

Good searches:

```bash
npx skills find frontend
npx skills find react performance
npx skills find css tailwind
npx skills find accessibility
npx skills find playwright testing
```

Also check `https://skills.sh/` and the relevant `https://skills.sh/<owner>/<repo>/<skill>` pages for metadata not shown
by CLI search.

Important metadata limits:

- `npx skills find` usually surfaces skill reference, install count, and skills.sh URL.
- GitHub stars, first-seen date, and GEN/Socket/Snyk audit details are web-only on skills.sh pages or audit pages.
- Missing audit data means unknown risk, not safe.

### 4. Apply quality gates

Prefer high-signal skills. The default recommendation threshold is **2,000+ installs**.

Filtering guidance:

- Prefer `>= 2,000` installs.
- Usually skip `< 2,000` installs unless the user explicitly wants niche coverage or no higher-install option exists.
- Prefer reputable sources and official/vendor repos when quality is similar.
- Skip any skill where **two or more** audit sources indicate serious risk:
    - Gen Agent Trust Hub: High Risk / unsafe categories such as remote code execution or prompt injection.
    - Socket: many alerts, malware, suspicious package, or high-severity alerts.
    - Snyk: High or Critical risk.
- Treat Snyk Medium/Warn or one scanner warning as “needs explanation,” not an automatic reject.
- Treat no audit data as “unknown”; report it clearly and ask before including if the skill is otherwise useful.

### 5. Report candidates before editing

Present a bundle proposal and ask for confirmation.

The report must include:

- Subgroup/category.
- Repo and skill name.
- Install count.
- Risk summary from Gen, Socket, and Snyk when available.
- Source reputation notes such as official repo, GitHub stars, or maintainer signal when available.
- Include/skip recommendation and reason.

Use this table shape:

| Group | Repo                     | Skill                       | Installs | Gen  | Socket   | Snyk | Recommendation |
|-------|--------------------------|-----------------------------|---------:|------|----------|------|----------------|
| React | vercel-labs/agent-skills | vercel-react-best-practices |    100K+ | Pass | 0 alerts | Low  | Include        |

Then ask:

```text
Should I create a new bundle, merge into an existing CSV, or revise the candidate list first?
```

### 6. Check existing CSVs

Search `lists/*.csv` for related category files before writing.

Examples:

- `frontend` request: check `lists/frontend.csv`, `lists/react.csv`, `lists/typescript.csv`.
- `backend` request: check `lists/backend.csv`, `lists/nest.csv`, `lists/django.csv`, etc.
- `python` request: check `lists/python.csv`.

If a related file exists, summarize what it already contains and ask whether to merge or create a new bundle.

Do not silently overwrite existing bundles.

### 7. Write or update the CSV

After confirmation, create or update the target CSV.

Rules:

1. Preserve exactly one header: `repo,skill_name,agents`.
2. Deduplicate rows by `(repo, skill_name, agents)`.
3. Sort data rows alphabetically by `repo`, then `skill_name`.
4. Keep comments only if they explain bundle-specific choices.
5. Use the confirmed agent targets on every row.

Example:

```csv
repo,skill_name,agents
anthropics/skills,frontend-design,opencode claude-code codex
vercel-labs/agent-skills,vercel-react-best-practices,opencode claude-code codex
vercel-labs/skills,find-skills,opencode claude-code codex
```

### 8. Verify

Run these checks when possible:

```bash
./skillless list
./skillless -n pack <category>
```

For edits to shell scripts or CLI behavior, also run:

```bash
bash -n skillless scripts/install-skills.sh
```

Report exactly what changed and whether the user still needs to run a real install.

## Common outcomes

### New bundle

Use when no close existing CSV exists or the user wants a separate concept.

Output:

- New `lists/<bundle>.csv`.
- Candidate report kept in the conversation.
- Dry-run command: `./skillless -n pack <bundle>`.

### Merge into existing bundle

Use when the request extends an existing category.

Output:

- Updated existing `lists/<category>.csv`.
- Sorted and deduplicated rows.
- Summary of added, skipped, and rejected candidates.

### Plan only

Use when the user wants research before modifying files.

Output:

- Bundle idea summary.
- Subgroup split.
- Candidate table with install/risk metadata.
- Recommendation for create vs merge.

## Avoid these mistakes

- Do not trust CLI search output alone for risk reporting; audits are web-only when available.
- Do not include low-install or unknown-risk skills without explaining the tradeoff.
- Do not install skills while building a bundle unless the user explicitly asks.
- Do not overwrite related `lists/*.csv` files without asking whether to merge.
- Do not leave CSV rows unsorted; stable order matters for review.
