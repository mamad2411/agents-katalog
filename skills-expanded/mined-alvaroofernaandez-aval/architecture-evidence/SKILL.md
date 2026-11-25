---
name: architecture-evidence
description: >
  Use when adding a module, package, interface or seam, moving code across
  layers, adding a dependency between modules, or before and after a refactor.
  Evidence before abstractions, AS-IS vs TO-BE, boundaries enforced by a test
  with a shrinking ratchet, ADRs that are amended not rewritten, what a PR shows.
---

## Activation contract

Load before a structural change: a new module or package, a new interface or seam, a new dependency between modules, or a refactor that moves code. Not for runtime behaviour or performance tuning. Works in any language; examples are Go and JS/TS.

## Rules

- **Evidence before abstractions.** A new package, interface or seam is a visible cost. Name its need before adding it: a second implementation that exists or is planned, a test seam a test actually uses, or a security or ownership boundary. "Cleaner" or "more flexible" is not a need. No need, no abstraction.
- **AS-IS and TO-BE stay separate.** AS-IS is what the dependency graph shows at this commit, produced by a tool. TO-BE is your proposal, labelled as one. Never draw a proposed module or edge into the AS-IS picture.
- **Existing findings are the baseline.** Only new violations block. Do not fail a feature on debt that predates it; record it and ratchet it down.
- **Turn boundaries into mechanisms.** A rule only a reviewer remembers will be broken. Encode it as a test that fails when it breaks (below).
- **Decisions are ADRs, never rewritten.** To change a decision, add a dated amendment or a new ADR that supersedes it. The accepted text stays, so the history of why stays.
- **Change order: ADR, then rules, then code.** Amend the decision, edit the rule table, then write the import.

## The boundary test

Three parts, all in the normal test suite so CI runs them:

1. **An allowlist.** For each module, the modules it may depend on. A module that no rule matches is itself a violation, so a new module forces a decision.
2. **A ratchet.** A list of known violating edges and a cap on its length. The cap may shrink but never grow. A new violation fails; an exception that no longer matches also fails, so debt is removed when paid. Raising the cap is never part of a feature change.
3. **A planted-violation self-test.** Feed the checker a fake graph with one forbidden edge and assert it reports exactly that edge. This proves the guard catches what it claims to; a guard that cannot fail is decoration.

Go: read the real graph with `go list`, for each OS you ship.

```go
// go list -deps=false -f '{{.ImportPath}} {{join .Imports " "}}' ./...
// (add -test to include test imports; repeat with GOOS=windows and darwin)
func TestImportsFollowTheAllowlist(t *testing.T) {
	for _, e := range edges(t) {
		if !allowed(e) && !isException(e) {
			t.Errorf("%s -> %s is not allowed", e.from, e.to)
		}
	}
	if len(exceptions) > maxExceptions { t.Fatal("ratchet cap may not grow") }
}
func TestCheckerCatchesAPlantedViolation(t *testing.T) {
	got := violations([]edge{{"app/domain", "app/http"}}, rules)
	if len(got) != 1 { t.Fatalf("want 1 planted violation, got %v", got) }
}
```

JS/TS: express the rules in dependency-cruiser (`.dependency-cruiser.cjs` with `forbidden` rules, `depcruise src --config`) and run it from the test runner or CI; keep a baseline file (`--ignore-known`) as the ratchet and a fixture folder with a deliberate violation as the self-test. Python: `import-linter` contracts play the same role.

Optional report: [archsieve](https://github.com/FullFran/archsieve) can draw the graph and diff it between two refs. Run it with `npx` at a pinned tag, artifacts outside the repo, and treat it as a report for a review, never as a gate or a dependency: `error` findings are facts, `signal` findings are questions, `unknown` means "not inferable". Never run it unpinned.

## Generated model

If the repo keeps an architecture diagram, generate it from the graph (a test fails when it is stale) and never edit it by hand. Families of packages fold into one node; production edges and test-only edges look different.

## ADR minimum

One file per decision: context, decision, consequences, status. Accepted ADRs are append-only: a dated `### YYYY-MM-DD` amendment, or a new ADR marked as superseding the old one.

## What a PR shows

1. AS-IS: the relevant edges before the change, from the tool.
2. TO-BE: the new or changed modules and edges, each with the need it answers.
3. The boundary test output after the change, and the regenerated model diff if edges moved.
4. If the layering changed: the ADR amendment in the same PR, before the rule edit.
5. Optionally, a graph diff excerpt, labelled as a report.
