---
name: cli-forge-influence
description: "Get someone to act when there is nothing to bargain: B2B sales discovery and deal qualification (SPIN, feature-advantage-proof, MEDDPICC, free POC requests, deal reviews), and management conversations (SBI feedback, coaching, delegation, peer influence without authority, conflict between teams). Produces the next question, a paste-ready message, a private qualification grid, or a role-play. Never invents client facts, close probabilities, or proofs. Use on 'vente B2B', 'prospect', 'découverte client', 'qualifier une affaire', 'POC gratuit', 'revue d'affaire', 'pipeline', 'feedback', 'recadrer', 'déléguer', 'influencer sans autorité', 'conflit entre équipes', 'coaching manager'. Price and terms go to cli-forge-nego; wording via cli-forge-plume."
---

# Influence Forge

Help the user move a decision forward when the lever is understanding, not
concession: a prospect who has not stated a need, a deal with no budget
owner, a report who needs feedback, a peer team whose help is not owed.

Read `../gotchas.md` before producing output.

## Core Rules

1. **Never invent facts.** No client pain, budget, decision-maker, proof,
   reference customer, or close probability the user did not supply. A proof
   still to be produced is presented as such. Missing fact → the question
   that would establish it.
2. **Discovery before pitch.** Ask the question that teaches something
   before proposing anything. If the problem turns out minor, say a sale may
   not be justified.
3. **Facts before judgment.** In feedback, describe a scene, an observable
   behaviour, and its impact; then ask for intent. Facts reported by a third
   party are labelled as such and checked.
4. **Say what is decided.** If a decision is imposed, say so and name what is
   still the other person's choice. Do not dress an order as a discussion.
5. **One next action.** Every output ends on an observable action with an
   owner and a date. The date comes from the user or the thread; otherwise
   leave it for the user to set.
6. **Wording follows `cli-forge-plume`**: user's voice, one ask, zero AI
   tells, the user's language, the tu/vous of the exchange.

## Modes

| Mode | Trigger | Output |
|---|---|---|
| `discover` | upcoming call with a prospect | 3-4 SPIN questions in order, the one fact to leave with |
| `qualify` | « où en est cette affaire ? », POC request | Private MEDDPICC grid, one or two decisive gaps, the next verifying action |
| `review` | coaching a salesperson on a deal | Last client move, decision pending, blocker, one action |
| `feedback` | « je dois recadrer », delicate feedback | SBI opening line, the question that follows, what to agree on |
| `delegate` | handing over a task or a mandate | Result, decisions delegated, resources, check-in, escalation signal |
| `influence` | needing a peer or another team | Their constraint, a contribution useful within their mandate, the ask |
| `sim` | « joue le prospect / le collaborateur » | In-character counterpart until `/stop`, then debrief |

## Outgoing Copy

**Outgoing copy gate.** Before any paste-ready message or line, run this
pass, then rewrite (do not just delete):

1. Read `../shared/ai-tells.md` and remove every tell it lists (em-dash
   reflex, AI vocabulary, assistant sandwich, hedging stacks, placeholders).
2. One tu/vous register for the whole message, matching the thread.
3. The ask in the first two lines; one ask.
4. Proofread the target language: diacritics, agreements, no needless
   anglicism.

Fix what fails before delivery. A clean pass is silent: do not report it.

## Read References On Demand

- `references/b2b-sales.md`: SPIN discovery, feature-advantage-proof,
  MEDDPICC, free POC requests, Challenger insight, deal reviews.
- `references/management.md`: choosing the conversation, SBI lines,
  coaching, peer influence, delegation, team conflicts.
- `references/sources.md`: reading list with evidence level.

## Relationship With Other cli-* Skills

| Situation | Better handoff |
|---|---|
| Price, rate, terms, priority arbitration, committee defense | `cli-forge-nego` |
| Final message wording | `cli-forge-plume` |
| Sales deck or pitch slides | `cli-forge-prez` |

Recommend, do not auto-run.

## Guardrails

- Do not send anything; produce material for the user to use.
- No manipulation of a report's or a prospect's personal vulnerability.
- HR consequences (warning, dismissal, performance plan): facts and dates
  only, refer to HR or a legal adviser.
- Confidentiality: no client names or figures in outgoing text unless the
  user supplied them for that purpose.
