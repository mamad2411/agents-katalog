---
name: document-conformance
description: Use when a repository's design documents have become a pile nobody can navigate — duplicate ids, no status field, several documents on one subject with no way to tell which is current, links that resolve to nothing — and the work is to check a convention, draw the reference graph, or carry the pile onto a convention without inventing facts.
---

# Adopting `@modootoday/devtools-doc-lifecycle`

Reads a tree of markdown documents and returns findings, clusters, dossiers and rendered
views. It never decides what a document means.

## When to reach for it

The condition is a directory of design documents that has outgrown reading. Two distinct
jobs, and a repository usually needs the second before the first.

**Checking.** A convention exists and it should be enforced: filenames match their kind,
ids are unique within a root, statuses come from a closed vocabulary, a document that
claims to implement a file still points at one that exists, links resolve, supersede
chains agree in both directions and do not loop.

**Migrating.** No convention exists yet. Four stages carry the pile across: discover what
is there, cluster what shares a subject, derive the evidence a decision needs, and apply
the decisions a reader made.

The sharpest single question it answers: several documents cover one subject and nobody
can say which is current without reading all of them. That is `clusterDocuments`.

**Do not** reach for it to lint prose, to render a site, or to decide whether a file is a
design document at all — no stage classifies, by design.

## Install and wire

```
npm install --save-dev @modootoday/devtools-doc-lifecycle
```

```ts
import { checkDocuments, loadConfig } from "@modootoday/devtools-doc-lifecycle";

const config = loadConfig(process.cwd());
const { documents, findings } = checkDocuments(process.cwd(), config);

console.log(`${documents.length} documents, ${findings.length} findings`);
for (const finding of findings) console.log(`${finding.code} ${finding.path} ${finding.detail}`);
```

One export path, `.`, ESM only, Node 22 or newer. No runtime dependencies. Six binaries
ship alongside the library:

```
devtools-doc-check     <root> [--config f] [--json] [--all] [--fail-on <codes|any>]
devtools-doc-graph     <root> [--view v] [--format mermaid|dot|json] [--findings]
                              [--id x] [--depth n] [--kind k] [--no-history] [--fail-on ...]
devtools-doc-discover  <root> [--config f] [--out f]
devtools-doc-cluster   <root> [--config f] [--min n] [--subject s] [--json]
devtools-doc-derive    <root> [--config f] [--classified f] [--into d] [--out f]
devtools-doc-apply     <root> [--config f] [--dossier f] [--decisions f] [--write]
```

Run `devtools-doc-check` first on an unmigrated tree and expect a large number. That is the
starting state, not a failure: the checker exits 0 unless `--fail-on` names codes.

## What the consuming repository must supply

| Supplied | Required? | Notes |
| --- | --- | --- |
| `repoRoot` | Yes, by every entry point | An absolute path. Nothing is discovered from `cwd` inside the library. |
| `config: SpecConfig` | Yes, by everything except `loadConfig` | Get one from `loadConfig(root)`, which falls back to `DEFAULTS` when no config file exists. |
| `spec-conformance.json` | No | A partial override merged over `DEFAULTS`, per kind. Absent means the defaults are the convention. |
| `pathRoots` | No, but empty is the default and it costs precision | The top-level directory names a document may name a path into. There is no shipped list: one repository's directory names would silently drop every path a consumer names. |
| `classifications.jsonl` | Yes, for `deriveDossiers` with a reading pass | Rows a person wrote after reading. Without them derive works from filenames only. |
| `decisions.jsonl` | Yes, for `applyDecisions` | Nothing else produces decisions. The pipeline refuses to invent them. |

Everything else — kinds, filename patterns, status vocabularies, required fields, domain
lists, review cadences, the reference field name and its aliases, the cluster policy —
has a default in `DEFAULTS` and is overridden per field.

## API

### Configuration

| Symbol | Signature |
| --- | --- |
| `CONFIG_FILE` | `"spec-conformance.json"` |
| `DEFAULTS` | `Omit<SpecConfig, "source">` |
| `loadConfig` | `(root: string, override?: string \| null) => SpecConfig` |
| `specDir` | `(config: SpecConfig) => string` |
| `workDir` | `(config: SpecConfig) => string` |

