---
name: aval-docs
description: "Use when editing any Markdown file in aval (README, docs/, guides, CHANGELOG, ADRs) or any documentation image or GIF. The house style the docs tests enforce: generated excerpts and images, vhs demos, verified numbers, ADR rules, no personal paths."
---

## Activation contract

Load before changing a README, a page under `docs/`, an ADR, the CHANGELOG, or any image or GIF they show. Where it disagrees with a global docs skill, this one wins (`AGENTS.md`). Visible surfaces (TUI screens, CLI output) also go through `design-pipeline`.

## Hard rules

- **Never hand-edit a generated file.** Change the generator or its input and regenerate:

  | File | Generator |
  | --- | --- |
  | README images (`docs/assets/*.<hash>.svg`) | `go run ./tools/brand` (content-addressed names; `tests/readme_test.go`) |
  | `docs/assets/hub.gif` | `vhs docs/hub-demo.tape` |
  | `docs/assets/hub-es.gif` | `vhs docs/hub-demo-es.tape` (same walk with `AVAL_LANG=es`) |
  | `docs/assets/installer.gif` | `vhs docs/installer-demo.tape` |
  | `docs/assets/environment.png` | `vhs docs/environment.tape` |
  | `docs/architecture/model.md` | `go test ./tests/ -run TestArchitectureModel -update` |
  | TUI goldens (`internal/ui/testdata/*.golden`) | `go test ./internal/ui/ -update` |

- **Excerpts come from goldens.** The hub excerpt in `README.md`, `docs/guide.md` and `npm/cli/README.md` must be the menu line of `internal/ui/testdata/view_hub_unicode_80x24.golden`, and every view has a `- **Name**` line (`tests/hub_docs_test.go`). Update the golden first, then copy the excerpt, never the other way.
- **Verify every number, command and path you write** against the repo or a run. A number you did not read from a file or measure is not written. Say which numbers were measured.
- **No personal data in public assets.** No home paths (`/Users/...`, `/home/...`), emails or IPs; `tests/readme_test.go` checks the docs and runs gitleaks. Recordings run in a throwaway HOME: `docs/hub-demo.tape` links the repo as `~/.aval` inside that HOME (`ln -s $R $HOME/.aval && export AVAL_REPO=$HOME/.aval`), so the GIF shows `~/.aval` instead of whoever recorded it. Copy that trick into any new tape.
- **Links resolve.** Relative links must point at files that exist (`TestReadmeHasNoBrokenRelativeLinks`). No hosted badge or image services for repo images.
- **English** for docs, code and commits (the i18n plan keeps docs English).
- Conventional Commits (`docs(scope): ...`), no AI attribution.

## README structure

`tests/readme_test.go` pins the hero and mark images, the stack cards, badges, the roadmap and the leak checks. Keep the existing order of sections; add a section by extending the matching test first (RED), then the README. Developer detail goes to `docs/guide.md` or `CONTRIBUTING.md`, release detail to `docs/releasing.md`.

## ADRs

Rules in `docs/adr/README.md`, enforced by `tests/adr_test.go`:
- Sections: Context, Decision, Rejected alternatives, Consequences, an optional Amendments section.
- `Status:` line; numbers contiguous from 0001, never reused; `NNNN-kebab-case.md`; listed in the index.
- **Never rewrite an accepted ADR.** A changed decision is a dated `### YYYY-MM-DD` entry under `## Amendments`, or a new ADR that supersedes it (example: ADR 0002's amendment recording the real allowlist).
- Every claim cites evidence (a file, commit or issue) checked before writing.

## GIFs and screenshots with vhs

1. Change the `.tape`, never the GIF.
2. Run `vhs docs/<name>.tape` from the repo root. A tape that runs aval builds it from this checkout into a throwaway dir and sets `AVAL_NO_UPDATE_CHECK=1` (as `docs/hub-demo.tape` and `docs/installer-demo.tape` do).
3. Look at the output, then report its size in the commit or PR.
4. `tests/hub_docs_test.go` requires `docs/hub-demo.tape` and `docs/assets/hub.gif` to exist and the README to show the GIF.

## Before finishing

```bash
go test ./tests/ -run 'Readme|Docs|ADR|Changelog|AgentsMD|Budget'
```

Report what ran, what skipped (gitleaks or vhs missing is a skip, not a pass), and which numbers you measured.
