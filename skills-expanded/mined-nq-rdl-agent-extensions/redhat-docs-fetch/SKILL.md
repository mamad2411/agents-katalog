---
name: redhat-docs-fetch
license: CC-BY-4.0
description: >-
  Fetch Red Hat product documentation and Customer Portal knowledge base (KCS)
  content, including subscriber-only solutions, with the user's own offline
  token. Use for a docs.redhat.com or access.redhat.com URL, a KCS id, or a Red
  Hat, OpenShift, or Ansible Automation Platform docs lookup. Never WebFetch
  these hosts; use curl/wget via rh-fetch (possible Akamai block or login page).
  Token setup: redhat:setup; entitlement is separate.
argument-hint: '<docs.redhat.com URL | access.redhat.com/solutions/<id> | kcs:<id> | search:<terms>>'
user-invocable: true
compatibility: >-
  Customer Portal search API (api.access.redhat.com/support/search/kcs) and
  Red Hat SSO offline-token exchange as of 2026-08; source-repo layouts of
  ansible/aap-docs (2.x branches) and openshift/openshift-docs (enterprise-4.x).
  Needs curl (or wget) and jq; gh optional (raises GitHub API rate limits).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Red Hat docs — fetch by the route that works

Red Hat's documentation is public, but **`docs.redhat.com` may return HTTP 403**
(Akamai edge handling varies). `rh-fetch.sh` tries a credential-free curl/wget GET
first, accepting only HTTP 200 HTML with a usable `<article>` and no block-page markers.
On failure it tries public source, then the KCS index. Do not evade a block.
Subscriber-only knowledge base content needs the person's **own entitled** Red Hat account.

| Target | Route | Credential |
|---|---|---|
| `docs.redhat.com/…/html/<book>/<page>#anchor` or `html-single` (also legacy `access.redhat.com/documentation/<locale>/…`) | Direct article text → GitHub AsciiDoc → indexed `docs-text:` | none for direct/source; offline token for index |
| `access.redhat.com/solutions/<id>`, `/articles/<id>`, `kcs:<id>` | Customer Portal **KCS search API** with `fq=id:` + Bearer token | offline token |
| `search:<terms>` | KCS search API (metadata is public) | none |
| `docs-text:<docs URL>` | *Experimental* — the KCS index's stored page text (keyed by page URL; `#anchor` ignored); fallback when direct/source routes fail | offline token |

## Do this

```bash
S="${CLAUDE_PLUGIN_ROOT}/skills/fetch-docs/scripts"     # canonical in-repo: skills/redhat-docs-fetch/scripts
bash "$S/rh-preflight.sh"                                # OS, fetcher, credential source (never the value)
bash "$S/rh-fetch.sh" 'https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/operating_ansible_automation_platform/assembly-configure-egress-proxy#proc-set-community-remote'
bash "$S/rh-fetch.sh" --includes '<docs URL>'            # inline first-level include:: modules on source fallback
bash "$S/rh-fetch.sh" kcs:7137578                        # Markdown: Environment/Issue/Resolution/Root Cause/…
bash "$S/rh-fetch.sh" --kind Solution --rows 5 'search:automation hub proxy 403'
bash "$S/rh-token.sh" --check                            # source=… access_token=ok expires_in=900s
```

Exit `3`: follow the message. Missing/rejected credentials need **`/redhat:setup`**;
a successful fresh exchange followed by `subscriber_only` means missing entitlement,
not a broken token. Review <https://access.redhat.com/management/subscriptions> and the
free Developer Subscription for Individuals at <https://developers.redhat.com/>.
Empty indexed text may instead mean the index has no body. Exit `4`: unresolvable;
offer `search:` or a browser. Keep the `// source:` provenance line in your answer.
Direct output is whole-article text (including for `html-single`); anchors are not
narrowed. Select the requested section yourself. Source fallback is AsciiDoc to render.

## Non-obvious facts the scripts encode (don't work around them)

