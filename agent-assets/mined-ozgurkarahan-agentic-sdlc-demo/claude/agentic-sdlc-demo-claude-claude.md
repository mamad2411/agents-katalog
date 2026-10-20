# Claude Code — Project Config

> Read `AGENT.md` for project instructions (auto-loaded via root `CLAUDE.md`).
> `AGENT.md` § Workflow Rules and § Platform & Environment hold the project's working rules.

## Claude-Specific

- Use subagents (`explore`, `task`) for research and verbose long-running work; keep main context for decisions and code edits only.
- When proposing code changes, verify locally before claiming done — run the checks in `AGENT.md` § **How to Verify**; keep that section current as the project evolves.
- Update the **Project Context** block below at session end with the active iteration's status — what changed, what's next.
- Durable lessons go to your team wiki, NOT to a project-local `.ai/` folder.

## Project Context

Agentic SDLC Demo is a presenter-led, reusable demo environment that showcases the full software development lifecycle driven by AI coding agents — from a raw input (a requirement, meeting notes, or an action item) through plan → implement → test → review → PR → deploy. Scaffolded 2026-06-18 from `project-template`. It is a customer-facing showcase, NOT a hands-on lab: the presenter drives, the audience watches the agentic workflow. First-session task: research demoable agentic-SDLC surfaces (Copilot CLI + coding agent + PR review, Claude Code, GitHub Actions, Azure deploy) and propose the sample app + the input→lifecycle story before building anything (see `AGENT.md` § First Session Instructions). Durable project knowledge lives in your team wiki.

**Iteration status:** Tier-1 offline backbone complete and green — sample app + multi-agent gate harness + dispatcher, validated by `node _internal/harness-selftest/validate/run.mjs` (**86/86 fixtures, 54/54 negatives**, every gate catches its seeded negative). The live path is now **proven twice**: two real orchestrator runs shipped full lifecycles in a private `<your-org>` org — (1) a keyless OpenAI-Agents-SDK coding agent (15 merged PRs incl. Azure deploy; exposed F6 no-enforcement / F7 spawn-sprawl / F8 no-pull-status) and (2) a declarative Foundry *prompt* agent with message-based intake (all units merged + real Foundry deploy + live E2E behaviours passing). Both runs were **observed by the loop/goal agent and used to harden the harness source** (`harness/`), which is committed + pushed to `origin/master`: enforce-first gates, HYBRID→cloud-agent-first delegation, pull-observable dispatch, human gates as HARD STOPS, GraphQL Copilot-agent assignment, one-implementer-per-unit, draft-PR-is-done, and `delete_branch_on_merge`. Durable findings graduated to the team wiki. **Next:** a 2nd scenario (add web-search grounding + relax the agent system prompt) re-runs the fixed harness end-to-end in a fresh session, watched by a separate loop/goal session. See `AGENT.md` § **How to Verify** for current checks.
