# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## What this project is

`bio_ai_experiment` is an experiment in using AI agents to re-implement popular
bioinformatics command-line tools in Go — making them faster, better tested, and
better documented than their originals (typically C, C++, or Perl). The original
tools are vendored as git submodules under `reference_code/` for reference.

### Project focus (current)

**The project is no longer taking on new tools.** The full focus now is to
**finish the tools already ported or started** — driving each to **100%**
upstream feature parity. There are **no "non-goals" and nothing is out of
scope**: every upstream feature, flag, input format (BED/GFF/VCF/SAM/BAM/CRAM),
and edge case must be matched. The only scope is: 100% feature parity, bug
fixes (fix-on-port even where upstream is buggy), better documentation,
unit/parity tests for everything, and drop-in POSIX CLIs. Do **not** add a new
`tools/<tool>` directory or start porting a tool that isn't already present.
"New work" means closing the remaining parity gaps in the existing tools (see
`docs/PARITY_ROADMAP.md`), not broadening the tool set.

## Repository layout

```
.
├── go.mod                    # single Go module: github.com/yassineS/bio_ai_experiment
├── Makefile                  # builds binaries into bin/ (see Common commands)
├── bin/                      # gitignored built binaries (bin/ours, bin/upstream) — `make`
├── pkg/                      # shared libraries used by all tools (htsgo/* + cliflag)
│   ├── htsgo/                # parsers/writers: fasta, fastq, vcf, bed, sam, bcf, cram, bgzf, iohelper
│   └── cliflag/              # helper for flags that accept both short (-i) and long (--input) forms
├── tools/                    # Go re-implementations, one subdir per tool
│   └── <tool>/
│       ├── cmd/<tool>/main.go        # CLI entry point
│       └── pkg/<tool>/*.go           # tool logic + *_test.go
├── pipeline/                 # Go validation harness: realbench/realparity/giab (real-data
│   │                         #   bench + parity) + crafted-input difffuzz/edgecases/
│   │                         #   roundtrip/conformance + fixtures/matrix/runner/internal/stats
│   └── cmd/<x>/main.go       # harness entry points (realbench, realparity, conformance, …)
├── reference_code/           # git submodules: upstream sources of the original tools
├── test/                     # validation + paper area (not Go *_test.go; that lives next to code)
│   ├── nextflow/             # Seqera/Nextflow real-data pipeline + Dockerfile (the canonical container)
│   ├── manuscript/           # the paper: strategy, claims, results, figures, bug corpus
│   ├── figures/              # figure-generation Python (plot_perf_parity.py, splice_membench.py)
│   └── scripts/              # manuscript-metrics tooling (recompute-metrics.sh)
├── mcp-servers/              # DESCOPED: MCP servers not being built (see its README)
├── docs/                     # project docs (see below)
└── .github/agents/           # role descriptions for the AI agents that build this repo
```

Implemented tools so far: the QC/format set (`seqtk`, `prinseq`, `sickle`,
`skewer`, `fastp`, `vcftools`, `mosdepth`), the htslib core (`bgzip`,
`tabix`, `htsfile`, `samtools` with 24 subcommands, `bcftools` with 24
subcommands), and ~37 `bed*` tools covering the bedtools surface
(`bedmerge`, `bedintersect`, `bedmap`, …). Each has its own `README.md`
under `tools/<tool>/`. For the current per-tool completion table see
`PROJECT_STATUS.md`; for the authoritative gap list see
`docs/PARITY_ROADMAP.md`.

### Important: it is ONE Go module

Despite what some older docs (`tools/README.md`, `CONTRIBUTING.md`,
`.github/agents/*`) say, there is **no per-tool `go.mod`**. Everything lives in
the single root module. Third-party dependencies are kept to an absolute
minimum — prefer the standard library and the shared `pkg/` libraries.
Adding a new external dependency needs its own conversation; the currently
sanctioned set is enumerated below.

#### Sanctioned third-party deps

Adding a new external dependency outside these zones requires explicit
owner approval.

1. **`gonum.org/v1/gonum`** (BSD-3) — used by the vcftools `--pca`
   family for symmetric eigendecomposition of the N×N Genomic
   Relatedness Matrix. Upstream calls LAPACK `dgeev_`; gonum's pure-Go
   `mat.SymEigen` is the equivalent without dragging in cgo / libblas.
   Confined to `tools/vcftools/pkg/vcftools/pca.go` today. **Scope:**
   reuse is allowed for other genuinely linalg-heavy paths
   (eigendecomp, SVD, matrix solve, etc.). Reuse for non-linalg
   utilities, or pulling in another top-level dep, still needs its
   own conversation — pre-approval is NOT extended to "any future
   stats-heavy tool" (e.g. Fst is a couple of means + a variance and
   should stay stdlib-only; ADMIXTURE-style models would deserve
   their own review). An in-tree symmetric eigensolver (~150-250 LOC
   Jacobi or Householder+QL) remains a viable alternative if the
   owner ever wants to drop the dep entirely; the current decision
   prefers gonum for the well-audited numerical-stability
   guarantees.
