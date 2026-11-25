---
name: crate-audit
description: Audit a Rust crate or module for bloat, dead code, unused features, repetition, over-broad API, and architectural debt — evidence-first, with a prioritized findings report that separates safe deletions from judgement calls. Use when asked to "crate-audit", "audit this crate", "debloat", "find dead code / unused features", "look for repetition / tech debt", or "what can we delete / simplify" in a given crate.
---

# crate-audit — crate/module debt audit

Find what a crate no longer needs, what's duplicated, and what's structurally
rotting — and, just as much, where a *warranted* abstraction would make it
better. Backed by evidence, not vibes. Produce a report the human acts on;
**do not delete, refactor, or abstract without explicit approval.**

Auditing is not only subtractive. Removing cruft and *adding* the right seam
(a shared helper, a named type, a trait that makes a thing testable) are both
in scope. Abstraction is good when it pays its way — the discipline is to
*offer* it with its trade-offs and let the human choose, never to impose it.

## Operating rules

1. **Evidence before every claim.** "Unused" = a grep with zero callers.
   "Duplicated" = both sites shown. "Dead feature" = the flag gates nothing. No
   finding without a command output behind it.
2. **Audit, then report. Don't edit.** Offer to apply the *obvious wins* only
   after the human picks them. Never bundle a refactor into the audit.
3. **Separate "delete now" from "needs your call."** Default to *flag*, not
   *delete*, for anything that might be deliberate (external API, reserved
   surface, intentional divergence).
4. **Justified duplication is not debt.** Code paths that look similar but serve
   different contracts (a text exporter vs a protobuf one) aren't collapsible.
   Say why it might be intentional.
5. **Debt is drift from the codebase's own norms** (CLAUDE.md, sibling crates) —
   not drift from your preferences.
6. **"No producer" ≠ dead for contract surface.** Wire formats, ABIs, protocol
   enums, public schemas are routinely defined *ahead of their consumers* — a
   variant with zero emit sites may be a reserved slot. Before flagging one,
   `grep -rin <Symbol> docs/ plans/`. If the design reserves it, the finding is
   *keep* (at most: make the source comment say so). A grep miss is a prompt to
   read the design, never the verdict.

## Step 1 — Scope

