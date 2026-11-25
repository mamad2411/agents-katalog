---
name: solana-onboarding
description: Diagnoses and fixes the entry experience of Solana products, wallets, DEXs, aggregators and lending apps, using components calibrated on a heuristic study of 13 apps. Use when the user is designing, reviewing or implementing onboarding, wallet creation or import, transaction confirmations, error states, identity verification, or when they paste an error code or ask why users abandon a flow.
license: MIT
compatibility: React 18+, Tailwind CSS, and lucide-react for the copy-in components. The skill itself has no runtime requirement.
metadata:
  author: draaujpeg
  version: "1.2.0"
---

# Solana onboarding

<context>
A heuristic study of 13 Solana products found the same handful of failures in
almost all of them. Not idiosyncratic bugs: patterns. Seed phrases shown with no
bridge to anything the user already understands, flows that end by dropping
someone into an empty screen, help that lives in another tab, jargon with no
explanation at the point of use, errors that diagnose without teaching, gates
that arrive as a surprise, and irreversible actions confirmed as casually as
reversible ones.

This skill carries the components that answer each of those, and the rules for
choosing between them. Both are calibrated on evidence: every rule exists
because something was measured failing without it.

Components are copied into the user's project. They are not a dependency, there
is nothing to keep updated, and the user owns and edits the result.
</context>

<objective>
Input: a codebase, a description of a product, an error code, or a question.

Output: either a diagnosis of what is missing, or components installed and wired
into the project, with the wording agreed rather than assumed.
</objective>

<rules>
Always:

- Read the reference for a pattern before proposing anything about it. The rules
  are not derivable from the components.
- Propose copy and wait for the user to confirm, edit or replace it. Product
  wording is theirs, and a plausible guess survives review by looking finished.
- Say when a screen should not exist. Confirming everything trains people to
  click through, which is what makes the one dialog that mattered invisible.
- Run the project's build after installing anything, and fix what you broke.

Never:

- Never invent a component. If nothing here fits, say so and describe what would.
- Never add a copy-to-clipboard control for a recovery phrase.
- Never assert the reason an identity verification was rejected. The reasoning
  is in `components/kyc-rejection-causes.ts`.
- Never write a literal colour into a component. Everything paints with `--so-*`
  tokens, which is what lets a copied component adopt the host brand.
</rules>

<process>

## Step 1. Work out what is being asked

Route on what the user gave you, not on the words they used. People rarely name
the pattern they need.

| What arrived | Where to go |
|---|---|
| An error string or code, or a screenshot of one | `references/error-codes.md` |
| "Review our onboarding", a repository, a flow to critique | Audit mode, below |
| "I need a confirmation for X", or a described screen | Implement mode, below |
| A term the product uses without explaining | `references/glossary.md` |
| Anything about creating, importing or social login | `references/custody-paths.md` first |

If the request is broad, run the audit first. Implementing without diagnosing
produces a well-built screen in the wrong place.

## Step 2. Load only what the task needs

Every reference is written to be applied on its own.

| File | Holds |
|---|---|
| `references/patterns/` | One file per pattern: the gap it closes, when it applies, its rules, the copy to propose |
| `references/risk-classification.md` | Whether an action needs a confirmation, and which of the four |
| `references/custody-paths.md` | Create, social login or import, and where the kit stops |
| `references/error-codes.md` | An error code, to the component that answers it |
| `references/glossary.md` | The terms the kit explains, and where the long version lives |
| `references/copy-rules.md` | How to propose wording, and what is not yours to change |
| `references/installing.md` | Copying components into a project without breaking it |
| `methodology/audit-grid.md` | The 30 questions the research scored, for audit mode |

## Audit mode

Diagnose before touching anything.

1. Find the entry flow: wallet connection, account creation, the first
   transaction, and any gate between them. Ask if you cannot tell.
2. Score it against `methodology/audit-grid.md`. Severity is calibrated by what
   a failure costs the user, not by how wrong it looks.
3. Look for the two failures that hide well: an irreversible action with no
   confirmation, and a confirmation a level below the action it guards. The
   second is more common and harder to see, because the screen looks considered.
4. Report gaps ordered by severity, each naming the pattern that closes it.
   Recommend, do not install.

Names in a codebase are candidates, not conclusions. Confirm before reporting.

## Implement mode

1. Identify the pattern. For a confirmation, run
   `references/risk-classification.md` first: it also answers "no dialog at all".
2. Read the project. Framework, styling, whether shadcn tokens exist, where
   components live, and what the product actually does. The wording depends on
   that last one.
3. Propose the copy and the blocks it needs. Say what you chose and why. Wait.
4. Install, following `references/installing.md`.
5. Build. Show it running if you can.

</process>

<state>
There is no state file. Each request stands alone, because a product's
onboarding is not a project with phases and the user may arrive at any point in
theirs.
</state>
