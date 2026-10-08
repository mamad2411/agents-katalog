---
name: mks
description: MKS (Metasploit-Kali Server) tool preference guide. Mount in Phase 0/1 alongside the primary skill. Provides URL resolution, REST endpoint patterns, response parsing, error handling, and fallback rules for all MKS-backed Kali tools.
---

# MKS — Kali Tool Server Preference

## Step 0: Resolve MKS URL

Run once at phase start and store as `MKS_URL`:

```bash
MKS_URL=$(cat .pentest-mks.json 2>/dev/null | jq -r '.url // empty')
```

- **Non-empty**: MKS is active — use the REST endpoints below instead of local Bash tool invocations.
- **Empty**: MKS not configured — skip all MKS calls and use local Bash commands as documented in the agent workflow.

## Step 0.5: Capability probe (do this once before the first tool call)

Some server builds have a defect where the structured `/api/tools/*` endpoints (and `/health`) crash
when the command is constructed as an argv **list** — every structured tool call returns an error like
`CommandExecutor expects a string, but got list`, and the tools appear unusable even though they are
installed. The generic `POST /api/command` endpoint (raw command string) is unaffected.

Probe once and set `MKS_TOOLS_MODE`:

```bash
PROBE=$(curl -s -m 20 -X POST "$MKS_URL/api/tools/nmap" \
  -H "Content-Type: application/json" \
  -d "{\"target\":\"127.0.0.1\",\"scan_type\":\"-sn\",\"additional_args\":\"-Pn\"}")
if echo "$PROBE" | grep -qiE 'got list|expects a string|TypeError|Internal Server Error|got a list'; then
  MKS_TOOLS_MODE="command"   # structured endpoints are broken on this server → route via /api/command
else
  MKS_TOOLS_MODE="structured" # structured endpoints work → use /api/tools/* as documented
fi
```

- `MKS_TOOLS_MODE="structured"` → use the `/api/tools/{tool}` endpoints in the Endpoints section.
- `MKS_TOOLS_MODE="command"` → use the **/api/command fallback** (see that section) for every tool.

Log the result: `{"action":"mks-capability-probe","tools_mode":"<structured|command>"}`.

> **Security note for `command` mode:** `/api/command` runs the string in a shell (`shell=True`-style),
> so it is injection-prone if any target/argument is attacker-controlled. In a pentest the target and
> args are operator-controlled against the operator's own Kali host, so this is an acceptable bridge —
> but never interpolate untrusted scan *output* back into an `/api/command` string. The structured
> endpoints are the safer design; prefer them whenever the probe says they work.

## Response Contract

Every MKS tool endpoint returns JSON:

```json
{ "output": "<raw tool stdout>", "error": "<stderr or empty string>" }
```

**Parsing pattern** (apply after every MKS curl call):

```bash
RESPONSE=$(curl -s -m TIMEOUT -X POST "$MKS_URL/api/tools/TOOL" \
  -H "Content-Type: application/json" \
  -d 'PAYLOAD')
RESULT=$(echo "$RESPONSE" | jq -r '.output // empty')
ERR=$(echo "$RESPONSE" | jq -r '.error // empty')
```

Replace `TIMEOUT`, `TOOL`, and `PAYLOAD` with values from the endpoint sections below.

## Error Handling — layered fallback

If a structured `/api/tools/{tool}` call fails — `RESULT` empty, OR the response contains
`got list` / `expects a string` / `TypeError` / `Internal Server Error` (the list-vs-string defect):

1. **First fall back to `/api/command`** (the raw-string endpoint — see the next section), not straight
   to local Bash. This recovers the tool when only the structured endpoint is broken. Log:
   ```json
   {"timestamp":"...","agent":"<agent-name>","action":"mks-fallback","tool":"<tool-name>","from":"structured","to":"command","reason":"<empty-response|type-error>"}
   ```
2. **Only if `/api/command` also fails** (or `MKS_URL` is empty), fall back to the local Bash
   equivalent documented in the agent workflow. Log `"to":"local-bash"`.
3. Continue the engagement — a failed MKS call is non-fatal.

If Step 0.5 already set `MKS_TOOLS_MODE="command"`, skip the structured call entirely and go straight
to `/api/command` for every tool.

## /api/command fallback (raw-string endpoint)

The generic endpoint takes a full command string and is unaffected by the list-vs-string defect.

**Request / response shape** (different from `/api/tools/*`):
```bash
RESPONSE=$(curl -s -m TIMEOUT -X POST "$MKS_URL/api/command" \
  -H "Content-Type: application/json" \
  -d "{\"command\":\"<full command string>\"}")
RESULT=$(echo "$RESPONSE" | jq -r '.stdout // empty')
RC=$(echo "$RESPONSE" | jq -r '.return_code // empty')   # 0 = success; .success is also returned
```

**Equivalent command string per tool** (build the same invocation the structured endpoint would run):

