---
name: discover-domain
description: >-
  Use as the first step of a new project or area of a product, before any boundary or code,
  or when the user describes a business process to build. A light event storming in writing:
  actors, commands, domain events, policies, read models, external systems.
argument-hint: "[the needs, or the process to explore]"
allowed-tools:
  - Read
  - Write
  - Edit
---

# Discover the domain

Subject: `$ARGUMENTS` (otherwise the `## Needs` section of `docs/architecture/plan.md`)

Read the needs, and nothing of the code. The output is one file,
`docs/architecture/discovery.md`, that the owner can correct in five minutes.

## 1. Draft from the needs, then ask

Write the first version yourself from what was stated, then put to the owner only what the
needs do not say. Ask in batches of at most five questions, each one about a fact of the
business (what happens when a payment fails?), never about technique.

## 2. Find the elements, in this order

1. **Domain events**, first: what happens that the business cares about, in the past tense
   (`Order placed`, `Invoice issued`, `Payment refused`). Put them on a timeline. Hunt for the
   unhappy ones: refused, expired, cancelled, late.
2. **Commands**: what someone or something asks for, that causes each event (`Place order`).
   An event without a command is caused by time or by another event: say which.
3. **Actors**: who gives each command, by role, not by person. Include the system itself and
   time (every night, after 30 days).
4. **Policies**: "whenever X happened, then do Y". Each is a reaction that links an event to
   a command, often across a future boundary.
5. **Read models**: what an actor must see to decide to give a command (a list, a status, a
   total).
6. **External systems**: what exists outside and is called or listened to (payment provider,
   mail, an ERP), with what is expected of it.
7. **Rules and hot spots**: invariants heard on the way ("an order cannot be paid twice"),
   and every disagreement, unknown or word used with two meanings. Hot spots are kept, not
   resolved by guessing.

## 3. Write the artefact

```markdown
# Domain discovery

## Timeline
| # | Actor | Command | Domain event | Then (policy) | Needs to see (read model) |
|---|---|---|---|---|---|
| 1 | Customer | Place order | Order placed | whenever Order placed, Reserve stock | Catalogue, prices |

## External systems
| System | Used for | Direction | What happens when it is down |

## Rules heard
- An order cannot be paid twice.

## Words with several meanings
| Word | Meaning for whom |

## Hot spots
- <question>, who can answer
```

Keep the words of the business exactly, even when two people use two words for one thing:
that difference is what the next step needs. No class, no table, no technical noun.

## Done when

Put this to the owner: **does every need appear as a command and a domain event, in your
words, and is every disagreement listed as a hot spot?** On a yes, the next step is
`ddd-ts-kit:bounded-contexts`.
