# CreditRadar — agent instructions

Personal credit intelligence and readiness system for the Brazilian credit
market. Tracked in Jira as **V1C-76**, which is the primary product
specification for this repository.

## What this system is

It consolidates credit information fragmented across bureaus (Serasa, Quod,
SPC, Equifax/BoaVista), Banco Central (SCR/Registrato and public datasets),
banks and creditors, into a historical, explainable view of one person's
credit position. It is not a debt tracker: it exists to support decisions
about settling debts, repairing credit and judging whether a financing offer
is worth taking.

## Non-negotiable safety invariant

CreditRadar **never** performs a financial action. It does not accept
settlement agreements, generate payments, authorize transactions, request
loans, apply for financing or open financial products. It observes,
normalizes and explains; anything that creates a financial obligation is
performed by the user, outside this system.

Any internal readiness or scoring indicator is a **CreditRadar heuristic**
and must be labelled as such. Never present one as a prediction of a bank's
or bureau's proprietary approval model.

## Architecture

```text
Browser → Next.js → FastAPI → services → domain → persistence
                                      └→ providers → BCB, bureaus, SCR
```

```text
credit-radar/
├── backend/    FastAPI, Python 3.13, uv, SQLAlchemy, Alembic
├── frontend/   Next.js, React, TypeScript, pnpm, shadcn/ui, Recharts
├── docs/
├── flake.nix   Nix devShell: interpreters and system tooling
└── docker-compose.yml
```

The frontend never talks to a provider, a browser-automation worker or the
database. All financial data flows through the backend.

Dependency boundary, kept explicit:

| Tool   | Owns                                   |
| ------ | -------------------------------------- |
| Nix    | development environment, system deps   |
| uv     | Python dependencies                    |
| pnpm   | frontend dependencies                  |
| Docker | running services                       |

Do not introduce Poetry, pipenv, npm, Yarn or Bun.

## Data modelling rules

- **History is the product.** Model as `Entity + Observation + Source +
  ObservedAt`. Never overwrite the previous state.
- **Provenance is mandatory.** Every collected value records its source,
  upstream reference, collector version and collection time. Every
  collection attempt is recorded, including failures — a gap is only
  explainable if the attempt was logged, and runs cannot be backfilled.
- **`reference_date` ≠ `collected_at`.** A reference date may be in the
  future: the Copom publishes the Selic target ahead of the dates it applies
  to.
- **`Decimal`, never `float`,** for any monetary or rate value. The API
  serializes them as JSON strings, because a JSON number is an IEEE-754
  double in the browser.
- **Preserve the source's scale.** "14.00" is not "14"; the trailing zero
  states the precision published. The database column is unconstrained
  `numeric` for this reason.
- **Keep bureaus separate.** Serasa, Quod, SPC and Equifax use different
  methodologies. Never merge them into a synthetic universal score.
- **The subject is implicit.** This is a single-user system, so there is
  exactly one person the data is about and the CPF does not need to be a
  column anywhere. Debts, scores and exposure belong to "the user" by
  construction. Introduce a subject identifier only if the system ever stops
  being single-user, and even then store a reference rather than the number.
- Preserve these distinctions: `Debt ≠ NegativeRecord ≠ SettlementOffer`;
  `CreditScore ≠ Creditworthiness ≠ Affordability`; `CreditAvailability ≠
  CreditAttractiveness`; "Can I get credit?" ≠ "Should I take it?".

## Provider rules

Integrate in this order of preference: official API → structured export →
downloadable report → authenticated browser automation → DOM scraping.
Check for a stable structured integration before writing automation.

**Verify a source's identity before trusting it.** Series codes and endpoint
meanings are checked against the provider's own catalog, never inferred from
a plausible-looking value. This caught a mortgage series that was labelled
market-rate but was in fact the regulated-rate series — a 3+ percentage
point error in exactly the comparison the product exists to make.

**Never bypass CAPTCHA, MFA, gov.br authentication or device confirmation**,
and do not build fingerprint, header or user-agent evasion to get past one.
This is settled by measurement, not preference: gov.br gates every Registrato
sign-in path behind invisible hCaptcha, so the login is not automated at all
and the user exports the report themselves. See
`docs/providers/registrato.md`.

## Security

- **The application stores no credentials.** Authenticated sources are
  reached by the user exporting a report in their own browser; CreditRadar
  parses the file. There is no password, CPF, session or browser profile
  anywhere in it. Do not reintroduce one without a source that both needs it
  and permits automation.
- **Never ask the user for a CPF, full name, date of birth, password or any
  other identifier, and never accept one pasted into a conversation.** An
  agent conversation is a transcript: a value pasted there has left the
  user's control, whatever happens next. If a task seems to need a real
  identifier, the task is wrong: use a synthetic fixture.
- Never commit credentials, CPF, financial records, session cookies, tokens,
  browser profiles or real credit reports.
