---
name: web-vuln-triage
description: "Take a list of web leads or a surface inventory, run targeted non-destructive checks, then dedupe, de-noise, and prioritize what looks genuinely exploitable. Turns a pile of scanner output into a ranked, human-reviewable findings list."
version: "1.0.0"
author: redteam-ops
license: Apache-2.0
allowed-tools: Bash Read Write
---

# Web Vuln Triage

> **Runtime: Claude Code.** Helper scripts are in this skill's `scripts/` directory; in commands below, `<skill-dir>` is the absolute skill path provided when the skill loads. `<active-engagement>` is the engagement folder path recorded in `~/.claude/engagements/active` (set by the engagement-setup skill) — read it before resolving paths. Active scope: `<active-engagement>/scope.yaml`. Write outputs to the engagement's numbered subfolders (01-recon, 03-evidence, 04-findings, 05-changes, 07-reports, logs/ — see that folder's CLAUDE.md). Tools are restricted to `Bash Read Write`; irreversible actions are governed by the F0RT1KA permission wall (`~/.claude/hooks/offensive-gate.py`) per the engagement's `autonomy.mode` — `gated` forces a Bash permission prompt, `supervised-auto` allows after a stage briefing.


TRIAGE phase. Run safe, targeted checks against in-scope leads, throw out the noise, and
keep what looks worth verifying. Triage shapes signal — it does **not** confirm or exploit;
confirmation is a deliberate later step.

## When to Use

- After `web-recon-surface`, or when handed a lead/`surface.json`.
- When asked to "triage these findings", "throw out the noise", or "tell me what's exploitable".

## Quick Reference

| Tool      | Role                                  | Notes |
| --------- | ------------------------------------- | ----- |
| `nuclei`  | Templated checks (CVEs, misconfigs)   | Default to non-destructive templates; rate-limit with `-rl` |
| `httpx`   | Targeted header/response inspection   | For manual signal on specific endpoints |
| `ffuf`    | Content/endpoint discovery            | Only if `active_scan` is allowed; throttle |

```bash
nuclei -l in_scope_hosts.txt -severity low,medium,high,critical -rl 50 -jsonl -o nuclei.jsonl
python3 <skill-dir>/scripts/triage_nuclei.py nuclei.jsonl -o triaged.json
```

## Procedure

1. **Scope + action check.** Ensure `engagement-scope` is loaded. Triage is `active_scan`; confirm each host returns `0` for `--action active_scan`. If only `passive_recon` is allowed, stop and ask the operator.
2. **Choose safe templates.** Default to detection/misconfig templates. **Exclude** intrusive, fuzzing, or DoS-prone templates unless the operator explicitly approves — some templates are disruptive and belong behind the exploitation gate, not in triage.
3. **Run at a polite rate.** Use `-rl`/concurrency limits. Scan in-scope hosts only; never expand the host list mid-run without re-gating.
4. **Dedupe & prioritize.**
   ```bash
   python3 <skill-dir>/scripts/triage_nuclei.py nuclei.jsonl -o triaged.json
   ```
   Informational findings are dropped by default; pass `--keep-info` only when the operator wants them.
5. **Apply judgment on top of severity.** Re-rank by exploitability and asset value, not raw scanner severity: an auth bypass on the login host beats a medium on a static marketing page. Note suspected false positives for manual review.
6. **Hand off.** Produce a ranked list with host, finding, severity, and why it matters. Route confirmed-interesting items to `web-exploit-chain` (for chaining/verification) or straight to `web-report`. Write `triaged.json` to the evidence dir.

## Pitfalls

- **Scanner severity ≠ real risk.** Treat template severity as an input, not the verdict.
- **False positives** are common (especially version-based CVE matches behind a WAF or backport). Flag, don't assume.
- **Noisy/destructive templates.** Some checks are disruptive; keep them out of triage and behind the exploitation gate.
- **Auth context matters.** Unauthenticated vs authenticated scans surface different issues — record which you ran.

## Verification

- `triaged.json` parses; every finding maps to an in-scope host with an assigned severity.
- Duplicates are collapsed and informational noise is removed (unless explicitly kept).
- The ranked list reflects exploitability/asset value, not just raw scanner output.
