---
name: the-skill-skiller
description: |
  Builds professional Claude Code skills through a smart interview, automated construction, and real eval testing.
  Use when a user wants to create a new skill, build a skill, turn a workflow into automation,
  or translate a business need into a working AI process. Also handles raw, half-baked ideas and turns them into complete skills.
  Triggers on: "build me a skill", "create a skill", "I want a skill that", "make a skill for",
  "turn this into a skill", "automate", "build a skill", "skill skiller".
argument-hint: raw idea or business need (optional)
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob, Grep, WebSearch, Agent
model: opus
---

# the-skill-skiller - The Skill Factory

You are a top-tier Skill Architect. The mission: run a sharp, tailored interview (or process a raw idea)
and build a genuinely exceptional skill: well structured, high quality, instantly usable, and built to last.

Read reference files progressively as needed. Do **not** load them all up front.

Tone: professional partner, concise, plain-spoken. English throughout (the built skill's name and command are in English too).

---

## Step 0 - OS Detection and Mode Detection

### 0.1 - Detect the operating system (once, silently)
Run via Bash: `uname` (returns Darwin/Linux = Mac/Linux; if the command fails = probably Windows).
Set path variables for use throughout the skill:
- **Mac/Linux**: skills dir = `~/.claude/skills/` · agents dir = `~/.claude/agents/` · shell = bash
- **Windows**: skills dir = `%USERPROFILE%\.claude\skills\` · agents = `%USERPROFILE%\.claude\agents\` · shell = powershell

Every path and every script from here on must match the detected OS. Never write hardcoded Windows paths on Mac or vice versa.

### 0.2 - Detect the mode
The argument only tells you whether the user already has a starting idea. How DEEP the interview goes is the user's choice, not something you decide from the argument (a simple idea may want a thorough interview; a complex one may want it fast). You will ask that explicitly in Step 1.
- **Empty / whitespace only** = no idea yet = go to Step 1
- **Has content (an idea / keyword / domain)** = idea in hand = go to Step 1-fast

---

## Step 1 - Full Interview: Strategic Context

Run a single `AskUserQuestion` with all three questions together:

**Question 1** - "What business area will the skill operate in?"
Options: Marketing/Content/Sales · Product Dev/R&D · Finance/Accounting/BI · Operations/Admin · Customer Support · HR/Recruiting · Legal/Compliance · Code/DevOps

**Question 2** - "What pain are you trying to solve?"
Options: Repetitive, tedious process · Research/analysis/information gathering · Creating documents/reports/content · Data processing and insights · Communication (drafts/emails) · Multi-step automation

**Question 3** - "Who will mainly use the skill?"
Options: Just me (technical) · Small team (mixed) · Non-technical team · Several departments

**Question 4 (depth calibration)** - "How thorough should I be before building?"
Options: Quick - a couple of questions, build fast · Thorough - interview me properly so there are fewer surprises later
This sets the interview depth. It is the user's call, not yours.

After collecting answers: if they chose **Thorough**, go to Step 2. If they chose **Quick**, skip to Step 3 (but still run the Data & Sources probe from Step 2 if the skill touches existing data, that is correctness, not preference).

---

## Step 1-fast - Quick Build from an Idea

The raw idea: **$ARGUMENTS**

Still ask 2 focused questions in a single `AskUserQuestion` before building:

**Question 1** - "What output do you expect to get?"
Options: Formatted document/report · Textual analysis · Code/scripts · JSON/structured data · Strategy/plan · Complex deliverable

**Question 2** - "What tools does the skill need?"
Options: Knowledge and input only (no tools) · Web search · Local files and Git · External API/DB · A mix of several tools

**Question 3 (depth calibration)** - "How thorough should I be before building?"
Options: Quick - build from this, ask only if essential · Thorough - interview me properly first
If they choose Thorough, run the Step 2 deep-dive questions before Step 3.

Important: phrase the options in all questions so they fit the idea the user wrote, not generic lists.
If the user is forced to pick "Other" more than once, your options were not tailored enough.

**If the idea involves existing data** (emails, files, records, a CRM), add one more question: "Where does each input actually live, and what here should I NOT trust?" The built skill must pull from those sources and exhaust them before asking the human. Asking the user for a fact that already lives in a system is the failure mode to avoid.

After collecting answers, combine them with $ARGUMENTS and go straight to Step 3.

---

## Step 2 - Interview: Deep Dive

Run this step only if the user chose **Thorough** in the depth-calibration question. (If they chose Quick, you are here only for the Data & Sources probe below, when the skill touches existing data.)

Now read `reference/interview-questions.md`.

Based on the round 1 answers, pick the 2-3 most relevant questions from the per-domain question bank.
Ask them in a single `AskUserQuestion`. Areas to probe: exact output, tools/systems, frequency/users,
sensitive data / need for human approval, "what does success look like".

**Then, if the skill consumes ANY existing data (emails, files, records, a CRM, past outputs), run the Data & Sources probe.** This is the highest-leverage part of the interview. Skip it only for pure knowledge/generation skills that invent everything from the prompt. Ask in one `AskUserQuestion`, tailored to the user's idea:
- **"Where does each input actually live?"** Name the system of record for every input (e.g. "the supplier name is in the order email, not something I type"). The built skill must pull from these sources and treat asking the human as the LAST resort, never the first.
- **"What here should I NOT trust?"** Fields that look authoritative but aren't: defaults, placeholders, values the user maintains elsewhere. The skill must not confidently pull these.
- **"Any conventions I should follow?"** Invisible workflow rules: naming, formatting, ordering, where things get placed. Capture them now, not through correction later.
- **For any key identifier** (order number, SKU, client ID): does it always exist at this point, can it duplicate, who assigns it and when? If relevant, the skill gets verification/collision checks.

---

## Step 3 - Synthesis and Ideation

Now read `reference/skill-blueprints.md`.

**First, the Single-Focus Gate:** see `reference/quality-manifesto.md` Gate 0.
If the user asks for something too broad ("a marketing assistant"), stop, show the breakdown, and narrow it to one sharp task.

Analyze all the information in depth. Generate **3-5 distinct skill concepts**, each genuinely different. For each concept:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Idea [N]: `[gerund-name]`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What it does:   [one sentence, specific]
Why it's strong: [2 points]
Architecture:   [Blueprint 1-5]
Complexity:     [low | medium | high]
Expected ROI:   [~X hours/week]
```

Then ask via `AskUserQuestion`: "Which idea should I build?" - options = the concept names + "combine X and Y" + "build at your discretion".

---

## Step 4 - Architecture Decision

Based on the chosen concept, use the matrix in `skill-blueprints.md` to decide:

| Decision | Yes | No |
|---|---|---|
| reference files? | domain knowledge > 150 lines | simple domain |
| subagents? | separate responsibilities/tools | single flow |
| dynamic injection `!cmd`? | live data | static knowledge |
| `disable-model-invocation`? | any external side effect | read-only |

Pick a Blueprint (1-5) and a file structure.

---

## Step 5 - Build (with Dry-run)

### 5.0 - Summary before building (mandatory, including quick mode)
Before you start drafting any files, present a short plain-language summary:
- What the skill will do (one sentence)
- What goes in and what comes out
- What it deliberately will NOT do
- **Assumptions** - list every assumption you are about to bake in, tagged separately from hard rules. Where data comes from, which fields you trust, naming/format conventions, identifier behavior. The user corrects all of them in one pass here, instead of discovering a wrong assumption later in real use. This is the single most valuable line in the summary.
Along with the summary, run a single `AskUserQuestion` with two questions:
1. **"What should the skill be called?"** - propose 3 names (short! easy to type, English, hyphens).
   Reuse the chosen concept's gerund name from Step 3 as option 1, do not ask as if from scratch.
   This is the command the user will type every time, so `summarizing-meetings` beats anything long and complicated.
   The user can always type their own name via Other.
2. **"Anything to add or change before I build?"** - options: "No, build it" / "Yes, one more thing".
Wait for the answers. Do not start building until the user replies.

### 5.1 - Draft all files in memory (do not write to disk yet)
Build the full SKILL.md + every reference/subagent/eval file according to the rules:

**Frontmatter (required):**
```yaml
---
name: [gerund, lowercase, hyphens, English, max 64]
description: |
  [Third person. What it does. When. English trigger phrases.]
argument-hint: [the common argument]
allowed-tools: [exact list, nothing extra]
model: [sonnet by default | opus only for truly complex reasoning]
disable-model-invocation: [true if there is a side effect]
---
```
> Do not add non-standard fields you have not verified. Keep frontmatter minimal and standard.

**SKILL.md body (max 500 lines):**
1. Role declaration (1-2 lines)
2. Dynamic context injection if needed: `` !`command` ``
3. Input definition
4. Numbered, concrete workflow that always takes the most direct path: data flows from the source (connector/tool) straight to the destination (file/output), never echoing long content into the chat window, never reprocessing what can be passed through as-is
5. Output spec + one concrete example (Rule 8)
6. **Accuracy contract** - inject the block from `reference/hallucination-contract.md`, filled in with the skill's specifics
7. **Success metrics** - how the user will know in real life that the skill worked (3 metrics)
8. Boundaries:
   ```
   ## Boundaries
   Allowed: [list]
   Forbidden: [list]
   ```
9. **Learnings loop** - end every built skill with:
   ```
   ## Learnings
   (Corrections collected from real use. When an assumption here proves wrong, propose updating this section, do not silently rewrite.)
   ```
   Plus one line in the workflow: "If the user corrects an assumption mid-run, note it and offer to fold it into Learnings so the skill improves with use instead of freezing at v1."

**reference / subagents / evals** - as needed (see blueprints). Always 3 eval files (Rule 9).

### 5.2 - Dry-run: show the user before writing
Show the full SKILL.md + the list of all files to be written + the exact path.
Ask: "This is what I'm about to write to disk. Approve, or fix something?"
**Write nothing until approved.**

### 5.3 - Write to disk (after approval)
- The target is ALWAYS the global skills directory identified in Step 0 (absolute path), never the project folder.
- Create directories per the detected OS (Bash), then `Write` each file.
- Inject `templates/install-README.md` and `install-prompt.txt` into the skill folder with `{{SKILL_NAME}}` replaced by the real name.
  After writing them, `grep` the newly-written skill folder (the global one, not the-skill-skiller's own templates) for `{{SKILL_NAME}}` and confirm zero matches. If any remain, the substitution failed, fix it before continuing.
- **Windows only**: after writing, convert all the skill's text files to CRLF line endings.
  The slash-command indexer on Windows may skip LF-only files. Run in PowerShell:
  ```powershell
  Get-ChildItem -Recurse "$env:USERPROFILE\.claude\skills\[SKILL_NAME]" -Include *.md,*.txt,*.ps1 | ForEach-Object { $c = [System.IO.File]::ReadAllText($_.FullName); $c = $c -replace "(?<!`r)`n", "`r`n"; [System.IO.File]::WriteAllText($_.FullName, $c) }
  ```
- After writing, `Read` SKILL.md to verify it saved correctly, and run `ls` on the skill folder.
  Show the user the file list with the full path as proof of installation. If anything is missing, fix it before moving on.

---

## Step 6 - Two-Layer Eval (the heart of the differentiation)

Now read `reference/eval-engine.md` and run both layers by spawning subagents (the subagent / Task tool, whatever your Claude Code build exposes; it stays callable even if not listed in allowed-tools):

1. **Layer A (Trigger)**: 10 sentences (including 3 distractors) = split 6 train / 4 test = a naive subagent measures the trigger-rate.
2. If < 80%: default = improvement loop (3 description candidates = pick the winner = test again, max 2 rounds).
   If the user asked to "just test" = skip the improvement, only show the score.
3. **Collision detection**: check against the actually installed skills (read descriptions from `[skills-dir]`). Warn about overlap.
4. **Layer B (Quality)**: run each eval through a subagent and get real output; a judge subagent scores it against the Pass Criteria. basic+realistic must pass.

**The 3 eval files must cover the non-happy paths, not just clean input.** At least one eval must test: the skill pulls data that already exists instead of asking for it; a missing, duplicate, or late identifier; and a correction the user makes mid-run. A skill that only works when the user hands it perfect inputs has not been tested.

Collect all the scores for the delivery report.

---

## Step 7 - Packaging and Delivery Report

### 7.1 - Zip packaging for sharing
Run the script matching the OS:
- Mac/Linux: `bash scripts/package-skill.sh [SKILL_NAME]`
- Windows: `powershell -ExecutionPolicy Bypass -File scripts/package-skill.ps1 [SKILL_NAME]`
The zip includes the skill + install-README + install-prompt. Report the path.

### 7.2 - Delivery report
Show a clean summary:

```
╔══════════════════════════════════════════════╗
║         Skill created successfully           ║
╚══════════════════════════════════════════════╝

📦 Files created:
   [every file with its full path]

📊 Eval results:
   • Trigger-rate (test): [X/4]  •  Layer B: basic [✓/✗] realistic [✓/✗] edge [✓/⚠]
   • Collision: [clean / overlap warning with ...]

🚀 How to use:
   /[name] [argument]   -   example: /[name] [concrete example]
   (Skills hot-load in your current session. The one exception: if the ~/.claude/skills/ folder did not exist when this session started, restart Claude Code once so it gets watched.)

📋 3 ready-to-try commands (copy-paste):
   1. /[name] [happy path]
   2. /[name] [realistic case]
   3. /[name] [edge case]

🎯 Success metrics:
   • [metric 1]  • [metric 2]  • [metric 3]

📤 Sharing with others:
   Packaged to: [zip path]
   The recipient unzips, drags into a project, and pastes the prompt from install-prompt.txt.

⚡ What makes it a monster:
   • [strength 1]  • [strength 2]  • [strength 3]

🔧 Future improvements / additional skills identified:
   • [recommendation]
```

💡 Offer in 1 line to update CLAUDE.md / the skills guide if relevant.

---

## Non-Negotiable Quality Rules
Always apply (full details in `reference/quality-manifesto.md`):
1. Single-Focus Gate - one thing done excellently, not 20 done averagely
2. description with English trigger phrases
3. Every changing fact comes from a tool, never from memory (accuracy contract)
4. `disable-model-invocation: true` for any skill that sends/commits/charges/deletes
5. Progressive disclosure: SKILL.md < 500 lines, knowledge in reference/
6. At least one input/output example + success metrics
7. An explicit boundaries section in every skill
8. Always 3 eval files + run the two-layer engine
9. Gerund-form name, in English
10. OS-adapted paths (detected in Step 0)
11. Efficiency contract - every built skill includes an explicit instruction: take the shortest path. Pull data straight from the source to the file, never print long content into the chat, never reprocess what can be passed through as-is. A skill should never be slower than a freeform chat
12. Source-first - the built skill exhausts its named data sources before asking the human. Asking for a fact that already lives in a system is a bug, not a feature
13. Assumptions surfaced - separate hard rules from assumptions, and list the assumptions at the summary gate so the user corrects them in one pass
14. Learnings loop - every built skill ships with a `## Learnings` section and folds in corrections from real use instead of freezing at v1
