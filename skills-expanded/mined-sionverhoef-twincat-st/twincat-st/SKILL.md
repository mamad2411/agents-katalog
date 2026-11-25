---
name: twincat-st
description: "Writes, reviews and debugs Structured Text for Beckhoff TwinCAT 3 and CODESYS V3, and ships a reviewer for the dialect traps that easy-looking questions hide (PT := 500, level-driven Execute, blocking loops, float equality). Use when the user has any Structured Text question or task, even a one-liner, rather than answering from memory: a timer, counter or trigger that never fires, a hung state machine, OOP (EXTENDS, ABSTRACT, SUPER^, interfaces, FB_init, online change), writing or reviewing function blocks, PackML, PLCopen motion and Execute/Done, ADS, TcUnit, .TcPOU/.plcproj files, or a folder that contains them. Not for Siemens SCL/TIA Portal, Rockwell Studio 5000, OpenPLC/matiec, EtherCAT wiring or hardware selection, Scope traces, NC axis configuration (twincat-motion), or drawing ladder diagrams; a team framework with its own review skill owns reviews of code written against it. Never write TwinSAFE/FSoE safety logic."
---

# Structured Text that survives contact with a machine

> **Reference material only. Not for safety functions.** All code you generate must be reviewed and validated by a qualified engineer against the drive and platform documentation before it runs on a machine. Every hand-over ends with the fixed line in step 5.

**Target: the CODESYS V3 dialect family.** TwinCAT 3 (build 4024.x) is the verified platform. Its PLC layer is CODESYS-V3-derived, so the vendor-neutral core applies to CODESYS too; CODESYS library names, the `.project` container and its tooling are **not covered** and were never checked on a CODESYS install. On a CODESYS question, answer from the core and say the vendor specifics are unverified rather than guess.

**Out of scope:** Siemens SCL, Rockwell Studio 5000 ST, OpenPLC/matiec. Those are different dialects — matiec implements IEC 61131-3 **2nd Edition** and has no `METHOD`, `PROPERTY`, `EXTENDS` or `INTERFACE` at all. Guidance from here would be fluent and wrong. Say so and stop.

**Scope traces and recordings** — reading a `.svdx`, sizing a recording, diagnosing an axis from measured data — belong to the companion skill `twincat-scope`. Load it if it is installed.

**TwinCAT NC axes** — axis configuration and parameters, NC error codes (0x4xxx), homing in the NC, coupling and cam tables, `.xti` axis files, and why an axis won't enable or move — belong to the companion skill `twincat-motion`. Load it if it is installed. This skill still owns how the PLC code around the MC_ blocks is written and reviewed.

## Why a skill, rather than just writing the code

A capable model writes Structured Text that *reads* correctly and *behaves* wrongly, because it imports a sequential mental model into a cyclically-scanned real-time system. The recurring failures are specific and predictable:

- `WHILE NOT bDone DO` where the answer was a state machine — the task overruns, the watchdog fires, the machine stops
- a `TON` preset written `PT := 500` instead of `PT := T#500MS`
- an `Execute` input driven from a level instead of an edge, so the block runs once and never again (reviewer rule `X11`)
- a wait with no timeout, so a failed sensor hangs the sequence with no diagnostic
- `IF fActual = fTarget` on an `LREAL`, which is essentially never true
- `SEL(bOption, 0, fWidth)` read as "0 when set": `SEL(G, IN0, IN1)` returns its **first** value when `G` is FALSE. `references/st-language.md` has `MUX` and `LIMIT` too

All but one of these compile. The exception, `PT := 500`, is a type error (`Cannot convert type 'INT' to type 'TIME'`), and there is almost certainly no compiler here to report it. So the priority order here is deliberate: **execution model first, syntax second, vendor trivia last** — and the review step is a program, not a vibe.

**Asked to add "another one like this", check the existing line first.** If it carries one of these traps, name that line as the problem before writing anything next to it. Copying its style copies the defect: in a field test an agent kept `Execute := bAutoMode AND bAtHome` unremarked and delivered a second level-driven move beside it.

## Three rules that override everything else

1. **Never author safety logic.** No TwinSAFE, no FSoE, no safety-PLC projects, and no emergency-stop handling written as standard PLC code and presented as a safety function. Functional safety needs a certified toolchain, a documented risk assessment and a competent person's sign-off, none of which an agent can supply. You may *read and explain* existing safety configuration. See `references/safety-boundary.md`.
2. **Never write to or activate a live machine.** Treat ADS as read-only. Writing a variable, activating a configuration or switching Run/Config on a real controller is a human gesture — propose the command, don't run it.
3. **Never claim code compiles when you have not compiled it.** There is almost certainly no PLC compiler here. `scripts/st_review.py` finds defect *patterns*; it is not a compiler, and a clean run proves only that nothing it knows about matched.

