---
name: docs-readme
description: "READMEs that answer the first questions: what it is in one sentence, who it is for, how to install and run it in under a minute, a quick start that works when pasted, usage examples, configuration, where the full docs are, how to contribute, the licence, and badges only for real signals; with variants for libraries, applications, CLIs and internal services. Read before writing or rewriting a README."
---

# READMEs that answer the first questions

The generated README opens with "ProjectName is a powerful, blazing-fast
solution for modern teams", lists twelve features as adjectives, gives an
install command for a package that was never published, a usage example
calling `foo()`, a row of fifteen badges and "PRs welcome!". Readers decide
on the first screen whether to go on, and that screen told them nothing.
This skill gives the order, what each section holds, and the variants for
each kind of project. The method (reader first, facts read from the code)
is in `docs`.

## 1. The first screen

In this order:

1. `# name`, then one sentence saying what it does, for whom, with what
   result: "Copies the rows that changed between two PostgreSQL databases,
   on a schedule or once." Not the name restated ("acme-sync is a sync
   tool"), not a slogan.
2. A few badges on the next line (section 7), or none.
3. Two to four sentences on when to use it and when not: its limits, and
   what to use instead. "It does not copy schema changes: run your
   migrations on both sides first." Saying when not to use it is what
   makes the rest believable.
4. A screenshot or a terminal recording, for anything people look at.
5. Install, then the quick start.

A status line goes at the very top when it changes the reader's decision:
"Experimental: the API will change before 1.0", or "Deprecated: use
`acme-replicate` instead", with a link.

## 2. The template

Every value in a real README comes from the project. This one illustrates
a Rust CLI:

````markdown
# acme-sync

Copies the rows that changed between two PostgreSQL databases, on a
schedule or once.

