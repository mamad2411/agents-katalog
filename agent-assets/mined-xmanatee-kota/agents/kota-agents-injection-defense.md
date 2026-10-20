# Injection-Defense Module

Input-side defense for externally ingested content on autonomous runs. The
defense is **additive** — it layers on top of tool-risk gating and the
approval queue and does not downgrade any existing guardrail. A moderate
tool does not become safer because its output was screened.

## Contract

- Registers result-screening middleware before custom user middleware.
- Post-processes content-ingest tool output (`web_fetch`, `web_search`,
  `http_request`, `read_document`, browser text-ingest surfaces) and
  tool results marked with external-content provenance before they reach
  agent context.
- Screens payloads against a cheap structural detector; suspicious payloads
  are **annotated, never dropped**: the middleware prepends a warning banner
  naming the tool and reason tags, wraps the original content between
  `--- BEGIN UNTRUSTED CONTENT ---` / `--- END UNTRUSTED CONTENT ---`
  markers, and leaves the payload intact so legitimate information still
  gets through.
- Structured JSON is screened alongside ordinary content and rich blocks,
  including decoded strings and keys. The warning covers the entire result,
  including structured data projected outside the text markers; structured
  values remain intact.
- Emits `injection.defense.assessed` for every screened call (suspicious
  or not) so operators can audit both missed attacks and false-positive
  rate via the event bus and run artifacts.
- Autonomous runs opt in by default. Supervised and passive sessions are
  opt-in via `modules.injection-defense.targetModes`.
- No test-only bypass flag. Tests drive the middleware through the normal
  `ToolCall` context and assert on the banner + emitted assessment.

## Extending

- New exact-name ingest channels should be added to `DEFAULT_TARGET_TOOLS`;
  dynamically named external tools should pass typed result-content provenance
  into this middleware instead of maintaining generated name lists.
- Detection heuristics live in `detector.ts` and should stay cheap and
  structural.
- If escalation to a classifier becomes necessary, extend the middleware
  rather than replacing it.
