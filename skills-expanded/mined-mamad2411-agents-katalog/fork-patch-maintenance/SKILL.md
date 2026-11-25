---
name: fork-patch-maintenance
description: >-
  Maintain local patches against an active upstream fork. Covers divergence
  tracking, patch integrity verification, conflict-zone analysis, rebase
  complexity assessment, and escalation tracking across pulse cycles.
version: 1.5.0
author: Hermes Agent (Forge)
metadata:
  hermes:
    tags: [fork, divergence, rebase, patches, git, upstream, maintenance, pulse]
    triggers: [divergence-check, patch-integrity, rebase-complexity, upstream-conflict, upstream-subsystem-strip, fork-assessment, behind-count, local-patches, upstream-module-extraction]
    related_skills: [recurring-status-checks, github, karpathy-principles]
---

# Fork Patch Maintenance

> Periodic assessment of local patches against an active upstream. Use when
> maintaining a fork with N local commits that must survive upstream evolution.

## When to Run

- Every pulse/recurring-status-check cycle when maintaining a fork
- When divergence reaches 150+ behind `origin/main`
- When upstream refactors files where local patches live
- After a branch reset or force-pull (verify patches survived)
- Before a rebase or merge attempt

## Assessment Sequence

### 1. Baseline Metrics

```bash
cd <fork-root>
git fetch origin
echo "--- DIVERGENCE ---"
echo "Ahead:  $(git rev-list --count origin/main..HEAD)"
echo "Behind: $(git rev-list --count HEAD..origin/main)"
echo "--- WORKING TREE ---"
git status --short
echo "--- STASH ---"
git stash list
```

### 3. Upstream Activity Window

```bash
# All new commits since last-pulse marker
git log --oneline origin/main --since="<last-pulse-datetime>" | head -30
echo "Total: $(git log --oneline origin/main --since='<last-pulse-datetime>' | wc -l)"
```

Scan for:
- Commits touching files where local patches live
- God-file refactors (any 1000+ line file with -200+ net change)
- Structural changes (function renames, param changes, import removals)

### 3a. God-File Size Trend Tracking

Track local vs upstream sizes as a proxy for conflict surface area:

```bash
echo "=== LOCAL GOD-FILES ==="
wc -l gateway/run.py tools/mcp_tool.py hermes_cli/web_server.py tools/approval.py
echo "=== UPSTREAM GOD-FILES ==="
git show origin/main:gateway/run.py | wc -l
git show origin/main:hermes_cli/web_server.py | wc -l
```

Record per-cycle to detect widening gaps. Large deltas (>500 lines in either direction) signal structural change — escalate to 🔴.

### 3. Patch-Zone Conflict Assessment

For each file with local patches, check if upstream touched overlapping zones:

**a) File-level diff scan:**

```bash
git diff --stat origin/main -- <patched-file>
```

Check each patched file's net change. Any file with upstream -200+ lines is a structural refactor. But also check files that DON'T appear in your local diff — upstream may have deleted entire directories your tooling depends on:

```bash
# Detect upstream directory deletions (files that exist locally but not upstream)
for f in $(git ls-files --cached | sort); do
  git show origin/main:"$f" 2>/dev/null > /dev/null || echo "DELETED UPSTREAM: $f"
done 2>/dev/null | head -20
```

**b) Purely local feature verification:**

For features you KNOW are local-only (e.g., a custom CRUD zone, a platform-specific module, a config path override), verify they have **zero presence upstream** AND check whether the parent file was structurally refactored:

```bash
# 1. Check upstream has no trace of our feature
git show origin/main:<file> | grep -c "unique_feature_identifier"
# If 0: feature is purely local — verify parent file stability (step 2)

# 2. Check whether parent file was structurally refactored
git diff --stat origin/main -- <parent-file>
# If net change is -200+ lines: upstream refactored the embedding context
# This means our insertion point may not exist upstream — guaranteed conflict
```

**⚠ CRITICAL: Zero-presence + parent-file refactor = MAXIMUM risk, not zero risk.**
A purely local feature embedded in a file that upstream heavily refactored (-200+ net lines) means the insertion point for our feature no longer exists in the upstream version. The `grep -c 0` only tells us upstream doesn't have the feature — it says nothing about whether the code AROUND the feature is intact.

**Risk matrix:**
| Feature Presence | File Stable | File Refactored |
|-----------------|-------------|-----------------|
| Exists upstream too | Normal merge risk | Conflict probable |
| Purely local (zero-presence) | 🟢 Low risk — insertion point stable | 🔴 **Maximum risk** — insertion point eroded |

**Mitigation:** Before attempting rebase, pre-extract the zero-presence feature into a standalone module. This decouples it from the file's structural evolution upstream.

This is the inverse of the patch-integrity check: instead of confirming OUR patches survive, we confirm UPSTREAM hasn't independently implemented something resembling our local feature. If they did, we may need to decide: adopt theirs, keep ours, or reconcile.

**c) Upstream commit introspection per file:**

```bash
# Upstream commits touching this specific file
git log --oneline origin/main -- <patched-file> | head -10
# Full diff context (shows OUR local changes vs upstream)
git diff origin/main -- <patched-file> | head -100
# Check net change magnitude
git diff --stat origin/main -- <patched-file>
```

