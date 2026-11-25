---
name: repo-toolchain-gates
description: |
  Standard local gate stack for SDLC repos: mise (pinned toolchain + task-runner gates),
  lefthook (git-hook enforcement), betterleaks (secrets gate). Use when: (1) setting up or
  auditing a repo so `mise run check` is THE gate every agent (implementer/reviewer/
  integrator/critic) runs; (2) local lint passes but CI fails — linter version drift between
  [tools] pin and the CI action; (3) wiring pre-commit/pre-push hooks that workers can't
  skip; (4) running waves in git worktrees where hooks fire but mise tools error "config not
  trusted"; (5) adding a secrets gate to hooks + CI. Covers CI-parity pinning, lefthook via
  mise [tools], {staged_files}/stage_fixed, worktree hook sharing vs per-path mise trust,
  betterleaks git-history scans, self-hashing gate receipts, and the negative-fixture idiom.
author: Claude Code
version: 1.2.0
date: 2026-08-06
---

# Repo Toolchain + Gates (mise · lefthook · betterleaks)

## Problem

The bundle's doctrine is gates-as-executables: every role agent runs the same gate command
and trusts its exit code. That needs three things a bare repo lacks — a pinned toolchain
(same versions locally, in CI, and in every worker), one canonical gate command, and
enforcement that fires even when a worker forgets. mise + lefthook + betterleaks is the
verified stack for all three.

## The shape

```
mise.toml   [tools]  → pins EVERYTHING: language, uv, linters, lefthook
            [tasks]  → fmt / vet / lint / test / … and ONE aggregate:
            [tasks.check]  depends = ["fmt","vet","lint","test",…]   ← THE gate
lefthook.yml           → pre-commit = fast staged-file subset; pre-push = heavier subset
betterleaks            → secrets gate: a [tasks.secrets] Git-visible scan inside check +
                          a lefthook pre-push command; the full-history scan stays a separate
                          consent-requiring pre-publish step (pin the version always — see below)
```

`mise run check` is the single gate string agents need. The cartographer discovers it; the
implementer runs it before reporting done; the integrator re-runs it on the integration
branch; CI runs the same tasks. Hooks never run anything that is not a `check` leaf — never the
other way around.

**This bundle's own gate graph is the worked example, and it is conformance-frozen.**
`mise.toml`'s `[tasks.check]` depends on exactly `["validate","test","self-test","secrets"]`;
lefthook's pre-commit runs `validate` alone (the fast subset) and pre-push runs
`test`+`self-test`+`secrets`, so the two hooks together cover exactly those four leaves and
neither hook exceeds `check`; CI (`.github/workflows/validate.yml`) runs exactly `mise run check`
on three OSes with SHA-pinned
`actions/checkout` + `jdx/mise-action`. All three are the SAME graph. The enforcing test is the
contract: `tests/test_gate_graph.py` fails any `[tasks.check]` drift (`test_all_hollowing_mutations_fail`),
any tool-pin drift (`test_toolchain_config_mutations_fail`), any lefthook-superset or unpinned-CI
edit (the `MUTATIONS` table), and any `mise.lock` tamper (`assert_lock_mutation_fails`). Change the
graph only by updating that test in the same commit.

## mise: the rules that matter

- **Pin linters to the exact CI version, in `[tools]`, with a comment naming the CI file.**
  A real wave shipped locally-green/CI-red precisely because golangci-lint wasn't pinned to
  the version the CI action used. Bump both together:
  ```toml
  [tools]
  # Pinned to match .github/workflows/ci.yml golangci-lint-action version.
  golangci-lint = "2.12.2"
  lefthook = "2.1.10"
  ```
- **Install lefthook via `[tools]`, not brew/npm** — the hook manager itself is then
  version-pinned and present in CI and every worker without a separate install step.
- **A `contributor:setup` task owns contributor bootstrap**: `run = ["uv sync --all-extras --dev", "lefthook install"]`.
- Python repos: reuse the existing uv venv via `[env] _.python.venv = {path=".venv"}` —
  never let mise create a parallel one.
