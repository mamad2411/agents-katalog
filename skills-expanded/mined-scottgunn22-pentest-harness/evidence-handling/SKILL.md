---
name: evidence-handling
description: How to capture, hash, name, and reference evidence so findings are reproducible and the report can cite them. Triggers when capturing screenshots, packet captures, or any artifact that supports a finding.
---

# Evidence Handling

## What "evidence" means here

An evidence artifact is anything that supports a finding — tool output,
screenshots, request/response pairs, decoded blobs, extracted samples,
trace snippets. The report cites them by sha256; without that citation, a
finding is unevidenced and fails `--final` validation.

## The automatic path (most cases)

The `evidence_logger` PostToolUse hook captures every non-local tool output
automatically:

- Output goes to `engagements/current/evidence/sha256/<hash>`
- A line is appended to `engagements/current/evidence/manifest.jsonl`
- `trace.jsonl` records the call with the hash

You don't have to do anything for tool output. Reference it in a finding by
the sha256 prefix:

```json
"evidence_refs": ["sha256:abcdef0123..."]
```

## The manual path (screenshots, proxy captures, decoded data)

When an artifact comes from outside a tracked tool call (Burp export, a
screenshot, a manually decoded blob), the operator drops it in and adds a
manifest line:

```bash
hash=$(sha256sum screenshot.png | cut -d' ' -f1)
mv screenshot.png engagements/current/evidence/sha256/$hash
cat >> engagements/current/evidence/manifest.jsonl <<EOF
{"ts":"$(date -u +%FT%TZ)","tool":"manual","sha256":"$hash","size":$(wc -c < engagements/current/evidence/sha256/$hash),"engagement":"$(basename $(readlink engagements/current))","source":"burp-screenshot","tags":["F-003","fileserver01"]}
EOF
```

The agent suggests this format; the operator runs it.

## What to capture, what NOT to capture

**Capture**:
- Tool output that proves a vulnerability exists
- Successful exploitation evidence (one shell prompt is enough — don't
  ride the box to capture novel things)
- Configuration files showing the vulnerable state
- The minimum data needed to prove the finding

**Do not capture**:
- Bulk PII unless the finding *is* "PII is exposed at endpoint X" — then
  capture one representative sample, document the count, redact the rest.
- Production data that isn't needed to prove a finding.
- Credentials in plaintext (those go to `creds.age`, referenced by ID).
- Anything specifically forbidden in `roe.yaml` `banned_techniques` or
  `evidence.exclusions` if present.

## Chain of custody

Every manifest entry includes:

- `ts` — UTC ISO-8601 when captured
- `tool` — what produced it (or `manual` + `source` for hand-drops)
- `sha256` — file digest
- `size` — bytes
- `engagement` — slug, matches the directory
- optional `cmd`, `url`, `host`, `source`, `tags`

The manifest is append-only. If an artifact is later determined to be PII
that should not have been captured, the operator (not you) handles
redaction: the manifest gains a redaction line, and the file is replaced
with a placeholder. The original digest stays in the manifest so the
audit trail is intact.

## Referencing evidence in findings

In a finding's `evidence_refs`, use either:

```
sha256:abcd1234ef5678...           (preferred — full hash)
sha256:abcd1234                    (short — first 8 hex; unambiguous within engagement)
```

In a finding's `reproduction_steps`, cite inline:

```
3. Send the SMB negotiate (see evidence/sha256/abcd1234ef56…) and observe…
```

## Redaction at delivery

`pt-report --final` runs a redaction pass:

- Scans evidence for credentials (NTLM, kerberos tickets, private keys,
  API tokens) and replaces them with `[REDACTED:cred-id=CRED-NNN]`.
- Surfaces PII candidates for operator review; does not redact PII
  automatically because false positives there are common.
- Strips `dead_ends[]` from the rendered report.

Redaction touches the rendered report, not the raw evidence. Originals
stay in `evidence/sha256/` for retest and audit.
