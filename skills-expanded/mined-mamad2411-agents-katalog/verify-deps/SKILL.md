---
name: verify-deps
description: Verify that requirements.txt, constraints.txt, and pyproject.toml are mutually consistent, and that every place in the repo describing current pin versions (comments in those files, README's Known Issue section, docs/SECURITY_AUDIT.md, other skill docs) still matches reality — no unbumped pins, no stale "current" claims left over from a prior fix. Use when asked to "verify deps", "check dependency consistency/accuracy", before a release, or periodically as a drift check. Distinct from deps-security-refresh (bumping pins / triaging new CVEs) — this skill makes no version changes, only catches and fixes documentation drift.
---

# verify-deps — dependency-file consistency and drift check

This is a **read-and-reconcile** skill, not a bump skill. Nothing in this repo's
dependency *pins* should change when you run it — only stale comments, docs, and skill
text that no longer match the pins should. Two real bugs motivate this:

- `pyproject.toml` shipped a comment claiming transformers was "Capped at <4.45" in the
  same commit (`9e5f8ff`) that its `dependencies` list already said
  `transformers>=4.53.0,<5.0.0` — self-contradictory from day one, never caught because
  nobody diffed the comment against the line six lines below it.
- Two skill docs (`deps-security-refresh`, `insight-optimize`) described
  `accelerate==0.34.2` as "the current" `constraints.txt` pin over a month after it was
  fixed to `1.14.0` in commit `312096b` — the fix shipped, the *narrative about the fix*
  didn't get updated everywhere it was duplicated.

Both bugs were **accurate when written, wrong by the time anyone read them again**.
That's what this skill hunts for.

## Step 1 — Cross-check the three source-of-truth files

Read all three in full:

- `requirements.txt` — ranges (`>=`, `<`) + `DEPENDENCY NOTES` comment block
- `constraints.txt` — exact `==` pins + comment block
- `pyproject.toml` `[project] dependencies` — ranges, must be **identical** to
  `requirements.txt`'s ranges (same packages, same bounds, same order is nice-to-have
  but not required)