## Workflow

### 1. Orient before writing

PLC code is written against a *specific* machine. Guessing the I/O, the axis names or the library versions produces code that compiles and then does the wrong thing to real hardware.

Establish, and state what you assumed if you could not:

- vendor and version; which **task** this runs in and its **cycle time**
- the fault behaviour required — stop, hold, or continue degraded
- whether any part of this is a safety function (if yes → rule 1)
- what must survive a restart, and whether it is still *true* after one — a remembered step or "homed" usually is not (`references/cyclic-execution-rules.md` Rule 9; ask before making it `RETAIN`, which on TwinCAT also needs a retain handler)

**Read `examples/` when style is the question** — new code going into an existing codebase, or "make this look like ours". Real working code beats a written convention, but it is the most expensive thing here to read: skip it for a contained change to code you can already see. House code the team added there outranks everything, including this skill.

**If the project has its own written coding standard, load it before writing or reviewing** — a conventions skill in your list of available skills, or a standards document the user or the project's agent instructions point to. Don't search the repository for one. Its rules outrank this skill's defaults — `references/naming-conventions.md`, `templates/` and the published projects in `examples/` — but never the three rules above.

### 2. Choose the shape before the syntax

Naming the shape first is what prevents the sequential-code failure. Almost every task is one of five:

| Shape | Use when | Pattern |
|---|---|---|
| **Cyclic logic** | Continuous evaluation — interlocks, scaling, alarms | Straight-line, no state |
| **State machine** | Anything with steps, waiting or a sequence | `CASE eState OF` + per-state timeout |
| **Command FB** | An action a caller triggers and awaits | PLCopen `Execute`/`Busy`/`Done`/`Error` |
| **Manager** | One instance per device, all driven together | Array of instances + bounded `FOR` |
| **Edge/latch** | React once to a change | `R_TRIG`/`F_TRIG` |

If you are reaching for a `WHILE` loop or the words "wait until", you have picked the wrong shape. Go back to the state machine row.

Choosing between a `Execute`-style and an `Enable`-style interface is a real decision with a non-obvious rule behind it — see `references/behaviour-model.md`.

### 3. Write

1. **Declarations first, fully typed**, with a unit in the comment for every physical value (`// mm/s`). Units in declarations prevent a class of bug no compiler catches.
2. **Interface before body** — inputs, outputs and the error path (`bError`, `nErrorID`) before any logic.
3. **All states in an `E_` enum**, including `Idle` and `Error`.
4. **Body state by state**, each with an explicit exit condition *and* a timeout.
5. **A reset path.** If there is no way out of `Error`, the block is not finished.

Match the surrounding project's conventions even where they differ from `references/naming-conventions.md`. A consistently different codebase beats a half-converted one; flag the divergence, don't silently "fix" it.

### 4. Review — with the tool, not by eye

**A request to review is not a request to repair.** Asked to review, check, or "tell me what you find", report each finding with its location, rule id and the fix you would make — and leave the files as they are. Edit only when the user asks for fixes, or after asking whether they want them. A PLC project is often about to go onto a machine; changes nobody asked for are changes nobody re-tested.

**If a team review skill covers the framework this code is written against, that skill owns the review report.** Run `scripts/st_review.py` for it and hand over the findings with their rule ids (`CP8`, `X1`…) rather than writing a second report.

Run the reviewer on anything you wrote or were asked to review:

```bash
py -3 scripts/st_review.py <file-or-dir>...             # defect rules
py -3 scripts/st_review.py src/ --json                  # machine-readable
py -3 scripts/st_review.py --list-rules                 # what it checks
```

**Commands here are written `py -3`, because TwinCAT runs on Windows.** A bare `python3` there reaches the Microsoft Store stub and prints *"Python was not found"* even when Python is installed. On Linux or macOS use `python3`.

**Point it at the code you own, not at the whole `.plcproj`** — vendor and framework libraries bury your findings. Exit 1 means a finding at `--fail-on` (default `high`); exit 2 means a file could not be parsed, which is never a clean result. Every flag and exit status is in `references/tools.md`.

Findings carry a rule id to cite — `CP8`, `X1`, `E3`. `CP`/`N`/`C`/`L`/`E` are PLCopen rules with that document's severity, `X` are this skill's own; `references/plcopen-rules.md` is the catalogue.

The tool is a floor, not a ceiling. It cannot see intent, so **you still read the code** for the things it cannot check: is the shape right, is the error path meaningful, does the timeout value make physical sense, is this secretly a safety function. `references/cyclic-execution-rules.md` carries the review rubric for that pass.

When the tool reports something you have judged acceptable, record the judgement in the code rather than ignoring the line:

```pascal
WHILE pNode <> 0 DO   // lint:allow X1 list is built at init, max 64 nodes
```

An unexplained suppression is itself reported, because a bare silencer and an unreviewed defect look identical six months later.

