---
name: web-sqli-validation
description: Validate a scoped SQL injection hypothesis through reproducible response differentials. Use when a supervisor assigns capabilities: web.sqli.validate.
license: project
compatibility: OpenTgtyLab Worker Protocol v1; manifest web.sqli-validation@1.0.0.
metadata:
  open-tgtylab-id: web.sqli-validation
  version: 1.0.0
  digest: 78b5dc0f642057624ad8325875888bf092e48d01f5bef5e89d72f249783a3e8d
allowed-tools: http.differential
---

# SQL Injection Validation Procedure

1. Verify the endpoint, parameter, baseline evidence, and scope snapshot. Finish when all anchors match the assigned Case revision.
2. Establish repeatable baseline ranges before changing the parameter. Finish when noise is measured rather than guessed.
3. Compare paired controls with SQL-semantic variants at low frequency. Finish when every claimed differential reproduces against a matched control.
4. Classify the hypothesis and return evidence-linked observations. Finish when the result states the oracle, confidence, blockers, and graph relation updates.

## Contract

Return `schemas/worker-result-v1.schema.json`. Echo skill ID `web.sqli-validation`, version `1.0.0`, and digest `78b5dc0f642057624ad8325875888bf092e48d01f5bef5e89d72f249783a3e8d` through the assigned task anchors.
