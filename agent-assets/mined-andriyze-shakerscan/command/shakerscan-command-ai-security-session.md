# Interactive Testing

Drive an authorized Interactive Testing browser workflow with the compatibility-named `ai-security-session` skill.

**Usage**: `/ai-security-session <target_url>`

## Instructions

Call the API with `shakerscan api METHOD PATH [JSON]` (it knows the instance address and credential; `SHAKERSCAN_API_BASE` overrides the address). Use
`UI_BASE=${SHAKERSCAN_UI_BASE:-http://localhost:3000}` for UI links; on a remote VPS, use the URL
printed by `./scanner.sh status`.

1. Read and follow `skills/ai-security-session/SKILL.md`.
2. Confirm the target is in the user's authorized scope.
3. Check health:

   ```bash
   shakerscan api GET /health
   ```

4. Bootstrap from the latest completed scan when one exists:

   ```bash
   shakerscan api GET "/scans?target=TARGET&status=completed&limit=5"
   shakerscan api GET /scans/{scan_id}/result
   shakerscan api GET "/findings?target_id={target_id}&status=active"
   ```

   If new scan context would help, ask before submitting it. `full`, `aggressive`, and `smart`
   require explicit active-testing authorization. After submitting a scan, report its ID and UI
   link and stop; do not continue the session in the same turn.

5. Start the browser session:

   ```bash
   shakerscan api POST /session/start '{"target":"TARGET_URL"}'
   ```

6. Use `POST /session/{id}/action` for same-origin navigation, clicks, fills, submits, waits,
   extraction, login, registration, or managed credential profiles.
7. Use distinct `user1` and `user2` contexts for access-control testing. Prefer managed credential
   profiles so ShakerScan can prove principal identity and distinctness.
8. Use `POST /session/{id}/test-endpoint` for a bounded replay. A 200 response or response difference
   is only a lead; verify ownership, principal distinctness, sensitive data or state impact, and a
   control request before saving a BOLA/IDOR finding.
9. Save only validated findings with `POST /session/{id}/findings`. Include the exact endpoint,
   principal roles, request/response evidence, control result, impact, and remediation.
10. End the session with:

    ```bash
    shakerscan api DELETE /session/{session_id}
    ```

Maintain the checklist from the skill. If no issue is validated, say so and report coverage,
evidence-backed leads, and blockers without fabricating a finding.
