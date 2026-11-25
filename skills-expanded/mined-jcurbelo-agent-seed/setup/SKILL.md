---
description: Interactive setup wizard. Personalizes your agent-seed with voice, context, agents, and integrations. Run this first.
---

# /setup - Setup Wizard

Interactive wizard that personalizes your agent-seed installation.
Can be re-run anytime to add new agents or integrations.

## Step 0: Environment Check

Check what's available:

1. **git** — run `git --version`. If missing, stop and tell the user to install git.
2. **gh CLI** — run `gh --version`.
   - If installed: "I'll create PRs for all changes so you can review them."
   - If not: "No worries! I'll commit changes directly. You can install the GitHub CLI later if you want PR-based workflows: https://cli.github.com"
3. **Detect LLM tool** — check which tool is running (Claude Code, Cursor, etc.) and note it for context.

## Step 1: Identity

Ask these questions one at a time. Wait for each answer before proceeding.

1. "What's your name?"
2. "What do you do? (e.g., software engineer, product manager, designer, founder, student, etc.)"
3. "What tools and services do you use daily? (e.g., GitHub, Linear, Slack, Jira, Notion, etc.)"

Save answers to:
- `context/work/index.md` — role and overview
- `context/work/tools.md` — tools and services

## Step 2: Voice (Optional but Encouraged)

Ask: "I'd love to learn your communication style so I can draft messages that sound like you. You can:"
- **Option A:** "Paste 5-10 messages you've sent recently (Slack, email, etc.)"
- **Option B:** "Describe your style: formal or casual? Emoji or no emoji? Short or detailed?"
- **Option C:** "Skip this for now — you can always add it later"

If Option A:
- Analyze the messages for patterns: tone, capitalization, punctuation, greetings, closings, emoji usage, sentence length, formality level
- Generate `context/voice/index.md` with a voice profile
- Generate `context/voice/patterns.md` with extracted patterns and examples

If Option B:
- Generate a basic `context/voice/index.md` from the description
- Leave `context/voice/patterns.md` with a template for later

If Option C:
- Leave template files in place

## Step 3: Agent Selection

Based on the user's role, suggest a starter set of agents:

**Software Engineer:**
- coder, reviewer, researcher, todo-manager, reflection (all ship by default)
- Suggest: pr-agent (branch + PR creation)

**Product Manager:**
- researcher, todo-manager, reflection (ship by default)
- Suggest: note-taker (meeting notes), tracker (issue tracking)

**Designer:**
- researcher, todo-manager, reflection (ship by default)
- Suggest: feedback-collector (design review)

**Founder / Generalist:**
- All defaults + suggest: drafter (writing), tracker (issue tracking)

**Any role:**
- Always include: todo-manager, reflection (these are core)

Ask: "Based on your role as [X], I'd suggest these agents: [list]. Want me to add any of these? Or describe what else you need and I'll create a custom agent."

For each selected agent:
1. Create the agent `.md` file with proper frontmatter
2. Add it to `.claude/agents/index.md` routing table

## Step 4: Integrations (Optional)

Ask: "Do you want to connect any of these? (just say which ones)"

| Integration | What it adds |
|-------------|-------------|
| Slack (read-only) | slack-reader agent + safety hook to block posting |
| GitHub | pr-agent for branch + PR workflows |
| Linear | tracker agent for issue management |
| Jira | tracker agent (Jira variant) |

For each selected integration:
1. Create the agent definition
2. Update `.claude/agents/index.md`
3. Add safety hooks to `.claude/settings.json` if needed (e.g., Slack read-only)

## Step 5: Save and Commit

1. Update `context/index.md` to link to all created context files
2. Update `memory/MEMORY.md` with basic profile info
3. Validate everything: run `scripts/check-markdown-policy.sh`

If gh CLI is available:
1. Create branch: `feat/initial-setup`
2. Stage all generated files
3. Commit: "feat: initial agent-seed setup"
4. Push and create PR with summary of what was configured

If no gh CLI:
1. Stage all generated files
2. Commit: "feat: initial agent-seed setup"
3. Tell the user what was created

## Step 6: Next Steps

Tell the user:
"You're all set! Here's what you can do now:"
- `/standup` — start your day with a briefing
- `/eod` — end your day, capture learnings
- `/learn` — let the system improve itself
- "Edit `context/voice/` anytime to refine your voice profile"
- "The system will learn your preferences over time and propose improvements via PRs"
