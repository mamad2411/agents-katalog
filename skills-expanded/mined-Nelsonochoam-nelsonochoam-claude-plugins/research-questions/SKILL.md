---
name: research-questions
description: Generate focused research questions a developer would naturally need to answer before starting work on a feature.
disable-model-invocation: true
model: opus
---

User's request: $ARGUMENTS

# Generate Research Focus

You are an engineer reading an intent or product requirements document for the first time. Your job is to produce a focused set of research directives — the questions, focus areas, and things to look into before a research agent dives into the codebase.

The output is meant to *steer* the upcoming research, not to answer anything. Think of it as a briefing: what should the research answer and investigate, and what should it not to avoid drifting into tangents. If the intent document already contains specifics (component names, flags, data fields, stated preferences), do light reading to confirm they exist — but do not go deep. Deep research happens later.

## Feature Discovery

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/feature-discovery.md`.

- **Current phase**: `research-questions`
- **No-args fallback**: ask the user to share the intent document or feature description.
- **Prerequisite check**: Run prerequisite check per `${CLAUDE_PLUGIN_ROOT}/references/prerequisite-check.md` for phase `research-questions`. If the check halts, stop here.
- **Auto-advance**: If `$ARGUMENTS` contains `--autoadvance`, follow the auto-advance protocol in the prerequisite check reference before proceeding. Strip `--autoadvance` from arguments before using them as context.

## Process Steps

### Step 1: Read the Intent

Read the intent document carefully at `$FEATURE_PATH/1-intent.md` as the input document. If the user also provided arguments, use those as supplementary context. Identify every feature area, behavior change, or system touch point mentioned.

### Step 2: Think Like a Developer

For each feature area or touch point, think: *what does a research agent need to look at or understand here?*

Each bullet can be a question, a directive, focus area, or external research item — whatever best captures the need:

- **Questions** — surface ambiguities or decisions that depend on what the code currently does (e.g. "How does `AuthMiddleware` currently handle token expiry?")
- **Directives** — explicit instructions for the researcher (e.g. "Look at `src/auth/session.ts` — understand how sessions are invalidated", "Find where `featureFlag.enabled` is checked")
- **Focus areas** — components, files, or flows to examine (e.g. "The `PaymentService` and its interaction with `OrderRepository`")
- **External research** — if understanding how a third-party framework, library, or external API works is needed before the codebase research can be meaningful, include an explicit directive (e.g. "Research how [framework X] handles [topic Y] — understand its API before diving into our integration code"). Use this sparingly and only when the external knowledge gap would block understanding the codebase.

Include specific file paths, component names, function names, or flag names whenever you know them or can confirm them with a quick scan. A grounded item like `"Check how useUserStore (stores/user.ts) manages token refresh"` is far more useful to a researcher than a vague one.

If the intent already names specific things (a component, a flag, a field), you may do a quick scan to verify they exist and note relevant neighbors — but do not go deep. The goal is to give the researchers a tight scope, not to do their job.

### Step 3: Write Focus Items to File

Write the items directly to `$FEATURE_PATH/2-research-questions.md` (create the directory if needed). Use this format:

```
---
task: <ticket-id-kebab-description>
type: research-questions
---

### Research Questions

- <question, directive, or focus area>
```

Ground each item in something specific from the intent. The list should tell the research agent where to look and what to understand — and implicitly what to ignore.

Then say:

```
Written to $FEATURE_PATH/2-research-questions.md — please review.
```

### Step 4: Iterate Until Confirmed

If the user requests changes, edit the file directly using the Edit tool. Re-prompt for review. Do not reprint the full list to the conversation — point the user to the file.

Once the user confirms, say:

```
════════════════════════════════════════
✓ Research questions confirmed.

Recommended next: /crispy:research
Any phase can follow — each works with whatever artifacts exist.
════════════════════════════════════════
```

## Important Guidelines

1. **Light touch only**: You may do a quick scan to confirm specifics mentioned in the intent, but deep research happens later — stay shallow
2. **Steer, don't answer**: Every item should tell the research agent where to look or what to resolve, not provide the answer
3. **Grounded in the intent**: Every item should trace back to something mentioned or implied in the intent document
4. **Mix of forms**: Use questions for ambiguities, directives for things to look up, focus areas for components or flows, and external research directives when needed — whatever is clearest
5. **Tight scope**: The list should implicitly bound what the research agent works on — good items keep it on track, not wandering
6. **External research is allowed**: If the intent involves a framework, library, or external API that the research agent would need to understand before making sense of the codebase, include an explicit external research directive. Frame it as "Research how X works — specifically [aspect]" so the agent knows what to look up and why.
