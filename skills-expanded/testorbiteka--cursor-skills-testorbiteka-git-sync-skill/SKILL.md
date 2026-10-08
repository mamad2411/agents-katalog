---
name: testorbiteka-git-sync
description: >-
  Synchronizes Testorbiteka repo with GitHub (msulich7-hub/Testorbiteka): evening
  push, morning pull, stash on conflicts, crm-engine Docker restart. Use when the
  user asks to pull from GitHub, push changes, sync local with remote, morning
  workflow, evening commit, git status, or Testorbiteka/crm-engine deployment.
---

# Testorbiteka Git Sync

## Repo layout (critical)

| Path | Remote | Role |
|------|--------|------|
| `Testorbiteka/Testorbiteka/` | `github.com/msulich7-hub/Testorbiteka` | Docs + scripts + **`crm-engine/`** |
| `MIMMS_CORE/orbiteus/` | `github.com/orbiteus/orbiteus` | **Separate** — do NOT push CRM weekend work here |

**Source of truth for CRM+orders code:** `Testorbiteka/crm-engine/`.

Full human doc: [docs/GIT-SYNC.md](../../../docs/GIT-SYNC.md)

---

## Evening — push to GitHub

```powershell
cd C:\Users\MARCINS\Documents\MIMMS_CORE\Testorbiteka\Testorbiteka
.\scripts\git-evening-push.ps1 "feat(scope): short description"
```

Or manually:
1. `git status` — review changes
2. `git add crm-engine/ docs/ scripts/` (or `git add .` if user confirms)
3. `git commit -m "..."` — never amend pushed commits unless user asks
4. `git push origin main`

For large features: branch `feat/name` → push → PR on GitHub.

**Never:** `git config` changes, force push to main, commit `.env` secrets.

---

## Morning — pull from GitHub

```powershell
cd C:\Users\MARCINS\Documents\MIMMS_CORE\Testorbiteka\Testorbiteka
.\scripts\git-morning-pull.ps1
```

Flow:
1. If dirty tree → `git stash push -u -m "pre-pull"`
2. `git fetch origin` + `git pull origin main`
3. `git stash pop` if stashed
4. Resolve conflicts: remove `<<<<<<<` markers, `git add`, commit

Check sync:
```powershell
git fetch origin
git status                    # up to date with origin/main?
git log --oneline HEAD..origin/main   # remote ahead → pull
git log --oneline origin/main..HEAD   # local ahead → push
```

---

## After pull — start stack

Ports 8000/5432/6379 often busy (Mercato/hub). Use local override:

```powershell
.\scripts\start-crm-engine.ps1
```

- Admin: http://localhost:3010
- API: http://localhost:8010
- Login: `admin@example.com` / `admin1234`

If backend fails with `entrypoint.sh: no such file` → CRLF issue; ensure `crm-engine/backend/entrypoint.sh` uses LF.

If migrations fail with multiple heads → check `crm-engine/backend/migrations/versions/` merge revision exists.

---

## Agent checklist

When user says "sync", "pull latest", "push to github":

- [ ] Confirm working directory is **Testorbiteka**, not orbiteus monorepo root
- [ ] Run appropriate script or git commands
- [ ] Report: commits ahead/behind, conflicts, push/pull result
- [ ] Offer `start-crm-engine.ps1` after successful pull
- [ ] Do NOT commit unless user explicitly asks
