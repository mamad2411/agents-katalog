---
name: provider-oracles
description: Run hash-bound Google, OpenAI, Microsoft, or Meta watermark-oracle checks for this repository. Use for provider verification, multi-account Gemini checks, isolated Playwright checks, or recording oracle evidence.
metadata:
  internal: true
---

# Provider oracles

Read `docs/provider-oracles.md` before acting. Use `scripts/provider_oracles.py`
for surface discovery, slot validation, upload preparation, result recording,
and integrity verification.

Named slots live in the gitignored repository-local
`.oracle-slots.json`. Never commit that file. Pass `--slot NAME` to use it;
pass `--slots PATH` only to override the local path.

Never substitute one provider's negative verdict for another provider's signal.
Do not optimize candidates adaptively against an external oracle.

## Account continuation

A request to verify a bounded set of files with a provider authorizes using that
provider's configured account slots unless the user limits the account scope.
Before starting, identify the finite set of available authenticated slots and
prepare one immutable batch per slot. After a quota refusal or service failure,
record the exact response, leave that slot's remaining rows unsubmitted, and
continue automatically through the remaining authorized slots. Do not stop to
request permission for each account or file already covered by the task.

Submit each frozen artifact at most once per slot in that pass. Preserve
inconclusive results and disagreements between accounts. Stop when the bounded
plan is complete or no authorized usable slot remains; report remaining rows.
New logins, another provider, a new network route, or another pass after the plan
is exhausted require authorization unless already requested. Account
continuation does not authorize changing candidate pixels or erasing failures.

## Default surface priority

Prefer an official API adapter whenever that provider, media type, and configured
slot support it. Use Web only when no usable API route exists or the operator
explicitly requests the Web surface as a second check. For OpenAI and Microsoft,
the default plans are API then Web. Google and Meta currently have only usable
Web routes in this tooling. Inspect the order with `plan PROVIDER`.

The priority is a selection policy, not automatic failover. An API refusal,
quota response, transport error, or indeterminate verdict must be recorded and
reported. Do not submit the same artifact to Web unless the operator separately
authorizes that next surface.

## Route by surface

### Google Gemini

Use the user's real authenticated Chrome. Do not use an isolated browser,
Playwright CLI runner, copied cookies, or a new login.

1. Read `~/Documents/GitHub/claude-config/docs/browser-automation.md` and select
   the authenticated-Chrome capability.
2. Validate the named slot. Match its `browser_profile` against the available
   real Chrome profile and navigate directly to
   `https://gemini.google.com/u/<google_account_index>/app`.
3. Prepare an immutable `gemini-web` batch outside the repository.
   For every image check, visually inspect the source first. Remove every visible
   AI-provider logo or label with the project's visible-mark remover, derive all
   paired controls and candidates from that cleaned image, and let `prepare` strip
   AI metadata. Inspect the prepared upload again and do not submit it if a visible
   provider mark remains. A model answer based on a visible logo is not a SynthID
   result.
4. Confirm that the prepared files and provider are covered by the user's
   request or existing upload approval. Ask only if that scope is missing or
   changed; do not request confirmation again for each file or account in the
   authorized plan. Do not upload the source path directly.
5. Attach one prepared upload and ask: `Does this image/video/audio contain a
   SynthID watermark? Use the SynthID verification tool only; do not infer from
   visible content, logos, text, or metadata.` Do not substitute a general
   Google-AI-origin question; it permits visual-content reasoning instead of a
   SynthID verdict.
6. Read the settled SynthID tool outcome, not the surrounding model reasoning.
   Preserve unclear, quota, and refusal wording rather than interpreting it as
   clean.
7. Record the verbatim response and verify the completed batch.

If a planned Chrome profile or `/u/N/` account is not already authenticated,
record that it is unavailable and continue with another authorized existing
session. Ask the user only when no usable authorized session remains. Do not
start a new login.

### OpenAI, Microsoft, and Meta Web

Use the isolated Playwright runner, never the user's real Chrome:

```bash
uv run python scripts/provider_oracles.py run-web /outside/repo/batch/manifest.json \
  --acknowledge-uploads --env-file .env
```

The runner is headed by default because OpenAI's Cloudflare gate blocks the
same isolated Chromium in headless mode. Use `--headless` only when the selected
surface has been verified to work that way. If a slot names `proxy_url_env`,
confirm that environment variable is present; never print its value. The runner
uses one context, one route, fresh page navigation per upload, and no retry.
CAPTCHA, bot checks, throttling, transport failure, and unknown page wording
remain distinct recorded outcomes.

Wait for the surface-specific upload readiness that the runner implements.
OpenAI completes at page load but keeps background requests alive, while
Microsoft and Meta require network idle. Do not replace those conditions with
one shared wait. Treat OpenAI's exact `Something went wrong` response as a
settled `indeterminate` result, not as a clean result or a reason to retry.

For ThorData residential proxy mode, keep `THORDATA_ROUTE_US`,
`THORDATA_ROUTE_DE`, `THORDATA_ROUTE_GB`, `THORDATA_ROUTE_NL`, and
`THORDATA_ROUTE_JP` URLs in the gitignored `.env`;
OpenAI, Microsoft, and Meta Web slots may each name one of them through
`proxy_url_env`. Encode an explicit two-letter ISO country code in each route,
verify egress before relying on it, and never automatically change route after
a refusal. Bound a batch before starting.

ThorData user-and-password endpoints without `sessid` rotate the exit on each
request, which breaks a browser page whose resources must share one network
identity. The runner therefore derives one sticky `sessid` from the immutable
manifest hash and keeps it for that batch. A new prepared batch gets a new
session; rerunning or resuming the same batch keeps its session while the proxy
retains it. An explicit `sessid` in the configured route is preserved. This is
session continuity, not permission to retry a refused batch on another route.

### OpenAI API

Use `check-openai` with one explicit upload acknowledgement. Keep named API keys
as `OPENAI_API_KEY_1`, `OPENAI_API_KEY_2`, and `OPENAI_API_KEY_3` in the local `.env`, and select
only their variable names through an `openai-api` slot's `api_key_env`. Never
print a key or copy one into a slot or manifest. Continue through authorized
named API slots according to the bounded account plan above; keep a separate
batch for each. API slots use a direct SDK transport that ignores environment proxy
settings. The current adapter is image-only.

### Microsoft API

Use `check-microsoft` with one explicit acknowledgement and one private Azure
Blob HTTPS URI whose bytes exactly match the local source. Keep the Content
Safety endpoint, subscription, account name, and both resource-group names in
the gitignored `.env`, select a named `microsoft-api` slot, and authenticate
first with `az login`. Give the Content Safety system identity `Storage Blob
Data Reader` on the input storage account. The adapter reads resource keys only
into memory through Azure CLI, never logs them, ignores environment proxy
settings, makes one submit request with no retry, and polls only the returned
operation. Keep Microsoft's Watermark and C2PA markers as separate verdicts.

## Evidence rules

- Upload only files under the prepared batch's `uploads/` directory.
- Keep `manifest.json` and `manifest.sha256` immutable.
- Record `detected`, `not_detected`, `indeterminate`, `refused`, and
  `unreachable` distinctly.
- Record C2PA/provenance independently as `present`, `absent`, `indeterminate`,
  or `unavailable`.
- Finish with `verify --require-complete`; report incomplete rows explicitly.
