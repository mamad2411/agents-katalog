# List Security Findings

Show security findings from scans.

**Usage**: `/findings [severity|dast|ai|ai_gate|ai_session|autonomous|model_intake|asm|manual]`

## Instructions

Call the API with `shakerscan api METHOD PATH [JSON]` (it knows the instance address and credential; `SHAKERSCAN_API_BASE` overrides the address). On a remote VPS, set it
to the API URL printed by `./scanner.sh status`.

1. Check if scanner is running:
   ```bash
   shakerscan api GET /health
   ```

2. Fetch findings based on arguments:

   If no argument (show all active):
   ```bash
   shakerscan api GET "/findings?status=active&limit=50"
   ```

   If a source type is specified:
   ```bash
   shakerscan api GET "/findings?source_type=$ARGUMENTS&status=active&limit=50"
   ```

   If severity specified (critical, high, medium, low):
   ```bash
   shakerscan api GET "/findings?severity=$ARGUMENTS&status=active&limit=50"
   ```

3. Format output as a table:
   ```
   | Type | Severity | Title | Target | Tool |
   |------|----------|-------|--------|------|
   | DAST | critical | SQL Injection in /api | example.com | sqlmap |
   | AI | high | Prompt injection compliance detected | support bot | shaker-ai-gate |
   ```

4. Include summary counts at the end

Keep reported/suspected and exploit-verified findings distinct. Include the latest verification
verdict when it affects the interpretation.
