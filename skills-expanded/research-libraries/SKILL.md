---
name: research-libraries
description: "Choosing a dependency: whether a library is needed at all, finding candidates, comparing them on fit, maintenance, adoption, licence, size, types, security history and API quality, trying the top one or two in a few minutes, and recommending with the trade-offs and the rejected options. Read before recommending or adding a library."
---

# Choosing a dependency

The naive pick is the first search result or a name remembered from
training, chosen by its stars: a whole date library with every locale for
one formatted date, an abandoned package with an install script, a GPL
licence inside a closed product, no alternative looked at, and no way out
later. A dependency is code you ship and maintain without having written it.
This is how to decide whether you need one, compare two or three on dated
facts, try the favourite, and recommend it with what was rejected and why.
Where the facts about packages live online is `research-web`.

## 1. First: is a library needed?

- The platform may already do it. For example:
  - JavaScript: `fetch`, `structuredClone`, `crypto.randomUUID()`, `URL` and
    `URLSearchParams`, `AbortController`, `Intl` (dates, numbers, plurals,
    lists, relative time, `Segmenter` for graphemes), `Object.groupBy`,
    `Array.prototype.toSorted`; in Node, `node:test` and `util.parseArgs`.
  - Python: `pathlib`, `dataclasses`, `zoneinfo`, `tomllib`, `argparse`,
    `itertools.batched` (3.12), `asyncio.TaskGroup` (3.11).
  - Go: `slices`, `maps` and `log/slog` (1.21), methods and wildcards in
    `net/http` route patterns (1.22).
  - Rust: `std::sync::OnceLock` (1.70) and `LazyLock` (1.80) in place of
    `lazy_static` and `once_cell`.
- The project may already have one: search the lockfile before adding a
  second date, HTTP or validation library.
- Write it yourself when it is small, stable and easy to get right (a
  `clamp`, an ASCII slug, a retry loop). Take a library when the domain is
  full of edge cases: cryptography, time zones and calendars, parsing (CSV
  with quotes, HTML sanitising, Markdown, URLs), Unicode, authentication
  protocols, anything security-sensitive.
- When the project or its framework already names a choice (`frontend`,
  the `backend-stack-*` skills), that choice wins over a fresh comparison.

## 2. The requirement, then the candidates

- Write the requirement in one sentence with the case that matters most:
  "format and parse dates in the user's time zone, DST changes included,
  in the browser and on Node 22". Every candidate is judged against it.
- Two or three candidates, not ten, from: the framework's docs (its
  recommended integrations and recipes), what mature projects on the same
  stack use (read their manifests), the registry's search, and curated
  lists as leads.

## 3. Compare on facts

| Criterion | What to find out | Where | Warning sign |
|---|---|---|---|
| Fit | the requirement, hard case included; runs where the project runs (Node version, browsers, edge runtimes, Bun or Deno, the OS) | docs, types, a trial | needs a polyfill or another runtime |
| Maintenance | last release and its date, commits in the last six months, issues answered, pull requests merged, active maintainers | repository, registry | archived; no release in two years with bugs open |
| Adoption | weekly downloads, dependents, projects you know that use it | registry, deps.dev | tiny use for a critical job |
| Licence | MIT, Apache-2.0, BSD and ISC suit most projects; LGPL with care; GPL and AGPL in closed or hosted software need the owner's decision; SSPL, BSL and Commons Clause terms are not open source | `LICENSE` at the version, `license` in the manifest | missing, custom, or changed recently |
| Size | frontend: the gzipped cost of what you import, tree-shaking (ESM, `sideEffects: false`); elsewhere: transitive dependencies, native builds, compile time | bundlephobia or pkg-size, `npm ls`, `cargo tree`, deps.dev | a large bundle for a small job; a native build step |
| Types | built in (`types` in `package.json`, `py.typed`) or a maintained `@types/` package | manifest, repository | `any` at the surface |
| Security | past advisories and how fast they were fixed, install scripts, provenance, the OpenSSF Scorecard | osv.dev, GitHub advisories, deps.dev | unfixed advisories; a `postinstall` that downloads |
| API and docs | clear, versioned docs with examples, a changelog, migration guides | the docs site | breaking changes in every minor |
| Way out | can you reach the layer below it, swap it, keep your data format | docs | owns your data format or your architecture |

- Stars measure attention at some moment, not health: weigh them least.
- Record each fact with its source and date ("4.1.0 released 2026-08-12,
  npm"), never an adjective ("actively maintained").

## 4. Fit with the project

- The latest stable release, not an alpha, beta, rc or canary, unless the
  feature exists only there; then it is a risk named in the recommendation.
- `peerDependencies` against the project's framework major (React, Vue,
  ESLint), and `engines` against its Node version.
