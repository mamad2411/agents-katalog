---
name: eml-header-injection-defense
description: >
  Defend parsers and processors of .eml / raw MIME against header injection and
  header smuggling: duplicate headers, folded lines, encoded-word abuse, and
  unsafe trust of From/Subject when rendering or re-sending. Use for owned
  inbound mail pipelines, ticketing email gateways, and security tooling that
  parses EML—not outbound mailer string concat alone (see email-header-injection-defenses).
---

# EML Header Injection Defense

## Scope And Authorization

- **In scope:** Inbound/outbound MIME parsing in systems you own (ticketing, phishing mailboxes, support tools).
- **Out of scope:** Crafting malicious mail against third-party providers as an attack.
- Treat every EML as untrusted input—like file upload.
- Redact message bodies and addresses in reports.
- Pair with `email-header-injection-defenses` for outbound SMTP construction.

## When To Use

- Building or reviewing EML/MIME parsers, “email to ticket” gateways, or malware sandboxes.
- Findings about header smuggling, ambiguous `From`, or CRLF in stored EML.
- Displaying Subject/From in HTML UIs (XSS via headers).
- Re-mailing or forwarding parsed messages.
- Security products that extract URLs/attachments from MIME.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Outbound SMTP header concat | `email-header-injection-defenses` |
| DMARC reporting | `email-dmarc-reporting-ops` |
| XSS generally | `xss-cross-site-scripting` |
| Attachment malware analysis | malware/RE skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Trust | Never trust client-supplied EML headers for authz |
| Duplicates | Define first vs last header wins; test both |
| Folding | RFC 5322 folded whitespace; reject overlong lines |
| Encoding | Encoded-word (`=?utf-8?b?...?=`) must be decoded safely |
| Display | Escape Subject/From for HTML; no raw HTML in headers |
| Re-send | Rebuild with structured APIs; don’t replay raw attacker headers |

## Workflow

### 1. Confirm scope and success criteria

1. List parsers (language MIME libs, custom split-on-newline).
2. Success: malicious headers cannot inject HTML, extra recipients on re-send, or auth bypass.

### 2. Inventory parse and use sites

```bash
rg -n "eml|message/rfc822|mailparser|BytesParser|MimeMessage|python-multipart" -i
rg -n "Subject|From|Reply-To" --glob '*mail*'
```

1. Note paths: display only, store DB, auto-reply, create user accounts from From:.
2. Flag custom parsers that `split('\\n')` headers.

### 3. Baseline attack corpus (lab)

| Case | Intent |
| --- | --- |
| Duplicate `From` / `Subject` | Ambiguous identity |
| Folded header with CRLF smuggling | Inject `Cc:` |
| Encoded-word with HTML | Stored XSS on decode |
| Extremely long header lines | DoS / truncate bugs |
| Nested multipart name tricks | Attachment confusion |

### 4. Harden parsing

```python
from email import policy
from email.parser import BytesParser

def parse_eml(data: bytes):
    if len(data) > 10_000_000:
        raise ValueError("eml too large")
    msg = BytesParser(policy=policy.default).parsebytes(data)
    # Use library accessors, not raw header block
    subject = msg.get("Subject", "")
    from_ = msg.get("From", "")
    return msg, subject, from_
```

1. Prefer maintained parsers (`email` stdlib, mailparse, etc.) over DIY.
2. Cap size, part count, nesting depth, and individual header length.
3. Normalize Unicode; reject NULs.
4. For security decisions, use **authenticated** results (SPF/DKIM/DMARC from the MTA) not raw From.

### 5. Harden rendering and re-send

1. HTML UI: treat Subject/From as untrusted text (encode entities).
2. Tickets: store original raw EML immutably; display sanitized fields.
3. Forward/replies: construct new messages with SDK; allowlist which headers copy.
4. Never pass EML header values into shell commands.

### 6. Verify with evidence

```bash
# Fixture tests with malicious .eml samples in repo (lab fixtures)
# Assert: no extra recipients on re-send; escaped HTML; parser time-bounded
```

1. Fuzz header blocks with afl/libfuzzer if custom C parser exists.
2. Confirm duplicate-header policy documented and tested.

### 7. Hand off

1. Document max sizes and supported MIME features.
2. SOC runbook if parser is used for phishing intake.
3. Link outbound skill for any generate-email paths.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Parser | Maintained MIME library | `headers, body = raw.split("\\n\\n")` |
| Auth | DMARC-aligned identity | Trust `From` for password reset |
| UI | Escape header text | `innerHTML = subject` |
| Limits | Depth/size caps | Unlimited nested multiparts |
| Re-send | Structured rebuild | SMTP write raw attacker EML |

## Output Checklist

- [ ] EML entry points inventoried
- [ ] Parser library + size/depth limits set
- [ ] Duplicate/folding/encoding cases tested
- [ ] UI escaping verified
- [ ] Re-send path cannot inject headers/recipients
- [ ] Auth decisions not based on raw From alone
- [ ] Residual risk documented

## Rules

- EML is untrusted input.
- Authorized fixtures only—no live phishing of third parties.
- Prefer MTA auth results over header claims.
- Outbound construction → `email-header-injection-defenses`.
- Redact real user mail from fixtures when possible.