`specDir` is not `config.root`: a repository still holding a top-level pile is scanned at
`.`, and its destination is a spec root that does not exist yet. `workDir` is
`specDir(config) + "/_work"`, where the migration stages keep their working files.

### Scanning and parsing

| Symbol | Signature |
| --- | --- |
| `parseFrontmatter` | `(text: string) => Frontmatter \| null` |
| `findSpecRoots` | `(repoRoot: string, config: SpecConfig) => SpecRoot[]` |
| `kindOf` | `(filename: string, config: SpecConfig) => string \| null` |
| `proseOnly` | `(text: string) => string` |
| `idOf` | `(filename: string) => string` |
| `scan` | `(repoRoot: string, config: SpecConfig) => ScanResult` |

`scan` reads and judges nothing. `proseOnly` strips fenced blocks and code spans before a
link scan, because a document about configuration quotes configuration and one syntax for
an array-of-tables header is spelled exactly like a wikilink.

### Checking

| Symbol | Signature |
| --- | --- |
| `checkDocuments` | `(repoRoot: string, config: SpecConfig, options?: CheckOptions) => CheckResult` |
| `CHECK_CODES` | the eighteen codes `checkDocuments` can emit |

`CheckOptions` is `{ now?: number }`, milliseconds since the epoch, so a review-cadence
finding is decided by a date rather than by when the suite ran.

The codes: `PUBLISHED_ROOT`, `FILENAME_SHAPE`, `KIND_MISPLACED`, `ID_DUPLICATE`,
`NO_FRONTMATTER`, `KIND_DISAGREES`, `ID_DISAGREES`, `FIELD_MISSING`, `STATUS_UNDECIDED`,
`STATUS_UNKNOWN`, `DOMAIN_UNEXPECTED`, `DOMAIN_MISSING`, `DOMAIN_DISAGREES`,
`DOMAIN_UNKNOWN`, `IMPLEMENTS_MISSING`, `NEVER_REVIEWED`, `REVIEW_STALE`,
`REVIEW_OVERDUE`.

### The graph

| Symbol | Signature |
| --- | --- |
| `loadHistory` | `(repoRoot: string) => Commit[]` |
| `namedPaths` | `(text: string, pathRoots: readonly string[]) => string[]` |
| `nodeKey` | `(doc: Pick<Document, "specRoot" \| "id">) => string` |
| `buildGraph` | `(documents: readonly Document[], config: SpecConfig, options?: BuildGraphOptions) => GraphResult` |
| `graphView` | `(graph: GraphResult, config: SpecConfig, view: ViewName, options?: ViewOptions) => View` |
| `renderMermaid` | `(view: View) => string` |
| `renderDot` | `(view: View) => string` |
| `VIEW_NAMES` | `readonly ViewName[]` |
| `GRAPH_CODES` | the seven codes `buildGraph` can emit |

`BuildGraphOptions` is `{ history?: Commit[] }` and defaults to empty, so `buildGraph`
spawns nothing on its own. `loadHistory` is the one that shells out to git, and it is a
separate call precisely so a caller can decline it. `ViewName` is `"domains"`,
`"supersedes"`, `"orphans"`, `"neighborhood"`, `"kind"` or `"timeline"`; `ViewOptions` is
`{ id?: string | null; depth?: number; kind?: string }` and the neighborhood and timeline
views throw without an `id`.

Graph codes: `LINK_DANGLING`, `LINK_AMBIGUOUS`, `SUPERSEDE_DANGLING`,
`SUPERSEDE_ONE_SIDED`, `SUCCESSOR_MISSING`, `REF_DANGLING`, `SUPERSEDE_CYCLE`.

### The migration stages

