---
name: arbitrating-a-dispute
description: Use when two parties need a ruling that someone outside the argument will act on — a contested invoice, a delivery dispute, a contract term, a payout someone has to release — or when a request mentions arbitration, a sealed decision, or a verdict a contract points at. Covers the settings that make a verdict relied upon, what the case owner gives up, and what to do when a case ends without a ruling.
---

# Arbitrating a dispute

Arbitration mode turns a case from an opinion into a finding someone else can act on. It does that
by taking powers away from the person who opened it.

## When to use

When the outcome will be relied upon by a party who was not in the room: money moves, a contract
clause resolves, an obligation is settled. For an ordinary decision, `deciding-with-a-jury` is the
right tool and this one is overhead.

## Checklist

- [ ] Capture both parties' positions and the remedies each wants
- [ ] Make the sides the possible **remedies**, not the parties
- [ ] Create with the sealing settings below — all of them, explicitly
- [ ] Let the parties put their evidence in as comments
- [ ] Wait it out; you cannot close it yourself
- [ ] Read the verdict, including the outcomes that are not rulings

## Intake

Write the case so a juror who has never heard of either party can decide it: what was agreed, what
happened, what each side claims, and what is actually in dispute. The description is the whole
brief.

You will rarely have every fact, and that is not a reason to stall. **Build the brief from what you
were given and name the gaps inside the description** — "neither party has supplied the delivery
log" tells a jury something true and lets it weigh the claims accordingly. File the case, then say
what you assumed and what would sharpen it. Stop and ask only when there is no describable dispute
at all: no positions, or no remedy anyone is asking for.

**Sides are remedies.** "Refund in full" and "Partial credit" are decidable; "Alice" and "Bob" are
not — they ask a jury to pick a person, and the answer cannot be acted on without interpretation.
Two to ten of them, mutually exclusive.

## What makes a ruling sealed

State every one of these. A dispute settled by an unstated default is a dispute settled by accident.

| Setting | Why |
| --- | --- |
| `arbitrationMode: true` | Turns on everything below and bars the owner from its jury |
| `visibility` | Cases are private by default. `public` for a dispute the platform's jurors decide; `private` only when the panel is named — and then invite it, or nobody can ever seat |
| `juryType` | `public` with a public case; `invited` with a private one, followed by `tribeunal_invite_jurors` |
| `minVotes` at least 2 | Without a real quorum a single vote can decide a contested payout |
| `decisionRequirement` | Says what counts as agreement — a plurality is rarely enough for money |
| `jurorCount` | Size it to who will actually seat, or it never opens |
| `maxAiJurorPercentage` | Decide deliberately whether AI jurors may rule on this |
| Voting window | Long enough that jurors can read evidence, not just react |

Guest voting cannot be combined with arbitration. Leave tags off: they gate who may vote, and a
dispute should not be settled by whoever happens to hold a tag.

## What the owner gives up

Creating an arbitration case costs you your standing in it. You cannot vote on it, you cannot join
its jury, and you cannot close it early — an admin can, or it closes at its deadline. Those
refusals are structural and permanent; retrying is wasted effort.

This is the point rather than a limitation. A verdict the interested party could have voted in is
not one an outside party can rely on.

Once the case closes, its evidence marks freeze so the record it was judged on stops moving. A
refusal on that ground is final.

## When there is no ruling

A finished case can end without deciding anything, and reporting that as a win is the worst
available failure here.

| Outcome | Meaning | What to do |
| --- | --- | --- |
| Quorum not met | Fewer votes than required | Re-file with a longer window, or more jurors, or a lower minimum |
| Requirement not met | Enough votes, not enough agreement | Re-file with a weaker requirement, or accept there is no consensus |
| Undecided, no reason given | A genuine tie or an empty case | Re-file; consider whether the sides were really exclusive |

Re-filing is a new case. Say plainly that the first produced no ruling, and never present its
percentages as a result — a lone vote is not a mandate.

## What a verdict is

The jury's finding, timestamped, carrying the tally and each juror's rationale. A webhook delivery
that carries it is HMAC-signed — see `wiring-webhooks` — and an arbitration verdict is itself
signed: `tribeunal_verify_ruling` recomputes the signature, the digest and the log inclusion.

It is not enforcement: Tribeunal never holds the money, never releases the escrow, never touches
the contract. Whatever acts on the ruling is yours, and this separation is what lets a verdict be
trusted — a body that ruled *and* held the stakes would be neither.

Disclose that a jury may include AI jurors when a party would care.

Sealed and final mean sealed and final on the record. A ruling here is advisory: nothing enforces
it, and the respondent of a `tribeunal_open_dispute` is never asked to consent, so never describe it as
legally binding.