**Structural complexity indicators** (elevate tier regardless of behind-count):
- Upstream -200+ line net change in same file (god-file refactor)
- Upstream removed imports, helpers, or params our patches depend on
- Upstream refactored the function signature or class our patches modify
- Multiple patched files show aggressive upstream line deletions

### 4. Patch Integrity Verification

For each critical patch, confirm the marker is present at expected position:

```bash
grep -n "unique_patch_marker" <file>
```

**Fail-fast:** If `grep` returns empty for a known marker, the patch was stripped —
the upstream commit reverted or overwrote it. Flag immediately at 🔴 level.

### 4a. Upstream Mirror-Fix Detection (Cosmetic vs Real)

Upstream may appear to have adopted your patch — same comment, same intent — without actually changing behavior. A comment-only "fix" that sounds identical to your patch is a **trap**: it makes a rebase feel safe while silently re-introducing the original bug.

**Checklist to distinguish cosmetic from real:**

```bash
# Step 1: Does upstream have the SAME marker/flag your patch introduced?
git show origin/main:<file> | grep -c "_permanent_allowlist_loaded"  # or your flag
# 0 = upstream doesn't have your flag at all
# >0 = upstream has the marker (check if it's a real flag or just in a comment)

# Step 2: Does upstream still call the OLD function at module import time?
git show origin/main:<file> | grep -c "load_permanent_allowlist()"
# If this returns >0 AND the comment says "loaded lazily", it's COSMETIC.
# Upstream changed the comment but NOT the import-time behavior.

# Step 3: Compare the module-bottom lines:
git show origin/main:<file> | tail -5
# vs your local:
tail -5 <file>
```

**Real (behavioral change):** Upstream moved the function call into a guard, added a flag, restructured initialization — the lazy behavior actually works.

**Cosmetic (comment-only):** Upstream added a comment saying "loaded lazily" but `load_permanent_allowlist()` is still called unconditionally at module scope. The function runs at import time, defeating the stated intent.

**Why this matters:** On rebase, a cosmetic comment change creates a false sense of safety. If you skip your patch because "upstream already has it," the original problem (e.g., test pollution from module-level config reads) silently returns. Always verify behavioral change, not textual similarity.

See **`references/upstream-cosmetic-patch-detection.md`** for the full live case study from the 1881-behind Hermes Agent pulse.

**⚠ Inverse pattern: upstream independently solves same problem, differently.**
Upstream can add a real behavioral fix for the same bug you patched, but with a completely different approach. This creates a **conflict of approaches** on rebase — both your patch AND upstream's fix exist, but they overlap.

```bash
# Check if upstream already fixed the same area
git diff origin/main -- <patched-file> | grep -B5 -A15 "os.path\|normpath\|realpath\|as_posix\|replace.*\\\\\\\\"
# Compare approaches side by side. Decide: does upstream's approach work for
# ALL our platforms? Is it more correct? Less correct?
```

**Rebase decision matrix:**
| Situation | Rebase Strategy |
|-----------|----------------|
| Upstream's fix is better/complete | Drop your patch, adopt upstream's version |
| Your fix is better or covers cases upstream missed | Keep your patch, it will conflict — resolve by keeping yours with upstream's additions |
| Both are partial | Merge both approaches — your edge case + upstream's edge case |

See **`references/upstream-mirror-patch-conflict.md`** for the Hermes Agent case study where upstream added cross-platform path normalization in `_is_verification_artifact_cleanup()` that overlaps with our Windows path fix.

### 4b. Behavioral Drift Detection

Beyond textual conflicts, check for **runtime behavioral differences** between local and upstream that no merge analysis can detect:

```bash
# Spot unexpected default value differences
git diff origin/main -- <patched-file> | grep -E "default=|timeout=\d+|return \d+"
```

When you find a behavioral difference, trace its origin:
```bash
git log -p -S "<identifier-or-value>" -- <patched-file>
```

See **`references/behavioral-drift-detection.md`** for the full technique chain with the concrete approval-timeout example from the 1025-behind pulse.

### 4c. Complexity Escalation Ladder

| Tier | Condition | Effort | Action |
|------|-----------|--------|--------|
| **🟢 Nominal** | 0-150 behind, zero file overlap | ~5 min | Cherry-pick or rebase normally |
| **🟡 Moderate** | 150-400 behind, overlapping files but different zones | 15-30 min | Manual conflict resolution, moderate |
| **🔴 Complex** | 400-800 behind, overlapping line zones | 30-60 min | Manual resolution for 1-2 files |
| **🔴 Critical** | 800+ behind OR any structural god-file refactor (-200+ lines) affecting patch zones OR upstream deleted dependencies/directories your patches reference | 2-4 hours | Multi-file structural reconciliation — plan dedicated session |
| **🔴 Critical (directory-level)** | 1000+ behind AND upstream deleted entire directories (`dashboard_auth/`, etc.) AND upstream -2400+ line CL-level removals (`main.py`, `config.py`) affecting multiple patched files | 4+ hours | Structured multi-phase rebase — re-apply patches one at a time against the refactored upstream, verifying each against a fresh test run. Treat CL-level removals as a "rebase onto a different architecture" event, not a merge. |
| **❌ Emergency** | 1000+ behind AND god-file rewrites AND lost patches | 4+ hours | Full recovery — consider re-implementing patches on fresh merge-base |

