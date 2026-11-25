---
name: benchmark-accuracy
description: Use when the user asks to convert and score a published Bankstatemently benchmark statement. Do not use for ordinary user-statement conversion, spending analysis, or reconciliation.
---

# Benchmark

**Input:** a benchmark statement id, PDF URL, or free-text benchmark request.
**Output:** extraction accuracy, integrity score, overall score, and major failure categories, citing the benchmark statement id and converted document content_hash.

Treat the input as a benchmark statement id, PDF URL, or free-text benchmark request.

<!-- claude-only:start -->
**Before anything else:** if the Bankstatemently tools are not available in this session, the Bankstatemently connector is not connected. Tell the user that first, and how to connect it: Customize → Connectors → Bankstatemently → Connect, which asks them to sign in to a Bankstatemently account. Then ask whether they want to connect or have you do the task directly. If you do it directly, say that the result was not produced by Bankstatemently.
<!-- claude-only:end -->

Follow this sequence:

1. Read the benchmark catalog resource and choose the named published statement.
2. Convert the benchmark PDF with `convert_statement`.
3. Fetch the converted data with `get_statement` using original data mode.
4. Pass the benchmark statement id and original parsed transactions to `evaluate_benchmark`.
5. Present extraction accuracy, integrity score, overall score, and any major failure categories. Cite the benchmark statement id and converted document content_hash.

**Example prompt:** Convert and score the published bsb-004 benchmark statement.
