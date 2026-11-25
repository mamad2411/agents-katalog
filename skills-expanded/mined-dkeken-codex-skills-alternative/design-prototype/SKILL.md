---
name: design-prototype
description: Assemble a clickable, runnable prototype from screens/components — wiring navigation, state, and interactions so a team can actually click through it. Use when the user says "make it clickable", "build a prototype", "wire up the flow", "interactive prototype", "make the screens navigate", or has static screens that need to come alive. Part of the Product Design set. Verifies interactions with a browser tool.
---

# Design — Prototype

Turn static screens into a working clickable flow that demonstrates the experience end to end. A prototype's job is to let someone *experience the flow* and give feedback — not to be production-hardened. Stubs are fine and expected; broken navigation is not.

## When to use
- You have screens/components (from image-to-code, url-to-code, or ideate) and need them connected.
- "Make it clickable", "wire the flow", "let me click through it".
- Validating a UX flow with stakeholders before real backend work.

## When NOT to use
- No screens exist yet → build them first (`design-image-to-code` / `design-url-to-code`).
- You need production code with real data/auth — that's an engineering task, not a prototype.
- Just checking a built prototype against the design → `design-qa`.

## Inputs
- The **screens/components** to connect.
- The **flow to demonstrate**: happy path + key states.
- `./design/context.md` for the JTBD (the flow should make *that* easy).

## Workflow
1. **Map the flow graph**: screens are nodes, actions are edges (click → navigate, submit → state change). Write it down before wiring.
2. **Wire routing/navigation** between screens.
3. **Add interaction states**: hover, active, disabled, loading, empty, error, success. Cover at least the **happy path + one error state** (the most-skipped, most-important state).
4. **Stub data** so it's clickable without a backend; clearly mark where real data plugs in.
5. **Verify**: drive the whole happy path in a browser-automation tool — click every step, confirm nothing dead-ends. Fix what breaks.
6. Keep it **runnable with one command**.

## Worked example
Flow (JTBD: create first project in <2 min): Welcome → Choose template → Name it → Dashboard.
```
flow graph:
 Welcome --[Get started]--> Template --[select]--> Name --[Create]--> Dashboard
 Name --[empty submit]--> Name(error: "Name required")
 Template --[back]--> Welcome
states wired: hover on cards, loading on Create (300ms stub), error on empty name,
 success → Dashboard with the new project card
stubs: templates = 3 fixtures; "Create" writes to in-memory store (TODO: real API)
verify (browser): clicked Welcome→Template→Name→Create→Dashboard ✓;
 empty-name error shows ✓; back nav works ✓; no dead ends
run: `npm install && npm run dev` → :5173
```

## Quality bar / Definition of done
- Full happy path is clickable end to end.
- At least one error/empty state is present and reachable.
- No dead ends or broken links.
- Runs locally; build + typecheck clean.
- A browser walkthrough of the happy path passes.

## Common pitfalls
- **Happy-path only** — skipping error/empty/loading states; those are where real feedback comes from.
- **Dead ends** — a button that goes nowhere kills the demo. Walk every path.
- **Over-engineering** — wiring a real backend/auth for a prototype. Stub it, mark the TODO.
- **Style drift** — re-styling screens during wiring so they no longer match the locked direction.
- **No verification** — assuming it works without clicking through it.

## Handoff
Working prototype → `design-qa` (conformance check vs the design + requirements) → `design-share` (publish for review). Don't share before QA on anything stakeholder-facing.

## Tooling
Needs a **browser-automation tool** to verify the flow by clicking through it. Without one, wire carefully and manually note that the walkthrough is unverified.
