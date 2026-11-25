# Leveled `thorough` skill for `arwyl-extras`

**Status:** ACTIVE since 2026-08-31 (reaffirmed 2026-09-01, 2026-09-02)
**Decision:** Ship a new `thorough` skill plus a dispatched `investigator` subagent in `arwyl-extras`
(`arwyl-extras/skills/thorough/`, `arwyl-extras/agents/investigator.md`) — not `arwyl-lite`, per the
same no-knowledge-tree-dependency split test as `decision-plugin-split.md`. Domain-agnostic: research,
an implementation plan that must strictly follow existing patterns, a non-technical review (diet,
finances, a document), anything big enough that missing something is costly — not scoped to
"investigation" as a task type, and not scoped to code. Three levels, trading cost for breadth and
depth:

- **`standard`** (default) — write the task's surface to a checklist file before doing anything else,
  then work it single-handed, citing evidence and chasing each item past its first plausible finding.
- **`deep`** — the same enumeration, then works the checklist through `investigator` dispatches (cap ~6
  branches), each writing its own findings straight to a per-branch results file (linked from the durable
  manifest file, not inlined into it) the moment its completion notification is verified, at every speed —
  narrow scope buying real depth per branch, checkpoint-on-notification buying real survivability of a
  mid-run interruption, and the direct-write buying back the token cost of the orchestrator re-emitting
  what the subagent already generated. A `speed` lever (`fast`/`regular`/`slow`, default `regular`)
  controls how many branches may be simultaneously outstanding, trading wall-clock speed against how much
  an interruption can lose. An interrupted run can be resumed, same session, a different session, or a
  different account, by reading a branch's own transcript file directly, with `SendMessage`-by-agent-ID
  and a fresh dispatch as successive fallbacks.
- **`max`** — finer decomposition (cap ~10-12 branches) plus an adversarial verification round that
  grades every finding CONFIRMED/UNCONFIRMED before it's reported.

Only `standard`'s enumerate-first step is backed by an observed failure. `deep` and `max` are a
reasoned bet, shipped anyway at the owner's explicit request for a genuine high-stakes option — not
something the evidence independently confirmed fixes anything.

## Why (current reasoning)

`audit-2026-08-31-thorough-skill-evidence.md` found **one** concrete instance of the failure this was
meant to fix — a session that skipped straight into ad-hoc coverage instead of enumerating the surface
first, caught by the owner, redone. Against this repo's own bar for a mandatory mechanism
(`decision-mechanism-over-prose.md`: observed **read-then-violated, repeatedly**), N=1 does not clear
it — and the same audit found the opposite signal too: the prose-only fix that followed held on its one
retest, and a separate case (a single agent given an explicit scope and explicit permission to take its
time) performed adequately with no mechanism at all. A blanket mandatory mechanism was not justified by
what was actually found.

What *is* justified, and what changed the scope from "build nothing" to "build the minimum": the
enumerate-first step is cheap, mechanical, and directly answers the one confirmed failure — it costs
one file write before searching starts, and turns "was this thorough?" from an assertion into a
checkable planned-vs-covered fact. That part ships as the always-on default, same honesty class as
`decision-retrievability.md` ("preventive, reasoned not measured").

The `deep`/`max` fan-out and verification machinery is a different kind of bet: the owner asked for it
directly, for cases where the stakes justify paying for breadth and depth regardless of whether last
week's transcripts happen to contain a matching failure. Gating it behind an explicit level, rather than
making it the default behavior every "be thorough" phrase triggers, keeps the honest half (`standard`)
and the speculative half (`deep`/`max`) from being presented as the same kind of claim. The two axes are
named separately throughout (`thorough/SKILL.md`, `investigator.md`'s "go deep, not just wide" section)
because the evidence and the owner's own framing both treat breadth (never covered) and depth (covered
but shallow) as distinct failure shapes, not one problem with one fix.

