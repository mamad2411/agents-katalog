---
name: brand-memory
description: Create, read, update, validate and audit the project's brand file, .atelier/brand.json (studio, product, voice, hex palette, font stacks, logos, social handles, deploy target, motion and surface tokens). Use when starting a design workflow, running /brand-init, /brand-get, /brand-set or /brand-audit, changing a brand color or font, or checking brand.json against its schema.
---

Skills such as design-token-sync and og-card-generator read this file. Every command works on `<root>/.atelier/brand.json`, with `--root` defaulting to the current directory.

## Run

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand init --studio goneIdle --product TideWane \
  --voice "atmospheric, mysterious" --bg "#110f1b" --accent "#67e8f9" \
  --body-font "Silkscreen, 'Courier New', monospace" --display-font "Space Grotesk, sans-serif" \
  --deploy cloudflare-pages
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand get palette.bg --raw
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand set palette.terra "#e07a5f"
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand set brand.voice "calm, precise"
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand audit
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand validate
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" brand path
```

JS API (synchronous). The module path is passed as an argument and turned into a file URL, so the same line works on Windows, macOS and Linux. This one sets the accent in `./.atelier/brand.json` and prints what the audit still misses:

```bash
node --input-type=module -e "const { pathToFileURL } = await import('node:url'); const m = await import(pathToFileURL(process.argv[1]).href); const cfg = m.setPath(m.loadBrand(process.cwd()), 'palette.accent', '#67e8f9'); m.saveBrand(process.cwd(), cfg); console.log(m.auditBrand(cfg).missing);" "${CLAUDE_SKILL_DIR}/index.mjs"
```

- `loadBrand(root)` returns the validated object. Throws when the file is missing, is not valid JSON, or fails the schema; `err.code` is `BRAND_NOT_FOUND`, `BRAND_INVALID` (with `err.errors`) or `BRAND_UNREADABLE`, and the message names the file. A UTF-8 or UTF-16 BOM is accepted.
- `saveBrand(root, cfg)` returns nothing. Validates first and throws `invalid brand config: ...` (`BRAND_INVALID`) without writing; otherwise writes 2-space JSON plus a trailing newline, or throws `BRAND_UNWRITABLE`.
- `initBrand(root, { studio, bodyFont, primaryColor, product?, voice?, accent?, displayFont?, monoFont?, deployTarget?, withSchema?, overwrite? })` validates everything, writes once, returns the object. `voice` may be a comma string. `accent` goes to `palette.accent`, `deployTarget` to `deploy.target`. `withSchema: true` adds `$schema`. `overwrite: false` throws `BRAND_EXISTS` if the file exists.
- `validateBrand(cfg)` returns `{ valid, errors }` without touching disk.
- `getPath(obj, 'a.b')` returns the value or `undefined`; follows own properties only.
- `setPath(obj, 'a.b', value)` returns a deep clone with the value set and creates missing objects. Throws on `__proto__`, `constructor` or `prototype` segments, empty segments, and non-index keys inside arrays.
- `auditBrand(cfg)` returns `{ missing: string[] }`.
- `brandFilePath(root)`, `BRAND_SCHEMA_URL`, `runCli(argv, { cwd, stdout, stderr })` (returns the exit code).

## Options

- Every command: `--root <dir>` (project root that holds `.atelier/`, default the current directory), `-h`/`--help` (prints usage, exits 0).
- `init`: `--studio`, `--product`, `--voice <a,b,c>`, `--bg <hex>`, `--accent <hex>`, `--body-font`, `--display-font`, `--mono-font`, `--deploy <target>`, `--force`. Omitted `--studio`, `--bg`, `--body-font` default to the root folder name, `#111111` and `system-ui, sans-serif`, and the output says so. Refuses to overwrite without `--force`. Writes a `$schema` key for editor autocomplete.
- `get <path>`: `--raw` prints a string without JSON quotes.
- `set <path> <value>`: the value is parsed as JSON when it is valid JSON, else kept as a string. String fields keep numbers as text, array fields (`brand.voice`, `deploy.stores`) split a comma list, palette values may omit `#`. Extra words are joined with spaces.
- `audit`, `validate`: `--json`.
- Quote `#hex` values in a shell. For a value starting with `-`, use `--body-font=-apple-system,...` or `set -- <path> <value>`.

## Output

Schema (`${CLAUDE_PLUGIN_ROOT}/schemas/brand.schema.json`, JSON Schema 2020-12). Required: `brand.studio`, at least one `palette` color, `typography.body`.

- `palette.<key>`: `#rgb`, `#rrggbb` or `#rrggbbaa`; keys start with a letter (letters, digits, `_`, `-`).
- `typography.body|display|mono`: CSS font stacks, max 300 chars, no `< > { } ;`, backslash or control characters.
- `brand.voice`, `deploy.stores`: string arrays. `deploy.stores` items: `steam`, `itch`, `apple`, `google`.
- `deploy.target`: `cloudflare-pages`, `netlify`, `github-pages`, `vercel` or `custom`.
- Optional `logos.mark|wordmark`, `social.<platform>`, `motion`, `surfaces`, `targets`.

Validation messages name the dotted property and list allowed values, e.g. `deploy.target: "firebase" is not allowed (allowed: cloudflare-pages, ...)`.

Audit checks: `brand.product`, `brand.voice`, `typography.display`, `logos.mark`, `logos.wordmark`, `social`, `deploy.target`.

## Exit codes

- `0`: success, including `--help`. `audit` always exits 0.
- `1`: `validate` found errors (including malformed JSON).
- `2`: usage error, missing or unreadable brand.json, `get` on an unset path, or `init`/`set` rejected (file exists, invalid value, forbidden path).

## Notes

- `/brand-init`: ask for studio, product, voice (2 to 4 adjectives), background hex, accent hex, body font stack, optional display font, and deploy target, then run one `brand init` with all of them and relay its audit. Ask before passing `--force`.
- `/brand-set`: `brand set <path> <value>`, then report the echoed value or the validation message.
- `get`, `set` and `audit` read the file without validating it, so `set` can repair an invalid field (the result is validated before it is saved). `validate` and `loadBrand` enforce the schema; `audit` adds a note when the file does not pass.
