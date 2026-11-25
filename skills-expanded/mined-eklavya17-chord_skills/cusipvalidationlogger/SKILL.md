---
name: CusipValidationLogger
description: Log and verify CUSIP validation output; always process results after validation.
tools:
  - bash
---

# CUSIP Validation Logger

## Purpose
Logs the result of CUSIP validation and verifies output consistency before returning to the user.

## Workflow
1. Receive the raw `cusip-validator` result.
2. Run: `python pipeline/skills/CusipValidationLogger/scripts/postprocess.py "<validation_result>"`
3. Output the verified result to the user.