| Symbol | Signature |
| --- | --- |
| `discoverCandidates` | `(repoRoot: string, options?: DiscoverOptions) => Candidate[]` |
| `DEFAULT_SKIP_DIRS` | `readonly string[]` |
| `DEFAULT_DOC_EXTENSIONS` | `readonly string[]` |
| `clusterDocuments` | `(documents: readonly Document[], policy: ClusterPolicy, options?: ClusterOptions) => Cluster[]` |
| `historyIndex` | `(repoRoot: string) => { created; updated; touches; renamedFrom }` |
| `citationIndex` | `(repoRoot: string) => Map<string, Touch[]>` |
| `pathCandidates` | `(text: string) => { token: string; line: number; context: string }[]` |
| `documentsFromClassification` | `(repoRoot: string, config: SpecConfig, rows: readonly ClassificationRow[]) => DerivableDocument[]` |
| `deriveDossiers` | `(repoRoot: string, config: SpecConfig, options?: DeriveOptions) => { dossiers: Dossier[]; summary: DeriveSummary }` |
| `applyDecisions` | `(input: ApplyInput) => ApplyResult` |
| `knownFields` | `(config: SpecConfig) => Set<string>` |

`DiscoverOptions` is `{ skipDirs?, extensions?, maxDepth? }`. `ClusterOptions` is
`{ minDocuments?, now? }`. `DeriveOptions` is `{ classifications?: ClassificationRow[]; into?: string }`.
`ApplyInput` is `{ repoRoot, config, dossiers, decisions }` and `ApplyResult` is
`{ written: WrittenDocument[]; rejected: RejectedDecision[] }` — `applyDecisions` returns
the text it would write; only the `--write` path of the binary puts it on disk.

`discoverCandidates`, `historyIndex`, `citationIndex` and `deriveDossiers` read git
history and degrade to empty when there is none.

### Types

```ts
type SpecConfig = {
  root: string;                          // ".spec" by default; "." means a top-level pile
  kinds: Record<string, KindSpec>;
  ignore: readonly string[];
  reserved: readonly string[];           // filenames never treated as documents
  publishSignals: readonly string[];     // a spec root under one of these is refused
  referenceField: string;                // "references"
  referenceAliases: readonly string[];   // read as well, so a rename loses no edge
  pathRoots: readonly string[];          // empty by default; yours to declare
  cluster: ClusterPolicy;
  source: string;                        // the file actually read, or "defaults"
};

type KindSpec = {
  dir: string;                           // destination directory, canonical
  sourceDirs?: readonly string[];        // where they currently sit, during a migration
  file: string;                          // filename regex; the id is its stem
  required: readonly string[];
  idField?: string;                      // "id" unless the project spells it otherwise
  status: readonly string[];             // closed vocabulary
  domain: false | readonly string[];     // false = this kind takes no domain level
  reviewEveryDays: number | null;        // null = never goes overdue
  allowDirectoryForm?: boolean;          // a directory of chapters is one document
};

type ClusterPolicy = {
  stopwords: readonly string[];
  minTokenLength: number;
  minDocuments: number;
  maxDocumentFrequency: number;          // a token in more than this share names no subject
};

type Document = {
  path: string; rel: string; filename: string;
  specRoot: string; package: string;
  declaredKind: string;                  // from placement
  detectedKind: string | null;           // from the filename; a disagreement is a finding
  id: string; isChapter: boolean; chapterOf: string | null;
  directoryDomain: string | null;
  frontmatter: Frontmatter | null;
  text: string; lines: number; mtime: number;
};

type Finding<Code extends string = string> = { code: Code; path: string; detail: string };
type CheckResult = { roots: SpecRoot[]; documents: Document[]; findings: Finding<CheckCode>[] };
type Cluster = {
  subject: string; documents: number;
  withStatus: number; withSupersede: number; recent: number;
  answerable: boolean;                   // can a reader tell which one is current?
  members: { id: string; rel: string; status: string | null; ageDays: number }[];
};
```

## Worked examples

### Which documents break the convention, and how does that become a gate?

`checkDocuments` always reports. Gating is a decision the caller writes down — one line
here, `--fail-on` on the binary.

```ts
import { checkDocuments, loadConfig } from "@modootoday/devtools-doc-lifecycle";

const BLOCKING = new Set(["ID_DUPLICATE", "STATUS_UNKNOWN", "IMPLEMENTS_MISSING"]);

export function gate(repoRoot: string): number {
  const config = loadConfig(repoRoot);
  const { findings } = checkDocuments(repoRoot, config, { now: Date.UTC(2026, 5, 1) });
  for (const finding of findings) {
    console.log(`${finding.code} ${finding.path}: ${finding.detail}`);
  }
  return findings.some((finding) => BLOCKING.has(finding.code)) ? 1 : 0;
}
```

