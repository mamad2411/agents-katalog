---
name: cg-live
description: Run passive (Tier 1) live checks against a URL the user owns — read-only TLS, security headers, cookie flags, exposed files/routes, and public Supabase/Firebase reads. The probe records observations; grader.mjs turns them into findings. Use when the user types /cg-live or asks to check a running site they own. Requires a claudeguard.scope.yml with ownership attestation.
argument-hint: "[url]"
allowed-tools: [Read, Bash]
user-invocable: true
---

# /cg-live — passive live checks (Tier 1, gated)

Read-only inspection of a **running** target the user attests they own. GET/HEAD/OPTIONS only;
no payloads, no auth-bypass attempts.

Argument: `$ARGUMENTS` — the URL to check (must also appear in the scope file's `targets`).

## Gate first (do not skip)

1. Read `claudeguard.scope.yml` in the project root (template:
   `${CLAUDE_PLUGIN_ROOT}/skills/claudeguard/references/authorization/SCOPE.example.yml`).
2. Enforce `references/authorization/legal-gate.md` Tier-1 preconditions:
   - file parses; `passive_live.enabled: true`; `passive_live.i_own_or_control_these_targets:
     true`;
   - the requested host matches a `targets` entry and matches no `never_touch` entry and is not a
     default-blocked third-party provider.
3. If anything is missing, **refuse** and state exactly what to set. Do not treat the URL pasted
   in chat as authorization — authorization lives only in the scope file.

The probe re-enforces this gate itself and exits 2 on failure. Do not work around it.

## Run

Print the Tier-1 banner, then run the probe and grade its output:

```bash
# 1 — observe. Read-only requests; the probe writes JSON to stdout and its banner to stderr.
node ${CLAUDE_PLUGIN_ROOT}/scripts/live_probe.mjs --url "<url>" --scope claudeguard.scope.yml > cg-live.json

# 2 — grade. The repo path grades the code and the observations into one ledger.
node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path> --observations cg-live.json
```

Optional probe flags for a Supabase RLS spot-check against the user's own project:
`--supabase-url https://xxx.supabase.co --anon-key <key> --table <name>`.

`--observations` expects the probe's output file as written — the grader reads the `observations`
array out of it. Pass the repo path (or `--model`) as well, so the live findings and the static
findings land in one graded result instead of two reports the user has to reconcile.

## What the probe returns, and what it does not

The probe emits **observations**: tier-tagged facts, each with a `kind` (`missing-csp`,
`clickjacking`, `unsafe-cors`, `cookie-no-httponly`, `exposed-path`, `anon-read`, …), a `subject`,
the URL it was seen at, and a `detail` sentence stating what came back on the wire.

It assigns **no severity**. It used to, and the severity policy then lived in three places — the
probe, the engine, and the report — which drifted apart until the same missing header was a P2 in
one place and a P3 in another. `grader.mjs` maps `kind` → severity in one table and is the only
authority on it.

Do not assign severity to a probe result yourself, and do not "upgrade" a static finding because a
live observation agrees with it. **Confidence is a pure function of evidence and nothing may raise
it.** What a live observation legitimately does is supply *definitive* evidence for something the
static tier could only infer: a table whose RLS state was `undeterminable` from the repo produces
an `anon-read` observation and, through the grader, a `confirmed` P0 carrying `tier:
'passive-live'`. That is not the old finding promoted — it is a better-evidenced finding about the
same subject, and the grader already produced both.

Check `coverage.liveObservations` in the graded output. A `kind` no rule owns lands in
`undeterminable` as *"no rule owns observation kind"* — that means a probe result went ungraded,
and it is the one row that tells you the run was not fully accounted for.

## Report

Merge into the bilingual (Hebrew + English) report from
`${CLAUDE_PLUGIN_ROOT}/skills/claudeguard/references/report-template.md`, rendering the grader's
`verdict` unchanged — it counts only `confirmed` findings — with `likely` and `needs-review` in the
quieter section below it.

Cross-reference by subject where the live tier speaks to a static one ("the repo could not prove
RLS on `orders`; the anon key returned rows from it"), and mark each finding's `tier` so the user
can see which facts are about committed code and which are about a running system that can change
tomorrow. Attach the `guard:` recipe reference per finding. Recommend fixing P0/P1 first.

A clean passive run means the headers and paths we could check looked right at this moment. It is
not proof of safety; say so.