[![CI](https://github.com/acme/acme-sync/actions/workflows/ci.yml/badge.svg)](https://github.com/acme/acme-sync/actions/workflows/ci.yml)
[![crates.io](https://img.shields.io/crates/v/acme-sync)](https://crates.io/crates/acme-sync)

Use it to keep a reporting database close to production without logical
replication. It does not copy schema changes: run migrations on both sides
first.

## Install

Needs PostgreSQL 14 or later on both sides.

```sh
cargo install acme-sync
```

## Quick start

```sh
export SOURCE_URL=postgres://reader@db.example.com/app
export TARGET_URL=postgres://writer@localhost/reporting
acme-sync run --tables orders,customers
```

```text
orders      1204 rows copied
customers     37 rows copied
```

## Usage

...

## Configuration

| Variable | Default | Description |
|---|---|---|
| `SOURCE_URL` | (required) | Connection string of the database to read |
| `BATCH_SIZE` | `1000` | Rows written per transaction on the target |

## Documentation

Guides and the full reference: https://acme.example.com/docs

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT OR Apache-2.0, at your option.
````

## 3. Install

- The real commands, for the package managers the project really
  publishes to. Check the name on the registry and in the manifest: an
  install line for a package or a Homebrew formula that does not exist is
  the most common README error.

| Ecosystem | Library | Command-line tool |
|---|---|---|
| JavaScript | `npm install acme` (or `pnpm add`, `yarn add`, `bun add`) | `npm install -g acme`, or `npx acme` to run it once |
| Python | `pip install acme` or `uv add acme` | `pipx install acme` or `uv tool install acme` |
| Rust | `cargo add acme` | `cargo install acme` |
| Go | `go get example.com/acme@latest` | `go install example.com/acme/cmd/acme@latest` |
| Homebrew | | `brew install acme` |
| Container | | `docker run --rm ghcr.io/acme/acme:1.4.0` |

- Prerequisites with versions, read from the manifest (`engines`,
  `requires-python`, `rust-version`, `go.mod`): "Node.js 22 or later", not
  "a recent Node".
- A container example pins a version tag (`:1.4.0`), never `latest`.
- From source, when people need it: clone, the build command, where the
  output lands.
- End with the check that it worked: `acme --version`, and what it prints.

## 4. Quick start

- It works when pasted in order, on a clean machine with only the stated
  prerequisites. This is the part readers try first; when it fails, they
  leave.
- The shortest path to one visible result, about a minute of the reader's
  time: 3 to 10 lines of commands or code, then the output they should
  see.
- No `$` prompts in the block; secrets through environment variables,
  never inline; each placeholder explained under the block.
- If it needs an account or an API key, say where to get one, with a link.
- A library's quick start is a whole program: imports, setup, the call,
  printing the result.

## 5. Usage and configuration

- Examples for the three to five main tasks, each under a heading named
  for the task ("Copy only new rows", "Run on a schedule"), with a sentence
  and a code block. Everything else goes in the docs.
- Configuration: a table of name, default and description for up to about
  15 options, with the defaults read from the code. Beyond that, the few
  everyone sets and a link to the full reference.
- Where configuration comes from and which source wins (flags, then
  environment variables, then the config file, then defaults), and the
  file's path on each operating system.

## 6. Variants

**Library**

- The three to six main entry points, a line each, and a link to the
  generated reference (docs.rs, pkg.go.dev, the TypeDoc or Sphinx site).
- Compatibility: supported runtimes and versions (Node.js, Deno, Bun,
  browsers; Python versions; the minimum Rust version), module formats
  (ESM, CommonJS), optional features (Cargo features, Python extras) and
  what each adds.
- The stability promise: semantic versioning, and what counts as public.

**Application** (web, desktop, mobile)

- "Run it locally" as numbered commands: clone, `cp .env.example .env`,
  install, start the services (`docker compose up -d`), migrate, seed,
  start, and the URL to open.
- The variables from `.env.example` in a table, required ones marked, with
  no secret values.
- The test command, and what must be running for it.
- The top-level folders, a line each, when the layout is not obvious.
- How it is deployed, or a link to that.

**CLI**

- Install for each platform, including prebuilt binaries from the
  releases page with their checksums, and shell completions.
- A table of commands (command, what it does), and a short excerpt of
  `--help` copied from the binary, never retyped.
- Exit codes when scripts depend on them; the config file's location; the
  environment variables.
- A terminal recording made with VHS (a `.tape` file kept in the repo, so
  it can be recorded again when the output changes) or asciinema.

**Internal service**

- Owners: the team, its chat channel, the on-call rotation.
- What it does, who calls it, and what it calls.
- Run locally, test, deploy: the pipeline, and how to roll back.
- Dashboards, logs, alerts and runbooks, linked (`docs-architecture`), and
  the SLOs if there are any.
- Where configuration and secrets live: the secret manager's path, never
  the values.

**Monorepo**

- The root README says what the repository holds, lists each package or
  app with a line and a link, and gives the shared setup.
- Each published package has its own README: that is the one its registry
  page shows.

## 7. Images, badges and GitHub details

- Screenshots or recordings of the real product at its current version,
  with alt text saying what they show. Never a mock-up presented as the
  product.
- Small files (compressed PNG, a GIF of a few MB at most) in `docs/images/`
  or `.github/`. Light and dark versions with `<picture>`:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/report-dark.png">
  <img alt="The sync report: three tables and the rows copied from each" src="docs/images/report-light.png" width="720">
</picture>
```

- Badges only for signals a reader uses: CI status of the default branch,
  the latest version, the licence, a docs link, coverage if someone
  watches it. Not "made with", "PRs welcome", or badges for services the
  project stopped using. Four to six at most.
- GitHub builds an outline from the headings, so a hand-written table of
  contents is only worth it for a long README read elsewhere.
- Alerts (`> [!NOTE]`, `> [!WARNING]`) for the one thing that must not be
  missed, never as decoration. Mermaid renders in fenced blocks tagged
  `mermaid`.
- A README published to a registry (npm, PyPI, crates.io) is shown there
  too, and relative links and images can break; PyPI does not resolve them
  at all. Use absolute URLs into the repository, and look at the rendered
  page after publishing.

## 8. The rest

- Documentation: one line with the link.
- Support: where to ask (issues, discussions, a chat), without promising a
  response time nobody gave you.
- Contributing: a link to `CONTRIBUTING.md` (setup, tests, style, how pull
  requests are reviewed); inline only for a very small project. The code of
  conduct, if there is one.
- Security: a link to `SECURITY.md`, which says how to report a
  vulnerability privately.
- Licence: the SPDX identifier and a link to the `LICENSE` file. Never
  choose or change a licence yourself: it is the owner's legal decision.
  With none, leave `[TODO: licence]` and say so in your report.
- Acknowledgements and sponsors only when they are real.

## 9. Length

- The README is the front door: the first screen, install, quick start,
  the main tasks and links. Past about 300 lines, move the reference and
  the guides into `docs/` and link them.
- Cut sections with nothing specific in them: a "Features" list of
  adjectives, a "Roadmap" with nothing dated or linked, an "FAQ" of
  questions nobody asked, "Why acme?" marketing.
- A feature list earns its place when each item is a capability:
  "Resumes an interrupted copy from the last committed batch", not
  "Reliable".

## Check it

- Every command pasted into a clean environment (an empty directory or a
  fresh container), and its output compared. Without `bash`, trace each
  one to the manifest, script or CI step that defines it, and list in your
  report the ones not run.
- Package names, commands and versions match the registry and manifests.
- Every link and image path resolves (`glob` the relative ones).
- The first sentence says what it does without restating the name, and
  nothing on the first screen is an adjective without a fact.
- No secrets in examples, and `.env.example` holds no real values.

## Avoid

The name restated as the first sentence; adjectives in place of
capabilities; install lines for packages that do not exist; a quick start
nobody ran; `foo` and `bar` examples; secrets or real-looking keys in
examples; walls of badges; screenshots of a mock-up or an old version;
choosing a licence for the owner; a README that tries to be the whole
documentation.
