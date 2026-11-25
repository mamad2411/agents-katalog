---
name: commix-cmdi-lab
description: >
  Use Commix for command-injection discovery only on owned labs, CTFs, and explicitly
  authorized targets: install/run safely, choose techniques (classic/time-based/file-based),
  limit payload impact, and export evidence. Use with cmdi-command-injection methodology
  and command-injection-defenses for fixes — never against systems without authorization.
---

# Commix CMDi Lab

## Scope And Authorization

- **In scope:** intentionally vulnerable labs (DVWA, custom, CTF), systems you own, written ROE.
- **Out of scope:** scanning the public Internet; destructive options; pivoting beyond lab.
- Prefer time-based/OOB to your collaborator only; no `rm`, ransomware, or miners.
- Pair manual reasoning with `cmdi-command-injection`; remediations with `command-injection-defenses`.

## When To Use

- Lab practice automating CMDi detection with **Commix**.
- Authorized assessment where Commix is approved tooling.
- Tokens: commix, command injection lab, `--technique`, `--os-cmd`, time-based.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Manual CMDi methodology | `cmdi-command-injection` |
| Defenses / argv hardening | `command-injection-defenses` |
| Unknown injection class | `injection-checking` |
| SQLi automation | SQLi tools skill |

## Tool Role

Commix automates probing of parameters for OS command injection. It can be noisy and aggressive — **constrain** level, threads, and OS commands.

## Workflow

### 1. Confirm authorization and lab target

1. Record target URL, ownership, ROE stop conditions.
2. Success: reproducible finding with minimal command (`id`/`whoami`) or documented clean miss.
3. Isolate network if possible (lab VLAN).

### 2. Install (controlled environment)

```bash
# Prefer venv / container for the tool itself
git clone https://github.com/commixproject/commix.git
cd commix
python commix.py --help
```

Pin commit in real ops; verify you are not on a compromised fork.

### 3. Baseline manual check

1. Confirm parameter manually with safe payload (`cmdi-command-injection`).
2. Note auth cookies, CSRF, method, WAF.

### 4. Run Commix with least impact

```bash
# Example: lab only — adjust URL/params
python commix.py -u "http://lab.local/ping?ip=127.0.0.1" \
  --data="" \
  --level=1 \
  --technique=t \
  --os-cmd="id" \
  --batch
```

| Flag area | Guidance |
| --- | --- |
| `--level` / `--risk` | Start low; raise only if needed |
| `--technique` | Prefer time-based (`t`) if no output; classic if reflected |
| `--os-cmd` | Non-destructive only (`id`, `hostname`, `whoami`) |
| Auth | `--cookie` / headers as required |
| `--batch` | Non-interactive; still watch output |
| Proxy | Burp for evidence capture |

### 5. Interpret results

1. Save full command line + output to engagement notes (redact cookies).
2. Validate “positive” manually — tools false-positive.
3. Map to sink if white-box available.

### 6. Evidence and report

1. Request/response or timing chart; Commix summary.
2. Impact: user of web process, not full post-exploitation chain unless ROE asks.
3. Recommend `command-injection-defenses`.

### 7. Cleanup

1. Stop scans; do not leave reverse shells.
2. Reset lab app if modified.
3. Remove temporary collaborator DNS records.

## Safety Table

| Allowed in lab | Forbidden without explicit ROE |
| --- | --- |
| `id`, `whoami`, `hostname` | Disk wipe, worm, mass scan |
| Controlled sleep timing | Crypto miner |
| OOB to your collab | OOB to random third parties |
| Read non-sensitive files if ROE | Credential dump for sale |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Target | Owned lab URL | Random .gov |
| Payload | `id` | Destructive OS cmd |
| Validation | Manual confirm | Blind trust tool |
| Noise | Low level first | Max risk all params |
| Secrets | Redacted notes | Paste session cookies publicly |

## Output Checklist

- [ ] Written authorization / lab ownership recorded
- [ ] Manual baseline attempted
- [ ] Commix run with constrained options
- [ ] Finding validated manually
- [ ] Evidence saved redacted
- [ ] Remediation pointer to defenses skill
- [ ] Lab cleaned; no leftover shells
- [ ] Residual false-negative risk noted if WAF blocked tool

## Rules

- **Lab/authorized only** — hard rule.
- Prefer minimal impact proofs.
- Tool assists; methodology skill owns reasoning.
- Never paste live production secrets into chat.