- **URL → source file (fallback).** AAP: `ansible/aap-docs`, branch = version (`2.5`), files under
  `downstream/{assemblies,modules}/`; the page slug and every `#anchor` are **file names**
  (`proc-set-community-remote.adoc`) whose `[id=…]` equals the anchor. OpenShift:
  `openshift/openshift-docs`, branch `enterprise-<ver>`; the page slug is the assembly
  file name located via `_topic_maps/_topic_map.yml` (nested `Dir`/`File`), modules under
  `modules/`, and anchors are `<module-file>_{context}` — the script strips the suffix to
  find the module (so `html-single/…/index#anchor` URLs resolve too). Satellite builds from `theforeman/foreman-documentation`
  (`guides/doc-<Title>/`, `BUILD=satellite`). **RHEL has no public source.**
  Details: `references/source-repos.rst`.
- **No "get solution by id" endpoint exists.** The `resource_uri` the API returns
  (`/rs/solutions/<id>`) is the decommissioned Strata API (HTTP 410). The body comes from
  the search endpoint filtered by id. `references/customer-portal-api.rst`.
- **A bad Bearer token is silently ignored**: HTTP 200 with the literal string
  `"subscriber_only"` in the body fields. `rh-fetch.sh` exchanges a fresh token and
  retries once: if placeholders persist, the account is *not entitled* (exit 3).
  Exchange failures retain credential/network diagnostics; never call placeholders empty.
- **`access.redhat.com` HTML redirects to a `/ja/` locale from some networks** regardless
  of `Accept-Language`, cookies, or an explicit `/en/` path, and the page body is
  login-gated anyway. Use `view_uri` for provenance only; the API is the content route.
- **Credentials never transit the model.** `rh-token.sh` resolves the offline token from
  `RH_OFFLINE_TOKEN` → OS keychain → sops + age → 0600 file → Bitwarden (`bw`, item
  `redhat-credentials`), exchanges it at Red Hat SSO (`client_id=rhsm-api`,
  `grant_type=refresh_token`) for a 15-minute access token cached 0600, and hands curl a
  `-K` config. Never `echo` the token, never put it in argv, never ask the user to paste
  it into the chat. Offline tokens die after **30 days unused** → `invalid_grant` → the
  script says to regenerate; hand the user to `/redhat:setup`.
- **Platform**: `curl` first, `wget` fallback (absent on stock macOS and many servers);
  scripts run on bash 3.2. `references/platform-notes.rst`.

## Verify against the canonical source when being wrong would mislead

Version-specific procedures change between branches: fetch the branch that matches the
user's product version (the script derives it from the URL) and quote the `// source:`
line. For API behaviour, Red Hat's own page is
<https://access.redhat.com/articles/3626371> (Getting started with Red Hat APIs).

## Reference files

| File | Contents |
|---|---|
| [references/source-repos.rst](references/source-repos.rst) | Verified docs.redhat.com → GitHub map, URL→path recipes, closed products |
| [references/customer-portal-api.rst](references/customer-portal-api.rst) | KCS search endpoint, params, fields, auth flow, the 410/`subscriber_only`/locale gotchas |
| [references/platform-notes.rst](references/platform-notes.rst) | macOS vs Linux differences the scripts account for |

## Scripts

| File | What it does |
|---|---|
| [scripts/rh-preflight.sh](scripts/rh-preflight.sh) | OS / fetcher / jq / gh / bw / credential-source report (`--json`, `--require-cred`) |
| [scripts/rh-token.sh](scripts/rh-token.sh) | Offline token → cached access token; `--check`, `--curl-config`, `--clear` |
| [scripts/rh-fetch.sh](scripts/rh-fetch.sh) | Route + fetch: docs URL, solution/article/`kcs:` id, `search:`, `docs-text:` |
| [scripts/rh-lib.sh](scripts/rh-lib.sh) | Shared helpers (credential resolution, curl/wget abstraction) |

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when delegating
would help or the user asks to “create a subagent to execute this.” Otherwise,
work directly from this skill; the reference does not need to be loaded.
