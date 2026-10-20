# Submit the deterministic Scan

Submit ShakerScan's single deterministic Web/API security workflow. Resource profiles are hard
ceilings; active testing is an explicit permission, not a scan type.

**Usage**: `/scan <target_url>`

## Instructions

Call the API with `shakerscan api METHOD PATH [JSON]` (it knows the instance address and credential; `SHAKERSCAN_API_BASE` overrides the address) and
`UI_BASE=${SHAKERSCAN_UI_BASE:-http://localhost:3000}` for UI links. On a remote host, use the URLs
printed by `./scanner.sh status`.

1. Check scanner and worker health:

   ```bash
   shakerscan api GET /health
   shakerscan api GET /workers
   ```

   If the scanner is not running, ask whether to start it with `./scanner.sh start`. Do not measure
   scan quality on a build-stale fleet.

2. Choose `fast`, `balanced`, or `thorough` ceilings. Passive `balanced` is the default:

   ```bash
   shakerscan api POST /scans '{
       "target": "$ARGUMENTS",
       "budget_profile": "balanced",
       "policy": {"active_testing": false}
     }'
   ```

3. Before enabling `active_testing`, confirm the user owns or is explicitly authorized to test the
   exact target. State-changing HTTP, network discovery, and encrypted credential profiles also
   require the matching target-bound approval receipt. Never put raw credentials in the request:

   ```bash
   shakerscan api POST /scans '{
       "target": "https://example.com",
       "budget_profile": "thorough",
       "policy": {
         "active_testing": true,
         "include_families": ["xss", "sqli"]
       },
       "approval_receipt_id": "TARGET_BOUND_APPROVAL_UUID"
     }'
   ```

   Read `GET /scan/contracts` for the server-advertised family vocabulary and advanced ceiling
   bounds. Known endpoints belong in `options.custom_endpoints`; saved traffic and authentication
   are referenced by opaque collection/profile IDs.

4. Report the returned scan ID and UI link, then stop:

   ```text
   Scan submitted: {scan_id}
   View progress: ${UI_BASE}/scans/{scan_id}
   ```

Do not poll or wait for completion. When the user asks later, read `/scans/{id}` and
`/scans/{id}/result`. Treat suspected candidates separately from deterministic verified findings,
and report coverage/budget gaps rather than implying that unattempted checks passed.
