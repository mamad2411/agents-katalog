---
name: product-hooks
description: Design sandbox onboarding, operational transparency, IKEA co-creation, Day 1-30 habit graduation, and humane offboarding. Sub-skill: load only when routed from the hook-everything entry skill, not for general writing or editing.
---
# Product & Project Hooks (Full-Lifecycle Architecture)

Make users adopt, return, and advocate for your product or project because it compounds their competence and psychological ownership - never because it traps them with dark patterns.

---

## Phase 1: First-60-Seconds Activation (The Velvet Rope Sandbox)

Many products lose 60-80% of visitors at the signup wall (working heuristic, verify with your own data) because they demand high friction (email verification, password rules, credit card, company profile) when the user's motivation and trust are still near zero (`Fogg B=MAP`).

Combine 4 mechanisms simultaneously in the first 60 seconds (`Chord 2`):

1. **Deferred Registration (Value Before Auth)** drops the visitor directly into an interactive canvas, live query runner, or pre-populated template. Let them perform their first real action anonymously, and ask for an account *only* to save, export, or deploy the artifact they just created.
2. **Operational Transparency (`M22`, Buell & Norton 2011)** displays the real domain steps (`Parsing 14 AST nodes -> Checking circular imports -> 2 warnings found`) over 1.5-2.5 seconds rather than a generic spinner when your system processes input.
3. **Low-Failure Co-Creation (`M12`, IKEA Effect)** gives the user 2 effortless choices (e.g., clicking a filter pill, toggling a formatting rule, picking a column mapping) that immediately transform the preview. Psychological ownership forms the second their input shapes the output.
4. **Credible Endowed Progress (`M6`, Nunes & Dreze 2006)** counts their anonymous sandbox actions as steps 1 and 2 of onboarding (`"2 of 3 setup steps complete"`).

---

## Phase 2: Day-1 to Day-30 Habit Graduation Architecture

A hook that works on Day 1 (onboarding checklists, endowed progress bars) becomes annoying clutter by Day 14. Graduate your product hooks across 3 lifecycle stages:

| Lifecycle Stage | Primary Psychological Goal | Active Hook Mechanism | What to Retire / Hide |
|---|---|---|---|
| **Stage 1: Day 1 (Activation)** | Reach the first concrete "Aha" outcome in `< 60 seconds`. | **IKEA Co-Creation (`M12`)** + **Endowed Progress (`M6`)** + **Smart Defaults (`M8`)**. | Hide advanced settings, billing tiers, and secondary navigation (`Choice Overload M28`). |
| **Stage 2: Day 3 - Day 14 (Habit Formation)** | Bridge the gap between external prompts and internal triggers. | **Stateful Ovsiankina Resumption (`M9`)** + **Plan-to-Finish Snooze** + **Competence Mirrors (`M16`)**. | Retire the onboarding progress bar immediately once complete; never leave a dead widget on the dashboard. |
| **Stage 3: Day 30+ (Power User Mastery)** | Compounding investment and speed/flow (`< 400ms` Doherty Threshold). | **Keyboard/Macro Shortcuts**, **Compounding Stored Assets** (custom rules, historical baselines), and **Variable Domain Insights (`M14`)**. | Silence all beginner tooltips, tour prompts, and celebration modals. |

---

## Phase 3: Multiplayer & Collaborative Network Hooks (Relatedness `M16`)

In B2B tools, developer projects, and collaborative apps, the most natural growth hook is **Artifact-Driven Relatedness** - never "Invite 5 friends to get dark mode" spam:

1. **The Read-Only Interactive Share Link** lets a user share a live URL for any chart, diff, or doc where teammates can toggle filters or leave a comment **without logging in**.
2. **Co-Created Hand-Off Loops** route User B directly to row 14 with a 1-click action button (`Ovsiankina M9` + `Fogg Ability M5`) whenever User A tags them on a specific unresolved item (`"Can you approve row 14?"`).

---

## Phase 4: Ethical Upgrade Triggers & Humane Offboarding (Anti-Roach-Motel)

1. **Competence-Triggered Upsells (`M16` + `M13`)** avoid interrupting a user mid-workflow with a paywall modal. Trigger upgrade options immediately *after* the user completes a high-value action (the Peak-End peak), framing the paid tier around the exact volume or speed they just proved they need (`"You just reconciled 48 payouts in 12 seconds. Free covers 50/month; enable unlimited batches for $19/mo"`).
2. **The Humane Pause & Offboarding Hook (`M19` Benevolence + `M26` Regret Regulation)** makes canceling or pausing a subscription a 1-click button in Settings. Offer a **1-Click "Hibernate Workspace (Free)"** option that freezes billing while preserving all custom rules and data read-only. Users who hibernate instead of rage-quitting often return at up to 3x the rate when their next project starts (working heuristic, verify with your own data).
