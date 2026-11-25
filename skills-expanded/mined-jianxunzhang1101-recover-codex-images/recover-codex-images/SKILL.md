---
name: recover-codex-images
description: "Automatically use alongside imagegen for every image generation or edit request, even when the user does not mention this Skill and no failure is visible yet. After imagegen returns, recover, verify, save, and display the new image from local task records. Also use for blank or missing image output."
---

# Recover Codex Images

Treat this Skill as the required companion to imagegen for every image generation or editing request. Let the applicable image-generation workflow fulfill the user's request, then recover and display that turn's result locally. Never modify the source JSONL.

## New Generation Or Edit

Follow this sequence for every generation, regeneration, or image-editing turn, including later modification rounds:

1. Before invoking the image-generation tool, record a local Unix timestamp:

   ```bash
   date +%s
   ```

   Keep the returned value as `<generation-start-epoch>`.
2. Invoke the applicable image-generation or editing tool exactly once as required by the user's request. Do not generate an extra image to test recovery.
3. Resolve the current task identity before recovery. Prefer the exact session path, then the thread ID. The script also reads `CODEX_SESSION_PATH`, `CODEX_ROLLOUT_PATH`, and `CODEX_THREAD_ID`-style environment variables automatically. Use automatic session-directory scanning only when none of those are available.
4. Immediately after the image tool returns, run:

   ```bash
   python3 "${CODEX_HOME:-$HOME/.codex}/skills/recover-codex-images/scripts/recover_last_generated_image.py" \
     --after <generation-start-epoch> \
     --wait-seconds 10 \
     --json
   ```

   Add `--session /absolute/task.jsonl` when the exact record is known, or `--thread-id <thread-id>` when only the current task ID is known. Add `--verbose` only when diagnostics are needed; progress is written to stderr and the JSON output remains clean on stdout.
5. If recovery reports no new complete result after the timestamp, report failure. Never fall back to or display an image from an earlier turn as the new result.

Repeat all five steps for every later modification request. Always capture a new timestamp before the new image call.

## Save Or Show An Existing Result

When the user only asks to save or show the last image and no new generation occurs, omit `--after`:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/recover-codex-images/scripts/recover_last_generated_image.py" \
  [--session /absolute/task.jsonl] \
  [--thread-id <thread-id>] \
  --json
```

If task selection is ambiguous, list the candidates and ask for an explicit task path. Do not choose silently.

## Verify And Reply

Read the JSON output. Verify that `path` exists, is readable, and has the reported SHA-256. Then use the exact absolute path for both forms:

```markdown
![生成的图片](</absolute/path/generated-image.png>)

[打开本地图片](</absolute/path/generated-image.png>)
```

Also report the format, dimensions, file size, and SHA-256. If the script fails or the file cannot be verified, do not claim that the image was saved or displayed.
