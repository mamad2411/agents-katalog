---
name: support-partner-deep-research
description: Investigates a reported customer issue interactively from intake to ranked resolution, emitting a JSON investigation summary and a Markdown report with stated confidence. Use when asked to diagnose, troubleshoot, or find the root cause of a reported issue, or to rank candidate fixes — not for open-ended research (use research) or for writing the escalation ticket itself (use support-escalation or escalation-writing).
spec_hash: 68f0a7dc96cd
---

# Support Partner Deep Research

Run the investigation as a **terminal script that owns the pipeline**. The script
enforces the stage order, the privacy gate, and rendering in code. You invoke the
model only for the judgment steps, through a role resolved by `ollama-role` —
never a hardcoded model tag. The agent skill wraps the script; it never
re-implements the pipeline in prose.

The stage order: read input → parse → anonymize + redact → gather evidence → form
hypotheses → test → rank solutions → emit summary.

## Parse by detected type

Sniff the input type from a fixed set — support thread / plain text, JSON /
JSONL, log / stack trace, HAR, configuration — and pick the streaming parser for
that type. Honor an explicit `--type` override when sniffing is wrong. Unknown
types fall back to plain text **with a note on stderr**, never a silent guess.

## Anonymize then redact before the model

No diagnostic model sees raw input. Pseudonymize attachments through the
`context-anonymizer` engine, then apply the fail-closed redaction layers. The
diagnostic model receives only pseudonymous, redacted text.

Hold the real→substitute mapping in the calling process — never send it to any
model or write it to any artifact. Anonymization and redaction must preserve the
technical literals the diagnosis depends on: error strings, version numbers,
timestamps. Losing the evidence is a failure, not a pass.

## Backstop the output

Before anything is emitted, re-run the deterministic detectors over the final
summary. A high-confidence hit fails closed: exit non-zero, write nothing.

## Frontier handoff is downstream of the gate

You MAY run heavy diagnosis on a powerful frontier model **only** when the input
has passed the `context-anonymizer` judge gate. Disclose that the material is
pseudonymous and that distinctive context may still re-identify the subject.
Never use a frontier model for anonymizing, redacting, or judging, and never send
it raw input or the mapping.

When the material may never leave the host, keep diagnosis on the local-only path
and make no frontier call, regardless of operator convenience.

## Refuse mis-invocation loudly

Reject duplicate input or output flags. Refuse to read stdin when stdin is a
terminal and no input was supplied — print the reason on stderr and exit
non-zero instead of hanging.

## Diagnose in phases

Validate the problem before proposing any fix: what the customer intended, what
happened instead, when it started, reproducibility, impact. Then:

1. **Form hypotheses** ranked by prior likelihood. Each carries the specific
   evidence or test that would confirm or eliminate it.
1. **Test** in order of safety and informativeness (logs → isolated non-production
   → production canary). Record why each hypothesis was confirmed or ruled out.
1. If no hypothesis is confirmed, keep testing — do not emit an ungrounded
   resolution.

## State calibrated confidence

Attach an explicit confidence band to the root cause and each resolution —
confident / most likely / multiple plausible / below threshold. Flag the
assumptions that would invalidate the diagnosis and the data that would change
the confidence. Below threshold, say so; never assert a single cause as settled.

## Rank solutions

Rank by feasibility, risk, impact, and timeline. Separate **immediate
mitigation** (stops the symptom), **root fix** (addresses the cause), and
**long-term prevention**. Each carries implementation steps, validation steps,
and a rollback plan.

## Detect escalation, don't write it

Escalation is warranted when the issue needs expertise outside the domain,
reveals a systemic gap, requires code changes, or leaves uncertainty when further
testing is risky. When warranted, name it and hand off to `support-escalation`
or `escalation-writing` with the problem summary, evidence gathered, ranked
hypotheses, what was ruled out, and the specialist input needed. Never write the
escalation ticket yourself.

## Emit both artifacts

Emit a JSON investigation summary and a Markdown report derived from the same
field values. JSON keys: `investigation_id`, `timestamp`, `problem_model`,
`root_cause_analysis`, `evidence_chain`, `hypotheses_eliminated`,
`solutions_ranked`, `next_steps`, `escalation`, `confidence`. Emit JSON only when
the user asks.

## Never

- Never send raw (unanonymized) input to any model.
- Never put raw input, the mapping, unverified output, or the summary into logs,
  progress output, error messages, or any retained or versioned artifact. Report
  a leak by class and count, never by value.
- Never fabricate an identifier — account name, org slug, issue ID, version,
  timestamp, attachment name, log line, URL — that is absent from the pseudonymous
  source. A stated gap beats a plausible-looking invention.
- Never build fixtures from real customer material, even redacted or paraphrased.
  Synthesize.
- Never use a retaining hosted endpoint for anonymize, redact, or judge. Local
  first; ZDR only as fallback for those stages; refuse and say why when neither is
  available.
- Never make a frontier call for material that may not leave the host.
- Never disable or route around the anonymization, redaction, judge-gate,
  local-inference, or human-review controls without saying so on stderr — and
  never offer a flag that skips verification while still producing output.
- Never run the proposed fixes, apply config changes, restart services, or file
  the summary into any external system. Implementation and egress are the
  operator's deliberate act.