| Tool | `/api/command` string |
|------|-----------------------|
| nmap | `nmap <scan_type> <ports?> <additional_args> <target>` (e.g. `nmap -sS -p- --min-rate 10000 -T4 -Pn $TARGET`) |
| gobuster | `gobuster dir -u $TARGET -w /usr/share/wordlists/dirb/common.txt -b 404` |
| dirb | `dirb $TARGET /usr/share/wordlists/dirb/common.txt` |
| nikto | `nikto -h $TARGET` |
| sqlmap | `sqlmap -u "$TARGET_URL" --batch --level=3 --risk=2` (add `--data="$POST_DATA"` for POST) |
| hydra | `hydra -L <user_file> -P /usr/share/wordlists/rockyou.txt $TARGET $SERVICE` |
| john | `john --wordlist=/usr/share/wordlists/rockyou.txt --format=$HASH_FORMAT $HASH_FILE` |
| metasploit | `msfconsole -q -x "use $MODULE_PATH; set RHOSTS $TARGET; set RPORT $PORT; run; exit"` |

Quote `$TARGET_URL` and any value containing shell metacharacters. Re-read the Step 0.5 security note
before interpolating anything into these strings.

**Verifying a tool is installed** (use this instead of trusting `/health`):
```bash
WHICH=$(curl -s -m 10 -X POST "$MKS_URL/api/command" -H "Content-Type: application/json" \
  -d "{\"command\":\"which <tool>\"}")
echo "$WHICH" | jq -r '.stdout // empty'   # non-empty path = installed
```

## Endpoints

### nmap
**Used by:** domain-assessment, cve-tester

SYN scan (full port, fast):
```bash
curl -s -m 120 -X POST "$MKS_URL/api/tools/nmap" \
  -H "Content-Type: application/json" \
  -d "{\"target\":\"$TARGET\",\"scan_type\":\"-sS\",\"additional_args\":\"-p- --min-rate 10000 -T4 -Pn\"}"
```

Service and version enumeration:
```bash
curl -s -m 120 -X POST "$MKS_URL/api/tools/nmap" \
  -H "Content-Type: application/json" \
  -d "{\"target\":\"$TARGET\",\"scan_type\":\"-sV -sC\",\"ports\":\"$OPEN_PORTS\",\"additional_args\":\"-T4 -Pn\"}"
```

Version fingerprinting (for CVE research):
```bash
curl -s -m 120 -X POST "$MKS_URL/api/tools/nmap" \
  -H "Content-Type: application/json" \
  -d "{\"target\":\"$TARGET\",\"scan_type\":\"-sV\",\"ports\":\"80,443,8080,8443\",\"additional_args\":\"--version-intensity 9\"}"
```

### gobuster
**Used by:** inventory-directory-scanner

```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/gobuster" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$TARGET\",\"mode\":\"dir\",\"wordlist\":\"/usr/share/wordlists/dirb/common.txt\",\"additional_args\":\"-b 404\"}"
```

### dirb
**Used by:** inventory-directory-scanner

```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/dirb" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$TARGET\",\"wordlist\":\"/usr/share/wordlists/dirb/common.txt\"}"
```

### nikto
**Used by:** inventory-directory-scanner

```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/nikto" \
  -H "Content-Type: application/json" \
  -d "{\"target\":\"$TARGET\"}"
```

### sqlmap
**Used by:** injection-tester, pentester-executor

GET parameter:
```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/sqlmap" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$TARGET_URL\",\"additional_args\":\"--batch --level=3 --risk=2\"}"
```

POST parameter:
```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/sqlmap" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"$TARGET_URL\",\"data\":\"$POST_DATA\",\"additional_args\":\"--batch --level=3 --risk=2\"}"
```

### hydra
**Used by:** pentester-executor

```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/hydra" \
  -H "Content-Type: application/json" \
  -d "{\"target\":\"$TARGET\",\"service\":\"$SERVICE\",\"username_file\":\"/usr/share/seclists/Usernames/top-usernames-shortlist.txt\",\"password_file\":\"/usr/share/wordlists/rockyou.txt\"}"
```

### john
**Used by:** pentester-executor

```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/john" \
  -H "Content-Type: application/json" \
  -d "{\"hash_file\":\"$HASH_FILE\",\"wordlist\":\"/usr/share/wordlists/rockyou.txt\",\"format\":\"$HASH_FORMAT\"}"
```

### metasploit
**Used by:** pentester-executor, pentester-orchestrator (Phase 5)

Requires operator approval before use (Phase 3 gate).

```bash
curl -s -m 300 -X POST "$MKS_URL/api/tools/metasploit" \
  -H "Content-Type: application/json" \
  -d "{\"module\":\"$MODULE_PATH\",\"options\":{\"RHOSTS\":\"$TARGET\",\"RPORT\":\"$PORT\"}}"
```

## Reminder

MKS is a REST API. Always invoke via `curl -X POST {url}/api/tools/{tool}` from Bash. Never invoke MKS tools as MCP tools.
