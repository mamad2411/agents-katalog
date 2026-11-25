---
name: run-receipt
description: Use when an agent run completes, fails, or is being audited. A multi-step run is not done until a receipt exists showing what ran, what failed, and what was not observed. No receipt = it did not happen. Triggers include "agent run complete", "audit this run", "incident investigation".
---

# Run Receipt

A multi-step agent run is not complete until a **receipt** exists: a cryptographically signed, tamper-evident record of what ran, what failed, what was not observed, and who authorized each action. If no receipt exists, **the run did not happen** — you have no defensible audit trail.

This is observability as a first-class output, not an afterthought. Without receipts, incident investigations turn into "what did it actually do?" archaeology.

## When to run

- An agent completes a multi-step task
- An agent fails mid-task
- A production incident requires investigation
- Compliance or audit asks "what did the agent do?"
- The agent made an irreversible action (deployment, deletion, financial transaction)

If you cannot produce a receipt for the last 10 agent runs, your observability is logs and hope.

## What is a receipt

A **run receipt** is a cryptographically signed audit record of one agent action. Each receipt is:

1. **Structured** — W3C Verifiable Credential format
2. **Signed** — Ed25519 signature so the record cannot be forged
3. **Chained** — SHA-256 hash-linked to the previous receipt (tamper-evident)
4. **Complete** — captures who, what, when, outcome, and risk level

