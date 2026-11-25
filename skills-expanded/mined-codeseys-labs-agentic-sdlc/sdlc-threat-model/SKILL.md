---
name: sdlc-threat-model
description: >-
  Fires when a trust boundary is created, moved, or deleted — during framing, planning, or
  review of one scoped subject (one diff, one subsystem, one boundary) — and before a change
  touching identity, credentials, untrusted input, or an authority boundary is accepted.
  Also fires on the symptom of a residual window named in prose with no threat record behind
  it, and when a mitigation claims to close a finding: a mitigated subject is re-reviewed,
  never waved through. Applies STRIDE-shaped lenses over the bound snapshot and returns
  classified, evidence-graded findings as seed-shaped recommendations with human-only risk
  disposition. Advisory, never a gate leaf: it attacks, never fixes; never scans beyond the
  bound subject; consumes no CVE or vulnerability feeds; files no seeds itself. Not for
  generic secure code review (reviewer/critic lenses) or complexity audit
  (reviewing-overengineering).
---

# SDLC threat model

Enumerate what threatens one bound trust boundary, then report without fixing. Threat analysis
is agent work; risk ownership is human work, and the two never merge (ADR-0026). The output is
a findings report a conductor can capture as evidence; it authorizes nothing.

## Bind the subject

A run binds exactly one subject before any lens fires — one diff, one subsystem, or one trust
boundary — as an immutable snapshot: commit, tree/diff digest, or frozen plan bytes. Record the
producer of the subject and the lens actor, and when available run the lenses from a different
model or independent perspective than the producer's. Record the session budget at admission.
The whole repository is never a subject: refuse "threat-model the repo" with an offer to scope.
A run that discovers an adjacent boundary returns it as a seed-shaped recommendation for a
future subject and never silently widens.

## Run the six lenses

Read `references/stride-lenses.md` for the full lens definitions, each grounded in one of this
repository's own named residual windows as a worked example. The question each lens asks of the
subject:

- **S — Spoofing:** enumerate every name resolved at use time (PATH lookups, provider and model
  ids, config keys) and ask who can write ahead of the resolver.
- **T — Tampering:** for every write sequence crossing the boundary, state the invariant at
  each intermediate step and which same-UID actor could interleave.
- **R — Repudiation:** for each mutation, name who writes the record, whether the mutator can
  rewrite it, and whether a later reader could reconstruct the action without trusting any
  single agent's prose.
- **I — Information disclosure:** list every sink a secret-adjacent value can reach (output,
  receipts, argv, configs, error text, caches) and verify the refusal fires before the first
  sink, not after.
- **D — Denial of service:** check that every loop, fan-out, render, and retry carries a budget
  and a stop condition, and that each deliberate refusal is distinguishable from a hang.
- **E — Elevation of privilege:** trace each verdict, receipt, or status the subject produces
  to every effect it could be cited for, and confirm an authorization step exists there that no
  agent can perform.

Coverage vocabulary: every subject element × lens pair records `applicable`, `not_applicable`
with rationale, `deferred` with owner and re-entry trigger, or `out_of_scope` citing the
approved boundary. A missing pair reads `not_evaluated` and blocks any coverage claim.
`no_threat_identified` states only that this run found none.

## Emit the report

One findings report per run, bound to the subject snapshot digest, in this order:

1. **Subject binding block** — subject kind (diff | subsystem | trust boundary), snapshot
   identifier, producer, lens actor and whether it is independent of the producer, date, and
   the admission-time budget.
2. **Disposition rows before findings** — one row per source consulted, per the `agentic-sdlc`
   skill's evidence-discipline reference: identifier, retrieved yes/partial/no, retrieval
   method, the class actually reached, author and relation, failed ranges for partials. Gaps
   stay in this report, visible: not-retrieved, partial, negative finding, staleness — never
   reconstructed across.
