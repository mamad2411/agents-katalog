# Gemini Agent Harness Module

Adapter module that registers the `gemini` harness: a multi-turn tool-calling
loop driven by the Google Gen AI SDK. Route work here with the `gemini`
preset, default harness config, or a step-level `harness`.

This module owns the `KotaTool` to Gemini `FunctionDeclaration` translation at
the adapter seam.

## Provider Routing

Models are passed directly to the SDK (`gemini-2.5-flash`,
`gemini-2.5-pro`, `gemini-2.0-flash`, ...). The SDK reads `GEMINI_API_KEY`
or `GOOGLE_API_KEY` from the process environment. This module does not use
`model-clients`; Gemini's content/tool wire shape is its own primitive.

## Loop Shape

Each turn builds Gemini tools from the filtered KOTA tool catalog, streams
`client.models.generateContentStream`, forwards text to the harness writer,
executes emitted function calls through core tool paths, appends
`functionResponse` parts, and repeats until the model returns no function
calls or the max turn limit fires.

Every call uses the shared permissioned tool runner, so autonomy mode,
configured guardrails, client or queued approval, idempotency, middleware,
secret masking, and telemetry match other KOTA-hosted loops. Filtered tools
are hidden from the catalog and denied again at runtime; `canUseTool` can
update inputs, deny with a tool response, or interrupt the run.

## Reasoning Effort

`AgentHarnessRunOptions.effort` maps to Gemini
`thinkingConfig.thinkingLevel`: `low` to `LOW`, `medium` to `MEDIUM`, and
`high`/`xhigh`/`max` to `HIGH`.

## Protocol Errors

Missing function names and non-object function arguments throw before reaching
tool runners. Coercion belongs at the wire boundary only.

## Conversation continuity

Gemini content parts, function results, and thought signatures persist as adapter-owned JSON in
the shared core conversation store. Current tools and system instructions are
rebuilt on resume; interrupted effects remain uncertain and are not replayed.
Budget errors return the owned conversation id, as do successful turns.
