---
name: command-injection-defenses
description: >
  Defend applications against OS command injection by avoiding shells, using argv
  arrays, allowlisting inputs and binaries, and preferring library APIs over exec.
  Use when hardening process spawning (subprocess/ProcessBuilder/child_process),
  CLI wrappers (ping, convert, ffmpeg, git), shell=True or system()/exec() review,
  or remediating CMDi findings — authorized/org-owned systems only. Assessment:
  cmdi-command-injection.
---

# Command Injection Defenses

## Scope And Authorization

- **In scope:** code and hosts you own; remediating authorized findings.
- **Out of scope:** “testing” defenses by attacking systems without permission.
- Prefer library APIs over OS CLIs whenever possible.
- Pair with `code-quality-standards` and retest via `cmdi-command-injection` / `commix-cmdi-lab` in labs.

## When To Use

- Fixing CMDi vulnerabilities or preventing them in new features.
- Code review of process execution sinks.
- Tokens: argv, shell=False, ProcessBuilder, execFile, allowlist, avoid system().

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Offensive proof of CMDi | `cmdi-command-injection` |
| Lab automation with Commix | `commix-cmdi-lab` |
| Generic injection triage | `injection-checking` |
| SQL injection | `sqli-sql-injection` |

## Defense Hierarchy (strongest first)

| Rank | Control |
| --- | --- |
| 1 | Do not invoke OS shell/CLI — use native library |
| 2 | Fixed executable + argv array; never concatenate |
| 3 | Strict allowlist of arguments/values |
| 4 | Escape (last resort; easy to get wrong) |
| 5 | Sandbox/container least privilege (depth only) |

Blacklists of `;` and `|` are **not** sufficient.

## Language Patterns

### Python

```python
# Bad
os.system(f"ping -c 1 {host}")
subprocess.call("ping -c 1 " + host, shell=True)

# Good
subprocess.run(
    ["/bin/ping", "-c", "1", host],
    check=False,
    capture_output=True,
    text=True,
    timeout=5,
)
# Better: validate host against allowlist or strict IP/hostname regex first
```

### Node.js

```javascript
// Bad
const { exec } = require("child_process");
exec("convert " + userPath + " out.png");

// Good
const { execFile } = require("child_process");
execFile("/usr/bin/convert", [userPath, "out.png"], { timeout: 5000 }, cb);
// Still validate userPath is under upload dir (path traversal)
```

### Java

```java
// Bad
Runtime.getRuntime().exec("bash -c " + cmd);

// Good
ProcessBuilder pb = new ProcessBuilder("/usr/bin/convert", input, output);
pb.redirectErrorStream(true);
Process p = pb.start();
```

### Go

```go
cmd := exec.Command("ffmpeg", "-i", in, out) // argv form
cmd.Run()
// not: exec.Command("sh", "-c", userString)
```

## Workflow

### 1. Inventory sinks

```bash
rg -n "shell=True|os\.system|popen|subprocess\.call\(|Runtime\.exec|ProcessBuilder|child_process\.exec|execSync|shell_exec|proc_open|System\(" 
```

1. Tag each: can remove, can argv, or must shell (rare).
2. Note privilege of process (container user).

### 2. Eliminate shell where possible

1. Replace ImageMagick/ffmpeg wrappers with maintained libraries if feasible.
2. For required CLIs: absolute path to binary; argv only.
3. Disable shell metacharacter interpretation by never using shell.

### 3. Validate inputs

| Input type | Validation |
| --- | --- |
| Hostname | Strict DNS label regex or resolve + IP allow policy |
| Enum mode | Allowlist map (`{"png": "--png"}`) — never raw flags from user |
| File path | Resolve realpath; must stay under base dir |
| Numeric | Parse int/float with bounds |

### 4. Least privilege runtime

1. Drop capabilities; non-root user.
2. Read-only root FS; dedicated temp dir.
3. Seccomp/AppArmor if platform supports.
4. Network egress deny if CLI does not need net.

### 5. Tests

```python
def test_rejects_metacharacters():
    for bad in ["; id", "| id", "$(id)", "`id`", "&& id"]:
        assert is_rejected(bad)

def test_safe_host_ok():
    assert run_ping("127.0.0.1").returncode in (0, 1)
```

1. Include Windows metacharacters if platform supports.
2. Integration test that old exploit payload from finding no longer works.

### 6. Code review checklist

- [ ] No `shell=True` / `bash -c` / `cmd /c` with user data
- [ ] Executable path fixed/allowlisted
- [ ] Args allowlisted or strictly typed
- [ ] Paths constrained
- [ ] Timeouts set
- [ ] Output not reflected unsafely (secondary XSS)
- [ ] Errors don’t leak shell internals to untrusted clients

### 7. Hand off

1. Document remaining intentional shells (why + controls).
2. SAST rules to ban new `shell=True`.
3. Retest with `cmdi-command-injection` methodology.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| API | argv array | String command line |
| Validation | Allowlist enums | Strip `;` only |
| Binary | Absolute path | `ping` from PATH attacker-controlled |
| Privilege | Nobody user | Root container |
| Proof of fix | Old payload fails | “Looks sanitized” |

## Output Checklist

- [ ] All sinks inventoried
- [ ] Shell eliminated or justified
- [ ] Argv + validation implemented
- [ ] Path confinement where files involved
- [ ] Least privilege applied
- [ ] Regression tests for exploit payloads
- [ ] SAST/review gates added
- [ ] Residual intentional exec documented

## Rules

- Owned systems only for changes.
- Prefer remove-exec over clever escaping.
- Evidence via failed exploit retests.
- Defense skill; offensive details stay in `cmdi-command-injection`.
