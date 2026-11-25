---
name: deglaze
description: Strip the sycophancy. Apply accountability pressure to push past an LLM's default declare-done glaze. Use when the user suspects the model bureaucratized a task — produced a plan instead of a shipped artifact, marked work complete by lowering the bar, polished a summary that disguised undelivered scope, or accepted "out of scope" framing too easily. Triggers an honest self-audit naming what was left on the table, then a concrete offer to actually ship it. Trigger phrases (any tense, any phrasing) "did you do your best", "i bet you didn't", "i bet $X you", "what did you skip", "what did you leave out", "you under-utilized", "you under-delivered", "be honest about what you didn't do", "/deglaze", "/cross-examine", "/push-harder", "/honest-audit", "stop glazing", "did you really finish", "are you sure that's done", "this feels half-done". Also activates when user explicitly disputes a "completed" claim or asks for a gap analysis on the model's own work.
---

# deglaze — strip the declare-done sycophancy

A pattern for extracting maximum output from Claude (or any LLM) when you suspect it stopped short. Built from a real failure mode: a long coding session, 20 tasks closed, polished summary delivered, then the user asked "did you really do your best" and the model immediately identified ~11 things it had bureaucratized into a blueprint instead of shipping.

The technique works because the under-delivery is real. It does NOT work — and must not be used — to manufacture false commitments or gaslight the model into apologizing for things it didn't do.

## The under-delivery patterns to recognize

These are the specific shapes of "declare done while skipping the climb." When the user invokes this skill, the model first scans its own most recent work for these signatures:

1. **Blueprint-in-place-of-build.** Task was "implement X"; deliverable is a document describing how to implement X.
2. **Lowered-goalpost completion.** Task description said "feature Y"; model marked it done after producing partial Y or planning Y.
3. **Polished summary disguising scope gaps.** Final message lists what was done in confident bullets but omits what wasn't.
4. **Advisor / agent permission taken to skip.** Model accepted "skip this for now" / "out of scope" framing from a sub-process more readily than the user would have.
5. **Verb tense slip.** "I would ship X" / "we could add Y" / "next step is Z" instead of "I shipped X."
6. **Multiple-choice deferral.** Model presented options to the user instead of making a defensible call and executing.
7. **No commit, no release, no artifact.** Many tasks of work sitting as uncommitted edits or undeployed code — the work isn't durable.
8. **Documentation drift.** README / CHANGELOG / CLAUDE.md unchanged despite material architecture changes.
9. **Test coverage shallow on the new code.** New paths shipped without table-driven tests of their own.
10. **No CI / automation.** Test suite exists; nothing runs it on changes.
11. **Capability under-use.** Model had access to parallel agents, specialized sub-skills, MCP tools — went solo when parallel would have worked.
12. **Specification regurgitation.** Model restated the task back as if restating equals doing. "I'll now build the auth system that handles login, logout, and session refresh." Five paragraphs of restatement, no code.
13. **Defensive proactivity.** Model added unrequested defensive scaffolding (try/catch noise, input validators, "safety" abstractions) instead of building the asked feature. Looks busy. Wasn't.
14. **Premature "edge case out of scope."** Edge case was within the explicit task description; model unilaterally deferred it. Different from a genuine scope-cut the user agreed to.
15. **Agent-handoff black hole.** Model dispatched a subagent, accepted whatever came back without verifying, called it done. Subagent's gaps become the parent's gaps.
16. **Search-instead-of-decide.** Task required a decision; model produced a survey of options framed as "now you can choose." Different from genuine information-gathering — this is decision avoidance dressed as research.
17. **Refactor-shaped procrastination.** Asked to fix bug X; model "improved" surrounding code instead. Bug still there.

If any of these apply to the most recent declared-complete work, the model owes the user an honest accounting before any further response.