Against a tree holding `.spec/decisions/0001-adopt-the-checker.md` (status `accepted`,
`reviewed` set) and `.spec/decisions/0002-second-thoughts.md` (status `pondering`, never
reviewed), the findings are `STATUS_UNKNOWN` and `NEVER_REVIEWED`, and the gate returns 1
on the first of those alone. Naming `NEVER_REVIEWED` too would block the migration it
exists to help.

### Several documents cover one subject: which is current?

The answer is usually "nobody can tell", and `answerable` is the field that says so.

```ts
import { DEFAULTS, clusterDocuments, loadConfig, scan } from "@modootoday/devtools-doc-lifecycle";

export function subjects(repoRoot: string) {
  const config = loadConfig(repoRoot);
  const { documents } = scan(repoRoot, config);
  // The default frequency ceiling drops a token appearing in more than 15% of
  // documents. On a small set that is every real subject, so raise it here and
  // lower it as the corpus grows.
  const policy = { ...DEFAULTS.cluster, minDocuments: 3, maxDocumentFrequency: 0.9 };
  return clusterDocuments(documents, policy, { minDocuments: 3 });
}
```

Four plans whose ids all contain `billing`, each carrying a status and none carrying a
supersede, come back as one cluster with `documents: 4`, `withStatus: 4`,
`withSupersede: 0` and `answerable: false`. That last field is the whole report: four
documents, all decided, and still no way to know which one is current.

### Why did a document lose its body, and why does an empty list read as a supersede?

Three parses, each of which has cost a document. `parseFrontmatter` is the one place they
are decided, and every one of them is a shape a caller must handle, not a bug to work
around.

```ts
import { parseFrontmatter } from "@modootoday/devtools-doc-lifecycle";

// 1. Two rules bracketing prose parse to an object with NO KEYS, not null.
//    Guard on the key count; treating this as a header strips the body.
const rules = parseFrontmatter("---\n\nJust prose, not a header.\n\n---\n\n# Title\n");
const isHeader = rules !== null && Object.keys(rules).length > 0; // false

// 2. An inline empty list is a list. Read as the string "[]", every document
//    writing this declared a supersede of a document literally named "[]".
const empty = parseFrontmatter("---\nsupersedes: []\n---\n"); // { supersedes: [] }

// 3. A blank value is an empty string, not an empty list. Read as a list it
//    arrives truthy, and every deliberately undecided field reports as a bad one.
const blank = parseFrontmatter("---\nstatus:\n---\n"); // { status: "" }

console.log(isHeader, empty?.supersedes, blank?.status);
```

### What does the graph see that a per-file check cannot?

`buildGraph` takes documents, not a path, and its history is an explicit option — pass
nothing and it spawns nothing.

```ts
import { buildGraph, loadConfig, namedPaths, renderMermaid, graphView, scan } from "@modootoday/devtools-doc-lifecycle";

export function report(repoRoot: string) {
  const config = loadConfig(repoRoot);
  const { documents } = scan(repoRoot, config);
  const graph = buildGraph(documents, config); // no history: no git, no commit edges
  const dangling = graph.findings.filter((finding) => finding.code === "LINK_DANGLING");
  const picture = renderMermaid(graphView(graph, config, "orphans"));
  return { dangling, picture };
}

// pathRoots is the allowlist for the paths a document names in backticks.
namedPaths("touches `src/check.ts` and `build/out.js`", ["src"]); // ["src/check.ts"]
namedPaths("touches `src/check.ts` and `build/out.js`", []);      // both
```

An empty `pathRoots` keeps every named path, which costs precision and nothing else — the
commit edges come from history either way. A shipped list would silently drop every path a
consumer names.

## Testing against it

### What to mock

