---
name: hypothesis-annotation-visibility
description: Diagnose and fix Hypothesis (hypothes.is) annotation visibility — why two people in the same group see different annotation counts, why a class or study group can't see someone's notes, why highlights never show up for anyone else, and how to safely move "Only Me" annotations into a group or pull accidentally-public ones back out. Use this whenever someone mentions Hypothesis, hypothes.is, web annotations, annotation groups, highlights that aren't appearing, mismatched annotation counts ("I see 5, they see 149"), students who can't see the teacher's notes, or annotations that went public by mistake — including when they describe it as a broken integration, a sync issue, a caching problem, or a membership/permissions bug, because it is almost never any of those.
---

# Hypothesis annotation visibility

Hypothesis visibility problems get misdiagnosed constantly. People report them as broken
integrations, stale caches, or group-membership bugs. They are almost always one thing:
a per-annotation read permission that points at a person instead of a group.

This skill exists because that mechanism is easy to state, easy to verify, and easy to fix
safely — but the failure looks nothing like its cause, and some of the widely-repeated
folklore about it is wrong (see `references/api-facts.md`).

## The mechanism

Every annotation carries two independent fields:

- **`group`** — a label. Which group was selected when it was written.
- **`permissions.read`** — the access check. Exactly one of three shapes:

| `permissions.read` | Who can read it |
|---|---|
| `["acct:alice@hypothes.is"]` | the author alone ("Only Me") |
| `["group:AbCd1234"]` | that group's members |
| `["group:__world__"]` | the public web |

These do not constrain each other. An annotation written privately while a group was
selected still stores `group: "AbCd1234"`. So it **matches** a `?group=AbCd1234` search,
which is why it inflates the author's sidebar count — and then the permission filter
drops it for everybody else.

That is the whole illusion: one query, two totals, no error. The `total` field in a search
response is computed against the requesting token's identity, not against the group.

Membership does not defeat it. Neither does moderator or owner. The check is per
annotation, and the only identity that satisfies `["acct:alice@..."]` is Alice.

## Four states, and the one that bites

Because the two fields are independent, there are four combinations. Three are ordinary.
The fourth is a trap worth naming before you touch anything:

| `group` | `permissions.read` | Meaning |
|---|---|---|
| `AbCd1234` | `acct:author` | in the group, invisible to it — **the usual complaint** |
| `AbCd1234` | `group:AbCd1234` | working as intended |
| `__world__` | `group:__world__` | on the public web — **a live leak** |
| `__world__` | `acct:author` | private, but scoped to Public — **"sharing" this publishes it** |

That last row is why "just make the private ones shared" is not a safe instruction. For an
annotation in group scope, sharing means ~N members. For one in `__world__` scope, the same
words mean the open internet. Always read the `group` field before changing `read`.

**If something is in `__world__` scope**, separate the two goals, because only one of them
has a verified fix:

- *Stop the exposure* — set `read` back to `["acct:<author>"]`. Reliable, reversible,
  needs no group. Do this first when anything is already public.
- *Move it into a group* — this is a scope change, not a permission change, and whether
  `group` can be PATCHed at all is **unverified** (see `references/api-facts.md` §5b). Test
  on one annotation and re-`GET` it before promising anyone a batch fix. Changing `read`
  alone would leave it in the public scope wearing a group permission, which is a state
  nobody intended.

## Triage order

Work read-only until you have the numbers. The audit is fast and it prevents the two
mistakes that actually cause harm: publishing something, and touching another person's data.

### 1. Establish identity

Whose token is this? It decides everything downstream, because a token can only ever fix
its own annotations.

```bash
export HYP_TOKEN="..."           # from https://hypothes.is/account/developer
python scripts/hyp_audit.py whoami
```

### 2. Audit, read-only

```bash
python scripts/hyp_audit.py group <GROUP_ID>          # inside one group
python scripts/hyp_audit.py site "example.org"        # public leaks across a site
python scripts/hyp_audit.py mine                      # everything this token owns
```

`group` reports, per author and per document: how many are visible to you, how many are
private, and how many of the private ones are text-less highlights versus written notes.
That highlight/note split is the single most useful number in the report — see step 4.

### 3. Prove it with a second identity

One token can never prove group visibility, because an author always sees their own work.
If a second token is available (any other member of the group), compare directly:

