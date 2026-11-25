---
name: lovable-prompting-playbook
description: >-
  Use when planning a session in Lovable, breaking a feature into prompts,
  asking Lovable to refactor or debug, or writing a backlog of Lovable prompts.
  Not when actually executing inside Lovable — this guides how to phrase work,
  not the work itself.
---

# Lovable prompting playbook

Lovable does best with **small, specific, verifiable** prompts. This skill helps you (or another agent) write prompts that ship.

## Anatomy of a good Lovable prompt

```
[Context]   What part of the app, which files or routes.
[Goal]      What "done" looks like in user-visible terms.
[Approach]  Optional. Pick stack / pattern if it matters.
[Limits]    What NOT to change.
[Verify]    How you'll check it works.
```

Example:

> On the `/dashboard` route, add a "Revenue (30d)" KPI card to the top row, using `useRevenue30d` (already exists). Show value, % delta, and a sparkline. Do not touch the other cards. I'll verify by loading the dashboard and comparing the number to Stripe.

## Sequence work into prompts

Break a feature into 3–7 prompts, each shippable on its own:

1. **Schema** — tables, RLS, types (`migration-playbook`).
2. **API** — fetchers + hooks (`typed-api-hooks-forms`).
3. **UI shell** — empty/loading/error layout (`error-states-and-empty-ui`).
4. **Wiring** — connect UI to hooks.
5. **Edge cases** — auth, permissions, validation.
6. **Polish** — copy, a11y, mobile.

After each prompt, review the chat diff before moving on.

## When Lovable goes off course

- "Revert to the previous version and try again, keeping `X` unchanged."
- "Show me only the diff for `path/to/file.tsx`."
- "Stop. Summarize what you changed in the last 3 messages before continuing."
- Use a **skill invocation** (`/refactor-safe-diff`) to constrain scope.

## Pair prompts with skills

| Task | Skills to invoke |
|------|------------------|
| New feature with Supabase | `/supabase-database-design` then `/typed-api-hooks-forms` |
| New form | `/typed-api-hooks-forms` (covers Zod + RHF) |
| Stripe webhook | `/stripe-payment-webhooks` + `/payment-webhook-idempotency` |
| Before launch | `/lovable-ship-checklist` |
| Slow page | `/performance-budget` |

## Phrases that work well

- "Implement X. Do not change Y."
- "Add a checklist comment in the PR description listing every file you touched."
- "If you are unsure between two approaches, ask me before writing code."
- "Reuse the existing `useFoo` hook; do not create a duplicate."

## Phrases that cause trouble

- "Improve the app." — undefined target.
- "Refactor everything." — invites scope creep; use `/refactor-safe-diff` with explicit files.
- "Add a few small fixes." — bundle multiple things; you'll lose track of regressions.

## Workspace setup recommendations

- Add **knowledge** entries for: stack, brand, banned patterns (`any`, inline Supabase in components).
- Add this repo's skills to your workspace and let descriptions trigger them automatically.
- Keep prompts in a note (Linear, Notion, or `prompts.md`) so they can be re-run on a new branch.

## Avoid

- Mega-prompts that mix schema, UI, billing, and copy.
- Trusting Lovable to "remember" earlier sessions — assume zero memory across chats.
- Letting failing diffs accumulate; revert early.
