---
name: add-kind
description: Adds a diagram kind to drawspec, or a style, field or text form to an existing one, from the originals to the merged pull request. Use when the user asks for a new kind of drawing in this repository — "add a kind", "support neural network diagrams", "a new style for tree" — or a change to src/drawspec/kinds/ or the field tables in src/drawspec/schema/ Owns scripts audit_kind.py. Do NOT use for writing a drawspec document of an existing kind; the drawspec skill does that.
---

# add-kind

Builds a drawspec kind end to end: proposal, schema, renderer, text form,
references, tests, generated files and documents, in one pull request.

CANARY: add-kind-loaded-2026-10-26-fb4653f5-017474c33acb767a

## When to load

Load it for a new kind, a new `style` of a kind, a new field or role, or a text
form for a kind that lacks one. A request for one drawing of a kind that
exists is the `drawspec` skill's; a renderer bug in an existing kind needs only
the steps it touches, so read the gotchas and skip the rest.

## Standing rules

- Ship everything in one pull request: the repository's `CLAUDE.md` makes a
  docs or gallery follow-up a defect, so a missing table row is a review finding.
- Find two or more real figures before designing, and say in the proposal
  which were opened and which were seen only as search results; the proposal is
  the evidence the owner reviews.
- Refuse what the kind cannot draw well, at its JSON pointer, with the reason
  and the alternative (often another kind). Never draw a degraded picture.
- Set each budget limit from the references, above the largest of them, with
  the evidence in a comment beside the constant.

## Procedure

### 1. Task and proposal

Create the task with the `queue-add` skill and claim it as the repository's
session protocol says. Then write `docs/proposals/<kind>.md`: the originals,
what the kind draws, what it refuses and why, and the questions for the owner.
Search for the originals in one batch:

```text
"<notation> diagram" textbook figure · "<tool> <notation>" documentation · "<paper>" figure 1
```

### 2. Schema, renderer, registration

Wire the kind into each point in
[registration-points.md](references/registration-points.md) (load it before
editing `schema/`). Write the renderer in `src/drawspec/kinds/<kind>.py` on
the model of the newest kind of a similar shape, and a text form when the kind
reads well as a table or a character grid.

### 3. References and tests

Write three or more `docs/reference/<kind>-*.json`, one per original, and
`tests/test_kinds_<kind>.py`. Render each reference and look at it; the
collision tool cannot see a figure that is correct but ugly.

```bash
uv run drawspec render docs/reference/<kind>-<name>.json -o /tmp/<name>.svg
uv run python tools/collisions.py /tmp/<name>.svg     # 0 collision(s)
uv run python tools/arrows.py /tmp/<name>.svg        # 0 short arrow(s)
uv run pytest tests/test_kinds_<kind>.py -q
```

### 4. Generated files and documents

Regenerate, then update the prose documents listed in the reference, then run
the audit until it reports nothing missing.

```bash
DRAWSPEC_UPDATE_GOLDEN=1 uv run pytest tests/test_text_output.py -k <kind> -q
make schema && make docs && make gallery
python3 "${CLAUDE_SKILL_DIR}/scripts/audit_kind.py" <kind>   # exit 0
```

### 5. Checks and pull request

Run the fast checks, then the full suite once (about twelve minutes), then open
the pull request with `Closes #<issue>` and ask CodeRabbit to review.

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy .
uv run pytest -q
```

## References

- [Registration points](references/registration-points.md) — load before
  editing `schema/`, or when `audit_kind.py` names a missing piece.

## Gotchas

- **A caption longer than 80 characters fails the text tests.** The text form
  wraps it, and the verbatim-label test looks for each label on one line.
- **`ruff` refuses a literal `×` in Python strings (RUF001).** Write `x` in
  schema descriptions, or `\N{MULTIPLICATION SIGN}` where the mark is drawn.
- **A nested object that refers back to its parent recurses.** Validation
  follows the reference into itself until Python's stack runs out; give the
  child its own object with only the fields it draws.
- **Editing `schema/` while the full suite runs fails the schema test.** The
  committed schema is compared with the field tables read mid-run; rerun
  `tests/test_schema.py` after `make schema` before believing the failure.
- **A fresh virtual environment has no `pytest`.** `uv sync --all-extras`
  installs the dev extras the suite needs.
- **An arrow that turns just before a box reads as a blot.** Its head then sits on
  the corner with no line behind it; give every turning arrow
  `routing.arrow_run(theme, role)` of straight run into the box.
- **CodeRabbit allows about one review an hour.** A rate-limited request says
  when the next is free; ask again then, or review the diff yourself as
  `CLAUDE.md` says.
