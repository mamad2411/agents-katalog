---
name: cyc-setup
description: "Set up CYC in the current project: activate it, find the project's real test, lint, and type-check commands, write them into the CYC config, and confirm everything works. Use when the user says \"set up cyc\", \"activate cyc\", \"install cyc here\", or right after installing the CYC plugin."
---

# Set up CYC in this project

Explain once: CYC finds relevant project knowledge, checks a change and retains consequential decisions for the next chat. Use onboard.experience for first-task guidance and responseChoices for an observed preference; unknown state cannot be called concise or unlimited. Guide the developer from installation to one useful task. Keep installed files, configured checks, executed checks, and live host activation distinct. Use the existing project conventions and ask only about consequential missing decisions.

The CYC CLI is [bin/cyc.mjs](../../bin/cyc.mjs), two folders up from this skill. Resolve it to an absolute path and run it with `node`.

## The core loop

1. **Inspect readiness.** Run `node <cli> onboard`. If this request supplied CYC gate context, add `--host codex|claude --session <gate ID> --token <injected review token>`. Otherwise omit the token: native Codex/Claude session identity is detected when available, and missing prompt state is an actionable setup failure. Inspection runs no project commands and changes no files. Explain its first unresolved step in plain language, not the entire JSON report.
   - A project manifest exists: the report includes `doctor` findings. Resolve actual installation conflicts while preserving customized files.
   - Only a config exists: the project is configured, but confirm that the host supplies the plugin. Do not reinstall or overwrite a team's existing checks just to repeat onboarding.
   - No config exists: continue with activation or the project installer, according to how the user obtained CYC.
2. **Activate.** Run `node <cli> activate --dry-run`, show the planned files, then run it without `--dry-run`. This creates `.cyc/config.json` and `.cyc/.gitignore` only. It changes nothing else.
3. **Find the real checks.** Read `onboard.evidenceSources`, actual CI/project scripts and contributing instructions. Discovery does not endorse commands. Explain each recommended check's detectable behavior/error. Missing checks need a bounded proposal within authorized scope; an always-successful command cannot substitute.
   Use `node <cli> recipe list`; reuse project tools and register successful reusable checks in `docs/context/recipes.json` under the [project-tools contract](../../docs/project-tools.md). Retain concrete coverage, references, prerequisites, effects and outcomes. Mandatory checks stay in `verification.commands`; recipes cannot replace them. Setup grants no publication permission or authority to copy CYC's development recipes into an application.
4. **Propose the commands in one round**, with each executable/arguments, observed CI or script reference, prerequisite, reason and recommendation. Keep required project checks; separate supplementary service-dependent recipes. Prefer bounded commands and separate independently judged unit/integration checks. Diagnostic baselines are off by default. Never guess a command or its duration.
   When no one can answer (an unattended run, or `/cyc` was invoked with instructions not to wait), do not stop: write only commands the project itself defines and runs (CI or a package script), prove them in step 7, and name them in the final handoff as configured checks. That disclosure is information, not a blocker.

   Do all of this before `run start`. The controller captures the checks when a run starts and protects `.cyc/config.json` while it runs; an edit then halts the run, and `run start` refuses code playbooks while no checks exist.
5. **Write the approved commands** into `verification.commands` as `{ "id", "command", "args": [], "timeoutMs" }`. Reuse already authorized team configuration; do not ask for approval again when the session already provides it. Do not change configuration beneath an active run. Split the executable from its arguments (`"command": "npm", "args": ["test"]`). On Windows, Node cannot launch `npm`, `npx`, or other `.cmd` shims directly, so wrap them: `"command": "cmd", "args": ["/c", "npm", "test"]`.
6. **Respect existing conventions.** Reuse the project ledger through `context.ledgerPath`. If another hook already enforces response formatting, configure `delivery.presentation: "project"`; preserve that hook. CYC still enforces controller completion. Show these choices with the proposed commands.
7. **Prove the configured commands run.** After reviewing side effects/authorization, run `node <cli> onboard --verify`. Explain its [bound diagnostic receipt and limitations](../../docs/onboarding-recovery.md#onboarding). Source-mutating/stale results cannot pass or replace task verification. Disclose existing failures; preserve unrelated code and checks.
8. **Check the hooks in the actual host.** Explain `guidance` and the first unresolved `host` step using the [setup states and trust procedure](../../docs/onboarding-recovery.md#onboarding). `onboard` exits nonzero until ready; `canStartTask: true` permits authorized work while its own Stop is pending. Report actual host/version, current prompt and separate post-turn completion observations. Missing state needs supported trust/reload controls; never simulate activation, edit trust/state, read an old token or invent a Cursor tag. Project-owned presentation changes rejection probes: a missing table alone is inconclusive. Preserve stale/rejected/blocked observations and disclose unavailable qualification.
9. **Connect setup to a first success.** Continue the authorized bounded task once prerequisites permit. Otherwise recommend one from project evidence for the user to choose before product edits. Explain its outcome/checks and connect delivery to the existing review. Explanation does not prove user understanding.

## Done when

- The report separates installation, configuration, executed checks, and host activation, with actual evidence and one next action for any unresolved step.
- Configured commands have recorded results; failed, stale or unavailable results remain disclosed. A failed setup is not called ready.
- The first task is continued when already authorized, or a concrete recommendation is offered without inventing approval. Setup completion and task completion remain separate.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Invented checks | Adding `npm test` to a project with no test script | Only use commands defined in the project |
| Silent writes | Changing config before showing the plan | Dry run first, then write |
| Fixing the baseline | "Tests were failing, so I fixed them" during setup | Report the failing baseline; fixing is a separate task |
| Committed secrets | Tokens or env values in config commands | Reference env vars by name only |

## Handoff

Report what is ready, the first unresolved step, and its smallest next action. Cite setup and host evidence separately. `ok`/`ready` require passing setup phases; neither establishes first-task completion or human understanding. Suggest sharing the existing project configuration through the team's normal review process.