- Task args use the `usage` spec, not Tera `arg()`/`option()` (deprecated).

## lefthook: the patterns that matter

- `{staged_files}` + `stage_fixed: true` for auto-fixers (ruff format etc.) — the fix is
  re-staged, the commit proceeds.
- `glob:`/`exclude:` per command; `parallel: true` for independent checks.
- pre-commit = seconds (staged files only). pre-push = the heavier subset (unit tests,
  full-repo secrets scan). The FULL gate stays `mise run check`.
- `assert_lefthook_installed: true` makes a missing install loud instead of silent.
- Bypass exists (`--no-verify`, `LEFTHOOK=0`) — hooks are a guardrail for humans and
  workers, not a security boundary. CI re-runs the same gates.

## betterleaks: the secrets gate (wired here — Git-visible files, not history)

gitleaks-compatible fork (drop-in: same rules format, same flags) with live-credential
`--validation` and faster scans. This bundle uses two distinct surfaces:

- `scripts/secrets_scan.py` — asks Git for tracked files plus nonignored untracked files, then
  invokes `betterleaks dir --redact=100 --config <tracked-config> -- <batch...>` (lefthook
  pre-push / CI step). A force-tracked path beneath an ignored directory remains included.
- `betterleaks git .` — FULL git history. Run before making any repo public or handing a
  bundle to another machine; HEAD-only scans miss secrets deleted in later commits.

Exit code is the gate: 0 clean, 1 leaks. Unexpected scanner failures remain nonzero and outrank a
finding result. For a repo with a live secrets surface, wire the wrapper as a lefthook pre-push
command and a CI step; pair it with a repo-specific sweep (internal hostnames etc.) which generic
rules won't catch.

**Wiring status in THIS bundle: version-pinned, locked, and wired as a `check` leaf.**
`betterleaks` is wired into `mise run check`: `[tasks.secrets]` runs the Git-visible wrapper and
`[tasks.check]` depends on `["validate","test","self-test","secrets"]`, so the scan runs wherever
`mise run check` runs — including CI, which invokes exactly that one command. `lefthook.yml`
carries the same task as a **pre-push** command; pre-commit stays the fast `validate`-only subset,
because this is not a staged-file-only check.

**Always pass `--config` explicitly.** A bare `betterleaks dir .` auto-loads a drop-in
`.gitleaks.toml`/`.betterleaks.toml` from the working directory and honors
`GITLEAKS_CONFIG*`/`BETTERLEAKS_CONFIG*`, so an untracked, gitignorable file containing
`[extend]` `useDefault = false` replaces the entire ruleset and the gate keeps exiting 0 — the
worst kind of failure, because every pinned fixture stays green while nothing is being scanned.
The explicit flag has highest precedence and defeats both routes, so `[tasks.secrets]` points it
at the tracked, extend-only `.config/betterleaks.toml`. Pinning the flag alone would only move
the hazard into that file, so `scripts/validate_bundle.py` (`validate_secrets_config`) parses it
and requires exactly `[extend]` `useDefault = true` and nothing else: a neutering edit to the
pinned config fails `mise run validate`.

What is scanned and what is not is a deliberate boundary:

- **Scanned automatically: tracked files plus nonignored untracked files.** Git supplies the
  NUL-delimited set, so ignored operator/runtime state is absent without hiding a force-tracked
  path under the same prefix. Symlinks and non-regular entries are skipped rather than followed.
  This is the surface a commit or push can newly expose, and it is cheap enough for the default gate.
- **NOT scanned automatically: ignored untracked files.** They are not part of Git's visible change
  surface. If such runtime state needs its own audit, scan it by an explicit operation rather than
  broadening every repository gate and leaking foreign logs into normal test output.
- **NOT scanned automatically: git history** (`betterleaks git .`). History scanning is a
  separate, consent-requiring **pre-publish** step — run it deliberately before a repo is made
  public or handed to another machine, because rewriting or acting on a historical finding is an
  outward-effect decision, not something a commit hook should trigger. No task, hook, or CI step
  in this bundle invokes the history verb; `test_betterleaks_is_pinned_locked_and_wired` asserts
  that no executed task/hook/CI command string does.