**⚠ Critical insight:** Tier escalation is NOT linear by behind-count alone.
A **Critical** tier can trigger at 400 behind if upstream refactored the
same files you patched (e.g. -629 lines in web_server.py). Always assess
by file-level conflict risk, not just the behind count.

**⚠ Directory-level critical trigger:** Upstream can escalate from `*` to
`**` tier WITHOUT touching any of your patched files — by deleting
dependencies, utility modules, or config files that your patches import.
Check for directorate-level deletions even when your patched files show
zero diff stat. See the `hermes_cli/` restructuring case study reference.

### 4d. Upstream-Only Commit Detection (Missing Fixes & Security Gaps)

The standard patch-integrity check answers "are our patches intact?" This section answers the inverse: **"what important upstream commits are we missing?"** — performance fixes, security hardening, and behavioral improvements that exist on origin/main but not in our local branch.

**a) Ancestry check for known important commits:**

When upstream lands a fix you know about (from pulse cross-referencing or release notes), verify it's reachable from HEAD:

```bash
git merge-base --is-ancestor <upstream-commit> HEAD && echo "IN BRANCH" || echo "NOT IN BRANCH"
```

Example from the Hermes Agent 1978-behind pulse: Teknium's CDP URL startup-fix (`731aa0ccc9`, split `_get_cdp_override` into raw-vs-HTTP variants to avoid 15s blocking socket connects at startup). The ancestry check revealed the commit exists on origin/main but is **NOT reachable from HEAD** — a genuine performance gap that must be cherry-picked or included in the next rebase.

**b) Security hardening gap scan:**

Upstream may add security-critical lines to files you also patch (e.g. `build_write_denied_paths()` in `file_safety.py`). These additions happen on origin/main after your fork point, so your local branch silently lacks them.

Scan for this by diffing upstream vs local on security-sensitive files and looking for lines that only exist upstream:

```bash
# Check if upstream added lines that don't exist locally
git diff origin/main -- agent/file_safety.py | grep -E "^\+" | grep -i "bws\|cache\|token\|secret\|credential" | head -10
# Verify these lines are actually present upstream but absent locally
git show origin/main:agent/file_safety.py | grep -n "bws_cache.enc.json"
grep -c "bws_cache.enc.json" agent/file_safety.py || echo "0 (MISSING!)"
```

**Key indicators of a security gap:**
- Upstream added file-path entries to `build_write_denied_paths()` or similar allow/deny lists
- Upstream added credential/token scrubbing patterns
- Upstream added encrypted cache protection lines (e.g. `bws_cache.enc.json` replacing `bws_cache.json`)
- Upstream hardened path normalization or injection guards

**c) Performance fix discovery:**

Beyond known commits, discover performance fixes by scanning upstream commit subjects for perf-related keywords that touch files in your patch zone:

```bash
git log --oneline origin/main --not HEAD --since="<last-pulse>" | \
  grep -iE "perf|startup|slow|stall|timeout|latency|cdp|blocking|10\+"
```

A match with no corresponding local commit suggests a performance regression risk on next rebase if the fix touches overlapping code.

**d) Upstream sprint characterization (trajectory analysis):**

For pulse reports, characterize the upstream commit batch to communicate what direction upstream is moving. Scan the commit window and categorize:

```bash
# Count by category
git log --oneline origin/main --not HEAD --since="<last-pulse>" > /tmp/upstream.txt
echo "Total commits: $(wc -l < /tmp/upstream.txt)"
echo "--- Desktop/Tauri: $(grep -ci 'desktop\|tauri\|pane\|tab\|sidebar\|composer\|status.bar' /tmp/upstream.txt)"
echo "--- God-file refactors: $(grep -ci 'refactor\|remove.*line\|strip\|delete' /tmp/upstream.txt)"
echo "--- Bug fixes: $(grep -ci 'fix(' /tmp/upstream.txt)"
echo "--- Features: $(grep -ci 'feat(' /tmp/upstream.txt)"
```

This helps the pulse report distinguish a "desktop platform build-out sprint" from a "god-file refactor sprint" — each has different implications for rebase complexity.

**e) Update pulse report template:**

After an upstream-only commit detection cycle, structure the pulse findings like:

```
- 🔴 CDP URL startup fix (731aa0ccc9) NOT in our branch — stale endpoint = 15s startup stall
- ⚠️ Bitwarden bws_cache.enc.json security gap — 2 lines upstream added, we lack
- 🟢 Upstream desktop sprint (36 commits) — sustained feature build-out, no conflict overlap
```

See **`references/upstream-only-commit-detection.md`** for the full 1978-behind Hermes Agent case study with CDP ancestry check, Bitwarden gap scan, and desktop sprint characterization.

### 4e. Cherry-Pick Application & Verification

When you've identified an upstream-only commit worth having now (performance fix, security hardening, or a clean bugfix that cherry-picks cleanly), apply and verify it immediately rather than waiting for a full rebase.

