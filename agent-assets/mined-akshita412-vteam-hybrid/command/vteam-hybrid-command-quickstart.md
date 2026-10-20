<!-- agent-notes: { ctx: "fast 5-min onboarding, skips full kickoff ceremony", deps: [CLAUDE.md, .claude/commands/kickoff.md, docs/methodology/personas.md], state: active, last: "pat@2026-03-21" } -->
Quick-start this project: $ARGUMENTS

This is the fast path — get from template to working code in ~5 minutes. Use `/kickoff` instead if you want full discovery with architecture debate, sacrificial concepts, and board setup.

---

## Phase 0: Template Cleanup

If this project was just created from the template, swap the storefront README and clean up template files:

```bash
# Swap README: replace storefront with project placeholder
if [ -f README-template.md ]; then
  mv README-template.md README.md
fi

# Move stub docs from scaffolds/ to docs/ root (if not already done by a scaffold command)
if [ -d docs/scaffolds ] && [ "$(ls -A docs/scaffolds/*.md 2>/dev/null)" ]; then
  mv docs/scaffolds/*.md docs/ 2>/dev/null
  rmdir docs/scaffolds 2>/dev/null
fi

# Remove samples directory (only useful on the template repo itself)
rm -rf samples/ 2>/dev/null

# Remove template-specific ADRs and research docs
rm -rf docs/adrs/template/ 2>/dev/null
rm -f docs/research/how-we-compare-*.md docs/research/agent-teams-comparison.md 2>/dev/null
rm -f docs/research/squad-vs-vteam-*.md docs/research/ux-gap-analysis-*.md 2>/dev/null
rm -f docs/research/what-*-can-learn-from-*.md docs/research/what-we-learn-from-*.md 2>/dev/null
```

---

## Phase 1: Quick Discovery (Cam — 3 questions)

Keep this focused. Ask the human these three questions and STOP. Do not go deeper unless they volunteer more:

1. **What are you building?** (one sentence)
2. **Who is it for?** (target user)
3. **What's the first thing it should do?** (MVP scope)

Summarize back: "So you're building [X] for [Y], starting with [Z]. Got it?"

**After confirmation**, update CLAUDE.md:
- Replace `[Your Project Name]` with the actual project name
- Replace `[Brief description of what this project does]` with their one-sentence description
- Replace `[Language, framework, key libraries]` with the tech stack (ask if not obvious from context)

---

## Phase 2: Create 3-5 Work Items

Based on the MVP scope, create a simple backlog. Write it to `docs/plans/quickstart-backlog.md`:

```markdown
# Backlog

## Sprint 1

- [ ] #1: [first work item — the "first thing it should do"]
- [ ] #2: [supporting item]
- [ ] #3: [supporting item]

## Later

- [ ] [anything else they mentioned]
```

Keep items small and concrete. Each should be completable in one TDD cycle. If the user mentioned more than 5 things, push extras to "Later" — ruthlessly.

**Ask:** "These are your first 3 items. Want to adjust, or should we start building?"

---

## Phase 3: First Test (Tara)

Once confirmed, immediately start TDD on item #1:

1. Invoke Tara as a standalone agent to write the first failing test for item #1.
2. Once Tara's test exists, invoke Sato to make it pass.
3. After green, mark item #1 as done in the backlog.

This is the moment the user sees the system work. Don't delay it with more planning.

---

## What This Skips (and How to Add It Later)

| Skipped | What it does | How to add later |
|---------|-------------|-----------------|
| Phase 1b (Human Model) | Captures your product philosophy | Run `/kickoff` Phase 1b standalone, or Pat learns organically over time |
| Phase 2 (Sacrificial Concepts) | Explores alternative approaches | Run `/design` before any major feature |
| Architecture Gate | Archie proposes + Wei challenges | Run `/adr` when you face a significant technical choice |
| GitHub Projects board | Sprint tracking with status columns | Ask Claude to set up a board (Grace handles this), or see `docs/integrations/README.md` |
| Threat model | Security analysis | Pierrot creates one during first `/code-review` |
| Test strategy | Testing approach doc | Tara creates one organically during TDD |

**You can always "upgrade" to the full methodology later.** Nothing is lost by starting fast — the agents learn your project as you work, and the process docs accumulate naturally. Run `/kickoff` at any point if you want the full ceremony.