**External corroboration.** `audit-2026-08-31-thorough-skill-external-techniques.md` checked the design
against Anthropic's own published multi-agent research system and the wider literature. Two production
failure modes named there had no guard and were added: per-item boundaries carried into `deep`/`max`
dispatch briefs, so branches don't quietly duplicate each other's work (an observed failure in Anthropic's
own system, not a hypothetical); and source-quality + "permission to conclude not found" guidance in
`investigator.md`, against the same system's observed unbounded/low-quality search failures. A third gap —
the skill never defined what makes one checklist *item* "covered", only that the whole checklist should be
— closed the same way, by a criterion converged on by multiple independent sources: 2+ corroborating
sources or 1 authoritative one, stop at exhausted novelty rather than the first plausible answer, and mark
a capped/unresolved item as such rather than reporting it as done. The `deep`/`max` branch caps (~6,
~10-12) sit close to Anthropic's own published effort-scaling bands — unchanged, with outside
corroboration rather than resting on this repo's judgment alone.

**Component choice:** one subagent type (`investigator.md`), not two. A real precedent for a dedicated
verifier exists (`claude-security`'s `scan-verifier.md` panel-of-voters pattern, confirmed live in the
official marketplace) but nothing in the evidence calls for a second agent type yet — `max`'s
verification round reuses `investigator` in a VERIFY-mode dispatch instead. `effort: xhigh` and a
restricted `tools:` list are frontmatter fields confirmed *in active use* across `claude-security`'s full
shipped agent suite (7 agents) before relying on them here; `effort: xhigh` has since been confirmed live in
a real dispatch, with `model: inherit` not escalating to a costlier model
(`incident-2026-09-01-thorough-deep-session-limit.md`). `tools:` is read/search
(`Read, Grep, Glob, Bash, WebSearch, WebFetch`) plus one narrow `Write` — see "Findings are written once".

**Checkpoint on a verified notification — not low concurrency — is what prevents loss.** The first real
`deep` run dispatched all branches in one batch and waited to "collect all reports" before doing anything
with them; when the account's usage limit hit mid-run, every in-flight branch was lost outright
(`incident-2026-09-01-thorough-deep-session-limit.md`). Live tests then showed batching itself was never
the exposure: the harness delivers a completion notification independently per agent, even for agents
dispatched together, and a notification can fire more than once, with an early one not always the final
result (`audit-2026-09-01-thorough-resume-design.md`, Findings 1–2). So each branch is checkpointed the
instant its notification verifiably reads like a finished report, at whichever speed is running, and
concurrency is a separate speed/exposure dial — `speed`: `fast`/`regular`/`slow`, default `regular`, up to
`ceil(cap/2)` branches outstanding at once, refilling as each is checkpointed. A second real run hit the
account limit again at `slow` and branches 1–3 survived, confirming the loss is driven by total token
spend, not concurrency (`audit-2026-09-01-thorough-gym-live-run.md`, Finding 1). A later 6-branch
`deep`/`regular` run completed fully with no limit hit, the window holding ≤3 outstanding throughout
(`audit-2026-09-02-field-study-ai-setup.md`).

**Resume reads a branch's own transcript first.** The durable checklist file carries a manifest: origin
session ID (`$CLAUDE_CODE_SESSION_ID`), project directory, and per-branch status, agent ID, and exact
subagent transcript path recorded at dispatch — those paths are documented and stable
(`audit-2026-09-01-thorough-resume-design.md`, Findings 3 and 6). Resuming an interrupted run — same
session, a different session, or a different account — tries a direct read of the branch's transcript
first, since that needs no live agent and no session or account match: in the one real cross-account case
it recovered a branch whose notification had arrived one turn before the limit killed the turn that would
have checkpointed it (`audit-2026-09-01-thorough-gym-live-run.md`, Findings 2–3). `SendMessage`-by-agent-ID
— confirmed same-session, and once cross-session at small scale on a single cleanly-completed transcript
(`audit-2026-09-01-thorough-resume-design.md`, Findings 4–5) — and then a fresh dispatch are the successive
fallbacks. Cross-session resume is best-effort, not guaranteed.

