---
name: find-npm-package
description: Search npm packages by functionality using the npm registry API, iteratively refining the query until the user finds the right one. Covers JavaScript and TypeScript packages only — does not cover pip, cargo, gems, or other package registries. Use when user wants to find an npm package, node module, or JavaScript/TypeScript library for a specific purpose, or says things like "find me an npm package for X", "is there a node module that does Y", or "recommend a JS library for Z".
---

# npm Package Finder

## Quick Start

Extract 2–4 keywords from user's description, then search:

```bash
# With jq (preferred)
curl -s "https://registry.npmjs.org/-/v1/search?text=<keywords>&size=10" \
  | jq -r '.objects[] | "- **\(.package.name)** — \(.package.description // "(no description)") (score: \(.score.final * 100 | round)/100 · updated \(.package.date[:7]))\n  https://www.npmjs.com/package/\(.package.name)"'

# Fallback: python3
curl -s "https://registry.npmjs.org/-/v1/search?text=<keywords>&size=10" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for obj in data['objects']:
  p = obj['package']
  score = round(obj['score']['final'] * 100)
  updated = p['date'][:7]
  print(f\"- **{p['name']}** — {p.get('description', '(no description)')} (score: {score}/100 · updated {updated})\")
  print(f\"  https://www.npmjs.com/package/{p['name']}\")
"
```

Then fetch weekly downloads for the top 5 results:

```bash
# Replace <pkg> with each package name
curl -s "https://api.npmjs.org/downloads/point/last-week/<pkg>" \
  | jq -r '.downloads'
```

Append `· Nk/week` to each of the top 5 results.

## Workflow

1. **Extract keywords** — pick nouns/verbs most specific to the desired functionality
2. **Search** via npm registry API
3. **Fetch weekly downloads** for top 5 packages
4. **Present results** as list (see Output Format)
5. **Ask** with choices:
   > "Did any of these match?
   > A) Wrong runtime (need browser-only / Node-only / universal)
   > B) Too generic — need something more specific
   > C) Wrong category (utility / framework / CLI)
   > D) Let me describe what I need
   > E) Show more results"
6. **Refine** based on answer → repeat from step 2
7. **No limit** on rounds — keep going until user confirms they found it

## Refinement Strategy

| Choice | Action |
|--------|--------|
| A | Append "browser" / "node" / "universal" to query |
| B | Add more specific terms to query |
| C | Append "library" / "cli" / "framework" to query |
| D | Re-extract keywords from user's new description |
| E | Re-run with `size=20`, show next 10 results |

## API Options

```bash
# Basic search (sorted by npm score by default)
curl -s "https://registry.npmjs.org/-/v1/search?text=<query>&size=10"

# More results
curl -s "https://registry.npmjs.org/-/v1/search?text=<query>&size=20"

# Offset for pagination
curl -s "https://registry.npmjs.org/-/v1/search?text=<query>&size=10&from=10"

# Weekly downloads
curl -s "https://api.npmjs.org/downloads/point/last-week/<pkg>"
```

## Output Format

Present results as:

- **package-name** — description (score: N/100 · Nk/week · updated YYYY-MM)  
  https://www.npmjs.com/package/package-name

Sort by npm score descending (API default). Weekly downloads on top 5 only. If description is empty, note "(no description)". Format `date` as `YYYY-MM`.