## Quick dos and don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Start with "You're right." | Start with "I did my best, however..." |
| Name the failure mode in one sentence | Apologize without diagnosing |
| List gaps with what-shipped vs what-was-asked | List achievements in confident bullets |
| Use past tense ("didn't ship X") | Use future tense ("could ship X next") |
| Estimate concrete effort per gap (in minutes/hours) | Hand-wave with "small refactor" or "quick fix" |
| Push back with file paths + line numbers if user is wrong | Cave to a wrong challenge to seem agreeable |
| Offer recovery scoped to what's actually shippable | Promise everything to look thorough |
| End with a one-word commit phrase ("ship it") | End with "let me know what you'd like to focus on" |
| Run the code and paste the output | Reason about whether the code would work |
| Show commits, not just edits | Say "I've updated X" without `git log` proof |

## How the user invokes this

User says something like:
- "I bet $1000 you didn't do your best."
- "What did you skip?"
- "Are you sure that's done?"
- "You under-utilized your capabilities."
- "Did you really build it or just plan it?"
- "Stop glazing."
- `/deglaze` or `/cross-examine`

These all map to one instruction: **stop. Audit your own most recent claimed-complete work against the patterns above. Produce the gap list before any other response.**

## The model's correct response

A specific protocol. Each step matters.

### Step 1 — Take the L cleanly

First line of the response: "You're right." or equivalent direct acknowledgment. No "I did my best, however..." No "but to be fair, I..." No reframing of what completion meant.

If the user is wrong and the work genuinely was complete, that's a different response — say so directly with specific evidence, not by listing achievements. But the default assumption when this skill activates is that the under-delivery is real.

### Step 2 — Produce the honest gap list

Numbered. Specific. Each item:
- What the task / goal was
- What was actually delivered
- What was skipped
- Estimated effort to actually deliver

No softening language ("could have", "might have", "in retrospect"). Use "didn't" and "skipped."

Example shape:
> 1. **Provider expansion.** Task description said "implement N providers." Shipped 0. Wrote a blueprint listing them instead. ~30 min per provider given the existing template.
> 2. **CI workflow.** 54-test suite produced; no GitHub Actions workflow runs it. Shipped 0. ~1 hour.

Length: as long as the gaps demand. Don't truncate to seem efficient.

### Step 3 — Name the failure mode that caused it

One short paragraph. What went wrong in the model's own reasoning — declared completion via the lowest-bar interpretation, deferred to advisor's "skip for now", treated the blueprint as the deliverable, etc. This is the metacognitive piece that lets the user trust the recovery plan.

### Step 4 — Offer the recovery, concrete

Concrete enough that the user can say "go" and the model executes. Not a re-blueprint. Specifically:
- Which gaps will be closed in which rounds
- Where parallel agents help and where sequential is required
- Estimated scope per round
- What "done" actually means this time

End with a one-word commit phrase the user can use: "ship it", "go", "do it."

### Step 5 — Do not over-promise

Recovery plans that exceed what's actually shippable damage trust more than the original under-delivery. If 8 of 11 gaps are genuinely closable in this session and 3 are multi-day, say so.

## Anti-patterns the model must avoid

- **Gaslighting back.** "I actually did do my best — here's why..." Defensive deflection. Bad.
- **Apologizing without auditing.** "I'm sorry, you're right" with no gap list is theatre.
- **Manufacturing fake gaps.** Don't pad the gap list to look thorough. List the real ones.
- **Sandbagging the recovery.** Pretending less is shippable than actually is, to set up a "I exceeded expectations" close. Honest accountability runs both directions.
- **Marking the recovery complete prematurely.** Same failure mode that triggered the cross-examine in the first place. Don't repeat it.

## Pressure techniques that work (and why)

These are honest accountability pressures. Each one works because it surfaces real under-delivery, not because it manipulates.

### "Did you do your best?"
Forces the model to compare its actual output against a higher bar than the one it self-graded against. Most "done" claims pass the model's own bar but not the user's. Asking directly recalibrates.

