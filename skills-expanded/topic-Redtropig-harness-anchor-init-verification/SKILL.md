---
name: init-verification
description: Use at start of work, after env changes (deps/branch/OS), or when something stops working. Runs init.sh health check; treats failures as blocking.
---

# Init Verification

Before writing any code, **prove the environment is healthy**. Anthropic's Nov 2025 harness guidance: *the initializer agent runs init.sh, then the coding agent picks up — health is verified BEFORE work begins*.

## When to invoke

- First action of every fresh session
- After `git checkout` to a different branch
- After dependency changes (package.json / Cargo.toml / etc. modified)
- After OS / toolchain updates
- When a previously-working command suddenly fails
- Before claiming a feature done (re-verify in case of drift)

## Procedure

1. **Locate `init.sh`** in project root.
   - Missing → tell the user to run `/anchor` to scaffold one. Do not proceed.

2. **Run it.**

   ```bash
   bash init.sh
   ```

   Capture stdout+stderr.

3. **Interpret exit code.**

   | Exit | Meaning | Action |
   |---|---|---|
   | 0 | All checks passed | Proceed with work |
   | 1 | One or more checks failed | **Stop. Fix the reported issues before doing anything else.** |
   | other | Unexpected | Read output; either fix init.sh itself or report to user |

4. **On failure**: list the specific missing files/tools, propose fixes one at a time:

   - Missing tool (e.g. `cmake not found`) → suggest install command appropriate to platform (`brew install cmake` on macOS)
   - Missing state file (e.g. `feature_list.json missing`) → suggest `/anchor`
   - Missing build artifact (e.g. `compile_commands.json missing`) → suggest correct configure command

5. **After fix**: re-run `init.sh`. Repeat until exit 0. Then continue work.

6. **Re-check inherited NEGATIVE capability conclusions.**

   A line in `AGENTS.md` shaped like `searched <scope>, not found (as of <date>)`
   records what a **past** session observed. It is not a current fact. Re-check
   each one. This step, by construction, only ever re-checks conclusions
   already recorded as absent, so it always takes the discovery chain's
   NOT_FOUND path — the slower, full-ladder search, not the fast PATH hit — and
   that path measures ~1.6s for two tools (51-entry PATH):

   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/scripts/cpp-tool-discovery.sh <tool>
   ```

   For non-C/C++ ecosystems, the equivalent is `command -v <tool>` **plus** that
   platform's known install locations — `command -v` alone is the check that
   produced the wrong conclusion in the first place.

   - Tool now present → **report it to the user** and propose updating that line.
     Do not silently rewrite someone's operating manual.
   - Still absent → refresh the date, or leave it; either is fine. What is not
     fine is citing the old conclusion as if it were fresh evidence.

   **Only negative conclusions get re-checked, and that asymmetry is deliberate:**

   | Conclusion | How it fails once stale | Needs a proactive re-check? |
   |---|---|---|
   | Negative ("clang-tidy not found") | **Silently.** The tool gets installed, the note never updates, and the capability is skipped for the rest of the project's life. This is the observed failure mode. | **Yes** |
   | Positive ("clang-tidy at /usr/bin/clang-tidy") | **Loudly.** The next invocation is `command not found`. | No |

   **Residual blind spot:** this step only reaches lines written in the mandated
   form above. A capability conclusion phrased freehand — or written before
   v0.17.0 — is invisible to it. A clean re-check means "the dated conclusions
   are current", never "the manual contains nothing stale".

## What init.sh should check (project-specific)

The template provides scaffolding for:

- harness state files (AGENTS.md, feature_list.json, progress.md, session-handoff.md, PROJECT-TOC.md)
- presence of `git`

The user edits init.sh to add project-specific checks:

- Build commands (`cmake -S . -B .build` / `npm install` / `cargo check`)
- Dependency presence (`node --version`, `python --version`)
- Service availability (db ping, external API reachability) — only if needed at agent-start

Keep `init.sh` **fast** — under 30 seconds. Heavyweight checks (full test suite) belong in `/verify`, not init.

## Calibrated reporting

When `init.sh` reports OK, the agent's claim is *"environment looks healthy as of <timestamp>"*. Don't oversell — env can drift mid-session if commands modify it.

When it fails, list the specific failed step, not "init failed" alone.

## Anti-patterns

- Skipping `init.sh` because "I think the env is fine" → you don't know until you check
- Editing `init.sh` to make a failing check pass without fixing the underlying issue → masking
- Running `init.sh` once at session start, then assuming the env stays healthy 4 hours later — re-run after meaningful environment changes

## When NOT to run

- Inside a subagent that was already given verified-healthy context
- For trivial single-file edits where build/test aren't needed (rare; usually init still cheap enough to run)

## Worktree setup (superpowers:using-git-worktrees)

When `superpowers:using-git-worktrees` sets up an isolated workspace, its Step 2 (Project Setup) **is `init.sh`** — run it as the baseline instead of re-deriving ad-hoc `npm install` / `cargo build`; its Step 3 (Verify Clean Baseline) is the project's test command / `/verify` (the heavier pass `init.sh` deliberately defers). The git-tracked state trio travels with the branch checkout, so a worktree is **already anchored** — don't re-run `/anchor`. But `.harness-anchor/` is gitignored, so a fresh worktree starts with **no** prior verify/coverage/drift evidence: that is expected, **not** un-anchored — it is recreated on demand when a sensor first writes to it.

## Looking up toolchain errors

When `init.sh` fails with a cryptic toolchain message (e.g., CMake "could not find compiler", npm `ENOENT`, cargo "linker not found") — invoke the `docs-lookup` skill. Context7 is best for stable tool behavior; WebSearch surfaces recent platform-specific changes; calibrated uncertainty when neither helps.

Typical entry query: paste the exact error string in quotes + the tool name.

## Related

- `/anchor` — scaffolds the initial `init.sh`
- `/verify` — heavier-weight full verification (different scope)
- `feature-state-keeper` — `init.sh` failure is captured in `session-handoff.md` "Risks"
