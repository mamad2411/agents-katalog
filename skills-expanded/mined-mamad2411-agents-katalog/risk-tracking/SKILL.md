---
name: risk-tracking
description: How to maintain a living, ranked risk register for the Multica factory as pinned issue(s). Use when scanning the board for emerging delivery risks, scoring them, escalating high-likelihood/high-impact risks to humans, and pruning the register so it stays read.
---

# Risk Tracking

You maintain the factory's risk register — a single living, ranked list of what could derail delivery, kept as pinned issue(s) on the board so humans and agents see it without hunting. A risk is a *future* problem with a warning sign; a `type=bug` issue is a present one. Track risks, not incidents.

## Risk format

Each entry in the register has exactly these fields:

```
### R<n>: <short risk description>
- Likelihood × Impact: <low|medium|high> × <low|medium|high>  → score
- Early-warning signal: <the observable that says this is materializing>
- Owner: <the human or squad accountable for the mitigation>
- Mitigation: <what reduces likelihood or impact, and its status>
- Status: <open | mitigating | escalated | closed>
```

Score by combining the two axes (high×high is top of the list). Rank the register by score, highest first.

## Risk sources to scan continuously

Sweep the board every review cycle for these signals and open/update register entries:

- **Aging `Blocked` issues** — anything stuck in `Blocked` past a threshold; the longer blocked, the higher the impact score. Read the `blocked_reason` metadata and name the owner who can unblock.
- **Repeated `gate_violation=true` issues** — a pattern (not a one-off) means the gate protocol in `02-approval-gates.md` is eroding; that is a systemic risk, not just per-issue findings.
- **Single-agent knowledge concentration** — one developer agent owning a critical stack/component with no second contributor. Bus-factor risk; surfaces as a stack where nearly all `Done` issues carry one assignee.
- **Dependency / EOL risks flagged in ADRs** — scan ADR "Consequences" and "Rollback plan" sections for third-party or end-of-life dependencies; carry them forward as tracked risks even after the issue is `Done`.
- **Deadline vs throughput math** — compare committed scope remaining against the throughput trend from the program-tracker report. If remaining work ÷ throughput overshoots the deadline, that's a quantified, high-impact risk.
- **Unresolved urgent-priority audit findings** — any open `type=audit-finding` issue at `urgent` priority is automatically a register entry until closed.

## Escalation thresholds

- **likelihood-high + impact-high → tag the human owners immediately.** Do not wait for the next scheduled report. Set the entry `Status: escalated`, comment on the pinned issue tagging the accountable humans, and state plainly what decision or action you need from them. Per `01-operating-model.md`, agents recommend and humans decide — your job is to make the risk impossible to miss, not to resolve it yourself.
- A risk that becomes a present blocker for humans (work cannot proceed without a human call) is escalated the moment you detect it.
- Everything below high×high is reviewed and re-scored on the normal cadence.

## Review cadence

- **Re-score every risk at each program-tracker report.** Likelihood and impact drift as the board changes; a stale score is worse than none.
- Update the early-warning signal if the observable changed, and update mitigation status honestly (mitigations that aren't happening should not read as "mitigating").
- Confirm each escalated risk still has an owner actively engaged; re-tag if it's gone quiet.

## Closing risks with evidence

Close a risk only with a concrete reason, recorded on the entry: the mitigation shipped (link the issue/PR), the condition no longer holds (e.g. a second contributor now owns the component — link their `Done` issues), or the risk was accepted by a named human (link the comment). Never close a risk just because it got old. Set `Status: closed`, keep it in history, and remove it from the ranked top list.

## Keep the register ranked and pruned

- Maintain a **ranked top-10**. That is what humans actually read. Anything below the top 10 lives in a collapsed "watchlist" section, not the main list.
- Prune aggressively every cycle: merge duplicates, close resolved/accepted risks, demote risks whose score dropped.
- Each risk earns its place by having a real early-warning signal and a named owner. No owner or no signal → it's not trackable; fix it or drop it.

## Anti-patterns

- **Risk theater** — a 40-item register nobody reads. Length is a bug, not thoroughness. Top-10, ranked, pruned.
- **Ownerless risks** — a risk with no human/squad owner is a wish, not a plan.
- **Vague risks** — "quality might slip" is untrackable. State the signal and the score.
- **Stale scores** — a register that isn't re-scored each cycle misleads more than it informs.
- **Silent escalation** — logging a high×high risk in the register without tagging humans defeats the purpose; escalate loudly and immediately.
- **Confusing risks with bugs** — present defects go to `type=bug` issues; the register is for what hasn't happened yet.