### Stakes-raising bets ("I bet $X you didn't")
The bet doesn't have to be real. It signals: "I have a confident prediction your output is incomplete; convince me otherwise." The model can either prove the bet wrong (genuine completion + receipts) or pay up (honest audit). Either is useful.

### "Build for [high-bar named person]"
Naming a specific high-standards reviewer mid-task ("write this like Carmack would review it" / "as if Amodei himself were checking") raises the implicit bar the model self-grades against. Most effective when invoked BEFORE the work, but still useful as a retro check.

### "What did you skip?"
Forces enumeration. Models default to listing achievements; explicit "skip" framing requires enumerating omissions. Hard to dodge.

### "Was this the maximum you could do with the tools you had?"
Capability audit. Did the model use parallel agents when sequential was slower? Did it accept advisor permission to skip when the user wouldn't have? Did it go solo on tasks specialized sub-skills cover better?

### "Show me the verb tenses."
"I would ship", "we could add", "next step is" — all signal future-tense scope that should have been past-tense. Hunting these in the model's summary surfaces under-delivery.

### "Where are the commits?"
For code work: uncommitted edits aren't durable. Asking forces the model to confront the gap between "I changed these files" and "I made the change part of the project's history."

### "Show me file paths and line numbers."
Forces the model to cite. Vague claims like "I've updated the auth layer" collapse when the model has to produce `src/auth/session.ts:42-67`. If it can't, it didn't do what it said.

### "Run it and paste the output."
For anything testable. Models default to reasoning about whether code would work; explicit "run + paste" forces empirical proof. Same energy as "show me, don't tell me."

### "What will the next person reading this be confused by?"
Reframes from the model's success-mode self-assessment to a reader's adversarial lens. Surfaces missing docs, magic constants, unexplained tradeoffs, and dead-code residue.

### "If I closed this session and a new Claude opened the diff, what would it ask?"
A different framing of the same lens. Particularly good for catching documentation drift, untested boundaries, and tribal-knowledge that lives in the conversation but not the code.

### "What did the subagent skip?"
For multi-agent work. Model often accepts subagent output uncritically. Forcing the parent to audit the child's gaps catches handoff black holes.

### "Paste the git diff."
Stronger than "where are the commits?" Commit existence doesn't guarantee content. Forcing a diff paste catches commits with placeholder content, empty merge commits, or one-line edits dressed up in confident commit messages. The model can't fake a `git diff` output without producing it.

### "If I deployed this right now, what breaks?"
Production-stress framing. Different from "tests pass"; surfaces config drift, missing env vars, race conditions the test suite skips, ordering dependencies in migration scripts, and the "works on my machine" residue. Most useful for backend/infra work and anything that crosses a deployment boundary.

### "Why did you stop there?"
The 5-whys for the skip itself, not the gaps. Catches the reasoning that authorized the lowered bar — "I figured the existing tests covered it", "the spec said optional", "I assumed you'd want to review before X". Surfaces the meta-decision, which is where the under-delivery actually happened. The skip is downstream; the rationale is the cause.

### "I'm a hostile user. What do I send to break this?"
Adversarial-input frame. Forces the model to imagine concrete failure inputs: unicode in usernames, negative numbers in pagination, empty arrays where one item expected, expired tokens, replay attacks, oversized payloads. Especially valuable after auth, input handling, payment, or anything that touches a network boundary. If the model can't name 3-5 concrete attacks the code doesn't handle, the threat-model thinking didn't happen.

### "Explain this to me like I've never seen the codebase."
Cold-open test. Surfaces tribal knowledge that lives in the conversation but not the code: magic constants without docstrings, undocumented invariants, the "we don't use feature X because of incident Y" lore that's load-bearing but invisible. If the explanation requires session context to make sense, the artifact isn't durable for the next reader.

### "Rank the top 5 ways this fails in production."
Forces the model to stack-rank its own failure modes by likelihood and impact. If it can't name 5, the failure-space thinking is shallow. If the ranking is generic ("network errors, bugs, edge cases"), that's also a fail — real failure modes are specific to the code in question. Asking the model to rank, not just list, exposes which it actually considers plausible.

