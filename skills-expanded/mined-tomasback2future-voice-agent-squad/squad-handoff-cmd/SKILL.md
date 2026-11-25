---
name: squad-handoff-cmd
description: End-of-session 3-bullet brief plus claim release. Invokes the squad-handoff skill.
argument-hint: ""
allowed-tools:
  - Bash
  - Edit
paths:
  - ".squad/**"
disable-model-invocation: true
---

You are wrapping up the session. Invoke the `squad-handoff` skill, then post the 3-bullet brief:

1. **Shipped:** items closed (by ID + one-line outcome). If nothing closed, say "nothing closed."
2. **In flight / queued:** what is `in_progress` or `review` and where it stands. If clear, say "queue clear."
3. **Surprised by:** anything the next session should know that is not in an item file or commit message. Skip the bullet if there is genuinely nothing.

If you are pausing mid-item:
- Leave the claim open.
- Add a `## Session log` entry to the item file with what you did, what is left, gotchas, and the next concrete step.
- Post `squad say "end of session, picking up <next step> tomorrow"`.

If you are truly handing off to another agent:

```bash
squad release $ARGS --outcome released
```

And name the next concrete step in the release message.

After posting the brief, sign off.
