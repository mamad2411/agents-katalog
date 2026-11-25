---
name: happycode-imagegen
description: Generate or edit raster images through the HappyCode OpenAI-compatible GPT Image 2 API. Use when the user requests HappyCode or this project uses it as the default backend for new images, reference-image transformation, composition, inpainting, editing, batches of 2-5 images, or first-use configuration.
---

# HappyCode Image Gen

Use only the HappyCode clients in `<SKILL_DIR>/scripts`; do not call the built-in `image_gen` tool or another provider. Run the client directly after reading this file. Do not inspect other skill files, read `config.json`, run tests, probe the API, or perform setup unless the client returns `CONFIG_REQUIRED`. The clients own authentication, request defaults, proxying, timeout, downloads, PNG validation, and output creation.

## Decide And Prompt

1. Treat a request without an input image as generation. Treat a requested change to an existing image as an edit; ask for a target only when none is available.
2. Identify each supplied image as an edit target, reference, mask, or supporting input. Pass every relevant non-mask image with repeated `--image`; use `--mask` only for a supplied mask.
3. Ask another question only when a missing detail makes execution impossible.
4. Pass the user's request verbatim as the `--prompt` argument, except for the batch transformation below. Do not translate, paraphrase, expand, censor, or add style, content, negative, or preservation instructions. Resolve pronouns only when selecting inputs.
5. Shell-quote every dynamic argument so the client receives the exact prompt and paths as argument values.

## Track Edit Inputs

- Internally remember the input target for every successful `SAVED` path; a text-only generation has no input. Do not print or persist this bookkeeping.
- For a normal follow-up, edit the latest successful result.
- If the user rejects the latest result, apply the correction to its remembered input target instead of the rejected image. If it had no input, generate again without `--image`. Preserve all other explicit requirements.
- For a batch, keep each saved path associated with its `BATCH_RESULT` index. Resolve ordinal references such as "the second image" by that index; ask which image only when a follow-up does not identify one of multiple results.

## Batch Generation

- Interpret a quantity as an output count only when it explicitly modifies the requested images. A subject count inside one image is not a batch.
- For 2-5 new images, derive one prompt per image and use one batch client. Replace only the output-count phrase with a one-image phrase; preserve all other text.
- If the request asks for differing attribute values, replace only the applicable `不同` with `随机` when that makes each derived prompt standalone; otherwise retain the wording.
- For more than 5 outputs, start no client and ask the user to reduce the count. For an unclear count such as "多个" or "一些", ask for a number.

## Execute

Use Node first:

```bash
node "<SKILL_DIR>/scripts/imagegen.mjs" --prompt "<request>"
node "<SKILL_DIR>/scripts/imagegen.mjs" --image "<target>" --prompt "<edit>"
node "<SKILL_DIR>/scripts/imagegen-batch.mjs" --prompt "<derived prompt 1>" --prompt "<derived prompt 2>"
```

When the protocol permits fallback, use an available Python 3 launcher (`python3`, `python`, or `py -3`) and the corresponding client:

```bash
python "<SKILL_DIR>/scripts/imagegen.py" --prompt "<same request>"
python "<SKILL_DIR>/scripts/imagegen-batch.py" --prompt "<derived prompt 1>" --prompt "<derived prompt 2>"
```

Add `--out` only when the user requests another destination. On image-capable surfaces, otherwise use the default `<working-directory>/output`; on other surfaces, ask for a destination first. Do not create unrequested variants.

The clients use a 600-second network timeout. Start one client process for the operation; the batch client owns its concurrent children and forwards termination signals to them. Never restart, inspect output files, or start another command while that process is active.

With `functions.exec`, keep the client invocation and every continuation inside one `functions.exec` call. Begin its JavaScript input with this exact first line and use the control flow below, replacing only `cmd` with the fully shell-quoted single or batch command:

```javascript
// @exec: {"yield_time_ms": 660000, "max_output_tokens": 20000}

const first = await tools.exec_command({
  cmd: '<shell-quoted client command>',
  yield_time_ms: 30000,
  max_output_tokens: 20000,
});
let result = first;
let output = first.output || "";
let sessionId = first.session_id;
while (sessionId != null) {
  const next = await tools.write_stdin({
    session_id: sessionId,
    chars: "",
    yield_time_ms: 300000,
    max_output_tokens: 20000,
  });
  result = next;
  output += next.output || "";
  sessionId = next.session_id;
}
text(JSON.stringify({ exit_code: result.exit_code, output }));
```

Do not let `functions.exec` return while `sessionId` is non-null, and do not move `write_stdin` into a later model turn. An outer `Script running with cell ID` is non-terminal; continue that same `functions.exec` cell rather than starting another model-driven client or session continuation.

## Client Protocol

| Result | Required action |
| --- | --- |
| `ERROR: CONFIG_REQUIRED: <path>` plus `CONFIG_EDIT_COMMAND:` | Follow Configure below. Do not retry until the user confirms configuration. |
| `RUNTIME_UNAVAILABLE:` | No API request started. Run the corresponding Python single or batch client exactly once; never show the marker. |
| `SAVED: <absolute-path>` | Treat the path as internal technical completion and edit-lineage state; never echo the marker. |
| `BATCH_RESULT: <json>` | Record the result by its 1-based `index`. Use `saved`, `config_path`, and `config_edit_command` according to `status`; never expose the protocol line. |
| `BATCH_SUMMARY: <json>` | Treat it as the batch outcome after the process exits. Follow Configure for `config_required`, use Python once for `runtime_unavailable`, and for `partial` keep saved paths in index order, report `failed_items` concisely, and never retry them automatically. |
| Explicit `ERROR:` or non-zero exit other than `RUNTIME_UNAVAILABLE:` | Treat the operation as failed or completion-unknown. Do not fall back or retry automatically. |
| Zero exit without `SAVED:` | Treat it as a client-protocol failure and do not retry automatically. |
| Active `session_id`, empty/truncated output, or no exit status | Treat it as non-terminal and continue waiting on the same process. Do not report completion or timeout. |

If the shell cannot start `node`, use the corresponding Python client because no API request started. Never search output directories for a result or switch providers.

## Configure

1. Check only whether the reported config path exists. If absent, copy `<SKILL_DIR>/config.example.json` there unchanged; if present, do not overwrite it.
2. Tell the user to set `api_key` locally. Normally leave `base_url` and `model` unchanged; set `proxy` to a URL or `""`.
3. In Codex desktop, provide an absolute clickable link to the config file. In a terminal-only response, provide its absolute path and the exact `CONFIG_EDIT_COMMAND:` value in one fenced block.
4. Wait for confirmation, then retry the original operation exactly once.

Never read, display, or modify existing config values, and never ask the user to paste an API key into the conversation.

## Complete

- `SAVED` proves only that a file was saved. Inspect it only when the user requests review, the task requires visual validation, or the next edit needs visual understanding.
- Compare an inspected result only with the exact request. Report unmet requirements without retrying; make a targeted correction only when the user asks.
- On image-capable surfaces, return saved batch images in `BATCH_RESULT` index order. Otherwise return only the saved images inline with concise alt text unless the user requested a path, explanation, or review, or a batch partially failed. On other surfaces, report the requested saved path concisely.
