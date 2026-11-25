---
name: log-tail-method
description: Tail structured logs from the dev server, filtered by correlation id, level, or module. Use when a request failed and you need what the server actually recorded — a 500 with no body, a trace to follow end-to-end, an error whose stack never reached the client. Reads what was already logged; it cannot recover a field the code never emitted, does not tail production, and is not a metrics or APM query.
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# log-tail-method

## Premise

Real artifacts only. Every claim cites the actual log line(s) observed + the timestamp + the correlation id used to filter. "Saw an error" without quoting the line is not a finding. The log source must be a real file, container, or process — never a paraphrase. PII (phones, emails, tokens) gets redacted before sharing; surfacing raw secrets is a halt-worthy mistake.

A "nothing in the logs" verdict without showing the exact `jq` filter run is a failed investigation.

Stream structured JSON logs (Pino / Winston / zerolog / structlog) with `jq` filters scoped to one request, level, module, or tenant.

**Scope boundary — this skill owns the mechanism, `/log-tail` owns the interpretation.** Everything here is how to *obtain* lines: source detection, the level-encoding probe, the field-name probe, the filters, the logger-specific gotchas. What the lines *mean* — the cluster halt, the no-match ladder, the reporting halts — lives in [`templates/packs/backend/commands/log-tail.md`](../../commands/log-tail.md) and is not restated here. One predicate, one owner: the level filter this skill emits shipping differently from the command's is exactly the defect that made a Pino project report a confident, false "nothing in the logs."

**Never hardcode the level predicate.** `.level` is a number in some loggers and a label in others, and a predicate built for the wrong encoding matches zero rows forever while looking correct. Probe first (Procedure step 3a), then build.

## When to use

- Endpoint returns 500 — find the stack trace + upstream calls in the same trace ID.
- Webhook receiver isn't firing — confirm payload arrived.
- Tenant reports "slow" — filter by their tenant ID and look for outliers.
- After enabling debug logs for one module without a global level change.

## Prerequisites

