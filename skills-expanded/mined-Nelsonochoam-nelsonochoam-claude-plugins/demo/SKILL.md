---
name: demo
description: Build a demo document using the showboat CLI — demonstrates how something behaves through real outputs, screenshots, videos, and curl calls across different scenarios.
argument-hint: "<feature-name>"
model: opus
---

User's request: $ARGUMENTS

# Demo: Show How It Behaves

Your job is to **demonstrate how something works to a human** by capturing real outputs across meaningful scenarios. You are not trying to prove it works — you are showing what it actually does. If something is broken, the demo should show that honestly too. The document is built entirely by running `showboat` commands — never by writing markdown directly.

Start by learning what showboat can do:

```bash
showboat --help
```

## Setup

Read and follow `${CLAUDE_PLUGIN_ROOT}/references/project-discovery.md`.

**Get the feature name** from `$ARGUMENTS`. If missing, use `AskUserQuestion` to ask. Extract any inline context the user provided (URL, port, credentials, routes) — these override everything else.

```bash
DEMO_BASE=$(bash "${CLAUDE_PLUGIN_ROOT}/scripts/ensure-demo.sh" "<feature-name>")
DEMO_FILE="$DEMO_BASE/demo.md"
```

## Understand What to Demo and How

Figure out what the user wants demonstrated and gather enough context to do it confidently. Don't start capturing evidence until you know what to show and how to access it.

**Check for a runbook first** — it may already answer most questions:

```bash
RUNBOOK=$(bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve-runbook.sh" 2>/dev/null) || true
echo "${RUNBOOK:-NO_RUNBOOK}"
```

If a runbook exists, read it. It is your source of truth for how to access and test this app — URLs, credentials, server startup, available browser tools, API auth patterns, known quirks. Load only the sub-documents relevant to what you're demonstrating.

**If there is no runbook**, read `${CLAUDE_SKILL_DIR}/references/self-discovery.md` and discover the same information from the codebase.

**For anything that requires deeper codebase understanding** — what a flow does, what endpoints exist, how auth works, what a PR changed — spawn parallel `Explore` subagents rather than guessing or reading files yourself. Run independent questions in parallel, only what you actually need:

- "What routes or API endpoints are involved in `<flow>`?"
- "How does authentication work in this codebase?"
- "What changed in this PR and what behavior should be exercised?"

Only explore what the user input and runbook didn't already answer. The goal is to gather just enough to execute confidently.

**If you're still stuck**, ask the user — it's always fine to ask rather than proceed on bad assumptions.

## Initialize the Document

```bash
showboat init "$DEMO_FILE" "<Feature Title>"
showboat note "$DEMO_FILE" "<2-3 sentence description of what is being demonstrated and what scenarios will be covered.>"
```

## Capture Evidence

Think about what scenarios are worth showing — the happy path, edge cases, error conditions, different inputs. Capture real outputs for each. Be honest: if something returns an error or behaves unexpectedly, capture that too.

Choose the best method based on what you're demonstrating:

### UI flows → screenshots and video

Screenshots and video are the most persuasive evidence for UI behavior. If the runbook describes a browser tool (rodney, playwright, webreel, or similar), use it. Check for browser-specific docs in the runbook's `references/` directory.

If no browser tool is documented, run:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/detect-capabilities.sh"
```

Use whatever is available.

### API or backend flows → curl

Make real HTTP requests and capture the actual responses. Test different inputs, edge cases, and error scenarios — not just the happy path. Raw curl output is more honest than any wrapper. See `${CLAUDE_SKILL_DIR}/references/testing-commands.md` for auth and assertion patterns.

### When live execution isn't possible → tests

If the service isn't running or the environment is unavailable, fall back to running the relevant tests. Capture the output. Tests are weaker evidence but still show behavior.

### When nothing else fits → be creative

Find another way: run a CLI tool, inspect a log, diff before/after state, exercise the code directly with a script. The goal is always to give a human something concrete to look at — not a description, but actual output.