**Findings are written once.** Write-token duplication was measured at three re-emissions of the same
material — the subagent's report, the orchestrator's checkpoint `Edit`, and step 4's re-`Write` into a
permanent knowledge file (`audit-2026-09-01-thorough-gym-live-run.md`, Finding 4). So `investigator` writes
its full findings to a single per-branch results file its dispatch brief assigns, and returns only a
**one-sentence** report — nuance that feels lossy at one sentence belongs in the results file; a failed
write falls back to reporting in full, so findings are never silently dropped. The checklist links to each
results file rather than inlining it, and keeps exactly one status-bearing line per branch, extended in
place through `pending` → `launched` → `finished` — never a second, disagreeing `Status:` line
(`audit-2026-09-02-field-study-ai-setup.md`, Findings 1–2). Scope, boundary, and lettered sub-items stay
intact through `finished`: the rule keeps findings *text* out of the checklist, not the enumeration. Step 4
reuses step 3's synthesis instead of regenerating it, and offers to delete the superseded working checklist
and results files once persistence succeeds. All of this is instructed, not harness-enforced: subagent
`tools:` is a flat allow-list and the `Agent` dispatch carries no per-invocation permission override, so
per-path write scoping isn't natively available (confirmed against `code.claude.com/docs/en/sub-agents`) —
see Rejected.

**Claude Code's native "dynamic workflows" overlap this, and are not adopted.** Workflows
(`/docs/en/workflows`) provide journaled subagent orchestration with native concurrency control, per-agent
cost visibility, and a large-run cost warning, and bundled `/deep-research` already does much of what
`deep` does — but workflow resume is same-session only, and workflows are gated (opt-in on Pro via
`/config`, org-disableable), so a workflow-only `thorough` would break for consumers without them
(`audit-2026-09-01-thorough-resume-design.md`, Finding 7). `thorough` stays a prose skill; whether to also
ship an experimental `arwyl-extras/workflows/*.js` alternative is an open, not-yet-decided direction.

## Rejected

- **A blanket mandatory mechanism (fan-out always-on, no levels)** — the evidence bar this repo already
  holds itself to (`decision-mechanism-over-prose.md`) is not met; N=1 with a clean retest does not
  justify making the heavy path the only path.
- **Ship nothing, rely on the free technique alone** (explicit scope + explicit permission to take time
  + strict framing — what worked in the TheScriv counter-instance) — rejected as the *only* answer: it
  is real and worth knowing, but it doesn't explain why the one confirmed failure happened (no scope was
  given at all, because nothing had been enumerated yet), and it leaves the owner with no path to a
  deliberately higher-cost option for cases they judge worth it.
- **Scoping the skill to "investigation" as a task type** (the original `investigate` name and framing,
  renamed same day, before any install) — rejected: the owner's two counter-examples — planning a feature
  implementation that must strictly follow an existing codebase's patterns (a *plan* is the deliverable),
  and a thorough review of a diet (no code, output is analysis plus recommendations) — run through the exact
  same mechanism, and naming it as if the output were always a findings report actively misleads for a
  planning or non-technical analysis task. Step 3 is "Synthesize": the deliverable shape follows the task.
- **Dispatch every branch, checkpoint only after collecting all reports** (the `0.3.1` shape) — a mid-run
  usage-limit hit lost every in-flight branch with zero findings recoverable
  (`incident-2026-09-01-thorough-deep-session-limit.md`).
- **Strictly sequential `deep`/`max` dispatch** (`0.3.2`, superseded the same day) — more conservative
  than the evidence required once live tests showed per-agent notifications are independent:
  checkpointing, not concurrency, prevents loss.
- **A second `verifier` agent type**, or a multi-voter panel for `max`'s verify round (`scan-verifier.md`'s
  three-voters-per-lens pattern, and self-consistency literature generally) — real precedent exists for
  the *idea*, confirmed twice (original design pass and `audit-2026-08-31-thorough-skill-external-techniques.md`),
  but self-consistency's own literature notes it doesn't clearly transfer to open-ended findings that
  can't be cleanly voted on, and nothing has shown our single-voter VERIFY mode actually produces wrong
  grades. **Named trigger to revisit:** a real `max` run whose single-verifier grade turns out wrong
  (a false CONFIRMED or false UNCONFIRMED caught later) — build the panel then, not speculatively now.
- **Reusing the `ReportFindings` tool** for the findings output — that tool is scoped to `/code-review`
  by its own description; not this skill's to borrow.