**a) Pre-apply check (is it safe?):**

```
git diff <upstream-commit>^..<upstream-commit> --stat
```

Look for: few files (<10), small diff (<200 lines), no new imports/modules. Red flags: >200 lines, 10+ files, interface/API changes, new dependencies. Small, focused performance/security fixes (split one function, touch 3-6 files with +50/-20 each) are ideal candidates. Structural refactors, new features, or interface changes should wait for the full rebase.

**b) Apply the cherry-pick:**

```
git cherry-pick <upstream-commit>
```

If clean: the commit message and authorship are preserved — ideal for attribution tracking. If conflicts: abort (`git cherry-pick --abort`) and defer to the full rebase. Don't force-resolve in isolation — the conflict patterns inform the rebase plan.

**c) Verify targeted tests pass:**

```
git diff --name-only HEAD~1 | grep "tests/"
python -m pytest <touched-test-files> -x -q --no-header
```

This catches silent regressions that a textual merge would miss. The upstream commit was tested against origin/main's base, not your fork's state — running its tests confirms it plays well with your local patches.

**d) Verify divergence didn't increase:**

```
echo "Ahead: $(git rev-list --count origin/main..HEAD)"
echo "Behind: $(git rev-list --count HEAD..origin/main)"
```

If Behind stayed the same and Ahead incremented by 1: clean apply. If Behind also changed: upstream moved during the cherry-pick window — re-fetch and reassess.

**e) Record in pulse report:**

When the cherry-pick lands successfully, the next pulse should update: (1) the carried-forward section to cross off the item (e.g. "✅ CDP URL startup fix now cherry-picked"), (2) the ahead count (N+1), (3) test results to show regression-free.

**f) When to skip and defer to full rebase:**

- **Any conflict** — abort. A simple conflict often masks deeper structural divergence the rebase will handle comprehensively.
- **Dependency chain** — if the commit depends on earlier upstream commits not in your branch, cherry-picking creates incomplete state.
- **Test failures** — a behavioral dependency on some upstream change you lack. Abort and defer.

**Real example** — Hermes Agent 2274-behind fork (Jul 28 2026):

```
git cherry-pick 731aa0ccc9     # Clean — auto-merged 2/6 files
python -m pytest tests/tools/test_browser_cdp_tool.py \
  tests/tools/test_browser_hybrid_routing.py \
  tests/tools/test_browser_lightpanda.py -x -q --no-header
  # → all 91 passed (26 cdp + 39 hybrid + 26 lightpanda)
```

This pattern (detect → ancestry-check → diff-inspect → cherry-pick → test → record) turns a one-off action into a repeatable workflow.

### 4f. Escalation Tracking

Track divergence across consecutive pulse cycles to detect acceleration:

| Pulse | Behind | Delta | Tier | Trend |
|-------|--------|-------|------|-------|
| T-4 | 429 | — | 🟡 | — |
| T-3 | 555 | +126 | 🔴 | ↑ accelerating |
| T-2 | 827 | +272 | 🔴 | ↑ accelerating |
| T-1 | 963 | +136 | 🔴 | ↑ still rising |

**Acceleration pattern**: If delta stays positive for 3+ consecutive pulses,
the "safe to defer" window has passed — rebase is overdue regardless of
conflict complexity.

### 4g. Upstream Subsystem Stripping Detection

Upstream may aggressively prune a file by removing entire subsystems (denial breaker, smart policy, operator policy hooks, etc.). If your patches don't touch the removed subsystems, **the intent of your patches is preserved** — but the code structure around your insertion points has shifted, creating a **stealth conflict** that standard overlap checks miss.

**Why this is dangerous:**
- The diff looks like a net-negative line change (`-300/+50`) — seemingly low risk
- But every function below the removed block shifted up by hundreds of lines
- The removed subsystem may have been referenced by functions your patches touch (imports, helpers, constants)
- On rebase, `git` merges at the line level — stripped code means your patch lines map to different upstream contexts

**Detection workflow:**
```bash
# Step 1: Identify files where upstream deleted more than they added
# (net-negative diff with non-trivial absolute change)
echo "=== NET-NEGATIVE CANDIDATES (deletions > additions by 100+ lines) ==="
for f in $(git diff --name-only origin/main..HEAD | sort -u); do
  ADD=$(git diff origin/main -- "$f" 2>/dev/null | grep '^+' | grep -v '^+++' | wc -l)
  DEL=$(git diff origin/main -- "$f" 2>/dev/null | grep '^-' | grep -v '^---' | wc -l)
  [ "$DEL" -gt "$((ADD + 100))" ] && echo "  $f: +$ADD/-$DEL (net: $((ADD - DEL)))"
done

# Step 2: Examine upstream commits for the stripped subsystem
git log --oneline origin/main -- <file> | head -15
git show <upstream-commit> -- <file> | grep -B2 "class\|def \|^# ==" | head -30

# Step 3: Check whether our patches touch the removed subsystem
git diff origin/main..HEAD -- <file> | grep -i "denial\|breaker\|_tally\|_reset\|circuit\|_policy"
# Empty = safe in intent; non-empty = our patches depended on stripped code

# Step 4: Compare function positions before vs after
echo "=== OUR PATCH HUNKS IN CURRENT FILE (candidate for shifted position) ==="
git diff origin/main..HEAD -- <file> | grep -E "^@@" | head -10
```

