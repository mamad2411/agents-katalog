---
name: forensic-investigation
description: Use when an incident needs investigating — a breach, credential abuse, unexpected spend or traffic, suspicious activity, data exposure — and the user asks to investigate, establish what happened, collect evidence, or build a timeline. Use before any report is written.
user-invocable: true
disable-model-invocation: true
---

# Forensic investigation

Establish what happened, from evidence that would survive challenge. The full
procedure is steps 0–4 of `references/RUNBOOK.md` and the package layout is
`assets/template/`, both in this skill's folder. This skill is the working
discipline. For the reasoning behind the rules — including the bias research —
read `references/PROCESS.md`; sources are in `references/REFERENCES.md`.

## Iron rules

1. **Read-only.** An investigation records; it never fixes. No create, modify,
   tag, start, stop, delete, no credential operations — even "harmless" ones.
   If remediation is urgent, hand it to a responder and timestamp their
   actions as timeline rows.
2. **Provenance first.** Before any other capture: collector identity as the
   system sees it, collection start time, exact tool versions. Evidence item
   zero is always "who am I and when is it".
3. **Copies, hashes, custody.** Work on copies. Hash at collection time. Sign
   or counter-sign the digest file. Custody log starts at row one, not at the
   end.
4. **Volatile first.** Collect what disappears soonest (RFC 3227 order of
   volatility). Check retention windows before starting and request
   preservation for anything near expiry.
5. **Everything is evidence.** Zero-event results, failed queries, capped
   samples — capture and label them. Truncation must be labelled SAMPLE with
   the window it truly covers.
6. **Two sources per claim.** Corroborate each finding from independent
   sources; record agreements and disagreements both.
7. **Write it down as you go.** Command, time, tool, result. Contemporaneous
   notes, not next-day reconstruction.

## Checklist (copy into todos)

- [ ] Authority in writing; scope quoted verbatim; legal posture decided
- [ ] Read-only access confirmed; correct account context; no elevation
- [ ] Retention clocks checked; preservation requested where needed
- [ ] Origin alert/ticket captured as evidence: payload, rule + version,
      triage notes, case record
- [ ] Containment order agreed with responders: preservation before
      rebuild/eradication; already-destroyed artefacts listed with time and
      actor
- [ ] Package created from `assets/template/`; custody log row 1 written
- [ ] Collection scripted (`scripts/collect.sh`), not improvised
- [ ] Provenance captured as evidence `00-*`
- [ ] Collection in volatility order; negative results kept
- [ ] `SHA256SUMS` written, signed; manifest generated
- [ ] Analysis only via one no-network transform script
- [ ] Every claim: evidence path + corroboration row + alternatives considered
- [ ] Timeline rows all cite evidence, labelled [F]/[A]/[R]
- [ ] Handoff: unknowns stated as unknown, not guessed

## Rationalisations to refuse

| Thought | Reality |
|---------|---------|
| "I'll just disable the key while I'm here" | That is response, not investigation. Hand it off; record the time. |
| "This log is probably irrelevant" | Collect it. Relevance is decided at analysis, not collection. |
| "I'll hash everything at the end of the week" | Unhashed days are undefendable days. Hash at collection. |
| "One source is clear enough" | Single-source claims are where corrections come from. Corroborate or label the limit. |
| "I'll clean up the raw JSON so it's readable" | Raw stays raw. Readability lives in `analysis/`. |
| "The timestamp is close enough" | Timezone slicing has produced material corrections. Convert programmatically, declare UTC. |
| "Responders already rebuilt the host, nothing to collect" | Record what was destroyed, when, by whom — the gap is a finding. Then collect the sources that survive. |
| "The SOC alert is just the trigger, not evidence" | The alert, the rule that fired and the triage notes are evidence item candidates like any log. Capture them with provenance. |

## Hand off

When collection and analysis are done, writing moves to the `forensic-report`
skill. That skill starts only when a person runs it, so report that the
evidence layer is hashed and catalogued and ask for `/forensic-report`. Do not
start writing findings before that point.

## Handling

Investigation packages contain sensitive material (account identifiers,
addresses, names, costs). Create packages outside this skills repository, give
them their own classification and handling rules, and never paste their
contents into external services. This skill sends nothing to any external
service; collection happens inside the environment under investigation, with
the access the investigation was authorised to use.
