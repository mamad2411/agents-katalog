# artemis — headless browser engine for agents

`artemis` is a single Go binary that fetches and renders web pages for agents.
Two kernels: a **renderless V8 path** (no Chrome needed, fast, low memory,
Chrome-coherent identity) and a **Chromium/CDP path** (real browser when a
page needs it). This file is the complete operating contract — do not guess
flags; everything below is verified.

## Decide which command (do not overthink)

| You need | Command |
|---|---|
| Page text/content to read | `artemis fetch <url>` |
| Just the links or structured data | `artemis fetch --dump links|structured|semantic <url>` |
| Run JS on the page / extract a value | `artemis fetch --eval '<expr>' <url>` |
| Click, type, navigate in a real browser | `artemis act --request '<json>' <url>` |
| See what's on a real browser page | `artemis observe <url>` |
| Bounded context or changes on a retained page | `artemis query --session SESSION_ID --page PAGE_ID --max-bytes 8192` |
| Persistent session / many steps | `artemis serve`, then `control` and `observe`/`act`/`fetch --server` |
| What this build can do | `artemis capabilities` |
| Is the environment healthy | `artemis doctor` |

**Default is `fetch`.** Only reach for `act`/`observe` (real Chromium) when
fetch's output proves the page needs real rendering (missing content, empty
semantic tree, JS-required). Measure latency and memory on the actual workload;
the two kernels have different resource costs.

## Action policy

Managed commands default to navigation/observation/extraction plus owned cleanup.
Inputs, caller JavaScript and assertions need explicit category permission.
Use an owner-approved `--action-policy policy.json` on one-shot `fetch`, `run`,
`observe` or `act`, or on `serve` for persistent clients. For example,
`{"default":"deny","allow":["navigate","observe","query","extract","click"],"domain_allowlist":["example.com"]}`
permits those categories on the named host and its subdomains. Do not expand a
policy merely to bypass a denial. `evaluate` is required for `--eval`,
`run --script` and caller JavaScript; `page.assert` needs `assert`, and `eval_truthy`
also needs `evaluate`. Low-level Go/raw CDP callers own their separate authority.

Environment compatibility: `AGENT_BROWSER_ACTION_POLICY`, fallback
`AGENT_BROWSER_POLICY`, and comma-separated `AGENT_BROWSER_CONFIRM_ACTIONS`.
`--confirm-actions` adds categories requiring confirmation. Denial wins over
confirmation, then allow/default. Confirmation dispatches nothing; seek the
owner's authorization before retrying. Configured invalid/missing files fail
startup. Atomic file replacements reload every five seconds; invalid changes
retain the last valid policy. Managed Chromium receipts include
`evidence.policyDecision`; verify it with effects and attempts. Navigation may
execute site scripts and is not a zero-effects operation.

## fetch — content extraction

```
artemis fetch [flags] <url>
```

stdout = the dump. stderr = diagnostics. Exit 0 ok, 1 runtime error, 2 bad args.

| Flag | Meaning |
|---|---|
| `--dump` | `markdown` (default, LLM-ready) · `text` · `html` · `title` · `links` (TSV: `href\ttext`) · `structured` (JSON: JSON-LD/microdata) · `semantic` (semantic tree, text) |
| `--eval <expr>` | evaluate a JS expression post-load; result replaces the dump on stdout |
| `--run-scripts` | execute inline `<script>` tags |
| `--header k=v` | extra request header; repeatable |
| `--user-agent <ua>` | override UA (default is a host-matched Chrome identity — leave it) |
| `--proxy <url>` | route through a proxy |
| `--timeout 30s` | request timeout |
| `--max-body-bytes N` | cap response size |
| `--allow-private-networks`, `--allow-port N` | opt out of SSRF guards |

Token-efficient usage: prefer `--dump markdown` for reading, `--dump links`
before navigating (TSV in one-shot mode), `--eval` to pull a specific value instead of
dumping whole pages.

## observe + act — real Chromium

```
artemis observe [flags] <url>          # bounded DOM/AX snapshot as JSON
artemis act --request '<json>' <url>   # one typed action, evidence JSON out
```

`--request` schema: `{"kind": "<kind>", "ref"|"url"|"text"|"key"|"expression"|...}`.
Kinds: `navigate reload back forward wait focus click hover scroll key type
clear fill fill_form select check uncheck drag tab_open tab_close tab_list
tab_switch evaluate assert viewport frame_evaluate`.

