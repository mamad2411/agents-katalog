---
name: html-workbench
description: Start or reuse the bundled local HTML Workbench and return a visual editor URL for a local .html file. Use when the user asks to generate HTML and make it editable, convert an HTML page to an editable state, open a local HTML file in a visual editor, or continue AI and human editing against the same source file.
---

# HTML Workbench

Open a complete local HTML document in the bundled GrapesJS workbench. Keep the source file as the shared source of truth for visual edits and later AI edits.

## Workflow

1. Resolve the target `.html` file to an absolute path. When the user asks to generate a page, read `references/editable-html-guidelines.md` and generate one complete, self-contained HTML document containing `html`, `head`, and `body`. Inline its CSS and JavaScript; embed required visual assets; do not create a multi-file web project or depend on a CDN unless the user explicitly asks for that trade-off.
2. Generate position-independent interactions that use stable semantic markers, delegated events, and idempotent initialization. For a page with business JS, test the interaction in preview mode after opening it.
3. Resolve the directory containing this `SKILL.md`. Treat its `scripts/workbench.py` as the service entrypoint and `scripts/validate_html.py` as the compatibility validator.
4. Find Python 3 in this order:
   - Run `python3 --version`.
   - Run `python --version` if `python3` is unavailable.
   - On Windows, run `py -3 --version` if both commands are unavailable.
5. Require Python 3.9 or newer. If no compatible interpreter exists, explain that the workbench needs Python 3.9+ and ask for confirmation before installing software. After confirmation, use the platform's normal trusted installer or package manager, then repeat the version check.
6. Read `references/validation-rules.md`, then validate the page before opening it. For a newly generated default page, require one self-contained file:

```text
<python> <skill-dir>/scripts/validate_html.py --require-self-contained <absolute-html-path>
```

For an existing page that intentionally has relative resources, omit `--require-self-contained` and clearly report that it is not a single-file deliverable. Fix every reported error. Review warnings and remove structural JS/CSS coupling when practical; if a warning is intentionally accepted, state the assumption.
7. Always run `open` as the normal entrypoint. Do not run `serve` first: `open` checks the default local port, reuses a running HTML Workbench service when available, or starts it in the background when needed. It prints one JSON object containing the editor URL and whether the service was reused.

```text
<python> <skill-dir>/scripts/workbench.py open <absolute-html-path>
```

8. On the first run, allow the service to download the pinned GrapesJS assets. It verifies their SHA-256 hashes and caches them locally; later runs do not require network access. Do not download or inject an unverified substitute yourself.
9. Read the JSON written to stdout. When `ok` is true, open `url` in the available browser when browser control is available. In every final response, also return the URL as a clickable link, name the generated HTML file, and state whether the service was started or reused. If a browser cannot be opened automatically, tell the user to open that exact URL in any browser.
10. If startup fails, report the returned error and inspect the log path when one is provided. For `VENDOR_DOWNLOAD_FAILED`, explain that all configured sources were unreachable and ask the user to check the network before retrying. Do not replace the service with an ad-hoc server.

## Service commands

Run the service independently in the foreground:

```text
<python> <skill-dir>/scripts/workbench.py serve
```

Use `serve` only when a user explicitly wants to manage the foreground service. For normal Skill use, run `open <html-file>` instead.

Check an existing service:

```text
<python> <skill-dir>/scripts/workbench.py health
```

Use `--port` only to avoid a confirmed port collision. `--editor-root` is accepted for backward compatibility but no longer restricts which files the workbench may open; the service resolves any existing local `.html` file by absolute path.

## Logs

The service writes rotating logs to a fixed per-user directory (survives temp cleanup):

```text
~/.cache/html-workbench/logs/          # Windows: %LOCALAPPDATA%\html-workbench\logs
```

- `workbench-<port>.log` — structured log (timestamp, level, request path, error code/message, unhandled stack traces), rotated at 1 MB × 5 files. This is the file to check first when something fails.
- `html-workbench-<port>.log` — raw stdout/stderr of the service process (startup JSON and anything not routed through the logger).

Override the directory with `--log-dir` on `serve`/`open`.

## Safety and file behavior

- Bind only to `127.0.0.1`; never expose the editor on a public interface.
- Treat the specified HTML file as the source of truth. The workbench writes visual edits back to it.
- Preserve external file changes with revision checks; never force an overwrite after a conflict.
- Do not install Python or another runtime without explicit user confirmation.
- Keep third-party assets pinned and hash-verified. The service tries a China-friendly npm mirror first and falls back to three public CDNs.
- Return the URL instead of claiming the browser is editable before the health check and document load succeed.
