---
name: shape
description: Turn a request or fault into one well-scoped piece before building. Typed alone, take the next piece that needs shaping. Shape records work and offers a ready piece to implement; it never builds.
---

# Shape

Shape itself never builds. Carrying on after a risk notice or an unchecked
fact finishes shaping; it never starts `/implement`, changes code, creates a
branch, commits or opens a pull request.

Run `triage` before acting. It chooses the route and says why. Follow the
named skill; the person does not sort work or answer what the agent can settle.

Read `masterplan.md` first, starting with the risk record. Refresh and read the
local plan with `sh .agents/tools/plan-refresh.sh`. `records/references/pieces.md`
holds the issue format, labels and plan rules.

## Make or refine a piece

Follow `records/references/pieces.md` for the issue. Preserve the person's
original words underneath a refinement. Include the masterplan change and read it back;
leave it proposed while shaping. On code projects, run
`quality.py reach --paths` for likely files and record `Reaches:` or
`Reaches: new files only`. Name the piece's risk areas on its `Risk areas:`
line, or `none`.

label it `ready` with `records/scripts/mark-ready.sh`. A clear,
sized request is ready at once; a note without `Done when` remains a request.
A new issue starts unassigned; `/implement` assigns it when building.

## Settle what the piece waits on

Use `clarify` to interview. For a decision best settled by seeing it, use an
existing artifact or throwaway prototype as that skill directs. Say which
step starts. If the person is absent, name what the piece needs; do not guess.

Use `research` for outside facts or existing work, including its notice for
unchecked facts; say which check and why.
Record what settled the question in `## Decided`, then mark ready.

Record acceptance only there with the date and the person's words, naming the
risk area or unchecked fact. Keep an accepted unchecked fact labelled unchecked.
For a named risk area, also follow
`fit-check/references/risk-acceptance.md`.

Typed alone, take an unreproduced repair, then the lowest-numbered question,
then the next note. If all are ready, offer `/implement`. Given a piece,
settle it or offer `/implement` if ready. If the person is leaving, settle
research and name remaining questions for them.

Name a ready piece and offer `/implement` or "not now". Acceptance of a risk or
unchecked fact is not a request for `/implement`, even after that offer.
A question during shaping never offers building as an answer.

## Done when

The route is recorded, the piece is ready or says what it waits for, and
building waits for `/implement`.