URL-based `observe` and `act` are independent one-shot browsers. Their refs
cannot be shared between processes. For a retained page, start `artemis serve`,
set `ARTEMIS_SERVER` and `ARTEMIS_SERVE_TOKEN`, run `control --cmd session.new`,
and retain its server-issued `clientId` as `ARTEMIS_CLIENT_ID`. Open the page
using `control --cmd chromium.open --params '{"sessionId":"SESSION_ID","url":"https://site.test"}'`.
Use the actual returned session/page IDs in this flow:

```sh
artemis observe --session SESSION_ID --page PAGE_ID
artemis act --session SESSION_ID --page PAGE_ID --snapshot-epoch EPOCH --request '{"kind":"click","ref":"REF"}'
artemis fetch --session SESSION_ID --page PAGE_ID --dump markdown
```

Replace `EPOCH` and `REF` with `snapshot.epoch` and an emitted node ref. Old
document epochs and refs bound to another explicit page are denied. Check
`success` and `evidence.postcondition.passed`, then verify the desired business
outcome; a dispatched click alone does not establish it. Persistent control
rejects local process flags; configure them on `serve`. One-shot integer byte
budgets use e.g. `--max-memory-bytes 2147483648`, not `2G`.

## query — bounded retained-page context

Use the same server/client/session/page identities as the persistent flow.
`query` defaults to interactive nodes; `--roles button,textbox`, `--text TEXT`,
`--frame FRAME_ID` or `--mode subtree --subtree REF` narrow relevance before
emission limits. `--target REF` prioritizes that observed target and adds typed
blocker evidence with at most three candidate references/remedies. It does not
execute repairs. Defaults: `--max-nodes 200`, `--max-bytes 32768`, `--timeout 20s`.
Budgets bound compact JSON bytes, not model-specific tokens. No positional URL
or `--snapshot-epoch` is accepted.

Repeat identical options with `--since REVISION` from the previous response.
`full` replaces the projection; `unchanged` retains its revision; `delta`
applies material added/changed/removed nodes only to its exact `baseRevision`.
Check `lost`, `truncated`, warnings and `resetReason`; never treat missing
evidence as a removed target. Only the latest complete matching baseline can
produce incremental output. Navigation, changed options, unavailable baseline
or oversized delta resets to full. Insufficient metadata/target bytes fail
explicitly. Use query's `epoch` and page-bound refs for subsequent `act`.

## serve — persistent sessions

`artemis serve` exposes JSON-over-WebSocket steering — use it for many
steps on one page or session reuse; one-shot work stays on the CLI.

Frames: `{"id": "<id>", "cmd": "<cmd>", "params": {...}}` →
`{"id": ..., "version":"2.0.0", "seq":N, "ok": bool, "value"|"error": ...}`. Commands:
`session.new`, `session.close`, `session.list`, `page.open`, `page.close`,
`page.eval`, `page.dump`, `page.click_by_text`, `page.type`,
`page.wait_idle`, `page.assert`, `chromium.open`, `chromium.observe`,
`chromium.query`, `chromium.act`, `chromium.close`, `stream`, `cancel`,
`token.rotate`, `heartbeat`, `capabilities`, `version`. Chromium actions require
`{sessionId,pageId,snapshotEpoch?,request}`. Tab operations use owned page
open/close commands. A failed action retains its outcome evidence. Never blindly
replay an effect after losing a response. Restarting the server invalidates
client capabilities and page IDs; reconnecting to the same live server retains
them.

## Stealth (only when asked)

`ARTEMIS_STEALTH=stealth|paranoid` + `ARTEMIS_STEALTH_PURPOSE=<why>` +
`ARTEMIS_STEALTH_LEGAL_BASIS=<basis>` enables measured-profile
anti-detection. It is fail-closed: no acknowledgement → hard error, never a
silent downgrade. Default renderless fetch is already Chrome-coherent (UA,
Sec-CH-UA headers, JA3 via uTLS) — stealth is for hardened targets.

## Errors and exits

0 = success · 1 = runtime failure · 2 = bad invocation. Policy denials
(private IP, robots, download limits) are typed errors on stderr, not silent
emptiness. `artemis doctor` diagnoses environment problems (missing Chrome,
CGO, permissions).
