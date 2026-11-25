---
name: frida-stalker-basics
description: >
  Use Frida Stalker for instruction-level tracing on owned/lab processes: follow threads,
  filter call/ret/block events, manage performance cost, and extract execution paths for
  reverse engineering. Use when Interceptor alone is insufficient on authorized targets—not
  for unauthorized tracing of third-party production apps.
---

# Frida Stalker Basics

## Scope And Authorization

- **In scope:** CTF/lab binaries, owned apps, authorized RE engagements.
- **Out of scope:** covert tracing of third-party users or unauthorized apps.
- Stalker is expensive—expect slowdown; avoid on fragile production without approval.
- Redact instruction traces that include secrets.
- Pair with `frida-hooking-playbook` for attach setup and `frida-compile-agent` for packaging.

## When To Use

- Need **basic block / call** trace through opaque code paths.
- Locating branches that validate licenses or parse packets in lab RE.
- Measuring which code runs for a given input (coverage-like insight).
- When single-function `Interceptor` is not enough.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General attach/hook playbook | `frida-hooking-playbook` |
| Agent bundling | `frida-compile-agent` |
| LibFuzzer coverage fuzzing | `fuzzing-libfuzzer-basics` |
| Static analysis first | `binary-re/static-analysis` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| API | Role |
| --- | --- |
| `Stalker.follow(tid, opts)` | Start tracing a thread |
| `Stalker.unfollow` | Stop |
| `transform` | Instrument blocks (advanced) |
| Events | `call`, `ret`, `exec`, `block` — enable sparingly |
| `Stalker.exclude` | Skip modules (e.g. noisy libc) |

## Workflow

### 1. Confirm scope and success criteria

1. Target process, thread of interest (main vs worker), authorization.
2. Success: manageable event volume answering a RE question (e.g. “which function validates packet magic?”).
3. Prefer offline lab reproduction.

### 2. Attach and identify threads

```bash
frida -p $(pidof lab_bin) -l stalker.js
# or Android lab spawn then follow app threads carefully
```

```js
Process.enumerateThreads().forEach(function (t) {
  console.log(t.id, t.state);
});
```

### 3. Minimal Stalker session

```js
var mainTid = Process.getCurrentThreadId(); // or chosen tid

Stalker.follow(mainTid, {
  events: {
    call: true,
    ret: false,
    exec: false,
    block: false,
  },
  onReceive: function (events) {
    // parse with Stalker.parse
    var parsed = Stalker.parse(events, { annotate: true, stringify: true });
    console.log(parsed);
  },
});

// trigger behavior, then:
// Stalker.unfollow(mainTid);
// Stalker.flush();
```

1. Start with **call events only**; `exec` is extremely heavy.
2. Exclude noisy modules when API available for your Frida version.

### 4. Narrow the window

1. Use Interceptor on a gate function: follow only after enter, unfollow on leave.
2. Filter by call target module (`Module.mapAddress` / `Process.findModuleByAddress`).
3. Dump symbols with `DebugSymbol.fromAddress` when available.

```js
Interceptor.attach(ptr("0xDEADBEEF"), {
  onEnter(args) {
    Stalker.follow(Process.getCurrentThreadId(), { events: { call: true } /* ... */ });
  },
  onLeave(retval) {
    Stalker.unfollow(Process.getCurrentThreadId());
    Stalker.flush();
  },
});
```

### 5. Performance and stability

| Issue | Mitigation |
| --- | --- |
| Massive logs | Time-box; call-only; exclude modules |
| Crashes | Avoid following all threads; patch less |
| JIT/runtime | Re-follow after recompile if needed |
| Mobile ANRs | Short windows only |

### 6. Verify with evidence

1. Trace contains expected library/function names for known lab path.
2. Change input → trace path differs (hypothesis validation).
3. Save traces to disk carefully (size limits).

### 7. Hand off

1. Summarize path diagram; interesting addresses for static RE.
2. Do not ship Stalker always-on in production builds.
3. Apply `code-quality-standards` for scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Events | call/block filtered | exec everything forever |
| Window | Gate with Interceptor | Follow all threads at spawn |
| Scope | Lab binary | Unauthorized banking app |
| Output | Symbolized highlights | Multi-GB raw dump unanalyzed |
| Goal | Answer RE question | “Trace for its own sake” |
| Ethics | Auth recorded | Covert user monitoring |

## Output Checklist

- [ ] Authorization recorded
- [ ] Thread selection justified
- [ ] Event types minimized
- [ ] Follow window gated
- [ ] Trace answers stated RE question
- [ ] Performance impact acceptable for lab
- [ ] Artifacts redacted/stored
- [ ] Static RE hand-off addresses listed

## Rules

- Authorized lab/owned targets only.
- Stalker is high-cost—scope tightly.
- Prefer Interceptor first; escalate to Stalker when needed.
- No guidance for unauthorized surveillance or app piracy.
