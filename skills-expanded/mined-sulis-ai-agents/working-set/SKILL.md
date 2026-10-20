---
name: working-set
description: Maintain the live reasoning-state Working Set for a change — the agent triggers this to keep current thinking (problem / solution / decisions, and the *why*) durable across turns and session boundaries.
---

# Working Set — keep the thinking durable, not in the scrollback

## Conclusion (what this is, lead-with-the-answer)

The Working Set is a small file that holds the **current state of thinking** on a
change — the problem, the leading solution, the decisions in flight, and (the part
that usually gets lost) the **rejected alternatives + the why**. The agent keeps it
current *as a side-effect of working*, so when a session ends — cleanly or abruptly —
the next session reloads the thinking instead of reconstructing it from a long
conversation that has drifted. It is the staging area that crystallizes into the
durable brain entities (Opportunity / Design / Decision) at the session boundary.

It lives at `{repo-root}/.changes/{primitive}-{slug}.WORKING-SET.md`, beside the
change's other artifacts (SPEC, RECON, scenarios). Full rationale:
`../../docs/working-set-and-session-chain.md`.

## The one rule that makes or breaks it

**Read it at the START of every turn; update it the moment a decision is made.**
"Living documents" die when updating them is a separate chore with no immediate
payoff. This one survives only because reading it *is* how the agent re-grounds each
turn, and updating it *is* part of making a decision — never a documentation task
done later. **If it isn't being read every turn, it isn't doing its job.**

## When to invoke (the three moments + the section edits)

1. **At the start of a change/session — `init`.** Create the six-section Working Set
   from the template (idempotent — never clobbers an existing one). Seed the Problem
   from the change intent:
   ```bash
   "$SCRIPTS_DIR/sulis-working-set" init --stem {primitive}-{slug} \
     --repo-root <repo-root> --intent "<one-line problem framing>"
   ```
2. **At the start of every turn — `show`.** Re-ground in the locked thinking before
   doing anything else:
   ```bash
   "$SCRIPTS_DIR/sulis-working-set" show --stem {primitive}-{slug} --repo-root <repo-root>
   ```
3. **As thinking moves — edit the file directly** (these need judgement, so the agent
   does them with `Edit`, not a CLI):
   - reframed the problem → rewrite **§1 Problem**
   - the leading approach shifted → rewrite **§2 Current best solution**
   - weighing a non-trivial choice → add/append **§3 Decisions in flight** (the choice,
     options, rejected alternatives + rationale, status `proposed`)
   - hit an unknown → add to **§4 Open questions**
   - abandoned a path → add to **§5 Rejected so far** *with the why*
   Then drop a one-line marker in the append-only log:
   ```bash
   "$SCRIPTS_DIR/sulis-working-set" log --stem {primitive}-{slug} \
     --repo-root <repo-root> --message "locked the auth approach: session cookie over JWT"
   ```
4. **At the session boundary — crystallize.** Distil the mutable sections into the
   durable brain entities: §1 → Opportunity, §2 → Design, §3/§5 → Decision (a
   `proposed` choice that locked becomes an `accepted` Decision carrying its rejected
   alternatives + rationale), unresolved items → the relevant entity's open-questions.
   *Until the Decision entity carries `rejected_alternatives`/`rationale`/`open_questions`
   natively (a queued source-ontology change), record the why in the Decision body and
   keep the Working Set as the carry-forward.* If the session ends without
   crystallizing, the file itself **is** the handoff — the next session's `show` reads it.

`$SCRIPTS_DIR` resolves the same way as the other wpx-*/sulis-* tools (find the
plugin's `scripts/` dir; dev fallback `plugins/sulis/scripts`).

## When NOT to invoke

- A trivial change (CW-05): a typo, a one-line config fix — no reasoning to track.
- A pure read/inspection turn with no decisions in play.
- When there's no change in flight (the Working Set is change-scoped; use `--path`
  for a one-off session-scoped file if you genuinely need one).

## The six sections

| § | Section | Holds | Write mode | Crystallizes → |
|---|---------|-------|-----------|----------------|
| 1 | Problem | situation / complication / question | overwrite | Opportunity |
| 2 | Current best solution | the leading approach right now | overwrite | Design |
| 3 | Decisions in flight | each choice being weighed + options + status | overwrite | Decision |
| 4 | Open questions | the live unknowns parking lot | overwrite | → §3 / entity open-questions |
| 5 | Rejected so far | abandoned paths **with the why** | overwrite | Decision.rejected_alternatives |
| 6 | Working log | timestamped "what changed + why" | **append-only** | — (history) |

Sections 1–5 are current-state (overwritten as thinking moves); section 6 is
append-only (never edited — it's the audit trail).

## Gotchas

- **Read-every-turn or it rots.** This is the whole game (see "The one rule"). A
  Working Set that's written but not read is worse than none — it looks like the
  thinking is captured when it isn't.
- **`init` never clobbers.** Re-running `init` on an existing Working Set leaves it
  untouched (`created: false`). Safe to call at every session start.
- **Don't edit the log by hand.** Section 6 is append-only via `log`; rewriting it
  destroys the audit trail. Sections 1–5 are the ones you overwrite.
- **The *why* is the point.** §5 (rejected + rationale) is the bit that's always lost
  at a handoff. If you abandon a path, record *why* — that's what stops the next
  session re-litigating it.
- **It's a staging area, not a second SPEC.** It holds *current reasoning state*,
  distinct from SPEC.md (*what to build*) and the run journal (*what happened*). It
  crystallizes into the brain entities; it isn't the permanent home.

## See also

- `../../docs/working-set-and-session-chain.md` — the spec + the chain-of-sessions model.
- `../../scripts/sulis-working-set` — the helper (init / show / log).
