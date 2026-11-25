# PR Review Checklist

Use this before requesting review on a pull request.

## Tests

- [ ] Unit tests added or updated for the changed behavior.
- [ ] Integration tests pass locally.
- [ ] No skipped or `xfail` tests without a tracking issue.

## Security

- [ ] No secrets, tokens, or credentials in the diff.
- [ ] User input is validated at every external boundary.
- [ ] Dependencies bumped do not pull in known CVEs.

## Performance

- [ ] No N+1 queries introduced.
- [ ] Loops over large collections are bounded or paginated.
- [ ] Hot paths have a measurement, not a guess.

## Docs

- [ ] Public API changes documented.
- [ ] CHANGELOG or release notes updated when user-visible.
