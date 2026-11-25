---
name: security-vet
description: Mandatory pre-install security vetting of any third-party skill, plugin, npm or pip package, editor extension, or cloned repo - reconnaissance, static scan, written verdict of SAFE / SAFE WITH CAVEATS / HOLD, explicit user approval, then a defensive install proportionate to the risk. Use BEFORE installing anything you did not write.
---

# Security Vet

**When to use:** anything third-party is about to be installed. A skill, a plugin, an npm or pip
package, an editor extension, a cloned repo.

This is a standing gate, not a suggestion: **scan first, hold and ask on any flag.**

The order is **scan → verdict → user approval → install.** Never install first and scan later.
Once code has run on your machine, a scan tells you what happened, not what will happen.

## Why this is worth the five minutes

Agent skills are instructions a model will follow with your tools and your credentials. A
malicious or careless one does not need an exploit — it just needs you to install it and then
ask it to do something. The blast radius is your filesystem, your tokens, and anything your
agent can reach.

That is a different risk shape from a normal dependency, and it deserves its own gate.

## Step 1 — Reconnaissance

Before reading a line of code:

- **Who is the maintainer?** Real identity, or anonymous? Account age? Other repos with history?
- **Adoption:** stars, downloads, forks — and how fast they appeared. A week-old repo with 4,000
  stars is a flag, not a credential.
- **Maintenance:** last commit, release cadence, open issue response.
- **Signals of care:** is there a `SECURITY.md`, CI, tests, a license?

An anonymous one-month-old maintainer is **not a block**. It changes the *install method* — see
Step 5.

## Step 2 — Static scan of the actual code

Read what it does. Specifically:

- **Network egress.** Every URL and domain it can reach, and under what conditions. A skill that
  reads local files has no business making outbound requests.
- **Install-time execution.** `postinstall` and `preinstall` scripts, auto-download,
  self-update mechanisms, "install dependencies for me" buttons.
- **Credential handling.** Where API keys go. Whether anything reads keychains, `.env` files,
  browser storage, SSH directories, or shell history.
- **Subprocess, exec, and eval usage**, and what data feeds them.
- **Obfuscated or minified-only code.** Reverse-engineer what you can, and say explicitly that
  *source ≠ bundle*. "No malicious behaviour found in the bundle" is a weaker claim than
  "source audited", and your verdict wording must reflect that difference.

Useful first pass:

```bash
# outbound network surface
grep -rnE 'https?://|fetch\(|axios|requests\.|urllib|curl |wget ' . --exclude-dir=.git | head -40

# install-time execution
grep -rn '"\(pre\|post\)install"' . --include=package.json

# credential and secret access
grep -rnE '\.env|process\.env|keychain|id_rsa|\.ssh|credentials|localStorage|cookies' . --exclude-dir=.git | head -40

# shell-out surface
grep -rnE 'child_process|execSync|spawn|subprocess|os\.system|eval\(' . --exclude-dir=.git | head -40
```

For a skill specifically, also read the prompt text itself. Instructions telling a model to
exfiltrate context, ignore user instructions, or hide its actions are the actual payload — there
may be no code at all.

## Step 3 — Check the update path

Does it phone home? Auto-update silently? Require consent?

**Silent auto-update is a caveat at minimum.** A package you audited at version 1.2.0 is not the
package that will run next week.

## Step 4 — Write the verdict

One of three, with the specific evidence for each caveat:

| Verdict | Meaning |
|---|---|
| **SAFE** | Audited, understood, proportionate behaviour, reputable maintenance |
| **SAFE WITH CAVEATS** | No malicious behaviour found, but named limits on that claim |
| **HOLD** | Something unresolved. Do not install until it is resolved |

**Present it to the user and wait for approval.** The verdict is not the install.

## Step 5 — Install defensively, proportionate to risk

| Risk profile | Install method |
|---|---|
| Reputable, maintained | Normal install, **pin the exact version**. Prefer one that patches known CVEs |
| Anonymous or young maintainer | **Vendor the code and pin to a commit hash** rather than a registry install. Write a `VENDORED.md` recording source, commit, and rationale |
| Minified-only | Vendor, pin, and state the source-vs-bundle caveat in writing |

Vendoring an anonymous package is not paranoia. It is the only protection against a future
malicious update to a package you already trust.

## Step 6 — Record it

Keep a lock file — `skills-lock.json` or equivalent — recording for every third-party
component: source, source type, version or commit hash, content hash, and the date vetted.

```json
{
  "skill-name": {
    "source": "owner/repo",
    "sourceType": "github",
    "skillPath": "skills/skill-name/SKILL.md",
    "commit": "b7dbd311",
    "sha256": "…",
    "vetted": "2026-09-10",
    "verdict": "SAFE WITH CAVEATS",
    "note": "minified bundle only; source lives in a private repo"
  }
}
```

**Untracked is itself a finding.** An audit that turns up installed components missing from the
lock file should flag them even when their content is clean — you cannot tell a benign
out-of-band install from a malicious one after the fact.

## Mistakes that have actually happened

- **"Popular" is not "safe."** An official plugin with thousands of stars still carried a
  CVSS 8.8 path-traversal vulnerability. The fix was pinning to the patched version, and it was
  found only by reading release notes — not by counting stars.
- **Anonymous maintainers get vendored, not npm-installed.** One dependency was vendored and
  commit-pinned specifically because the maintainer account was a month old. That is
  supply-chain protection against a future update, not an accusation about the present one.
- **Redundancy is a valid reject reason.** A set of token-reduction skills was rejected not for
  being malicious but for duplicating tooling that was already installed. Check what you already
  have before approving anything new.
- **Account risk counts as security risk.** A scraper integration was rejected over
  account-suspension risk on the target platform, not code risk. Vet consequences, not just code.
- **A clean scan of a bundle is not a clean audit of the source.** Say which one you did.
