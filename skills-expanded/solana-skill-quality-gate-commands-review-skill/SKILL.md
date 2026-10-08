---
name: review-skill
description: >
  Run a quality, safety, and merge-readiness audit on a Solana AI Kit skill
  and get a go/no-go recommendation for PR submission.
---

# /review-skill <path>

Audit a Solana AI Kit skill and get a submission-readiness verdict.

## What It Does

1. Runs `node scripts/skillqa.mjs audit <path>`
2. Summarizes findings in plain English
3. Lists blockers (must-fix errors)
4. Lists top 3 improvements
5. Gives a final verdict: **READY** / **FIX FIRST** / **DO NOT SUBMIT**

## Supported Layouts

```
<repo>/skill/SKILL.md    # Solana AI Kit repo layout
<skill-root>/SKILL.md    # Standalone skill layout
```

## Example Output

```
Skill: solana-nft-verifier
Score: 91/100 (Excellent)

Blockers: None

Top 3 Improvements:
1. Add examples/ directory with sample outputs
2. Add GitHub Actions CI workflow
3. Consider adding command definitions

Verdict: ✅ READY — This skill is submission-ready.
```

## Safety

- Does NOT execute any code from the audited skill
- Does NOT run install.sh or test scripts
- Read-only file scanning only
- No network calls
