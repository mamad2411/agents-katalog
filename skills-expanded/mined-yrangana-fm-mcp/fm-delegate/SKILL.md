---
name: fm-delegate
description: Use when a task involves summarising logs, documents or transcripts, pulling fields out of text, sorting many texts into categories, or reading text in screenshots or photos, and the fm-mcp tools are available.
---

# Delegating to fm-mcp

fm-mcp runs a small, free, private model on this Mac. Give it bulk, low-stakes text work you can check.

**For a file, pass `path`; don't read it yourself.** Once you've read it, doing the task yourself is cheaper.

## Use fm-mcp for

| Task | Tool |
|---|---|
| Condense a log, document, transcript or commit messages | `summarise` |
| Pull named fields from one text as JSON (flat schema) | `extract` |
| Sort texts into labels you choose (one text per call) | `classify` |
| Read the text in a PNG, JPEG, HEIC, TIFF, GIF or BMP image (not PDF) | `ocr` |

## Do it yourself, or with a script, when

- It involves code, config, diffs, maths, or judging causes, designs or correctness.
- A wrong answer would be costly or unsafe: legal, medical, financial, security, or anything published unchecked.
- A script does it exactly: grep, jq, a YAML parser, counting line prefixes.
- It's one short item.

Splitting a task is fine: `ocr` reads a stack-trace screenshot; you fix the bug.

## Size and speed

- `summarise` gives the gist (a paragraph, or at most 7 bullets), not a full record. For every release, item or event, read or grep yourself.
- It takes up to about 30,000 words of prose, but only about 1,000 lines of a dense log; filter bigger logs first. Long input is split and combined: slower, and it can drop details.
- `extract` and `classify` take about 3,500 words of prose per call, far less of a log. Send only the relevant part.
- Calls queue on the shared model; don't send many in parallel.

## Check the results

The model can drop or distort details, mislabel, or put a nearby wrong value in a field. Spot-check what matters.

## When a tool returns an error

| The error says | Do this |
|---|---|
| safety filter refused | Do the task yourself. Don't retry. |
| too long | Send a smaller or filtered part. |
| took longer than | Retry once with shorter input, or do it yourself. |
| got stuck, or didn't match the schema | Try once more: `extract` with a flatter schema and fewer fields, `classify` with fewer labels. (The model may just be busy with another session.) If it fails again, do it yourself. |
| not available, could not start, stopped responding, keeps crashing, could not measure | Do it yourself; suggest `fm-mcp doctor`. |
| a bug in fm-mcp | Do it yourself; tell the user. |
| anything else (unusable schema, unsupported file, labels, empty text) | Fix the call as the message says, once. Otherwise do it yourself. |