- Dev server logging in JSON (check the project's actual logger lib from extraction — Pino / Winston / zerolog / structlog / log15 / etc.).
- `jq` installed.
- One of: log file, container name, or running PID.

## Procedure

1. Identify log source from `CLAUDE.md` or running process:
   ```bash
   # File-based
   ls -1 logs/*.log 2>/dev/null
   # Container
   docker compose ps --services
   # Foreground process — pipe its stdout (redirect at start: `bun run start:dev | tee logs/app.log`)
   ```
2. Tail with the right command:
   ```bash
   tail -F logs/app.log                # file
   docker compose logs -f api          # container
   ```
3a. **Probe the encoding before building any predicate** — this step is not optional:
   ```bash
   tail -n 50 logs/app.log | jq -r '.level | type' | sort -u   # number | string | null
   tail -n 1  logs/app.log | jq -r 'keys | join(",")'          # which key carries the correlation id
   ```
   | Probe returns | Level predicate to use |
   |---|---|
   | `number` | `select(.level >= 50)` — Pino's ascending scale (`trace=10, debug=20, info=30, warn=40, error=50, fatal=60`); use `>= 40` to include warn. |
   | `string` | `select((.level \| ascii_downcase) as $l \| $l == "error" or $l == "fatal" or $l == "warn")` — downcased because some JSON handlers emit the label uppercase (`"level":"INFO"`). |
   | `number`, scale not Pino's | Establish the direction from that logger's own docs first. On a descending scale `>= 50` selects everything *except* errors. Direction unknown → escalate, do not guess. |
   | more than one type | Two log sources are interleaved in this file — separate them before filtering. |
   | `null` / absent | The level lives under another key (`severity`, `levelname`, `lvl`); read `keys` and re-probe. |

   The correlation key is probed the same way and passed in — `reqId`, `req.id`, `correlationId`, `request_id`, `traceId` and `trace_id` are all in live use; assuming one is how a filter returns nothing on a correctly-instrumented app.

3b. Apply the filter via `jq`, using the level predicate and correlation key 3a resolved:
   ```bash
   # Errors only — predicate from 3a, never hardcoded
   tail -F logs/app.log | jq -c 'select(.level >= 50)'                 # numeric-level logger
   tail -F logs/app.log | jq -c 'select((.level|ascii_downcase) as $l | $l=="error" or $l=="fatal")'   # label logger
   # Single request trace — probed key, both flat and nested forms
   tail -F logs/app.log | jq -c --arg id "abc-123" 'select(.reqId == $id or .req.id == $id or .correlationId == $id or .request_id == $id or .traceId == $id)'
   # One module
   tail -F logs/app.log | jq -c 'select(.context == "OrdersService")'
   # One tenant
   tail -F logs/app.log | jq -c --arg t "tenant_42" 'select(.tenantId == $t or .tenant_id == $t)'
   # Slow requests
   tail -F logs/app.log | jq -c 'select(.responseTime > 500)'
   ```
4. For unstructured fallback, swap `jq` for `grep -E`:
   ```bash
   tail -F logs/app.log | grep -E 'ERROR|FATAL|reqId=abc-123'
   ```
5. Pretty-print one event when investigating:
   ```bash
   tail -n 200 logs/app.log | jq 'select(.reqId=="abc-123")' | jq -s '.'
   ```

## Output

```
[2026-04-24T09:14:02.123Z] ERROR  OrdersService  req=a1b2c3  tenant=t_42  failed to create order: validation error
[2026-04-24T09:14:02.124Z] ERROR  ExceptionFilter req=a1b2c3 tenant=t_42 ValidationError: items[0].sku must not be empty
   at CreateOrderDto.validate (src/orders/dto/new-order.dto.ts:34)
   at OrdersController.create (src/orders/controllers/orders.controller.ts:58)
[2026-04-24T09:14:02.125Z] INFO   HttpLogger     req=a1b2c3 tenant=t_42 POST /orders 400 2ms
```

**Lines are the output of this skill, not the answer.** Hand them to `/log-tail`'s cluster halt (group by signature, enumerate every correlation id) — and when the filter returns **zero** rows, to its no-match ladder, which distinguishes "wrong source", "wrong predicate", "request never reached the handler" and "chain swallowed mid-flow". Reporting an empty result without walking that ladder is the failed investigation this skill's premise forbids.

## False positives / gotchas

- Multi-line stack traces break naive `tail | grep` — Pino keeps them as a single JSON line; some loggers don't.
- Time zones: log timestamps may be UTC while CLAUDE is in local time — convert when correlating with user-reported timestamps.
- PII: phone numbers, emails, tokens may be in logs — redact before sharing (`jq` with `.user.phone |= sub("(\\d{3})\\d+(\\d{3})";"\(.1)***\(.2)")`).
- `tail -f` (lowercase) drops the file on rotation; `tail -F` follows the rename — always use `-F` for long sessions.
- Dev only — never tail prod logs from this skill; use the central log aggregator.

## Related

- Used by `@bug-investigator` — the agent invokes `log-tail-method correlation:<id>` (or `log-tail-method error` + timestamp) as its first evidence-gathering step.
- `.claude/skills/debug-tenant/SKILL.md` — supplies log-tail-method the tenant id / correlation id to walk the tenant-resolution chain; log-tail-method produces the cited log lines that playbook requires.
- `.claude/skills/endpoint-test-method/SKILL.md` — when a test case returns 500 or a wrong shape, log-tail-method follows that request's trace into the logs.
- `ai/patterns/error-handling.md` — the `traceId` correlation id + structured-log discipline these filters key on.
- `.claude/rules/backend-principles.md` — the structured-logging + no-PII-in-logs MUSTs this skill enforces at read time.

## Halt conditions

- Halt on hand-waves: every finding must quote the actual log line + timestamp + correlation id.
- Halt if PII (phone, email, token) appears in the report unredacted — sanitize before surfacing.
- Halt if a "nothing found" verdict is returned without showing the exact `jq` (or `grep`) filter executed.
- Halt if this skill was pointed at production logs — refuse and redirect to the central aggregator.
- Halt if a level predicate was applied without the step-3a encoding probe — a hardcoded predicate on the wrong encoding returns zero rows and reads as an all-clear.
