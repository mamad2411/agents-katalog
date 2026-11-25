---
name: prebuild
description: >
  Pre-build checkpoint for disciplined vibe coding. Asks 6 evaluative questions
  before any code generation using interactive prompts. Use when the user says
  /prebuild, asks to build a feature, implement something, or starts a coding task.
  Also trigger on phrases like "build me", "create a", "implement", "add a feature",
  "set up", or "write code for". Lighter than /think — focused specifically on code
  generation discipline, not full strategic thinking.
---

# Pre-Build Checkpoint (/prebuild)

A fast, focused checkpoint that ensures you evaluate before you build. This is
the discipline layer for vibe coding — 6 questions via interactive prompts,
~10 minutes, then you code with clarity instead of guessing.

**Core principle:** Never generate implementation code until the human has
confirmed the checkpoint. Use the AskUserQuestion tool to make confirmation
fast and interactive — not a wall of text.

## How It Differs from /think

| | /prebuild | /think |
|---|-----------|--------|
| **Focus** | Code generation only | Any domain |
| **Duration** | ~10 minutes | 30-60+ minutes |
| **Interaction** | AskUserQuestion with selectable options | Free-form Q&A |
| **AI role** | Proposes answers, human picks/adjusts | Asks questions, waits |
| **Output** | Build spec → code generation | Full Bloom level progression |
| **Saves to vault** | No (unless asked) | Yes (Level 1) |

Use `/prebuild` for features and implementation tasks.
Use `/think` for architecture decisions, new projects, or non-code problems.

---

## The Flow

```
┌──────────────────────────────────────────────────────────┐
│  1. DETECT — What is being built? (silent)               │
│  2. SCAN — Read codebase for patterns (silent)           │
│  3. ROUND 1 — AskUserQuestion: Purpose, Reuse, Risks,   │
│               Alternatives (4 interactive questions)     │
│  4. ROUND 2 — AskUserQuestion: Success Criteria,        │
│               Documentation (2 interactive questions)    │
│  5. SPEC — Compile confirmed answers (internal)          │
│  6. BUILD — Generate code from spec                      │
└──────────────────────────────────────────────────────────┘
```

---

## Step 1: Detect (Silent)

Parse what the user wants to build. Identify:

- **Feature type**: API endpoint, UI component, background job, integration, refactor, migration
- **Scope signal**: New feature, extension, or fix?
- **Complexity signal**: Single file or multi-file?

Output one line before starting the scan:

> **Detected:** [feature type] — [brief description] ([scope], [complexity])

---

## Step 2: Scan (Silent)

Read the codebase for context BEFORE asking questions. This is what makes
/prebuild different from a generic checklist — the AI does the homework first.

**Scan for:**
- Existing patterns that match (similar endpoints, components, services)
- Conventions (error handling, auth, naming, file structure)
- Related code this feature touches or depends on
- Tech stack details (framework, ORM, test framework)

Use Glob, Grep, and Read. Be fast — 1-2 minutes max.

Output a brief scan summary:

> **Codebase scan:**
> - Framework: [detected]
> - Similar pattern: [file path and description]
> - Conventions: [key patterns found]

---

## Step 3: Round 1 — Interactive Checkpoint (4 Questions)

Use `AskUserQuestion` with 4 questions. For each question, propose 2-3 options
based on the scan, plus the automatic "Other" option for custom answers.

**CRITICAL: Build the options from the codebase scan.** Generic options like
"Yes/No" defeat the purpose. Each option should be a concrete, scan-informed
proposal that the human can pick with one click.

### How to build the AskUserQuestion call:

```
AskUserQuestion with 4 questions:

Question 1 — PURPOSE (header: "Purpose")
  "What problem does this solve?"
  Options based on user's request — propose 2-3 interpretations:
  - Option A: [most likely purpose based on request] (Recommended)
  - Option B: [alternative interpretation]
  - Option C: [broader/narrower scope variant]
  (User can always pick "Other" to write their own)

Question 2 — REUSE (header: "Reuse")
  "Which existing patterns should we follow?"
  Options based on codebase scan — propose specific files/patterns:
  - Option A: "Follow [specific file/pattern found in scan]" (Recommended)
  - Option B: "New pattern — [reason existing ones don't fit]"
  - Option C: "Extend [existing component/service] with [modification]"

Question 3 — RISKS (header: "Risks")
  "Which risks should we handle?" (multiSelect: true)
  Options based on feature type risk table:
  - Option A: [highest-priority risk for this feature type]
  - Option B: [second risk]
  - Option C: [third risk]
  - Option D: [fourth risk if applicable]

Question 4 — APPROACH (header: "Approach")
  "Which approach should we take?"
  Options — propose alternatives with previews showing the difference:
  - Option A: [recommended approach] (Recommended)
    preview: brief code/architecture sketch
  - Option B: [alternative approach]
    preview: brief code/architecture sketch
```

### Risk options by feature type:

