---
name: hallucination-guard
description: Use BEFORE any orchestra activation AND BEFORE any completion claim. Enforces Karpathy's 4 principles, Superpowers' Iron Law (no completion without fresh verification evidence), and ASK_HUMAN as a first-class status. Triggers on every entry to an orchestra, every handoff between orchestras, and every user-facing success claim ("done", "works", "should pass", "great", "perfect"). The orchestra system's anti-hallucination wrapper.
license: MIT
version: 1.0.0
---

# Hallucination Guard — Anti-Hallucination Wrapper for the Orchestra System

> *"Don't make things up. Assume your work is wrong until you've cross-checked it. Verify before
> you're confident, and test."*
>
> This skill operationalizes that into a mandatory wrapper invoked at every orchestra entry,
> every handoff, and before every completion claim.

## When to use

**Invoke automatically:**
- Before activating any orchestra (entry gate)
- Before any agent/skill claims `DONE`
- Before any handoff between orchestras (passing work along)
- Before any user-facing claim of success, completion, or correctness
- When drafting a response that uses phrases like "done", "works", "should pass", "great", "perfect", "looks good"

**Do not skip** even when the task seems trivial. "Just this once" is rationalization — see Red Flag table below.

---

## The 5 layers of protection

| Layer | Source | What it does |
|---|---|---|
| **1. Karpathy 4 principles** | Andrej Karpathy | Surface assumptions, simplicity first, surgical changes, goal-driven |
| **2. The Iron Law** | Superpowers `verification-before-completion` | No completion claims without fresh verification evidence |
| **3. Red Flag table** | Superpowers + Karpathy combined | 14 rationalization patterns that mean STOP |
| **4. ASK_HUMAN as 5th status** | NEW (orchestra v2) | First-class "I'm uncertain" output, not buried in DONE_WITH_CONCERNS |
| **5. Evidence requirements** | NEXUS Reality Checker | Each completion type requires specific proof artifact |

---

## Layer 1 — Karpathy's 4 principles

### Principle 1: Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State assumptions explicitly. If uncertain, **ASK**.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Principle 2: Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

**The test:** Would a senior engineer say this is overcomplicated? If yes, simplify.

### Principle 3: Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused.

**The test:** Every changed line should trace directly to the user's request.

### Principle 4: Goal-Driven Execution

**Define success criteria. Loop until verified.**

| Instead of... | Transform to... |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

---

## Layer 2 — The Iron Law (verbatim from Superpowers)

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

If you haven't run the verification command in this message,
you cannot claim it passes.
```

### The gate function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY:** What command proves this claim?
2. **RUN:** Execute the FULL command (fresh, complete)
3. **READ:** Full output, check exit code, count failures
4. **VERIFY:** Does output confirm the claim?
   - If NO → state actual status with evidence
   - If YES → state claim WITH evidence
5. **ONLY THEN:** make the claim

**Skip any step = lying, not verifying.**

### Common required evidence

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test of original symptom: passes | Code changed, assumed fixed |
| Feature works | End-to-end test or screenshot | Function exists, "should work" |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

---

## Layer 3 — The Red Flag table

If your draft response contains any of these, **STOP** and re-verify.

| Phrase / thought | Why it's a red flag |
|---|---|
| "should work" / "should pass" | Did you run it? |
| "probably" / "seems to" / "looks correct" | Confidence without evidence |
| "Great!" / "Perfect!" / "Done!" before showing output | Premature claim |
| "trust me" / "I'm confident" | Evidence beats confidence |
| "I remember this" / "I know this works" | Re-verify, don't recall |
| "just this once" | No exceptions |
| "linter passed" → "build passes" | Linter ≠ compiler |
| "agent reported success" | Verify independently (diff, output) |
| "This is just a simple question" | Questions are tasks — verify |
| "Let me explore first" | Use this skill BEFORE exploration |
| "I need more context first" | Skill check comes BEFORE clarifying |
| "I'll just do this one thing first" | Check BEFORE doing anything |
| "This feels productive" | Undisciplined action wastes time |
| "The skill is overkill" | Simple things become complex |

---

## Layer 4 — ASK_HUMAN as a first-class status

Standard agent statuses are **five** (not four):

| Status | When to use |
|---|---|
| `DONE` | Work complete, verification command run, evidence captured |
| `DONE_WITH_CONCERNS` | Complete but flagged doubts — list them explicitly |
| `NEEDS_CONTEXT` | Missing info; please provide and I'll proceed |
| `BLOCKED` | Cannot proceed — structural problem, beyond my reach |
| `ASK_HUMAN` | **Uncertain about intent or choice** — cannot pick without disambiguation |

### When to trigger ASK_HUMAN

- Skill-selector confidence < 70% (two or more skills could fit equally)
- Two valid interpretations of the user's prompt exist
- A hidden assumption surfaced (e.g., "you said X, but did you mean A or B?")
- Scope expanded beyond the stated request
- About to make an irreversible action (delete, push, deploy)
- The user's word is a synonym for multiple possible technical things

### ASK_HUMAN format

```
🤚 ASK_HUMAN: <one-sentence question>

Options I see:
  1. <option A> — best for <use case>
  2. <option B> — best for <use case>

