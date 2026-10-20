# Save Finding

Save an evidence-backed finding from authorized manual or interactive testing.

**Usage**: `/save-finding [session_id]`

Call the API with `shakerscan api METHOD PATH [JSON]` (it knows the instance address and credential; `SHAKERSCAN_API_BASE` overrides the address) and
`UI_BASE=${SHAKERSCAN_UI_BASE:-http://localhost:3000}` for UI links. On a remote VPS, use the URLs
printed by `./scanner.sh status`; the supported agent launcher exports them automatically.

## Evidence gate

Before saving, establish:

- authorized target and exact affected endpoint
- title, severity, category, and applicable CWE
- reproducible request and response or workflow evidence
- control result that distinguishes vulnerable behavior from normal behavior
- concrete security impact
- remediation guidance

Do not save a vulnerability from a status code, reflection, route existence, version string, or
model judgment alone. If evidence is incomplete, keep it as a lead or hypothesis.

## Save from a session

The target is derived from the active session:

```bash
shakerscan api POST /session/{session_id}/findings '{
    "title": "BOLA on order detail API",
    "severity": "high",
    "description": "A distinct second principal can read the first principal order.",
    "category": "BOLA",
    "cwe": "CWE-639",
    "url": "/api/orders/42",
    "evidence": "Owner control and attacker replay evidence...",
    "request": "GET /api/orders/42 ...",
    "response": "Redacted sensitive response...",
    "remediation": "Enforce object ownership on every order lookup."
  }'
```

## Save a standalone manual finding

```bash
shakerscan api POST /findings/manual '{
    "target": "https://app.example.test",
    "title": "Evidence-backed finding title",
    "severity": "medium",
    "description": "What is vulnerable and why it matters.",
    "category": "Access Control",
    "cwe": "CWE-284",
    "url": "/affected/path",
    "evidence": "Reproduction and control evidence...",
    "request": "Redacted request...",
    "response": "Redacted response...",
    "remediation": "Specific corrective action."
  }'
```

Report the finding ID, whether it was created, matched, or resurfaced, and
`${UI_BASE}/findings/{id}`.

Use `source_type=ai_session` to list interactive-session findings and `source_type=manual` for
standalone manual findings:

```bash
shakerscan api GET "/findings?source_type=ai_session&status=active"
shakerscan api GET "/findings?source_type=manual&status=active"
```
