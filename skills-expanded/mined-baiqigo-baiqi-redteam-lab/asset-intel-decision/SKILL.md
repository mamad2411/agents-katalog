---
name: asset-intel-decision
description: Turn external asset and OSINT collection into ownership-aware, scope-safe decisions and a deterministic next-action queue. Use after subdomain/ASN/port/web/URL collection and before active testing; complements recon-scope-triage by providing a repeatable JSON decision layer and Kali CLI/MCP routing instead of another scanner.
metadata:
  sources: project-local-and-public-recon-tools
  focus: asset-ownership-triage, attack-surface-prioritization, next-actions
---

# Asset intelligence → decision workflow

Use this skill when the input is an asset list, ASM export, subdomain/ASN result,
Internet-wide search result, port inventory, HTTP probe, screenshot inventory, or
URL/parameter collection. It is **not** a replacement for Hunter scope gates or
for vulnerability-specific hunting skills.

## Non-duplication boundary

- Hunter remains the authority for authorization, case/scope, evidence, and web/API orchestration.
- Existing `recon-scope-triage` remains the human ownership/collision playbook.
- Kali remains the CLI execution layer.
- This skill adds the missing deterministic layer: normalize → deduplicate → classify ownership → rank → emit `next_actions`.
- Do not actively probe an asset merely because a search engine, keyword, or scanner returned it.

## Required order

1. Establish the canonical owned apex/domain set and engagement case.
2. Call Hunter scope controls before any active action:
   - `hunter_engagement_open` or `hunter_scope_set`
   - `hunter_scope_check` for each candidate
   - `hunter_target_context_register` only from real HTTP/DNS evidence
3. Collect broad, mostly passive evidence with the least-overlapping tool:
   - `bbot_scan` for recursive event-driven external attack-surface discovery;
   - `asnmap_enum` for organization/domain → ASN/CIDR enrichment;
   - `uncover_search` only when the operator has configured search-engine credentials;
   - existing `subfinder_enum`, `amass_enum`, `gau_urls`, `katana_crawl`, `dnsx_resolve` for their established roles.
4. Enrich confirmed candidates, bounded and rate-limited:
   - `naabu_scan` → ports;
   - `httpx_probe` / `whatweb_fingerprint` → liveness and technology;
   - `gowitness_screenshot` → visual verification of many web assets;
   - `arjun_params` → parameters only after an owned live URL is confirmed.
5. Combine outputs as JSON or JSONL and call the offline decision layer:
   - CLI: `python tools/skills/mcp/KaliDockerMCP/asset_decision.py --input assets.jsonl --owned-domain example.com --output decision.json --pretty`
   - MCP: `kali_asset_decide(assets_json, owned_domains=[...], mode="balanced")`
6. Read `summary`, `ranked_assets`, and `next_actions`. Re-check scope immediately before executing a suggested action.

## Ownership classes and hard stops

The decision layer emits one of:

- `confirmed`: exact owned apex/subdomain or explicit verified proof;
- `unverified`: no ownership proof yet; passive fingerprinting only;
- `third_party`: provider/dependency marker; no active testing without scope confirmation;
- `brand_collision`: keyword/name collision, typo, unrelated repository/bucket/app;
- `soft_404`: catch-all response or explicit soft-404 evidence; verify with a random control;
- `stale`: decommissioned/expired marker; revalidate before testing;
- `out_of_scope`: explicit scope exclusion.

`brand_collision`, `third_party`, and `out_of_scope` are not active-test queues.
A `soft_404` requires a body/length/control comparison before treating a path as
an exposure. An `unverified` live asset gets an ownership action, not an exploit
action.

## Deterministic prioritization

The planner scores ownership first, then liveness/status, exposed ports,
technology signals, and independent sources. `balanced` is the default; use
`conservative` when the input is noisy or the brand is a common word, and
`aggressive` only when the operator has explicit broad authorization. The score
is a triage aid, not a severity claim.

Typical action meanings:

- `verify_ownership` / `revalidate_stale_asset`: use scope, DNS, WHOIS, certificate, and program evidence;
- `enrich_ports`: `naabu_scan` followed by targeted `nmap_scan` where authorized;
- `fingerprint_http`: `httpx_probe` then `whatweb_fingerprint`;
- `crawl_and_build_url_surface`: `katana_crawl`, `gau_urls`, and Hunter surface discovery;
- `discover_parameters_and_api_surface`: `arjun_params` only after ownership/liveness, then API-specific Hunter skills;
- `verify_soft_404_with_control`: compare the candidate response with a random nonexistent path on the same host;
- `quarantine_collision`: record the reason and do not send active requests.

## Output contract

Keep the decision JSON as a reviewable artifact under `exports/` or the case's
evidence directory. It must retain the input sources and ownership reason. Do not
store cookies, bearer tokens, private customer data, or raw third-party exports in
the public repository. Feed confirmed assets back to Hunter case state and use
`hunter_recommend_next`/`hunter_workspace_recommend` for evidence-aware follow-up.
