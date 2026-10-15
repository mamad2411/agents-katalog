---
name: playbook-linkedin-engagement
description: Turn the people who like and comment on a source account's LinkedIn posts (a competitor, or one of the client's own customers) into ICP-filtered prospect rows, with an optional copy-ready personalization line when the campaign asks for one. Triggers on "who engages with our competitors", "likers and commenters", "LinkedIn engagement list", "people commenting on competitor posts", "who engages with our customers' posts", "warm LinkedIn audience", "competitor engagers". Outputs one clean prospect row per engager; engagement_line only on request.
---

# Playbook: LinkedIn Engagement

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when** an account's audience is the client's audience — a **competitor** or the **client's own
customer**.

**Do not use for** more companies in a market, similar companies (`playbook-lookalikes`), or job
changers (`playbook-new-in-role`). The chain is the same for both lanes; only the target URL changes.

**Output:** one row per engager — who, employer, post, evidence URL. `engagement_line` is **opt-in**.

## The number that governs planning

⚠️ **Roughly 1 in 10 raw engagers survives. Harvest 10 to 15x what you need.**

Cost follows from that: about **$4.45 per 1,000 raw engagers**, which is about **$45 per 1,000
usable prospects** at the measured survival rate. That is squarely in expensive territory, so
**shortlist posts by engagement count before you scrape.**

## The source-company rule (both halves, always automatic)

This is the rule that separates a usable engagement list from an embarrassing one, and **it has two
halves that people implement only one of.**

**(a) Drop every engager employed by ANY source company** — not just the author of the post they
engaged with. Match each current employer on **resolved domain first**, then profile URL, then
squashed name, and also on **resolved email domain**.

**(b) Push every source company onto that client's do-not-contact list.** Row drops fix only this
run; **the block list runs at send time**, which is what stops the same people arriving through a
different lane next month.

**It bites hardest on the customer lane**, where the source companies are people the client already
works with.

⛔ **Never block the client's own domain.** If it appears in the source set, **the list is wrong —
stop.**

## Before any paid call

1. **The operator confirms the source list.** Say it out loud: *"these companies and everyone who
   works at them go on this client's DNC list."*
2. **Resolve every source account to a bare domain first.** An unresolved source silently disables
   **both halves** of the rule above. **Unresolved means stop, not continue.**
   (`playbook-social-link-finding` does this conversion in both directions.)
3. **If the client's ICP is unknown, ask.** Never infer a headcount band, a country list, or a title
   set.

## Run it

```
0   Confirm source URLs, client ICP, and whether the brief wants a line (default: no).
0b  Resolve every source account to a bare domain -> source-companies.json (EXACT match only).
    Unresolved => STOP.
1   Company posts, windowed to the last month, shortlisted by engagement count.
2   Post reactions + post comments for the shortlisted posts.
3   ICP enrichment (headcount, company) on the engagers.
4   Deterministic pre-gate: source-company drop, ICP filter, dedupe.
5   Suppression pass: client DNC, existing TAM, live campaigns.
6   DNC push (once per harvest).
7   Email finding, valid only.
```

**Rows are the deliverable; lines are opt-in.** Never run a line writer unless the brief asks. When
it does, an empty-line row leaves *that* campaign for the normal one rather than shipping a gap.

## Verification

**PASS 17/18 correct outcomes** on the source-and-gate test — **and note what that counts:** a
correct **exclusion** is scored as a usable outcome. **Raw signal yield was 1 usable prospect in 17
unique people.**

Both numbers are true and they measure different things. The gate works; the yield is thin. **Plan
from the yield.**

⚠️ The end-to-end harvest has never been run in one pass. **Do a one-post run and read the output
before scaling.**

## Clay implementation

- **`clay-table.md`** — where the gate lives in a table.
- **`clay-workflow.md`** — the CLI-buildable version.

## Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The list contains the client's own employees | The client's domain got into the source set | **Stop. The list is wrong** |
| The list contains the competitor's own staff | Only half (a) was implemented, matched on name alone | Match on **resolved domain first**, then profile URL, then squashed name, then email domain |
| The same people reappear next month through another lane | Half (b) was skipped | The DNC push is what persists. Row drops do not |
| The source-company rule appears to do nothing | An unresolved source URL produced an **empty** source set | **An empty set silently disables both halves.** Unresolved means stop |
| Cost per usable prospect is 10x the estimate | You costed raw engagers, not survivors | ~1 in 10 survives. Harvest 10-15x |
| A person's employer is wrong | Taking the **first** entry of an experience array rather than the current one | Read the current experience explicitly |
| Rows silently vanish on a join | Post and engager records key differently | Confirm the join key on one post before scaling |
| The run stalls waiting on a scraper | There is no fallback source by design | **The run waits.** A different scraper is not a drop-in substitute here |

### Hard rules

- **Both halves of the source-company rule, every run, automatically.**
- **The operator confirms the source list before any paid call.**
- **Rows are the deliverable. Lines are opt-in.**
- **If the ICP is unknown, ask.**