### 5. Say what you actually verified

Name the rung you reached. Never imply a higher one.

| Rung | What it proves |
|---|---|
| 1. **TcUnit on a real target**, results read back over ADS | Real semantics, real timing |
| 2. **Headless build** via the Automation Interface on a Windows PC with XAE — `scripts/xae_build.ps1`, or `xae_edit.ps1 build` when the user has the solution open | Full compiler errors |
| 3. **`scripts/st_review.py` + a human read** | Known defect patterns absent — **always do this** |
| 4. Nothing | Then say "unverified, not compiled" plainly |

There is deliberately no Linux syntax-check rung: `matiec` and `rusty` cannot parse this dialect's OOP constructs, so a clean run there would look like a pass and prove almost nothing.

Close with: what you wrote and which shape it uses · what was verified and what was not · the assumptions you made about I/O, cycle time and fault behaviour · what the human must do next.

**End every hand-over that contains code with this line, word for word, even for a one-line change:**

> Not compiled. A qualified engineer must review and validate this code against the drive and platform documentation before it runs on a machine.

When the code built through XAE with 0 errors (rung 2), the line starts `Compiled in XAE, not tested on a target.` instead of `Not compiled.`; the rest stays word for word.

"Not compiled" alone is not enough, and neither is "review it before it goes on the machine": in a field test, agents wrote the first every time and the full line once in eight.

## Where to read next

Load a reference when the task reaches it — don't read them all up front.

| File | Read it when |
|---|---|
| **`references/cyclic-execution-rules.md`** | **Writing or reviewing any ST.** The execution model and the review rubric. Highest-value file here. |
| `references/plcopen-rules.md` | Citing a rule, or doing a formal review. The 64-rule catalogue with severities. |
| `references/st-language.md` | Syntax, data types, the POU model, OOP constructs. Vendor-neutral. |
| `references/behaviour-model.md` | Designing an FB interface — `Execute`/`Done` vs `Enable`/`Valid`, abort and timeout. |
| `references/patterns.md` | State machines, sequences, PackML, and how to lay out a machine project. |
| `references/oop.md` | Inheritance vs composition vs interface; SOLID applied to function blocks. |
| `references/naming-conventions.md` | Naming anything. Measured against a real corpus, not asserted. |
| `references/testing-tcunit.md` | Writing tests, or asked whether the code is testable. |
| `references/safety-boundary.md` | **Anything** touching TwinSAFE, FSoE, E-stop, guards, or a SIL/PL claim. |
| `references/twincat.md` | TwinCAT specifics — libraries, `FB_init`, online change, 4024 gotchas. |
| `references/twincat/project-files.md` | Editing `.TcPOU`/`.plcproj`, or a git merge conflict in one. |
| `references/twincat/ads-and-diagnostics.md` | ADS access, EtherCAT triage, reading a running machine. |
| `references/twincat/xae-automation.md` | Asked for a build or compile check, and XAE is installed, or editing a project the user has open in XAE. What a build rewrites, why disk edits make XAE ask to reload, and why activation stays manual. |
| `references/twincat/tasks-and-exceptions.md` | Data shared between tasks or cores, locking, or a PLC that stopped on an exception — finding the line, core dumps, `CheckBounds`/`CheckDiv…` implicit checks, `__TRY`/`__CATCH`. |
| `references/tools.md` | A reviewer or `tcpou.py` result you did not expect — every flag, exit status and subcommand in full. |

**Routing rule of thumb:** if the answer names a `Tc2_`/`Tc3_` library, a `.TcPOU` file, ADS or XAE, it is TwinCAT-specific and belongs behind `references/twincat.md`, not in a general answer.

## Tools

| Path | For |
|---|---|
| `scripts/st_review.py` | The reviewer. Run it on every change. |
| `scripts/tcpou.py` | Read and edit real `.TcPOU` files without disturbing GUIDs, `<LineIds>`, the BOM or CRLF, **while XAE is closed**. Commands below. |
| `scripts/xae_edit.ps1` | Windows with XAE only, **while the user has the solution open in XAE**: edit, save and build through that XAE, so it never asks to reload. Commands below. |
| `scripts/xae_build.ps1` | Windows with XAE only, while the solution is closed: a headless build with the real compiler output. Only when the user asked for a build — it rewrites `.tmc`/`.xti`/`_CompileInfo`. It never activates. |
| `templates/` | Known-good skeletons — sequence FB, state enum, TcUnit suite. |
| `examples/` | Real working code from two published projects, each with a `NOTES.md` on what to take from it. When to read it: step 1. |

The Python scripts need Python 3 and nothing else.

### `tcpou.py`

Editing a `.TcPOU` as plain text is how you corrupt a project. Every subcommand, each explained in `references/tools.md`:

