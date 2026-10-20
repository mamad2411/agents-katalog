---
name: web-recon-surface
description: "Map the attack surface of in-scope web assets. Passive subdomain discovery, live-host probing, technology fingerprinting, and endpoint crawling, aggregated into a normalized surface.json of leads worth a deeper look."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# Web Recon — Attack Surface

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


OBSERVE phase. Turn a scope into a structured inventory of live web assets and their
technology stack, so triage has clean leads to work from. Passive first; active probing
only against confirmed in-scope hosts.

## When to Use

- Start of a web engagement, once `engagement-scope` is loaded.
- When asked to "map the attack surface", "find subdomains", or "fingerprint the stack".

## Quick Reference

| Tool        | Role                              | Typical invocation |
| ----------- | --------------------------------- | ------------------ |
| `subfinder` | Passive subdomain discovery       | `subfinder -d acme-staging.io -all -silent` |
| `dnsx`      | Resolve / filter live DNS         | `dnsx -silent -a -resp` |
| `httpx`     | Probe live HTTP, title, tech, CDN | `httpx -json -title -tech-detect -status-code -cdn` |
| `katana`    | Crawl endpoints                   | `katana -jc -d 3 -silent` |
| `nuclei`    | Technology fingerprint            | `nuclei -tags tech -silent` |
| `gowitness` | Screenshot live pages             | `screenshot_hosts` (f0-recon) |
| `tlsx`      | TLS metadata / SAN harvesting     | `tlsx -san -silent` |

Confirm scope on every host with the `engagement-scope` skill's `scope_check.py` before probing.

## Procedure

1. **Scope first.** Ensure `engagement-scope` is loaded. For each root domain/host, run `scope_check` (`--action passive_recon`); drop anything that is not `0`.
2. **Passive discovery.** `subfinder` per in-scope root domain into a host list. Keep it passive — no brute force unless `active_scan` is allowed and the operator asks.
3. **Resolve & re-gate.** Resolve with `dnsx`. Re-run `scope_check` on every resolved host (a discovered subdomain may be out of scope or CDN-owned).
4. **Probe live hosts.** Run `httpx -json` over the in-scope, resolved hosts to capture status, title, web server, technologies, and CDN. Use a polite rate (`-rl`); avoid hammering.
5. **Fingerprint & crawl.** Add `nuclei -tags tech` for stack detail and `katana` for reachable endpoints on the most interesting hosts.
6. **Screenshot the interesting ones.** Run `screenshot_hosts` over the in-scope hosts whose titles or tech suggest a login portal, admin panel, or default install — one rendered page settles what a status code and title cannot. This **fetches and renders the page**, so it is active traffic like every other step here: in-scope hosts only, after step 3's re-gate, and keep the list short rather than screenshotting the whole inventory. PNGs land in the engagement's `03-evidence/gowitness/`.
7. **Aggregate.** Normalize everything into one inventory:
   ```bash
   python3 <skill-dir>/scripts/merge_surface.py \
       --httpx httpx.jsonl --hosts subfinder.txt -o surface.json
   ```
8. **Summarize leads.** Report which assets look worth a deeper look (auth surfaces, admin panels, APIs, old stacks) and hand `surface.json` to `web-vuln-triage`. Reference the screenshots for anything you call a login or admin surface. Write `surface.json` to the engagement evidence dir.

## Pitfalls

- **Out-of-scope subdomains** surface constantly from passive sources — re-gate after discovery, never assume inheritance.
- **Wildcard DNS** inflates the host list with non-existent names; `dnsx` resolution filtering helps.
- **CDN / WAF fronting** means the IP and observed stack may be the edge, not origin. Note CDN in the inventory; don't mistake the edge for the target.
- **Rate limits / blocking.** Aggressive probing trips WAFs and pollutes results. Throttle and prefer passive sources.

## Verification

- `surface.json` exists, parses, and every asset host passes `scope_check`.
- Live hosts carry status codes and at least partial tech fingerprints.
- A short, prioritized lead list is produced for triage.
