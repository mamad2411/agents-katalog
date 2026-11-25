---
name: e2e-tests
description: Set up or extend end-to-end integration tests that drive a real, disposable Joomla or standalone PHP stack in Docker over real HTTP, with a version matrix derived from what the project actually declares. Use when adding E2E or browser-level integration tests, testing template and HTTP behaviour that in-process tests cannot observe, or building a disposable Docker test stack for an extension. Unit and in-process integration tests belong to the joomla skill's testing reference.
---

# End-to-end integration tests

E2E tests run PHPUnit on the **host**, driving a real, disposable stack in Docker over real HTTP.
Nothing boots the application in-process; the suite observes it exactly as a browser — or an attacker
— would.

## Where this layer sits

Three layers, each with a job the others cannot do. This skill owns only the third.

| Layer | Mechanism | Answers |
|---|---|---|
| **Unit** | In-process, stubs and doubles | Does this class's logic work? |
| **Integration** | In-process, real CMS classes loaded from a Joomla checkout | Does it work against Joomla's actual signatures? |
| **E2E** | Host-side PHPUnit over HTTP against Docker | Does the running site behave correctly for a real request? |

The first two are covered by the `joomla` skill's testing reference — real-CMS bootstrap, query
stubs, model and table patterns, Jest for JavaScript. **Do not convert them.** An in-process
integration suite that loads real Joomla classes is a legitimate, cheap, fast layer; it catches
signature drift across Joomla versions in seconds, which no Docker run will ever match on speed.

What it cannot do is observe anything that only exists in a real request: rendered template HTML,
response headers and status codes, redirects, session and cookie behaviour, ACL as enforced by the
actual dispatcher, `.htaccess` rules, and whether a refusal actually prevented the state change.
That is this layer's job, and it is why the testing reference points here.

If an E2E suite already exists, evaluate it against this skill first. Expand what already follows the
pattern; port assertions rather than deleting and starting over.

## Step 0 — establish the target

Before writing anything, derive — never guess:

1. **Software type** — Joomla extension or standalone PHP. Usually obvious from the manifest (an
   `*.xml` with `<extension>`, or `composer.json` alone).
2. **Supported PHP range** — `composer.json` → `require.php` (or `config.platform.php`). The maximum
   satisfying version is the day-to-day target; the minimum is the floor of the E2E matrix.
3. **Supported Joomla range**, if applicable — the installer's declared minimum (`$minimumJoomla` in
   `script.<element>.php`, or the manifest's minimum-Joomla tag) is the matrix floor. The latest
   stable release is the day-to-day version and the ceiling.

Write down where you got each bound. Matrices go stale the moment a new PHP or Joomla release ships,
or the project's own declared floor moves — re-derive rather than hand-editing version numbers.

## Architecture

A self-contained `tests/integration/` (or `tests/e2e/`) directory:

```
tests/integration/
  docker/
    docker-compose.yml       # services only; never composed or run by hand
    Dockerfile.<service>     # one per built image (php, web, …)
    env.dist                 # committed template; run.sh copies it to .env on first run
    run.sh                   # the one-shot orchestrator
    config/                  # vhost configs, php.ini overrides
  src/
    Engine/                  # host-side HTTP client, DB access, session helpers
    Tests/                   # the PHPUnit test classes
    AbstractE2ETestCase.php  # base class: logged-in actors, refusal/assertion helpers
  bootstrap-e2e.php          # registers the autoloader, probes that the site is reachable
  config.dist.php            # committed defaults; config.php is generated and git-ignored
  README.md                  # requirements, quick start, options, matrix rationale
phpunit-integration.xml      # separate from the unit config; bootstrap = bootstrap-e2e.php
```

`run.sh` is the supported entry point and must, in order: scrub any previous stack and volumes to a
clean slate, build and bring the services up, install and configure the target software, provision
fixtures, run PHPUnit, then tear down unless told to keep it. **A run that fails partway must never
leave a stack behind in an unknown state** — scrub on entry as well as on teardown, not only on
success.

