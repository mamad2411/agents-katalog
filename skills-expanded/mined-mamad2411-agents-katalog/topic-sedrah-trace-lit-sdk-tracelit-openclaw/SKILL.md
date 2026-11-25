# Trace-lit Observability Skill

This skill instruments OpenClaw sessions and sends traces to Trace-lit for observability.

## What it does

- Activates automatically when a session starts — no manual instrumentation needed
- Sends a span for every tool call (name, duration, tokens, errors)
- Sends a final span on session end with total token usage and duration
- All traces appear in the Trace-lit dashboard under the configured agent name

## Setup

Set the following environment variables before starting OpenClaw:

```bash
export TRACELIT_BROKER=app.trace-lit.com:9093
export TRACELIT_API_KEY=your-api-key
export TRACELIT_AGENT_NAME=my-openclaw  # optional, defaults to "openclaw"
```

To use a self-hosted Trace-lit instance:
```bash
export TRACELIT_BROKER=your-server:9093
```

## View traces

Open https://app.trace-lit.com after running a session. Traces appear within a few seconds.

## Notes

- If `TRACELIT_BROKER` or `TRACELIT_API_KEY` are not set, the skill disables itself silently — your sessions are unaffected
- Zero outbound connections except to the configured Kafka broker
- Token costs are calculated server-side by the Trace-lit ingestion pipeline
