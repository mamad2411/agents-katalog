---
name: library-first-development
description: Use BEFORE hand-writing any non-trivial functionality or mechanical scaffolding — parsing, dates/timezones, auth, retries/backoff, HTTP, validation, state machines, queues, crypto, file formats, migrations, generated clients, framework boilerplate, etc. Forces researching existing libraries and official CLIs/generators first, preferring maintained tooling over hand-rolling, then vetting it properly before adopting. Trigger on "let's write a", "I'll implement", "build a helper for", "we need to handle X", "roll our own", and any moment you're about to reinvent something a library or CLI already does.
---

# Library-First Development

Default position: **someone has probably already built this, better, and maintains it.** Hand-rolling means *you* now own the bugs, the edge cases, and the maintenance forever. So you research first and reach for the project library, framework feature, or official CLI/generator — and you only build it yourself when nothing genuinely fits, and you say why.

This is not "add dependencies carelessly." It's "don't reinvent the wheel, *and* don't bolt on a junk wheel." Library-driven development means: use the ecosystem's maintained code path first, prefer mechanical generation for mechanical files, then vet hard.

## The workflow

1. **Name the capability** in one sentence ("parse and diff ISO-8601 durations", "rate-limit outbound calls with backoff", "create a database migration for a new table"). If a mature library or framework tool category exists for it, you're in scope.
2. **Check the project first** — dependency files, framework docs, local scripts, `bin/`, `scripts/`, package scripts, Makefiles, task runners, and existing generated-file conventions. Prefer what the repo already uses.
3. **For mechanical output, check the CLI/generator before editing files.** Migrations, scaffolds, models, controllers, routes, SDK clients, generated types, config stubs, locks, snapshots, and boilerplate should usually start with the official command, not a hand-created file.
4. **Find real candidates** — use [[research]]. Get actual maintained options from primary sources (official docs, registries, GitHub, the ecosystem's "awesome" lists), not a half-remembered name.
5. **Vet before adopting** (below). A popular library that's abandoned or risky is not the answer.
6. **Adopt the best fit, use the CLI, or hand-roll with a written reason** (below).

## CLI-first scaffolding

If the work creates or updates files that a framework normally generates, the first implementation question is:

```text
Is there a CLI command that scaffolds this mechanically?
```

Use the closest official or locally-standard command when available: framework generators, ORM migration tools, codegen clients, schema/type generators, package manager init commands, project scripts, or repository-specific wrappers.

Before keeping generated output:

- Prefer `--help`, `--dry-run`, `--pretend`, `--create-only`, `--check`, or scratch-directory generation when the tool supports it.
- Run commands through the project's package manager or local bin (`npm exec`, `pnpm exec`, `bundle exec`, `bin/rails`, `python manage.py`, `go generate`, etc.) so versions match the repo.
- Inspect the diff. Generated code is a starting point, not an exemption from review.
- Keep generated files only if they match the requested slice; delete or regenerate accidental scaffolding with the tool's undo command when one exists.
- If you hand-create a migration/scaffold/client because the CLI cannot express it, say which CLI you checked and why manual code is safer.

## Vetting — judge the library, not its marketing

Stars and download counts are gameable; ignore them as primary signals. Use real adoption and health data. `ecosyste.ms` covers every major registry:

```bash
curl -s "https://packages.ecosyste.ms/api/v1/registries/<registry>/packages/<package>" | jq '{
  dependent_repos: .dependent_repos_count,
  dependent_packages: .dependent_packages_count,
  latest_release: .latest_release_published_at,
  first_release: .first_release_published_at,
  maintainers: (.maintainers | length),
  license: .normalized_licenses,
  advisories: (.advisories | length),
  archived: .repo_metadata.archived
}'
# registries: npmjs.org, pypi.org, rubygems.org, crates.io, proxy.golang.org, nuget.org, repo1.maven.org, ...
```

**Adopt-worthy signals:** high dependent-*repo/package* count (real projects rely on it), recent release, multiple maintainers, OSI-approved license, few open advisories, not archived.

**Red flags — slow down:** archived repo; last release >2 years ago; single maintainer / high bus factor; <90 days old; known advisories; non-OSI or missing license; vendors copies of common deps; runs code on install.

Bus factor — single-maintainer dominance is a real risk:
```bash
# .repo_metadata.metadata.development_distribution_score  (<0.15 = one person carries it)
```

Security posture (optional, for anything load-bearing):
```bash
curl -s "https://api.scorecard.dev/projects/github.com/<owner>/<repo>" | jq '{score, checks: [.checks[] | {(.name): .score}]}'
```

**Verify it actually exists before you install it.** AI assistants hallucinate plausible package names, and attackers register them (slopsquatting). Confirm on the registry (`npm view <pkg>`, `pip index versions <pkg>`), check it's not a typo of the real package, and copy the name from official docs rather than typing it from memory.

## When hand-rolling IS the right call

Build it yourself only when one of these is true — and write the reason in a comment or the PR:

- No maintained library actually fits (you evaluated real ones; document which and why they fell short).
- No official/local CLI can safely generate the mechanical files (you checked it; document the command or docs).
- The capability is genuinely trivial (a few lines, no edge cases, no ongoing maintenance burden).
- A dependency would be reckless here (unmaintained, unacceptable license, security-critical surface you must control).

"I'd rather just write it" is not a reason. "I evaluated `x`, `y`, `z`; `x` is abandoned, `y` pulls 40 transitive deps for a 10-line need, `z`'s license is GPL and we ship proprietary — so a 12-line inline implementation is the right trade-off" *is* a reason.
"I created the migration by hand because it was faster" is not a reason. "I checked `framework migrate --help`; it cannot express this database-specific constraint, so I generated an empty migration and hand-edited that file" is a reason.

## Supply-chain hardening

This skill chooses dependencies; it also has to spot when a dependency deserves a deeper risk pass. Slow down when a package is single-maintainer, stale, very new, anonymous, low-adoption for its ecosystem, missing a security contact, has critical CVEs, runs install scripts, or touches high-risk surfaces like deserialization, native code, auth, crypto, or third-party code execution.

For load-bearing dependencies, record the risk factors you checked and any safer alternatives. Prefer real registry/GitHub data over vibes: release recency, dependent repos/packages, maintainers, advisories, license, repository archival status, and security policy. If a risky dependency is still the right choice, say why.

---

*Original skill for Oisín's skills repo. Vetting criteria (ecosyste.ms / OpenSSF Scorecard / risk thresholds / slopsquat checks) drawn from [andrew/managing-dependencies](https://github.com/andrew/managing-dependencies) by Andrew Nesbitt (CC0-1.0), with the default lean flipped from minimalist to library-first and supply-chain risk guidance folded in from local oisin-pipeline material. CLI-first scaffolding guidance is informed by official framework generator/migration documentation such as Rails, Prisma, Django, and Laravel. Pairs with [[research]].*
