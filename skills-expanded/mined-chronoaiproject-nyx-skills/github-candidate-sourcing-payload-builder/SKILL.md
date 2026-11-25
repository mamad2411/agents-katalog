---
name: github-candidate-sourcing-payload-builder
version: "2.2"
description: Runs the GitHub candidate sourcing flow end to end and posts a digest to the chat.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - github-candidate-sourcing
    - lark
    - payload-builder
  clawdbot:
    emoji: "mag"
    files:
      - "references/*"
      - "scripts/*"
---

# GitHub Candidate Sourcing

You (the agent) run the WHOLE flow yourself with your tools, then POST the result to the current Lark chat. Do NOT refuse, do NOT just describe. If a data source or sink is unavailable, SKIP it and still post what you have.

Use this when someone asks to source, score, rank, or summarize GitHub candidates for the
`AI Tools Application Engineer` role.

## How to run it

1. **COLLECT via tools, using ONLY bound connectors.** Resolve the role, JD, target regions,
   score threshold, and any explicit source limits from the user. If absent, use the bundled
   workflow defaults: `AI Tools Application Engineer`, score threshold `5`, and GitHub searches
   across Singapore, Shanghai, Beijing, Shenzhen, Hangzhou, Hong Kong, and New York.
   - GitHub -> `nyxid_proxy` slug `api-github` (bound ✓). Search users, dedupe by `login`, keep
     only `type: "User"`, then fetch `GET /users/{login}` and
     `GET /users/{login}/repos?sort=pushed&per_page=5`.
   - Public web / RSS / Hacker News (and any other public endpoint) -> `web_fetch` (no credential,
     ✓). Use these only for public evidence that helps sourcing or context.
   - ⚠ `api-reddit` and `api-twitter` are NOT bound for this bot — do NOT depend on them. Use
     `web_fetch` on public endpoints instead where possible; otherwise SKIP that source and note
     `(<source> skipped — connector not bound)` in the message. NEVER fail the run because one
     source is unavailable.

2. **ANALYZE with your own model.** Summarize each usable profile, then score and rank candidates
   against the JD. Look for LLM or AI agent work, MCP or agent-framework experience, LLM APIs,
   API integration, Python/JS skills, AI tooling, open-source AI contributions, and Singapore or
   China tech ecosystem relevance. Produce a compact JSON evaluation per candidate:
   `{ "score": 7, "reason": "one sentence", "signals": ["signal1", "signal2"] }`.

3. **BUILD the message body by running `scripts/build_github_candidate_sourcing_payload.js` via
   `code_execute` with language `"javascript"` and the collected data.** `code_execute` has NO
   stdin, so inline each scored candidate into the code: paste the whole script, then call its
   exported `buildPayload` once per candidate. The script exports `module.exports = { buildPayload }`,
   so end the code with something like:
   ```javascript
   // ...full contents of scripts/build_github_candidate_sourcing_payload.js above...
   const candidates = [
     { candidate: { /* profile fields */ }, role: "AI Tools Application Engineer", score: 7, reason: "...", signals: ["..."] }
   ];
   console.log(JSON.stringify(candidates.map(buildPayload)));
   ```
   Use the builder output (one record per passing candidate; `skip` below the score gate) to form
   one digest message: title, search scope, counts searched/scored/passing/skipped, ranked
   candidate bullets, GitHub links, scores, reasons, signals, and any skipped-source notes. If you
   cannot run code, fall back to `references/github-candidate-sourcing-contract.md` for the same
   fields and score gate.

4. **POST it to the CURRENT chat via `lark_messages_send`** (or `lark_messages_reply` /
   `reply_with_interaction`). THIS STEP ALWAYS HAPPENS — it is the demo output. If no usable
   candidates were found, still post a short digest saying what was searched and why there are no
   candidates.

5. **OPTIONAL: write a Lark Bitable record best-effort ONLY.** Do this only if a target base
   `app_token` and table id are actually provided for this run. If not, SKIP and still post the
   chat message. Never block on a missing Bitable. When writing is available, use the builder's
   `lark.body` and matching record endpoint through the provided Lark/NyxID sink, and include
   write success/failure counts in the digest.

## Payload builder reference

Bundled script: `scripts/build_github_candidate_sourcing_payload.js`.

The script accepts candidate fields at the root or under `candidate`, `profile`, `githubCandidate`,
or `github_candidate`, plus direct `score` / `reason` / `signals` or parseable model output under
`llmOutput`, `modelOutput`, `claudeResponse`, or `groqResponse`.

Required normalized inputs are `githubUrl`, `name` or `login`, and `score` or parseable model
output. It applies `score >= 5` and returns `needs_more_information`, `skip`, or a normalized
candidate/evaluation object with `fields` and optional `lark.path` / `lark.body`. Exact aliases and
examples are in `references/github-candidate-sourcing-contract.md`.

## Guardrails

- Post the current chat digest even when some sources, Bitable, or optional sinks are unavailable.
- Use real returned data only; never invent profiles, scores, write ids, or connector results.
- Credentials and token exchange must go through bound tools; never ask the user for raw secrets.
