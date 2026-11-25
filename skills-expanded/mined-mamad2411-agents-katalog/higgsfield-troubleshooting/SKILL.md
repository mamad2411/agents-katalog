---
name: higgsfield-troubleshooting
description: Diagnose Higgsfield failures, stuck generations, credit and rate limit errors, NSFW rejections, and format problems. Use when a Higgsfield tool call errors or a generation never completes.
---

# Higgsfield troubleshooting

Work down this ladder in order; most failures are auth, credits, or patience.

## 1. Auth failures

- MCP tools returning unauthorized: the OAuth grant is stale. Disconnect and
  reconnect the Higgsfield connector, sign in again in the browser.
- Cloud API 401/403: wrong or revoked key, or the plan tier does not include
  API access. Verify at https://cloud.higgsfield.ai/api-keys.

## 2. Credits exhausted

Generations spend plan credits, priced by model and resolution. Symptoms:
submissions rejected or failing immediately after auth succeeds. Check the
account dashboard balance. Mitigations: lower resolution (4K costs the
most), shorter videos, cheaper models, or top up the plan. Credits may have
expiry terms depending on plan; confirm in the dashboard rather than
assuming they roll over.

## 3. Stuck or slow generations

- Everything is async. Images complete in seconds; videos can take minutes.
  Poll the generation status tool instead of resubmitting.
- Resubmitting a "slow" job doubles the credit spend. Only retry after a
  status explicitly reports failure.
- For long video jobs in direct API integrations, prefer webhooks over tight
  polling loops.

## 4. Failed and NSFW statuses

- `Failed`: transient model or capacity error; retry once, then simplify the
  prompt or switch models.
- `NSFW`: the content filter rejected the prompt or source image. Do not
  retry the same input; the credit-safe fix is rewording (remove suggestive
  wording, real-person likenesses, violence) or a different source image.

## 5. Rate limits

Published rate limits are sparse and vary by plan tier. If you see
throttling (429s or queued jobs piling up): serialize requests, add
exponential backoff, and batch work rather than firing parallel
generations. Sustained throttling on a paid plan is a support ticket, not a
code bug.

## 6. Input format problems

- Image-to-video and image utilities need a reachable source image (URL the
  service can fetch, or an upload through the tool's expected parameter).
  Local paths that only exist on the user's machine will not work for the
  hosted server unless passed through the tool correctly.
- Respect the caps: images up to 4K, videos up to 15 seconds. Requests past
  the caps fail or get clamped.
- Aspect ratios: pick standard ones (1:1, 16:9, 9:16); unusual ratios are
  more likely to be rejected or distorted.

## 7. Model unavailable

The 30+ model catalog rotates. If a named model errors as unknown, list the
server's current models and pick the closest current equivalent instead of
retrying the stale name.