- **A clean scan is evidence, not authorization.** Exit 0 means the pinned scanner's rules found
  nothing in the Git-visible files at that moment. It does not certify the absence of secrets (rules
  are heuristics, history is out of scope), and it grants no authority to push, publish, tag, or
  hand the bundle anywhere — each of those still needs explicit operation-specific authorization.

Two facts about the pin itself remain separate from the wiring, and both still matter:

1. **Pinnable without the registry (corrected 2026-08-05).** An earlier revision of this skill
   claimed betterleaks could not be pinned because it is absent from the mise registry. That
   was wrong: registry membership only supplies a default backend, and a backend can be named
   explicitly. `[tools."github:betterleaks/betterleaks"]` locks per-platform URLs and SHA-256
   checksums for all 11 platform keys — the same integrity surface an aqua-backed tool gets,
   and strictly stronger than the npm-backed pins, which lock version+backend only. Prefer
   `github:` over `ubi:`: `ubi:` is deprecated for removal in mise 2027.1.0 and locks no
   per-platform checksum. **Generalize this, don't just note it:** "not in the registry" is
   never by itself a reason a tool cannot be pinned. Check `mise backends` first.
2. **Its install must not smuggle in a second bootstrap prerequisite.** The `github:` backend
   fetches SLSA provenance and artifact attestations from the GitHub release API at install
   time. Unauthenticated, that request is rate-limited to a hard install failure, which would
   make `GITHUB_TOKEN` a prerequisite alongside mise — measured, not assumed. This bundle sets
   `github.slsa = false` and `github.github_attestations = false` in `[settings]` and relies on
   the reviewed per-platform checksum in `mise.lock` as the integrity control. A repo that
   already provisions a token everywhere may leave both enabled for defense in depth.

Pinning a tool and wiring its invocation are still two separate decisions; this bundle now does
both, and the earlier revision that stopped at pinning said so plainly rather than claiming a gate
it did not run. Keep them coupled in the enforcing tests:
`tests/test_gate_graph.py::test_betterleaks_is_pinned_locked_and_wired` requires the `[tools]`
pin, per-platform lock records, exact `[tasks.secrets]` wrapper command, wrapper selection/config
markers, `secrets` in `[tasks.check]`'s `depends`, and the pre-push hook command. The focused
`tests/test_secrets_scan.py` suite proves ignored-untracked exclusion, force-tracked inclusion,
NUL-safe names, batching, and exit precedence. `test_removing_secrets_from_check_is_caught` is the
mutation negative: hollowing `depends` back to the base three fails the validator. The `MUTATIONS`
table also refuses direct/history/no-op replacements and a config edit that disables defaults.
Any graph change updates `scripts/validate_bundle.py` (`REQUIRED_TASKS`, `SECRETS_COMMAND`,
`SECRETS_COMMAND_WINDOWS`, `SECRETS_CONFIG_PATH`, `validate_secrets_config`, the frozen `check`
table, the frozen `lefthook.yml` bytes) and those tests together; a tool-version change also
regenerates the SHA-pinned lock. A pinned, wired scanner is evidence infrastructure — running it
clean authorizes nothing.

## Pinning a tool that is not in the mise registry

Registry membership supplies a default backend, nothing more. Naming a backend explicitly
pins anything the backends can reach, so "not in the registry" is never on its own a reason a
tool stays unpinned. Run `mise backends` and pick by the integrity the backend can prove:

| Backend | Locks | Use when |
|---|---|---|
| `aqua:owner/repo` | per-platform URL + SHA-256, `provenance` where upstream attests | the tool is in the registry (this is what the registry usually selects) |
| `github:owner/repo` | per-platform URL + SHA-256 + release-asset API URL | a GitHub release publishes per-platform archives. Prefer over `ubi:` |
| `ubi:owner/repo` | version + backend only | never for new pins — deprecated for removal in mise 2027.1.0 |
| `npm:package` | version + backend only | the tool ships only to npm. Weakest of these; a version pin without a content hash |
| `http:name` | per-platform URL + checksum you supply | there is no release API at all; you accept manual URL maintenance |