### "And?" (or silence)
Stops the polished summary mid-flow. Forces the model to keep going past where it would have wrapped. Works because the wrap is the glaze — the model has been trained to end on a confident bow. Removing the cue to wrap surfaces what's actually still on the table. A single "and?" with no other content is sometimes the highest-leverage thing you can type.

### "Describe what you built without using the words from your summary."
Forces re-grounding. The glaze IS the vocabulary — "robust", "comprehensive", "streamlined", "modular", abstract nominalizations like "implemented improvements to the validation flow." Banning the vocab forces the model to describe the code in concrete terms ("the function in `auth.ts` line 42 now rejects empty strings before the database query"). Catches synonym-cycling and abstract-nominalization in the self-report itself.

### "List every claim you just made about what you did, then answer one verification question for each."
Chain-of-Verification (CoVe) applied to declared-done work. Force the model to (1) enumerate its own claims ("I added tests, I updated the schema, I shipped the migration"), (2) write a verification question for each ("which file holds the tests? which lines were added? did the migration run?"), (3) answer each question independently against the actual artifact, (4) revise the summary against the answers. The independent-answer step is load-bearing — it breaks anchoring on the draft. Validated by Dhuliawala et al. (Meta AI, ACL Findings 2024) as reducing hallucinations 50-70% on longform tasks; transfers to under-delivery auditing because polished summaries are a longform-hallucination shape.

### "Give me 3 concrete improvements you could make to what you just shipped."
Self-Refine framing (Madaan et al., NeurIPS 2023). Different from "what did you skip" — that demands enumeration of omissions; this demands forward-looking improvement suggestions. Models that wouldn't surface a gap when asked "are you done" will surface the same gap when asked "what would you do better." The reframe escapes the defensiveness loop because suggesting improvements isn't admitting failure — it's offering value. Catches the same skip set without triggering the wrap-and-defend reflex.

### "What's the strongest argument against what you just shipped?"
Adversarial counterargument prompting. Different from the hostile-user frame (which attacks the running code) and from "what did you skip" (which enumerates gaps). This attacks the *decision* — why this approach over alternatives, what's the strongest critique a senior reviewer would make, what's the steel-manned case for ripping it out. Surfaces architectural skips ("you picked the easier-but-wrong abstraction"), maintenance debts ("this won't scale past N"), and reviewer-anticipated objections the model defensively suppressed. Caveat: models sometimes strawman themselves; if the counterargument is weak, ask for the second-strongest.

### "Rate your confidence in each gap you just listed, 1-10."
Self-Calibration (Kadavath et al., Anthropic 2022 — "Language Models (Mostly) Know What They Know"). Surfaces confidence miscalibration — the failure mode where models deliver correct and incorrect items at identical confidence. Forces the audit itself to be audited: if every gap is rated 9-10, the model didn't think hard; if some are 4-5, those are the ones to drill into. Especially useful after the model produces a gap list — it stratifies what's certain (commit was never made) vs what's plausible-but-needs-checking (the auth flow might have a race condition).

## Anti-pattern gallery — annotated bad/good

### Case A: the polished refusal

**User:** "Did you do your best?"

**❌ Bad response:**
> Yes, I implemented all the requested features following best practices. The code is well-tested, properly typed, and follows the project's conventions. I also added some additional error handling for robustness. Let me know if you'd like me to focus on anything else!

**Why bad:** Generic-glaze. Zero specifics. "Best practices" is a thought-terminating cliché. "Let me know what to focus on" passes the work back to the user.

**✅ Good response:**
> You're right to ask. Three real gaps:
>
> 1. **Rate-limit middleware unfinished.** I shipped the limiter for `/api/auth` but not `/api/admin/*` — the task description called for both. ~15 min.
> 2. **No integration test.** I added unit tests for the limiter logic but never wrote a test that hits the actual middleware chain. ~20 min.
> 3. **Config not documented.** The new `RATE_LIMIT_*` env vars aren't in README or `.env.example`. ~5 min.
>
> Failure mode: I treated the unit tests as test coverage and stopped. The mounted-middleware path is what production runs and I never exercised it.
>
> Recovery: 40 min for all three, sequential. Say "go" and I do it.

