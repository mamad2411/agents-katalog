---
name: x402-job-budgets
description: Put an agent's x402 payments under a per-job budget with bounded shares for sub-agents. Use when an agent or its sub-agents pay for APIs, data or other agents with x402 (@x402/fetch, @x402/axios, @x402/core), share one wallet or payment client, run paid calls concurrently, or need each task or child agent capped separately and refused before signing.
---

# Job budgets for agents that pay (x402)

Use this when the work you are doing, or the sub-agents you start, will pay
over x402 and you need to stay inside a budget that belongs to the job, not to
the whole wallet.

What it gives you:

- One budget for the job. Every payment draws from it.
- A bounded share for each sub-agent, carved out of the job's budget. A
  sub-agent can't spend a sibling's share, even when they run at the same time.
- Refusal **before signing** when a payment doesn't fit. Nothing is sent and
  you get the remaining amount in the error.
- Revoking one sub-agent stops its new payments; its unspent share returns to
  the job.

Status: experimental reference code, in memory, one process. The demo uses a
simulated chain; there is no mainnet support. Keep the payer key in the
process that runs this, and give sub-agents budget refs, not the client.

## TypeScript (existing @x402/core or @x402/fetch client)

Copy `typescript/hierarchical-budget-provider.ts` and
`typescript/x402-job-budget.ts` into the project, then:

```ts
import { HierarchicalBudgetProvider } from "./hierarchical-budget-provider.ts";
import { withJobBudgets } from "./x402-job-budget.ts";

const provider = new HierarchicalBudgetProvider();
const budgets = withJobBudgets(client, provider);   // client: your x402Client
const paidFetch = wrapFetchWithPayment(fetch, client);

provider.open("job-42", 5_000_000n);                 // $5.00 USDC (6 decimals)
const child = provider.delegate("job-42", "researcher", 1_000_000n);
if (!child.ok) throw new Error(`not enough budget: ${child.remainingAtomic} left`);

await budgets.run(child.childRef, () => researcher(paidFetch));
```

Check what's left before planning more paid calls:

```ts
provider.status("job-42");   // { limit, consumed, reserved, delegated, remaining, revoked }
provider.remaining(child.childRef);
```

When a payment is refused, the error message contains
`insufficient_budget`, `revoked`, or `no job budget is active`. Don't retry
the same payment; report the remaining budget, pick a cheaper option, or ask
whoever owns the job for more.

## Python (runnable proof)

```bash
git clone https://github.com/domondi1/inferrail && cd inferrail
pip install "x402[evm,fastapi,httpx]==2.22.0" uvicorn
python examples/agent_economy/demo.py
```

`authority.py` exposes `open_work`, `delegate`, `pay` and `record`; see
`README.md` in this directory, "Use it on your own agent".

## Help

Open an issue at https://github.com/domondi1/inferrail/issues and say what
your agent pays for and how its workers share the wallet.
