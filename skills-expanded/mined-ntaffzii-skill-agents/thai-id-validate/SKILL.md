---
name: thai-id-validate
description: Use this skill for any task validating a Thai national ID or tax ID checksum, normalizing a Thai phone number, or generating a PromptPay QR code payload. Trigger on "เลขบัตรประชาชน", "เลขประจำตัวผู้เสียภาษี", "checksum บัตรประชาชน", "PromptPay QR", "สร้าง QR พร้อมเพย์", "Thai national ID validate", "13 digit ID checksum". If the task only needs a regex length check with no checksum or QR generation, this skill is still the right one to load — a naive 13-digit regex is exactly the mistake this skill exists to prevent.
---

# Thai ID / Phone / PromptPay Validation

## Overview

A Thai national ID (and tax ID, same 13-digit scheme) has a checksum digit, not just a fixed length — a model that validates with `^\d{13}$` alone will happily accept an ID that fails the real check. PromptPay QR codes are EMVCo TLV-encoded with a CRC-16 checksum; hand-rolling this without the exact tag structure and CRC algorithm produces a QR code that scanner apps reject. This skill supplies the real checksum algorithm, phone normalization, and a working EMVCo payload builder.

## When to use

- ตรวจเลขบัตรประชาชน/เลขผู้เสียภาษี 13 หลักว่า checksum ผ่านไหม
- Normalizing a Thai phone number from mixed formats (`081-234-5678`, `+66 81 234 5678`, `66812345678`) to a single canonical form
- Generating a PromptPay QR payload string for a mobile number or national ID proxy, static or with a fixed amount

## When NOT to use

- The task needs to verify an ID belongs to a real, specific person — that requires a government lookup (DOPA), not a checksum; checksum only proves the *number is well-formed*, not that it is *real* or *belongs to anyone in particular*
- The task needs an actual scannable QR *image* — this skill produces the payload string; rendering it as a QR code image needs a QR-encoding library (e.g. `qrcode` in Python), which is outside this skill's scope

## Core knowledge

**National ID / tax ID checksum** (13 digits, weighted mod-11):

```
sum = Σ d[i] * (13 - i)   for i = 0..11  (first 12 digits)
check_digit = (11 - (sum % 11)) % 10
```

The 13th digit must equal `check_digit`. This is the same algorithm for a personal national ID and a juristic-person tax ID.

**Phone normalization**: canonical local form is `0` + 9 digits (10 digits total, e.g. `0812345678`). International form drops the leading `0` and prefixes `66` (e.g. `66812345678` or `+66 81 234 5678`).

**PromptPay QR payload** (EMVCo QR Code for Payment Systems, Thai PromptPay profile): a flat TLV (tag-length-value) string:

| Tag | Meaning | Value |
|---|---|---|
| `00` | Payload Format Indicator | `01` |
| `01` | Point of Initiation Method | `11` static (no amount) / `12` dynamic (fixed amount) |
| `29` | Merchant Account Info (PromptPay) | nested TLV: `00`=GUID `A000000677010111`, `01`=mobile proxy (`0066` + 9-digit phone) or `02`=13-digit national/tax ID proxy |
| `53` | Transaction Currency | `764` (ISO 4217 numeric code for THB) |
| `54` | Transaction Amount | THB amount, 2 decimals — only present on a dynamic QR |
| `58` | Country Code | `TH` |
| `63` | CRC | CRC-16/CCITT-FALSE (poly `0x1021`, init `0xFFFF`, no reflect, xorout `0`) of everything up to and including the `6304` tag+length prefix, appended as 4 uppercase hex digits |

Each TLV entry is `tag(2 chars) + length(2-digit decimal) + value`.

## Common mistakes

1. Validating a Thai ID with only a `^\d{13}$` length regex — misses the checksum entirely, the most common "looks valid, isn't" bug.
2. Computing the checksum with the wrong digit order or off-by-one weight — the weight is `13 - i` for 0-indexed `i`, not `12 - i` or reversed.
3. Normalizing a phone number by just stripping dashes without handling the `+66`/`66` international prefix — produces an 11-12 digit string that isn't the canonical local form.
4. Building a PromptPay payload with the wrong CRC algorithm (e.g. plain CRC-16/IBM or a reflected variant) — the spec requires CRC-16/CCITT-FALSE specifically; any other variant produces a QR that fails the bank app's checksum check even though it looks structurally right.
5. Forgetting that the CRC is computed over the payload string *up to and including* the literal `6304` prefix, not the full string with a placeholder CRC already in it.
6. Using proxy type `02` (national ID) with an ID that hasn't been checksum-validated first — a malformed ID produces a QR that scans but routes to nothing.

## Code

`validate.py` — no dependencies:

- `validate_thai_id(id_number)` → `bool`, accepts input with spaces/dashes
- `compute_thai_id_checksum(first_12_digits)` → the check digit
- `generate_test_id(first_12_digits)` → checksum-valid synthetic ID, for test fixtures only
- `normalize_phone(raw)` → canonical `0XXXXXXXXX` form
- `build_promptpay_payload(proxy_type, proxy_value, amount=None)` → `proxy_type` is `"mobile"` or `"national_id"`
- `crc16_ccitt_false(data: bytes)` → the raw CRC, independently testable against the standard catalogue vector

Run `python3 validate.py` for the self-test — includes a CRC-16/CCITT-FALSE reference check value (`"123456789"` → `0x29B1`, the standard catalogue test vector) plus round-trip checksum generation/validation and full TLV round-trip parsing of a generated PromptPay payload.

## Known limitations

- Checksum validation proves the *number is well-formed*, not that it belongs to a real, specific person — never treat a passing checksum as identity verification.
- `build_promptpay_payload` does not render an image; pass the returned string to a QR-encoding library to get a scannable image.
- Only mobile-number and national-ID proxy types are implemented; e-Wallet ID proxy (tag `03`) is not covered.
- All example IDs used in this skill's self-test are generated by the checksum function itself — never hardcode or commit a real person's national ID as a "test fixture."