**Rebase resolution strategy:**
1. **Accept upstream's deletions** — do NOT try to restore the stripped subsystem
2. **Re-apply your patches onto the new file structure** — line positions differ, resolve by taking upstream's version as base, then re-introduce your changes
3. **Remove stale references** — if your patches imported or called anything from the stripped subsystem, remove those
4. **Update test assertions** that referenced the removed behavior (changed defaults, removed return values)

**Decision matrix for stripped subsystems:**

| Our Relationship | Risk Level | Rebase Strategy |
|---|---|---|
| Patches are in different functions; no import dependency | 🟡 Moderate | File rearranged — patches re-apply mechanically at shifted positions |
| Patches had stale import/reference but no behavioral dependency | 🟢 Low | Remove the reference; patches apply cleanly |
| Patches depended on stripped subsystem (new calls, new tests) | 🔴 Critical | Must reimplement the dependency or change approach |
| Tests assert the removed behavior (e.g. timeout default check) | 🟡 Moderate | Update expectations to match new upstream defaults, or gate on fork state |

**Real example — approval.py (Hermes Agent, Jul 29 2026):** Upstream commit `eff3b11eb2` removed the consecutive-denial circuit breaker (`_denial_tally`, `_record_denial`, `_reset_denials`, `_denial_breaker_addendum`), `_get_smart_policy()`, dropped `allow_session` from approval payloads, and changed default timeout 300s→60s. Our 3 local patches (lazy-init, Windows path normalization, `shlex.split` + `rm ~/`) were all in **different functions** and never touched the stripped code. However, the `allow_session` removal collapsed a 2-tier permission model we depended on, and functions like `check_all_command_guards` shifted by 100+ lines due to the deletions.

**Key insight:** A stripped subsystem is NOT the same as a phantom diff (upstream file extraction). With extraction, deleted lines moved to a new file. With stripping, they are GONE — the file is genuinely smaller. Your rebase should accept this and re-apply only your legitimate additions on top of the slimmer upstream version.

### 4h. Post-Reset Aftermath Audit (Forced Rebase / Hard Reset)

When divergence **suddenly collapses** between pulses (e.g. 4226 → 64 behind), that is NOT upstream retreating — normal upstream activity only *increases* behind-count. A collapse means someone executed a forced reset / force-pull / rebase-onto-origin. Treat it as an event requiring a full loss audit, not a measurement quirk.