- **Target**: which crate / module(s), and its **mandate** (read its lib.rs /
  module docs — bloat is code that doesn't serve the mandate).
- **Consumers + publish status** — the decisive scoping fact:
  - `publish = false` + few internal consumers → "unused-by-them == dead"; no
    external-API escape hatch, so the "might be public API" caveat doesn't apply.
  - **Bin/leaf crate** (nothing depends on it) → there are no consumer dirs at
    all; every `pub` is internal-only. Lean on the `dead_code` build + a
    "called only by tests" check rather than cross-crate greps.
  - Published / many consumers → be conservative about `pub` items.

  ```bash
  grep -n publish <crate>/Cargo.toml
  grep -rln '<crate_underscored>::' <other-crates>/   # who imports it
  ```

## Step 2 — Gather evidence

**Start with the tool.** `cargo xtask audit <crate> --json` does the boring 80%
mechanically (it's the SnitchOS replacement for the fragile per-symbol bash — see
`plans/xtask-audit.md`). One command gives you, for the crate:

```bash
cargo xtask audit <crate> --json    # for parsing; drop --json for the human table
```

- **`symbols[]`** — every bare-`pub` item with `{name, kind, file, line, ext,
  int, test, verdict}`. `ext` = sibling-crate callers, `int` = this crate
  non-test, `test` = test-only. `verdict` ∈ keep-public / demote-pub(crate) /
  test-only / dead-candidate.
- **`unused_deps[]`** — `cargo machete` findings (`cargo install cargo-machete`).
- **`markers[]`** — `TODO/FIXME/HACK/#[allow]/#[expect]/dead_code/stub` sites.

**Trust it, but know its blind spots** (it's word-boundary heuristics, no name
resolution — `plans/xtask-audit.md` has the full rationale):

- It **over-counts on name collisions**: a `pub fn new` / `is_empty` / `len`
  reads as `ext` huge because every other `new` in the workspace matches. So a
  *high* count on a common name proves nothing; a **zero** count is the
  trustworthy signal. Treat `dead-candidate`/`test-only` rows as the candidate
  list; for common-named items, fall back to the manual cross-ref below.
- It only sees **bare `pub`** (skips `pub(crate)` and items inside
  `#[cfg(test)]`) and ≤2-char idents (pass `--include-short` to include them).
- It **under-counts** (false `ext=0`) two ways the heuristic can't see — both
  proven on the itest-harness sweep (`plans/audit-revisit-post-xtask-audit.md`):
  (a) **re-export aliases** — `pub use x as y` then the consumer calls `y`, so the
  count-by-declared-name misses it; (b) **a type used positionally in a public
  signature** — the consumer calls `Foo::bar()` returning `Result<_, MyError>`
  without naming `MyError`, so `MyError` shows `ext=0` despite being public API.
  (c) **required by a lint, not a caller** — a `pub is_empty` exists only to
  satisfy `clippy::len_without_is_empty` next to a `pub len`; it has zero callers
  but demoting it trips the lint. The sweep's clippy pass catches this.
- `verdict` is a candidate, never a conclusion — **rule 6 still applies**: a
  zero-caller wire/ABI variant may be reserved surface. Verify in docs/plans.

**To act on an `ext=0` batch, let the compiler be the oracle** (the privatization
sweep): demote the whole `ext=0` set to `pub(crate)`, rebuild **and clippy** the
crate **+ its consumers**, and re-promote exactly what breaks. This converts all
three blind spots above into hard signals — a re-export alias fails with E0364, a
positionally-used type with `private_interfaces` / "type is private" (re-promote
the transitive closure: a pub field's type must be ≥ as visible as the field), a
lint-required item with its own clippy warning (e.g. `len_without_is_empty`).
Iterate to green; what stays `pub(crate)` was genuinely internal. For a crate with
a non-host consumer (e.g. a bare-metal kernel), rebuild **its** target too —
`cargo xtask build` + `cargo test -p <crate>` + `cargo clippy -p <crate>`. Zero
deletions, zero guesswork.

**Then fill the gaps the tool doesn't cover:**

```bash
wc -l <crate>/src/*.rs | sort -n                       # where's the mass?
cargo xtask loc                                        # prod vs test split

# Features (tool doesn't analyse these):
grep -A30 '\[features\]' <crate>/Cargo.toml; grep -rn 'cfg(feature' <crate>/src/   # declared vs gating
grep -rn 'feature = ' . --include=Cargo.toml                                       # who enables them

# Privatization detector — the compiler finds what grep/heuristics miss:
# demote `pub mod`→`mod` and rebuild; it flags every now-unreachable `pub fn`
# (esp. test-only ones). The tool can't do this — it's the strongest check.

# Manual cross-ref ONLY for common-named symbols the tool over-counts, or to
# double-check a candidate. SANITY-CHECK on a symbol you KNOW is used first —
# an all-zero table means the grep is broken, not that everything's dead.
for sym in <CommonNamedSym> ...; do
  printf "%-30s ext=%s int=%s\n" "$sym" \
    "$(grep -rw "$sym" <consumer-dirs> | wc -l)" "$(grep -rw "$sym" <crate>/src | wc -l)"
done
```

Multi-module lib with re-exports? Also check which modules the consumer
*path-accesses* (`grep -rhoE '<crate>::[a-z_]+::' <consumer-dirs> | sort -u`) —
never-accessed ones can be private. And before trimming a re-export, confirm
internal code imports siblings via `crate::mod::Item`, not the bare `crate::Item`
re-export (the latter breaks on removal).

## Step 3 — Analyse across dimensions

Record findings with evidence — name the specific symbol/line/site.

### A. Dead code & unused exports
- `pub` items with zero callers outside their module *and* zero consumer usage.
- **Privatization is a dead-code detector.** After confirming a module is
  internal-only, demote `pub mod`→`mod`: the compiler then checks every `pub fn`
  inside and flags ones grep misses (e.g. called *only by tests*). Test-only
  survivors: scope `#[cfg(test)]` if they keep tests readable; else delete.
- Still-public-but-internal items that should be `pub(crate)` / private.
- `#[allow(dead_code)]` waiting for a caller that never came. **Read the
  justification — it may describe a crate shape that no longer exists** (e.g.
  "for the lib build" on a crate that's bin-only).
- Unreachable arms, `if false`, error variants never constructed, dead re-exports.

### A′. Lint/style "debt" — check it's ENFORCED first
Before reporting lint findings, check the lint is actually enforced (`[lints]`
table, `deny`/`warn` attrs, `clippy.toml`, CI). A standard from a docs file that
nothing enforces is **aspiration, not a norm** — and if the crate matches its
siblings, it isn't drifting. Report it as a workspace-policy question, not crate
debt. (But a lint that *is* enforced and *fires today* is real — fix or
`#[allow(..., reason)]` it.)

### B. Unused / vestigial features & config
- Cargo features that gate nothing, or that nobody enables; flags always-on (noise)
  or never-on (dead).
- CLI flags / config knobs parsed but never read, or that only ever take one value.

### C. Speculative / YAGNI code
- Abstractions (traits, generics, hooks) with one impl and no second on the
  horizon — is the indirection paying rent?
- Parked "for the future" code with no caller — delete it; git remembers.
  **Exception: contract surface** (wire/ABI/schema) defined ahead of its producer
  is reserved, not speculative — rule 6.
- Extensibility points exercised by one case; params always passed the same value.

### D. Repetition (collapsible)
- Near-duplicate logic — show both, propose the shared helper *or* explain why
  they must diverge.
- Repeated construction boilerplate → constructor / `From` / builder. Copy-pasted
  fixtures → factory. Parallel `match` arms → macro / trait method.
- **The "edit-N-places" tell:** a recent change that touched the *same logical
  thing* in multiple files (a catalogue/enum/list kept in parallel) *will* drift.
  Strong signal for "extract a single source."

### E. Architectural debt
- `too_many_arguments` (6+) → a context struct. God-functions/modules, or the
  inverse (a "module" that's one function nobody else needs).
- Two ways to do the same thing; primitive obsession (`(u32, u32)` where a named
  type prevents bugs); leaky abstractions (a "pure" module that does I/O); a layer
  that just forwards; A reaching into B's internals; CLAUDE.md says X, code does Y.

### F. API surface & types
- Over-broad `pub`; all-public-field structs that want invariants/constructors;
  types that exist only to be immediately converted to another.

### G. Test & doc debt
- Test-to-prod ratio anomalies; weak tests (`assert!(true)`, round-trip-only,
  restating the impl); duplicated fixtures (→ D).
- Stale comments, what-not-why comments, and **SAFETY/invariant comments that lie**
  (assert a guarantee the code doesn't keep — high severity).
- **Load-bearing claims in module/header docs the code doesn't keep.** A confident
  noun ("length-prefixed on the wire", "lock-free", "O(1)") reads as authoritative
  and greps as fine — verify it against the implementation. Surfacing trick: try to
  *explain the module from its docs*; the false claim dies when you re-derive it.

### H. Dependencies
- Deps pulled in for one trivial call (replaceable with std / a few lines); heavy
  transitive cost for light use; two deps doing the same job.

## Step 4 — Report

Prioritized table, one row per finding:

| # | Dimension | Severity | Finding | Evidence | Recommendation | Effort | Risk |

- **Severity**: high (active hazard) · med (clear debt) · low (nit).
- **Evidence**: file:line + the grep/command output that proves it.
- **Risk**: of *acting* — "may be external API," "changes wire format."

Then split into lists for the human:

- **Obvious wins** — zero-caller private items, dead branches, parked code,
  exact-duplicate fixtures, stale docs, unused deps. Low risk, high confidence.
- **Needs your call** — public API, wire/serialization formats, load-bearing
  subtle code, "duplication" that might be intentional. Present the trade-off;
  don't decide for them.
- **Abstraction opportunities** — where the audit surfaces *missing* structure
  that would genuinely pay: duplication a shared helper collapses (fewer
  edit-N-places sites), primitive obsession a named type designs a bug class out
  of, an untestable dependency a trait/seam unlocks. Propose each as a concrete
  sketch with its **benefit and its cost** (indirection, more code, a new
  module), and **ask before applying** — recommend only when you'd defend it on
  the merits, and say plainly when the duplication is honestly fine as-is.

**This bucket is mandatory, never empty by omission.** `xtask audit` only finds
the subtractive stuff (dead code, unused deps); the additive wins are invisible to
it and are often the highest-value outcome of the whole audit. Always run the
abstraction pass by hand and **state the conclusion explicitly** — either "here
are the opportunities" or "none warranted, and here's why." A report that lists
only deletions has skipped half its job. Fast heuristics for the by-hand pass:
- **Primitive obsession:** a function returning a bare tuple (`-> (usize, usize,
  usize, usize)`) or a cluster of free functions all taking/returning the same raw
  `u64`/`usize` that has a *semantic* identity → a newtype. **Tell:** the same
  tuple destructured (`let (a, b, _, _) = …`) at many call sites.
- **Finish-the-pattern:** the crate already has one newtype (`PtePerms(u64)`) but
  a sibling concept stays raw (`u64` PTEs) → extend the existing idiom, low
  friction, matches house style.
- **God-`u64`:** one `u64` plays several roles (a PTE, a PA, perm-bits) so the
  compiler can't stop you passing the wrong one → newtypes make the mix a type
  error.

> **Worked example (SnitchOS, kernel-core `mmu`).** The mechanical audit found
> only `spin` (unused dep) + 3 demotes. The *valuable* outcome came from the
> mandatory by-hand pass: PTEs were raw `u64` manipulated by 6 free functions, and
> `split_va` returned a 4-`usize` tuple destructured at 8 sites. Offered two
> newtypes — `Pte(u64)` (`#[repr(transparent)]`, finishing the `PtePerms`
> precedent) and `Sv39Va` — with benefit/cost. Both shipped TDD-first behind the
> existing mmu tests + riscv build, net-neutral on lines, real safety gain
> (a PTE can no longer be confused with a PA; a vpn swap is a field-name error).
> *This is the kind of finding to actively hunt for — not a bonus, the point.*

Close with a one-line **mass estimate** (lines each bucket adds or removes).

## Step 5 — Apply (only on request)

Only if the human picks items. Follow the project's workflow (TDD where logic
changes); re-run tests + clippy after *each* removal to confirm nothing depended
on it; keep changes small and independently revertable. Never batch a big delete
without checking the suite is green.

## Anti-patterns

- Declaring code dead from one narrow grep — cross-check consumer crates and
  trait-dispatch / macro call sites (grep misses these), and for contract surface,
  the design docs (rule 6).
- Trusting an all-zero usage table without sanity-checking the grep harness.
- Treating all duplication as collapsible — some is honest divergence.
- Deleting `pub` API because the *repo* doesn't use it — it may be the point.
- *Imposing* an abstraction, or adding indirection that doesn't pay rent. (The
  opposite mistake is just as real: refusing to *offer* a warranted one because
  "less code" feels safer. Propose it, with costs, and let the human decide.)
- Bundling the refactor into the audit. Report first.
