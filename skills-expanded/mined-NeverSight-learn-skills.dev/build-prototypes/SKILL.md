---
name: build-prototypes
description: Stage 4. Generates N (default 3) wireframe alternatives in parallel via the Designer subagent, then dispatches Critic + User Advocate + Engineer per alternative for parallel critique, then asks the Designer to evolve each. Writes 03-prototypes/alt-*/ + index.html landing page.
---

# $build-prototypes — stage 4: parallel prototype generation with critique evolution

## Inputs

- `context/*`
- `ideas/<slug>/02-scope.md`

## Refuse if

- `02-scope.md` missing (run `$document-scope`)

## Vendoring assets (one-time per ideas repo)

1. Check if `<ideas-repo>/.proto-maker-assets/` exists and contains
   `pico.min.css`, `components.css`, `annotations.js`.
2. If not, copy them from the proto-maker installation's
   `templates/wireframe-base/` directory:
   ```bash
   mkdir -p .proto-maker-assets
   cp "$PROTO_MAKER_HOME/templates/wireframe-base/pico.min.css" .proto-maker-assets/
   cp "$PROTO_MAKER_HOME/templates/wireframe-base/components.css" .proto-maker-assets/
   cp "$PROTO_MAKER_HOME/templates/wireframe-base/annotations.js" .proto-maker-assets/
   ```
   `$PROTO_MAKER_HOME` is set by the installer (Plan 4) to the install root
   (e.g., `~/.proto-maker/` or `%USERPROFILE%\proto-maker\`).

## Process

1. Ask the PM: "How many prototype alternatives? (default 3)" Accept 2–5.
2. For each alternative, ask the PM for an "angle" — a short label like
   "minimalist", "guided", "power-user", "mobile-first". Suggest options if
   the PM is stuck. Validate they're meaningfully distinct.
3. Convert each angle to a folder name: `alt-<index>-<angle-slug>`.
4. Create `ideas/<slug>/03-prototypes/alt-*/` directories.

### v1 round (parallel)

5. Dispatch N `designer` subagents IN PARALLEL, one per alternative. Each gets:
   - The ideas-repo root path
   - Its alternative folder path
   - Its assigned angle
   - Full text of `context/*` and `02-scope.md`
   - "v1 round" instruction (no critiques yet)

6. Wait for all designers. Confirm each produced `index.html`, screen files,
   and a DESIGN-LOG.md skeleton.

### Critique round (parallel)

7. For each of the N alternatives, dispatch THREE subagents in parallel:
   - `critic` writing to `<alt>/critiques/critic.md`
   - `user-advocate` writing to `<alt>/critiques/user-advocate.md`
   - `engineer` writing to `<alt>/critiques/engineer.md`

   That's 3N parallel invocations total.

8. Wait for all 3N. Retry any that returned garbage per AGENTS.md tension
   protocol.

### Evolution round (parallel)

9. Dispatch N `designer` subagents IN PARALLEL again, each reading its
   alternative's three critique memos. Each updates the screen HTML AND fills
   in DESIGN-LOG.md sections (Critiques received, Changes made, Critiques NOT
   addressed, Unresolved tensions).

### Landing page

10. Write `ideas/<slug>/03-prototypes/index.html` — a static landing page
    listing all N alternatives with one-line descriptions and links to each
    alternative's `index.html`. Use the `mock-card` component from
    `components.css`.

## Output

After completion, the folder structure is:

```
03-prototypes/
  index.html
  alt-1-<angle>/
    index.html
    screen-*.html
    DESIGN-LOG.md
    critiques/
      critic.md
      user-advocate.md
      engineer.md
  alt-2-...
  alt-3-...
```

## Done

Tell PM:
"Prototypes built. To review:
1. Run `$preview` to start the local server (if not already running).
2. Open http://127.0.0.1:4788/ideas/<slug>/03-prototypes/index.html
3. Click through each alternative.
4. When ready, run `$review-prototypes` to capture feedback and pick a winner."
