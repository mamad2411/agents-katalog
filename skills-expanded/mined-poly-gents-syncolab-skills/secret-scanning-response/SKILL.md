---
name: secret-scanning-response
description: "Respond to a detected secret leak (token in source, log, build artefact, or chat) with a fixed rotate-then-purge-then-trace sequence, never the other order."
---

# Secret scanning response

When a secret leaks, the wrong order is: try to delete the commit first. The right order is: rotate, then purge, then trace.

## When to run

- GitHub secret scanning alert.
- A scanner (gitleaks, trufflehog) finds a hit.
- A user reports a token in chat, logs, or screenshots.
- You catch it yourself before commit.

## The fixed sequence

1. **Rotate.** Immediately invalidate the leaked credential at the issuer (Stripe key in Stripe dashboard, GitHub PAT under settings, AWS key under IAM, etc.). If you can't, escalate to a human with the issuer name.
2. **Replace.** Generate a new credential and update the live consumer (env var, secret manager, deploy pipeline). Confirm the consumer is healthy with `production-validation` gate 3.
3. **Purge from source.** Force-removal (`git filter-repo` or BFG) plus a forced rewrite of the affected branches. Coordinate with the team on coordinated re-clone.
4. **Purge from artefacts.** Build logs, screenshots in shared docs, screenshots in Slack threads, container layers, package registries.
5. **Trace.** Pull access logs (last 30 days or whatever the issuer retains). Look for use that did not originate from your own infra. Document.
6. **Write up.** File a planning issue with the timeline. If access logs show unauthorized use, treat it as an incident and run `incident-postmortem-loop`.

## Never

- Rotate AFTER purge. The attacker still has the live key in the window.
- Delete the leaking commit before rotating. It's already on every clone.
- Skip the trace step. Even with no evidence of misuse, the log review is part of due diligence.

## Tools

- Issuer dashboards (out of band) for rotate.
- `agent_filesystem_search` + git history tools for purge.
- `pagerduty` to page security on-call when the secret was production / customer-data scope.
