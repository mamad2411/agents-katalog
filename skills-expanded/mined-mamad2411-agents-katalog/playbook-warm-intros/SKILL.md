---
name: playbook-warm-intros
description: Build prospect lists where the prospect is already one hop from the client, and write the line that says so. Seven members, each with its own source. Current-customer alumni is the priority member - everyone who ever worked at one of the client's customers or case-study companies and has since moved on. Triggers on "warm intro", "who do we know at that account", "they used to work at our customer", "alumni of our case study company", "shared investor angle", "who is in the same city as our rep", "did they visit our site". Outputs warm_intro_line plus a per-member evidence column.
---

# Playbook: Warm Intros

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the campaign's whole premise is that the prospect is **already one hop from the
client**, and you need both the list and the line. The strongest version, and the one to build first,
is *"you used to work at a company that is now our client's customer"*.

**Do not use when:** you want a second contact at an account you already email
(`playbook-name-to-other-prospects`), people who engaged with a competitor's or customer's posts
(`playbook-linkedin-engagement`), or companies similar to a seed set (`playbook-lookalikes`).

**One-line output:** `warm_intro_line = "you came up through Coca-Cola, who we work with now"`,
rendering as `Noticed you came up through Coca-Cola, who we work with now.`

## ⚠️ Status: sources probed, no line graded

**This is the least proven playbook in the library, and it is written that way deliberately.**

- **Member 2's source probe passed** — 20/20 rows carried a dated matched past experience, a profile
  URL and a city, and **15/20 had moved on.**
- **Member 5's source probe passed** — the investor filter returns a real result count.
- **No member has produced a graded `warm_intro_line`.**

**Everything below §3 is a build spec, not a measured path.** Treat the coverage and quality claims
as unverified until you run one.

## 1. A family, not one playbook

A warm-intro signal is any evidence that the prospect is already one hop from the client, so email 1
can lean on a real connection instead of a cold pitch.

**Seven members share the copy shape `warm_intro_line`. They do not share a data source.** So this is
one routing table plus one build recipe per member.

| # | Member | What it means | Status |
|---|---|---|---|
| 1 | **same-company alumni** | Everyone who **ever** worked at the case-study company and has since moved on | live, same build as 2 |
| 2 | **current-customer alumni** | The prospect used to work at one of the client's **current customers** | **live, top priority, build this first** |
| 3 | engagement overlap | The prospect engages with the same content the client's world does | live, but **routed to `playbook-linkedin-engagement`** |
| 4 | same metro | The prospect sits in the same city as the client, a named rep, or an upcoming trip | live |
| 5 | shared investor or advisor | A common investor, board member or advisor links the two companies | live |
| — | ~~mutual connection~~ | A first-degree connection in common | **deleted. Do not re-add it, do not prototype it** |
| 7 | event attendee | Both attended, spoke at or sponsored the same event | live as a **custom scrape every time. There is no reusable recipe and there will not be one** |
| 8 | website visitor | The prospect's company already visited the client's site | live as a **per-client toggle**, not a standing integration |

### Why member 1 was reframed, and why it matters

Member 1 originally meant *"overlapped in time with someone on the client's team"*. **That list is
always too small, and it never once got run.**

Reframed, it means **everyone who ever worked at the case-study company and has since moved on** —
which is a large, buildable list from the same source as member 2.

**The general lesson: a warm-intro definition that requires a time overlap between two specific
people produces a list too small to campaign on.** Widen to "worked there at all, and left" and the
same data source suddenly supports a real segment.

## 2. Output contract

| Field | Type | Example | Null? |
|---|---|---|---|
| `warm_intro_line` | string | `you came up through Coca-Cola, who we work with now` | yes, `""` |
| `warm_intro_member` | enum | `current_customer_alumni` | no |
| `warm_intro_evidence` | string, **QA only** | `Coca-Cola, Brand Manager, 2018-2021` | yes |

**Abstain value:** `""`.

