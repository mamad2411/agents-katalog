---
name: agentic-ops-core
description: "Shared reference for the agentic-ops cluster: the evidence-first operator loop (resolve surface → read live state → smallest reversible action → prove it → report exact status), the surface taxonomy, the status-word vocabulary, and the secrets/PII guardrails every operator spoke obeys. USE WHEN operating any live external surface — inbox, repo, tracker, billing, docs — or before any send/push/refund/mutation in this cluster."
cluster: agentic-ops
version: 1.0.0
---

# Agentic Ops Core

Shared model for the `agentic-ops` cluster. Every spoke — comms, code-host, tracker, knowledge,
billing, audit — runs the **same loop** over a different surface. Keep that loop and its vocabulary
consistent here so no spoke claims state it didn't prove and no spoke widens a mutation silently.

## 1. The operator loop (this cluster's defining model)

Operations are **read-before-write** and **prove-before-claim**. Every spoke walks the same five
steps; only the surface changes:

```
Resolve surface ──> Read live state ──> Smallest reversible action ──> Prove it ──> Report exact status
   (which?)            (inspect)           (draft / narrow / no-op)      (evidence)     (one status word)
```

1. **Resolve the exact surface.** Which mailbox/account, repo+branch, thread, tracker item, billing customer, or store. Ambiguity here is the #1 source of wrong actions. → every spoke opens with this.
2. **Read live state before mutating.** Inspect the thread, diff, ticket, invoice, or config *now* — never act from memory when the live surface is readable. → `terminal-ops`, `email-ops`, `automation-audit-ops`.
3. **Smallest reversible action first.** Default to **read-only / draft / no-op** unless a live send/push/refund/delete was explicitly requested. Restore self-serve before refunding; narrow the fix before a repo-wide pass. → `customer-billing-ops`, `terminal-ops`.
4. **Prove it.** Attach concrete evidence: a Sent-folder entry, the branch that moved upstream, the CI run, a file path, a snapshot timestamp, an exact failure signature. A claim without proof is a guess. → `finance-billing-ops`, `terminal-ops`.
5. **Report one exact status word.** No vague "done". Use the spoke's status vocabulary (§3).

**Rule:** if you cannot prove a step, **say what's blocking it** rather than asserting completion.

## 2. Surface taxonomy

Operations group into six surface families. Routing is **surface × intent**; the orchestrator
picks the family, the spoke owns the loop.

| Surface family | Spokes | The thing being operated |
|---|---|---|
| **Communication** | `email-ops`, `messages-ops`, `unified-notifications-ops` | inboxes, DMs, alert streams |
| **Code-host & execution** | `github-ops`, `git-workflow`, `terminal-ops` | repos, branches, CI, releases |
| **Project flow & trackers** | `project-flow-ops`, `jira-integration` | issues, PRs, execution lanes |
| **Knowledge & documents** | `knowledge-ops`, `google-workspace-ops` | KB layers, Drive/Docs/Sheets/Slides |
| **Revenue** | `customer-billing-ops`, `finance-billing-ops` | subscriptions, invoices, pricing truth |
| **Audit & observability** | `automation-audit-ops`, `workspace-surface-audit`, `connections-optimizer`, `dashboard-builder` | live inventory, env surface, social graph, metrics |

## 3. Status-word vocabulary (the proof contract)

Each spoke reports a **bounded, exact** final state. Never substitute a vaguer word.

| Spoke / family | Allowed terminal states |
|---|---|
| `email-ops` | drafted · approval-pending · sent · blocked · awaiting-verification |
| `messages-ops` | read · code-found · blocked · awaiting-reply-draft |
| `terminal-ops` | inspected · changed-locally · verified-locally · committed · pushed · blocked |
| `automation-audit-ops` / `project-flow-ops` | keep · merge · cut/close · fix-next · park |
| billing (`customer-`/`finance-`) | classified · refunded · preserved · converted · no-op |

The rule behind the table: **a status word is a promise you can back with evidence.** "sent"
requires a Sent-folder check; "pushed" requires the upstream branch to have moved; "verified-locally"
requires the proving command to have been re-run; "refunded" requires the charge to be classified first.

## 4. Live vs. snapshot (the freshness rule)

- Prefer **live** data on every read (live mailbox, live `git`/`gh` state, live billing API, live config).
- If data is **not** live, state the snapshot timestamp explicitly. → `finance-billing-ops` ("SNAPSHOT — timestamp").
- "Present in config" is **not** "working". Mark surfaces as configured / authenticated / recently-verified / stale / missing — they are different. → `automation-audit-ops`, `workspace-surface-audit`.

## 5. One canonical home (the no-duplicate rule)

- Keep **one canonical home per fact set**; avoid parallel copies of the same plan across notes, repo files, and tracker docs. → `knowledge-ops`.
- Dedupe **before** storing: search first, then create-or-update. → `knowledge-ops`, `google-workspace-ops` (find the current tracker, not the stale duplicate).
- Public vs internal split is deliberate: **GitHub = public truth, Linear = internal execution truth**; not every issue needs both. → `project-flow-ops`.
- `customer-billing-ops` (one customer's remediation) and `finance-billing-ops` (operator revenue/pricing truth) are a **deliberate split**, not a duplicate — route per question, don't merge.

## 6. Shared guardrails

- **Read before write; prove before claim.** Inspect live state; never assert *sent/pushed/fixed/refunded* without naming the proof.
- **Default-deny on mutation.** Draft/read-only/no-op unless the live action was explicitly requested; smallest reversible step first; never use destructive `git` or blind refunds.
- **Secrets & PII.** Never expose API keys, tokens, webhook secrets, full card details, or unnecessary customer PII; redact before committing to Git.
- **Separate fact from recommendation.** Keep revenue fact / customer impact / code-backed truth / recommendation in distinct buckets; same for audit findings vs proposed fixes.
- **Audit before remediate.** When overlap or breakage is suspected, build the evidence table first (`automation-audit-ops`, `workspace-surface-audit`) before merging, cutting, or rewriting.
- **Right surface, stated plainly.** If the real fix is a different surface — better triage, a hook policy, a product/billing gap — say so instead of forcing the current tool.