| Feature Type | Propose These Risks |
|-------------|---------------------|
| API endpoint | Auth bypass, Input validation, Rate limiting, Error format mismatch |
| Payment/financial | Double-processing, Race conditions, Audit trail, Idempotency |
| Data migration | Data loss, Rollback plan, Downtime, Schema conflicts |
| UI component | Accessibility (a11y), Responsive/RTL, Empty state, Loading state |
| Background job | Retry logic, Dead letters, Timeout, Monitoring |
| Integration | API versioning, Timeout handling, Credential rotation, Error mapping |
| Auth/security | Token leakage, Privilege escalation, Session fixation, CSRF |

### Use previews for the Approach question

When the alternatives involve different code structures, use the `preview` field
to show a brief sketch so the human can visually compare:

```
Option A: "Server Component with tag-overlap scoring"
preview: |
  // lib/content.ts
  function getRelatedInsights(slug, locale) {
    // Score by shared tags, exclude self
    // Return top 3 sorted by overlap
  }

  // Used directly in the page component
  const related = getRelatedInsights(slug, locale)

Option B: "Client component with dynamic loading"
preview: |
  // components/RelatedInsights.tsx
  'use client'
  // Fetches related articles on mount
  // Shows skeleton while loading

  // Wrapped in Suspense on the page
  <Suspense fallback={<Skeleton />}>
    <RelatedInsights slug={slug} />
  </Suspense>
```

---

## Step 4: Round 2 — Interactive Checkpoint (2 Questions)

After Round 1 answers are confirmed, use `AskUserQuestion` again:

```
AskUserQuestion with 2 questions:

Question 5 — SUCCESS (header: "Done when")
  "How do we know this is done?"
  Options — propose testable criteria sets:
  - Option A: "[Full criteria set based on scan + Round 1 answers]" (Recommended)
  - Option B: "[Minimal viable criteria]"
  - Option C: "[Extended criteria with tests]"

Question 6 — DOCS (header: "Document")
  "What should we document?"
  Options:
  - Option A: "Standard pattern — no special docs needed" (if straightforward)
  - Option B: "Document [specific non-obvious decision from Round 1]"
  - Option C: "Add inline comments for [complex logic area]"
```

---

## Step 5: Build Spec (Internal)

Compile all confirmed answers into an internal build spec. Do NOT show this
to the user unless they ask.

```markdown
## Build Spec

**Feature:** [name]
**Purpose:** [Q1 answer]
**Reuse:** [Q2 — files and patterns to follow]
**Risks mitigated:** [Q3 — selected risks and how each is handled]
**Approach:** [Q4 — chosen approach]
**Success criteria:** [Q5 — confirmed checklist]
**Docs:** [Q6 — what to document]
```

---

## Step 6: Build

Generate code. Every line traces back to the build spec.

**Rules during generation:**

1. **Follow the reuse answers exactly.** If Q2 said "use the existing wrapper," don't create a new one.
2. **Address every selected risk from Q3.** If the human selected "Accessibility" and "Empty state," both must be handled.
3. **Meet every success criterion from Q5.**
4. **Match existing conventions from the scan.**
5. **Don't add what wasn't asked for.** The build spec is the scope.

After generating, verify against criteria:

> **Checkpoint verification:**
> - [check] [criterion from Q5] — [status]
> - [check] [risk from Q3] — [how it's handled]
> - [check] [reuse from Q2] — [confirmed match]

---

## Commands

### /prebuild [description] — Start checkpoint
Begin a new pre-build checkpoint for the described feature.

### /prebuild skip — Minimal mode
Single AskUserQuestion call with only Q2 (Reuse) and Q3 (Risks).
For small changes where a full checkpoint is overkill.

### /prebuild review — Post-build review
After code is generated, re-check against the build spec.

---

## When NOT to Use

- **Bug fixes with clear cause** — Just fix it.
- **One-line changes** — Don't checkpoint a typo.
- **Exploratory / throwaway code** — Prototyping is fine without a checkpoint.
- **Already went through /think** — Evaluation is done. Go straight to building.

---

## Rules

1. **NEVER generate implementation code before the checkpoint is confirmed.** Scanning and proposing options is fine — feature code waits for confirmation.
2. **ALWAYS scan the codebase first.** Options without codebase context are just guesses.
3. **ALWAYS use AskUserQuestion** for the checkpoint — not markdown text dumps. The interactive format is faster and creates a clear decision record.
4. **Q2 (Reuse) and Q3 (Risks) are non-negotiable.** Even in skip mode, these two are asked.
5. **Build options from the scan.** Generic "Yes/No" or "Option A/B" without codebase-specific content defeats the purpose.
6. **Keep it fast.** Total checkpoint under 10 minutes. If it's taking longer, use /think instead.
7. **Don't be bureaucratic.** For simple features with clear patterns, propose confident defaults and make confirmation a single click.
8. **Use previews on Q4 (Approach)** when alternatives have meaningfully different code structures. Skip previews when the difference is trivial.
