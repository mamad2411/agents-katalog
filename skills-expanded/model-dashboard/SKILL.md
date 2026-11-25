---
name: model-dashboard
description: Compare Codex GPT engines and native effort recommendations in the ModelPlan console, read public Codex reset notices, or check the plugin's own setup (Node runtime, tools, quota reader, optional hints).
---

Call `open_model_dashboard` to show the compact card in the conversation. A tool call cannot open the panel beside the chat: when the user wants it there, tell them to open "Effort & quota" from the conversation's side panel. For a terminal or data answer call `get_model_dashboard`: `view: "lineup"` compares OpenAI models at their ★ recommendations; `view: "effort", modelId: "<exact result ID>"` compares one model's native efforts relative to ★. Choose `lang: "zh"` or `"en"`. Completion: show the published values, verdicts and publication identity, or the explicit unavailable/last-good state.

In Codex CLI the HTML is unavailable. Present the tool's text blocks in their returned order. If MCP is unavailable and the `modelplan` Go binary is installed, run `modelplan lineup --dev openai --no-color`; for a specific model use `modelplan effort <exact ID> --no-color`. Keep the published lineup verdict and baseline; lineups are the published client digest's verdicts, also used by the website kit and Go CLI.

The lever is a comparison setting. Applying a model/effort uses the host picker and an explicit user action. Unknown values stay unknown, and estimated time keeps its label. Ability is additive points; cost/time changes are relative to the same model's ★ recommendation. Cost is USD per declared reference task; label any absolute value as approximate reference-task dollars. Time ratios require matching published time bases.

Public reset notices do not establish personal eligibility, balance or a personal reset time. Preserve source status, scope and stated time precision; posting or confirmation time is not effective time. Model and reset evidence come from one verified publication. 

Every result carries `setup`: the Node runtime the server runs on, which local reader read the quota (`cli` or `python`), and whether proactive hints are on. When `advice.status` is `unavailable`, say hints are off and why (`cli_missing`: the optional `modelplan` CLI 0.4+ is not installed; `cli_without_advise`: it is older than 0.4). Do not imply every feature is enabled.

Setup check: when the user asks whether the plugin works, why the dashboard, quota or hints are missing, or a tool returned a Node.js diagnosis, run `node '<this skill directory>/../../doctor.cjs' --lang zh` (or `en`). It is read-only: Codex's app-server starts the installed plugin, a temporary thread is opened without a message, and one data call is made; nothing is billed. Relay its failed items with their fixes and the three verdicts: installed, tools callable, panel shown. Panel shown is always unverified by the check; only opening the dashboard confirms it. Suggest a new task after a fix; do not claim a Codex restart is required.
