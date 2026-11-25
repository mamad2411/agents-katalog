---
name: jevlaya-playtest
description: Test gameplay in a running Unity uGUI game or bounded local browser game with JevLaya GameTest, optional Jev/Laya/OmniJev/Laya-MLX/Agent decisions, and independent evidence checks. Use for gameplay trials and reports; includes sourced case drafts, browser regression suites and host adapters; engine builds need separate validation.
---

# JevLaya GameTest

Turn a gameplay test request into a bounded run with declared expectations, actual input,
independent checks, and a report that preserves failures. This alpha coordinates existing
tools through the host Agent. JevLaya GameTest owns the Harness: provider selection/adapters,
bounded gameplay execution, evidence and independent verification. Models and inference
environments are external dependencies; reuse what the user already has.

## Establish the run

For a new engine/runtime target, read [engine coverage](references/engine-coverage.md)
before setup. Product targets include Unity, UE, Cocos Creator and LayaAir; currently
the Unity uGUI route and a bounded local-browser prototype are implemented. LayaAir and the Laya decision model
are different roles. Match the actual running surface, not just an engine name.

For runtime selection or supplied Cocos/LayaAir Web builds, read
[runtime onboarding](references/runtime-onboarding.md). For reviewed case generation and
batch regression, read [sourced regression](references/sourced-regression.md). For another
Agent host, read [portable hosts](references/portable-hosts.md).

For bounded local DOM/Canvas cases, follow [browser sessions](references/browser-sessions.md).
Unity and browser share `core session`; their input backends stay separate. Use existing
Node/Playwright/Chromium and the selected provider. The browser creates an owned headless
instance, never attaches to personal tabs. The earlier [browser experiments](references/browser-experiments.md)
entry remains available for compatibility.

1. Read [setup](references/setup.md). Use existing Python/provider environments and `prepare`
   to unpack Harness sources only. Do not install dependencies or download models as part
   of normal checks or provider selection. A source checkout is not required. Identify the user's
   **game project** separately; installation does not install game components or start Play.
   On Windows, read [Windows setup](references/windows.md) for native PowerShell, paths and
   device selection. Compatibility implementation does not imply live Windows acceptance.
2. Reuse the user's game target, provider, stop point and permissions. Clarify only missing
   information. Record the expected behavior and its source before input. Unknown rules
   can be explored but cannot be turned into invented assertions.
3. Read [providers](references/providers.md). Recommend **Jev first** when the user has no
   preference; honor an explicit or saved choice of Laya, OmniJev, Laya-MLX or host Agent.
   Save project preferences outside the game/Skill in a private config file. Connect the
   selected existing route; report missing capabilities without installing or silently switching.
4. Read [workflow](references/workflow.md) to observe, decide, execute and verify. Use
   [reporting](references/reporting.md) to preserve the plan, evidence and outcome.
   For a bounded reusable case, use [sessions](references/sessions.md): the `core session`
   commands freeze the case/configuration, check backend capabilities, bind fresh targets,
   archive receipts and preserve failed steps while the Agent handles vision and decisions.
   New provider requests use the generic v2 goal/observation/constraints/candidates contract.
   Read [rules and feedback](references/decisions-and-rules.md) for opt-in assisted decisions.
   This session path has offline protocol and owned browser-sample coverage; Unity session
   regression and general engine-game acceptance remain pending.

Before testing, show the selected combination: host Agent, vision provider, decision
provider and input backend. In the report, show **actual calls** and model/version/usage
when available. An installed or configured provider is not proof it was called. Do not
label host-only or deterministic actions as Jev/Laya decisions.

## Boundaries that matter

- Attach only to the identified running game. The user starts/stops Unity Play. Do not
  operate editor UI, evaluate arbitrary C#, mutate success flags or change game state
  through debugging APIs. Initial bridge installation is a separate setup operation;
  proceed when authorized, otherwise obtain that specific authorization.
- This first route uses the **game-local uGUI pointer**, not built-in Computer Use or
  system mouse input. No automatic fallback to desktop input, activation or GM controls.
  Stop on session/layout mismatch, uncertain input effect, or required editor interaction.
- Respect the host's image handling rules. In the current project, image reads and visual
  verification belong to a visual child; return text and artifact paths to the coordinator.
  Other hosts must supply a supported visual workflow before claiming compatibility.
- The decision provider chooses an existing candidate. Its probability helps choose an
  action; it does not determine PASS. Independently check actual post-action evidence.
  Missing evidence stays INCONCLUSIVE; input completion alone is not game success.
- Preserve every failed attempt. A later win does not repair a previously observed bug.
  Separate model mistakes, input misses, environment problems and confirmed game defects.
- Keep game mechanics in explicitly sourced project profiles. Core assumes no game genre,
  one-to-one assignment, last-slot solution or retry budget. Rules, feedback elimination
  and verified replay are opt-in; record them separately from actual model decisions.
- Budgets and allowed recovery come from the current run plan. Never import the historical
  three-attempt trial limit, old level answers, model credentials or saved coordinates.

Current evidence covers Codex-coordinated SeatClue on macOS/Unity uGUI. Other Agent hosts,
games, operating systems, general browser games, APK and IPA require their own validation.
The browser prototype has separate real DOM/Canvas sample checks with host-Agent decisions;
provider switching also has fixture coverage, not new live acceptance for every model. Different
game results do not establish a Jev/Laya/OmniJev ranking.
