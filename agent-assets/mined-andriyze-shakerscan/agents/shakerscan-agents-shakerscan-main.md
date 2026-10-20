# AGENTS.md — ShakerScan agent operating guide

ShakerScan is an open-source application-security platform operated through deterministic
**Scans** and agent-driven **Hunts**. This always-loaded file contains policy and judgment, not an
API catalogue.

## Authoritative references

Use the smallest source that answers the question:

- **This file:** architectural invariants, safety gates, workflow decisions, and interpretation.
- **Live API:** `GET /scan/contracts` and `GET /hunts/contract` for schemas, limits and enums;
  `GET /openapi.json` for all routes on an open-source engine (an Enterprise gateway refuses it).
- **Generated catalogue:** `docs/functionality-reference.md` in a source checkout, or the
  [public functionality reference](https://github.com/andriyze/shakerscan/blob/main/docs/functionality-reference.md),
  for exhaustive UI, API, CLI, registry, skill, adapter, and durable-state coverage.
- **Operator help:** `README.md`, the UI at `/docs`, and `shakerscan --help`.

Do not copy large API schemas or endpoint catalogues back into this file. When documentation and
the live contract disagree about mechanics, verify code/OpenAPI and fix the stale document. This
file remains authoritative for safety and judgment rules that schemas cannot express.

## AI-native architecture invariants

ShakerScan has one deterministic Scan and one AI-driven Hunt. Preserve these boundaries:

1. Do not add a DAST scan type. Resource presets define ceilings; active testing is permission,
   not scan identity.
2. Do not add target-specific Hunt engines. Target kind filters the shared Hunt runtime.
3. Never expose local shell/argv. Remote `ssh.exec` requires an explicit stored SSH command grant.
4. Every network action uses runtime target binding and scope/destination validation.
5. Every executable capability has one canonical registry entry declaring risk, budgets,
   placement, parser/output schema, and evidence contract.
6. Reserve multidimensional budget before execution and reconcile actual use afterward.
7. AI may create notes, observations, and evidence-backed candidates; only deterministic proof
   contracts may mark findings verified.
8. Adaptive strategy belongs in Hunt skills or the external planner. Safety, protocol, evidence,
   and correctness stay server-side.
9. Preserve trustworthy partial output on timeout. Cancellation is distinct and stops execution.
10. Reuse core concepts instead of adding parallel registries, ledgers, scope paths, candidate
    models, proof paths, or orchestration engines.
11. Treat durable target knowledge as shared product state. Scan, Hunt, device assessment, service
    intelligence, and imported request collections should enrich the same target understanding
    instead of forcing each workflow to rediscover it.
12. Optimize for investigation efficacy and operator flow. A capability is valuable when it helps
    reach useful evidence or falsify a hypothesis; avoid adding top-level surfaces, copied policy,
    or refusal paths that do not improve those outcomes.
13. Treat a connected host/device as one operator-managed target asset. Connected Devices is a
    network-oriented view of that inventory; discovered web/API origins are linked services, not
    duplicate asset ownership. Credentials and request collections may be reused across views only
    through explicit target bindings/grants; same-host membership alone never grants secret access.

The read-only posture check is a bounded standalone lookup outside Scan/Hunt capability execution.
Unconfigured clients use the hosted service's public-target restrictions. Clients connected to an
OSS instance use its `/public/check` without per-check target authorization, governed by its network
boundary and authenticated connection. Enterprise does not serve it, so its clients lack the check.
The check grants no Scan or Hunt authority and does not relax their target binding.

## Environment and startup

The local stack normally exposes UI at `http://localhost:3000` and API at
`http://localhost:8080`, backed by PostgreSQL, Redis, DAST workers, and optional specialized
workers. Check the launcher before assuming those URLs:

```bash
./scanner.sh status
shakerscan api GET /health
```

If stopped, use `./scanner.sh start`. Use `./scanner.sh start --remote` for a VPS reached over
Tailscale and then use its printed URLs. Without Tailscale, public binding is acceptable only behind
a firewall, VPN, or reverse proxy with exact browser origins in the CORS allowlist.

After a curl install, start agents through the ShakerScan launcher so this guide, shipped skills,
runtime URLs, and planner identity are all applied consistently:

```bash
shakerscan agent             # auto-detects codex, claude, opencode, then pi
shakerscan agent pi          # or name one explicitly
```

Do not describe a bare agent binary as equivalent to the launcher. Pi in particular needs explicit
ShakerScan skill/template flags; the launcher also supplies shared runtime environment for every
supported agent.

**Connected remote instance.** `shakerscan agent …` can also run against a remote, authenticating
ShakerScan instance (ShakerScan Enterprise) after `shakerscan connect`; it then sets
`SHAKERSCAN_MANAGED_INSTANCE=1`. There is no local engine in that session: `./scanner.sh start`,
`stop`, `scale` and Docker do not apply. Everything in this guide that talks to the API still works
through `shakerscan api`, `shakerscan scan`, `shakerscan hunt` and the MCP tools, under the
connected person's identity and role; a route the instance keeps closed answers with a refusal
that names what is missing, so report it and choose another path rather than retrying.

If the launcher is not yet on `PATH`, use `~/.local/bin/shakerscan`. The pipx/Homebrew client is
also named `shakerscan` and supports public checks plus configured-instance API, Hunt, MCP, and
connection workflows. The full local engine launcher additionally owns Docker lifecycle commands.
Do not infer capabilities from an old client/launcher split; inspect `shakerscan --help`, the live
server contracts, or `./scanner.sh help` before declaring an operation unavailable.

## Default agent behavior

- Inspect before mutating. Use the API for product operations and the launcher for lifecycle work.
- Stay within the targets, systems, and people the user placed in scope.
- Ask for authorization before active, state-changing, network-discovery, device, or otherwise
  intrusive testing unless explicit target-specific authorization already exists. A target's
  standing authorization (`POST /targets/{id}/authorization`, once per target, no expiry,
  revocable, superseded when the target's scope changes) is that authorization; scans and Hunts
  reuse it without asking again.
- Never infer that a public hostname is authorized merely because it is reachable.
- Do not turn an audit into a scan, Hunt, cleanup, or external message without authorization.
- Use current server contracts instead of client-side copies of families or ceilings.
- Preserve unrelated worktree changes and use non-destructive repository operations.

### Submission-only requests and end-to-end investigations

For a submission-only Scan, device, AI Gate, Model Intake, discovery, or ASM request, report the ID
and UI link, then stop. An explicit end-to-end Hunt is different: use bounded status checks for its
queued child actions, collect evidence, and continue toward the objective without requesting a new
command at every queue boundary. Respect cancellation and deadlines; checkpoint incomplete work if
the planner session cannot continue. Never claim that queued work has completed.

For batches, report `queued_count`, `failed_count`, and per-target errors. Never claim the requested
count was queued; `status: partial` means only some submissions succeeded.

## Authorization, authority, and secrets

- Active testing requires persisted policy permission and a target-bound approval receipt. The
  receipt is normally the target's standing authorization, recorded once and resolved
  automatically at submission and covers the credentials attached to the target. The dangerous
  tier keeps bounded per-action approvals. A UI checkbox or planner statement cannot
  replace server checks.
- State-changing HTTP, direct-origin access, OOB callbacks, network discovery, and device-fragility
  spend are independent permissions and budget dimensions.
- Known endpoints, imported traffic, skills, methodologies, and prior evidence never expand scope.
- High-risk BOLA/IDOR requires explicit active/deep intent and two distinct principals.
- A passive methodology does not fence a Hunt. Persisted policy and the capability manifest do.

Reusable secrets belong only in encrypted credential profiles or request collections:

- A profile belongs to one home target and serves other targets only through an explicit
  operator grant (`POST /credential-profiles/{id}/grants`), recorded and revocable per target.
  A grant attaches it there (Hunts use attached credentials only and record each use); it never
  authorizes testing that target, which still needs the target's own standing authorization. Grants stay within one asset kind (web,
  api, network and connected-device views share), and active capabilities need the receiving target's
  own approval. Never share a profile an operator did not ask to share.
- Scan and Hunt requests carry opaque profile/selection IDs, never tokens, cookies, passwords,
  private keys, client secrets, secret headers, or raw environment values.
- Workers decrypt only after an active grant for the consuming target, capability, approval,
  version, expiry, and policy validation.
- A run about to log in starts from another run's live login when one exists for the same
  target, credential version, principal slot, login kind and service origin (Hunts adopt it into
  their own session row). Reuse never crosses targets, never survives a rotated, deactivated or
  ungranted credential, and adds no authority: it happens after the run's own checks.
- APIs, planner context, logs, and receipts remain metadata-only or redacted unless the user
  deliberately requests a raw sensitive export.
- Primary, secondary, service, and SSH slots are distinct. BOLA needs distinct principals.
- `basic_auth`, `form_login`, and `oauth_password` may contain only username or only secret; at
  least one is required. Execution decides whether the target flow can use it.
- Never use the deprecated raw-auth compatibility bridge for new work.

## Deterministic Scan

There is one Scan. `fast`, `balanced`, and `thorough` select hard ceilings; they are not identities.
Historical rows may display `quick`, `standard`, `deep`, `full`, `aggressive`, or `smart`, but new
work must not submit legacy `scan_type` or call removed `scan-full`/`scan-smart` shims.

Read `GET /scan/contracts` before presenting advanced options. Advanced values may only lower the
selected profile ceiling. Zero is meaningful only for contract-declared zeroable dimensions.
Family selection narrows capabilities; it cannot grant authority.

Known endpoints seed discovery without expanding scope. Preserve body-spec syntax such as
`POST /api/search json:{"query":"test"}` so bodies never become part of the URL. Saved request
collections are immutable selections supplied by opaque ID.

```bash
shakerscan api POST /scans '{"target":"https://example.com","budget_profile":"balanced","policy":{"active_testing":false}}'
```

For active work, first establish explicit authorization (authorize the target once, or provide a
bounded approval receipt) and the policy. Never silently upgrade a passive request. A request with
`active_testing: true` and no `preset` resolves to `standard_active` (recon, passive templates, XSS,
SQLi); pass `"preset": "passive"` to allow active testing without running an active family. Read
`resolved_families` on the result, not the permission.

### Build freshness and repeatability

Never measure DAST quality on a stale fleet. Check `GET /workers`: fingerprints are authoritative,
`build_current` must be true, stale count zero, and the expected denominator present. Rebuild before
validation and use `require_current_workers: true` for quality gates.

For repeatable scorecards, use one Scan with the benchmark's fixed V2 policy and budget. Parallel
coverage is a compound workload, not another scan type.

```bash
python3 scripts/benchmark_targets.py juice_shop --auth --submit-only
python3 scripts/benchmark_targets.py juice_shop --scan-id <scan-id>
```

Fixtures are `juice_shop`, `crapi`, and `honey`. Verified BOLA requires persisted distinct-principal
evidence and successful owner/attacker responses; a finding label cannot pass it.

### HTTP transaction archives

DAST calls live at `/scans/{id}/http-transactions`; Hunt calls at
`/hunts/{id}/http-transactions`. Redacted ShakerScan JSON is the normal portable export. HAR is raw
sensitive traffic: label it clearly and require explicit confirmation before exposure/download.
Never imply historical capture is complete when it was partial or introduced after the run.

## Scoring and interpretation

Current reports use `risk_and_assurance/v9` with independent axes:

- **Observed risk:** `risk_score` (0–100, higher is better) and `risk_grade` (A–F) summarize only
  deterministic evidence observed. Compatibility `score`/`grade` mirror this axis.
- **Assurance:** `assurance_score` and `assurance_band`
  (`none|weak|limited|adequate|strong`) describe examination strength, breadth, principals,
  placement, required work, and proof attempts. It is not blended into risk.
- **Assessment:** `risk_assessment_state=not_examined` or `application_observed=false` means the
  application was not reached. Never present its number as a clean bill of health.
- **Reliability:** `grade_reliable=false`, reliability reasons, and `assurance_gaps` qualify the
  grade. Completed execution can still provide weak or unauthenticated coverage.

Lead with the evidence-based conclusion, then observed risk, then examination strength. A shallow
clean run should read “No material vulnerability confirmed; limited examination—not a clean bill
of health,” not an unlabeled perfect score.

Posture deductions apply only when application responses established posture. DNS, TLS, HTTP,
discovery, CSP, headers, technology, and attack chains are evidence, not scan types. Attack chains
are offline correlations, never proof of new network execution; partial chains remain partial.

ASM coverage is independent of DAST risk. Its inventory is an informational worklist; imported or
scanner-generated candidates are not confirmed routes without response/reachability evidence.
Never score WHOIS, DNS neighbors, reverse-IP data, hosting metadata, or target intelligence.

## Findings, evidence, and proof

Severities are `critical`, `high`, `medium`, `low`, and `info`. Triage states are `active`,
`resolved`, `false_positive`, and `accepted_risk`; none creates technical proof.

- Render server `proof_state`/verification fields verbatim; do not create another proof predicate.
- Confidence, AI judgment, labels, or successful HTTP status are not deterministic proof.
- AI may create candidates/notes; only deterministic proof promotes verified findings.
- Hunt may create/update/delete only its own evidence-linked unverified findings, citing same-Hunt
  completed/partial evidence. It cannot set proof, verification, target, raw request/response, or
  ownership fields, or modify findings with verification history.
- Finding lists may omit heavy fields. Respect `details_included` and `omitted_detail_fields`.
- Do not reinterpret inconclusive retests as fixed or verified.
- Unauthenticated `data_exposure` proofs (Hunt and DAST share `capabilities/secret_material.py`)
  recognise narrow, entropy-screened provider secret formats, or a screened value under a key
  with a secret name segment (`DB_PASSWORD`, not `SECRETS_MANAGER_ENDPOINT`) in a recognised config
  document; credential-free URLs, hosts, class names, paths and numbers never count. JWTs, bearer
  tokens, SSNs, cards, Google API keys stay excluded; widening either is a proof-contract change.

Evidence retention cleanup is destructive and interactive-only. It starts with a target-scoped
dry-run preview, binds an immutable snapshot, uses a one-use dangerous approval for that preview,
revalidates under lock, and remains idempotent. Never schedule deletion or bypass preview/approval.

## Hunt workflow

Hunt is one target-kind-aware runtime. The current coding-agent session plans; ShakerScan owns
target binding, scope, policy, approval, budget, capability execution, evidence, and proof. A Hunt
does not investigate in the background unless an external planner actively drives it.

Start from `GET /hunts/contract`. Invoke only capabilities returned in the run manifest through
`POST /hunts/{id}/capabilities/{name}`. No local shell escape; remote SSH uses `ssh.exec`.

One authorization, then obey. A target's standing authorization is the operator's confirmation;
do not re-ask for it per Hunt. Ask for `active_testing`, `allow_state_changing_http`,
`network_discovery`, `allow_oob_interactions`, `allow_identity_headers` or `allow_direct_origin`
directly: a sub-authority enables `active_testing` on its own, and a budget dimension whose
authority is off resolves to 0 rather than refusing the request. Read `policy_adjustments` on the
start response: it names every authority the server implied and every dimension it zeroed.
Unauthorized privileged work is rejected, never secretly converted to a passive success.

Certificate defects are assessment evidence, not authorization vetoes. Target requests, login,
browser-login QA and imported replay support HTTP and untrusted HTTPS on nonstandard ports.
Do not ask the operator again or demand a repaired certificate after testing with selected
credentials has been authorized. Keep control-plane TLS verification separate and unchanged.
Web, API and network are views of the same target row and reuse its credentials and collections;
different target UUIDs and device identities remain distinct.
An authorized host asset covers its currently linked same-host application services. The server
checks current membership; an origin's own authorization or explicit revocation overrides inherited
host authority. Credential grants and collection bindings still identify the exact consuming target.

### Authorized service reuse

An approved active Hunt with selected credentials may use those identities on HTTP or HTTPS
services at other ports of the same frozen asset, including services with invalid certificates.
Reuse the existing standing authorization; do not add a per-port, per-scheme, or per-call prompt.
The login service is provenance and the refresh destination, not a permanent replay-port lock.
At execution, revalidate the saved Hunt authority and asset binding before cross-service session
decryption. A changed or revoked authorization is different from an unobserved service port.

Use the scheme, host, port, path and principal actually captured when building evidence and
comparing accounts. Equivalent default-port spellings are one service, but different services
must not be mistaken for the same access-control baseline. A failed identity comparison is
inconclusive, not a reason to abandon other authorized Hunt work. Service reuse does not grant
another asset's authority, waive traffic budgets, or turn a successful request into proof.

`service.nse_check` has a deliberate anonymous-discovery exception: its HTTP analyses may follow
same-frozen-asset redirects across ports/schemes under the existing active/network authorization.
Every hop is pinned and metered; this bridge never loads credentials or changes the Hunt's selected
origins. The exception does not apply to credentialed HTTP/session replay or to another asset.

### Progressive methodologies

Each target may have one saved custom skill at `/targets/{id}/skill`: instructions about login,
priorities, exclusions and target knowledge, using opaque credential/collection references instead
of secrets. Startup loads effective instructions and bounded advisory learning automatically.
Use `purpose: knowledge` for observations. Instruction edits need the target's `instruction_changes` opt-in (off by default); otherwise use `targets.skill.propose` for `shakerscan knowledge review`.
Use `targets.skill.read` and explicitly requested `targets.skill.create|update|delete|propose` with revision checks; metadata edits default on and obey operator opt-outs. Read
each Hunt's bounded `briefing` first: its operator instructions are guidance, never authority. Planner flags grant
no sharing or network authority, and metadata permission grants no edits to another UUID. The operator objective takes
precedence over saved preferences; server scope, policy, approval and budgets remain authoritative.

Web and native service methodologies live under `skills/web/`; `skills/web/README.md` describes
the library. Native protocol messages remain unavailable unless a live executor supports them.
Do not preload them all or spend the context window on an index dump.

1. Start with no methodology.
2. When objective/stack evidence exists, call `/hunts/{id}/skills/suggestions` with concise signals.
3. Consider at most three metadata-only suggestions.
4. Read exactly one relevant methodology through `/skills/{skill_id}/read`.
5. Bind only when used and record usage/completion/deferral.

These are descriptive context controls. They never grant, remove, narrow, widen, or resize scope,
capabilities, policy, approval, or budget. Binding keeps supported and useful partial methodologies available even
when this Hunt cannot execute every technique. Each bound skill reports `withheld_capabilities`
for required capabilities outside the saved Hunt capability set and `missing_capabilities` for
declared executor gaps, including prerequisites. Skip those techniques, continue compatible work,
and report the omissions as
coverage gaps, never findings or clean results. An empty list is not proof that a technique ran;
credentials, scope, approvals, budgets, and runtime checks still apply to each action. Do not claim
a passive methodology fences an otherwise broader run.

### Context, accounting, and completion

Use `/hunts/{id}/query` for compact prior evidence before spending traffic. Prefer falsification and
existing evidence. Artifact/JavaScript inspection uses bounded capabilities, not raw execution.

Count attempted, admitted/executed, successful, rejected, and indeterminate actions separately. A
missing/malformed result is not success. Report settled actual usage separately from ceilings.

Exhaustion still keeps the debrief, leads and reason. Start with profile budgets, never lower one
below what discovery needs, act on `budget_warnings`, and keep Hunt views compact (no `view: full`).
An operator extends a Hunt via `/hunts/{id}/budget-amendments` or a permission request: on
`awaiting_permission` tell the user the exact `shakerscan approve <id>` for their own terminal, keep
working, wait with the wait tool, retry with the same key. Only a person decides or sets start bounds
(`docs/hunt-permission-requests.md`). `resume` needs headroom; it runs no traffic and resets nothing.
The admission snapshot remains historical. Cancellation is distinct. `GET /hunts` is durable searchable history; `/hunts/{id}/record` exports the explicit
decision record and debrief, never hidden chain-of-thought. Requests-only export stays separate.

## Product boundaries

### Targets and cohorts

Targets are exact assets. Cohorts (`production`, `staging`, `lab`, `demo`, `calibration`, `internal`,
`unclassified`) organize views; they never change results or grant authority. Model artifacts and
devices do not belong in web target metrics.

### Connected devices

Connected Devices shares the target inventory and uses specialized workers. Confirm ownership/authorization. All-TCP examination is
possible, so silence is inconclusive and receives no score. Imported Postman/HAR/OpenAPI never
executes scripts, external references, or arbitrary destinations. In an authorized active Hunt,
select an HTTP(S) service on the same canonical host at any valid port using `origin`; the target
ID and frozen addresses never change. The operator-selected collection or credential workflow
may name that same-host service directly. Selected credentials work over HTTP and untrusted
HTTPS; certificate defects are evidence, not an extra authorization prompt. Session refresh
uses the saved login service, not the inventory record's default port. Do not bypass managed
credentials or redirect credentials to another asset; a credential reaches another target only
through an operator's grant.

`ssh.connect` is authentication-only. With an explicit stored `ssh.exec` grant, use direct commands,
reuse the returned session ID, and `ssh.close` when done; no inventory scan or repeated confirmation.
Host pins, grants and budgets still apply. See `docs/hunt-ssh.md` for streaming and cancellation.
Legacy exact-command SSH plans remain available; they are not required for already-delegated commands.
Device Hunt uses the shared runtime; do not revive retired device-agent writes. Startup supplies one
dedicated network worker, separate from DAST slots. Opt out with `SHAKERSCAN_NETWORK_WORKER_ENABLED=false`
or `shakerscan devices stop`; `shakerscan devices start` re-enables it. Use `./scanner.sh` only in source instructions.

### Continuous ASM

Prefer recommendations from `/targets/{id}/asm/gaps` or `/asm/improve`; do not invent campaign
logic or duplicate pending/running work. Auth checks need primary credentials. BOLA needs deep
intent and two identities. Stale, partial, auth-blocked, rate-limited, and error attempts are not
current completed coverage. Distinguish routes, variants, attempts, fresh examination, historical
completion, and proof-bearing variants.

### AI Gate

AI Gate tests chat, RAG, agent-trace, and MCP surfaces. It is preview: deterministic real-stack
smoke exists, while planned policy/exception and deterministic-judge seams are not automatically
release-gated. Production targets require explicit confirmation. AI judgment enriches but cannot
replace proof.

### Model Intake

Model Intake owns model repositories/artifacts; never create web Targets for them or mix them into
DAST/ASM. Core API/workers must not import publisher code. Strict profiles fail closed without
authoritative acquisition, trust, required scanners, or runtime evidence.

The Firecracker runner is opt-in host infrastructure requiring possible root mutation and large
downloads. Agents must not install it or route installation through API/Docker. `UNSUPPORTED_HOST`
and `NOT_READY` differ and both fail closed.

Use `make e2e-model-intake` for the real path and `make e2e-model-intake-fixture` only when external
network is intentionally unavailable. Truncation is `known_unverified_truncated`, never verified or
a false hash mismatch.

## Compatibility boundaries

- Removed `/interactive`, `/exceptions`, and `/settings/ai-ops-router` UI pages retain APIs only
  because Command Arsenal consumes them; do not present them as primary products.
- Historical `/agent/hunt/*`, `/device-agent/*`, `/research/*`, and `/deep-hunt/*` may be readable
  or redirect. New investigations use `/hunts`.
- Deprecated writes fail closed and never advertise arbitrary tool execution.
- Evidence cleanup stays interactive; legacy retention schedules remain disabled.
- Old scan labels are display history, not new-submission guidance.

## Fleet and deployment

Managed Fleet is Linux-only and opt-in. Check the non-secret `fleet` object from `/health` or
`/workers` before offering placement. Standalone/macOS must not display unavailable controls. The
supported production transport is outbound-only HTTPS broker; WireGuard is preview.

Remote lifecycle actions use explicit operator credentials retained only for the browser session.
Do not claim physical acceptance without the content-free multi-node fault/reclaim receipt.

## Development and verification

- Search with `rg`/`rg --files`; edit with `apply_patch`.
- Preserve user changes and avoid destructive Git commands.
- Generate public contracts from the app instead of hand-copying them.
- Add behavioral tests that fail without the fix; source-string assertions alone are insufficient.
- Diagnose a scan failure from the primary signal, not a summary. `GET /scans/{id}/actions` gives
  per-action status and error, `GET /scans/{id}/logs` and the worker container logs
  (`docker compose logs worker`) carry the actual failure, and `GET /scans/{id}/http-transactions`
  the traffic. A family-coverage rollup (`/result` coverage counts) is a CONSEQUENCE, never a cause:
  a family showing `action_incomplete` / 0 verified is most often a crashed action
  (`[scan] action <id> adapter raised <Error>` in the worker log), not a budget race. Read the
  action error and the worker log BEFORE theorising about budgets, allocation, or ordering, and
  before changing any scheduler or allocator code. Reasoning from the rollup alone has produced
  repeated wrong diagnoses and live recall regressions.
- One candidate must never fail a whole batch action. A per-candidate exception is recorded as a
  failed attempt and the batch continues; a batch that fails every candidate because one raised is
  a robustness bug, not a coverage outcome.
- Do not weaken a gate to make it pass. Fix code or deliberately update characterized contracts.

`scripts/check_module_size.py` is blocking in CI. Extract cohesive modules rather than raising
ratchets. Run API/capability inventory checks when routes, registries, skills, CLI, or types change.

### Rebuild semantics

UI, API, scanner, and workers share one release identity. Use `./scanner.sh rebuild`; do not bypass
launcher trust with raw compose. UI-only changes can retain cached heavy layers even when services
are recreated to publish one coherent identity.

After rebuild verify readiness, revision/fingerprint, current workers, specialized pools, restart
counts, migration/crash logs, and the affected workflow through API and UI.

```bash
make test
npm --prefix ui test
python3 scripts/check_module_size.py
python3 scripts/generate_capability_inventory.py --check
```

Use proportional release/E2E gates. Do not launch external acceptance scans without authorization.
Unit tests do not replace migration, live API, and UI verification when those surfaces changed.

## Minimal command reference

Set `API_BASE`/`UI_BASE` from `./scanner.sh status`. Bodies: `/scan/contracts`, `/hunts/contract`.

```bash
./scanner.sh start
./scanner.sh status
./scanner.sh logs -f
./scanner.sh rebuild
./scanner.sh restart
./scanner.sh scan https://example.com --budget-profile balanced

shakerscan api GET /openapi.json      # open-source engine only; an Enterprise gateway refuses it
shakerscan api GET /scan/contracts
shakerscan api GET /hunts/contract
shakerscan api GET /workers
shakerscan api GET "/scans?limit=10"
shakerscan api GET "/findings?status=active&limit=50"
```

The normal scan list hides shards, internal ASM rows, and Model Intake evidence scans. Include them
only for debugging/evidence selection via OpenAPI flags. Use `/scans/{id}` and `/result` for current
results, bounded logs for raw activity, and canonical cancel routes only for pending/running work.

That is the intentional limit of this quick reference. Discover all other operations from the live
contract or generated catalogue instead of expanding this always-loaded file.
