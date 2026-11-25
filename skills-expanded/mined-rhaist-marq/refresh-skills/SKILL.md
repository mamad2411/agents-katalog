---
name: refresh-skills
description: Runs the 6-8 week review sweep of the skills/ knowledge pack against primary sources, bumps review dates and the pack version, and cuts a local pack release. Use when the user asks to refresh, re-verify or release the skills pack, or when `marq skills --stale` reports overdue skills.
disable-model-invocation: true
metadata:
  internal: true # maintainer workflow, not part of the pack
---

Run the periodic review sweep of the `skills/` pack. Today's date is the review date.

1. **What's due.** Run `go run ./cmd/marq skills --stale` and note the list. A full sweep reviews every skill anyway; the list says which ones are overdue.

2. **Sweep in parallel** — spawn two general-purpose agents in one message, each with the date, this repo path, and these rules:
   - Directories: agent A `skills/{standards,grc,ciso,enablers,resilience,physical-human}/`; agent B **every other directory under `skills/`** (list them with `ls skills/` so a new category is never skipped).
   - Find content outdated as of today: regulatory dates and application status (CRA, NIS2 transposition, DORA, AI Act, GDPR/Digital Omnibus, US state privacy, SEC/CIRCIA/CMMC, NERC CIP, TSA SDs), standard versions (ISO 27001/27002, NIST CSF / SP 800-53, PCI DSS, SOC 2, IEC 62443, CIS Controls, CVSS), ATT&CK and OWASP versions, EPSS/NVD/KEV, tool flags, dead feed/API URLs, and marq tool names that no longer exist in `internal/registry/*.go`.
   - **Verify every change against a primary or authoritative source (WebSearch/WebFetch). Never edit from memory.** If unverifiable, don't change it — list it.
   - Minimal, surgical edits in place; keep frontmatter, style and the agentskills.io rules (name == directory, description 1-1024 chars in third person saying what the skill covers and "Use when ...", double-quote a description containing `: `). Don't restructure or add skills. Don't commit.
   - Report per file: one line per change with the source URL, then the unverified suspects.

3. **Review the diff** (`git diff skills/`) and resolve anything the agents flagged as unverified with the user.

4. **Bump review dates** for every skill the sweep covered, and the pack version:

   ```bash
   d=$(date +%F)
   v=$(date +%Y).$((10#$(date +%m))).$((10#$(date +%d)))   # semver: no leading zeros
   find skills -name SKILL.md -exec sed -i '' "s/^  verified: \".*\"/  verified: \"$d\"/" {} +
   sed -i '' "s/\"version\": \".*\"/\"version\": \"$v\"/" skills/.claude-plugin/plugin.json
   ```

   (GNU sed: drop the `''` after `-i`.)

5. **Gates:** `go vet ./... && go test ./... && bash scripts/e2e.sh`, `go run ./cmd/marq skills --stale` (expect 0), `claude plugin validate . && claude plugin validate ./skills`, the official validator (`pip install "git+https://github.com/agentskills/agentskills#subdirectory=skills-ref"` in a venv, then `skills-ref validate` on every `skills/*/*/`), and `npx -y skills add ./ --list </dev/null` must report every skill with nothing skipped.

6. **Release:** commit on a branch (`skills: <month> review sweep` with the per-file change list in the body), merge to main locally, and tag `pack-<date>`. Leave pushing (commits and tag) to the user.
