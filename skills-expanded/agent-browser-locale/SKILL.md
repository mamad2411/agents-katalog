---
name: agent-browser-locale
description: Test locale- and i18n-specific browser behavior with agent-browser by forcing a non-English JavaScript runtime locale through CDP. Use when reproducing or verifying bugs involving date/time markers, number or currency separators, Intl APIs, RTL behavior, or behavior that differs under locales such as sv-SE, tr-TR, zh-TW, de-DE, or ar-EG.
---

# Test browser locale behavior

Use the installed `agent-browser` skill. Before running browser commands, load its current core guide with `agent-browser skills get core`.

`agent-browser` has no locale-emulation command. Chrome's `--lang` flag does not reliably change the JavaScript runtime locale on macOS. Use CDP `Emulation.setLocaleOverride` and keep the CDP session that applied it open for the entire test.

## Set up an isolated browser

1. Resolve `scripts/cdp-locale.mjs` relative to this `SKILL.md`. Run it through its shebang; do not prefix it with `node`.
2. Create a task-specific Chrome profile with `mktemp -d`.
3. Launch Chrome headlessly with that exact profile and a dynamically assigned debugging port:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --user-data-dir="$LOCALE_PROFILE_DIR" \
  --remote-debugging-port=0 \
  --no-first-run \
  --no-default-browser-check \
  about:blank
```

Run Chrome as an ongoing execution session and retain its execution-session ID. Do not background it with `&`. Wait for `$LOCALE_PROFILE_DIR/DevToolsActivePort`, then read the first line as the assigned port. If visible Chrome is genuinely necessary, launch it through an escalated execution request because it is a GUI action.

4. Generate a dedicated browser session name:

```bash
LOCALE_SESSION=$(agent-browser session id --scope cwd --prefix locale-test)
```

Pass `--session "$LOCALE_SESSION"` to every `agent-browser` command.

5. Start the helper as a second ongoing execution session and retain its execution-session ID:

```bash
/absolute/path/to/agent-browser-locale/scripts/cdp-locale.mjs sv-SE "$LOCALE_PORT"
```

The helper must print `setLocaleOverride sv-SE: ok` and remain running. If it exits, every later result is invalid.

6. Connect agent-browser to the same Chrome target:

```bash
agent-browser --session "$LOCALE_SESSION" connect "$LOCALE_PORT"
agent-browser --session "$LOCALE_SESSION" reload
agent-browser --session "$LOCALE_SESSION" eval "(1234.5).toLocaleString() + ' | ' + new Intl.DateTimeFormat().resolvedOptions().locale"
```

Expect the requested locale, such as `1 234,5 | sv-SE`. If the result still reports `en-US`, stop. Do not report browser behavior gathered without a passing locale gate.

## Drive and verify the page

Use the normal agent-browser snapshot and interaction loop, always with the dedicated session. Re-snapshot after navigation because refs become stale.

When proving a fix, compare the buggy and fixed builds under the same live locale. Confirm the buggy baseline reproduces before treating the fixed result as evidence. If a baseline is unavailable, retain the locale-gate output as the minimum validity evidence.

Useful stress locales include:

- `sv-SE`: Swedish `em`/`fm`
- `tr-TR`: Turkish `ÖS`/`ÖÖ`
- `zh-TW`: Chinese `下午`/`上午`
- `ar-EG`: Arabic formatting and RTL behavior

The locale override survives navigation on the attached page while the helper remains connected. It does not automatically prove that a newly created page target inherited the override. Re-run the locale gate after opening a new tab or target.

## Clean up safely

Stop only the two retained execution sessions. Never use `pkill`, process-name matching, or `agent-browser close --all`.

Close only the skill-owned browser session:

```bash
agent-browser --session "$LOCALE_SESSION" close
```

After Chrome has stopped, remove only the exact profile directory returned by this run's `mktemp -d`. Validate that the recorded path is non-empty, is not `/`, and is the task-created temporary directory before recursively removing it.

## Failure rules

- If the helper dies or the locale gate changes to `en-US`, discard subsequent results.
- If Chrome or the helper hangs or fails, stop and report the captured error instead of retrying broad cleanup commands.
- Never use the user's real Chrome profile for locale testing.