- **An effort-level vocabulary matching `/code-review`'s full low/medium/high/xhigh/max/ultra ladder** —
  three levels cover the breadth/depth tradeoff this evidence supports; a finer ladder can be added if a
  real case shows these three don't discriminate enough.
- **A `PreToolUse`-hook-enforced per-branch write scope** — the mechanically-correct version of the
  write-duplication fix, checking each `Write`/`Edit` call against a live agent-id→path manifest and
  denying anything outside it. Not shipped: it needs a way to identify which dispatched subagent a given
  tool call belongs to and keep the manifest current under concurrent (`fast`/`regular`) dispatch, and one
  run's evidence doesn't justify that complexity yet against this repo's own mechanism bar
  (`decision-mechanism-over-prose.md`). Shipped instead: the prompt-scoped version (see "Why"). **Named
  trigger to revisit:** `investigator` writing outside its assigned path in a real run.

## Consequences accepted

- `deep`/`max` ship as a reasoned bet, not a validated fix — if a future review finds they don't help
  (or that `standard` alone was already sufficient), that's a real possible outcome, not a contradiction
  of this decision; revisit then rather than treating the bet as proven by having shipped it.
- **The cost is real and can exhaust a session-limited account.** A single `deep` dispatch burned a
  near-full 5-hour session window (`incident-2026-09-01-thorough-deep-session-limit.md`); checkpointing
  means branches already checkpointed survive a limit hit (`audit-2026-09-01-thorough-gym-live-run.md`,
  Finding 1), not that the run is cheap.
- `investigator`'s read-only design is narrowly relaxed (one `Write`, one assigned path, prompt-enforced) —
  a real departure from its original "no editing tools" framing, accepted because the cost it removes is
  measured, not assumed, and the fallback (report in full if the write fails) keeps the read-only design's
  actual guarantee — findings are never silently dropped — intact.
- **Still open:** `SendMessage`-by-agent-ID resume across accounts was never attempted — the one real
  cross-account case read the transcript instead; cross-session resume is unverified at real-branch scale
  and against a usage-limit-killed transcript; the `investigator` `Write` restriction is instructed, not
  harness-enforced (see Rejected); the cost warning still doesn't name a session-limit figure for non-API
  accounts; and `max` has never run, so its cost — finer branches *plus* a full verify wave, plausibly
  several times `deep`'s — is unmeasured.
- A second local-transcript search of this depth is expensive (two background passes, ~108
  transcripts); not a pattern to repeat casually for every future plugin addition — reserved for
  proposals of this size.

## Deliberation

- `audit-2026-09-02-field-study-ai-setup.md` — first observed full `deep` completion (a fourth,
  unrelated consumer): the checklist-collapse and investigator-report-length fixes behind `0.3.5`.
- `audit-2026-09-01-thorough-gym-live-run.md` — the second real `deep` run: write-token duplication
  measured directly, a real cross-account resume case, and the `0.3.4` fixes it justified.
- `audit-2026-09-01-thorough-resume-design.md` — the five live tests behind the `0.3.3` speed-lever and
  resume design: notification independence/duplication, subagent transcript path stability, same- and
  cross-session resume-by-ID, and the `$CLAUDE_CODE_SESSION_ID` env var.
- `incident-2026-09-01-thorough-deep-session-limit.md` — first real `deep` dispatch: cost confirmed via
  measured tokens/tool-calls, hard session limit hit.
- `audit-2026-08-31-thorough-skill-evidence.md` — the evidence review: the one confirmed failure,
  the clean retest, the counter-instance, and the verdict this decision is built on.
- `audit-2026-08-31-thorough-skill-external-techniques.md` — same-day external corroboration against
  Anthropic's own multi-agent research system and the wider literature; the source of the boundary,
  "covered"-criterion, and source-quality fixes, and of the named multi-voter-panel revisit trigger.
- `decision-mechanism-over-prose.md` — the bar this proposal was checked against, and did not clear in
  full (hence the leveled, opt-in shape rather than an always-on mechanism).
- `decision-retrievability.md` — the precedent for an honestly-labeled preventive addition on thin
  evidence.
- `decision-plugin-split.md` — why `arwyl-extras`, not `arwyl-lite`.