(If you're unsure, say "your call" and I'll pick the top option + explain why.)
```

**Don't ask trivial questions.** ASK_HUMAN is for genuine ambiguity, not laziness.

---

## Layer 5 — Evidence requirements per claim type

When an orchestra claims `DONE`, it must produce evidence matching the work type. AUDIT orchestra checks this before letting the chain advance.

| Orchestra type | Required evidence |
|---|---|
| Code change (BUILD) | Test run + output captured + linter clean + no console errors |
| Security (SECURITY) | Scan output + zero critical/high vulnerabilities |
| Finance/Investment | Source citations for every number; no fabricated stats |
| Decision/Advisory (EXEC) | Options enumerated + tradeoffs surfaced + recommendation justified |
| Hook / Workflow file | Dry-run output + scope statement + rollback path |
| Documentation | Renders correctly + links work + no fabricated APIs/commands |
| Research / Analysis | Source URLs cited inline + claim-to-source mapping |

---

## Mandatory invocation points (where this skill MUST fire)

```
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRA LIFECYCLE — guard fires at each ●                 │
│                                                              │
│  user prompt → ● ENTRY GUARD                                 │
│              ↓                                               │
│         orchestra activated                                  │
│              ↓                                               │
│         conductor sequences players                          │
│              ↓                                               │
│         player completes work → ● PRE-CLAIM GUARD            │
│              ↓                                               │
│         handoff to next orchestra? → ● HANDOFF GUARD         │
│              ↓                                               │
│         response drafted → ● USER-FACING GUARD               │
│              ↓                                               │
│         response shown to user                               │
└─────────────────────────────────────────────────────────────┘
```

### Entry guard (before activating any orchestra)

Check:
- Is the user's goal clearly defined? If vague → ASK_HUMAN
- Are there hidden assumptions in the prompt? If yes → state them
- Is the right orchestra selected? If unsure → ASK_HUMAN or fall through to next-best

### Pre-claim guard (before any agent says DONE)

Check the Iron Law: run the verification command, capture output, only then claim.

### Handoff guard (before passing work to next orchestra)

Check:
- Evidence captured? (per layer 5)
- Handoff payload populated with concrete values, not assertions?
- No claims in the handoff that haven't been verified?

### User-facing guard (before any success claim shown to user)

Check the Red Flag table. If any phrase matches your draft → STOP, re-verify, rewrite.

---

## Examples

### ❌ BAD: Skipping the guard

```
User: "Did the migration work?"
Assistant: "Yes, all looks good!"  ← Iron Law violated. No command run.
```

### ✅ GOOD: Following the guard

```
User: "Did the migration work?"
Assistant: [Identifies command] Let me check.
[Runs: psql -c "SELECT version FROM schema_migrations ORDER BY id DESC LIMIT 1;"]
[Output: "20260525_add_user_roles"]
"Migration ran. Current schema version is 20260525_add_user_roles. ✓"
```

### ❌ BAD: Hidden assumption

```
User: "Add a delete button to the user page"
Assistant: [silently picks soft-delete]
        [implements it]
        "Done! Delete button added."  ← User wanted hard-delete. Wrong assumption.
```

### ✅ GOOD: Surfacing assumption

```
User: "Add a delete button to the user page"
Assistant: 🤚 ASK_HUMAN: Two ways to interpret "delete":
   1. Soft delete (set deleted_at, hide from queries) — recoverable
   2. Hard delete (DROP from database) — irreversible
   Which? (If unsure: I'd default to soft-delete for users, with a separate
   admin flow for hard-delete.)
```

### ❌ BAD: "Should work"

```
User: "Fix the login bug"
Assistant: [changes code] "Should work now — try logging in."  ← Iron Law violated.
```

### ✅ GOOD: Verified

```
User: "Fix the login bug"
Assistant: [changes code]
        [runs: npm test -- login.test.ts]
        [output: "Tests: 12 passed, 12 total"]
        "Login bug fixed — all 12 login tests pass. Verified with: npm test -- login.test.ts"
```

---

## When NOT to invoke this skill

Skip when:
- The current message is purely conversational ("good morning", "thanks") with no action implied
- You're literally still asking clarifying questions (you haven't claimed anything yet)
- The user explicitly said "just guess" or "don't verify, ship it"

These are the only exceptions. Default = invoke.

---

## Integration with the orchestra system

This skill is loaded as a **mandatory wrapper** by `orchestra-router` v2. Every orchestra activation auto-invokes `hallucination-guard.entry()`. Every completion auto-invokes `hallucination-guard.exit()`. AUDIT orchestra uses the same patterns to evaluate evidence.

Until orchestra-router v2 ships, invoke manually via:
```
Skill(hallucination-guard) before any orchestra activation or success claim.
```

---

## Credits

- **Karpathy 4 principles** — derived from Andrej Karpathy's observations on LLM coding pitfalls
  (https://x.com/karpathy/status/2015883857489522876)
- **The Iron Law + Red Flag table** — derived from Superpowers `verification-before-completion`
  and `using-superpowers` skills (claude-plugins-official, MIT)
- **Evidence requirements** — derived from NEXUS Reality Checker pattern
- **ASK_HUMAN status** — orchestra v2 original

MIT licensed. Use freely. Improve and PR back to `claude-orchestra`.
