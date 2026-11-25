---
name: pynecore-docs
license: MIT
description: "Read the complete PyneCore documentation offline from the copy bundled in this skill. Use whenever a PyneCore / Pyne question needs an exact API signature, parameter list, setting name, CLI flag, file format or behaviour detail that memory cannot guarantee: `ta.*`, `strategy.*`, `request.security`, `input.*`, `ScriptRunner`, `pyne run` / `pyne data` options, the symbol `.toml`, live mode, bar magnifier, profiling, internals. The skill carries every documentation page (about 110 Markdown files), a topic map, a page inventory, a grep/print tool, a version check against the installed runtime and a script that refreshes the snapshot from a PyneCore release. No network and no editor installation are needed."
---

# PyneCore documentation, offline

The full PyneCore documentation lives in this skill's `docs/` folder (PyneCore's own Markdown
pages, Apache-2.0, see `docs/LICENSE` and `docs/NOTICE`). `docs/MANIFEST.json` records which
PyneCore version the snapshot describes. Nothing outside the repository is read.

## 1. Find and open pages

```bash
python3 <skill>/scripts/find_docs.py                    # docs path, documented version vs installed runtime
python3 <skill>/scripts/find_docs.py --list             # every page with its title
python3 <skill>/scripts/find_docs.py --grep "process_orders_on_close"      # search all pages
python3 <skill>/scripts/find_docs.py --grep "exit\(" --context 2
python3 <skill>/scripts/find_docs.py --page reference/lib/strategy.md      # absolute path
python3 <skill>/scripts/find_docs.py --page reference/lib/strategy.md --print
python3 <skill>/scripts/find_docs.py --online reference/lib/strategy.md    # URL of the same page online
```

`--root <project>` points the version check at a project's interpreter (`.venv`, `venv`,
`.pyneide/venv`, or `VIRTUAL_ENV`). Pages can also be opened directly:
`<skill>/docs/<section>/<page>.md`.

## 2. Version check

`find_docs.py` prints the documented version (from `MANIFEST.json`) and the installed
`pynesys-pynecore` version. When they differ and the question concerns a recently changed
feature, confirm against the installed package (`pyne run --help`, `inspect.signature(...)`,
`runner.script.settable_fields()`) before relying on the text, and say so in the answer.

Refresh the snapshot when a new PyneCore release is adopted:

```bash
python3 <skill>/scripts/sync_docs.py --tag v6.12.1            # from the GitHub release (network)
python3 <skill>/scripts/sync_docs.py --from /path/to/pynecore/docs   # from any local checkout
python3 <skill>/scripts/sync_docs.py --check                  # verify files against MANIFEST.json
```

Without access to the release download, the installed wheel is a source too: from 6.12.1 on,
`pynesys-pynecore` ships its documentation as `pynecore/docs/` inside the package (6.12.0 does
not), and the license files sit in the package's `dist-info/licenses/`:

```bash
SP=<venv>/lib/python3.X/site-packages
python3 <skill>/scripts/sync_docs.py --from $SP/pynecore/docs --version 6.12.1 --commit <tag commit> \
    --license $SP/pynesys_pynecore-6.12.1.dist-info/licenses/LICENSE \
    --notice  $SP/pynesys_pynecore-6.12.1.dist-info/licenses/NOTICE
```

`git ls-remote --tags https://github.com/PyneSys/pynecore` prints the commit of each tag.

The sync builds the new snapshot (pages, LICENSE, NOTICE, `MANIFEST.json`) in a temporary folder
and only then replaces `docs/`, so removed pages do not linger and a failed download leaves the
old snapshot intact. It refuses a `--dest` that is not empty and holds no `MANIFEST.json`, and a
`--from` that is the destination or nested with it.
Two pages about converting scripts written in another language through a cloud compiler are
left out by default (`--keep-all` includes them); such conversions are done locally with the
`pynecore-pine2pyne` skill (`../pynecore-pine2pyne/SKILL.md`), which documents its own tool;
the excluded pages matter only when the user asks for the cloud compiler by name.

## 3. Read only what the task needs

Pages are long. Open the one page that answers the question, read the relevant section, and
quote the signature or rule from it instead of paraphrasing from memory. The topic map names
the first page to open; `references/inventory.md` lists every page with a one-line summary.

