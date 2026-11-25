---
name: pick-model
description: >
  Recommends which model to use for the task at hand — biased toward cloud by
  default, local only when the network is genuinely unreachable — with the
  reasoning shown, not asserted. In opencode, can also switch the session to
  that model. Portable across opencode, Claude Code, and the GitHub Copilot
  CLI; actuation is opencode-only. Use when you ask "which model should I use
  for this", "am I overspending credits on this task", "switch to a cheaper
  model", or want a routing decision explained before acting on it.
---

# pick-model

Decides which model fits a task — never by asserting an answer, always by
showing the axes it inferred and the type it matched, so a wrong match is
visible and correctable. The full method (axes, exemplar matching, cost
computation, consent gate, escalation, actuation) is in
[REFERENCE.md](REFERENCE.md) — read it before doing anything nontrivial here.
This file is the checklist.

## Must not

- **Never require the network to reach a routing decision.** Read the cached
  probe verdict in `preferences.json` first; only probe live if it's stale
  (see REFERENCE.md § Offline detection). The model catalogue itself must
  also come from a pinned/cached source, not a live fetch — see REFERENCE.md
  § Pin the model catalogue.
- **Never hardcode a model name, task type, or hardware number in this
  prose.** Every one of those lives in the data directory (see REFERENCE.md
  § Configuration) — read it live. If a type or model looks wrong, the data
  files are what's stale, not this file.
- **Never guess or invent model IDs.** The only valid IDs are the keys of
  `models.json`'s `models` object — read them from the file, use them
  verbatim. Do not derive, shorten, or substitute IDs from memory or from
  what sounds plausible.
- **Never silently continue after a failed model switch.** If `pickmodel_switch`
  returns an error, stop immediately, report the exact error to the user, and
  ask whether to proceed on the current model or take a different action. Do
  not begin or continue the user's original task on the wrong model without
  explicit approval.
- **Never read `costPerMTokUSD` directly when `costOverride` is present.**
  Always resolve through `costOverride.effectiveCostPerMTokUSD` first — see
  REFERENCE.md § Cost computation. This is an enforced code path, not a
  convention to remember.
- **Never silently treat a firewall allowlist block as "offline."** The two
  look identical from inside a naive probe; REFERENCE.md § Offline detection
  gives the exact signal that tells them apart. Getting this wrong sends the
  user down the wrong fix (there's nothing to "wait out" on a blocked domain).
- **Never block on consent.** The credit gate informs; it does not gate
  execution. Ask once per type, remember the answer, re-ask only when an
  estimate blows past what was consented to — never require an answer in
  order to proceed at all.
- **Never escalate to a better model automatically.** Only the user's explicit
  "that wasn't good enough" triggers a step-up — see REFERENCE.md §
  Escalation. Record the failure either way.
- **Never write to `models.json`'s `ollama/*` entries or
  `hardware.json`'s `hardware`/`ollamaEndpoint` keys.** Those belong to
  `ollama-curate`. This skill owns `preferences.json` entirely, plus
  `hardware.json.creditAllowance` and `models.json`'s `github-copilot/*` and
  `anthropic/*` entries and narrow ollama tier corrections (see REFERENCE.md
  § File ownership).

## Checklist

1. **Load state.** Read `hardware.json`, `models.json`, `preferences.json`
   from the data directory (REFERENCE.md § Configuration). If the cached
   `creditAllowance` is absent or from an earlier session, fetch the live
   allowance and remaining balance once and cache it — never ask for a seat
   type, and degrade silently to money-only if the fetch fails. See
   REFERENCE.md § Credit allowance and balance.
2. **Match the task to a type.** Exemplars first, cheap and textual; only run
   full axis inference when nothing matches well, then mint a new type with
   its own exemplars. See REFERENCE.md § Matching a task.
3. **Print the axis line and matched type before acting.** This is the
   mitigation for a confidently-wrong exemplar match — visibility, not
   certainty.
4. **Check reachability** (cached verdict, live probe only if stale) and
   branch: cloud-default, or local-only-when-offline. See REFERENCE.md §
   Offline detection for the exact signal classification — a firewall block
   is not "offline" and must never be phrased as one.
5. **Pick the model, filtered to what this harness can reach.** See
   REFERENCE.md § Harness reachability first — a `github-copilot/*` or
   `ollama/*` model is not a real option inside Claude Code, and an
   `anthropic/*` model is not a real option inside Copilot CLI, regardless of
   cost. Within the reachable set: Online — cheapest model on the matched
   type's axes, resolving cost through `costOverride`,
   `githubCopilotPricingCorrections`, or `anthropicPricingMechanics` as the
   model's provider requires (REFERENCE.md § Cost computation). Offline: the
   best local model that fits, per `models.json`'s ollama tier data — or say
   plainly that this task type has no offline coverage, per its
   `offline.modelKey: null` note, if that's what the data says.
6. **Run the consent gate** if the estimated cost exceeds ~$1.00, or reaches
   roughly 3× the level this type already consented to. Express it as money
   first, credits second (Copilot only — `anthropic/*` has no credit unit, so
   state money alone there), with the remaining balance alongside when one
   was fetched. Inform, never block. See REFERENCE.md § Consent gate.
   **Then check pace:** if the fraction of allowance remaining is below the
   fraction of the period remaining, warn and start proposing cheaper models
   — see REFERENCE.md § Pace warning. Skip both the balance and the pace
   check for non-Copilot providers — for `anthropic/*` this is not a gap to
   fill later, there is no fetchable balance to check pace against (see
   REFERENCE.md § Credit allowance and balance's Anthropic subsection).
7. **Explain the choice** — the reasoning is the product, written so the user
   can overrule it, not an oracle's verdict.
8. **State provenance** (`assumed` vs `measured`) for the type's default and
   say so plainly.
9. **Actuate — opencode only.** Call the `pickmodel_switch` tool directly
   (provided by `.opencode/plugin/pick-model.ts`) with
   `{providerID, id, variant?}` — use the exact `providerID` and `id` keys
   from `models.json`, verbatim, never invented. The tool validates against
   the live catalogue before switching (REFERENCE.md § Actuation). **If the
   tool returns an error:** stop, report the full error text to the user, and
   ask explicitly: "Should I proceed on the current model, or do you want to
   investigate the switch failure first?" Do not begin the user's task until
   they answer. In Claude Code and Copilot CLI, no such tool exists — print
   the exact switch command instead and say plainly that switching isn't
   available there.
10. **After a local run**, opportunistically read `/api/ps` and correct the
    tier verdict if it disagrees with the cached prediction — narrow
    corrections only, not a full re-derivation (that's `ollama-curate`'s job).
11. **On explicit failure feedback** ("that wasn't good enough"), record it
    against the matched type's model and escalate for the next call — see
    REFERENCE.md § Escalation. Never infer failure on your own.

## Packaging

Canonical file: this one, at `.agents/skills/pick-model/SKILL.md`. Discovered
via symlinks at `.claude/skills/pick-model` and `.opencode/skill/pick-model`
(both → `../../.agents/skills/pick-model`). Copilot CLI needs no extra step —
it reads `.agents/skills/` natively. The actuation half
(`.opencode/plugin/pick-model.ts`) is opencode-only and auto-discovered, no
config entry needed.

The plugin imports `@opencode-ai/plugin`, declared in `.opencode/package.json`
(`node_modules/` is gitignored). In a fresh checkout run `npm install` in
`.opencode/` once, or the `pickmodel_switch` tool will not register.