**Keep the member field.** Seven members share one copy shape, and without it you cannot tell later
which angle actually produced replies — which is the only way this family gets narrowed to the two or
three members worth keeping.

### ⛔ Never name a real third party in copy without permission

The line says *"who we work with now"*, not *"we work with Coca-Cola"* — **unless the client has
explicitly approved naming that customer.**

Naming a client's customer in cold email is the client's decision, not yours, and it is the fastest
way to turn a clever campaign into an awkward phone call. **Default to the unnamed form.**

Note this is the same posture `playbook-lookalikes` takes with case-study companies, for the same
reason.

## 3. Build member 2 first

The source is a **people search with a past-company filter** set to the client's customer or
case-study companies.

What the probe confirmed on 20 rows:

- a **dated** matched past experience,
- a profile URL,
- a city,
- and **15 of 20 had moved on** — which is the population you actually want.

That last number is the one to plan from. **Roughly three quarters of "ever worked there" is "worked
there and left"**, and the rest are current employees who must be excluded (they are the customer's
staff, not prospects).

### The exclusions this family needs

Inherit them from `playbook-linkedin-engagement`, because the shape is identical:

- **Drop anyone currently employed by a source company.** They work for the client's customer; they
  are not a warm intro, they are the customer.
- **Never include the client's own domain** in the source set. If it appears, the list is wrong —
  stop.
- **Push the source companies onto the client's do-not-contact list**, so this run's exclusions
  persist into future lanes.

## 4. Verification

**Untested for the line.** Sources probed only. See the status box above.

**The first person to run a member owes the file:** a real fill rate, a graded sample of at least 10
lines, and the member name on every row.

## 5. Clay implementation

- **`clay-table.md`** — the labelling half as columns.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. The line

The line is short, and the copy risk is entirely in **what it names**, not in how it is written.

Shape: `you came up through <former employer>, who we work with now`.

Rules:

- Lowercase first word, no trailing period, no em dashes, under 90 characters.
- **Name the prospect's former employer** (a public fact from their own profile) — **not the client's
  customer relationship in identifying detail**, unless approved.
- **Never state a date.** "In 2018 you were at X" is both creepy and frequently wrong when a profile
  is imprecise.
- **Never imply you know someone in common** unless you do. The deleted mutual-connection member
  exists as a warning: that claim is unverifiable at scale and reads as a lie when it is wrong.

**Verification for this family is source-side, not model-side.** The facts come from the prospect's
own profile, and the model only phrases them — so the risk is a stale or mismatched profile, which no
verifier over your own output can catch. **Prefer sources that return a dated experience you can
check.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The list is tiny and not worth a campaign | The member was defined as a **time overlap between two specific people** | Widen to "ever worked there, and has since moved on" |
| The list is full of the customer's current staff | No current-employment exclusion | Drop anyone currently employed by a source company |
| The client's own employees appear | The client's domain got into the source set | **Stop. The list is wrong** |
| The same people reappear next quarter | Row drops only fix this run | Push the source companies to the client's DNC list |
| A client is unhappy that their customer was named | The line named a real third party | **Default to the unnamed form.** Naming is the client's decision |
| The line states a date that is wrong | Profile date ranges are imprecise | **Never state a date** |
| Replies cannot be attributed to an angle | Seven members share one copy field | **Keep `warm_intro_member` on every row** |
| Someone proposes rebuilding mutual connections | It is a deleted member | It is unverifiable at scale and reads as a lie when wrong. Do not re-add it |
| An event member becomes a maintenance burden | It was turned into a standing recipe | **Event overlap is a custom scrape every time.** That is the decision, not a gap |

### Hard rules

- **Build member 2 first.** It is the only one with a passing source probe and a real population
  behind it.
- **Never name a client's customer in copy without explicit approval.**
- **Never claim a mutual connection.**
- **Inherit the source-company exclusions**, both halves.
- **No member ships a line until at least 10 rendered lines have been read and graded.**