| Question | Page (relative to `docs/`) |
|----------|----------------------------|
| How a Pyne script is structured, decorators, `main()`, inputs as parameters | `reference/script-format.md` |
| Series, Persistent, function isolation, `na` model | `overview/core-concepts.md`, `scripting.md` |
| Types, `int`-as-float, `NA`, collections, UDTs, enums | `reference/types.md` |
| `input.*` functions and the script `.toml` | `reference/inputs.md`, `overview/configuration.md` |
| Writing and backtesting a strategy, settings, sizing | `strategy.md` |
| `strategy.entry/exit/close/order`, variables, fill timing, several closes per bar | `reference/lib/strategy.md` |
| Open/closed trade queries, risk rules | `reference/lib/strategy_opentrades.md`, `reference/lib/strategy_closedtrades.md`, `reference/lib/strategy_risk.md` |
| Any `ta.*` function | `reference/lib/ta.md` |
| `time()`, sessions, `na`/`nz`/`fixnan`, plot family signatures | `reference/lib/builtins.md` |
| A namespace (`math`, `array`, `map`, `string`, `color`, `barstate`, `timeframe`, `syminfo`, `session`, `label`, `line`, `box`, `table`, `plot`, `log`, `alert`, `request`, ...) | `reference/lib/<namespace>.md` (`reference/lib/str.md` for `string`) |
| `request.security`, lookahead, security data, confirmation timing | `lib/request-security.md`, `reference/lib/request.md`, `overview/symbol-map.md` |
| Currency rates, corporate events | `lib/request-data.md` |
| Running scripts, `pyne run` options, outputs | `cli/run.md`, `cli/basics.md` |
| Data download / convert / aggregate, symbol info | `cli/data.md`, `programmatic/data-and-syminfo.md` |
| `ScriptRunner`, overrides, trades, live feed from Python | `programmatic/script-runner.md`, `programmatic/integration-patterns.md` |
| Plot styles and drawings export (NDJSON) | `programmatic/visual-output.md` |
| Bar magnifier, `calc_on_order_fills` | `advanced/bar-magnifier.md` |
| Live mode, broker trading | `advanced/live-mode.md`, `cli/broker.md` |
| Extra CSV columns in scripts | `advanced/extra-fields.md` |
| Debugging, logging, AST dump | `debugging.md` |
| Profiling | `profiling.md` |
| What is and is not implemented, intentional divergences (no lookahead) | `overview/compatibility.md` |
| Workdir layout, config files, environment variables | `overview/configuration.md`, `overview/project-structure.md` |
| Installation, type-checker setup for editors | `getting-started/installation.md`, `getting-started/ide-setup.md` |
| Plugins, broker plugin authoring, testing | `development/plugin-system.md`, `development/broker-plugin-authoring.md` |
| FAQ | `faq.md` |

Each page starts with an HTML comment holding front matter (`title`, `description`,
`lastmod`); skip it. Internal links are relative (`../reference/lib/ta.md`) and resolve inside
`docs/`.

## 4. Using what you read

- The pages are the upstream project's documentation, verbatim. They describe PyneCore's API
  partly by comparison with the charting language it mirrors; take the PyneCore behaviour and
  signatures from them and leave the comparisons out of your own code and explanations.
- Prefer a page's signature table over an example when they disagree; examples are
  illustrative.
- "Compatibility" notes at the end of reference pages are authoritative for PyneCore's own
  behaviour (what returns `na`, what raises, what diverges on purpose).
- Before using a flag or parameter for the first time, run the CLI `--help` or
  `inspect.signature()` on the installed version once; it costs seconds and catches version
  drift.
- Quote the relevant line with the page name in an answer or code comment; do not paste whole
  pages into project files.

## 5. Bundled files

| Path | Use |
|------|-----|
| `docs/` | The documentation snapshot (`MANIFEST.json`, `LICENSE`, `NOTICE`, pages by section) |
| `scripts/find_docs.py` | Version check, list, grep, resolve and print pages, online URL (stdlib) |
| `scripts/sync_docs.py` | Refresh or verify the snapshot from a PyneCore release tag or a local folder (stdlib) |
| `references/inventory.md` | Every page with a one-line summary, grouped by section |
