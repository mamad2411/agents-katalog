---
name: ctf-pwntools
description: Use when pi needs focused pwntools workflow guidance for exploit scripting, local or remote tube setup, ELF or libc loading, ROP payload building, leak parsing, shellcraft helpers, or reusable pwn scaffolding. Trigger on mentions of pwntools, `from pwn import *`, process(), remote(), ELF(), ROP(), cyclic, p64/u64, flat(), fit(), SigreturnFrame, fmtstr_payload, shellcraft, or exploit script cleanup.
---

# CTF Pwntools

Use this skill when the main question is how to structure or refine a `pwntools` exploit script.

## Default Behavior

- Prefer small, reusable scaffolds over one-off throwaway scripts.
- Keep local and remote startup paths separate from exploit logic.
- Use exact binaries and matching `libc` files when symbol or offset math matters.
- Hand off binary triage to `ctf-pwn-local-analysis` if protections, offsets, or gadgets are still unknown.

## Workflow

1. Normalize the target mode.
   Decide whether the script should use `process()`, `remote()`, `gdb.debug()`, or a shared `start()` helper.
2. Load artifacts once.
   Set `context.binary = elf = ELF("./chall")` and load `libc` only when the exploit depends on it.
3. Separate the exploit stages.
   Keep leak collection, base-address math, gadget lookup, and final payload assembly in distinct blocks.
4. Use pwntools helpers on purpose.
   Reach for `cyclic`, `cyclic_find`, `flat`, `fit`, `p64`, `u64`, `ROP`, `SigreturnFrame`, `fmtstr_payload`, and `shellcraft` only when each helper clearly reduces bug risk.
5. Leave the script rerunnable.
   Parameterize host, port, GDB mode, and local or remote selection instead of editing constants by hand every run.

## Preferred Scaffold

```python
from pwn import *

context.binary = elf = ELF("./chall")
context.terminal = ["tmux", "splitw", "-h"]

HOST = args.HOST or "127.0.0.1"
PORT = int(args.PORT or 31337)

def start():
    if args.GDB:
        return gdb.debug([elf.path], gdbscript="b *main\nc")
    if args.REMOTE:
        return remote(HOST, PORT)
    return process([elf.path])

io = start()
```

Keep the rest of the script organized as:

- setup and target selection
- leak or state collection
- address resolution
- final payload
- interactive or proof step

## Guardrails

- Do not mix guessed offsets with confirmed ones.
- Do not hardcode remote libc assumptions without labeling them.
- Do not hide parsing logic inside giant one-liners when a named helper makes failure easier to debug.
- Prefer a short proof-of-control script before a polished final exploit.

## Handoff Rules

- If the blocker is binary understanding, switch to `ctf-pwn-local-analysis` or `ctf-ida`.
- If the blocker is Linux runtime behavior, loader differences, or live debugging, run the binary directly in the native Linux shell (this is already a Linux host).
- If the exploit math is heavy or benefits from SageMath, switch to `ctf-sage` (the local `sage10.9` conda env).

## Output Expectations

- Return a script structure that is runnable, easy to toggle between local and remote, and explicit about what data still needs to be confirmed.
