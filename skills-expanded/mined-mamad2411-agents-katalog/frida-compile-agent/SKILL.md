---
name: frida-compile-agent
description: >
  Package Frida agents with frida-compile/frida-fs bundling: TypeScript/JS agent entry,
  compile to single script, load via frida/-U, and manage dependencies for lab RE. Use
  when building maintainable instrumentation agents for owned apps and authorized CTF
  work—not for unauthorized third-party app abuse.
---

# Frida Compile Agent

## Scope And Authorization

- **In scope:** packaging instrumentation for apps/binaries you own, labs, CTFs, authorized engagements.
- **Out of scope:** bypassing protections on third-party apps without written authorization.
- Keep agents out of production user devices without consent/legal basis.
- Redact captured tokens from agent logs.
- Pair with `frida-hooking-playbook` for attach patterns and `code-quality-standards` for agent code.

## When To Use

- Building multi-file **Frida JS/TS agents** that need bundling.
- Using `frida-compile` to produce one script for `frida -l`.
- Sharing reusable agent modules (Java bridges, native interceptors) in a team lab.
- CI lint/build of agent sources.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Attach/spawn/hook playbook | `frida-hooking-playbook` |
| Stalker instruction tracing | `frida-stalker-basics` |
| Mobile SSL pin bypass methodology | `mobile-ssl-pinning-bypass` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Tool | Role |
| --- | --- |
| `frida-compile` | Bundle agent entry + imports → single JS |
| Agent source | ES modules / TS depending on setup |
| Runtime | `frida` CLI, Frida Gadget, or embedded |
| Output | `agent.js` loaded with `-l` |

## Workflow

### 1. Confirm scope and success criteria

1. Target platform (Android/iOS/desktop), Frida versions on host and device.
2. Success: reproducible `npm run build` → agent loads without syntax errors; hooks fire on lab app.
3. Authorization recorded.

### 2. Project layout

```text
agent/
  package.json
  tsconfig.json   # if TS
  src/index.ts    # entry
  src/hooks/*.ts
dist/agent.js     # compiled output
```

```json
// package.json scripts sketch
{
  "scripts": {
    "build": "frida-compile src/index.ts -o dist/agent.js -c",
    "watch": "frida-compile src/index.ts -o dist/agent.js -w"
  }
}
```

### 3. Write modular agent

```ts
// src/index.ts
import { hookJava } from "./hooks/java";
import { hookNative } from "./hooks/native";

rpc.exports = {
  ping() {
    return "pong";
  },
};

setImmediate(() => {
  if (Java.available) hookJava();
  hookNative();
});
```

1. Prefer `rpc.exports` for host→agent control.
2. Avoid giant single files; compile bundles them.
3. Do not ship secrets inside agents.

### 4. Compile and load

```bash
npm ci
npm run build
# USB Android lab device with frida-server (authorized)
frida -U -f com.example.lab -l dist/agent.js --no-pause
# or attach
frida -U "Lab App" -l dist/agent.js
```

1. Match **Frida major versions** across pip package, frida-tools, and frida-server.
2. On compile errors, fix TS target / DOM libs; agent env is Frida, not browser.

### 5. Verify with evidence

| Check | Expect |
| --- | --- |
| Build | `dist/agent.js` non-empty |
| Load | No immediate exception |
| rpc | `ping` returns pong from Python API if used |
| Hooks | Lab log lines appear |

```python
# Optional host control
import frida
# device = frida.get_usb_device()
# session = device.attach("Lab App")
# script = session.create_script(open("dist/agent.js").read())
# script.load()
# print(script.exports_sync.ping())
```

### 6. Operate

1. Watch mode during development; rebuild before demos.
2. Pin dependency versions in lockfile.
3. Document required frida-server version for the team.

### 7. Hand off

1. README: build, deploy, authorization warning.
2. Link hook patterns to `frida-hooking-playbook`.
3. Apply `code-quality-standards` to agent TypeScript.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Owned/lab package | Weaponized agent vs third-party prod |
| Structure | Modules + compile | 5k-line paste into `-l` |
| Versions | Pinned Frida stack | Mixed 14/16 mismatches |
| Secrets | Never hardcode | API keys in agent source |
| RPC | Explicit exports | Eval remote strings blindly |
| Evidence | Load + hook logs | “Should work” |

## Output Checklist

- [ ] Authorization recorded
- [ ] Agent project builds cleanly
- [ ] Frida versions aligned
- [ ] Load test on lab target success
- [ ] rpc/hooks verified
- [ ] README with build steps
- [ ] No secrets in agent
- [ ] `code-quality-standards` applied

## Rules

- Authorized instrumentation only.
- Packaging skill—not a license to bypass third-party protections.
- Keep agents modular and version-pinned.
- Use companion Frida skills for hook and Stalker depth.
