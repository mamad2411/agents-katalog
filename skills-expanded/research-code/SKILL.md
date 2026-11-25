---
name: research-code
description: "Understanding an unfamiliar codebase quickly: entry points and build files, tracing one request or command end to end, finding definitions and every use, reading history with git log, blame and pickaxe searches, tests as documentation, mapping data flow and dependencies, and writing the map down with paths and lines. Read before answering questions about how a codebase works."
---

# Understanding an unfamiliar codebase

The naive way reads files in alphabetical order, opens forty of them,
guesses behaviour from names, answers "how does X work" with a folder
listing, and misses the middleware, decorator or event listener that
changes everything. The fast way orients in one step, finds the entry
point, traces one real path end to end with a line number at every hop,
and writes the map down. How to weigh evidence and present the answer is
`research`.

## 1. Orient in one step

Request these together, then decide where to go:

- `README`, `CONTRIBUTING`, `docs/` (architecture notes, ADRs in
  `docs/adr/`), `AGENTS.md` or `CLAUDE.md`, `DESIGN.md`.
- The manifest and its scripts: `package.json` (scripts, workspaces),
  `pyproject.toml`, `Cargo.toml` (workspace members), `go.mod`,
  `composer.json`, `Gemfile`, `pom.xml` or `build.gradle`, and the task
  runner (`Makefile`, `justfile`, `Taskfile.yml`).
- CI config (`.github/workflows/*.yml`, `.gitlab-ci.yml`): it holds the
  commands that really build, test and lint.
- Config: `.env.example`, `config/`, `settings.py`, `application.yml`,
  `docker-compose.yml`, the `Dockerfile`.
- The tree: the workspace's top level is in your prompt; `read` a folder to
  list it (`read src`); `glob` by name or extension (`**/*.test.ts`,
  `**/migrations/**`) to find a kind of file and see how many there are.

`glob` and `grep` skip `.git`, `node_modules` and whatever `.gitignore`
lists. A `*` in a `glob` pattern also matches `/`, so `src/*.ts` finds
nested files too: narrow by name, not by depth.

## 2. Find the entry points

| Kind | Where | Search for |
|---|---|---|
| Node server | `main` or `start` in `package.json`, `src/index.ts`, `server.ts`, `app.ts` | `listen(`, `createServer`, `express()`, `fastify(`, `new Hono` |
| Next.js | `app/**/page.tsx`, `app/**/route.ts`, `middleware.ts` or `proxy.ts`, `pages/api/**` | the folder path is the route |
| Python web | `manage.py`, `urls.py`, `main.py`, `asgi.py` | `@app.get(`, `@router.`, `urlpatterns`, `path(` |
| Go | `cmd/*/main.go`, `main.go` | `func main(`, `HandleFunc(`, `r.Get(`, `mux.Handle(` |
| Rust | `src/main.rs`, `src/bin/`, `[[bin]]` in `Cargo.toml` | `fn main`, `#[tokio::main]`, `Router::new()` |
| Rails, Laravel | `config/routes.rb`, `routes/web.php`, `routes/api.php` | `resources :`, `Route::get(` |
| Spring | the `@SpringBootApplication` class | `@RestController`, `@GetMapping` |
| CLI | `bin` in `package.json`, `[project.scripts]`, `[[bin]]` | `#[derive(Parser)]`, `cobra.Command`, `@click.command`, `argparse`, `commander` |
| Jobs | queue and scheduler setup | `new Worker(`, `@Cron`, `celery`, `sidekiq`, `schedule`, `on: schedule` |
| Library | the exported surface | `exports` in `package.json`, `index.ts`, `pub mod` and `pub use` in `lib.rs`, `__all__` |
| Browser app | `index.html`, `main.tsx` | `createBrowserRouter`, `createRouter`, `routes` |

## 3. Trace one path end to end

Pick one concrete request or command the question is about, and follow it
from where it enters to where it leaves, writing each hop as you go:

```
POST /orders
1. src/routes/orders.ts:12    router.post("/orders", requireUser, validate(OrderIn), createOrder)
2. src/middleware/auth.ts:30  requireUser: session cookie to req.user; 401 when absent
3. src/orders/handlers.ts:44  createOrder calls orders.place(req.user.id, body)
4. src/orders/service.ts:71   place(): checks stock, opens db.transaction
5. src/orders/repo.ts:23      INSERT INTO orders ... RETURNING id
6. src/orders/service.ts:98   queue.add("send-confirmation"), inside the transaction
7. src/errors/handler.ts:15   OutOfStock mapped to 409 { code: "out_of_stock" }
```

- The usual order: route, middleware (auth, validation, rate limits),
  handler, service, data access, the database or outside call, the response
  mapping, the error handler.
- Where the trail goes indirect, find the other end:
  - events and pub/sub: grep the event name (`"order.created"`) for its
    listeners;
  - dependency injection: where the container registers the implementation;
  - interfaces and traits: every implementation (`implements Store`,
    `impl Store for`);
  - decorators and annotations: what the framework does with them;
  - conventions: file-based routing, Rails naming, magic method names;
  - generated code: the schema it comes from (OpenAPI, GraphQL, protobuf,
    Prisma), which is the thing to read;
  - feature flags and environment switches that choose the branch.
- Note surprises as you pass them. Here: the confirmation is queued before
  the transaction commits.

## 4. Find definitions, then every use

`grep` takes a Rust regular expression (no lookaround or backreferences;
`\b` and `(?i)` work) and returns `path:line:text`, 200 hits by default.
It shows no context, so `read` the range around a hit with `offset` and
`limit`.

Definitions, one language per line:

```
TS, JS        (function|class|interface|type|enum)\s+Name\b    (const|let)\s+Name\s*=
Python        ^\s*(async\s+)?def name\b    ^\s*class Name\b
Go            func (\([^)]*\)\s*)?Name\(    type Name\s+(struct|interface)
Rust          fn name\b    (struct|enum|trait|type|mod)\s+Name\b    impl.*\bName\b
Java, Kotlin  (class|interface|record|enum|object)\s+Name\b    fun name\(
Ruby, PHP     def (self\.)?name\b    function name\s*\(    class Name\b
```

- Then the uses: `\bName\b`, calls `name\(`, methods `\.name\(`, imports
  (`import .*\bName\b`, `from \S+ import .*\bname\b`, `use .*\bName\b`).
- Every spelling of a concept that crosses layers: `userId`, `user_id`,
  `user-id`, `UserId`, `USER_ID`, plurals, abbreviations. One pattern
  covers most: `user[_-]?ids?` with `case_sensitive: false`.
- The strings that join layers are often easier to find than the code:
  route paths, event and queue names, error codes, config keys, environment
  variables (`process\.env\.`, `import\.meta\.env\.`, `os\.environ`,
  `getenv\(`, `env::var\(`), table names, translation keys.
- Too many hits: narrow with `path` or a longer pattern rather than raising
  the limit and reading them all. None: try the other spellings, a shorter
  fragment, the message the code prints; only then call it absent.
- With a shell, ripgrep adds context and file types: `rg -n -w -C 3 Name`,
  `rg -n -t py 'def name\b'`, `rg -n -g '!dist' 'pattern'`.

## 5. Read the dependency, not your memory of it

When the answer turns on what a library does (a default, a retry, what an
option means), read the installed version:

- Node: `node_modules/<pkg>/package.json` gives `version`, `main`,
  `exports` and `types`; read the file they point to, and the `.d.ts` for
  the surface. pnpm keeps the files in
  `node_modules/.pnpm/<pkg>@<version>/node_modules/<pkg>`. A search from the
  root skips `node_modules`, so give `grep` the package's folder as `path`
  (`node_modules/zod`), and `read` a folder to list it.
- Python: `.venv/lib/python3.*/site-packages/<pkg>/`. PHP:
  `vendor/<vendor>/<pkg>`. Go: `vendor/` when the project vendors.
- Outside the workspace, where `read` cannot go (the Cargo registry, the Go
  module cache, global gems): read the source at the locked version on the
  web (`research-web`).
- Minified bundles are not for reading: find the unminified build (`esm/`,
  `cjs/`, `src/`) or the source at the tag.

## 6. History: why it is like this

These need `bash` and git. Without them, name the command that would
answer, and read what the project keeps instead (CHANGELOG, ADRs, docs).

```sh
git log --oneline -- src/orders/refund.ts       # who changed it, and when
git log --follow -p -- src/orders/refund.ts     # every change, across renames
git log -S'MAX_REFUND_DAYS' --oneline           # commits that added or removed the text
git log -G'retry.*[Ll]imit' --oneline           # commits whose changed lines match
git blame -w -C -L 40,60 src/orders/refund.ts   # last change per line, moves followed
git show <sha>                                  # the message and the whole change
git log --since='2 weeks ago' --stat            # what changed lately
```

- The commit message, the pull request it came from (`#123`, or
  `gh pr view 123` where `gh` is installed) and the linked issue hold the
  why. Quote them.
- When a formatting commit hides the real author, use
  `--ignore-revs-file .git-blame-ignore-revs` if the project keeps one, or
  blame from the commit before it: `git blame <sha>^ -- <path>`.

## 7. Tests as documentation

- Find them: `**/*refund*.test.*`, `**/test_*refund*.py`, `*_test.go`
  beside the file, `#[cfg(test)] mod tests` in the same Rust file, `spec/`
  for RSpec.
- Test names state the intended behaviour, fixtures show valid shapes of
  the data, and the edge cases tested are the ones someone cared about.
- A case with no test is not pinned down: say so when the answer rests on
  it.
- End-to-end tests show which journeys the team considers important.

## 8. Map data flow and ownership

For one piece of data (a column, a field, a cache key, a setting), find who
writes it, who reads it, where it is validated and where it leaves the
system:

| Data | Written by | Read by | Notes |
|---|---|---|---|
| `orders.status` | `service.ts:88` (place), `webhooks.ts:40` (payment) | `handlers.ts:61`, `reports/daily.ts:17` | two writers, no transition check |
| `REFUND_WINDOW_DAYS` | `.env.example:12`, the deploy config | `config.ts:30` | 30 when unset |

Writers turn up with assignment and update patterns (`\.status\s*=`,
`status:\s`, `SET status`, `update\(.*status`); readers with the field name
and the serialiser.

## 9. Write the map down

- The entry, each hop with `path:line` and a clause on what it does, then
  the surprises: dead code (no references found), two implementations that
  disagree, a flag that changes the path, a TODO that matters.
- Keep what you read apart from what you assumed: a function you did not
  open is named as not read.
- Keep to the question: the refund path, not the repository.
- A sweep too wide for your context (every caller across thirty files) goes
  to `librarian`, which returns excerpts with lines.

## 10. Time-box

- A question about one path: 10 to 20 tool calls. A map of a whole system:
  30 to 40, and say what was skipped.
- Request independent reads and searches together, in one step.
- Follow the branch the question needs; list the others as not followed.

## Check it

- Every hop in the trace has a path and line that you actually read.
- Claims about a dependency cite its installed version.
- Every spelling was searched before anything was declared absent.
- The map answers the question that was asked.

## Avoid

Reading the repository file by file; guessing behaviour from names; a
folder listing as an answer; skipping middleware, decorators, events and
generated code; docs trusted over the code that runs; one spelling searched
and the concept declared missing; reading minified bundles; history claims
without the commit.
