# gamechanger

## gstack

Use the `/browse` skill from gstack for all web browsing. Never use `mcp__claude-in-chrome__*` tools.

Install: `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

Available skills: `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/design-consultation`, `/review`, `/ship`, `/browse`, `/qa`, `/qa-only`, `/design-review`, `/setup-browser-cookies`, `/retro`, `/debug`, `/document-release`

## Testing

Run tests (dev, fast):     `bundle exec rspec`
Run tests (with coverage): `COVERAGE=1 bundle exec rspec`
Test directory: `spec/`

- 100% test coverage is the goal — tests make vibe coding safe
- When writing new functions, write a corresponding test
- When fixing a bug, write a regression test (see ISSUE-001, ISSUE-002 in spec files for pattern)
- When adding error handling, write a test that triggers the error
- When adding a conditional (if/else), write tests for BOTH paths
- Never commit code that makes existing tests fail

Test conventions: RSpec with `instance_double`, `WebMock` for HTTP stubs, `Dir.mktmpdir` for temp config dirs, seeded in-memory SQLite (`':memory:'`) for storage fixtures.

## Working with the GameChanger API

This repo is **public**. Real GameChanger identifiers (team UUIDs, opponent UUIDs, player names, jersey numbers) are not credentials in the auth sense, but they identify real youth-baseball teams and minors — treat them as PII and keep them out of committed code.

- **Never hardcode team UUIDs, opponent UUIDs, or other live API identifiers** as Go constants, Ruby constants, or test fixtures. Read them from env vars (`os.Getenv("GC_PROBE_TEAM_UUID")`), config files outside the repo, or `~/.gamechanger/cache.db`.
- **Probe / discovery binaries** that hit live `api.team-manager.gc.com` endpoints belong under `cmd/` only if they read identifiers from env vars; treat them as throwaway and delete them in the same PR that lands the durable artifacts (HAR captures, endpoint-notes doc).
- **HAR fixtures** stay in `testdata/har/` which is gitignored. If they're ever promoted to a shared corpus, anonymize player/opponent names and dates via `internal/parity/anonymize/anonymize.go` (or a HAR-shaped analog) first — see the plan-level note in `docs/plans/2026-05-15-001-feat-scouting-tool-phase-1-plan.md` under "Deferred to Follow-Up Work".
- **Logs and error output** must not echo raw 403 / 401 response bodies if those bodies include decoded JWT claims, user UUIDs, or scoped role information. Sanitize before display.

If you discover that real identifiers slipped into a commit on a public branch, see the existing E1 disposition in the scout Phase 1a plan's "Open Questions" section before deciding whether to rewrite history.
