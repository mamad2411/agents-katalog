---
name: fly-logs
description: >-
  Fetch and filter production logs from Fly.io apps. Trigger on "show me the logs",
  "check prod logs", "what is in the logs", or when debugging any production
  issue on a Fly-hosted app.
---

# Fly logs

## Fetch

```bash
fly apps list                              # find the app name
fly logs -a <app>                          # live tail
fly logs -a <app> --no-tail | tail -200    # recent burst, non-blocking
fly logs -a <app> -i <machine-id>          # one machine only
```

`fly logs` tails by default; for analysis prefer `--no-tail` piped through
grep so the command terminates.

## Filter

```bash
fly logs -a <app> --no-tail | grep -iE 'error|traceback|exception' | tail -50
fly logs -a <app> --no-tail | grep ' 500 '       # server errors on requests
fly logs -a <app> --no-tail | grep '<endpoint>'  # one route's traffic
```

## Read the result properly

- A traceback's LAST frame in app code (not library code) is where to look.
- Repeated identical errors every N seconds = a crash-looping background job
  or health check, not user traffic.
- Shape-mismatch / feature-names errors on prediction routes = FEATURE_COLS
  drift between serving and training repos; fix the sync, don't restart.
- For deeper analysis hand the evidence to the `debugger` subagent.
