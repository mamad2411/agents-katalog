---
name: symfony-yoandev-local-dev
description: >-
  Set up and run a Symfony project locally: PostgreSQL and Mailpit in Docker, the
  Symfony CLI dev server which auto-injects DATABASE_URL and MAILER_DSN from the running
  containers, HTTPS and HTTP/2 out of the box, and an optional FrankenPHP container for
  checking the app in production-like conditions before shipping. Use this skill whenever
  someone asks how to start or run the project, set up a development environment, get the
  database running, find where sent emails went, fix "connection refused" or "could not
  find driver", configure compose.yaml or compose.override.yaml, enable HTTPS locally,
  onboard onto an unfamiliar Symfony project, or verify that something works with
  APP_ENV=prod. Also use it when a project has no README explaining how to boot it.
---

# Local development

> **Tier: core** — a project that cannot be booted cannot be tested. The production-like container is the on-demand part: run it before shipping, not daily.

Services in Docker, PHP on the host, the Symfony CLI wiring the two together.

```bash
docker compose up -d          # PostgreSQL + Mailpit
symfony server:start -d       # dev server, HTTPS, variables injected
symfony open:local            # open the app
symfony open:local:webmail    # read the emails it sent
```

That is the whole daily loop. What follows is why it works and what breaks it.

## The part that surprises people

You do not write `DATABASE_URL` or `MAILER_DSN` anywhere. The Symfony CLI inspects the
running containers, matches each exposed container port against a table of known
services, and exports the variables into the PHP process it starts.

```bash
symfony var:export --debug     # exactly what is being injected, and from where
```

This is why `compose.override.yaml` publishes ports **without a host port**:

```yaml
services:
  database:
    ports:
      - "5432"     # not "5432:5432"
```

Docker picks a free host port, the CLI discovers it. Two projects run side by side and
nobody edits a file to dodge a collision. Pinning the host port throws that away for no
benefit.

Consequences worth knowing:

- **`symfony console` is not `php bin/console`.** The first gets the injected
  variables, the second does not. On a project set up this way, `php bin/console
  doctrine:migrations:migrate` fails to connect while `symfony console …` works — and
  the error message does not explain why.
- **The injected variables win over `.env.test`.** `symfony console
  doctrine:database:drop --force --env=test` drops the *development* database, because
  the Docker variables are applied regardless of `--env`. This is documented behaviour
  and it has cost people real data. Use `php bin/console` for anything targeting the
  test database.

The full detection table, the service-naming labels, and how to opt a service out:
`references/symfony-cli.md`.

## Setting up a project that has neither

Copy `assets/compose.yaml` and `assets/compose.override.yaml` to the project root.
They match what the Doctrine and Mailer recipes generate, which means a project that
still has its recipes needs nothing from here.

Then:

```bash
docker compose up -d
symfony console doctrine:database:create
symfony console doctrine:migrations:migrate --no-interaction
symfony console doctrine:fixtures:load --no-interaction   # if the project has fixtures
symfony server:start -d
```

If the project has no fixtures and no seed data, say so rather than inventing rows —
an empty application that boots is a normal outcome, and quietly making up data hides
the fact that onboarding is incomplete.

## HTTPS, and why it is not optional here

```bash
symfony server:ca:install     # once per machine
```

Then every project is served over HTTPS with HTTP/2, without a certificate warning.

This matters beyond comfort. **AssetMapper depends on HTTP/2 multiplexing**: it serves
many small files instead of one bundle. Developing over plain HTTP means the one
environment where you would notice a problem behaves differently from production. It
also surfaces mixed-content and secure-cookie issues on the day you write the code
rather than after a deploy.

## Emails

Mailpit catches everything. Nothing leaves the machine.

```bash
symfony open:local:webmail
```

Two things to check when emails seem to vanish:

- **They may be queued, not sent.** This standard routes `SendEmailMessage` to the
  async transport, so nothing reaches Mailpit until a worker consumes it. Run
  `symfony console messenger:consume async -vv`, or accept that the mail appears late.
  In tests, `assertQueuedEmailCount()` is the assertion that applies, not
  `assertEmailCount()`.
- **The `mailer` service must expose port 1025**, which is what the CLI matches on.
  Port 8025 is only the web interface.

## Checking it the way production will run it

The dev server is forgiving in ways production is not: the profiler is loaded,
OPcache is off, assets are served through PHP, errors are visible. Some bugs only
exist on the other side of that line.

```bash
docker compose -f compose.yaml -f compose.prod-like.yaml up --build
open https://localhost
```

`assets/Dockerfile.prod-like` builds with `APP_ENV=prod`, production `php.ini`, an
authoritative classmap and `asset-map:compile`. It answers questions the dev server
cannot:

- do the assets actually compile, and are they served rather than generated;
- does the application boot without dev-only bundles;
- is anything depending on the profiler or on `APP_DEBUG=1`;
- does a page still work when errors stop being displayed.

**This is a verification step, not a working environment.** Do not move daily
development into it: you lose instant reload and step debugging, and you pay a rebuild
for every change. Run it before shipping something significant, not before every
commit.

**It is also not a production Dockerfile.** For real deployment use
[`dunglas/symfony-docker`](https://github.com/dunglas/symfony-docker), which handles
workers, healthchecks, non-root users and TLS. Details and the checklist of what to
look at while it runs: `references/frankenphp.md`.

## When something does not start

| Symptom | Cause |
|---|---|
| `connection refused` on the database | The container is not running, or `php bin/console` was used instead of `symfony console` |
| `could not find driver` | `pdo_pgsql` is missing from the **host** PHP — the container's extensions are irrelevant here |
| Variables not injected | Containers started from a different directory, or the compose project name differs. Check `symfony var:export --debug` |
| Port already in use | A host port was pinned in `compose.override.yaml`. Remove it and let Docker choose |
| Emails never arrive | They are queued; consume the transport |
| Migrations run against the wrong database | The Docker variables override `--env=test`. Use `php bin/console` for the test database |

`symfony server:log` shows the server, PHP and application logs in one stream, which
is usually faster than opening `var/log/dev.log`.

## Reference files

| File | When to read it |
|---|---|
| `references/symfony-cli.md` | Variable injection, service detection, naming labels, worker processes |
| `references/frankenphp.md` | Running the production-like check and what to look for |
