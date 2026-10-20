# ReqToCode Traceability (MANDATORY)

Requirements in `docs/requirements/` (frontmatter `req-id: SWR-<n>`; see
`docs/requirements/README.md`) compile into `src/rotaris_core/reqtocode/swr.py`
(generated — never hand-edit). Implementations carry `@traces(SWR.SWR_<n>)`,
covering tests `@verifies(SWR.SWR_<n>)`
(`from rotaris_core.reqtocode import SWR, traces, verifies`). Enforced by the
verifier, `tests/unit/reqtocode/` meta-tests, CI, and the pre-commit hook.

- **Implementing a requirement**: add `@traces` on the implementation,
  `@verifies` on a real behavioral test, set `status: approved` in the same
  change, update the epic index table.
- **Writing tests that cover a requirement**: annotate with `@verifies`; the
  test must exercise real behavior of the traced code (transitional
  `# @req: SWR-<n>` comments still count; prefer `@verifies`).
- **Editing anything under `docs/requirements/`**: follow
  `docs/reference/reqtocode-playbook.md` — classify the change (text changed /
  deprecated / removed / new / flag flipped), run
  `rtk python -m rotaris_core.reqtocode check --fix` then `check`, and work the
  violation list; rework every `SWR_<n>` reference site.
- Commit requirement docs + `swr.py` + baseline + code + tests as one unit,
  requirement id in the message.
- Never silence a violation (no deleting annotations, weakening requirements,
  or adding entries to `docs/requirements/traceability-baseline.txt` —
  shrink-only). Never bypass the pre-commit hook. Never reuse or renumber an
  `SWR-<n>` id — deprecate instead of deleting.