- Module format: an ESM-only package in a CommonJS project needs `import()`,
  or a Node recent enough to `require()` an ES module (22.12 and later).
  Read `type` and `exports` in its `package.json`.
- Python: `requires-python`, and wheels for every platform the project
  runs on (without one, the install compiles from source). Rust: its
  `rust-version` against the project's toolchain. Go: its `go` directive.
- Duplicates: a second major of a library already in the tree ships both;
  `npm ls <pkg>` and `cargo tree -d` show them.

## 5. Red flags

- Abandoned: archived, no release in two years with security issues open, a
  maintainer asking for someone to take over.
- One inactive maintainer on something critical.
- Install scripts (`preinstall`, `install`, `postinstall`) that download or
  run binaries; read the package's `scripts`.
- A dependency tree far larger than the job.
- A breaking change in every release, or no changelog at all.
- A name one letter from a popular package, a missing or mismatched
  repository link, a new package with a sudden jump in downloads.
- Minified or obfuscated code in a package that should be readable.
- Ownership transferred recently, followed by a burst of releases.
- A licence changed away from open source. For infrastructure that did
  this (Terraform, Redis, Elasticsearch), compare the current licence with
  the community fork (OpenTofu, Valkey, OpenSearch) before choosing.

## 6. Try the favourite in fifteen minutes

With a shell that may install, in a scratch folder outside the project:

```sh
mkdir -p /tmp/try-dates && cd /tmp/try-dates && npm init -y >/dev/null
npm i date-fns@4
node --input-type=module -e 'import { format } from "date-fns";
  console.log(format(new Date(2026, 8, 29), "d MMM yyyy"))'        # 29 Sep 2026
echo 'export { format } from "date-fns"' > entry.mjs
npx esbuild entry.mjs --bundle --minify --format=esm | gzip -c | wc -c   # bytes shipped

uv run --with httpx python -c 'import httpx; print(httpx.__version__)'  # Python, throwaway env
cargo new /tmp/try-x && cd /tmp/try-x && cargo add <crate> && cargo tree | wc -l
```

- Try the main use and the hard case from the requirement (a DST change for
  dates, a 500 MB file for a parser, a timeout for an HTTP client), and the
  error it gives when misused.
- Measure what you ship, not the package's full size: the bundle of what
  you import, or the dependency count after install.
- Agents that cannot install (`research`, `review`, the orchestrator) read
  instead: the README's examples, the types (`index.d.ts`), the
  repository's tests for the hard case. Their recommendation says the trial
  is still to be done, and gives these commands.

## 7. The recommendation

```
Pick: <name> <version> (<licence>)
Why: <how it meets the requirement, hard case included>;
  <maintenance facts with dates>; <size, measured or reported, with source>
Runner-up: <name>: better at <x>; not chosen because <y>
Rejected: <name> (archived <date>), <name> (AGPL-3.0),
  <name> (<n> kB gzipped for one function)
Without a library: <what the platform offers, and where it falls short>
Risks: <one maintainer, a major in beta, a native build>; to replace it
  later, keep its imports in one module (<path>)
Evidence: <registry and repository URLs> read on <date>; trial: <output, or not run>
```

- Facts with dates and sources, not adjectives.
- The runner-up and the rejected are part of the answer: they show a choice
  was made, and save the next person from making it again.
- Say when the honest answer is "no library": the platform covers it, or the
  code is ten lines.

## 8. After it is added

- Installed with the project's package manager, so the lockfile changes in
  the same commit; one package manager per project.
- A replaceable library is imported in one module that the rest of the code
  calls, so replacing it later touches one file. Frameworks are not wrapped.
- Updates arrive through Renovate or Dependabot with the project's
  grouping, where it has them; majors are read, not merged blind.
- A security or licence review, if the project has one, sees it before it
  ships (`security-supply-chain`).

## Check it

- The requirement is one sentence with its hard case, written before the
  comparison.
- Every criterion has a fact, a source and a date.
- The licence was read from the `LICENSE` file at the version, not only
  the registry's field.
- The trial ran, or the recommendation says it did not and gives the
  commands.
- The platform alternative was considered and its limit stated.

## Avoid

Picking by stars or from memory; a library for a few lines; a second
library for what an installed one already does; abandoned packages and
surprise install scripts; GPL or AGPL added without the owner's decision;
bundle size ignored for frontend code; adjectives instead of dated facts; a
recommendation with no runner-up and no rejected options; adapters around
frameworks.