For every package, check by hand (don't eyeball — actually compare the numbers):

1. Does `pyproject.toml`'s range match `requirements.txt`'s range exactly?
2. Does `constraints.txt`'s `==` pin satisfy both ranges (`>=` floor and `<` ceiling)?
3. Is any package present in one file but missing from another?

If you find a mismatch, the fix is almost always to `constraints.txt` or one comment —
**do not** widen/narrow a range to make a mismatch disappear; that's a behavior change
and is ask-first per CLAUDE.md §6. Report the mismatch and stop if the right fix isn't
obviously "the comment is wrong."

## Step 2 — Hunt for stale version claims repo-wide

The bug pattern is always the same shape: a comment or doc asserts "the current pin is
X" and X used to be true. Grep the whole repo — not just the three dependency files —
for both the *current* pinned versions and every version this repo has ever pinned and
moved away from:

```bash
grep -rn "4\.44\.2\|3\.0\.1\|<4\.45\|0\.26\.0\|0\.34\.2\|3\.4\.1\|4\.53\.0\|<5\.0\.0\|1\.14\.0" --include='*.md' --include='*.toml' --include='*.txt' .
```

(That list is this repo's known historical pins as of 2026-08 — `transformers` capped
at `<4.45`, `transformers==4.44.2`, `sentence-transformers==3.0.1`,
`accelerate==0.26.0`, `accelerate==0.34.2`, `sentence-transformers==3.4.1`,
`transformers==4.53.0` / `<5.0.0`, `accelerate==1.14.0`. If
`constraints.txt` has moved further since this skill was written, extend the
grep with whatever pin it now shows.)

For every hit, read the surrounding paragraph and classify it:

- **Historical / diff context** (a changelog entry, a "Hardened Manifest Changes
  Applied" diff block, a "previously pinned" or "fixed in commit X" sentence) — fine,
  leave it.
- **Asserted as current state** ("the current constraints set...", "pins X", with no
  past-tense marker) — this is the bug. Reword to past tense, name the fixing commit if
  `git log -S"<old-version>"` finds one, and state what the pin actually is now.

Known places this has bitten before — always check these even if the grep above comes
back clean, since new drift accumulates in the same spots:

- `pyproject.toml`'s dependency comment block
- `README.md`'s "Known Issue" sections (`ModelLoadError`, `TorchTensorParallelPlugin`)
- `docs/SECURITY_AUDIT.md`'s executive summary and addenda
- `.claude/skills/deps-security-refresh/SKILL.md` and
  `.claude/skills/insight-optimize/SKILL.md` — both narrate specific pin numbers

## Step 3 — Verify the install and the compatibility triangle

Don't take the files' word for it — prove they actually resolve together, in a clean
Python 3.12 venv (and 3.13 if available, matching the CI matrix):

```bash
python3.12 -m venv /tmp/depcheck && /tmp/depcheck/bin/python -m pip install --upgrade pip
/tmp/depcheck/bin/python -m pip install -r requirements.txt -c constraints.txt
/tmp/depcheck/bin/python -m pip install -e .
/tmp/depcheck/bin/python - << 'EOF'
import accelerate, sentence_transformers, transformers
print("transformers", transformers.__version__)
print("sentence-transformers", sentence_transformers.__version__)
print("accelerate", accelerate.__version__)
from accelerate import init_empty_weights
from accelerate.utils import TorchTensorParallelPlugin
from sentence_transformers import SentenceTransformer
print("triangle OK")
EOF
```

CI never runs this combination — `.github/workflows/ci.yml` installs with
`pip install -e ".[dev]"`, **no** `-c constraints.txt`, so a broken constraints pin (like
`accelerate==0.34.2` was) is invisible to CI and only surfaces for someone who follows
the README's documented install command. This step is the only thing that catches that
class of bug — don't skip it because "CI is green."

## Step 4 — Confirm the four CI gates still pass

Comment-only edits shouldn't break anything, but prove it — install dev deps in the same
venv and run all four gates, on 3.12 and 3.13 if both are available:

```bash
/tmp/depcheck/bin/python -m pip install -e ".[dev]"
/tmp/depcheck/bin/ruff check src/ tests/
/tmp/depcheck/bin/ruff format --check src/ tests/
/tmp/depcheck/bin/mypy src/insight_extractor
/tmp/depcheck/bin/pytest tests/unit/ -v --tb=short
```

## Step 5 — Optional: spot-check pip-audit against the pinned environment

This is a lighter touch than `deps-security-refresh`'s full CVE triage — you're checking
whether `docs/SECURITY_AUDIT.md`'s finding set has silently gone stale, not doing new
reachability analysis.

```bash
/tmp/depcheck/bin/pip install pip-audit
/tmp/depcheck/bin/pip-audit
```

Compare the finding IDs against `docs/SECURITY_AUDIT.md`'s tables. If the set is
unchanged, nothing to do. If there's a **net-new** ID not listed anywhere in the doc,
add one factual line noting it exists (ID + fix version, no verdict) to the existing
"not yet triaged" addendum — do **not** write a reachability verdict or touch a pin;
assigning a verdict is a `deps-security-refresh` job and is out of scope here. If
findings *disappeared* from what's documented, leave the doc alone (it's describing
history, not a live claim) unless the disappearance means a documented "unreachable" CVE
is now moot — flag that for the owner rather than deleting the row yourself.

## Step 6 — Commit

Only if Steps 1-2 found real drift (most runs, especially soon after this skill is
created, should find nothing — say so and stop):

```
fix: <one-line summary of the drift found>

- <file>: <what was stale> — root cause / when it went stale (commit if found via
  `git log -S`)
- <file>: <what was stale> — ...

<constraints/requirements/pyproject bounds were already mutually consistent — only
docs/comments drifted, if that's the case; otherwise state what numeric mismatch was
found and how it was resolved>

Verified: clean venv install (3.12[, 3.13]), compatibility triangle, ruff check, ruff
format --check, mypy --strict, pytest tests/unit/ (<N>/<N> passed). Integration tests
skipped — no model download in this environment.
```

No pin in `requirements.txt`, `constraints.txt`, or `pyproject.toml` should appear in
this diff unless Step 1 found an actual mismatch between the three files (not just a
stale comment) — that case is rare and worth double-checking against CLAUDE.md §6
before touching a version number.

## Full checklist

- [ ] Every package's range identical between `requirements.txt` and `pyproject.toml`
- [ ] Every `constraints.txt` `==` pin satisfies both files' ranges
- [ ] No package missing from any of the three files
- [ ] Repo-wide grep for historical pin numbers run; every hit classified
      historical-context vs. asserted-as-current
- [ ] `pyproject.toml` comment block, README Known-Issue section,
      `docs/SECURITY_AUDIT.md`, and both dependency-aware skill docs checked by hand
- [ ] Clean-venv install with `-c constraints.txt` succeeds
- [ ] transformers/accelerate/sentence-transformers triangle imports cleanly
- [ ] Four CI gates green (3.12, and 3.13 if available)
- [ ] `pip-audit` spot-checked against documented findings; any net-new ID logged
      factually, no verdict assigned
- [ ] `git diff --stat` contains no pin changes unless Step 1 found a real mismatch
- [ ] Report states plainly if nothing was found to fix — a clean pass is a valid,
      useful outcome, not a failure to find something
