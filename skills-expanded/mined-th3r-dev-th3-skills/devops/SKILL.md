---
name: devops
description: >-
  DevOps toolkit for a small platform team, generalised from a Thai-government integration
  project: (1) change — any infra work that touches a real machine (ssh via a jump host, kubectl,
  HAProxy / ingress / vault-backed secrets, incident root cause) done in a fixed order and closed
  with a before / steps / after / rollback report with a SEV level; (2) release-scope — what goes
  up in the next release and what is still pending, from git keys across the product's repos plus
  the issue boards, written as the PM list and checked against the customer message; (3)
  network-diagram — the team's system / network diagram as one draw.io file with a board per
  version, exported to a clean one-page PDF, rebuilt from a PDF, benchmarked. Use WHENEVER the work
  is "ssh to the server", "edit haproxy", "root cause / postmortem", "what's in release X",
  "release note for the PM", "update the system diagram", "export the drawio", "เขียน rootcause",
  "สรุป release ให้ PM", "แก้ diagram ระบบ". Read the sub-skill's SKILL.md before acting.
---

# devops — sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| "ssh to <ip>", "kubectl on the cluster", "edit haproxy.cfg", "root cause", "before/after/rollback report" | [`change/SKILL.md`](change/SKILL.md) + [`references/`](change/references/) (change template TH/EN, incident template) | `change/scripts/jssh.py` (jump-host ssh from an ini, `--sudo` `--kube` `--forward`) · `snapshot_haproxy.sh` |
| "what's in v1.2.x", "pending for the next release", "summary for the PM", "check the PM's customer message" | [`release-scope/SKILL.md`](release-scope/SKILL.md) | `release-scope/scripts/release_scope.py` (`--repo` × N, `--key-regex`, `--board` × N → `scope.md` + `scope.json`) |
| "update the system diagram", "export the drawio to one PDF", "rebuild the drawio from the PDF", "compare with the final PDF" | [`network-diagram/SKILL.md`](network-diagram/SKILL.md) | `network-diagram/scripts/drawio_board.py` (`list` `clone` `export` `trace` `compare`) + `assets/icons/` |

They chain: a `change/` report links the diagram that explains it (`rootcause.html`, or a version
board from `network-diagram/`); `release-scope/` tells `change/` which tag a prod deploy carries.

## Rules every sub-skill keeps

- **Read the project's own `docs/`, `changes/` and `incidents/` before guessing about a machine.**
  Facts about your fleet beat any generic cloud / Kubernetes advice.
- **Passwords never appear on a command line, in a report, or in chat.** `jssh.py` reads them from
  `~/.config/devops/hosts.ini` (chmod 600) and hands them to ssh through `SSH_ASKPASS`.
- **Evidence before change, same commands after.** Snapshot the *running* config, md5, inode,
  start time and the numbers that will judge the result; verify by re-running them, not by "no errors".
- **Rollback is written before step 1**, with the command that proves it worked.
- **Prod facts come from the owner** (what prod runs, which hotfix never shipped), not from tags.
- **Diagrams are editable sources**, exported to PDF — never the other way round, and never with
  icons cut from a PDF.
- **Scripts run with `uv run <script>`** (PEP 723 inline dependencies); `drawio_board.py` also needs
  the draw.io desktop app.

## Tests

```bash
cd skills/devops && python -m pytest -q     # needs: pytest pymupdf numpy pillow (git on PATH)
```