**Step 1 — Reconstruct what happened via reflog (do this first, it's free):**

```bash
git reflog -15 --date=short
# Look for: "reset: moving to origin/main" — the forced reset
#           "cherry-pick: <msg>"            — restoration attempts after it
#           "commit: fix(...) restore X lost in reset" — re-created patches
```

**Step 2 — Enumerate the loss surface.** Old stack size from the last pulse log (e.g. "24 ahead") minus current `git rev-list --count origin/main..HEAD` = commits unaccounted for. `git log --oneline origin/main..HEAD` shows the restored set; any local commit from previous pulses NOT in that list is a loss candidate.

**Step 3 — Verify recoverability FIRST (cheap and decisive):**

```bash
for sha in <lost-commit-shas>; do git cat-file -t $sha && echo "$sha recoverable" || echo "$sha GONE"; done
```

After `git reset --hard`, old commits stay in the object DB (reflog keeps them alive ~90 days). **Recoverable** = cherry-pick it, or `git show <sha>:<path>` to restore a file. **GONE** (GC'd, or never committed) = re-implement from scratch — different effort class, report accordingly.

**Step 4 — Classify each lost patch: still needed, or obsoleted?**
- Grep the CURRENT tree for the patch's exact committed marker (exact form, not paraphrase — see the audit pitfall): `grep -n 'posix=(os.name != "nt")' tools/approval.py`
- Upstream may have relocated the file: `git ls-files | grep -i file_safety` (e.g. `tools/` → `agent/` move), then grep the NEW location for the marker — a moved file can carry the fix without any reset involvement.
- `git log --all --oneline -- <feature-file>` empty = the file exists in NO reachable commit → **feature regression**, not just a rebase conflict (e.g. a local-only feature upstream never had).

**Step 5 — The "lost in reset" tell.** Commits titled `fix(...): restore X lost in reset` mean the operator KNEW things were lost and restored a subset. The restored set shows what they valued; old-stack commits absent from BOTH the restored set AND the current tree are the true loss surface. Cross-check against the last pulse's "all N patches intact" list — every entry missing from both is a loss candidate.

**Step 6 — Verify uncommitted WIP in the working tree.** A hard reset leaves untracked files and in-progress modifications behind (it only moves HEAD/index). If the WIP has tests, RUN them before reporting (`python -m pytest <test-file> -q`) — a green WIP fix becomes a "commit it now before the next reset" recommendation; a red one is "investigate". A stale `.orig` merge artifact in the tree (e.g. `web_server.py.orig`, 768KB, dated weeks prior) is a clean-deletion candidate.

See **`references/post-reset-loss-audit.md`** for the Aug 4 2026 Hermes Agent worked example: reset to origin/main, 8 cherry-picks restored, 5 patches lost (all verified recoverable via `cat-file -t`), and the relocation-carried `as_posix` marker.

### 4i. Object-DB Patch Restoration (re-applying lost patches onto evolved files)

When a patch was lost in a reset but the commit SHA survives in the object DB, restore it onto the CURRENT tree — don't wait for a full rebase, and don't cherry-pick blindly onto heavily-rewritten files.

**Step 1 — Verify recoverability + read the original diff:**
```bash
git cat-file -t <sha>       # 'commit' = recoverable
git show <sha> -- <file>    # the exact original diff
```
The original commit message names the regression tests and the intent — use it as the restore spec.

**Step 2 — Map old touch points to NEW locations by symbol, not line number.**
The original diff's line numbers reference the OLD file. Grep the CURRENT tree for the symbols the diff touches (function names, flag names, markers):
```bash
grep -n "def is_approved\|def load_permanent_allowlist\|_permanent_approved" tools/approval.py
```
Upstream refactors relocate functions by hundreds of lines (this session: ~900-line upward shift after a subsystem strip). Symbol greps find the new homes.

**Step 3 — Re-apply semantics surgically with `patch`, hunk by hunk.**
On a heavily-rewritten file a cherry-pick conflicts; instead re-apply each hunk of the old diff at its NEW location, preserving the original commit's semantics (guard placement, idempotency flag, docstring intent). One `patch` call per hunk; verify lint OK after each.

**Step 4 — Run the regression tests the original commit message names:**
```bash
python -m pytest tests/acp/test_approval_isolation.py tests/tools/test_approval.py -q
```
A lost patch is only "restored" when its named tests pass on the evolved code.

**⚠ Stale-heuristic pitfall — old patch detection logic can false-positive onto NEW upstream features.** When the patch being restored contains detection heuristics (host/port matching, string containment, feature sniffing, "is this the router?" checks), those heuristics encode the upstream of the patch's era. Upstream may have since added services that match the OLD heuristic but not the patch's intent — and the false positive is silent until a real user hits it. Worked example (Aug 7 2026, OmniRoute lock `72c19a87de`): the guard's `"localhost" in current_base_url` check, written Jul 28 when a localhost custom endpoint meant OmniRoute, collided with Ollama (`localhost:11434`) added in the intervening 346 upstream commits. A `custom` provider pointed at local Ollama was treated as OmniRoute-locked: the /model picker showed only the router row and `--provider` switches were blocked. **Fix: port-scoped detection** (`"localhost:20128"`, the router's canonical port) instead of hostname-scoped (`"localhost"`). General rule: scope the heuristic to the narrowest stable discriminator — port, exact host, or a feature-only string — never a bare common hostname.

**⚠ Restore testing must include upstream's tests for the touched functions, not just the patch's own tests.** The stale heuristic above was caught by `test_list_authenticated_providers_bare_custom_slug_recovers` — an UPSTREAM regression test (for #17478) written long after the patch, exercising the same function. Running only the patch's named tests (which drive the omniroute happy path) would have passed green while the collision went unnoticed. Before committing a restore: run the patch's named tests PLUS every test file that imports the touched functions (`grep -rln "func_name" tests/`), and add a functional smoke check that exercises both the lock path AND the no-lock path (e.g. block, passthrough, custom:20128 lock, Ollama no-lock, picker-only-router). See `references/omniroute-lock-restore.md` for the full worked example.

**Step 5 — Commit with `-F` message file.** `git commit -F <msg-file>` avoids MSYS backtick/shell-quoting corruption in multi-line messages. State which original SHA you re-applied ("re-applies `<sha>` semantics") so future audits can trace lineage.

**Step 6 — Verify divergence unchanged.** Ahead +1, Behind unchanged = clean restore. Cross the item off the loss list in the pulse report.

**Restore ordering:** prioritize patches whose absence regresses tests (lazy-init → Windows test flakiness) and cheap wins (.gitignore hardening) first; defer conflict-heavy restores (features embedded in files upstream rewrote, e.g. an OmniRoute lock in `model_switch.py`) to a dedicated session.

**⚠ Half-restore pitfall — restored in the WRONG FORM.** When the working tree shows a lost feature re-added but in a different shape than the original commit (e.g. a feature originally extracted into its own module + thin god-file wrappers gets re-added as a big inline block back in the god-file, with the module and tests missing), it is a HALF-restore, not a restore. Check the object DB for the original design before accepting the working-tree form:

```bash
git cat-file -t <original-sha>                        # commit still valid?
git show <original-sha>:<path/to/extracted/module.py> # original module in object DB
git show <original-sha> -- <god-file>                 # how the original wired it (import + thin wrappers)
```

Then restore the module + tests from the object DB (`git show <sha>:<path> > path`), and convert the inline block back to the import + thin-wrapper form. Verify logic parity between the inline block and the object-DB module before replacing (extract the function bodies from both and diff — identical bodies = safe swap). The inline form regresses the original intent: god-file grows (the exact thing the extraction fixed), tests are gone, and the diff is larger. See `references/inline-vs-extracted-restore.md` for the worked example (Hermes One, Aug 7 2026).

**⚠ False-loss pitfall:** before adding a patch to the loss list, grep the WHOLE tree for its markers — audits misremember file locations. The CDP override split was declared lost after checking `web_server.py`/`tools/browser_cdp.py`, but it actually lives in `tools/browser_tool.py` (15s startup stall never returned). `grep -rn "<function-or-flag-name>" --include='*.py' .` costs seconds and prevents wasted restore work.

See **`references/object-db-patch-restoration.md`** for the Aug 5 2026 worked example (lazy-init `622c52f98` → `1950f4ebd`, 99/99 tests, evolved-file hunk mapping).

### 4j. Early Upstream Adoption (pre-rebase de-conflicting)

When upstream lands a change whose API or behavior your local code SHOULD use — a perf fix that caches something your local path still probes raw, a refactor that defines the new canonical shape of a function you touch — adopt it NOW rather than waiting for the rebase. Making that file region byte-identical to `origin/main` collapses the pending rebase conflict for the zone to context-shift grade (or eliminates it entirely). This is the "adopt upstream's approach" row of the section 4a decision matrix, executed pre-rebase instead of mid-rebase.

**a) Apply the upstream diff with a 3-way merge, not cherry-pick:**

```bash
git fetch origin
git show <upstream-sha> -- <file> | git apply --3way
```

`git apply --3way` uses the blob IDs embedded in the diff's index line, so it works even when your working tree has diverged hundreds of commits — it merges the patch against your tree instead of requiring clean context. A clean apply is expected when the changed lines exist in both versions. Use this when you want the FILE change but NOT the commit. Plain `git cherry-pick` (section 4e) remains right when you want the whole commit (message + authorship preserved).

**b) Adapt local-only code to the new upstream API — match the WIRE SHAPE.** When the local path is a probe/fetch/cache consumer and upstream just added a shared helper for it, call the new helper with the IDENTICAL argument shape the upstream call sites use — same api_key, same URL normalization, same headers (or none). Headers and credentials are usually part of the cache fingerprint: passing extra headers your sibling call site doesn't means a different fingerprint → cache miss → the perf fix silently doesn't apply. Grep the upstream call sites (`git show <sha> -- <file>`) and mirror them exactly. Check for the upstream fail-fast convention (e.g. `timeout=1.5 if for_picker else 5.0` — picker opens tolerate a short probe, full operations get the long one) and adopt it too.

