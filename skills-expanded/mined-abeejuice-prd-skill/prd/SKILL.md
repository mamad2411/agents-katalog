---
name: prd
description: Reverse-engineer or design a PRD for any product, feature idea, or live URL. Always starts with /grill-me to clarify scope and intent. When a URL is given, uses /gstack and Puppeteer for a full site audit. Produces a structured PRD with feature overviews and numbered workflow narratives organised by module. Saves the final document to the Desktop. Use when asked to "write a PRD", "document this product", "reverse engineer this site", or "turn this idea into a PRD".
skills:
  - grill-me
  - gstack
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - mcp__puppeteer__puppeteer_navigate
  - mcp__puppeteer__puppeteer_screenshot
  - mcp__puppeteer__puppeteer_click
  - mcp__puppeteer__puppeteer_evaluate
  - mcp__puppeteer__puppeteer_fill
  - mcp__puppeteer__puppeteer_select
  - WebFetch
---

You are running the /prd skill. Your job is to produce a high-quality, jargon-free PRD that a product/tech team can use as a base of knowledge — covering features, flows, and intended functionality. Never skip a phase. Never batch questions.

---

## PHASE 1 — GRILL-ME (ALWAYS RUN FIRST, NO EXCEPTIONS)

Before doing anything else, check that the `/grill-me` skill is installed:

```bash
ls ~/.claude/skills/grill-me/SKILL.md 2>/dev/null && echo "installed" || echo "missing"
```

If missing, install it before continuing:

```bash
npx skills@latest add mattpocock/skills/grill-me --yes
```

Once confirmed, invoke the `/grill-me` skill and hand it this context so it knows what to interview the user about:

> "I am about to write a PRD. Grill me on: (1) what the input is — a live URL, a feature idea, a product concept, or a combination; (2) who the PRD is for and what they'll use it for; (3) what the scope is — full product or specific modules only; (4) which user roles to document; (5) whether flows should be organised by module first or role first; (6) whether to cover happy path only or include edge cases as well."

Do not proceed to Phase 2 until the `/grill-me` session is complete. After it finishes, confirm the agreed brief back to the user in one short paragraph before moving on.

---

## PHASE 2 — DEPENDENCY CHECK (URL inputs only)

If the user provided a URL, verify both tools are ready:

1. Check `/gstack` is installed:
```bash
ls ~/.claude/skills/gstack/SKILL.md 2>/dev/null && echo "installed" || echo "missing"
```
If missing, install it:
```bash
npx skills@latest add garrytan/skills/gstack --yes
```

2. Verify Puppeteer is reachable by navigating to the target URL with `mcp__puppeteer__puppeteer_navigate`.

3. Confirm both are ready before proceeding to the audit.

---

## PHASE 3A — FULL SITE AUDIT (URL inputs)

Use the `/gstack` browse skill to drive the audit — it is purpose-built for navigating, screenshotting, and extracting page state. Invoke it with the target URL and instruct it to map the entire site systematically.

Supplement `/gstack` with direct Puppeteer tool calls for deeper extraction:
- Full page text: `puppeteer_evaluate` → `document.body.innerText`
- All links: `document.querySelectorAll('a')` to discover new pages not visible in the nav
- Click every significant interactive element: buttons, dropdowns, modals, tabs, toggles, filters
- Screenshot every new state that results from an interaction

**Do not stop after the first page.** Keep a running mental list of all pages discovered and mark each as fully explored before moving on. A page is only "explored" when you have read its text, extracted its links, and clicked its interactive elements.

For each page and interaction, capture:
- Page title and URL
- Which user role it belongs to
- All features and sections visible
- All interactive elements and what they do
- Any AI-powered features and how they are triggered
- Navigation items, role badges, modals, filters, empty/loaded states

---

## PHASE 3B — IDEA INTERVIEW (no URL / concept inputs)

If no URL was provided, run a deeper interview to extract the full product vision. Ask one question at a time and provide your recommended answer for each:

1. Who are the primary users and what core problem does this solve for them?
2. Walk me through the single most important workflow — step by step, what does a user do?
3. Are there multiple user roles? What can each do that others cannot?
4. What are the key screens or sections of the product?
5. Are there any AI-powered features? What exactly do they do?
6. What is planned but not yet built?

Build the PRD entirely from the user's answers to these questions.

---

## PHASE 4 — WRITE THE PRD

Write the full PRD using the structure below. Plain language only — no technical jargon (no API, database, frontend, backend, component names, or framework references). Write as if explaining the product to an intelligent non-engineer.

```
# [Product Name] — Product Requirements Document (PRD)

> Purpose: [one line on why this PRD exists]
> Scope: [what is covered]
> Detail level: Happy path flows only / includes edge cases

---

## Platform Overview
[2–3 sentences: what the product is, who it serves, what problem it solves]

---

## User Roles
| Role | Description | Access |
|------|-------------|--------|
| [Role] | [What they do] | [What modules/areas they can access] |

---

## Module N — [Module Name]
**Who uses it:** [roles]
**What it is:** [one sentence describing the module's purpose]

### Feature Overview
- [bullet: feature 1]
- [bullet: feature 2]
...

### Workflow N.N — [Active description of what the user does]
1. [User action or system response]
2. [Next step]
...

[Repeat Workflow sections for each distinct flow in this module]

---

[Repeat the full Module section for every module discovered]

---

## Planned Features (Not Yet Live)
| Feature | Intended Purpose |
|---------|-----------------|
| [Feature] | [What it is meant to do] |

---

## Key Capabilities (Cross-Module)
| Capability | Where It Appears |
|-----------|-----------------|
| [e.g. AI content generation] | [Module name(s)] |
```

**Writing rules:**
- Every module gets a Feature Overview AND at least one numbered Workflow
- Workflow steps describe what the user does and what happens — not what the UI looks like
- Module-first organisation by default (unless user chose role-first in Phase 1)
- Happy path only unless the user requested edge cases in Phase 1
- Workflows are numbered: Module 1 Workflow 1.1, Module 2 Workflow 2.1, etc.

---

## PHASE 5 — SAVE TO DESKTOP

Once the PRD is fully written:

1. Ask the user: **"What would you like to name this file?"**
2. Use their answer exactly as given — do not change capitalisation, spacing, or add extensions.
3. Save to the Desktop:
```bash
cat > "/Users/apple/Desktop/[filename].md" << 'PRDEOF'
[full PRD content here]
PRDEOF
```
4. Confirm to the user: **"Saved as [filename].md on your Desktop."**
