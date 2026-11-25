---
name: skill-radar
description: Decompose a concrete task and select the best installed or curated agent Skills for each step, with platform and constraint gates, evidence, gaps, and an execution order. Use when the user asks which Skill to use, asks to find or compare Skills for a task, wants a task-to-Skill plan, or explicitly invokes Skill Radar. Do not use for browsing project ideas.
---

# Skill Radar

Turn a task into the smallest reliable set of Skills that can complete it. Optimize for an accepted first result, not for the number or popularity of recommendations.

## Beginner Starter Pack

When the user explicitly asks to set up the beginner starter pack, read [starter-pack.json](references/starter-pack.json), then run the checker for the current Agent:

```bash
python3 <skill-radar-directory>/scripts/bootstrap_starter_pack.py --agent <codex|claude-code|cursor|other> --format json
```

Run the same command with `--install` only when starter-pack installation was requested. Merely installing or invoking Skill Radar does not authorize installing eight more Skills. Re-running is safe: installed items are skipped and every attempted install is checked at the Agent's actual destination. Report each item as `installed`, `missing`, `disabled`, `partially_disabled`, `install_failed`, `failed_verification`, `installer_unavailable`, or `local_unavailable`; do not turn a detected runtime such as `gh` into a claimed installed Skill.

The starter pack contains `Find Skills`, the safe task-scoped subset of `Superpowers`, `github-issues`, the user's `xiaobai-frontend-design`, `Guizang PPT`, and Vercel deployment. GitHub CLI remains a separate curated execution tool in `references/whitelist.json` and is detected at search time. Superpowers' global behavior switches (`using-superpowers`, `brainstorming`, and `using-git-worktrees`) are intentionally not auto-enabled. Use the installed local `xiaobai-frontend-design` only where its local Refero workflow is available.

## Search order

Search in this order for every subtask:

1. Skills already installed for the current agent, especially the user's local and custom workflows. Include nested Codex plugin Skills instead of checking only top-level folders.
2. Active entries in `references/whitelist.json`, including approved command-line tools that a Skill may depend on.
3. The installed `find-skills` workflow and skills.sh only when the first two sources have no close match.

An installed local Skill wins over a generic ecosystem Skill when it directly covers the task and its requirements are satisfied. Presence on disk proves availability, not outcome quality.

## Workflow

1. Convert the request into a task contract:
   - desired outcome and final deliverable;
   - current agent, application, operating system, repository, and available inputs;
   - hard constraints such as offline-only, no account, no API key, privacy, deadline, budget, or required platform;
   - the smallest visible result that proves useful progress.
2. Ask one short question only when a missing fact would change the selected Skill. Continue with facts that can be inspected from the current environment.
3. Decompose a compound task into outcome-bearing subtasks. Keep a single-output task as one step. Record dependencies and preserve the user's final outcome; do not turn implementation details into separate steps unless they need different capabilities.
   The helper returns `plan.steps` for common input-to-output and build-to-publish tasks. Use each step's primary Skill and acceptance check; a missing step remains a `plan.gaps` item, even when another step has a match. Read [scenarios.md](references/scenarios.md) when choosing among adjacent domains or explaining a gap.
4. Resolve every referenced file relative to this `SKILL.md`; never assume the user's project is the Skill directory. For each subtask, state its requested output explicitly and run the local search helper when Python is available:

   ```bash
   python3 <skill-radar-directory>/scripts/search_skill_library.py --query "<full task outcome>" --agent <codex|claude-code|cursor|other> --format json
   ```

   Add `--offline`, `--no-account`, or `--no-api-key` when the user stated those constraints. If the script cannot run, inspect the current agent's installed Skill manifests and `references/whitelist.json` directly.
5. Read the actual `SKILL.md` for each installed candidate that survives the search. The helper scans nested local Skill roots and the Codex plugin cache, and probes approved CLIs such as `lark-cli`, `opencli`, `wx`, and `gh`. A detected CLI is a tool, not an installed Skill; label it accordingly.
6. For curated candidates, read the source or manifest when the recommendation depends on a detail that the whitelist does not establish. Treat `constraintWarnings` as unresolved checks rather than evidence that a constraint is satisfied.
7. Apply hard gates before ranking:
   - exclude agent-incompatible candidates;
   - exclude account, API key, cloud, hardware, or write-access requirements that conflict with the request;
   - identify contradictory requirements instead of silently relaxing one;
   - exclude candidates that cannot produce the requested output.
8. Rank survivors by task/output fit, environment availability, verified same-task feedback, evidence level, time to first result, source trust, then popularity. Do not use installs or stars as proof that the task will work.
9. Choose one primary Skill per outcome-bearing step. Add distinct supporting Skills only for work the primary does not cover. Reuse one Skill or approved tool across steps and install or enable it once. For a compound task, do not present the first item in `matches` as though it covers every step; follow `plan.steps` and report `plan.gaps`.
10. Mark an uncovered required step as a gap. For that step only, invoke `find-skills` with outcome, agent, and constraint terms. Review the returned source and requirements before adding a result to the plan.
11. Return the decision using `references/output-format.md`. Keep no more than one primary choice and two alternatives per subtask.
12. When the user asked to execute the task, continue with the selected Skills after presenting the compact plan. When the user asked only for selection or comparison, stop after the recommendation. Install a missing Skill only when the request includes installation or the user accepts the recommendation.
13. After a real attempt, record `passed`, `blocked`, or `mismatch` with `<skill-radar-directory>/scripts/record_feedback.py`. Record `passed` only after inspecting the first result against its acceptance check.

## Evidence rules

Use these levels exactly:

- `source_checked`: the source and intended scope were reviewed.
- `manifest_checked`: setup instructions and declared requirements were reviewed.
- `install_verified`: installation succeeded in the stated environment.
- `outcome_verified`: the first result was observed and passed its acceptance check.

Never promote an evidence level from popularity, a search result, or an installation command. A copied prompt and a successful installation are not task completion.

## Feedback

Same-task feedback changes later ranking:

- `passed`: prioritize the candidate for the identical normalized task and environment.
- `blocked`: demote it and preserve the actual blocker in the next plan.
- `mismatch`: exclude it from that task.

The feedback helper stores a hash of the normalized task rather than the raw task text. Do not put secrets, raw private content, tokens, or credentials in the feedback note.

## Boundaries

- Do not recommend a Skill merely because it is popular or broadly related.
- Do not invent availability, installation commands, compatibility, or evidence.
- Do not claim a catalog entry is installed until the current environment confirms it.
- Do not present an installed executable as a Skill. Show it as an execution tool and name the Skill or workflow that will call it when one exists.
- Do not ask the user to run a search or inspection that the current agent can perform.
- Do not hide a missing capability behind a generic all-purpose Skill.
- Do not treat Skill Radar as a project-idea directory or a webpage feature.
