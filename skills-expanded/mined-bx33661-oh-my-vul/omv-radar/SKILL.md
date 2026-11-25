---
name: omv-radar
description: |
  Variant-driven diffusion hunting for oh-my-vul. Use when the user has a confirmed or publicly disclosed vulnerability pattern and wants to find the same bug class in sibling packages, forks, or downstream consumers; also when they ask for watchlist maintenance, radar brief, or `/omv-radar`. Reads seeds from findings and advisories, applies variant playbooks, and hands screened candidates to omv-audit.
---

# omv-radar

Turn one vulnerability pattern into many findings.

Radar's job is diffusion: a deeply understood bug (even one you could not
submit because it was already public) amortizes across every sibling package,
fork, and downstream consumer that still has the same sink and the same
missing guard.

## Invocation

```text
/omv-radar variant <seed-id>     # build a diffusion campaign from a seed
/omv-radar brief                 # watchlist + active campaign status
/omv-radar refresh [--dry-run]   # watchlist maintenance only
```

## Variant Workflow

1. Ingest the seed: read `.omv/findings/<seed-id>.yaml` (or a public
   advisory/fix-PR supplied by the user). Extract the seed fingerprint:
   sink shape, missing guard, and reachability precondition. All three are
   required — a sink without its precondition yields false positives.
2. Load `references/variant-playbooks.md` and classify the diffusion paths:
   sibling (same niche), fork/copied code, or downstream impact. State which
   paths apply to this seed and why.
3. Build the candidate list per path using the passive search mechanics in
   the playbook (registry keywords, code search, dependents graph, fix-commit
   mining). Names only, no auditing yet.
4. Quick-screen each candidate within the fetch budget (≤3 files): does the
   sink fingerprint exist, is the guard missing in the same way? Record
   candidates that pass with the evidence lines you saw.
5. Hand screened candidates to omv-audit as separate findings. Variant origin
   grants no exemption: each candidate still needs the full evidence chain
   and its own six-source dedup before any report.
6. Write the campaign to `.omv/campaigns/<seed-id>-variant.yaml` and link it
   back into the seed finding's notes.

## Judgment Rules

- A publicly disclosed seed is still a valid seed. Novelty is determined per
  target by dedup, not by the seed's disclosure state.
- If a campaign starts passing everything, the sink fingerprint is too wide —
  narrow it before continuing (see playbook §6).
- Prefer downstream targets where untrusted input demonstrably reaches the
  sink; they carry their own CWE and higher acceptance odds.

## Watchlist (secondary input)

The watchlist remains a low-cost input, not the product:

1. Read `.omv/radar/watchlist.yaml`.
2. `omv radar refresh --dry-run` for fixture-backed offline validation;
   `omv radar refresh` to append events locally.
3. `omv radar brief` for summaries.
4. Watchlist signals are triage aids: treat advisories, releases, and
   suspected-fix commits as new seeds for variant campaigns, never as proof.

## Passive Boundary

Radar may read advisories, registries, and public repository metadata. It
must not install or publish target packages, send requests to target runtime
services, run PoCs against targets, or probe deployments. Local reproduction
happens only inside omv-repro.

## Output

End with a concise brief:

- seed fingerprint (one line)
- diffusion paths pursued and candidate counts
- screened candidates handed to omv-audit, with the file:line seen
- watchlist changes worth knowing

If the watchlist is missing, tell the user to create `.omv/radar/watchlist.yaml`
with a sanitized example. Do not present any real active vulnerability as a
tutorial target.
