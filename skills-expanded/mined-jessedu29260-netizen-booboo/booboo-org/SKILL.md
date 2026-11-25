---
name: booboo-org
description: Design or reshape a Booboo organigram — the agent hierarchy in org.booboo.json that fleets boot from. Covers the seed onboarding ritual, reading a real structure out of a project instead of inventing one, rule inheritance, memory buckets, and reparenting through the panel. Use when someone wants to model their agents as a company, change who reports to whom, or fix an org that is a flat list instead of a hierarchy.
---

# The organigram — run a fleet like a company

Read `RULES.md` first. Rules 6 and 7 are the load-bearing ones here.

`org.booboo.json` is **SOURCE**, not output. It is versioned, validated before
every write (a cycle can never land), and edited through the panel or a reviewed
change. The chart is not a diagram of the authority — it *is* the authority.
Agents that boot with `booboo_boot` obey the shape on their next session.

## First: is this brain shaped at all?

If `org.booboo.json` contains `"seed": true`, it still holds the scaffold's sample
Writer/Researcher pair, which belongs to nobody.

**Stop and run the project's `ONBOARDING.md` before any other work.** Do not add
agents, do not write memories against the sample agents, do not build on the
placeholder. Everything downstream inherits from the org, so work done against a
fake structure gets redone against the real one.

## Read before you ask

Most of an organigram is already in the project. Look, in this order:

- `package.json` / `pyproject.toml` / `go.mod` — what this is and what it is built from
- the README and any architecture doc — what it claims to do, for whom, **and how
  the parts relate**
- the top two directory levels — candidate divisions
- an existing `CLAUDE.md` / `AGENTS.md` / `.cursorrules` — conventions already agreed
- `git log --oneline -40` and `git shortlog -sn` — what actually gets worked on, by how many people
- `docs/`, `ops/`, `infra/` — surfaces that need an owner

Then ask the human only what the repo could not tell you.

## Folders give you nouns, not shape

This is the mistake to design against. A directory listing is flat by
construction. An org built straight from one is a root with fifteen children and
no structure — which is a list, not an organigram, and it makes rule inheritance
useless because there is nowhere to declare a rule except the root.

The grouping almost always lives in the prose. "X is the contract at the centre, Y
and Z feed it, A and B render it" is **three divisions**, and no amount of staring
at folder names will produce it. Read for how the parts relate, then group the
nouns underneath.

A good check: if you cannot name what a branch would declare as an inherited rule,
the branch probably should not exist.

## What each agent carries

A card in the panel, and a slice from `booboo_boot`:

- **identity** — who it is, its id
- **authority chain** — its parent, up to the root
- **inherited rules** — the stack, in boot order, declared at branches above it
- **bucket access** — which memory buckets it may reach
- **skills** — what it is equipped to do
- **children** — who reports to it
- **reports** — what it has closed, newest first

Rules inherit top-down: declare once at a branch, everything beneath is bound.
That is the reason to build real depth rather than a flat fan — a rule that must
be restated on fifteen siblings is a branch that was never created.

## Reshaping

Drag an agent under a new parent in `booboo panel`, hit apply, and the org file
changes — versioned in git, validated before the write. Fleets pick it up on their
next boot.

Prefer the panel over hand-editing. It validates; your text editor does not, and a
cycle in an org file is a boot loop that manifests as an agent hanging with no
error.

## The five tabs

One org file plus one snapshot gives you: **organigram** (drag-drop hierarchy) ·
**buckets** (who remembers what) · **reports** (what the fleet closed, newest
first) · **rules** (who declares, who inherits) · **graph** (the 3D brain,
embedded).

Reports and buckets fill two ways — live, when an agent calls `booboo_remember` or
`booboo_report`, or in bulk from your own tables via config. The live path needs no
rebuild; the journal sits beside the snapshot and is queryable the same session.

## Verify a reshape

Do not trust the drag. After applying:

1. `booboo_boot` the moved agent and read its inherited-rule stack. It should now
   carry the new parent's declarations in boot order.
2. `booboo_boot` a sibling that did **not** move and confirm its stack is unchanged.
3. Open the panel's rules tab and check nothing is declared twice at two levels —
   duplicate declaration is how contradictory inheritance starts.

Then `booboo_report` what you changed and why, so the next operator inherits the
reasoning instead of re-deriving it from a diff.
