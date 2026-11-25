---
name: complete-stage
description: Run declared deterministic Validators and record the only legal route after a CodeBuddy Stage Agent returns.
---

# Complete Stage

Require the absolute Workspace path, active Workflow, and current Stage. First
inspect the returned Task's owned outputs and Handoff, then record the durable
output return:

```powershell
python scripts/stage_control.py record-output --workspace <workspace> --workflow <workflow> --stage <stage>
```

Then evaluate exactly its declared Validator bindings:

```powershell
python scripts/stage_control.py evaluate --workspace <workspace> --workflow <workflow> --stage <stage>
```

Interpret the exit code and persisted Status only. `FAIL` means redispatch the
same producing Stage with its persisted Repair Findings. `ERROR` means stop at
the recorded blocker. `PASS` advances only to the route emitted by the helper;
run `authorize` again before creating that Stage's display Task and dispatching
its child Agent, whose start Hook will claim it. Never use a CodeBuddy Task or
child-Agent completion message as proof that the Stage is valid.