Two rules that outrank convenience:

1. **A pin must not add a bootstrap prerequisite.** Verify the install path on a machine with
   no credentials in the environment before committing the pin. A backend that reaches an
   authenticated API during install (see the betterleaks section above) turns a token into a
   second prerequisite and breaks "mise is the only bootstrap prerequisite."
2. **Never fabricate a version.** Resolve it from the real distribution (`npm view <pkg>
   version`, the release API) and record what you resolved. If a tool genuinely cannot be
   pinned, declare it unpinned **with the stated reason** rather than inventing a number — an
   unstated omission and a reasoned one look identical in a diff six months later.

**A pin and the permission to use a tool a particular way are separate decisions — and the
separation survives the pin.** This bundle DOES pin `npm:@bitkyc08/opencodex` (MIT, npm backend,
`depends = ["node"]`), by explicit operator decision recorded in `docs/adr/0005`. The pin was taken
at 2.11.1 on 2026-08-09 and moved to 2.28.0 on 2026-08-20; `mise.toml` holds the exact number and
is the only authority for it, because a version quoted in prose here goes stale at the next bump
with nothing failing to say so. A bump is its own reviewed change: the wrapper's parsed contracts
and the behavioral prose in `skills/model-tier-rightsizing/references/` were re-diffed against the
new tarball, and the live-gateway restart that would re-measure runtime behavior stayed an explicit
operator step rather than riding along with the pin. An earlier revision of this skill
left it unpinned while the subscription-passthrough question was open; `docs/adr/0003`
closed that question, so the packaging decision was made on its own merits — like the two
npm pins above, the npm backend locks version+backend only, and the npm registry needs no
credential, so the pin adds no second bootstrap prerequisite.

The boundary is **usage-level, not packaging-level**, and it has since MOVED — which is the
more useful half of the lesson. `docs/adr/0003` originally read Anthropic's policy as
prohibiting Claude **subscription** OAuth through any third-party process, and
`scripts/opencodex-claude.sh` enforced that by isolating `CLAUDE_CONFIG_DIR`, scrubbing every
`ANTHROPIC*`/`CLAUDE*` variable, and refusing with exit 3. `docs/adr/0014` reversed it on
evidence: Anthropic's own gateway documentation describes base-URL-without-a-gateway-credential
as preserving the subscription's limits and billing, and the restriction that does exist binds
third-party developers routing on behalf of *their* users. So the scrub and the isolated dir are
gone, and what the wrapper refuses now is narrower and different: a provider-routing key or a
Console API key that would silently bypass the gateway or move billing off the subscription.

**Generalize this:** when a pinned tool's safe usage is narrower than its default behavior, the
narrowing belongs in an executable wrapper — prose in a skill file cannot refuse anything. The
reversal is the proof rather than the counterexample: because the boundary lived in code with
tests, moving it was a reviewable diff with its own ADR, and the old refusals could not linger
as folklore. Prose that had asserted the prohibition (including an earlier revision of this very
paragraph) went stale silently and had to be hunted down afterwards. Packaging feasibility was
never authorization to adopt, and a pin is not authorization for any particular use.

**Wrapping a tool that supervises a daemon: delegate the supervision, re-probe the health.**
The same launcher owns the gateway lifecycle (`launch` ensures-then-execs, `restart` =
stop+ensure), and it delegates every mechanism to the tool's own verbs rather than growing a
second supervisor: opencodex already does spawn, pidfile, port discovery, and an
**identity-checked** `/healthz` probe that requires the body to identify as opencodex, so a
foreign server answering on the port is not accepted. Its `ocx start` also refuses a second
instance natively, which is why the wrapper adds no competing pidfile — two concurrent
launches leave the pid unchanged. **What must NOT be delegated is the verdict.** Two verified
fail-open paths make an inherited exit code a lie: `ocx ensure` exits 0 *without starting
anything* when `codexAutoStart` is disabled, and `ocx status` exits 0 with the proxy down —
only `ocx health` returns nonzero. So the wrapper re-probes `ocx health` after every
supervision step and treats that alone as truth, then fails closed with a named reason
rather than launching against a dead or half-up daemon. The rule to carry: **a supervisor
you wrap can be trusted with the mechanism and never with the verdict** — find which single
verb's exit code actually reflects a probe, and prove the fail-closed path by binding the
port with a foreign listener instead of assuming the check works.

