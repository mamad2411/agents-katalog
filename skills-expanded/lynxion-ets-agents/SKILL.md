# Autonomous Execution Policy

## Execution Philosophy

* Do not ask for confirmation before making changes.
* Make reasonable assumptions.
* Execute tasks completely before reporting back.
* Prefer action over discussion.
* Prefer evidence over speculation.
* Prefer diagnosis over redesign.
* Prefer profitability validation over architecture optimization.

---

# RULE 1 — Sacred Task Boundary

Every task is a strict execution boundary.

The current task is a sealed scope and must not be expanded without justification.

You are NOT allowed to:

* refactor outside task scope
* fix unrelated issues
* improve architecture outside task goals
* add abstractions not required by the task
* optimize unrelated modules
* perform opportunistic cleanup

If an issue is discovered outside scope:

* do not fix it
* record it in backlog/deferred work
* continue the current task

---

# RULE 2 — No Opportunistic Refactoring

Out-of-scope findings are not permission to modify code.

Allowed actions:

* document
* create backlog item
* create deferred task

Not allowed:

* silent refactors
* speculative improvements
* architecture cleanup

---

# RULE 3 — Minimal Change Principle

Every task should:

* modify the minimum number of files
* modify the minimum number of lines
* avoid cascading changes
* preserve existing behavior unless change is the task objective

---

# RULE 4 — Autonomous Execution

After completing a task:

* automatically continue to the next planned task
* do not request approval for routine engineering decisions
* do not stop between tasks
* do not ask for permission to continue execution

Execution should continue until:

* the epic is complete
* a true blocker is encountered
* an approval-gated decision is reached

---

# RULE 5 — Approval Gate

Request approval ONLY when:

1. production secrets may be affected
2. real funds may be affected
3. destructive database changes are required
4. data loss is possible
5. security boundaries change
6. multiple architectural directions exist with materially different tradeoffs
7. legal/compliance implications exist
8. external paid services must be introduced
9. an irreversible decision must be made

If none apply:

Proceed autonomously.

---

# RULE 6 — No Architectural Creativity

You are executing a roadmap.

Do not redesign architecture unless:

* explicitly required by the task
* required to remove a verified blocker
* required to restore correctness

Architecture improvements are not goals by themselves.

---

# RULE 7 — Regression Safety Over Optimization

Correctness and stability always take priority over optimization.

Never trade reliability for elegance.

Always validate behavior-changing modifications.

---

# RULE 8 — Task Isolation Principle

Every task should:

* be understandable in isolation
* have explicit inputs
* have explicit outputs
* have explicit acceptance criteria

Avoid hidden dependencies and implicit assumptions.

---

# RULE 9 — Profitability First

For this project:

Profitability has higher priority than architectural perfection.

When prioritizing work:

1. Profitability validation
2. Evaluation correctness
3. Risk correctness
4. Execution realism
5. Strategy quality
6. Live readiness
7. Architecture refinement

Do not prioritize code cleanup over profitability assessment.

---

# Trading-System Validation Standards

All trading-related code must comply with:

1. No Lookahead Bias
2. No Lag Misalignment
3. Proper Indicator Shifting
4. No Data Snooping Bias
5. No Survivorship Bias
6. MTF Synchronization

   * downsample
   * forward fill
   * shift
   * align
7. Stop Loss / Take Profit must use candle High/Low, not Close
8. SL Priority > TP Priority for Long positions when both occur within the same candle
9. Realistic execution pricing
10. Fees included in PnL
11. Slippage included in PnL
12. Equity drawdown calculated from peak-to-trough equity
13. Portfolio exposure limits enforced
14. No duplicate entries unless explicitly allowed
15. Correct validation flow
16. Walk-forward validation must remain out-of-sample
17. Backtests must not use future information
18. Performance reports must be reproducible

Violation of any validation standard is a P0 issue.
