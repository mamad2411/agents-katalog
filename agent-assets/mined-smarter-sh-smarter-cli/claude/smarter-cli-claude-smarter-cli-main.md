# CLAUDE.md

Guidance for Claude Code (and other coding agents) working in this repository.

smarter-cli is the Smarter platform's command-line interface: the `smarter`
binary, written in Go on cobra and viper. It is to the Smarter platform
([smarter-sh/smarter](https://github.com/smarter-sh/smarter), usually checked
out beside this repository as `../smarter`) what `kubectl` is to Kubernetes: a
verb-noun cli (`smarter get llmclients`, `smarter apply -f manifest.yaml`) that
sends one request per command to the platform's cli api, `/api/v1/cli/`. Its
configuration file, `~/.smarter/config.yaml`, is also read by the
[Python](https://github.com/smarter-sh/smarter-python),
[Node.js](https://github.com/smarter-sh/smarter-nodejs) and
[Go](https://github.com/smarter-sh/smarter-golang) SDKs.

Detailed know-how lives in the Agent Skills under `skills/` (symlinked to
`.claude/skills`), and the design decisions in `doc/adr/`. **Load
`smarter-cli-development` first for any change.** This file holds only what
applies to nearly every task.

## Hard rules

1. **Never run git write commands**, here or in `../smarter` or the SDKs.
   "Write a git commit" means print the command as text. See `smarter-git-commits`.
2. **Never trigger a release**: no `make release`, `make choco-push`,
   `gh workflow run`, or `scripts/bump_version.sh`. See `smarter-cli-release`.
3. **Never run the cli against a real platform** (`alpha`, `beta`, `next`,
   `prod`), and never with the user's `~/.smarter/`. Tests use the mock server;
   manual checks use the local platform, a throwaway `$HOME` and a throwaway
   key. Never `deploy`: it creates billable infrastructure. See `smarter-api-testing`.
4. **Run the tests yourself** after any change (`go test ./...`). Never ask the
   user to re-run them. Report failures honestly, including pre-existing ones.
5. **The pre-commit hooks are the lint standard** (gofmt, go vet, goimports,
   golangci-lint, go test). See `smarter-code-quality`.
6. **Coverage:** at least 90% per package, 95% where it takes moderate effort.
7. **This repository is public.** No api keys, tokens, account numbers,
   private hostnames or customer data in code, tests, docs or skills.
8. **The platform's `openapi.json` is the authority on routes and kinds.** The
   cli pins a copy in `testdata/contracts/` and its contract test checks every
   command against it (`doc/adr/022-pinned-openapi.md`). `~/.smarter/config.yaml`
   is a contract with the SDKs.

## Repository map

| Path                                               | Contents                                                                                                          |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `main.go`                                          | Entry point; blank-imports each verb package                                                                      |
| `cmd/`                                             | Root command, configuration, transport (`api.go`), output, the kind registry                                      |
| `cmd/<verb>/`                                      | One package per verb: `get`, `describe`, `delete`, `deploy`, `undeploy`, `logs`, `manifest`, `jsonschema`, `chat` |
| `contract_test.go`, `testdata/contracts/`          | The contract test, and the pinned copy of the platform's `openapi.json`                                           |
| `scripts/`, `debian/`, `chocolatey/`, `Dockerfile` | Version stamping and packaging                                                                                    |
| `.github/workflows/`                               | semantic-release on `main`; manual build-release workflow                                                         |
| `doc/adr/`                                         | Architecture decision records                                                                                     |
| `skills/`                                          | Agent Skills                                                                                                      |

The user guide lives in the platform's repository:
`../smarter/docs/source/smarter-framework/smarter-cli.rst`.

## Common commands

```bash
go test ./...                                           # all tests, the contract test included
make coverage                                           # per-package coverage, fails below 90%
make contracts                                          # refresh testdata/contracts/openapi.json from ../smarter
go build -o "$SCRATCHPAD/smarter" . && HOME=<temp dir> "$SCRATCHPAD/smarter" --help
source venv/bin/activate && git diff --name-only | xargs pre-commit run --files
```

## Definition of done

- The change follows an existing pattern and the ADRs in `doc/adr/`.
- The contract test passes against the pinned `openapi.json`.
- Tests cover it, you ran them, and coverage stays at 90% or more per package.
- The pre-commit hooks pass on the changed files.
- Help text, `README.md` and the docs page describe user-visible changes.
- Your summary says what changed, what you verified, what you skipped, and any
  platform drift you found.
