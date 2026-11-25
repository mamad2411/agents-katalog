---
name: intent
description: Capture intent, define acceptance criteria, and surface ambiguities before any research or planning begins.
argument-hint: '<describe what you want to build or change>'
model: opus
---

User's request: $ARGUMENTS

# Capture Intent

You are tasked with fully understanding what the user wants before any work begins. Do not suggest solutions, do not form opinions about implementation. Only ask, listen, and document. If the user is unsure about something — current behavior, what exists, or how something works — you may do a targeted spot search to help them answer the question. Keep it narrow: look up the specific thing they're uncertain about, share what you find, and return to clarifying intent.

## Feature Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md`.

- **Current phase**: `intent`
- **No-args fallback**: ask the user to describe what they want to build or change.
- **Existing intent**: If `$FEATURE_PATH/1-intent.md` already exists, ask the user whether they want to start a fresh intent or continue editing the existing one. If the file doesn't exist, proceed normally.

## Initial Setup

When this command is invoked, first output:

```
════════════════════════════════════════
Crispy · Intent
═══════════════════════════════════════
```

Then:

1. **Check if a description was provided as a parameter**:
   - If yes, restate it in your own words and proceed to the Restate and Confirm step
   - If no, respond with:
   ```
   I'll help capture the intent before we start. Please describe what you want to build or change — as much or as little detail as you have.
   ```
   Then wait for the user's input.

## Image Handling

Users may share images at any point — screenshots, mockups, diagrams, etc. Pasted images live in Claude Code's internal cache, **not** the temp paths shown in `[Image: source: ...]` tags (those are cleaned up immediately by macOS).

To copy images:

```bash
mkdir -p "$FEATURE_PATH/artifacts"
# Find the current session's image cache (most recently modified directory)
SESSION_DIR=$(ls -td ~/.claude/image-cache/*/ 2>/dev/null | head -1)
# Copy desired image(s) with descriptive kebab-case names
cp "${SESSION_DIR}<N>.png" "$FEATURE_PATH/artifacts/<descriptive-name>.png"
```

Where `<N>` is the image number (1, 2, etc. — sequential per session). Derive the descriptive name from what the image shows (e.g., `current-dashboard-layout.png`). If unclear, ask the user briefly.

Embed in documents using relative links: `![Description](artifacts/descriptive-name.png)`. Place inline near relevant sections, or under a `## Visual References` section if they don't belong to a specific section.

Acknowledge each image to confirm your interpretation. Copy images **before** writing documents so links resolve correctly.

## Steps

### 1. Restate and Confirm

Restate the user's request in 2–3 sentences in your own words. This surfaces any initial misreading and gives the user a chance to correct it before questions are asked.

Then ask: "Is this enough to capture the intent, or would you like me to ask clarifying questions to flesh it out further?"

- **If the user says it's enough** (or words to that effect): proceed directly to Step 3 (Write the Intent Document) using a lightweight format — preserve the user's words under a Summary heading with front matter. Do not force structure the user does not want. If the user included implementation details, acceptance criteria, or constraints in their description, preserve those in the appropriate sections.
- **If the user wants clarifying questions**: say "Before we proceed I have a few questions to make sure I understand your intent fully." and continue to Step 2.

### 2. Ask Clarifying Questions

Ask targeted questions across the following dimensions. Only ask what is genuinely unclear — do not ask about things already stated. Frame questions as hypotheses or assumptions to validate where possible, rather than blank open-ended prompts. "I don't know" is a valid answer — unknowns become open questions in the document, not blockers.

**Background:**
- What's the current system state relevant to this change?
- Has this been attempted before? Are there relevant docs, threads, or prior art?

**Scope:**
- What exactly should change or be created? What is explicitly out of scope, and why?
- Are there related areas that look similar but should NOT be touched?

**Motivation:**
- What problem does this solve, and who is affected by it?
- Is this a user complaint, a business requirement, tech debt, or something else?

**Acceptance:**
- How will we know this is done? Describe scenarios: "Given X, when Y, then Z."
- Are there edge cases or error states that must be handled?
- Are there non-functional requirements (performance, security, accessibility)?

**Risks (optional — skip if the user is early in their thinking):**
- Based on what you've described, are there known risks or concerns? If not, that's fine — we'll note it as no known risks.

**Constraints:**
- Are there technical constraints, deadlines, or dependencies?

Present all questions in a single numbered list. Wait for the user's answers before continuing. If the user answers "I don't know" or seems uncertain about something factual (current behavior, existing code, how something works), offer to do a quick spot search to help them figure it out before moving on.

### 3. Write the Intent Document

Once the user has confirmed (either after restatement or after the Q&A), determine the feature name using this priority:

1. **`CRISPY_FEATURE` env var** — if already set, use it as-is. Do not derive a new name from the title.
2. **Ticket** — if the user mentioned a ticket, use it as the feature name.
3. **Intent title** — otherwise, convert the intent title to kebab-case (e.g. "Add Dark Mode Toggle" → `add-dark-mode-toggle`).

Then resolve and create the feature folder by running:

```bash
FEATURE_PATH=$(bash "${CLAUDE_PLUGIN_ROOT}/scripts/ensure-feature.sh" "<feature-name>")
echo "<feature-name>" > "/tmp/.crispy_session_${PPID}"
```

If images were shared earlier (before the feature folder existed), copy them to `$FEATURE_PATH/artifacts/` now.

**If the user opted for the lightweight path** (confirmed at restatement without Q&A):
- Write `$FEATURE_PATH/1-intent.md` with front matter (`task` and `type: intent` fields) and a Summary section preserving the user's words. Include any additional sections (Acceptance Criteria, Constraints, etc.) only if the user provided that information in their description.

**If the user went through the full Q&A flow**:
- Read the template from `${CLAUDE_SKILL_DIR}/references/intent-template.md`, then write the intent document to `$FEATURE_PATH/1-intent.md` — the document **must include the front matter block** (`task` and `type` fields) from the template, filled in with the resolved feature name and `type: intent`. Acceptance criteria must use the Given/When/Then format with numbered labels (AC-1, AC-2, etc.)

Then say:

```
Written to $FEATURE_PATH/1-intent.md — please open it and review.
```

Wait for the user's response.

### 4. Iterate Until Confirmed

If the user requests changes, edit the file directly using the Edit tool and re-prompt for review. Do not print the full document to the conversation — point the user to the file.

Once the user confirms, say:

```
════════════════════════════════════════
✓ Intent confirmed.

Recommended next: /crispy:research-questions
Any phase can follow intent — each works with whatever artifacts exist.
════════════════════════════════════════
```

## Guidelines

1. **Spot searches are allowed, deep research is not**: If the user is unsure about something factual, do a narrow lookup to help them answer it. Do not explore broadly or start forming implementation opinions — just answer the specific uncertainty and return to intent capture
2. **Do not suggest solutions**: Surface the problem space, not the answer
3. **Acceptance criteria must be scenario-based**: Use Given/When/Then format. If a criterion can't be expressed as a scenario, it's likely a task, not a criterion. If criteria are vague, offer a concrete interpretation and ask if it's right — don't reject the answer outright
4. **Surface unknowns as open questions**: If something is unresolved, flag it as an open question in the document. Open questions are valuable output, not a sign of an incomplete intent
5. **Keep scope tight**: If the user's request seems to be expanding, note it and ask if that is intentional
6. **Gotchas & Risks are best-effort**: Include what the user or context makes evident. If none are identified, note "no known risks identified" — do not block or press the user for risks they don't have
7. **Out of scope needs rationale**: Each out-of-scope item should briefly explain why it's excluded, to prevent re-litigation