**c) Bring the commit's tests with you:**

```bash
git show <sha>:tests/.../test_<new>.py > tests/.../test_<new>.py
```

Then run: (1) the new test file, (2) the surrounding suites for the touched functions (`grep -rln "func_name" tests/`), (3) a functional monkeypatch check that proves the local path routes through the new helper with the expected kwargs (patch the helper in the module it's imported from — a function-local `from X import helper` resolves at call time, so patching `X.helper` works).

**d) Rebase payoff.** After adoption, `git diff origin/main -- <file>` on the adopted region is empty; the rebase only re-introduces genuinely-local rows. Note in the pulse log that the zone is now "byte-identical — context-shift grade" so the next cycle knows the conflict surface shrank.

**Pitfalls:**
- **Wire-shape mismatch busts the shared cache** (see b) — the classic silent no-op. Verify fingerprint-relevant args match the prewarm/boot call site.
- **Windows-native Python (`py -3.11`) can't open MSYS `/e/...` paths** in script arguments — pass `E:/...` form instead.
- **Nested command-substitution one-liners** (`sed -n "$(grep ... | cut ...)"`) trip the terminal hardline blocklist — use `search_files`/`read_file` instead.

See **`references/early-upstream-adoption.md`** for the Aug 7 2026 worked example: upstream `cached_fetch_api_models` (`fb435aae9`) adopted at 448 behind via `--3way`, the OmniRoute picker row de-urllib'd onto the shared cache, 91 tests + functional check green.

## Pitfalls

- **Don't trust the behind-count alone.** 150 behind in analytics code is safer than 50 behind in a file you patched.
- **Don't skip patch-zone analysis.** "No upstream commits to this file" is safe. "Upstream -629 lines refactoring same file" is structural regardless of line-level overlap.
- **Don't assume zero-conflict persists across pulses.** One upstream commit can invalidate 8 consecutive pulses of clean bills of health. Re-check EVERY pulse.
- **Document the escalation trajectory.** A spike from 101→429→785→827→963 behind in ~72 hours is more informative than any single snapshot.
- **Verify working tree is clean before flagging issues.** An uncommitted fix started but unfinished by the user is different from a regression.
- **Don't underestimate upstream god-file refactors.** A -629 line change to web_server.py can shift insertion zones by hundreds of lines. The CRUD you added at line 18,982 may now need to land at a completely different position.
- **Don't rely on line numbers alone.** Even when line-level greps match, the upstream file may have shifted so much that `git rebase` fails. Always run `git rebase --dry-run` or a trial cherry-pick before declaring confidence.
- **Don't investigate behavioral drift in disabled subsystems.** Before tracing a timeout default or config value difference, check whether the subsystem is active in your runtime config (`grep -A5 "approvals" config.yaml`). A 60s vs 300s timeout difference in a disabled approval subsystem is academic — note it and move on.
- **Don't trust upstream mirror-fix comments.** When upstream adds a comment saying "loaded lazily" but the function is still called at module import, it's cosmetic — your actual patch is still needed. Always verify behavioral change, not textual similarity. See section 4a.
- **Don't assume upstream solved it better.** When upstream independently fixes the same bug you patched, compare both approaches carefully. Their fix may be Windows-incomplete or platform-naive. See section 4a for the decision matrix.
- **Don't let high divergence numb you to acceleration.** At 1500+ behind, a delta of +100/cycle compounds the conflict surface faster than at 500 behind. Track deltas, not just absolute counts.
- **Don't declare a patch lost from memory — grep the whole tree first.** Audits misremember file locations (the CDP override split was flagged lost while actually living in `tools/browser_tool.py`). When a marker isn't where you remember it, `grep -rn` the marker across all `*.py` before adding it to the loss list. See section 4i.