Useful options: an override for the CMS/PHP version under test, `--matrix` to iterate the full
matrix, `--filter` passed through to PHPUnit, `--skip-build` to reuse a built package,
`--keep-containers` to leave the stack up for fast iteration (provisioning is the slow part;
re-running against a kept-up stack should take seconds), `--down` to tear down and exit, and
`--no-tests` to provision without running the suite.

`bootstrap-e2e.php` loads no application code and opens no direct database connection. It registers
the autoloader and probes the site over HTTP, failing with a clear "run `docker/run.sh` first"
message instead of a wall of connection-refused errors.

### Where PHPUnit runs

The E2E runner executes on the host while the site runs in a container, so **the runner's PHP version
is independent of the site's PHP version under test** — that separation is the point, and it is what
lets one runner drive a whole matrix. Whether PHPUnit is a project dev-dependency or a global install
is the project's own convention; follow whatever it already does, and only raise it if the project's
`require.php` constraint actually prevents installing a runner that can drive the matrix.

Write a `README.md` in the test directory covering requirements, quick start, the options table, and
— critically — **why the matrix contains the versions it does**, tied to specific version-gated code
paths where possible. A green single-version run proves less than it looks; say so when that is the
situation.

## Joomla specifics

- Services: `db` (MySQL), `php` (PHP-FPM running Joomla and the Joomla CLI), `web` (Apache proxying
  to `php` over FastCGI). Add an nginx service only if the project has server-specific behaviour
  worth exercising twice — `.htaccess`-based access control that nginx does not honour, say. Don't
  add it by default.
- This harness targets Docker and Linux. Joomla also supports IIS, but reproducing it here is out of
  scope; note that as a coverage gap rather than pretending it is covered.
- Install Joomla via its own `installation/joomla.php` CLI installer inside the `php` container, not
  by hand-seeding the database.
- Enforce the installer's declared minimum version before touching Docker at all, reading it from the
  same file the installer itself reads, so the two cannot drift apart.
- If the project sends mail, add a Mailpit (or equivalent SMTP sink with an inspectable API) service
  rather than stubbing the mailer — that exercises the real mail configuration end to end. Add an
  IMAP/POP3 source only if the project actually fetches mail.

## Standalone (no CMS) specifics

- Services: `php` (CLI or built-in server, whichever the software actually runs under) plus any real
  dependency it talks to. Prefer running a real dependency over mocking what Docker can run.
- No CMS install step; provisioning means getting the software's own fixtures and config into place.
- Default to the latest supported PHP; `--matrix` covers the declared range.

## Writing tests

- Each class lives under `src/Tests/`, extends the shared base case, and drives the site through the
  host-side HTTP client — never through direct database writes for the behaviour under test.
  Fixtures and setup are the exception.
- **When a request should be refused, assert both the refusal and the absence of its effect.** A
  rejected message is easy to fake; a row that was not written is not.
- Where a refusal's evidence lives in session state — a flash message, a redirect target — assert it
  against the actor whose session it belongs to, not a fresh unrelated client.
- **Before trusting a new "must be refused" test, confirm it can actually fail.** Point it at a
  legitimate variant of the same request and check the assertion would catch a missing guard, not
  merely a syntactically different one.
- When behaviour looks like a genuine product bug rather than a test-writing mistake, skip the test
  with a clear diagnosis and raise it. Do not assert today's buggy behaviour as correct to get a
  green suite.

## Safety

- Default to tearing the stack down after a run, and always scrub before starting — a previous
  crashed run must never leak into the next one.
- Never point these services at a non-disposable database or a real mail server. Check for an
  existing local dev stack before picking ports and container names, so the two cannot collide.

---

*Adapted for this suite from the `e2e-tests` skill in
[nikosdion/pm-skill-demo](https://github.com/nikosdion/pm-skill-demo), MIT licensed,
Copyright (c) 2026 Nicholas K. Dionysopoulos. Reconciled with this suite's existing testing guidance:
in-process integration tests are presented as a complementary layer rather than something to convert
away, and the PHPUnit installation mandate and IIS exclusion are stated as project choices and
coverage gaps rather than requirements. The MIT permission notice accompanies this adaptation; full
text at <https://github.com/nikosdion/pm-skill-demo/blob/main/LICENSE>.*