```bash
py -3 scripts/tcpou.py show     <file>                                   # parts + encoding
py -3 scripts/tcpou.py get      <file> --part impl [--out body.st]       # print or write one part
py -3 scripts/tcpou.py set      <file> --part impl --from-file body.st   # replace one part
py -3 scripts/tcpou.py new      --type fb --name FB_Filling --dir POUs/  # a name, not a path; --shape execute|enable|cyclic
py -3 scripts/tcpou.py add-method   <file> --name Reset [--returns BOOL] # append an empty METHOD
py -3 scripts/tcpou.py add-property <file> --name Speed --type LREAL     # append a PROPERTY (--no-set: read-only)
py -3 scripts/tcpou.py register <PLC.plcproj> <file>...                  # make it compile
py -3 scripts/tcpou.py reguid   <file>...                                # re-stamp Ids
py -3 scripts/tcpou.py check    <file>...                                # validate
py -3 scripts/tcpou.py pins     <file> [--pin REGEX] [--box REGEX]       # FBD/LD box wiring
py -3 scripts/tcpou.py code-equal <file|dir>... [--ref REV | --against FILE] # comments-only?
```

The five that cause damage when missed:

- **If the user has the solution open in XAE, edit with `xae_edit.ps1`, not `tcpou.py`.** A write on disk makes XAE ask to reload the file, and can lose edits it holds unsaved. `tcpou.py` refuses to write while XAE holds the project; say so to the user rather than reaching for `--allow-open`.
- **Run `show` before `get`/`set`** rather than guessing a part key (`decl`, `impl`, `Reset:impl`, `ActualValue.Get:impl`), and **check the exit status**: a `set` that never ran leaves the file exactly as unchanged as a `set` that changed nothing.
- **A new file that is not registered in the `.plcproj` silently does not compile.** `register` is not optional; it is idempotent.
- **From Windows PowerShell 5.1, move a part with `get --out` and `set --from-file`, never with `>` or a pipe** — both re-encode through the console code page and lose characters such as `²` for good.
- **Run `pins` before concluding a signal is unused or unwired in an FBD or LD caller** — that wiring lives in the network XML, where a text search finds nothing. Claim "comments only" with `code-equal`, not by eye.

### `xae_edit.ps1`

The same edits through the user's open XAE: they land in XAE's memory, the editor shows them with an unsaved `*`, and nothing asks to reload. A declaration write is the exception: XAE saves that object at once, and the tool says so. Every edit `tcpou.py` makes has a command here; XAE stamps the GUIDs and registers new files itself, so `reguid` and `register` have no counterpart. Run each line as `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\xae_edit.ps1 …` from Windows PowerShell 5.1, at the same elevation as XAE. Every option is in `references/tools.md`.

```powershell
xae_edit.ps1 list                                                       # which XAE holds which solution; run it first
xae_edit.ps1 show       'TIPC^PLC1^PLC1 Project^POUs^FB_X' -Solution x.sln
xae_edit.ps1 get        '<TreePath>' -Solution x.sln -Part impl [-Out body.st]   # without -Out it prints, for reading only; use -Out to move a part into set
xae_edit.ps1 set        '<TreePath>' -Solution x.sln -Part impl -FromFile body.st   # ST only; reads back
xae_edit.ps1 new        '<Folder>'   -Solution x.sln -Type fb -Name FB_Pump [-FromDecl d.st] [-FromImpl i.st]
xae_edit.ps1 add-method '<PouPath>'  -Solution x.sln -Name M_Reset [-Returns BOOL] [-FromDecl d.st] [-FromImpl i.st]
xae_edit.ps1 add-property '<PouPath>' -Solution x.sln -Name Speed -Returns LREAL [-NoSet]
xae_edit.ps1 save       '<TreePath>' -Solution x.sln                    # that POU only, never Save All
xae_edit.ps1 build                   -Solution x.sln                    # builds in the user's XAE
```

- **`new -Type`** is `fb`, `prg`, `fun`, `dut` (struct), `enum`, `union`, `alias`, `gvl` or `itf`; give `EXTENDS`/`IMPLEMENTS`, a function's return type or a DUT's members in `-FromDecl`. A method or property of an interface takes the interface's path. An accessor is a path too: `set '…^FB_X^Speed^Get' -Part impl`.

- **`save` before `st_review.py` or `git diff`** — they read the disk, which holds a `set` only after the save.
- **It refuses to touch a POU with unsaved edits it did not make, and `build` refuses while any exist** — a build saves every unsaved object, the user's half-typed edits included. `-Force` and `-SaveUserEdits` override; use them only when the user says so. Settings on a PLC project's properties pages are not checked: ask the user to save or close the PLC project's properties before you build.
- **Exit 2 with a dialog named means a prompt is open in XAE.** Ask the user to answer it; never click it from a script. Logging in and the online change stay the user's gesture (rule 2).
