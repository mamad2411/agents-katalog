---
name: person-intake
description: "Onboards a person (a new collaborator, client, or unfamiliar name) into persistent context in one pass: checks existing memory, researches their public web presence, searches your projects and your own GitHub account for prior work with them, harvests the brand tokens of anything already built for them, and writes a contact memory file. Use when the user says look up X, who is X, find info on X, or is about to start work for someone Claude has no record of."
user-invocable: false
---

# Meet: bring a person into persistent context

For when the user mentions someone Claude does not know yet. Build the picture once and save it, so later sessions never research the same person twice. The step that pays off most often is finding earlier work you already did for them: it turns a cold start into continuity.

## When to use

| Use meet when | Use something else when |
|---|---|
| "look up X", "who is X", "find info on X" | X is a coworker in your company directory: look them up there |
| You are about to pitch or build for a person | You need a deep investigation of an organization: that is research, not onboarding |
| Memory has no `contact_<name>.md` yet | You only need a fact already in memory: read it |

## Settings

Read the settings file if it exists: `cat "${SESSIONFLOW_CONFIG:-$HOME/.claude/sessionflow.json}" 2>/dev/null`.

- `memory_dir` (env `SESSIONFLOW_MEMORY_DIR`): where the contact file goes. Default: the project's auto memory folder, else `<project root>/.claude/memory/`.
- `meet.github_owner`: the GitHub user or org to search for prior work. Default: the logged-in account, `gh api user --jq .login`.
- `meet.search_paths`: local folders to search. Default: the current project root, plus `~/projects` when it exists.

## Step 1: memory check, always first

```bash
ls "<memory_dir>" | grep -i -e "<first name>" -e "<last name>"
grep -ril "<full name>" "<memory_dir>"
```

If a `contact_<name>.md` exists, read it and stop, unless the user asked for a refresh or the file is old enough that the facts may have moved.

## Step 2: web research

Search for the person with whatever hint the user gave (profession, company, city): `"<full name> <hint>"`. If results are thin, search known brands, employers, books, or domains. For someone who works mainly in another language, search in that language too.

## Step 3: read their canonical presence

Fetch the two or three most meaningful sources (personal site, business site, the platform where they publish) and ask each fetch for: who they are professionally, what they offer (services, products, programs), pricing if listed, the visual brand (colors, typography, tone), and the site's main navigation. Triangulate; a fact from one source only is marked as such.

## Step 4: local recon

Search your own storage for earlier mentions, with every alias learned so far:

```bash
grep -ril -e "<name>" -e "<brand>" "<memory_dir>"
find <search paths> -maxdepth 4 \( -iname "*<name>*" -o -iname "*<brand>*" \) -not -path "*/node_modules/*" 2>/dev/null | head -20
grep -ril -e "<name>" -e "<brand>" <search paths> --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null | head -20
```

## Step 5: GitHub recon

Prior work often lives in your own repositories. With `gh` authenticated:

```bash
gh search repos "<name or brand>" --owner <owner> --limit 50
gh search code "<name or brand>" --owner <owner> --limit 30
gh api repos/<owner>/<repo>/contents --jq '.[] | "\(.type)\t\(.name)"'   # structure of a likely match
```

If the name maps to a public GitHub user, `gh api users/<login>` gives their public profile.

When a repo built for them turns up, read it through the API (no clone needed) and harvest:

- `package.json` or `manifest.json`: name, theme color, description
- design tokens (`variables.css`, a tokens file, a Tailwind config): palette, typography, spacing
- `index.html` head: fonts, meta description
- `README.md`: purpose, status, who it was for

## Step 6: save to memory

Write `<memory_dir>/contact_<lastname>_<firstname>.md`:

```markdown
---
name: <Full name>
description: <one line: profession, location, why they matter for your work>
type: person
---

**Who**: <bio summary, location, public contact channel if they list one>

**Brands and properties**: <their businesses, sites, products>

**Offerings**: <table: name | format | price, when they sell something>

**Brand voice and visual identity**: <tone words, palette, typography, imagery>

**Sources** (looked up <YYYY-MM-DD>): <urls>

**Prior work with them**: <what was built, repo url, status, brand tokens established>

**Current context**: <what is being built for them now, and why>

**How to apply**: <what to remember when resuming work for this person>
```

Then add one line to `<memory_dir>/MEMORY.md`: `- [<Full name>](contact_<lastname>_<firstname>.md): <role, why they matter>`.

If a prior repo was found, write a second file, `<lastname>_brand_<repo>.md`, with the design tokens, and index it too.

## Step 7: report

Keep it tight:

- who they are (one or two sentences)
- what they offer (highlights)
- whether prior work exists, and its brand spine if so
- memory files written (absolute paths)
- sources, as a list of links (required whenever web research was used)

## When nothing turns up

Say so plainly. Do not fabricate. Ask the user what they know (how they met, shared projects, why the name came up), then save what is known and mark the rest unknown.

## Privacy rules

- Save only what is material to working with the person. No home addresses, age, family details, or personal phone numbers unless the person publishes them for business contact and they matter to the work.
- Do not write memory for a passing mention; only for people who will recur. If unsure, ask.
- Do not fabricate sources, employers, books, or schedules. If a fetch did not surface a fact, leave it out.
