---
name: pdf-translate
description: Translate a local text-based PDF through bounded JSON batches while preserving the source layout workflow. Use when the host can access local files, read and write UTF-8 files, run Python and shell commands, and the active chat model must perform the translation without provider APIs or model subprocesses.
---

# PDF translation

The active chat model is the translator. Bundled scripts only prepare, persist, render, and validate local PDF work; never call a model, provider API, or credentialed service. Default output is translated-only.

## Compatibility boundary

Before starting, confirm that the host has local PDF access, UTF-8 file read/write access, Python process execution, shell access, and permission to run first-time dependency setup. If any capability is absent, stop and report: `Unsupported host: pdf-translate requires local files, UTF-8 read/write, Python, shell access, and first-run setup.` Do not attempt a fallback.

## Workflow

Take the target language and page range from the request. Infer an omitted source language from the first text-bearing page; ask only if either language remains ambiguous. Use a writable `<job-dir>` and run:

```text
<python> pdf-translate/scripts/run.py doctor --json
<python> pdf-translate/scripts/run.py setup --json
<python> pdf-translate/scripts/run.py prepare --source <pdf> --job-dir <job-dir> --source-lang <code> --target-lang <code> [--pages <range>] [--output-mode translated|bilingual] [--glossary <file>] [--style academic]
<python> pdf-translate/scripts/run.py next --job-dir <job-dir> --json
<active chat model reads batch_path and writes {"translations":[{"id":"...","text":"..."}]} only to the returned job-owned response_path>
<python> pdf-translate/scripts/run.py submit --job-dir <job-dir> --input <batch-response-path>
<repeat next/submit until state is READY_TO_RENDER>
<python> pdf-translate/scripts/run.py render --job-dir <job-dir> --json
<python> pdf-translate/scripts/run.py validate --job-dir <job-dir> --json
```

For an existing job, run `<python> pdf-translate/scripts/run.py status --job-dir <job-dir> --json` instead of `prepare`, then continue from its next action. Follow this decision tree exactly: `doctor/setup -> prepare or status -> next -> active model translation -> submit -> repeat -> render -> validate -> return PDF`. `render` only stages output; `validate` publishes after all blocking structural checks pass. Return only the non-conflicting final PDF path reported by a successful `validate`, together with linguistic warnings and the first/middle/last preview pairs for visual inspection. Read [translation policy](references/translation-policy.md) before translating and [job format](references/job-format.md) before handling job JSON. Whenever work stops before completion, report the `<job-dir>` so a later task resumes from files rather than transcript history.
