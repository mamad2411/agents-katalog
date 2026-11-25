---
name: self
description: Use when the user's request depends on self-system editing or maintenance, assistant identity or model/runtime behavior, tool, harness, or script access, user-specific context, habits, beliefs, or personalization, session history or continuity, first-use setup or onboarding, or Self package diagnostics. This includes who the assistant is or what model or environment it is using, what it can access, remember, or do in the current harness, how user preferences, habits, beliefs, or worldview should shape the answer, setting up Self after first upload, the Self package version or install date, making new Self content easier to find later, or adding or editing files, rules, or remembered content inside the Self folder.
compatibility: Portable Agent Skills bundle for Claude Code, Codex, and compatible clients. Markdown files are the primary runtime source of truth; manifest.json and scripts are optional helpers for apps and maintainers.
---

# Self

When the user's question depends on runtime self-knowledge about editing files or rules inside self, self-system maintenance, created or installed Self diagnostics, assistant identity, model maker or provider, model name or capabilities, routing or orchestration behavior, context loading workflow, model or subagent selection, tool mediation, model or harness adaptation, runtime environment, tool access, harness capabilities, script or app routing, user-specific context, professional context, preferences or beliefs, habits or routines, decision or planning preferences, belief-aware personalization, worldview, religion, philosophy, or existential framing, prior sessions or continuity, session history, first-use setup, onboarding after adding Self, completing unknown Self fields, or wiring Self into a project, or when the user asks to change the Self system itself, read `SELF.md` first. When in doubt, check Self before answering from memory.

## Self Edit Protocol

If the user asks to add, edit, move, remove, summarize, rename, or explain anything inside `self/`, treat that request as Self-aware work.

1. Read `SELF.md`.
2. Open the smallest matching Self file.
3. Make the requested change.
4. Review whether the change affects when Self should trigger, which slot should open, what private context should load, or how bridge guidance should steer the harness.
5. If discovery or routing changed, update `SKILL.md`, `SELF.md`, and any installed bridge copies in the same task.

## Keyword Compression Rule

Do not grow the `SKILL.md` description by appending every new belief, preference, synonym, or example literally. Prefer short umbrella domains such as `beliefs`, `runtime environment`, `session history`, or `self-system maintenance`. Merge overlaps, deduplicate terms, and keep the description compact enough to stay within platform limits.

## Instructions

1. Read `SELF.md` first.
2. Use the slot catalog to choose the smallest relevant file.
3. Read private slots such as `user.md` and `chrono/` only when the user requests personalization, belief-aware context, remembered preferences, remembered habits, belief updates, or continuity.
4. If the user asks to add, edit, move, remove, or explain anything inside `self/`, open the smallest matching Self file and make the change there.
5. For structural Self changes, or plain-language requests such as "make Self notice this next time," "make this easier for Claude or Codex to find," "check Self is up to date," "scan Self after this change," or "keep the skill in sync," prefer the local script helpers when Bash and Node are available: run `node self/scripts/sync-self.js` to rebuild `SKILL.md` and mirror trigger hints into `manifest.json`, then run `node self/scripts/validate-self.js` to check limits and coherence. If scripts are unavailable, follow the manual fallback rules in `SELF.md`.
6. After any edit inside `self/`, review whether the change also affects skill discovery or Self routing. If a Markdown slot gained a new recurring domain, update that file's `trigger_domains` or `private_trigger_domains` frontmatter before refining `SKILL.md` and `SELF.md`.
7. For non-Markdown resources that introduce recurring trigger domains, refine the trigger guidance in `SELF.md` directly because those files cannot carry frontmatter trigger lists. Keep `metadata.json` as a minimal diagnostic stamp, not a routing file.
8. If you refine the `SKILL.md` frontmatter description, keep it broad, deduplicated, and within the 1024-character Agent Skills limit. If a `when_to_use` field is present, keep `description` plus `when_to_use` within Claude's 1536-character listing cap. Prefer umbrella domains over appending every new fact word-for-word.
9. Do not assume the harness automatically reads `manifest.json`, `app.js`, or files in `scripts/`. In uploaded-skill environments, `SKILL.md` and `SELF.md` are the runtime truth. Open other files only when the current environment exposes them and the task requires them.
10. Prefer natural-language Self maintenance rules even when scripts are unavailable. Use script helpers as accelerators, not as the only way to keep Self coherent.
11. If the user says to close the program, close the app, quit Claude, or quit Codex, treat that as a harness app-control request. Read `harness.md`, verify the current shell can control the same host machine as the target app, confirm the target and any unsaved-work risk, then open the matching quit helper for the current OS directly. If the shell is remote, sandboxed, browser-only, or on the wrong OS, explain the limitation instead of running the helper. Use `scripts/README.md` only if the helper or platform is unclear.
12. For other script or tool questions, read `harness.md`, then `scripts/README.md`, then only the specific script or harness-action file.
13. For install, setup, or first-use wiring, read `skills/first-use.md`.
14. Report which Self files influenced the answer when that helps the user understand the response.
