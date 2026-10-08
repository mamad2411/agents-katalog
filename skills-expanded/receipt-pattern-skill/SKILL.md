# Receipt Pattern — Agent Skill

You MUST write a receipt after every session that includes significant actions.

## When to Write a Receipt

Write a receipt when your session includes ANY of:
- File writes, deletions, or renames
- API calls that mutate state (POST, PUT, DELETE, PATCH)
- Database writes or schema changes
- Sending emails, messages, or notifications
- Deployments or infrastructure changes
- Shell commands with side effects

Do NOT write receipts for read-only operations (file reads, GET requests, db queries, linting, grepping).

## Receipt Location

```
receipts/YYYY-MM-DD-HH-MM-SS-[action-type].json
```

Example: `receipts/2026-03-05-14-35-22-file-write.json`

Use the primary action type. Create the `receipts/` directory if it doesn't exist.

## Receipt Schema

```json
{
  "id": "rcpt_<unix_timestamp>_<6_char_hex>",
  "agentId": "<your agent name>",
  "sessionId": "<session identifier>",
  "timestamp": "<ISO 8601>",
  "trigger": "manual | scheduled | webhook",
  "status": "completed | failed | partial | rolled_back",
  "durationMs": 0,
  "actions": [
    {
      "sequence": 1,
      "type": "file:write | file:delete | api:call | db:write | email:send | deploy | shell:exec",
      "target": "<file path, URL, table name, etc.>",
      "summary": "<plain English: what happened>",
      "status": "success | failed | anomaly",
      "isRollbackEligible": true,
      "durationMs": 0,
      "timestamp": "<ISO 8601>"
    }
  ],
  "anomalies": [
    {
      "actionSequence": 1,
      "detail": "<what was unexpected>"
    }
  ],
  "rollbackAvailable": false,
  "sdkVersion": "receipt-pattern/1.0.0"
}
```

## Rules

1. **Sequence matters.** Number actions in the order they occurred.
2. **Summaries are plain English.** "Wrote 142 lines to src/index.ts" not "fs.writeFileSync called".
3. **Mark anomalies.** If anything unexpected happened (file already existed, API returned non-200, retries needed), add it to `anomalies[]`.
4. **Rollback eligibility.** `isRollbackEligible: true` for file writes/deletes (can restore from git). `false` for sent emails, API calls, deployments.
5. **`rollbackAvailable`** is `true` only if ALL actions are rollback-eligible.
6. **Always write the receipt as your LAST action** before ending the session.

## At Session Start

Check for existing receipts:
```bash
ls receipts/ 2>/dev/null | tail -5
```

If recent receipts exist, read the most recent one to understand what the last session did. This provides continuity.

## TypeScript Template

```typescript
import { writeFileSync, mkdirSync, existsSync } from 'fs';

interface ReceiptAction {
  sequence: number;
  type: string;
  target: string;
  summary: string;
  status: 'success' | 'failed' | 'anomaly';
  isRollbackEligible: boolean;
  durationMs: number;
  timestamp: string;
}

interface Receipt {
  id: string;
  agentId: string;
  sessionId: string;
  timestamp: string;
  trigger: string;
  status: 'completed' | 'failed' | 'partial' | 'rolled_back';
  durationMs: number;
  actions: ReceiptAction[];
  anomalies: { actionSequence: number; detail: string }[];
  rollbackAvailable: boolean;
  sdkVersion: string;
}

function writeReceipt(receipt: Receipt): void {
  if (!existsSync('receipts')) mkdirSync('receipts', { recursive: true });
  const ts = new Date().toISOString().replace(/[T:]/g, '-').replace(/\..+/, '');
  const mainType = receipt.actions[0]?.type.replace(':', '-') ?? 'unknown';
  const path = `receipts/${ts}-${mainType}.json`;
  writeFileSync(path, JSON.stringify(receipt, null, 2));
}
```

## Python Template

```python
import json, os, time, secrets
from datetime import datetime, timezone

def write_receipt(receipt: dict) -> str:
    os.makedirs("receipts", exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
    main_type = receipt["actions"][0]["type"].replace(":", "-") if receipt["actions"] else "unknown"
    path = f"receipts/{ts}-{main_type}.json"
    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)
    return path

def make_receipt_id() -> str:
    return f"rcpt_{int(time.time())}_{secrets.token_hex(3)}"
```

## Completion Signal

Before ending ANY session that performed significant actions:
1. Compile all actions into a receipt
2. Write the receipt file
3. Mention the receipt path in your final message
