---
name: oh-my-design
description: |
  Use this skill when the user asks to design / mock up / prototype a UI,
  iterate on visual design, compare visual candidates, or explore visual
  approaches before implementation. Triggered by phrases like "design a UI",
  "mockup", "prototype the screen", "give me 3 visual options", "make it
  look like…", or any request that is fundamentally about look-and-feel
  rather than business logic.

  The skill writes React 18 prototypes under `<cwd>/.design/<slug>/`,
  hands the user a Tweaks panel to pick / iterate, and returns the
  selection plus a self-describing manifest the next agent can implement
  against.

  DO NOT trigger for: refactoring, debugging business logic, code review of
  existing UI code, or generic "make a website" requests where production
  code in a specific framework is wanted — those are coding tasks, not
  design tasks.
---

# oh-my-design

## Engineering rules

1. React 18 + standard TSX, esbuild on every shoot/serve. No UMD, no
   Babel-standalone, no importmap. Write it like a real React project.
2. Output to `<cwd>/.design/<YYYY-MM-DD-HHMM>-<slug>/` (flat, no nested
   `project/`). Never inside the skill directory, never in the user's
   source tree. `<slug>` is lowercase-kebab, ≤ 32 chars.
3. `shots/` is for the agent's eyes only. When implementing, read source
   (`variants.tsx` etc.), not screenshots.
4. `panel/` is the protocol core. `App.tsx` must `import { Tweaks } from
   '@panel/Tweaks'` and mount it via `createPortal` into `#tweaks`. Schema
   in `panel/types.ts`. `examples/` is structural reference (mount points,
   file naming, types) — **never copy variant content, theme tokens,
   frame/theme picker schema, or aesthetic choices from it.** Aesthetic
   direction comes from the user, not examples.

## Behavioral contracts

### Screenshot routing

Self-produced screenshots: **always delegate, never self-evaluate** (self-preference bias).
User-supplied images: read or delegate based on context.

### Candidate count

Match the task — reproducing a mockup → 1 (don't manufacture variants),
exploring directions → multiple, unclear → ask. Don't default to a number.

### Subagent role

Subagents may do any task **except L5 aesthetic judgment** — that belongs
to the user. LLMs have documented self-preference bias when judging their
own outputs (arXiv:2410.21819).

## Flow

### 1. Clarify

Ask follow-up questions only when needed; skip if the request is already concrete.

### 2. Scaffold

```
<cwd>/.design/<YYYY-MM-DD-HHMM>-<slug>/
├── README.md       # written by agent at ship time (playbook ship-time README)
├── App.tsx         # esbuild entry — imports Tweaks from @panel/Tweaks
├── index.html      # must contain <div id="root"> + <div id="tweaks">
│                   # and <link rel="stylesheet" href="/__panel/tweaks.css">
├── config.json     # matches panel/types.ts:UIPrototypeConfig
├── variants.tsx    # candidate components (or organize however you like)
├── frames/         # if you use frames (optional — your call per task)
├── notes/          # distilled insight (1 sentence per file, named by topic)
├── drafts/         # unrefined material; dump freely, promote to notes/ when distillable
├── uploads/        # user-supplied reference images, if any
├── shots/          # populated by shoot.ts
├── app.js          # esbuild output, gitignored
└── selected.json   # written by serve.ts on user submit
```

**Axis-inversion check**: before writing `config.json`, list each axis
value (frames / themes / variants), trace each to either (a) user-stated
need or (b) task constraint. If a value traces back to `examples/`, drop
or reframe it — `examples/` is not your task spec.

### 3. Write candidates

Produce variants per the Candidate count rule above. The shape of each
variant component, file split, naming, styling, frame use — your call,
driven by the task. The protocol contract is in `panel/types.ts`; your
`config.json` must match `UIPrototypeConfig`.

### 4. Self-screenshot

```bash
node <skill-root>/lib/shoot.ts <project-dir>
```

`<skill-root>` is wherever this skill is installed. Outputs PNGs to `<project-dir>/shots/`.

### 5. Self-critique

Delegate review of every PNG in `shots/` to a subagent (Screenshot routing —
self-produced images always delegate). Document findings in
`notes/self-critique-<step>.md`.

### 6. Hand to user

```bash
node <skill-root>/lib/serve.ts <project-dir>
```

Prints the URL to stderr (random OS-assigned port). Process stays alive until
the user submits (`selected.json` written → server exits 0) or Ctrl-C (exit 130).

### 7. Iterate or finalize

- `action === "iterate"` → back to step 3 with selection + feedback as new
  constraints. Move discards into `drafts/`, sediment lessons into `notes/`.
- `action === "ship"` → read `playbook.md` and write `<slug>/README.md`
  per its ship-time README prompt (a prompt, not a template — compose
  from full conversation context). Skill ends. Return slug path,
  selection (variant + frame + theme), and a one-sentence summary.
