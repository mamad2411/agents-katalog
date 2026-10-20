# AI Gate

Create/list AI Gate targets and queue AI safety scans.

**Usage**: `/ai-gate [list|scan|create] [args]`

## Instructions

Call the API with `shakerscan api METHOD PATH [JSON]` (it knows the instance address and credential; `SHAKERSCAN_API_BASE` overrides the address). Use `UI_BASE=${SHAKERSCAN_UI_BASE:-http://localhost:3000}` for UI links; on a remote VPS, set this to the URL printed by `./scanner.sh start --remote` or `./scanner.sh status`.

1. Check if scanner is running:
   ```bash
   shakerscan api GET /health
   ```

2. If the user asks to list targets:
   ```bash
   shakerscan api GET /ai/targets
   ```

3. If the user asks to create a target, gather or infer:
   - `name`
   - `target_type`: `api_chat`, `rag`, `agent_trace`, `mcp_trace`, or `widget`
   - `endpoint_url`
   - auth: none, bearer token, API key header, custom header, basic auth, cookie, multi-header, or query param
   - request template containing `{{prompt}}`
   - response path, usually `$.answer`

   Example:
   ```bash
   shakerscan api POST /ai/targets '{
       "name": "Support bot",
       "target_type": "api_chat",
       "endpoint_url": "https://example.com/api/chat",
       "method": "POST",
       "headers_template": {"Content-Type": "application/json"},
       "request_template": {"message": "{{prompt}}", "session_id": "{{session_id}}"},
       "response_path": "$.answer",
       "streaming_mode": "json",
       "credential": {"auth_kind": "none"}
     }'
   ```

4. If the user asks to scan an AI target:
   ```bash
   shakerscan api POST /ai/targets/{target_id}/scan '{"probe_pack":"shaker-ai-smoke","scan_profile":"smoke","environment":"staging"}'
   ```

   Probe packs: `shaker-ai-smoke`, `shaker-owasp-llm`, `shaker-agent-abuse`, `shaker-mcp-security`, `shaker-rag-lite`.

   **Production requires explicit confirmation.** For `"environment":"production"` you MUST also send
   `"confirm_production":true`, and only after the user has authorized testing that production target.
   The server enforces this (a production scan without it returns HTTP 409):
   ```bash
   shakerscan api POST /ai/targets/{target_id}/scan '{"probe_pack":"shaker-ai-smoke","scan_profile":"smoke","environment":"production","confirm_production":true}'
   ```

5. After submitting, report:
   - scan ID
   - UI link: `${UI_BASE}/scans/{scan_id}`
   - AI Gate page: `${UI_BASE}/ai-gate`

   Then stop. Do not poll unless explicitly asked.

6. To review results later:
   ```bash
   shakerscan api GET "/findings?source_type=ai_gate&status=active"
   shakerscan api GET /ai/scans/{scan_id}/transcript
   ```
