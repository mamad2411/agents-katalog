---
name: cyc-frame
description: "Turn a request into a destination, scope, and acceptance criteria someone could check, interviewing the user only on real decisions. Use at the start of a task, when the request is vague, or when feedback shows the goal was misunderstood."
---

# Frame the work

Name the destination before choosing the road. A good frame lets another skill say what "done" means without guessing. Use the [handoff contract](../../docs/skill-contract.md) inside a CYC chain.

## The core loop

1. **Name the destination in one sentence, in the user's words.** "A student can mark homework finished and it stays finished after refresh." Keep their chosen mechanism unless it cannot reach the destination; if so, say why.
2. **Set the quality bar at excellent.** Write what excellent looks like in *this* codebase for this task: its conventions, test style, error handling, and performance expectations. Name the shortcuts that would fall short of it (the tells a senior reviewer would reject), and what must survive every revision. Some of this only becomes clear after the user sees a draft; when it does, raise the bar here.
3. **Name the stage.** Exploring an idea, choosing an approach, building, or evaluating. "What do you think about X?" is exploring. Do not build it.
4. **Look up facts yourself; ask the user only for decisions.** Existing storage, frameworks, and conventions are facts: read the code or send a subagent. Whether finished items hide or move is a decision: ask.
5. **Ask the frontier, not a questionnaire.** The frontier is every open decision whose prerequisites are settled. Ask all of them in one numbered round, each with your recommended answer and a one-line reason, so the user can reply "yes to all" or change one. Stop when the frontier is empty or the remaining choices are cheap to reverse.
6. **Write acceptance criteria as checks.** Each criterion is observable: "After reload, the assignment still shows as finished." Include preserved behavior ("Adding homework still works"). No invented numbers for taste; mark those "user judgment".
7. **Write the out-of-scope list.** Name the tempting extras you are not doing (accounts, sync, reminders). This protects scope better than a vague "keep it small".

## Done when

- The destination sentence and the quality bar exist.
- Every criterion could be marked pass or fail by someone reading the result.
- There is at least one preserved-behavior criterion and an out-of-scope list.
- No open question remains that would change the solution; cheap choices were made and stated as assumptions.

## Question format

```text
1. Should finished homework disappear or move to a "Finished" section?
   Recommended: move to a collapsed section. Hiding makes accidental clicks unrecoverable.
2. Persist per browser (current localStorage) or per account?
   Recommended: per browser. The app has no accounts yet.
```

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Interrogation | Asking the user where the save code lives | Read the code |
| Drip questions | One question per turn over five turns | Ask the whole frontier at once |
| Menu without a pick | "Option A or B?" with no recommendation | Recommend one, give the reason |
| Mechanism swap | User asked for a button, frame says "keyboard shortcut" | Keep their mechanism or explain the conflict |
| Bare minimum bar | Criteria only say "it works" | Add what excellent looks like in this codebase |
| Vibe criteria | "Works well", "clean UI" | Rewrite as an observation, or mark user judgment |

## Handoff

Pass the destination, quality bar, stage, criteria (with stable IDs), preserved behaviors, out-of-scope list, assumptions, and user decisions to [Understand](../cyc-understand/SKILL.md). If feedback later shows the frame was wrong, update it here, keep the failed criterion on record, and name which downstream work is now invalid.
