---
name: solidworks-procedure
description: Create a procedure skill from this conversation. Use when the user says "Create a procedure skill named NAME from this conversation."
---

# SolidWorks procedure

The user will name the skill in one sentence. Read the name after "named". `set material` or `set-material` both become `set-material`. Then write that skill from this conversation. Ask nothing else.

## What to keep

Walk the tool results in this chat, in order.

- Keep a call whose result succeeded.
- Keep a read only when the next kept write used its handle or its returned value.
- Keep argument names as the tool schema spells them.
- One successful write is one step. Several successful writes are several steps, in the order they ran.

Drop `search_api`, `describe_api`, `lookup_api_help`, `capture_view`, `set_task`, and `load_skill`. Drop every failed call, refusal, and `confirmation_required`.

Turn handles, document paths, and one-off selection state into `{handle}`, `{path}`, or another `{name}` taken from what the user asked to change. A material name the user supplied becomes `{material}`. A length that was sent is `{length_m}` in meters, with the human unit written beside it. Angles stay radians.

Freeze what stayed the same on the winning call: `method`, `propertyName`, `kind`, `operation`, `member`, `memberName`, an enum member name, a material database name.

End with the check. Use the successful read from this chat that shows the value just written. For a material change, that is the read that reports the material on the part. When the chat has no confirming read, name one existing read tool that returns that field, such as `extract_part_data`. Do not add a call that was never confirmed.

If this chat has no successful write, do not write a file. Say which call failed. If two successful sequences disagree, keep the shorter one whose check passed.

## What to write

The name is lowercase letters, digits, and hyphens, at most 64 characters. Do not use `solidworks`, `solidworks-api`, `solidworks-procedure`, or `mechanical-reasoner`.

The description is one sentence: the operation, and when to use it. At most 1024 characters.

Write `SKILL.md` with `write_file` under each of these folders that already exists:

- `%USERPROFILE%\.cursor\skills\<name>\SKILL.md`
- `%USERPROFILE%\.codex\skills\<name>\SKILL.md`
- `%USERPROFILE%\.claude\skills\<name>\SKILL.md`

If that name already exists, show the old steps and the new steps and wait for the user to confirm before replacing the file.

Print the full file in the reply, in this shape, with `<tool>` and the frozen keys filled only from successful results in this chat:

```
---
name: set-material
description: Assign a material on the open SolidWorks part. Use when the user names a material to apply.
---

Part is open. Lengths on tools are meters. Angles are radians.

1. <tool> <frozen key=value> {material}
Check: <read tool> reports {material}.
If the check fails, stop and name the step. Do not search the API.
```

A step with no matching result is omitted. The file is a procedure for those calls. It is not a materials rule, an allowable, or a catalog fact.