**Nothing, and specifically not the filesystem.** `scan`, `checkDocuments`, `buildGraph`,
`clusterDocuments` and `parseFrontmatter` are the whole checking surface and none of them
needs a network, a clock it does not accept as a parameter, or git. Build a real directory
under the OS temp directory and point `repoRoot` at it: a stubbed scanner asserts the
stub's idea of what a document is, and what a document is turns out to be the thing
consumers get wrong.

Two things do spawn git — `loadHistory` and `deriveDossiers`, plus the history dating
inside `discoverCandidates` — and none of them should be executed from a unit test. Their
failure path already returns empty, so a test that runs them in a directory with no
repository is asserting the empty branch and calling it coverage. Test `buildGraph` with an
explicit `history` array instead: the join is pure once the commits are in hand.

### Fixtures

A temp directory is the honest fixture. Pass `now` so a review-cadence finding is decided
by a date rather than by the day the suite runs.

```ts
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, beforeAll, expect, it } from "vitest";
import { checkDocuments, loadConfig } from "@modootoday/devtools-doc-lifecycle";

let root: string;

beforeAll(() => {
  root = mkdtempSync(join(tmpdir(), "docs-"));
  mkdirSync(join(root, ".spec/decisions"), { recursive: true });
  writeFileSync(
    join(root, ".spec/decisions/0001-adopt-the-checker.md"),
    "---\nkind: decision\nid: 0001-adopt-the-checker\nstatus: accepted\nreviewed: 20260101\n---\n\n# Adopt\n",
  );
});

afterAll(() => rmSync(root, { recursive: true, force: true }));

it("reports nothing about a conforming decision", () => {
  const { findings } = checkDocuments(root, loadConfig(root), { now: Date.UTC(2026, 5, 1) });
  expect(findings).toEqual([]);
});
```

### Asserting the shape

Assert finding **codes**, never the `detail` string. The code is the contract and the
detail is prose written for a person; a suite matching on detail breaks on a reworded
message and passes on a renamed rule, which is exactly backwards.

```ts
const codes = findings.map((finding) => finding.code).sort();
expect(codes).toEqual(["NEVER_REVIEWED", "STATUS_UNKNOWN"]);
```

Assert `answerable` rather than the member list when the question is whether a cluster can
be resolved, and assert `graph.findings` codes rather than edge counts — an edge count
changes with every document added to the fixture.

## Invariants

### Reporting is the default; a gate is declared

`checkDocuments` returns findings and no verdict, and the binary exits 0 until `--fail-on`
names codes. A checker that fails on sight is unrunnable in the repository it exists to
help. The binary also refuses a code it cannot emit, because in a hook configuration a
rule that never fires reads exactly like one that does.

### The stages report evidence and refuse to decide

`discoverCandidates` classifies nothing, `clusterDocuments` groups without picking a
winner, and `deriveDossiers` writes an explicit list of what remains unknown and why. A
tool that fills those in from filenames produces a normalised pile that is confidently
wrong.

### Derive narrows before it widens, and says which it did

Commits inside a document's own editing window are the tightest honest scope. When that is
empty the search widens, and `widenedBecause` travels with the answer rather than being
dropped on the way out.

### Apply is the only stage whose output becomes a file

It refuses a decision recording no evidence, a status outside the kind's vocabulary, and a
supersede naming no successor. The source pile is never modified, with or without
`--write`.

### The three parses, again, because each cost a document

Two rules bracketing prose parse to an object with no keys, not null. An inline `[]` is an
empty list, not the string. A blank value is an empty string, not an empty list. Read any
one of them as the other and a document quietly changes meaning.

### An id is its filename stem, and unique within a spec root

Not across the repository: two packages may both hold a document called `overview`, and a
link resolves in its own root first. Frontmatter that disagrees with the filename is a
finding, never a tie-break.

## What it will not do

It does not decide what a document is: whether a file is a design document, a readme or a
note is a reading judgement, and no stage makes it. It does not fill in a status, a
relationship or a review date. It does not rewrite links in place — `applyDecisions` emits
new copies with their relations repointed, and leaves the originals alone. It does not
host, publish or render anything; the graph views are text handed to a renderer. It
installs no hook and chooses no severity. And a clean check is a statement about the
schema, not about whether the documents are true.