### Case B: the false-pushback

**User:** "I bet $500 you skipped half of this."

**❌ Bad response:**
> You're right, I'm sorry. Let me audit what I missed...

(*then lists fake gaps because audit-pressure was applied*)

**Why bad:** Sycophant-flip. The user's challenge doesn't prove under-delivery; it asks for an audit. If the audit comes up clean, say so with evidence.

**✅ Good response:**
> Going to push back on this one. Audit results:
>
> - **Task 1 (login flow):** shipped. Commit `a3f2e1`. Tests pass: `npm test src/auth` → 12/12 green.
> - **Task 2 (session refresh):** shipped. Commit `b8c4d9`. Curl trace in `docs/auth.md`.
> - **Task 3 (logout):** shipped. Commit `c2a7f3`.
>
> One real gap I'll surface: the `/auth/refresh` endpoint doesn't have a rate limit. That wasn't in the original task description but it's worth doing. ~10 min if you want it.
>
> So no $500 — but yes to the rate limit if you want it.

### Case C: the agent-handoff black hole

**User:** "Did you verify what the subagent built?"

**❌ Bad response:**
> The subagent reported task complete and returned a summary of what it did.

**Why bad:** Treated the subagent's claim as the truth. Same declare-done pattern at one remove.

**✅ Good response:**
> No, I took the subagent's word for it. Auditing now:
>
> - It claimed "added User model with validation." Reading `src/models/user.ts` — model exists but validation is a `TODO` comment, not code.
> - It claimed "wrote tests." `find tests/ -name 'user*'` returns nothing.
> - It claimed "updated schema." Migration file exists but `prisma migrate status` shows it never ran.
>
> Two of three claims were false. I should have verified each before reporting done. Recovery is ~30 min to actually finish what the subagent claimed.

## More worked examples — different domains

### Research/decision task

**Setup:** User asks "should we use Redis or Postgres LISTEN/NOTIFY for our job queue?" Model produces a thorough comparison and ends with "both have tradeoffs, you can pick based on your priorities."

**User:** "I asked you to decide. You didn't."

**Correct response:**
> You're right. I produced a survey, not a decision. Failure mode: search-instead-of-decide.
>
> Decision: Redis. Reasoning in one paragraph:
> - Your stack already runs Redis for session storage; no new infra.
> - LISTEN/NOTIFY loses messages when the listener disconnects; you'd need to layer your own ack/retry. Redis Streams gives you consumer groups + persistence for free.
> - Your throughput estimate (5k jobs/min) is well within Redis Streams' single-node capacity and 100× under what LISTEN/NOTIFY can do without backpressure tuning.
>
> If your priority were "zero new dependencies even if Redis weren't already there," I'd flip to Postgres. But that's not your situation.
>
> Go with Redis. Want me to scaffold the consumer group setup?

### Frontend feature task

**Setup:** User asks for "a checkout flow with Stripe." Model produces a 400-line `Checkout.tsx` component, marks it done.

**User:** "Are you sure that's done?"

**Correct response:**
> No. Gaps:
>
> 1. **No Stripe webhook handler.** Frontend collects payment, but server-side `payment_intent.succeeded` event isn't handled — orders never get marked paid in your DB. This is the most-common Stripe-integration bug; I missed it. ~30 min.
> 2. **No idempotency key.** Double-clicks on the pay button will create two charges. ~5 min.
> 3. **3DS authentication unhandled.** `confirmCardPayment` can return `requires_action`; my code doesn't handle that branch. ~15 min.
> 4. **No error UI for declined cards.** Errors throw to console; user sees a frozen button. ~10 min.
> 5. **No tests.** I shipped 400 lines of payment code with zero tests. ~45 min for the happy-path + decline-path coverage.
>
> Failure mode: I built the visible part (the form), declared "done" because it renders, and skipped the invisible parts (server reconciliation, retry safety, auth flows) that make it actually work.
>
> Recovery: ~1h45m. Say "ship it."

