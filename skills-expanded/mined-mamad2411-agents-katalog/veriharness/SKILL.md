---
name: veriharness
description: Multi-rollout verification harness for high-stakes tasks. Generates independent candidate solutions, resolves disagreements against disk evidence, and actively challenges shared consensus to eliminate model blind spots before delivering code.
---

# VeriHarness: Multi-Rollout Verification Protocol

Based on the Google Research **VeriHarness** methodology (*"Same model. Better evidence."*).
Use this skill for complex bugs, critical architectural changes, high-stakes refactoring, or algorithmic tasks where single-rollout execution is prone to hallucinations or silent edge-case failures.

---

## Core Philosophy

1. **Agreement is NOT proof.** Rollouts from the same model share training blind spots. When candidates agree, actively challenge that consensus against the real environment.
2. **Evidence before judgment.** Never pick a solution by intuitive debate. Every decision must cite ground truth extracted directly from files, git history, or probe commands.
3. **Isolate, challenge, adjudicate.** Keep investigations focused and testable.

---

## 4-Step Verification Workflow

```
Task Inputs ──► Candidate Rollout A (Isolated) ──┐
            ──► Candidate Rollout B (Isolated) ──┼──► Disagreement Resolver ──► Ledger of Eliminations
                                                 │
                                                 └──► Consensus Challenger  ──► Ledger of Falsifications
                                                                    │
                                                                    ▼
                                                            Adjudication Turn
                                                                    │
                                                                    ▼
                                                            Repaired Deliverable
```

---

### Step 1: Generate Independent Rollouts

Spawn 2 independent subagents (or generate 2 distinct approaches in separate branches/drafts) using the exact same problem statement:
- **Rollout A:** Approach focused on direct, idiomatic implementation.
- **Rollout B:** Approach focused on defensive, minimal-state implementation.

Each rollout must output its concrete plan, code diff, and key technical assumptions.

---

### Step 2: Disagreement Resolution

Compare Rollout A and Rollout B to identify where they diverge:
- Different API choices or method signatures
- Conflicting assumptions about data schemas or environment state
- Divergent edge-case handling

**Action:** For every point of disagreement:
1. Write a minimal, deterministic probe (e.g., inspect schema file, run typecheck, probe a command).
2. Execute the probe against the codebase.
3. Record the winner and eliminate contradicted claims in a `ledger_elim` record:
   ```json
   {
     "disagreement": "Whether User.created_at is UTC datetime or timestamp string",
     "probe": "inspect models/user.py line 45",
     "evidence": "models/user.py defines created_at as datetime.datetime with tzinfo=UTC",
     "eliminated": "Rollout B assumption"
   }
   ```

---

### Step 3: Consensus Challenging

Identify claims, constants, or architectural assumptions that **both rollouts agreed upon**:
- Shared assumptions about third-party library behavior
- Shared assumptions about directory structures or config locations
- Shared omissions (e.g., neither rollout handled error status 429)

**Action:** Actively try to **falsify** the shared consensus:
1. Formulate a counter-hypothesis: *"What if this shared assumption is completely wrong?"*
2. Search the codebase or environment for contrary evidence (using `fff` search tools or shell probes).
3. If falsified, record the failed consensus in a `ledger_fals` record:
   ```json
   {
     "consensus_claim": "Shared assumption that Redis cache key TTL is in seconds",
     "falsification_probe": "Check config/cache.py settings",
     "evidence": "Cache helper expects milliseconds (TTL * 1000)",
     "status": "falsified"
   }
   ```

---

### Step 4: Adjudication & Evidence-Backed Repair

The lead agent acts as adjudicator, combining both ledgers:
1. **Select Base:** Choose the rollout with fewer eliminated claims as the `base`.
2. **Construct Repair Plan (`work[]`):**
   - Incorporate winning elements from the secondary rollout.
   - Patch all falsified consensus assumptions uncovered in Step 3.
3. **Execute & Deliver:** Apply the patch, run full project tests (`uv run pytest`, `pnpm test`), and deliver the final verified artifact with an audit trail explaining why each change was made.