2. **CRAM codec layer.** CRAM uses several custom compression codecs
   that have no Go-stdlib equivalent. The owner OK'd third-party deps
   here, but in practice the rANS coders (4x8, 4x16) are ported
   **in-tree as pure Go** — the port is ~700 LOC per codec, well
   within the codebase's in-tree appetite, and `pkg/htsgo/cram/codec`
   proves it byte-exact against the htscodecs corpus. The **only**
   sanctioned third-party dep for CRAM is **`ulikunitz/xz`** for LZMA
   block decode (genuinely hard to port; a rare optional codec). It
   must be confined to `pkg/htsgo/cram/codec/` so the rest of the
   repo can still claim "stdlib + gonum only" for non-CRAM
   workflows. See `docs/CRAM_ROADMAP.md` §1.2 (the actionable
   decision) and `docs/CRAM_DESIGN.md` (the rationale).
3. **`github.com/klauspost/compress`** (BSD-3) — the DEFLATE backend for
   BGZF (and gzip-framed) I/O, both **compress and decompress**. It is a
   pure-Go, no-cgo flate implementation that is faster than the stdlib
   `compress/flate` while emitting/consuming standard DEFLATE bit
   streams. **Scope:** the BGZF/gzip deflate writer *and* reader,
   confined to `pkg/htsgo/bgzf/` (imported there as `kflate`). The
   reader was originally left on stdlib `compress/flate` (the dep is not
   strictly *needed* for reads — klauspost output is ordinary DEFLATE),
   but BGZF decompression is on the hot path of every BAM/CRAM/.vcf.gz
   reader, and the owner's "≤1× vs upstream across the board" performance
   mandate made the faster inflater worth adopting there too: the decoded
   bytes are identical (validated against our own reader, the stdlib
   `compress/gzip` reader, and live upstream `bgzip`), only the speed
   changes. At the default level 6 the writer is ~2x faster at an
   essentially identical ratio, and the reader is measurably faster on
   every BGZF-consuming tool. **Also sanctioned: CRAM gzip blocks.** The
   CRAM writer compresses every series block with gzip and previously
   used the stdlib `compress/gzip` — DEFLATE was ~37% of encode time. It
   now uses klauspost's gzip backend (imported as `kgzip` in
   `pkg/htsgo/cram/writer.go`, with a pooled writer), emitting a standard
   gzip stream the stdlib reader and upstream htslib both decode. Note
   klauspost's level scale differs from the stdlib's: **level 7**
   reproduces stdlib level-6 ratio (the writer's `cramGzipLevel`), so
   CRAM size stays on par with upstream while encoding faster.
   **Also sanctioned: plain-gzip tool OUTPUT.** `iohelper.OpenWriterFast`
   (in `pkg/htsgo/iohelper/`) is a klauspost-backed sibling of
   `OpenWriter` for `.gz` *output*: it emits a standard RFC 1952 gzip
   stream (byte-decodable by compress/gzip and upstream tools) but
   deflates much faster than the stdlib encoder. It exists because for
   FASTQ tools like fastp ~80% of wall time was single-threaded output
   gzip; fastp now routes all its `.gz` output through it (honouring the
   upstream `-z/--compression` level, default 4), cutting the chr20 PE
   run ~2.6× and SE ~3.6× with byte-identical decompressed output.
   `OpenWriterFast` is a *separate* entry point on purpose — the global
   `OpenWriter` shared by every tool stays on the stdlib encoder, so only
   opt-in callers change their compressed bytes. Reuse beyond the BGZF,
   CRAM gzip, and `OpenWriterFast` output paths (e.g. its zstd/s2/snappy
   packages, or as a general compression utility) still needs its own
   conversation.

Preference order:

1. Standard library.
2. In-tree implementation (the bgzip / tabix / sam / bcf packages all
   went this route).
3. Sanctioned third-party dep (gonum for linalg, klauspost/compress
   for the BGZF deflate backend, CRAM codec libraries).

## Common commands (run from repo root)

```bash
go build ./...                                   # build everything
go test ./...                                    # run all tests
go test -race -cover ./...                        # race detector + coverage (matches CI)
go test ./tools/seqtk/...                          # test one tool
go test -bench=. -benchmem ./tools/<tool>/...      # benchmarks
gofmt -l .                                        # list unformatted files (CI fails if any)
gofmt -w .                                        # format
go vet ./...                                      # vet
go build ./tools/seqtk/cmd/seqtk                  # build a single tool binary
go run ./tools/seqtk/cmd/seqtk comp file.fasta    # run a tool without installing
make ours                                         # build all our binaries into bin/ours/
make upstream                                     # best-effort build upstream oracles into bin/upstream/
make build                                        # ours + upstream ; make clean removes bin/
```

The canonical full upstream container (all oracles incl. fastp/vcftools/prinseq)
is `test/nextflow/Dockerfile`, built from the repo root:
`docker build -f test/nextflow/Dockerfile .`.

CI (`.github/workflows/ci.yml`) runs on every push to `main` and every PR
targeting `main`: `gofmt -l`, `go vet ./...`, `go test -race -coverprofile=...
./...`, `go build ./...`, markdown lint (`**/*.md`), and a live
**upstream-parity** job that builds htslib/bcftools/samtools from the submodules
and runs the `*Upstream*` parity tests against them (the independent,
non-self-reported re-execution of the byte-exact gate). Keep markdown
well-formed. The Go toolchain is read from `go.mod` via `go-version-file`, so it
matches the declared version (currently 1.24.9) — there is no separate 1.21 pin.

## Conventions

### Code

- Idiomatic Go, `gofmt`-clean, passes `go vet`. Small focused functions, meaningful names.
- Document all exported identifiers with complete-sentence doc comments.
- Tool logic goes in `tools/<tool>/pkg/<tool>/`; `cmd/<tool>/main.go` only does
  argument parsing, wiring, and exit codes.
- Reuse `pkg/htsgo/*` for file format parsing instead of re-implementing it.
  Use `pkg/htsgo/iohelper` for transparent gzip and stdin/stdout (`-`) handling.
  The htsgo migration completed across PRs A–I; the legacy
  `pkg/bioformats/` path no longer exists.

### CLI design

- Tools should accept both POSIX short flags (`-i`, `-o`, `-q`, `-l`, ...) and
  GNU long flags (`--input`, `--output`, `--min-length`, ...). Use the
  `pkg/cliflag` helpers (`cliflag.StringVar`, `cliflag.IntVar`, `cliflag.Float64Var`,
  `cliflag.BoolVar`) which register both names on a `flag.FlagSet`.
- `-` means stdin/stdout. Always provide `-h/--help` and `-v/--version`.
- Where practical, keep compatibility with the original tool's flags.
- Full rules: `docs/CLI_CONVENTIONS.md`.

### Tests

- Every new behavior gets a test. Prefer table-driven tests. Aim for >80% coverage.
- Tests live next to the code as `*_test.go` in `tools/<tool>/pkg/<tool>/`.
- Add benchmarks for performance-sensitive paths; this project cares about being
  faster than the originals (see `docs/METRICS.md` for the scope/speed summary).
  The performance + real-data parity harness is `pipeline/realbench` (run via the
  `test/nextflow/` Seqera pipeline on real GIAB HG002/GRCh38 data); `pipeline/cmd/realparity`
  is the real-data samtools/bcftools parity+perf runner. The crafted-input
  correctness suites (`pipeline/difffuzz`, `pipeline/edgecases`,
  `pipeline/roundtrip`, `pipeline/conformance`) live alongside them.

### Commits & PRs

- Imperative, concise commit subjects (e.g. "Add reverse complement to seqtk seq").
- Branch off `main`. PRs target `main`; there's a PR template in `.github/`.
- Run `go test ./...`, `go vet ./...`, and `gofmt -w .` before committing.

## Submodules

`reference_code/` contains the upstream tool sources as submodules. They're
read-only references for behavior/parity checking — never modify them. Init with
`git submodule update --init reference_code/<tool>` only if you actually need a
specific one; you usually don't.

## Where to look

- `README.md` — project overview and per-tool quick start.
- `docs/GOLANG_GUIDE.md` — Go patterns/best practices used here.
- `docs/CLI_CONVENTIONS.md` — the canonical CLI flag spec.
- `pkg/htsgo/README.md` — format library docs (post-migration home;
  superseded `pkg/bioformats/README.md`).
- `docs/README.md` — the **docs map**: which document owns which kind of
  status/design info (start here when unsure where something lives).
- `PROJECT_STATUS.md` — top-level completion table (the summary view).
- `docs/PARITY_ROADMAP.md` — authoritative per-tool parity gap list.
- `tools/PORTING_STATUS.md` — per-subcommand feature inventory + test notes.
- `tools/<tool>/README.md` — per-tool usage and parity notes.
- `.github/agents/*.md` — the agent roles (tool-analysis, golang-recoding, testing,
  documentation) and how the work is divided. The mcp-server role is deprecated:
  MCP servers are descoped in favor of drop-in POSIX CLIs.

## Caveats / known stale docs

The major status docs were consolidated (see `docs/README.md`, the docs map):
`PROJECT_STATUS.md` (summary table) and `docs/PARITY_ROADMAP.md` (gap detail)
are the source of truth; `tools/README.md`, `tools/PORTING_STATUS.md`, and the
`.github/agents/*` structure diagrams were corrected to the single-module
reality and now link to those two rather than restating status. The former
`docs/archive/` point-in-time summaries (the old `tools/IMPLEMENTATION_SUMMARY.md`
lineage) have been removed — their state is captured by commit history and the
canonical status files above.

When in doubt, trust the actual code and the two source-of-truth status docs
over any older Markdown, and feel free to fix stale docs as part of related work.