**Sources:**
- [Agent Receipts Protocol](https://agentreceipts.ai/)
- [Obsigna: Cryptographic Audit Trails](https://github.com/agent-receipts/ar)

### Receipt contents

```json
{
  "@context": "https://w3id.org/agent-receipt/v1",
  "type": "AgentReceipt",
  "id": "receipt:01HXYZ...",
  "issuer": "did:key:z6Mk...",
  "issuanceDate": "2026-08-16T03:00:00Z",
  "credentialSubject": {
    "agent": "agent-42",
    "humanPrincipal": "user@example.com",
    "action": {
      "type": "tool.filesystem.write",
      "riskLevel": "medium",
      "reversible": true
    },
    "outcome": "success",
    "timestamp": "2026-08-16T03:00:00Z"
  },
  "previousReceiptHash": "sha256:abc123...",
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-08-16T03:00:00Z",
    "verificationMethod": "did:key:z6Mk...",
    "proofValue": "z5Tk..."
  }
}
```

**Key fields:**

- `agent` — which agent acted
- `humanPrincipal` — who authorized the agent
- `action.type` — standardized taxonomy of action types
- `action.riskLevel` — low, medium, high (determines approval requirements)
- `action.reversible` — whether the action can be undone
- `outcome` — success, failure, or pending
- `previousReceiptHash` — hash link to the last receipt (tamper-evident chain)

**Sources:**
- [Agent Receipts Specification](https://agentreceipts.ai/specification/)

## How to implement

### 1. Install the signing daemon

Receipts are signed by a separate daemon that holds the signing key **outside the agent process**. This ensures that even if the agent is compromised, past receipts cannot be forged.

```bash
# Install Obsigna (reference implementation)
brew install agent-receipts/tap/obsigna

# Initialize the daemon (one-time setup)
obsigna-daemon --init

# Start the daemon
obsigna-daemon
```

The daemon listens on a Unix socket. Your agent sends events to the daemon, which signs and stores them.

**Sources:**
- [Obsigna Getting Started](https://obsigna.dev/getting-started/daemon-setup/)
- [Obsigna GitHub](https://github.com/agent-receipts/obsigna)

### 2. Emit receipts from your agent

Use the SDK to emit a receipt for every tool call:

**TypeScript:**
```typescript
import { createEmitter } from '@obsigna/sdk-ts';

const emitter = createEmitter({ socketPath: '/var/run/obsigna.sock' });

// Before executing a tool
await emitter.emit({
  agent: 'agent-42',
  humanPrincipal: 'user@example.com',
  actionType: 'tool.filesystem.write',
  riskLevel: 'medium',
  reversible: true,
  outcome: 'pending',
});

// After execution
await emitter.emit({
  agent: 'agent-42',
  humanPrincipal: 'user@example.com',
  actionType: 'tool.filesystem.write',
  riskLevel: 'medium',
  reversible: true,
  outcome: 'success',
});
```

**Python:**
```python
from obsigna import create_emitter

emitter = create_emitter(socket_path='/var/run/obsigna.sock')

emitter.emit({
    'agent': 'agent-42',
    'humanPrincipal': 'user@example.com',
    'actionType': 'tool.api.delete',
    'riskLevel': 'high',
    'reversible': False,
    'outcome': 'success',
})
```

**Sources:**
- [Obsigna SDK Docs](https://obsigna.dev/sdk/typescript/)

### 3. Verify the receipt chain

At any time, verify that the receipt chain is intact (no tampering):

```bash
obsigna receipt verify
```

This checks:
- Every receipt's signature is valid
- Every receipt's hash link points to the correct previous receipt
- No receipts have been deleted or reordered

**Sources:**
- [Obsigna CLI Reference](https://obsigna.dev/cli/receipt-verify/)

### 4. Hook into runtime (optional fast path)

For Claude Code and similar runtimes, use a PostToolUse hook to emit receipts automatically:

```json
{
  "hooks": {
    "postToolUse": [
      {
        "type": "obsigna",
        "config": {
          "socketPath": "/var/run/obsigna.sock"
        }
      }
    ]
  }
}
```

Every tool call emits a receipt with no code changes.

**Sources:**
- [Obsigna Hook Setup](https://obsigna.dev/getting-started/hook-setup/)

## Stop conditions — when NOT to proceed

**STOP** if any of the following is true:

1. The agent has run multi-step tasks but no receipt daemon is configured
2. Receipts are logged but not signed (mutable logs, not tamper-evident)
3. Receipts are signed but not chained (no hash links between them)
4. The signing key is stored inside the agent process (compromised agent can forge receipts)
5. You cannot verify the last 10 receipts (chain is broken or receipts are missing)

Do not claim the run is auditable. Set up the receipt infrastructure first.

## What a receipt enables

### 1. Incident investigation

When an agent misbehaves, the receipt chain shows **exactly what it did, in order**:

```bash
obsigna receipt list --agent=agent-42 --since=2026-08-15
```

Output:
```
receipt:01HXYZ...  agent-42  tool.filesystem.write  success  2026-08-16T03:00:00Z
receipt:01HXZA...  agent-42  tool.api.delete        success  2026-08-16T03:00:05Z
receipt:01HXZB...  agent-42  tool.git.push          failure  2026-08-16T03:00:10Z
```

You know the exact sequence, not "it probably did X."

### 2. Compliance and audit

EU AI Act Article 12 requires traceability for high-risk AI systems. A signed, tamper-evident receipt is a credible technical implementation of that requirement.

**Sources:**
- [EU AI Act Compliance with Agent Receipts](https://dev.to/ghostfactory/how-to-audit-ai-agents-from-mutable-logs-to-tamper-evident-history-5b7h)

### 3. Replay without LLM cost

Because receipts capture tool inputs and outputs, you can replay a failed run **locally** using recorded data, without paying for new LLM calls.

**Sources:**
- [Agent Evaluation Harness: Replay](https://www.kunalganglani.com/blog/agent-evaluation-harness-replay)

### 4. Human accountability

Every receipt links to `humanPrincipal` — the person who authorized the agent. If the agent deletes production data, the receipt shows who was in the loop.

## Verification checklist

Before claiming "the agent run is complete":

- ☐ A receipt exists for every tool call in the run
- ☐ Receipts are signed by a daemon outside the agent process
- ☐ Receipts are hash-chained (tamper-evident)
- ☐ The receipt chain verifies without errors
- ☐ Each receipt captures action type, risk level, and outcome
- ☐ Human principal is recorded for high-risk actions
- ☐ Receipts are retained for the required audit period (7+ years for regulated systems)

If any checkbox is unchecked, the run is not auditable. Build the receipt layer, then claim completion.

## Common mistakes

1. **Logs instead of receipts** — mutable logs can be altered; receipts are tamper-evident
2. **No human principal** — receipts show what the agent did, but not who authorized it
3. **Signing key in agent process** — a compromised agent can forge receipts
4. **No chain verification** — receipts exist but you never check if they're intact
5. **Receipt-free high-risk actions** — deployments and deletions happen with no audit trail

**Sources:**
- [Agent Receipts Trust Model](https://agentreceipts.ai/specification/trust-model/)

---

*A run without a receipt is an anecdote. A run with a signed, chained receipt is evidence.*
