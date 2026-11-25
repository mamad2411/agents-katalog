---
name: osint-source
description: Use when an open-source finding needs recording — captures what was observed, where it came from, and when, keeping the observation separate from the inference and checking the finding against the workspace scope before it is written. Triggers - "log this source", "record this OSINT finding", "add this to the source register".
allowed-tools: Bash(mkdir *), Bash(date *), Bash(grep *), Bash(wc *), Read, Write
---

# OSINT Source

Record an open-source finding with its provenance, keeping what was observed apart from
what it is taken to mean.

## When to use

- Something relevant was found in public material and needs to be on the record.
- A source must be captured before it changes or is removed.

## Inputs

- A URL, or a description of where the material was found. Required.
- Notes on what it shows. Optional — asked for if not supplied.

## Procedure

### 1. Check it against scope first

Read `SUBJECT`, `SCOPE`, and `BOUNDARIES` from the workspace fact block. If the finding
falls outside the declared scope, or reaches material the boundaries exclude, stop and
say which boundary it crosses. Do not record it and then note the problem — refuse
first.

Boundaries commonly exclude: material about people incidental to the subject, anything
requiring a login or circumvention to reach, and anything that would identify a private
individual who is not the subject. Treat what the workspace says as binding.

### 2. Preserve the material

A live URL is not a record. Hand the URL to the companion evidence agent's `capture-web`
skill to archive it, and use the resulting path here. If that agent is unavailable, say
so and record that the source is unpreserved — that is a real weakness in the finding.

### 3. Separate the three layers

Record them as distinct fields, never merged into a narrative:

- **Observed** — what the material literally shows. Quotes, visible dates, stated names.
  A second person reading the archive must be able to confirm every word of this.
- **Inferred** — what it is taken to mean, and why.
- **Confidence** — how firmly, and what would change it.

The discipline here is the whole value of the record. An inference recorded as an
observation cannot be unwound later.

### 4. Record provenance

- The URL or location, exactly.
- When it was accessed, in UTC.
- What kind of source it is — primary, secondary, self-reported, aggregated, or unknown.
- Whether the account or site is attributable to anyone, and on what basis.
- The path to the preserved copy.

### 5. Append to the register

One JSON object per line in `sources/register.jsonl`, never rewriting an earlier line.
Write the readable finding to `findings/<slug>.md` and reference the register id.

### 6. Check for contradiction

Search existing findings for the same subject or claim. If this contradicts something
already recorded, say so and record both — do not overwrite an earlier finding, and do
not quietly prefer the newer one.

## Output

- One line in `sources/register.jsonl` and one finding file.
- A note of any contradiction with existing material.

## Notes

- Aggregator sites and republished content are not primary sources. Record what was
  actually looked at, not what it claims to be quoting.
- Absence of a result is a finding too, and worth recording — including what was searched
  and how.
- Public availability is not the same as free use. Say when material carries constraints.