- Never log secrets or personal data; redact sensitive fields.
- Nothing sensitive in `NEXT_PUBLIC_*` — those are inlined into the browser
  bundle. Provider credentials belong to the backend only.
- Services bind to loopback by default.
- Tests use synthetic or public fixtures. Never real credentials or real
  personal financial data.

## UI rules

- Never invent a value. Distinguish *loading*, *collected nothing* and
  *provider not implemented* as separate visible states. A section with no
  backend module shows no digits at all — not a placeholder, not a skeleton.
- Show provenance: source, series, reference date, collection time.
- Financial state uses the semantic tokens, never a raw colour, and colour
  never carries a meaning on its own.
- Nothing about a credit position reaches a title, description, Open Graph
  tag or manifest. Those are quoted verbatim wherever a link is shared.
- Conventions in full: [docs/interface.md](docs/interface.md).
- Show staleness and failed collections. Never present a stale or failed
  source as current.
- **The interface is pt-BR.** This is the one exception to the en-US rule
  below, and it is the exception that rule names: an explicit product
  requirement for user-facing localization. Everything a user reads is
  Portuguese, including accessible labels (`aria-label`, `sr-only`), page
  titles and metadata. Numbers, dates and rate notation follow Brazilian
  convention (`14,00% a.a.`, `16/09/2026`).
- **Nothing else is pt-BR.** Code, identifiers, comments, documentation,
  commit messages and Jira technical comments stay en-US.
- Domain `name` and `description` from the API are NOT rendered: they are
  en-US domain documentation. Presentation labels live in
  `frontend/src/lib/labels.ts`, keyed by the stable internal code and typed
  as exhaustive Records, so a new indicator fails to compile until it has a
  label instead of leaking a raw enum value onto the screen.

## Testing rules

- **The default suite never touches the network.** No test may depend on an
  external provider being up. A suite that fails for reasons outside the
  repository stops being a signal. Real-provider checks go behind the `live`
  marker, which is excluded by default.
- **Integration tests use real PostgreSQL, never SQLite.** What they cover is
  PostgreSQL behaviour: unconstrained `numeric` scale, `ON CONFLICT`
  deduplication, `DISTINCT ON` revision selection.
- **Never real personal data.** Fixtures are captured from public endpoints
  or generated synthetically, and E2E values are deliberately unlike the real
  figures so a screenshot cannot be mistaken for a real reading.
- **A fixture that opens its own session must clean up after itself.**
  Leaning on another fixture's cleanup made the suite order-dependent once.
- Use the cheapest level that reliably catches the behaviour. Do not test
  through the browser what a unit test can prove.
- Financial calculations get unit tests over `Decimal` with explicit rounding
  assertions, never floating point.

## Working rules

- **Everything in en-US**: code, comments, docs, commit messages, technical
  names, Jira technical comments. The sole exception is user-facing interface
  copy, which is pt-BR (see the UI rules above).
- **Commit incrementally**, one coherent unit per commit. Never a single
  large commit at the end.
- **Never** add `Co-authored-by:` or attribute commits to Claude, Anthropic,
  an AI or any assistant.
- Before each commit: review the diff, check no secret was introduced, run
  the relevant checks.
- Keep the repository building and running as you advance.
- Sync meaningful decisions, discovered provider limitations, blockers and
  milestones to Jira V1C-76. Do not post trivial updates.

## Deployment

Served at `https://credit.v1cferr.dev`, LAN and WireGuard only; the reverse
proxy answers 403 from the public internet. That reach is the security
control, not a default: this app has no login and holds a CPF. Widening it
requires application authentication first, never just a config change.

Owned by the NixOS config in `../dotfiles`: the `credit` entry in
`hosts/nixos-kingston/services.nix`, `system/services/credit-radar.nix`, and
`docs/notes/services/credit-radar.md`. That repo has stricter prose rules
than this one: no em dashes, no emoji, first person.

The proxy routes `/api/*` and `/health` to the backend and the rest to the
frontend, so the backend keeps its whole surface under `/api/v1`. Browser
calls are same-origin; the app uses no `NEXT_PUBLIC_*` variable.

## Commands

```bash
nix develop                  # dev shell: python, uv, node, pnpm, psql

docker compose up -d         # full stack
docker compose up -d postgres

# The quality gate. A change is not finished while any of these fails.
cd backend  && uv run ruff format --check . && uv run ruff check . \
            && uv run mypy && uv run pytest
cd frontend && pnpm lint && pnpm typecheck && pnpm test:unit && pnpm build
cd frontend && pnpm test:e2e          # full-stack, manages its own database

cd backend  && uv run pytest -m live  # opt-in: contacts the real BCB API
```

Default host ports are offset (postgres 5434, backend 8007, frontend 3007)
because the development machine runs other projects on the conventional
ones. All are environment-overridable.