```bash
export HYP_TOKEN="<member A>"
export HYP_TOKEN_B="<member B>"
python scripts/hyp_audit.py compare <GROUP_ID>
```

This prints both totals side by side and lists exactly which annotation IDs one identity
can see and the other cannot. That difference *is* the bug, expressed as data. It converts
an argument into a diff, and it is the only way to confirm a fix actually landed.

### 4. Decide what may be shared — this is not your call to make

Before proposing any write, split the private set in two. The audit does this for you:

- **Text-less highlights** (`text: ""`, no tags) carry no opinion. Someone marked a passage.
  Sharing these is low-stakes.
- **Annotations with text or tags** are written notes. On a person's own draft, these are
  often candid — *this section is weak*, *cut this*, remarks about other people. Publishing
  them to a group is an editorial decision belonging to their author, not a permissions fix.

Print the text-bearing ones and let the author read them before deciding. If the whole
private set turns out to be bare highlights, say so plainly — that removes the risk and the
decision gets much easier.

### 5. Fix — only the author can, and only with a backup

```bash
python scripts/hyp_share.py --group <GROUP_ID>                        # dry run, writes nothing
python scripts/hyp_share.py --group <GROUP_ID> --apply --one          # one, to verify
python scripts/hyp_share.py --group <GROUP_ID> --apply --highlights   # bare highlights only
python scripts/hyp_share.py --group <GROUP_ID> --apply                # all private
python scripts/hyp_share.py --revert backups/<stamp>.jsonl            # undo a batch
```

Every `--apply` writes the complete pre-change records to `backups/<stamp>.jsonl` before
touching anything, so any batch is one command from being undone. Convert one first and
verify it cross-account before running the rest; a batch that was wrong in a way you didn't
predict is much cheaper to discover at n=1.

## Safety rules

**Tokens come from the environment, never from a file, an argument, or a chat message.**
The scripts read `HYP_TOKEN` and `HYP_TOKEN_B` and never print them. A Hypothesis developer
token is full read/write on that account. If one has been pasted into a transcript, a
ticket, or a shared terminal, say so and recommend rotating it at
`hypothes.is/account/developer` — especially when it belongs to somebody else.

**Never write `group:__world__`.** No visibility problem is solved by publishing to the open
web, and the value is one character away from a group id in a config. `hyp_share.py`
refuses it outright.

**Only the author can write.** Any other token gets HTTP 404 — not 403, so the API doesn't
even confirm the annotation exists. When the person asking is not the author, the honest
answer is that they cannot fix it and the author must. Don't route around this by asking
for someone else's token; suggest they run the script themselves.

**Reversibility is technical, not social.** A batch can be reverted in seconds, but people
who saw the annotations in the meantime have already seen them. Treat exposure as one-way
and get the decision right beforehand.

## Reporting the diagnosis

Lead with the number that proves it, then the mechanism. Something like:

> Not an integration problem. Of the 156 annotations in the group, 153 have
> `permissions.read: ["acct:alice@hypothes.is"]` — private to Alice. They carry the group
> id, which is why Alice's sidebar counts them, but the permission check runs per
> annotation, so no other member can read them. All 153 are text-less highlights, so
> nothing written is at stake. Only Alice can change them.

State counts, permission values, and who can act. Avoid speculating about caching or
membership once the audit has the answer — a permission split falls along document and
author lines, which is a shape a cache cannot produce, and that asymmetry is usually the
fastest way to rule the alternatives out.

## References

- `references/api-facts.md` — behaviors verified against the live API, including several
  that contradict widely-repeated advice, plus one question explicitly marked unverified.
  Read it before telling anyone that highlights can't be shared, that a PATCH will clobber
  permissions, or that an annotation can be moved between groups.
- A deployment reference, if one is present in `references/` — some installations keep a
  local file with the group ids, annotated domain and accounts they triage repeatedly, so
  the audit can skip the lookup. These are environment-specific and often name real
  people, so they are kept out of public copies of this skill. When none is present, ask
  for the group id and the site.

## Fixtures and tests

`fixtures/` holds synthetic API responses (invented accounts and group ids) for exercising
the workflow with no token at all, and `evals/evals.json` defines the cases the skill is
tested against. Regenerate the fixtures with `python fixtures/make_fixtures.py`. Use these
rather than a live group when demonstrating or debugging the skill — an audit is read-only,
but a demo that reaches for a real token is a demo that can write to someone's account.