3. **Per-lens coverage table** using the vocabulary above.
4. **Findings**, each one a classified seed-shaped recommendation matching the critic's shape:

   ```
   {title, type, severity, blocking?,
    found_by: sdlc-threat-model,
    source: <subject snapshot digest>,
    stride: [<letters>],
    evidence: file:line + the observed mechanism, each claim carrying exactly one of the five
              evidence classes (primary-artifact | primary-claim | vendor-doc | author-claim |
              community-report; sub-class partial retrievals, e.g. vendor-doc-snippet),
    acceptance: what a mitigation must demonstrate, stated as a checkable condition,
    class: ACTIVE_MILESTONE | BLOCKED_CI | BLOCKED_DESIGN | BLOCKED_DEPENDENCY |
           POST_MILESTONE | OUT_OF_SCOPE | DUPLICATE | INVALID,
    rationale}
   ```

   Classes come once, at retrieval, from the agent that retrieved the artifact; no later actor
   raises one. Refuse the refused phrasings: never "verified" — write the command and its
   output; never "the code does X" — write `path:line` plus class.
5. **Structured submission** with exactly the critic's headings — `role`, `scope`, `findings`,
   `evidence`, `recommendation`, `blockers`, `unknowns`, `next_action` — so a conductor
   consumes threat findings and critique findings through one contract.

**Human-only disposition.** The report carries a disposition column that the run leaves empty
except for `pending`. Agents may draft a proposed disposition in `recommendation`, clearly
labeled a proposal; only a human writes accepted / action / deferred / dismissed / external,
with rationale, identity, and (for deferrals) expiry. A disposition written by any agent,
including the conductor, is a defect. Mitigation of an accepted finding is an ordinary
authorized SDLC workstream; its verification is a new run by a different actor against the new
snapshot — a mitigated subject is re-reviewed, never waved through, and `implemented` never
implies `verified`.

The report's closing line states verbatim that no finding, coverage result, or disposition in
it authorizes any outward effect.

## What this skill refuses, by name

1. **No scanning-the-world.** The subject is one named immutable snapshot; a whole-repository
   request is refused with an offer to scope one boundary, one subsystem, or one diff.
2. **No CVE or vulnerability feeds, no scanners.** Vulnerability scanning, dependency scanning,
   penetration testing, red-team execution, incident response, forensics, and compliance audit
   are separate capabilities or human responsibilities. Work from the repository's own
   artifacts, ADRs, and stated residuals; route a feed request away by name.
3. **No gate integration.** Never a gate leaf: not reachable from the repository gate, git
   hooks, or CI, and no policy may make a run's outcome block a commit. A completed run never
   means the system is secure.
4. **No auto-filed seeds.** Findings are recommendations for conductor capture; only the
   conductor mutates the queue, through its own recorded write path.
5. **No fixes, no self-verified mitigations.** Attack, never fix: never edit the subject and
   never propose a patch hunk as a finding.
6. **No agent-written risk disposition, no completeness claims.** Disposition stays `pending`
   until a human writes it. Full STRIDE coverage, a clean coverage table, or zero findings
   never becomes a security-completeness claim, and the report states its snapshot and date
   because its truth decays silently from there.
7. **No sensitive-content egress by default.** The working set defaults to local, untracked
   storage; publishing a threat report anywhere outward — repository tracking, a PR body, an
   external tool — is a separately authorized, operation-specific effect. A threat report is a
   map of the softest ground and is treated with the sensitivity of one.

## References

Read only what is needed:

- `references/stride-lenses.md`: the six STRIDE lenses in full — what each letter means against
  a real trust boundary, a worked example anchored in a named, already-documented residual
  window of this repository, and the question the lens asks of any subject.

## Admission rationale

This skill clears all four admission gates: its description selects trust-boundary threat
enumeration and rejects both neighbors (generic secure code review belongs to the
reviewer/critic lenses; complexity audit belongs to reviewing-overengineering); the rate of
authority-boundary changes justifies one small row; residual windows named in prose with no
threat records behind them exist now; and a bounded run over one bound subject is task-shaped,
not always-on. It clears all five promotion signals: **Recurs; needs sequencing; has repeated
failure modes; has stable input/output; benefits from explicit handoff**.
