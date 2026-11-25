---
name: handoff-prompt
description: Draft a self-contained implementation prompt that an agent can execute with zero prior context. Use when the user says "draft a prompt", "write a handoff", "make a prompt I can copy-paste", "create a delegation brief", or wants to hand off a task to another agent, tool, or conversation.
metadata:
  author: epicenter
  version: '1.0'
---

# Handoff Prompt

Follow [writing-voice](../writing-voice/SKILL.md) for prose tone.

A handoff prompt is a self-contained delegation brief. The recipient agent has never seen this codebase, this conversation, or this context. Everything they need to execute must be in the prompt itself.

## When to Apply This Skill

Use this pattern when you need to:

- Draft a prompt the user will copy-paste into another agent, tool, or fresh conversation.
- Package codebase context so an agent can execute without exploration.
- Hand off a well-scoped task with explicit guardrails.
- Create a reusable prompt template for a recurring type of work.

## How It Differs from Specs

| Spec (`specification-writing`) | Handoff Prompt |
| --- | --- |
| Planning document, lives in `specs/*.md` | Communication artifact, lives in clipboard |
| Tracks progress with checkboxes | Single-shot execution |
| Assumes the reader has repo access and can explore | Assumes the reader has zero context |
| Leaves open questions for the implementer | Closes all questions—the recipient shouldn't need to ask |
| Written before work starts | Written when handing off work to another context |

A spec says "here's the plan." A handoff prompt says "here's everything you need to do it right now."

## The Prompt Structure

Every handoff prompt has six sections. Order matters—context before requirements, requirements before guardrails.

### 1. Task Statement (1-2 sentences)

What to build and where. Be specific about file paths.

```
Create an About page for OpenSidian at `apps/opensidian/src/routes/about/+page.svelte`.
This page explains the technical architecture to visitors and is linkable from the app toolbar.
```

Not: "Build a page that explains the app." The recipient needs exact locations.

### 2. Context Dump

Everything the recipient needs to understand the codebase without reading it. This is the most important section—it's what makes the prompt self-contained.

Include:

- **Relevant source code** — paste actual code snippets, not descriptions. If the data layer is 10 lines, paste those 10 lines.
- **Architecture summary** — how the pieces fit together, in 2-3 sentences.
- **File inventory** — what exists that the recipient will interact with (components, routes, state files).
- **Tech stack** — framework, UI library, styling approach, key dependencies.

```
## Context

The entire app's data layer is this one file (`src/lib/workspace.ts`):

\`\`\`typescript
// paste the actual code
\`\`\`

That's it. 10 lines. The workspace API provides: Yjs CRDT table storage, per-file Y.Doc
content documents, IndexedDB persistence, and an in-browser SQLite index.
```

Rules for context dumps:

- **Paste real code, not paraphrases.** "The workspace uses Yjs" is useless. The actual `createWorkspace()` call is useful.
- **Include file paths.** Every code snippet gets its source path.
- **Name the components that exist.** If there's a Toolbar, a FileTree, a TabBar—list them with paths.
- **State what's available.** If the UI library has Card, Badge, Separator—say so explicitly.

### 3. Design Requirements

Structured description of what to build. Use numbered sections or a clear hierarchy. Be exhaustive—the recipient can't ask clarifying questions.

For UI work, describe each section of the page/component with:
- What it contains
- What components to use
- What data it displays
- How it behaves

For logic work, describe:
- Input/output contracts
- Edge cases to handle
- Integration points with existing code

### 4. Available Tools and Components

Explicit inventory of what the recipient can use. Don't assume they know what's in the project.

```
## Available shadcn-svelte components

Import from `@epicenter/ui/{component}`. Available: `card`, `badge`, `separator`,
`accordion`, `tabs`, `button`, `alert`. Also `@lucide/svelte` for icons.
```

### 5. MUST DO

Non-negotiable requirements. Frame as explicit constraints, not suggestions.

```
## MUST DO
- Use only components from `@epicenter/ui/*` and `@lucide/svelte`
- Follow existing Svelte 5 runes patterns (`$props()`, `$derived`, `$state`)
- Use em dashes (closed, no spaces) per the project writing conventions
- Create no more than 3 files total
```

### 6. MUST NOT DO

Explicit anti-requirements. Block the most common ways agents go off-rails for this type of task.

```
## MUST NOT DO
- Do not install any new dependencies
- Do not modify any files outside of `apps/opensidian/`
- Do not use images or external assets
- Do not make the page feel like a SaaS landing page
```

Think about what the recipient might do wrong and preempt it.

## Drafting Process

When asked to create a handoff prompt:

1. **Gather context first.** Read the relevant files, understand the codebase patterns, check what components/tools are available. You can't write a self-contained prompt without knowing the details.

2. **Identify the recipient's blind spots.** What does someone need to know that isn't obvious? The tech stack, the import conventions, the existing patterns, the file structure.

3. **Paste, don't paraphrase.** Real code > descriptions of code. Real file paths > vague references. Real component names > "use the UI library."

4. **Close all decisions.** A spec can leave open questions. A handoff prompt cannot. If there's a choice to make (which component, which layout, which approach), make it in the prompt.

5. **Scope aggressively.** The tighter the scope, the better the output. "Create 3 files" beats "build the feature." "Modify only these 2 existing files" beats "update as needed."

6. **Test mentally.** Read the prompt as if you've never seen this codebase. Could you execute it? If you'd need to grep for something, that information should be in the prompt.

## Common Mistakes

### Too abstract

```
## Context
The app uses a workspace API built on Yjs CRDTs for data storage.
```

This tells the recipient nothing actionable. Paste the workspace setup code instead.

### Missing file paths

```
Create a new page component and link it from the toolbar.
```

Where? What's the toolbar file called? What's the routing convention? Be explicit.

### Assuming knowledge

```
Use the standard shadcn components for this.
```

Which ones? The recipient doesn't know what "standard" means in this project. List them.

### Leaving decisions open

```
You could use either a Card grid or an Accordion for this section—pick whichever works better.
```

Pick one. The recipient will waste time deliberating instead of building.

### Forgetting guardrails

Without MUST NOT DO, agents will:
- Install new dependencies
- Modify unrelated files
- Add features you didn't ask for
- Use patterns inconsistent with the codebase

Preempt this explicitly.

## Good vs Bad

### Good (self-contained, specific, closed)

```
Create `src/routes/about/+page.svelte`. Import `Card` from `@epicenter/ui/card`
and `Badge` from `@epicenter/ui/badge`. The page has 4 sections...

The workspace setup code is:
\`\`\`typescript
export const ws = createWorkspace({ id: 'opensidian', tables: { files: filesTable } })
  .withExtension('persistence', indexeddbPersistence)
\`\`\`

MUST NOT: install dependencies, modify files outside apps/opensidian/, use images.
```

### Bad (vague, open-ended, assumes context)

```
Create an about page for the app that explains the architecture.
Use whatever components make sense. Make it look good.
```

The good version works cold. The bad version requires a follow-up conversation.
