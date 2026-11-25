---
name: github-publish
description: Take a local project public safely - sweep for secrets including the full git history, harden real weaknesses like plaintext credentials, strip copyrighted and bloat files, write a README from verified claims only, and enable repo security features. Use when asked to publish, open-source, or push a project to GitHub.
---

# GitHub Publish

Publishing is irreversible. A secret pushed to a public repo is compromised the moment it lands,
and deleting the commit does not un-compromise it — it is already in forks, mirrors, and
scrapers within minutes.

So the sweep comes first, every time, and the push is the last step.

## Step 1 — Secret sweep, before anything else

**The working tree is not enough. Check the full history.**

```bash
# every file ever committed that looks like a secret carrier
git log --all --name-only --pretty=format: | sort -u | grep -iE '\.env|\.pem$|\.key$|id_rsa|credentials|secrets?\.(ya?ml|json)'

# high-signal patterns across all history
git grep -nE '(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)' $(git rev-list --all) 2>/dev/null | head -20

# working tree
grep -rnE '(api[_-]?key|secret|password|token)\s*[=:]\s*["\x27][^"\x27]{12,}' . --exclude-dir=.git --exclude-dir=node_modules | head -20
```

A dedicated scanner such as `gitleaks detect --no-git=false` is worth running as well. Do not
rely on it alone; do not skip it either.

**If the history is dirty, it must be rewritten or the repo re-initialised before pushing.**
There is no "we'll clean it up after" option here.

Then confirm:

- `.env` is gitignored, and only `.env.example` with empty labelled keys is public
- Code reads keys from the environment. No hardcoded credentials anywhere
- A `.gitignore` appropriate to the language exists at all

## Step 2 — Harden what the sweep exposes

Publishing forces the security bar up, and that is a feature. Fix what you find:

- Plaintext passwords → salted hashes
- Database credentials → environment variables
- Overly-permissive CORS, debug modes, default admin accounts left on

Treat every publish as a security review of the code, not only of the secrets.

## Step 3 — Strip what does not belong

- **Copyrighted material.** Cite it, do not commit it. A base research paper gets a citation and
  a link, not a PDF in the repo. Check dataset licenses; permissively-licensed data is fine
  **with attribution**.
- **Bloat.** Duplicate archives, build artifacts, scratch and extraction directories. Extract
  what you need, delete the scratch, never commit it.
- **Anything personal that is not the point of the repo.** Local paths with your username,
  private notes, screenshots with credentials or personal data in them.

## Step 4 — Write the README from verified claims only

What it is, the honest headline result, the stack, and how to run it.

**Real shipped claims only.** If a number is illustrative or seeded rather than measured, label
it as such on the page. Presenting example figures as real usage is the same failure as
fabricating them.

## Step 5 — Name it properly the first time

Descriptive kebab-case. `vehicle-co2-emission-prediction`, not `project1`. Bad names stick, and
renaming later breaks every link anyone has shared.

## Step 6 — Publish, then verify the remote

Create the repo with a clear description. Push. Then **browse the pushed tree and confirm it is
clean.** Do not assume the ignore rules worked — look.

## Step 7 — Repo hygiene

- Enable Dependabot alerts and automated security fixes
- Add `SECURITY.md` with a reporting path
- Add a `LICENSE`. An unlicensed public repo is legally "all rights reserved", which means
  nobody can use it, which defeats the point
- Enable branch protection on the default branch if others will contribute
- Consider release tags, so people can pin rather than track a moving `main`

## Step 8 — Close the loop

Update your own notes or knowledge base with the repo status and URL. A publish that is not
recorded is invisible to every future session.

## Mistakes that have actually happened

- **A live API key sat in a `.env` in a project queued for publishing.** It was caught by the
  sweep and the project stayed unpublished until verified clean. Never publish on the assumption
  the ignore rule works — verify staging *and* the remote after pushing.
- **Plaintext passwords in a database-backed project** were found at publish time and converted
  to salted hashes. The publish is what surfaced them.
- **150MB of duplicate zip archives** were dropped pre-publish, and a 94MB scratch directory was
  deleted afterward. Both would have been permanent in the history.
- **A copyrighted base paper** was excluded and cited instead. Do not push other people's PDFs
  or datasets without reading the license.
- **`project1`** had to be renamed later. Name it properly the first time.
