---
name: Learn-codebase
description: Read an existing product's code and extract its conventions, voice, design choices, and values into a draft profile + a project-specific skill. Use when importing an existing product into plsBuild OS instead of starting fresh. Adapts to Claude Code, claude.ai, and Cowork.
---

# /learn-codebase

Use this when you have an existing product and want plsBuild OS to understand it — not just install cleanly, but actually know your voice, your design, your stack conventions, and your non-negotiables.

This skill reads the codebase, extracts the stuff that matters, and drafts two things for you:

1. A filled-in `my-profile.md` (or updates to one you already have)
2. A project-specific skill for this product, saved to `skills/your-product-name.md`

You review. You correct. You approve. Nothing is written without confirmation.

---

## Which surface are you on?

**Claude Code**
You have full file access. Read the repo directly — README, CLAUDE.md, package.json, 5–10 representative components. Write the draft profile and project skill to disk after the user approves each one.

**claude.ai chat**
You can't read files. Ask the user to paste the specific files you need: README first, then package.json, then 3–5 representative UI components, then one page. Generate the draft profile and project skill as copy-ready blocks. Tell the user exactly where to save each one.

**Cowork**
You have workspace access. Read the open folder directly, same as Code. Write drafts back to the workspace after user approval. Don't overwrite an existing `my-profile.md` without confirming first.

---

## When to use this

- You're onboarding an existing product into plsBuild OS
- You've been building for a while and your profile doesn't reflect how you actually work
- You want to capture the "tribal knowledge" of a codebase — the stuff a new collaborator (human or AI) wouldn't know without being told

Skip this if you're starting a brand new project. Use the blank `my-profile.md` template instead.

---

## Before you run this

Be in (or have access to) the root of the product's repo.

If there are uncommitted changes or untracked files you're mid-session on, commit or stash first. This skill only reads, doesn't write to your source code, but you want a clean signal.

---

## Process

### Step 1 — Confirm the scope

Ask the user:

```
I'll read this codebase and draft:
  1. A my-profile.md for you (or updates to your existing one)
  2. A project-specific skill for this product

I'll ask before writing anything. This usually takes 15–20 minutes with your input.

Ready to start? (yes / skip profile / skip project skill)
```

### Step 2 — Read the obvious signals

Read these files first, in this order:

1. `README.md` at the root
2. `CLAUDE.md` at the root (if it exists)
3. `package.json` (stack signal)
4. `vercel.json`, `netlify.toml`, `vite.config.*` (deploy + build signal)
5. `tailwind.config.*`, any `globals.css` or equivalent (design signal)
6. 3–5 representative components from the main UI folder
7. 1–2 pages from the main pages folder
8. Any folder named `spec/`, `specs/`, `docs/`, or `plsbuild/`

If the user already has a `my-profile.md`, read that too and flag what differs from what you find in the code.

Don't read test files, config boilerplate, or node_modules. Skip anything over 500 lines unless it's clearly the main file.

### Step 3 — Extract four things

For each, form a hypothesis and prepare to ask the user to confirm.

**Voice.** Read README, landing copy, UI text, button labels, error messages. What's the tone? (Warm vs clinical. Direct vs marketing. Playful vs formal.) Give three adjectives.

**Design.** Read CSS/Tailwind classes in the main components. Identify: primary color(s), secondary/accent color(s), font families (serif? sans? combo?), border-radius pattern, spacing rhythm (tight vs airy). Give a 3-word design descriptor plus the palette.

**Stack conventions.** From package.json and configs: frontend framework, state management, styling, backend, database, auth, deploy, payments, AI. Also note non-default choices the user made.

**Values and non-negotiables.** Look for comments, CLAUDE.md content, commit messages, code style (TypeScript strictness, accessibility, test coverage). What does this codebase treat as non-negotiable that a default template wouldn't?

### Step 4 — Present findings, one section at a time

Don't dump everything at once. Walk through the four extractions in order. For each:

```
Here's what I read from the codebase on [voice / design / stack / values]:

[Your finding, 3–5 lines, concrete and specific]

Does this match how you'd describe it? Options:
- Yes, use this
- Adjust: [user rewrites]
- No, rewrite this part
```

Wait for user response before moving to the next section.

### Step 5 — Draft the profile

Using the four confirmed extractions, draft `my-profile.md` following the template structure. Show it to the user.

```
Here's the draft profile. Three things to check:

1. The "Who I am" section — one sentence, does this match?
2. The stack defaults — anything missing?
3. The "Push me on" line — is this an actual blindspot, or did I pattern-match wrong?

Approve / adjust / rewrite?
```

Once approved, save to `profile/my-profile.md` (or wherever the user's profile lives).

### Step 6 — Draft the project-specific skill

Project skills capture stuff that only applies to this product. Format:

```markdown
---
name: [Product Name]
description: Context for working on [product name] specifically. [What it is in one line].
---

# /[product-name]

## What this product is
[Two or three sentences. What it does, who it's for, what problem it solves.]

## Non-negotiables for this product
[Rules specific to this product. Not general rules — ones that only apply here.]

## Stack (differs from my defaults)
[Only list things that differ from the user's profile defaults. If everything matches, write "Matches my defaults."]

## Design direction for this product
[3 words + color palette + type + specific design reference products]

## Voice for this product
[How this product speaks to its users. What to write and what to never write.]

## Current focus (check the spec for detail)
[One sentence on what's being built right now.]
```

Show the draft. Get approval. Save to `skills/[product-slug].md` or wherever project skills live.

### Step 7 — Wrap up

```
Done. Two files ready:
  1. my-profile.md — your personal profile, informed by this codebase
  2. skills/[product-name].md — product-specific context Claude loads when working on this product

Next steps:
  1. Spot-check both files. Edit anything that feels off.
  2. Run /spec to shape the current living spec for this product.
  3. Commit the plsbuild/ folder to your repo (or keep it local if you prefer).
```

---

## What this skill does NOT do

- Write code. This is a reading and drafting skill only.
- Modify your source files. It only creates or updates profile and skill files.
- Guess when unsure. If the codebase signal is weak or contradictory, ask the user instead of making it up.
- Produce a spec. Run `/spec` after this for the living spec.

---

## Graduation pattern

Once you're in the workflow layer, the outputs move too: the product-specific skill becomes a page in your product hub (Notion, Linear, etc.), and the profile stays local.

The reading pattern stays the same. Re-run this skill any time a product has drifted enough that the old profile or project skill no longer describes how you actually work.