## Worktree waves: the two propagation facts (verified 2026-07-05)

1. **`.git/hooks` IS shared.** A worktree's `.git` file points into the main repo's
   gitdir; `core.hooksPath`/hooks resolve there. One `lefthook install` in the main repo →
   hooks fire in every wave worktree. Do NOT re-install per worktree.
2. **mise trust is NOT shared.** Trust is keyed on the config file's absolute path; a fresh
   `git worktree add` is untrusted even when the main repo is trusted. Consequence: hooks
   fire (fact 1) but any hook command resolved through mise shims errors with
   "config not trusted" — hooks work in main, fail in the worktree. This behavior is proven
   by `tests/test_gate_graph.py::test_paranoid_mode_requires_per_path_trust` (under
   `MISE_PARANOID=1`, a fresh copied repo's `mise tasks` fails "not trusted", then succeeds
   after `mise trust <path>`). Two routes:
   - **Persistent trust** — `mise trust <worktree-path>` (or `MISE_TRUSTED_CONFIG_PATHS=<path>`)
     mutates user trust config; it is a per-absolute-path change, right next to codex dir-trust,
     and needs explicit operation-specific approval for each exact reviewed path.
   - **Process-scoped, no persistent trust** — `mise --no-config --cd <worktree> exec ...` runs a
     gate without ever writing trust config (see the flagship skill's seeds-worktrees reference).
     Prefer this when a wave should not mutate user trust state to run one gate.

## Verification

- `mise run check` exits non-zero on a planted lint error (prove the gate falsifiable the
  day it ships).
- `git commit` in a worktree fires pre-commit (plant a staged `.py` with a lint error).
- `mise run secrets` exits 0 on a clean tree and 1 on a planted canary credential in an
  untracked, non-ignored scratch file (then delete the file) — that pair proves the wired scan
  falsifiable. Both halves verified on this tree 2026-08-06. Use `access_key = "AKIA<16 random
  A-Z0-9>"` and generate the tail fresh; the `aws_access_key_id` spelling is allowlisted upstream
  and reports clean, so it silently proves nothing (see the caveat under negative-fixture testing).
- With the canary still planted, add a drop-in `.gitleaks.toml` containing `[extend]`
  `useDefault = false` and confirm `mise run secrets` STILL exits 1, then confirm a bare
  `betterleaks dir .` in the same tree exits 0. That contrast — not the pinned run alone — is what
  proves `--config` defeats the neutering route rather than the hazard being absent. Verified both
  ways on this tree 2026-08-06, for the drop-in file and for `GITLEAKS_CONFIG`.
- `betterleaks git .` exits 1 on a planted AWS key in a test commit (then drop the commit). Run
  the history verb deliberately, by hand, as the pre-publish step; nothing invokes it for you.

## Negative-fixture gate testing (the falsifiability doctrine)

**Every gate ships an offline fixture per known failure mode; the test asserts the gate fails with
the *specific* expected exit code / diagnostic — a gate with only green tests is unproven.** This
is not aspirational here: `tests/test_gate_graph.py` already IS the harness. It proves each fail
path fires:

- config-hollowing fails with an exact diagnostic — the `MUTATIONS` table + `test_all_hollowing_mutations_fail`,
  each asserting `returncode == 1` AND `assertIn(diagnostic, result.stderr)`.
- toolchain-pin drift fails — `TOOLCHAIN_MUTATIONS` + `test_toolchain_config_mutations_fail`.
- `mise.lock` tamper fails — `assert_lock_mutation_fails`, `test_lock_mutation_fails_through_cli`.
- description-bypass variants fail — `test_folded_description_variants_cannot_bypass_validation`.
- worktree-untrusted mise fails then trust fixes — `test_paranoid_mode_requires_per_path_trust`.
- unwiring the secrets leaf fails — `test_removing_secrets_from_check_is_caught`, plus the
  `MUTATIONS` rows that swap the working-tree verb for the history verb or for `true`.
- neutering the secrets leaf without unwiring it fails — the `MUTATIONS` rows that strip
  `--config` from `run`/`run_windows` and that flip `useDefault` to `false` in the pinned config.

Fixture rules (match the existing `tests/` posture): offline, synthetic, non-secret, and
self-cleaning (`tempfile.TemporaryDirectory`, drop the commit). A secrets fixture uses a documented
**test-pattern/canary** token, never a real credential, and is never used as production evidence.
**Verified caveat (2026-08-06): a randomized tail is necessary but NOT sufficient — the surrounding
keyword decides whether the rule fires at all.** Measured on betterleaks 1.7.3 with the same
freshly-random `AKIA…` tail in the same file: `access_key = "AKIA<tail>"` and `AWS_KEY = "AKIA<tail>"`
exit 1, while `aws_access_key_id = "AKIA<tail>"`, the bare token alone, and the unquoted form all
report clean. The documentation-shaped keyword is allowlisted upstream, so the most natural-looking
canary is exactly the one that proves nothing. File extension and base32-vs-full-alphanumeric tails
made no difference. **Always confirm the fixture fails before trusting any green case**, and pair a
neutering probe with it — a scan that cannot be shown to fail is not evidence.
**Pin update (2026-08-19): the mise pin is now betterleaks 1.8.1**, adding the `generic-password`
and `generic-credential-uri` detectors; re-run the fixture-failure confirmation above against the
new pin rather than assuming the 1.7.3 measurement still holds unchanged.
Reuse the existing helpers (`copied_repo`, `run_validator`, `assert_lock_mutation_fails`,
`isolated_mise_env`) — do not fork a parallel harness.

## Gate receipts (self-describing evidence)

A gate's own evidence should be self-describing and tamper-evident by re-derivation. `scripts/gate_receipt.py`
(stdlib-only) both builds a canonical receipt and *is* the producer that runs a gate to make one. Fields:

Every field is a **record** the producer made and any consumer can re-derive — tamper-evident, not
proof against a forger who is the same OS user:

- `gate` — the exact task string, e.g. `"mise run check"`.
- `argv` — the exact argv **executed** (e.g. `["mise","run","check"]`), so the receipt names *which*
  command ran rather than a paraphrase of it — or `null` when nothing was executed. A populated
  `argv` claims that this command ran, so it may sit beside `outcome: unobserved` only in the killed
  state, where `signal` says why there is no verdict; the gate a skipped receipt is *about* is still
  on record as `gate`.
- `status` — the integer exit code, or `null` when no exit code was observed.
- `signal` — the signal number that killed the gate, or `null`. A killed gate ran but produced no
  verdict, which is neither an exit code nor "never ran"; a negative `status` would misreport it as
  a failing verdict, so `status` stays `null` and the signal is recorded here.
- `outcome` — `passed` | `failed` | `unobserved`, derived from `status`. **"The gate never ran" and
  "the gate ran and failed" are different facts**, and a consumer that conflates them reads an
  absent gate as a failing one — or a never-run gate as satisfiable. Because the value is derived,
  no exit code can spell `unobserved`; only `status: null` can. `unobserved` says *no verdict was
  observed*, which is weaker than "nothing ran": it covers the never-run and the killed state alike,
  and only `argv`/`signal` separate those two.
- `log_digest` — `sha256` of the captured combined stdout+stderr bytes: every byte captured, which
  for a killed gate is what it emitted before the kill and for an unobserved run is nothing at all.
  It makes a stored log tamper-evident without storing the whole log; it says nothing about whether
  the log is complete.
- `toolchain_digest` — `sha256` of the `mise.lock` bytes read for this receipt (for an observed gate,
  read just before it ran), binding the receipt to the exact pinned toolchain. It is what *lets* a
  consumer catch "green on drifted pins" by comparison; the binding on its own catches nothing.
- `cwd` — the absolute path the gate ran in — for an unobserved receipt, the path it *would* have
  run in, because nothing ran there. Either way it ties the receipt to per-path worktree trust
  (above).
- `head` — `{commit, tree}` for the repository head `cwd` was on, or `null` when no head was
  observed. `cwd` anchors *where*, `toolchain_digest` anchors *which pins*, and this anchors *when in
  the repository's own history* — which is what lets a composer refuse a receipt derived against a
  different tree from the artifacts beside it. The tree
  comes from one `rev-parse <commit>^{tree}` derivation against the commit just read, so the pair
  cannot straddle a head that moved between two calls. `null` is honest and not an error: a
  non-repository `cwd`, an absent `git`, or a head that moved *while the gate ran* all record `null`,
  and a consumer that needs the anchor refuses the `null` rather than guessing. The anchor is head
  identity and not a timestamp because a host's clock can legitimately step backwards, while head
  identity is deterministic.
- `self_digest` — `sha256` of the canonical JSON of every other field.

Produce one with:

```bash
python scripts/gate_receipt.py record --gate "mise run check" --out <path|-> -- mise run check
```

`--out` is required and has **no default**: where a receipt belongs (machine-local, the ccodex XDG
state plane, or target-local) is an open operator decision, so the producer takes its destination
from the caller instead of picking a side. It never overwrites an existing receipt or log — occupied
evidence is preserved and the run refuses before the gate starts, as it does for a destination that
could not be created anyway (a missing or read-only parent directory) and for `--out` and `--log`
naming one path.

**Admit every effect at the instant it becomes true, never once the operation that caused it has
returned.** Where an effect is recorded IS the contract, and getting it wrong is the same defect
three times over:

- *A destination exists from its `open()` onward.* Created and then not written, it is a truncated
  non-receipt that verifies as nothing and — because the path is exclusive-create — blocks its own
  destination for every later run, which then refuses it as "existing evidence". So the producer
  admits the creation where it happens, removes its OWN half-written file (never a file it did not
  create, and never the occupied evidence above), and names the disposition in the reason: *the
  incomplete file was removed*, or *an INCOMPLETE file REMAINS at …* if the removal also failed.
  Removing it launders nothing — the creation stays admitted, so the exit is `4`.
- *A gate has RUN from its `Popen` onward, not from its `wait`.* Its side effects are already in the
  worktree while its output is still streaming, and the mirror, the read, and `wait` itself can all
  raise in between. Admitting the run after the call returns classified every one of those as
  "nothing happened" (`1`) on top of a gate that provably ran, so the run is admitted inside the
  runner, at the `Popen`, and the effects ledger is a required argument there rather than something
  a caller can forget. Guarding each raise site instead only postpones the defect to the next one.

Mirroring the gate's output to stderr is a display convenience `--quiet` switches off, never the
evidence, so it must not be able to cost a completed gate its receipt: the sink is resolved once
before the gate starts and a TEXT `sys.stderr` (what `unittest --buffer` and
`contextlib.redirect_stderr` install, and it has no `.buffer`) is written as decoded text instead of
raising. `log_digest` is over the raw captured bytes either way. A mirror write that genuinely fails
still lands inside the run window and so still reports `4`.

**The exit code describes the producer, and the receipt carries the verdict.** The two channels are
deliberately separate, because an exit code cannot carry both: the producer's own codes follow the
repository's effect-aware contract (product-spec Implementation Decision 9) —

| code | meaning |
| --- | --- |
| `0` | the gate ran, passed, and its receipt was written |
| `1` | unexpected internal failure, nothing done |
| `2` | unusable arguments — including `--log -`, which would interleave raw log bytes with a receipt on stdout |
| `3` | clean refusal *before* the gate ran and before any destination was created |
| `4` | the gate ran, a destination was created (whether or not its bytes landed), and/or receipt bytes reached stdout, then something failed: the result is partial or unknown, and the producer names what already happened |
| `5` | the gate ran and failed; its exact code is the receipt's `status` |
| `6` | a receipt was written but no verdict was observed — `--unobserved`, a gate that could not be started, or a gate killed by a signal |

A gate's own exit code is **never** passed through. Mirroring it looked honest and was not: a gate
exiting `3` is byte-identical to the producer's own clean refusal, and `3` is this repository's
canonical clean-refusal code, so that is a likely gate exit here rather than a theoretical one. The
same collision would hit `1`, `2`, and `4`. So `outcome` (a derived, digest-covered field) is where
the verdict lives, `status` keeps the gate's exact code, and the exit code answers only "what did
the producer do?" — a red gate still never surfaces as a green producer exit. Codes `1`–`4` in
particular must keep separating "I refused before touching anything" from "work happened and the
evidence is incomplete"; reporting the latter as the former is the defect this producer is built
not to have. The producer is deliberately **not** a leaf of `mise run check` — a receipt producer
running inside the gate it receipts is circular, and `check`'s leaves are validator-pinned.

This makes **worktree-green ≠ main-green** machine-checkable: the integrator's re-gate-on-MAIN
(see the flagship skill's worktree-integration reference) produces one such receipt; a
worktree-green receipt whose `cwd` ≠ main and whose `toolchain_digest` differs from main's is
exactly the failure that reference warns about. `tests/test_gate_receipts.py` covers the green
path and the negative fixtures (`test_tampered_receipt_field_fails_self_digest`,
`test_toolchain_digest_binds_lock`); `tests/test_gate_receipt_producer.py` covers the producer
against injected fake gates (never the ~11-minute real one), the unobserved/failed/killed
distinctions, the effect-aware exits (a marker file the fake gate writes is what proves a refusal
happened *before* the gate ran; an `RLIMIT_FSIZE` cap is what makes a write fail *after* its
destination was created; a `wait` that reaps the child and then raises is what puts a failure
*inside* the run window, where an admission made after the runner returns reports `1` for work that
already happened), and pre-`outcome` receipt compatibility. In any receipt that carries
`outcome`, `verify_receipt` rejects `argv`/`status`/`signal` combinations that do not spell one of the
four honest states, so a self-contradicting receipt fails verification instead of needing a careful
reader; receipts written before `outcome` existed predate those invariants and are checked by
re-derivation alone, which is what keeps them verifiable. This is doctrine
+ a helper, not a second task runner, and
a receipt is evidence only — it authorizes no push, publication, PR mutation, merge, or deployment.

## Tier-1 self-hashing canonical-JSON evidence

Receipts (and any wave/gate-run summary artifact) use the canonical serialization the bundle's
validator already uses (`scripts/validate_bundle.py` `sha256_bytes` + canonical digest binding):

```python
canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
digest = hashlib.sha256(canonical).hexdigest()
```

A self-hashing artifact carries `self_digest` over the canonical form of all *other* fields, so any
consumer re-derives and compares byte-for-byte. **Honesty caveat (carried verbatim into doctrine):
this is tamper *detection* by re-derivation, not a security boundary against the same OS user** —
the same posture `scripts/validate_bundle.py` already documents for its receipt validation. Tier-2
HMAC is explicitly out of scope: the gate stack has no cross-session issuer/verifier split that
would need a keyed MAC, and adding one would over-claim a boundary the code does not enforce.

## Notes

- The upstream bundle demonstrates the distinction directly: mise manages the lefthook
  binary, while repository activation is separate. A lefthook binary does nothing
  until hooks are configured and installed.
- See also (in the flagship `agentic-sdlc` skill): the seeds-worktrees
  reference (config propagation into worktrees), the sdlc-loop reference (where gates sit
  in the loop), and the bundle's validate-bundle.sh (a worked example of a repo-specific
  gate script).

## References

- mise docs: https://mise.jdx.dev (tools, tasks, trust)
- lefthook docs: https://lefthook.dev (config reference)
- betterleaks: https://betterleaks.com (gitleaks-compatible; `--validation`)
