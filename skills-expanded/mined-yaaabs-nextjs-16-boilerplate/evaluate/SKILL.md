---
name: evaluate
description: Self-review a change before declaring it finished. Use after implementing any feature or fix, before committing or reporting completion.
---

# Evaluate

Never declare work finished on the strength of "it compiles." Evaluate every change
against this checklist and report honestly what was and wasn't verified.

## 1. Run the gates (non-negotiable)

```bash
npm run lint
npm run type-check
npm run test
npm run format:check
```

All four must pass. These are the same checks the pre-commit hook enforces — running them
yourself avoids a blocked commit.

## 2. Review your own diff

Read the full diff as if reviewing a stranger's PR:

- Does every changed line serve the stated goal? Revert drive-by edits.
- Any leftover `console.log`, commented-out code, TODO, unused import, or dead file?
- Did you duplicate something that already exists in `src/components/` or `src/lib/`?
- Do new names read clearly at the call site?

## 3. Exercise the behavior

Tests passing is not the same as the feature working:

- New/changed page or component → run `npm run dev` and load the route.
- New logic → add or update a test in `src/__tests__/` (or co-located `*.test.tsx`) that
  fails without your change.
- Changed config → run the affected command and confirm the new behavior.

## 4. Check the blast radius

- Does the change affect other routes, shared components, or global CSS?
- Server/client boundary still correct? (No secrets or server-only code in client
  components.)
- Works in both light and dark mode if it touches UI?

## 5. Report truthfully

State what you verified and how. If something is untested or uncertain, say so
explicitly — never imply verification that didn't happen.