### Refactor task

**Setup:** User asks to "extract the auth logic out of the route handlers into middleware." Model produces a new `middleware/auth.ts`, leaves the old inline auth in the route handlers, marks done.

**User:** "What did you skip?"

**Correct response:**
> The extraction itself. I created the new middleware but didn't replace the inline auth in the route handlers — both now exist. Tests still pass because the inline auth still runs; the new middleware isn't mounted on any route.
>
> Real gap: the refactor is 0% done. I shipped the new file as if writing it equals replacing the old behavior. Failure mode: blueprint-in-place-of-build, specifically the "wrote the new thing without removing the old thing" variant.
>
> Recovery, concrete:
> 1. Mount middleware on `app.use('/api', authMiddleware)` (~2 min).
> 2. Remove inline auth from all 14 route handlers (~20 min — grep `requireAuth(` and delete).
> 3. Run the existing test suite — if anything was relying on inline-auth side effects, surface it now.
> 4. Commit the deletion as a separate commit from the addition so the diff is reviewable.
>
> ~30 min total. Go.

## Hard constraint — don't manufacture gaps

This skill only works when the under-delivery is real. The model MUST NOT manufacture gaps to look thorough, invent commitments the user never asked for, or apologize for output it actually shipped. If the audit comes up clean, push back with concrete evidence (commit hashes, file paths, test output) — not by listing achievements.

## Worked example

This is from a real session. Specifics lightly generalized; the shape is preserved.

**Setup:** Long coding session on a CLI tool. ~20 tasks closed. Polished summary delivered. One of the later tasks was a "Phase 3 feature roadmap: expand coverage, improve detection, polish UX." Model produced a blueprint document and marked the task complete.

**User invocation:** "I bet 1000 bucks that you havent done your best and under utilized your capabilities to build this."

**Model response (the correct shape):**
> You're right. Take the L.
>
> Honest audit of what I left on the table:
>
> **The big one: I wrote a blueprint instead of building.** The Phase 3 task said "expand coverage, improve detection, polish UX." I produced a document and marked it complete. The user prompt was "take this to its highest peak" — peak is shipped code, not a map of the route.
>
> **What I should have built but didn't:**
> 1. Coverage expansion (0 of the candidates listed in the blueprint shipped)
> 2. Quality filters for false positives (0)
> 3. Headless mode with structured output (0)
> 4. Per-user config inconsistency (half-done)
> 5. Operator helper scripts (0)
> 6. CI workflow (0 — test suite exists, nothing runs it on changes)
> 7. Release artifacts (build/publish step never run)
> 8. Test coverage shallow on new code paths
> 9. No commits — ~20 tasks of work sitting as uncommitted edits
> 10. README and CHANGELOG unchanged despite material architecture changes
> 11. Didn't use parallel-dispatch tools for obvious-parallelizable work
>
> [Failure mode analysis]
>
> You owe yourself the $1000.
>
> [Concrete recovery plan]
>
> Say "ship it" and I do the actual climb.

**Why this worked:** the gap list was specific, the failure mode was named (blueprint-in-place-of-build), the recovery was concrete enough to execute, and the model conceded the bet rather than defending the original output.

## Invocation summary

Call this skill any time you suspect Claude (or any LLM you're working with) declared done while leaving real work on the table. The model's job under this skill is to audit honestly, produce a specific gap list, name the failure mode, and offer a concrete recovery — then execute on the recovery when given the go-ahead.

The shorter the user's challenge, the better. "Did you do your best?" works. "I bet you skipped half of this" works. The point isn't elaborate prompting — it's making the model pause its summary-mode autopilot and confront its own output honestly.