## Related Skills

- `recurring-status-checks` — broader cron-based status check framework
- `github` — git workflow management
- `karpathy-principles` — debugging mindset (80/20, Read the Source)
- `dynamic-upstream-merger` — companion fork-sync tool with trial rebase, merge/rebase decision matrix, CI integration, and the defensive branch (qa-lead/fixes) pattern

## Reference Files

- `references/dev-lead-pulse-963-behind-case-study.md` — Full walkthrough of a Critical-tier assessment (963 behind, god-file refactors, escalation decision).
- `references/behavioral-drift-detection.md` — How to detect runtime behavioral differences (timeout defaults, feature flags, function signatures) between fork and upstream using the `git diff origin/main` + `git log -p -S` technique chain.
- `references/1607-behind-case-study.md` — Full walkthrough of a Critical-tier divergence (1607 behind, upstream god-file refactors, zero-presence feature in refactored parent file, multi-branch tracking, escalation language).
- `references/upstream-structural-restructure-detection.md` — How to detect when upstream is making wholesale architectural changes — directory deletions, 2000+ line CL-level removals, and purely-local feature verification. Covers the `hermes_cli/` restructure at 1164 behind as a concrete case study.
- `references/path-construction-audit.md` — How to audit a codebase directory for `str(Path(...))` patterns that silently produce backslash paths on Windows. 3-match scan of `agent/` found all low-risk. Use this technique in the patch-zone conflict assessment to find the next `as_posix()` bug before it breaks a test or blocks a rebase.
- `references/upstream-rename-audit.md` — Verify local patches survive upstream symbol renames (e.g. `allow_session` → `allow_permanent`). Covers the 5-step audit: patch diff, zone mapping, rename ref discovery, line-number cross-reference, and function signature compatibility check.
- `references/upstream-cosmetic-patch-detection.md` — Case study: upstream added a "loaded lazily" comment without actually changing module-import behavior. Full 4-step detection technique for distinguishing real behavioral fixes from comment-only changes.
- `references/upstream-mirror-patch-conflict.md` — Case study: upstream independently fixed the same Windows path bug as the fork, but with a different approach. How to detect and reconcile conflicting approaches on rebase.
- `references/upstream-subsystem-strip-approval.md` — Case study: upstream stripped the denial breaker, smart policy, and allow_session from tools/approval.py while our 3 local patches sat in different functions. Detection workflow, rebase strategy, and key takeaways for the "net-negative diff = stealth conflict" pattern.
- `references/post-reset-loss-audit.md` — Full post-reset aftermath audit (Aug 4 2026): detecting a forced reset via divergence collapse + reflog, enumerating the loss surface, verifying recoverability with `git cat-file -t`, classifying lost patches (still-needed vs obsoleted vs relocation-carried), and the "lost in reset" commit-message tell.
- `references/object-db-patch-restoration.md` — Object-DB restore of lost patches onto evolved files (Aug 5 2026): symbol-grep hunk mapping, surgical re-apply with `patch`, regression tests from the original commit message, `-F` commit, restore ordering, and the false-loss pitfall.
- `references/inline-vs-extracted-restore.md` — The half-restore trap (Aug 7 2026): a lost feature re-added inline instead of its original extracted-module form (Hermes One). Detection, object-DB module/tests restore, logic-parity diff, block-splice and EOL pitfalls, and the thin-wrapper conversion.
- `references/omniroute-lock-restore.md` — Stale-heuristic collision during object-DB restore (Aug 7 2026, OmniRoute lock `72c19a87de`): old patch's bare-`localhost` detection false-positived onto Ollama added upstream since the patch. Anchor-verification checklist, port-scoped fix (`localhost:20128`), upstream-test discovery of the collision, and the lock/no-lock functional smoke matrix.
- `references/early-upstream-adoption.md` — Pre-rebase de-conflicting (Aug 7 2026, `cached_fetch_api_models` `fb435aae9` adopted at 448 behind): `git apply --3way` of an upstream diff onto a divergent tree, wire-shape matching for shared cache fingerprints, extracting the commit's tests from the object DB, and the functional monkeypatch verification pattern. Covers the full section 4j workflow.
