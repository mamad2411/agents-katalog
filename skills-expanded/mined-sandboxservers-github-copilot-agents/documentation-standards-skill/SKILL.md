---
name: documentation-standards
description: >-
  Documentation templates and writing standards for READMEs, runbooks, and
  technical writing. Includes ready-to-use templates, the Diátaxis framework,
  audience adaptation guidelines, and writing style rules.
when-to-use: >-
  Invoke when starting documentation for a project, writing a README, creating
  a runbook, or establishing documentation standards for a team. Also invoke
  when reviewing documentation for completeness and quality.
categories:
  - documentation
  - standards
  - templates
---

# Documentation Standards

Documentation is a product, not an afterthought. Every doc answers three questions: who is the audience, what type of doc is this, and what do they need to know.

## Documentation Types (Diátaxis Framework)

| Type | Orientation | Audience State | Example |
|---|---|---|---|
| **Tutorial** | Learning | "I'm new, teach me" | Step-by-step guided experience |
| **How-To Guide** | Task | "I need to do X" | Goal-driven steps for a specific task |
| **Reference** | Information | "What does X do?" | Complete, consistent, dry |
| **Explanation** | Understanding | "Why does X work this way?" | Context, tradeoffs, history |

**Don't mix types.** A runbook is a how-to, not a tutorial. An ADR is an explanation, not a reference.

---

## README Template

```markdown
# Project Name

One-sentence description of what this project does and why it exists.

## Quick Start

The fastest path from clone to running. Three commands or fewer.

\`\`\`bash
git clone <repo-url>
cd <project>
<run-command>
\`\`\`

## Prerequisites

- Runtime/language version (e.g., Node.js 20+, .NET 8)
- Required tools (e.g., Docker, Terraform, Azure CLI)
- Access requirements (e.g., Azure subscription, API keys)

## Installation

Step-by-step setup beyond the quick start.

## Usage

Common usage examples with expected output.

## Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | Yes | — | Connection string |
| `LOG_LEVEL` | No | `info` | Logging verbosity |

## Architecture (optional)

High-level overview with diagram for systems with 3+ components.

## Contributing

Branch strategy, PR process, code style, testing requirements.

## License

License type and link to LICENSE file.
```

### README Rules
- Under 2 screens of scrolling — link to deeper docs
- Quick Start works in under 5 minutes
- All commands are copy-pasteable without modification
- Update when setup steps change — stale READMEs are the #1 onboarding blocker

---

## Runbook Template

```markdown
# Runbook: [Service] — [Scenario]

## Metadata
- **Last Verified**: YYYY-MM-DD
- **Owner**: [Team]
- **Review Cadence**: Quarterly

## Trigger
What alert or symptom triggers this runbook.

## Prerequisites
- [ ] Access to [system/tool]
- [ ] Permissions: [specific role]
- [ ] Tools installed: [CLI, kubectl, etc.]

## Steps

### 1. Diagnose
1. Open [dashboard] at [URL]
2. Run:
   \`\`\`bash
   <diagnostic command>
   \`\`\`
   Expected output: [what healthy looks like]
3. If [condition A] → Step 2. If [condition B] → Escalate.

### 2. Resolve
1. Run:
   \`\`\`bash
   <resolution command>
   \`\`\`
   Expected output: [what success looks like]
2. Wait [duration] for stabilization.

## Verification
1. Check [metric/dashboard] — should be [expected state]
2. Monitor for [duration]

## Rollback
1. Run: \`<rollback command>\`
2. Verify original state restored
3. Escalate with context

## Escalation
- **Level 1**: [Team] — [contact]
- **Level 2**: [Person] — [contact]
- **Emergency**: [process]
```

### Runbook Rules
- Copy-pasteable steps — exact commands, not "run the script"
- Include expected output after every command
- Include rollback for every change
- No tribal knowledge — if it requires unstated knowledge, the runbook is incomplete
- Test quarterly — have someone who didn't write it follow the steps
- One scenario per runbook — link between them if needed

---

## Writing Style

### Sentence Rules
- Maximum 25 words per sentence
- One idea per sentence
- Lead with the action: "Run the command" not "The command should be run"
- Put conditions first: "If using Premium tier, configure..." not "Configure... if Premium"
- Delete qualifiers: "basically", "actually", "simply", "just", "really"

### Paragraph Rules
- Maximum 4 sentences per paragraph
- One topic per paragraph
- Lead with the key point — don't build up to it

### Headers
- Descriptive, not clever: "Configure authentication" not "Lock it down"
- Sentence case: "Configure the gateway" not "Configure The Gateway"
- Never skip levels (H2 → H4 without H3)
- Should work as a scannable table of contents alone

### Code Blocks
- Always specify language identifier
- Test all examples before publishing
- Use realistic values, not `foo` and `bar`
- Mark placeholders: `<RESOURCE_GROUP>` not `myResourceGroup`

### Tables
- Under 5 columns — wide tables are unreadable
- Right-align numbers, left-align text
- Include units in column headers

---

## Documentation Review Checklist

- [ ] Doc type identified (tutorial, how-to, reference, explanation)
- [ ] Audience identified (engineer, ops, executive, new hire)
- [ ] `metadata` or header with title, last updated, owner
- [ ] Prerequisites listed with specifics
- [ ] Commands are copy-pasteable
- [ ] Expected output shown after significant steps
- [ ] Links to deeper documentation included and working
- [ ] No mixing of doc types within one document
- [ ] Diagrams included for systems with 3+ components
- [ ] Comprehension test: "Could someone not in the room understand this?"

## Related Skills

- `architecture-decision-records` — ADR template and process
- `observability-baseline` — Runbook links and alert documentation
