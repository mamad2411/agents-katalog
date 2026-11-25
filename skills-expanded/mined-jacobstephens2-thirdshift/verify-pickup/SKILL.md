---
name: verify-pickup
description: Model-check competing Pickup reservation and Claim changes. Use when changing src/pickup.rs, src/pickup/, src/ready.rs, src/claim.rs or their GitHub label and dispatch adapters, or when investigating double dispatch across hosts.
---

# Verify Pickup

The requested property is **at most one Run or Spec run dispatched per Ready
generation of one issue**. Duplicate dispatch can send competing work to the
same Issue branch. A Ready generation is identified by the Claim-application
count observed at selection; a fresh selection after a released Claim belongs
to the next generation. Reservation release alone starts no new generation.

**Known finding:** the literal property fails before the Claim. A Run can be
dispatched, fail before `claim::make` changes labels, and release its reservation.
A later Pickup dispatches that same generation. This check reports that failure;
its green CI regression is evidence that the counterexample remains reachable,
not a proof of the requested property. See [protocol.md](protocol.md) for the
request mapping, bounds, mutations and counterexamples.

## Run and judge

From the repository root, run:

```bash
cargo test --locked --test pickup_model -- --nocapture
```

Stateright is pinned in Cargo.toml and Cargo.lock; the existing Rust CI job runs
the same test target. No GitHub credentials, JVM or paid Harness is needed.
The ordinary run exhaustively checks the narrower **claimed dispatch** property,
records the known literal-property counterexample, and requires counterexamples
for both broken safeguards. The explicit literal assertion remains executable:

```bash
cargo test --locked --test pickup_model assert_requested_property -- --ignored --exact --nocapture
```

That assertion currently exits nonzero. Never describe a normal green suite as
proof that the literal property holds. Keep the original property when reporting
a bug; any change to the promise belongs to the Day shift.

For each new counterexample, replay every action against its named request and
the intervening local control flow. If an action cannot occur, correct the model
from the code and rerun. If all actions can occur, report a product bug in
GLOSSARY terms with its trace; keep the failing property and the evidence.
This skill authorizes verification edits only. Product fixes need their own task.

## Coverage and sync

Last confirmed source commit: `8b09cc703d76f5d081a2bd9a7742704db8fa872b`.
`ListReady` now maps to `GitHub::open_candidate_issues` (`src/ready.rs` → `src/github.rs`), which executes sequential read-only requests (`issues_labelled` REST, `graphql_open_issues_labelled` GraphQL, and optional per-omitted-issue `issue_labels` when `labels.hasNextPage` is true) and records disagreements in `activity.log`. Interleavings during those non-mutating reads preserve protocol safety because `standing_of` and `ready::refresh` re-read `candidate`, `issue`, and `candidate` under reservation before any Claim. Pickup ordering, paginated/REST-vs-GraphQL snapshot races, and Triage Pass candidate listing remain outside the one-issue model; same-second Claim history is normalized within its complete, ordered-read assumption. The known pre-Claim counterexample and both sensitivity mutations remain reachable. Claimed-dispatch safety passes; the explicit literal-property assertion and both mutation commands still fail with their expected traces. This change preserves the protocol and requires no model or property edits.
The model describes these functions, including their ordering:

| Source | Covered functions / requests |
| --- | --- |
| `src/pickup.rs` | `run`, `run_through`: reserve → refresh → dispatch; reservation lifetime |
| `src/pickup/reservation.rs` | `Reservation::take`, `Drop::drop`: empty create lease, owner-token release |
| `src/ready.rs` | `first`, `Search::first_priority`, `standing_of`, `refresh`: Ready reads and Claim-count comparison; Pickup keeps the settling wait |
| `src/claim.rs` | `make`, `Claimed::label_in_progress`, `Claimed::end`, `put_labels_back_unless_on_origin`, `release_labels`, `Claim::needs_info`, `Claimed::needs_info` |
| `src/github.rs` | `open_candidate_issues`, `open_issues_labelled`, `issue`, `candidate`, `ClaimHistory::after`, `issue_labels`, `set_labels` |
| `src/labels.rs` | `Edit::apply`, `request`: whole-label PUT; existing Claim is accepted |
| `src/pass.rs`, `src/run.rs` | `LaunchAndGitHub::dispatch`, `start`, `make_claim`, `end_claim`: dispatch before Claim; both Run kinds share it |

Compare all covered paths against the sync commit, including staged and unstaged
changes. Follow moved functions and search for new writers of reservation refs,
Ready/Claim labels and dispatch. Before updating this model, read ADR-0017 and the
relevant GLOSSARY entries via `docs/agents/domain.md`.

Update from changed requests and ordering, then run the check and both mutations
in protocol.md. Preserve every interleaving between distinct requests. Advance
the sync commit to the actual source commit reviewed only after confirming the
mapping and reporting any bugs. Record limits or newly uncovered paths rather
than implying they are verified. For merges that skipped this check, use
[maintain-formal-verification-skill](../maintain-formal-verification-skill/SKILL.md)
and report `in sync`, `updated`, `bug` or `blocked` for each check.