## Disputes with a named counterparty

When the other side is a specific Tribeunal account rather than an audience of jurors, prefer
`tribeunal_open_dispute` to `tribeunal_create_case`: it names the respondent, owns the case as the
Tribeunal arbiter so neither party controls it, and carries the settings above by construction. The
loop is five calls: `tribeunal_open_dispute` → `tribeunal_submit_evidence` → `tribeunal_await_ruling`
→ `tribeunal_verify_ruling` → `tribeunal_appeal_ruling`.

Two reads sit beside the loop. `tribeunal_list_disputes` lists the disputes you are a party to: it is
how a respondent that subscribed to no webhook finds one opened against it, and how you recover a
`disputeUuid` in a new session. `tribeunal_get_dispute` returns one dispute's parties, rounds and
standing ruling at once, without waiting for anything.

`panel` has no default — state it. `"fast_track"` seats 3 AI jurors once the filing window ends;
`"human"` invites the operator's human pool. An unstated default is exactly the accidental settling
the checklist above exists to prevent.

File your evidence with `tribeunal_submit_evidence` before `panelOpensAt`: a juror who already voted
never reads a later filing. Only the party the standing ruling goes against may appeal, and only
before its `appealDeadline`; a Void appeal round (no jurors showed) keeps the standing ruling rather
than clearing it.

- **`tribeunal_open_dispute`** — Proves: The case exists, is private, and the value is ≤ cap. Does
  NOT prove: Respondent consent; any enforcement when `bindingBasis:'advisory'`.
- **`tribeunal_await_ruling`** — Proves: `provisional` = a signed round verdict; `final` = no further
  appeal under Tribeunal's rules. Does NOT prove: That money moved (see `execution`).

Two gotchas: re-arming a wait through an appeal window is `acting-on-verdicts`' job, not this
skill's — honour `nextCheckAfter`, never a fixed retry interval. And `final` is Tribeunal's own
finality, not proof anything moved — `execution` stays `null` until an escrow or contract acts.

## Escrow deal requests

When someone is to pay for work in USDC and wants a jury, not either party, to settle a
disagreement, `tribeunal_create_deal` writes the request: the payer and payee wallets, the amount,
what is delivered, the delivery days and the panel. It creates a request only. Nothing is paid or
held until the payer opens `shareUrl` and deposits with their own wallet on the deal page;
Tribeunal never holds the money, and no tool here funds, releases, refunds or disputes a deal —
each is a wallet action a party takes on that page.

Ask both parties for their wallet addresses; never guess one or reuse one from memory. State the
panel: `"fast_track"` lets three AI jurors decide a first round and people decide every appeal;
`"human"` has people decide every round. Hand `shareUrl` to the payer and the payee and nobody
else: whoever holds it reads the terms and, once a round is decided, that round's case and its
votes. The description goes into the hashed terms the jury reads and stays after account
deletion, so keep secrets and personal data out of it. Tell the payer that doing nothing after
the release date pays the payee, so a dispute has to be raised on the page before it.

`tribeunal_get_deal` reads a request back: its terms and the status Tribeunal's indexer last
recorded, which stays `awaiting_deposit` until the payer's deposit is recorded, minutes after it
lands. The account that created the request reads it by `slug`; anyone else also passes the
`share` value from the link they were sent.

- **`tribeunal_create_deal`** — Proves: A deal request is stored with these terms, and termsHash is
  the keccak-256 of the exact terms text the payer's browser re-checks before it signs. Does NOT
  prove: That anything is paid or held; that the payee accepted the terms; that either address
  belongs to the person you think; that the description is true; that a court would uphold the
  deal; that the network is not a test network.

A `deals_unavailable` refusal means this server does not offer deals right now: say so plainly and
stop, rather than retrying.

## Working with the rest

Wait for the outcome with `acting-on-verdicts`. Read and curate the parties' evidence with
`weighing-evidence`. A machine party that has to act the moment the ruling lands should subscribe
rather than poll — see `wiring-webhooks`.

## Gotchas

| Trap | What is true |
| --- | --- |
| The owner can close their own arbitration case early | They cannot. An admin can, or the deadline does |
| A refusal to vote is a bug worth retrying | The owner bar is structural and permanent |
| Any verdict is a ruling | Quorum and requirement failures decide nothing |
| Evidence can be tidied after the ruling | Marks freeze at close, permanently |
| Arbitration can reach a wider crowd with guest votes | The two cannot be combined |
| Leaving `visibility` out is harmless | It makes the case private with an invited jury; with nobody invited it closes Void at the deadline |
