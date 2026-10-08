# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

```bash
# Start PostgreSQL (required before running the app)
docker compose up -d

# Run app with hot-reload (Tailwind watch + dotnet watch + browser open)
npm run dev

# Build the full solution
dotnet build KlavLor.slnx

# Run just the web project
dotnet run --project KlavLor.Web/KlavLor.Web.csproj

# Build Tailwind CSS once (also runs automatically before dotnet build via .csproj target)
npm run build:css

# Run the integration tests (needs a working Docker daemon — Testcontainers starts its own Postgres)
dotnet test KlavLor.IntegrationTests/KlavLor.IntegrationTests.csproj

# Run the unit tests (no database, no Docker)
dotnet test KlavLor.UnitTests/KlavLor.UnitTests.csproj

# Run the JS tests (roll-ticker.js under jsdom — no browser, no Docker)
npm run test:js
```

**App URL:** https://localhost:7081

**Database:** PostgreSQL on localhost:5432, database `klavlor`, user/password `postgres/postgres` (local dev via compose.yaml). Migrations run automatically on startup.

### EF Core Migrations

```bash
# Add a new migration
dotnet ef migrations add <MigrationName> --project KlavLor.Infrastructure --startup-project KlavLor.Web

# Remove last migration (if not applied)
dotnet ef migrations remove --project KlavLor.Infrastructure --startup-project KlavLor.Web
```

## Architecture

Clean Architecture with four layers. Dependencies flow inward: Web → Application → Domain, Infrastructure → Domain.

- **KlavLor.Domain** — Entities, repository interfaces, domain services. No external dependencies.
- **KlavLor.Application** — Feature handlers (CQRS-style), FluentValidation validators, the Result pattern. Handlers and validators are auto-registered via assembly scanning (classes ending in `*Handler` get scoped registration).
- **KlavLor.Infrastructure** — EF Core DbContext (`DataContext`), repository implementations, OSRS Wiki API client, image caching. Repositories are auto-registered via reflection — see "Repository Auto-Registration" below.
- **KlavLor.Web** — ASP.NET Core host, Razor components, HTMX endpoints, cookie auth + API key auth.
- **KlavLor.IntegrationTests** — xUnit tests over a real PostgreSQL (Testcontainers, `postgres:16-alpine`) with the full migration set applied. See "Integration Tests" below.
- **KlavLor.UnitTests** — xUnit tests over the pure loot maths plus the architecture rules. No database, no Docker. See "Unit Tests" below.

### Repository Auto-Registration

`AddDomainRepositories()` / `AddApplicationRepositories()` in `InfrastructureDependencyConfiguration` scan the Infrastructure assembly for every concrete class and register it against the **first** interface it implements from the Domain (resp. Application) assembly whose name **ends in `Repository`**. That is the whole predicate — the naming convention is just "`I…Repository`", not specifically `IxxxQueryRepository`/`IxxxLogRepository`.

Two failure modes are silent, because nothing throws when the scan misses:

- An interface the scan doesn't match simply has **no registration**, and the first request for it throws at runtime on whichever page needs it.
- The scan takes `FirstOrDefault`, so a class implementing **two** repository interfaces from the same assembly gets exactly one of them registered — which one depends on reflection ordering.

`KlavLor.UnitTests/RepositoryRegistrationTests.cs` enforces all of this: every implemented repository interface is registered, no class claims two per assembly, no interface has two implementations, and every repository actually resolves from a request scope (it builds the real container — no DB is touched, since Npgsql opens no connection until a query).

### The Loot-Log Query Surface Is Five Repositories, Split By Consumer

`ILootLogRepository` / `LootLogRepository` no longer exist. What was one 2,768-line class with 38 methods is now five, grouped by the consumer feature that reads them (matching the "organised by feature, not technical concern" rule above) — interfaces in `Application/Interfaces/Repositories/`, implementations in `Infrastructure/Persistence/EntityFramework/Repositories/Loot/`:

- `ILootLogSearchRepository` — admin sync log, public character list, per-character log search, sources table. Read by `LootLogHandler` and `IngestLogHandler`.
- `ILootSourceDetailRepository` — source detail + paged kills, hover popover, monthly kill trend, collection-log panel. Read by `LootLogHandler`, `SourcePopoverHandler`, `LootCharacterProfileHandler`, `LuckLeaderboardRefreshService`.
- `ILootSessionRepository` — per-source sessions, one session's kills, cross-source session history.
- `ILootFeedRepository` — the live feed's per-tier backfill, the character day feed, the first-time feed.
- `ILootProfileRepository` — profile header, window stats, activity heatmap, monthly trend, personal records, top items, plus bulk deletion by character/user.

`LootLogSharedQueries` holds the two private helpers used by more than one of them (`GetTopDropsForSource`, `NullableTimestampParam`), imported with `using static` so the call sites read unchanged. `SessionSql.GapIslandsWithCap` remains the shared gap-and-islands CTE.

A handler that serves several surfaces injects several of these — that is intended, and is what the old single interface was hiding.

### Key Patterns

**Endpoint registration:** Each endpoint class implements `IEndpoint` with a static `MapEndpoint` method and is declared `sealed` (endpoints are never subclassed — `MapEndpoint` is static, so inheritance buys nothing). Registration is **not** automatic — every new endpoint class must be added to the explicit `MapEndpoints<T>()` list in `KlavLor.Web/Configuration/ConfigureEndpoints.cs` (called from `MapApplicationRequestHandlers()` in Program.cs), or its routes silently 404.

**Handler flow:** Endpoint receives request → validates via FluentValidation → handler loads aggregate root from repository → calls domain method on entity → saves via repository → returns `Result<T>`.

**Result pattern:** `Result<T>` with `Success(T)`, `Failure(string)`, and `ValidationFailure(errors)` variants. Handlers never throw; they return Result.

**HTMX integration:** Endpoints return Razor components via `IResultExtensions.Component<TComponent>()`. Other HTMX results: `HtmxRedirect()`, `HtmxRefresh()`, `HtmxRetargetResult<T>()`. These are C# extension members hanging off `IResultExtensions`, defined in `KlavLor.Web/Application/HttpResults/`. Auth redirects are HTMX-aware (returns HX-Redirect header instead of 302 when HX-Request header present).

**Never name a namespace `Results`.** That folder is `HttpResults`, not `Results`, on purpose: a `KlavLor.Web.Application.Results` namespace shadows the framework's `Microsoft.AspNetCore.Http.Results` static class for every file under `KlavLor.Web.Application.*`, because C# resolves enclosing-namespace members before using-directives. It previously forced ~117 call sites to write `Microsoft.AspNetCore.Http.Results.Ok(...)` in full. Plain `Results.Ok(...)` / `Results.NotFound()` now works everywhere; keep it that way.

**Route conventions:** Routes are defined as constants in `AppRoutes.cs`. The `.FromApi()` helper prepends `/api` to all route paths.

### Strict DI Rules

- **Never use `Task.Run`, fire-and-forget (`_ = Task...`), or discard async operations.** All async work must be awaited inline within the request pipeline. The scoped DbContext/Npgsql connection is not thread-safe — concurrent access causes `Connection is busy` errors.
- **Never manually create DI scopes** (`IServiceScopeFactory`, `CreateScope()`, `GetRequiredService()`) in request-scoped code. Always use constructor injection. The only acceptable places for manual scopes are `Program.cs` startup and `BackgroundService` implementations.
- **Never instantiate services directly** (`new HttpClient()`, `new SomeRepository()`). Use the registered DI abstractions.

### Razor Component Data-Access Rules

A production incident (June 2026, fixed in `effdbd6`) was caused by the layout sidebar querying the DB during SSR. Blazor static SSR runs **sibling components' `OnInitializedAsync` concurrently on the same request scope**, so two components loading data in one render pass race on the shared scoped DbContext. EF's "second operation on this context" guard does **not** catch this here, because many repositories execute raw ADO commands directly on `Database.GetDbConnection()` — the race instead corrupts the Npgsql wire protocol (`Received backend message BindComplete while expecting ReadyForQueryMessage`), poisons the connection, and surfaces as intermittent 500s in unrelated requests.

The rules:

- **At most one component per SSR render pass may touch the database.** In practice that is the routed page component only.
- **Layout components and shared/partial components must never query.** They must be parameter-driven, read claims via `ISessionStateManager`, read singleton caches, or fetch their data through their own HTMX request (`hx-trigger="load"` → endpoint → handler), which runs in its own request scope. Reference example: `SidebarAccountEndpoint` + the placeholder in `SidebarComponent.razor`.
- **Components must never inject repositories** (`I*Repository`). When a page component loads its own data, it goes through a `*Handler`. There are no exceptions.
- **Multiple loads inside one component must be awaited sequentially** — never `Task.WhenAll` over handler or repository calls.
- **A page with several independently-loaded panels loads them all at once, and that is fine.** Use `DeferredSection` (`Loot/Log/Profile/DeferredSection.razor`): it fetches on `load` and distinguishes *deferred* (flat placeholder, no spinner) from *in flight* (spinner, driven by htmx's `htmx-request` class and the `.defer-spinner` rule in `app.css`). `CharacterProfile.razor` is the reference caller.

  These panels used to be **staggered** 500ms apart down the page, on the reasoning that "one page view shouldn't open six concurrent queries". That was caution rather than a measurement, and the measurement does not support it. The character page's six endpoints cost **127ms of query time between them**; run all six at once they finish in **68ms**, bounded by the slowest (`sessions`), with every other endpoint as fast or faster than it was alone. The stagger spent **3,000ms** — `Delay(n) = (n+1) x 500`, so the last panel waited three seconds before it *asked* — to spread 127ms of work. End to end the page's panels now complete **197ms** after navigation start instead of ~3,100ms. 90 concurrent requests across three characters returned 90 200s, nothing empty or truncated.

  **This does NOT relax the rule above it.** The two are about different things and it is worth being explicit, because conflating them is how the outage happens again: the SSR rule is about *sibling components in one render pass sharing one scoped DbContext*, which is still forbidden. A `DeferredSection` is its own HTTP request with its own request scope and its own DbContext, which is exactly why several of them may be in flight together. Concurrency **between requests** is ordinary; concurrency **within one request scope** is the bug.

**These rules are enforced by tests, not just documented.** `KlavLor.UnitTests/RazorComponentDataAccessTests.cs` holds three checks:

- `No_razor_component_injects_a_repository` — reflects over the `KlavLor.Web` assembly for `ComponentBase` subclasses with an injected member (`[Inject]` property/field, or a constructor parameter) whose type is an `I*Repository`. This is the rule whose violation caused the outage.
- `No_razor_file_injects_a_repository_type` — a supplementary text scan of the `.razor` files for `@inject` of a repository type, catching declarations the metadata check could miss.
- `No_component_uses_Task_WhenAll` — flags **any** `Task.WhenAll` inside a component. Deliberately conservative: it does not try to classify the operands, because a false negative here is an outage while a false positive is one line of human review. If a flagged `Task.WhenAll` provably touches neither a handler nor the DB, that still needs a human decision — do not add a silent exemption to the test.

### The Roll Ticker Is Every Kill, And Is Cheap Because It Carries No Loot

The banner above the swimlanes (`#roll-ticker` in `LootFeedContent.razor`) shows every kill as it
lands — "ClaudeLock rolled Vorkath #1,204" — with **no loot on it at all**. That is what lets it show
the thing the lanes structurally cannot: a dry kill. The lanes start at 10k, so a Vorkath that
dropped nothing appears here and nowhere else.

`ILootRollFeed` / `LootRollFeedService` is **deliberately separate from `ILootFeedService`**. The two
have different shapes: the feed is partitioned by tier, merges kills into grouped cards and has a
value floor; the ticker has no tiers, no grouping, no floor and no loot, so folding it in would mean
a tier dimension that is always meaningless and a merge path always skipped. The concurrency model is
copied from `LootFeedService` on purpose — partitions pre-populated at construction (so a plain
`Dictionary` is safe under a per-partition lock), one bounded `Channel` per subscriber with
`DropOldest`, and a synchronous non-blocking `Publish` that fans out with `TryWrite` outside the lock.

Three things make it affordable at one event per kill:

- **One stream per scope**, not one per tier.
- **The connect backfill is the in-memory ring**, so opening the page costs no query — which is what
  lets the banner live on the query-free page shell. The lanes' backfill is a database read each.
- **One render per roll, not one per subscriber.** `StreamFeed` builds an `HtmlRenderer` per event
  *per subscriber*, so one publish costs N component renders with N viewers. The feed can carry that
  because it only publishes drops worth 10k or more; the ticker carries every kill. It stays a
  **Razor component** (`LootRollChip.razor` — markup belongs in a `.razor` file, and Razor escapes
  the user-supplied character name for free) and the rendered frame is memoised per entry in a
  `ConditionalWeakTable`, which needs no eviction of its own: an entry is reachable only while the
  ring buffer holds it, so the markup is collected with it. **TWO** such tables, not one — the same
  roll is legitimately rendered both ways, streamed live as it lands and later replayed out of the
  ring as backfill, and one cache would hand the second caller the first one's markup.

**The banner paces arrivals: one roll at a time.** `roll-ticker.js` — its own file, not a block in
`site.js`, so the logic below can be tested without a browser (`tests/js/roll-ticker.test.js`, jsdom).
htmx swaps every SSE frame in the moment it arrives, so a sync landing five kills at once inserts
five chips in one task and slides them in as a single block, which reads as a jolt rather than as
news arriving. Arrivals are detached on sight, queued, and released one per `SLIDE_MS + GAP_MS`.
Order is preserved, so the row ends up exactly where htmx would have left it.

Three things about that file are load-bearing and each has already been got wrong once:

- **A `MutationObserver`, not an htmx event.** The callback is a microtask and therefore runs before
  the next paint, which is what lets a chip be detached, deduped or shifted without ever having been
  drawn. `htmx:afterSettle` is a `setTimeout` away — at least one frame too late.
- **The cadence is held against the CLOCK, not against the queue being non-empty.** Rolls land a
  millisecond or two apart, so an "is anything queued" gate is already empty by the time the second
  one arrives, and the batch stacks into one slide anyway.
- **Chips are deduped on `LootRollEntry.DomId`.** An `EventSource` reconnects on any blip — a sleep,
  a proxy timeout, a deploy — and the server answers by replaying its whole ring. That id existed
  for exactly this, and its doc comment claimed the ticker keyed on it while nothing did; a partial
  replay put the same roll on the banner twice.

**THE QUEUE HOLDS WHILE THE TAB IS HIDDEN, and drains when it comes back.** A background tab does not
paint and its timers are throttled hard — Chrome to one second, then to one *minute* after five
minutes hidden — so a ticker that keeps releasing spends its backlog on slides nobody sees, at a
cadence nothing is honouring. `schedule()` refuses to arm while hidden and `visibilitychange` cancels
any timer already armed; coming back re-arms it. Nothing else changes: rolls keep arriving into the
queue while away, capped at `maxQueued` as always, so what survives a long absence is the newest 40
rather than the oldest.

The resume needs no catch-up logic, and that is worth knowing before adding some. The cadence is held
against the CLOCK (see above), so on return `lastReleaseAt + slideMs + gapMs` is long past, the first
chip is released immediately, and every one after it falls back into the normal spacing on its own. A
two-second alt-tab is therefore a no-op rather than a special case.

**The signal is VISIBILITY, not focus**, and the difference matters here specifically: this is exactly
the page people leave open on a second monitor while they play, and that window is visible-but-
unfocused for hours. Pausing on `blur` would freeze the main way the feed is used. Hidden means tabbed
away or minimised, which is the only state where nobody can be watching.

Production reads `document.visibilityState`; the tests inject `opts.isHidden`, because jsdom has no
way to make a document hidden. That seam means the default is not covered by the suite — it was
verified in a browser instead: six live rolls arriving while hidden left the banner untouched, and
the leader then changed once every ~2.2s on return rather than all at once.

The slide itself is a **transform on the track**, never a width on the chips: a prepended chip shoves
the row right by its own width, the shove is cancelled before paint and then released, so one
composited transform carries the whole row. It reads the COMPUTED transform, not the inline one —
inline is the target (`translateX(0px)`) the instant it is set, so a roll released mid-slide would
start from zero and jerk the row backwards. The DOM cap (`data-max-chips`) is
`ILootRollFeed.BacklogSize`: when it was smaller, every connect built chips, animated them and
destroyed them in the same breath. The file's `slideMs` must stay equal to `.roll-ticker-track`'s
transition duration in `app.css` — a test pins the two together.

**The slide ignores `prefers-reduced-motion`, and is the only thing in the app that does.** It was
honoured at first, and the result was a bug report: with Windows' animation effects off — an OS
setting, so every browser on the machine agrees — the chip appeared in place and only faded, which
reads as a flicker rather than as a gentler version of the same idea. There is no reduced form of
"this just arrived" that still says it, and the motion here is one ~100px horizontal nudge of a 34px
band lasting half a second, which is the mild end of what the preference exists to catch. The LIVE
dot is the other end — it loops forever — and still yields. `tests/js/roll-ticker.test.js` pins the
override, because restoring the guard would look like an accessibility fix and would put the ticker
straight back to where it was reported broken.

**Each character gets a colour, assigned in order and remembered.** `RollChipHues` — first come,
first served across twelve hues, held in a static map for the life of the process, deliberately the
same lifetime as the ring buffer so nothing on screen can disagree with it. Not a hash of the name:
a hash needs no memory but can collide, and on a clan this size two of five characters sharing a
colour defeats the point. The classes are ours (`.roll-hue-N` in `app.css`), not Tailwind utilities,
because computed class names are invisible to Tailwind's scanner. Unlike the profile charts'
`StackPalette` each hue carries a light/dark PAIR: those are fills behind dark text, these are small
semibold text, and a 400 that reads on the dark band is barely there on the near-white one.

**The ticker is seeded from the database at startup**, in the same pass as the swimlanes
(`LootFeedSeederService`). Its ring is in memory, so without that the banner is blank after every
restart until the clan's next kill. Two reads, not one: `ILootFeedRepository.GetRecentRolls` for the
kills, then `GetKillOrdinals` for their roll numbers — inlining the ordinal maths into the seed query
would be a third spelling of that rule to keep in step. `SeedBuffer` **replaces** rather than appends
(so a re-run cannot double the banner) and deliberately does **not** notify subscribers — anyone
connected would otherwise see the whole buffer animate in at once as if 40 kills had just landed.
The ticker's seeding is wrapped in its own try/catch: it must never abort the swimlanes' seeding.

**Imported records never reach the ticker.** A first sync with full history is thousands of kills
from months ago and a banner labelled live must not replay them. The feed damps imports by value;
the ticker excludes them outright.

**Kill ordinals are resolved once per batch, and both surfaces read the same number.**
`ILootRecordRepository.GetKillOrdinals` does the whole batch in one round-trip;
`GetKillOrdinal` (two round-trips — the count and the admin baseline) is no longer on the publish
path. That was up to 500 queries for a 250-record sync batch, and the ticker needs an ordinal for
every kill rather than only the ones valuable enough to publish. Two spellings of the "roll number"
rule would drift and the ticker and the feed card would disagree about the same kill, so
`LootIngestHandler.ResolveOrdinals` is the only caller and hands the result to both.
`KlavLor.IntegrationTests/KillOrdinalBatchTests.cs` pins the batch resolver against the single-record
one, plus the same-timestamp tie-break, the baseline, and per-character independence.

**The `sse` permit count moves with the number of streams a feed page opens.** It went 20 → 24 when
the ticker was added, because the policy is a per-IP *concurrency* limiter and the page went from
five sockets to six — leaving it at 20 would have silently cut a viewer from ~4 tabs to ~3. Any new
long-lived stream on this page has to do the same arithmetic.

A roll published between the backfill snapshot and the subscription is missed. That window is
microseconds, and unlike the lanes — where a missed drop is a hole in the history — nothing reads
back through a ticker and nothing is derived from it, so it does not get the interleaving the
swimlanes need.

### The Loot Feed Loads Its Swimlanes After First Paint

The feed page route (`GetPage`) and both routable feed pages are deliberately **query-free and synchronous** so the shell paints without a DB round-trip (~15ms / 7KB, versus ~1.2s when it was server-rendered). `LootFeedContent` renders skeleton columns plus `hx-trigger="load"` on `#feed-grid-container`, which then fetches `GetGrid`.

That one grid response carries **both** halves of the feed together — the backfill entries and the `sse-connect` attributes — so history and live streaming arrive in the same swap and htmx opens the EventSources as it processes the new nodes. Keep them together: splitting them would open a window where published drops are missed. Do not reintroduce a handler on the page route.

The saved tier filter is appended by site.js's `htmx:configRequest` hook (it matches any `/api/loot/feed/**/grid` request), so the initial fetch is already filtered and `initFeedFilter` must NOT re-fetch — that would double-request and re-open every stream.

**The filters live in the URL as well as in localStorage.** `?tiers=rare,epic` and `?characterId=42` on the feed page (same names as the API params, so page URL and grid request read alike). A present param WINS over localStorage — a link someone sends must beat your own last choice — and an absent one means "no opinion", never "clear", because an in-app HTMX navigation pushes `/loot/feed` with no query. Writes use `replaceState`, so Back leaves the feed rather than stepping through each checkbox. `?tiers=none` is the all-off state, and it is the reason `getActiveTiers` now distinguishes a saved empty list from nothing saved: the `configRequest` hook cancels a grid/lane fetch outright when no tiers are active, because the server reads an empty `tiers=` as no filter and would answer with every lane.

`StreamFeed` flushes an SSE comment (`: connected`) immediately. Without it the response head is withheld until the first drop, leaving the browser's EventSource in CONNECTING — indistinguishable from a failed connection, unable to fire `onopen` or detect a dead socket.

### Luck Maths: One Path Only

`SourceLootService` is the **only** place expected kill counts are computed. Never derive a rate from `numerator`/`denominator`/`rolls` at a call site — that bug shipped once in the (now deleted) progression auto-completer and made the same drop read "dry as the desert" on one page and "lucky" on another, because the hand-rolled maths skipped raid unique-table scaling and admin rate modifiers.

- `ExpectedCompletions(...)` returns expected KC; `EffectiveRate(...)` also returns the display string (`"1/540"`).
- **Admin rate modifiers are a global baseline.** They are applied inside the facade, so every surface — collection log, character/source page, luck leaderboard, live feed cards, global source and drop pages — must read its rate through it. Rate columns render `EffectiveRarity`, not the raw stored `Rarity`, so an override or model-derived rate is visible rather than silently applied.
- **Depth-modelled sources are scored per run, never from an aggregate depth.** Doom of Mokhaiotl rolls loot at every delve level a run clears, so `SourceCollection.Runs` carries the derived depth of *every* actual claim and `ExpectedCompletionsForRuns` sums the per-run probabilities: `expected runs per drop = runs / Σ P(item | depth_r)`. An earlier version used the character's max-ever depth, which scored shallow runs as if they had all been deep delves and reported everyone as dry. An obtained item is windowed to the runs up to its first receipt (`CollectionEntry.FirstRecordId`); missing items use every run so far. Global (all-players) pages have no run to attribute, so they show no rate for depth-modelled sources rather than assuming a depth.

**Board entry is one rule, ranking is one number.** Any item past its expected roll count qualifies for the dry board — obtained or still being chased, no separate bars — provided it clears the rarity floor (`LuckScore.MinExpectedRollsForBoard` = 100 expected rolls, or a single receipt worth 100k+). Rarity is measured as `ExpectedKc`, never `RarityDenominator`: the latter is 0 for a depth-modelled source and ignores multi-roll tables.

`LuckScore.For(multiple, expectedRolls)` is the sole ranking key, and `GetBoard` orders by it. It exists because the two things that make a streak notable pull apart: improbability depends **only** on the multiple (2× dry is ~13% on a 1/1000 and on a 1/5000 alike), while grind size depends on rarity. Ranking on either alone is wrong — the multiple ignores a 10,000-roll grind, and rolls alone puts a mundane 1× on a rare item above a 5× on a common one. The score is `multiple^1.5 × expectedRolls^(0.316 + 0.02·ln expectedRolls)`; the rarity exponent *grows* with rarity so a 1/5000 is weighted harder than a 1/1000, and `RarityGrowth` is the one tuning knob. The `1.5` sits at the boundary where extreme streaks still hold the top of the board — raise it and the rare-grind preference inverts.

There is deliberately no synthetic ranking multiple any more. The old "rare grind" floor overwrote `Multiple` with `denominator/1000`, which forced the results view to recompute the true ratio for display; `Multiple` is now always the honest figure.

**A depth-modelled source is quoted in delves on the board.** Both `ObservedKc` and `ExpectedKc` are multiplied by the run's average depth, so `Multiple` is mathematically unchanged — `count/expectedRuns` equals `(count·d)/(expectedRuns·d)`. What changes is the unit (a delve is what Doom's rates are per) and therefore the rarity weight `LuckScore` applies: an Eye of ayak becomes a ~1,600-delve grind rather than a ~200-run one, which is what gives Doom uniques standing proportionate to the time they take. `ScoredInDelves` on the entry tells the view which word to print, so no consumer branches on source name. Note the *luck ratio* is still runs-vs-runs everywhere else (see the rule above) — this is a units change on one surface, not a second scale.

**A raid unique-table share is identified by ITEM NAME first, denominator second.** `RaidUniqueShareStrategy` scales a share ("given a unique dropped, which item is it") by the raid's average completions per unique; a tertiary (pet, dust, thread, kit) is already per-completion and passes through. It recognises a share two independent ways — the item being on the raid's declared unique list, or its denominator matching a known table weight — because each covers the other's silent failure:

- In August 2026 the wiki restructured the CoX table from `x/69` to `x/60` (normal) and `x/56` (challenge mode). Our code did not change; the hourly drop-rate sync stored the new numbers, the denominator-only test stopped matching, and every CoX unique quietly reverted to its raw share — a twisted bow reading **1/30 raids instead of ~1/960**, on the leaderboard, every rate column and every feed card. Nothing failed, nothing logged, and no test noticed, because every test pinned the denominator it asserted about.
- The denominator list covers what the name list cannot: an item being renamed, or a new unique appearing on an existing table.

Item names are matched **case-insensitively** — three vocabularies reach this maths and they disagree on case (the wiki's drop rows, RuneLite's drop names, and the collection log, which spells it "Scythe of vitur (uncharged)"). `ISourceLootStrategy.ExpectedCompletions` takes the item name for exactly this reason; do not drop it. `KlavLor.UnitTests/RaidAndDefaultStrategyTests.cs` pins each unique at the shares the wiki publishes today **and** pins that every declared unique still scales on a denominator no strategy knows about.

Note the mode variants (`Chambers of Xeric Challenge Mode`, `Theatre of Blood Hard Mode`, `Tombs of Amascut Expert Mode`) have no registered strategy of their own, so a record stored under one of those source names gets no share scaling.

**Both sides of a luck ratio are RUNS.** `ExpectedCompletionsForRuns` returns expected *runs*, so every observed figure compared against it must be a run count too — never a delve total. This has been got wrong twice, on the live feed card and on the leaderboard's obtained-item branch (which summed a window's depths and so reported every Doom drop as depth-times drier than it was). `KlavLor.UnitTests/FeedCardDepthTests.cs` pins the scale.

**A feed card rates a FIRST receipt only, and `FeedLuckRules.ShouldRate` is the whole rule.** Every reason a drop gets no lucky/dry line lives in that one method — not a collection-log item, not the character's first receipt (`LootDrop.IsFirstTime`), admin-excluded at the record level, no usable rate, or too common to judge (`WorthRating`). It sits in the Application layer specifically so it can be unit-tested; `LuckLabel` in `LootFeedItem.razor` is markup and no test can reach it. When a drop isn't rated the **whole line** goes, never just the verdict: a bare rate and roll number are noise on their own.

Repeats are excluded because a luck figure answers "how long did this take to arrive", and only a first receipt has an answer. That also means the roll it landed on *is* the gap — every roll at that source was spent waiting for it — which is why there is no longer a "rolls since the previous receipt" query. The old `RollsSincePrevious` and `GetRollsSincePreviousReceipt` existed to give a repeat an honest denominator (judging one against its absolute position reported a second 1/100 item at roll 200 as "2x dry" when the player had gone 150 rolls since the last one); with repeats unrated they had no consumer left and were removed. Restoring repeat ratings means restoring that gap query — never judge a repeat against its absolute roll number.

**An admin can take one record out of the luck maths without deleting it.** `LootRecord.ExcludedFromLuck`, toggled per row in the admin record-audit panel (`/admin/settings/record-audit`). It is for a receipt that cannot be rated honestly rather than a kill that never happened — a crystal armour seed logged against Hunllef — where deleting the record would throw away a real kill to silence one bad figure. Deletion remains the tool for a record that is wrong in its entirety.

The semantics are deliberately asymmetric, and `KlavLor.IntegrationTests/RecordLuckExclusionTests.cs` pins them:

- The record still counts as a **roll**. The kill happened; only the attribution of what fell out of it is disowned. `GetSourceCollection`'s `runs` list is left unfiltered for exactly this reason.
- Its **drops stop being receipts**. The one filter that achieves this is `AND NOT lr."ExcludedFromLuck"` on `GetSourceCollection`'s `unrolled` CTE — the single query behind both the luck leaderboard and the character page's collection panel, so the two cannot disagree about which receipts count.
- An item whose **only** receipts are excluded is neither obtained nor being chased. The missing-items query is deliberately *not* filtered, so the item does not reappear as an ongoing dry streak for a drop the player has actually had.
- On the feed the drop keeps its value, tier and chip; only the luck line goes, via `LootFeedDrop.ExcludedFromLuck` (carried from `FeedTierProjection`) and `ShouldRate`. A grouped chip standing for several receipts is silenced if **any** of them is excluded — half a verdict is worse than none.
- Toggling invalidates exactly what a delete does and calls `RecomputeTrigger.LuckInputsChanged()`, so the board rebuilds within ~60s.

**Only items of 1/6 or rarer get a lucky/dry verdict** (`FeedLuckRules.WorthRating`, one of the conditions `ShouldRate` checks). Below that, ordinary variance renders as a lurid multiple. The threshold reads **expected rolls** from `SourceLootService`, never the raw stored denominator — that is precisely what keeps raid uniques rated and is why Chambers of Xeric, Tombs of Amascut and Theatre of Blood need no special case: a CoX prayer scroll is stored as 12/56 (which as a bare fraction looks like 1 in 4.7 and would be filtered out), but it is a share of the unique table and `RaidUniqueShareStrategy` has already scaled it to ~149 raids by the time the feed sees it. `KlavLor.UnitTests/FeedLuckRulesTests.cs` pins this; `KlavLor.UnitTests/FeedLuckShouldRateTests.cs` pins the other four conditions.

**Feed tiers are per drop, everywhere.** Anything that classifies an item into a swimlane must use the value of a single receipt, never a running total — `LootDropSummary.BestDropValue` exists for exactly this, so 500 cheap drops summing to millions can't read as a legendary. Always classify via `ILootFeedService.GetDropTier` rather than re-hardcoding thresholds; the character/source page's drop grid and the live feed cards share it.

The one place a card's TOTAL is consulted is `ILootFeedService.ExceedsTier`, and it is not an exception to that rule: it decides *presentation only*. A card whose total outgrew its lane's ceiling — three 90M drops from one source merge into one Epic card worth 270M — is marked in **its own** tier colour (`.tier-overflow` plus a `.tier-overflow-{tier}` hue variable in `app.css`, driven by `GetTierOverflowClasses`). The cue is **a still, faint tint of the lane's colour across the card body, and nothing else** — no pulse, no glow, no ring, and the border is left exactly as the tier gave it. It got there the long way round: brightening the border alone was invisible (every card in a lane already has that colour there), a detached ring with a halo read as a double border and bled into the neighbouring swimlanes, and turning the brightness down twice still left it shouting, because what shouted was the MOTION. This cue lands on roughly a fifth of the cards on a feed page, so it has to be readable when you look at a card rather than visible from across the page. Differ from a neighbour in **area**, never in brightness or movement; if it needs strengthening, raise the tint alpha rather than reintroducing either. The card is never promoted, so cheap drops still cannot fake a rarer lane; they can only make the lane they are in glow. Always false for Legendary, which has no ceiling. It yields to `.legendary-card` and `.giga-card`, which animate the same border — they can't collide in practice, since both a 250M+ drop and an injected special classify as Legendary, but the razor states the precedence rather than relying on stylesheet order. `KlavLor.UnitTests/LootFeedTierClassificationTests.cs` pins the boundaries and the "total never changes the lane" property.

**An injected special gets the card ring, not a second bolt.** `.giga-card`'s spinning cyan-violet ring is the whole effect for an `IsSpecial` drop (Infernal cape in production). The pill inside used to carry its own SVG lightning border too, which competed with the ring for the same attention; it and the `#giga-electric` filter defs are gone, and `.giga-item` is now enlargement only — so the chip keeps its ordinary tier border, which the bolt had suppressed. The 250M+ `legendary-item` bolt is untouched: it is the only lightning left, and it is on the pill rather than the card.

### Item Values: DropsJson Is Raw, The Projection Is Effective

Some genuinely valuable drops are untradeable and so have no Grand Exchange price — the Noxious halberd's three components are worth ~10m each and RuneLite reports every one of them at 0 GP. `ItemValueOverride` lets an admin set a flat intrinsic value per item id, applied through `IItemValueOverrideCache` (singleton, immutable-snapshot swap, primed in Program.cs before the feed seeder — same shape as `ISourceRateModifierCache`).

It is a **global, timeless** override, deliberately not a price history: setting one re-values every past and future receipt of that item. It carries no special-casing downstream, so it flows through ordinary tier classification — 10m lands the drop in Epic, 100k in Uncommon. This is **not** the same thing as `LootDrop.IsSpecial`, which stays what it is: the zero-value admin-injected giga drop for genuine one-offs. The two compose (a special-injected item with a value gets that value) but `IsSpecial` still owns the Legendary lane.

The invariant that makes it consistent:

- **`DropsJson` keeps the RAW RuneLite price and is never rewritten.** It is the canonical record, and it is what makes an override reversible — removal re-derives straight back from it.
- **`LootDrops.Price` and `LootRecords.TotalValue` are the DERIVED projection and hold the EFFECTIVE price.** Every SQL read site therefore needs no change at all, which is why this design was chosen over materialising a parallel `EffectivePrice` column across ~40 query sites.
- **Every site that deserialises `DropsJson` and then looks at a price must call `IItemValueOverrideCache.WithEffectivePrices`.** That is `LootIngestHandler` (both the publish check and the live card), `LootFeedRepository` (`CollapseProjections`, `CollapseDay`), `LootProfileRepository` (biggest kill), `LootSessionRepository` (session kills) and `LootSourceDetailRepository` (notable drops, paged kills, source-session kills). Miss one and the same drop reads one way live and another way after a refresh — the bug class already called out for Doom's depth maths. Sites that only read names and quantities (`LootLogSearchRepository`, `SourceLootService.ParseClaim`, `LootDerivationBackfillService`) correctly do not.
- **Every write re-primes the cache, then re-derives.** `ItemValueOverrideAdminHandler` persists, calls `cache.Replace`, then `RebuildForItem`, which re-prices `LootDrops` from `DropsJson` in bounded batches and rolls `LootRecords.TotalValue` back up with a set-based raw UPDATE (no audit or RowVersion churn — `TotalValue` is derived, not a user edit). Set, change and remove all run the same pass, so it is symmetric and idempotent. It then invalidates `LootStatsCache`, `GlobalSourceCache` and `GlobalDropCache` for exactly what the rebuild touched.
- **Every write also reseeds the live feed buffer** (`FeedBufferSeeder.Reseed`). The swimlanes are an **in-memory buffer, not a query**, so nothing above reaches them: re-priming a cache and re-deriving the database fixes every surface that reads on request and leaves the feed exactly as it was. This shipped broken. An untradeable is reported at 0 GP, so it is under the feed's 10k floor and never enters a lane at all; setting a value fixed the database — so a page load showed every past receipt — while the buffer still held nothing for them. The next live kill at that source merged against the stale buffer and broadcast a card carrying only itself, which read on screen as the card *refusing the new item*: its roll count and KC range climbed (ordinals are resolved fresh on every publish) while its chips and total stood still. A restart "fixed" it, which is what a stale in-memory buffer always looks like from outside. `KlavLor.IntegrationTests/FeedBufferOverrideTests.cs` drives the real handler, so deleting the call fails the suite.
- **`RebuildDropsForCharacter` must re-apply the override too.** It rebuilds the projection from the canonical `DropsJson` — and *equal to* `DropsJson` is not *copied from* it, because the JSON holds the RAW price by design. A straight copy silently reset every overridden item to the figure it had been overridden **for** (measured: a record left with `TotalValue` 5,000,000 and `LootDrops.Price` 0), for the **whole character**, on any imported batch or special-drop injection — long after the admin had set the value and watched it work. It carries `IsSpecial` across for the same reason: the legendary lane finds injected specials by querying that column, and `SpecialLootHandler` calls `RecomputeFirstTimeFlags` immediately after writing the flag, which un-wrote it on the next statement. `KlavLor.IntegrationTests/ProjectionRebuildTests.cs` pins both.

`KlavLor.UnitTests/ItemValueOverrideTests.cs` pins the cache and the tier consequence; `KlavLor.IntegrationTests/ItemValueOverrideRebuildTests.cs` pins the rebuild and the restore-on-removal against real SQL.

### "Is This A Collection-Log Item" Is ONE Rule, Asked In Four Places

`ICollectionLogCache.IsCollectionLogItem` matches on **item id OR name**, case-insensitively, and the name half is not a nicety: the id RuneLite reports is not always the id the wiki sync recorded (variants, renames, an untradeable logged with no usable id), and the name is what survives that.

**Every SQL site that asks the same question must ask it the same way.** Two did not, and matched on id alone:

- `GetSourceCollection`'s drop-events query, which fills the KC column's hover popover. An item that qualified by NAME appeared in the table as received and then had its KC cell render `cursor-help` over an **empty** popover — the "?" pointer with no tooltip behind it, reported from production.
- `GetSourcePopover`'s unlocked count, which then reported "1 of 3" while the table underneath it listed two items as received.

Both now use the same **two separate `EXISTS`** the entries query uses — split rather than one `EXISTS` with an `OR` inside, because the `OR` blocks the `ItemId` PK index and forces a full clog-view scan per drop; separately each half uses an index (`ItemId` PK, `lower(Name)` expression index) and the id path short-circuits the common case. `KlavLor.IntegrationTests/SourceCollectionClogMatchTests.cs` pins both, plus an id-matched control so the fix cannot trade one for the other.

The panel also carries an on-request "Find items with no value" report (`FindZeroValueItems`), which is how you discover what needs an override. It is a full scan of the drop table grouped by item, filtered to `MAX(Price) = 0`, so it is deliberately never given a load trigger — the admin has to press the button. Collection-log membership is stamped from `ICollectionLogCache` rather than joined, and sorts those items to the top, because a clog item at 0 GP is the signal and everything below it is usually junk.

### Superior Slayer Monsters Are A Static Registry, Not A Table

`/loot/superiors` compares every tracked character's kills of each superior slayer monster.
`SuperiorSlayerMonsters` (Application/Features/Loot/Superiors) is the whole catalogue — name, base
monster(s), Slayer level, combat level — and it is **code, deliberately**: 38 rows of reference data
that change only when Jagex ships an update, which is itself a code change. A table would need a
migration, an admin panel and a sync job to hold a list nobody edits. Same reasoning as the
hardcoded raid unique lists in `RaidUniqueShareStrategy`.
`KlavLor.UnitTests/SuperiorSlayerRegistryTests.cs` pins the count, the ordering, the level ranges and
the absence of name collisions.

**Case-insensitive matching needs EXPRESSION INDEXES, and it did not have them.** Every name match
here is `lower(x) = ANY(...)`, and a plain btree on `"SourceName"` cannot serve a `lower()`
predicate — so these queries fell back to sequential scans. Measured: `GetCounts` filtered 26,732
rows off a Seq Scan of `LootRecords` and the receipts query filtered another 39,810 off `LootDrops`,
143ms of query time on ~29k records, both scans growing with the table.
`IX_LootRecords_SourceNameLower` and `IX_LootDrops_NameLower` (migration
`AddLoweredSourceAndItemNameIndexes`, hand-written SQL because EF cannot model an expression index)
took that to **24ms** — counts 19→6ms, base kills 4→0.1ms, receipts 120→18ms, with every one of
those scans now an index or bitmap scan. The case-sensitive indexes stay: plenty of queries still
match a name exactly.

**Names are matched case-insensitively, and that is not optional.** Three vocabularies produce a
source name and they disagree on case for about a third of the list — the wiki's article title
("Colossal Hydra"), the wiki's own summary table ("Colossal hydra"), and whatever RuneLite reports
for the NPC. Both queries filter `lower("SourceName") = ANY(@names)` against the registry's lowered
lists; a case-sensitive match would silently split one monster's kills across rows, or drop it
entirely. `Name` stores the in-game name (verified against each monster's wiki infobox `name`, not
the summary table) purely for display. The `Aliases` field is empty today and exists for the one
failure a lowercased match cannot survive: a rename.

**The shared unique table is why the page is ordered the way it is.** Every superior, level 5 to
level 95, rolls the same table, and the chance of hitting it is `1 / (200 - (slayerLevel + 55)^2 /
125)` — so a Colossal Hydra (1/20) is worth about eight and a half Crushing hands (1/171).

**THAT FORMULA IS DELIBERATELY NOT COMPUTED, and the reason is a domain fact rather than laziness.**
It gives a BASE chance per Slayer level, but a Slayer master's bonus moves it substantially and
**nothing in a loot record says which master a kill was on** — the ingest payload has no field for
it and never will. Any weighted figure would therefore be a precise-looking number nobody can stand
behind.

It was computed, briefly: `SourceLootService.SuperiorUniqueChance` fed a per-row rate and a
per-character "expected rolls" total. Both were removed once that was pointed out. If it is ever
wanted again the blocker is the missing master, not the maths — and the honest version would have to
carry a visible caveat, because the error is not small.

**Hardest first, and only monsters someone has killed.** The registry is stored ascending because
that is how a reference list is naturally written and maintained; `SuperiorSlayerHandler` reverses it
and drops any row with no kills behind it. Display order is the page's decision, not the registry's.
The two ends are pinned separately: `SuperiorSlayerRegistryTests` on the stored ascending order,
`SuperiorSlayerComparisonTests` on the handler's reversal and filtering.

**Each cell shows the player's own base-monster kills under their superior count** (`68` over
`from 12,920`), summed across both bases where a superior has two. It is **per character, never a
roster total**: superiors only appear while killing the base, so this is the grind each player's
count sits on top of, and one shared figure could not say whose grind it was.
`GetBaseMonsterKills` UNIONs tracked `LootRecords` with `CharacterSourceBaselines` grouped by
(character, monster). The UNION rather than a `LEFT JOIN` matters: for an ordinary slayer monster a
baseline with no records at all is the common case, since nobody's loot tracker logged ten thousand
Gargoyles. Zero renders as nothing, never as "from 0" — untracked and none are not the same fact.
The wording is **"from N", not "of N"**: 68 superiors turned up over the course of 12,920 Hydra, and
"of" read as a fraction of a total. The monster it is *from* is named once in the row header rather
than repeated in every cell, because it is a fact about the row, not about the player.

Kills of the superior itself use the canonical definition, `GREATEST(MAX(KillCount), COUNT(*) +
baseline)`, matching `LootSourceDetailRepository.GetSourceCollection`. Both halves are near-always
moot for a superior, but sharing the definition is what stops this page and the character's own
source page quoting different numbers.

The page is `.AllowAnonymous()`, which **differs from the house rule** stated on
`CollectionLogEndpoint` that cross-character comparison surfaces are clan-internal. That is a
deliberate exception, recorded on the endpoint: it exposes kill counts and nothing else, and it sits
in the public sidebar, where an authorization policy would 401-redirect signed-out visitors.

**THE PAGE PAINTS BEFORE IT QUERIES.** Three routes, not one: `/loot/superiors` serves a query-free
shell, and `/loot/superiors/table` and `/loot/superiors/receipts` each fetch themselves on `load`,
in their own request scope. The routed page injects no handler at all. It used to render everything
during SSR, so nothing appeared until every query had run and **239KB** of markup had been built —
measured at 1.25s on a cold process. The shell is **20KB**, both halves start within 0ms of each
other, and the whole band is populated 595ms after navigation on a cold process.

Both halves read the SAME cached aggregate (5-min TTL keyed off `AggregateCacheGeneration`), so the
pair costs one set of queries: whichever arrives first fills the entry and the other hits it. The
receipts half asks for the DEFAULT sort deliberately — sorting is applied after the cache and only
reorders the table, so passing the sort through would be a second cache key for identical receipts.

**A sort re-fetches the table alone.** The header links `hx-get` the table route and target
`#superiors-table`, while `hx-push-url` pushes the *page* URL — so the address bar stays linkable
and the receipts beside it, which no ordering affects, are not re-rendered to change one. Verified:
clicking a character header fires exactly one request and leaves the receipts DOM node untouched.

Each half re-declares the `id` and layout classes of the shell's placeholder it replaces, because
the swap is `outerHTML` — if they drifted, a panel would land in a differently-shaped box than the
skeleton it replaced.

Note `AggregateCacheGeneration.Bump` is called from **one** place, `CollectionLogAdminHandler`. Loot
ingest does **not** invalidate this page; it goes stale for up to the 5-minute TTL after a kill.

The columns are Superior, one per character, Clan. **Clan totals each row**, which the
per-character totals could not: "how much has the clan killed of this one" was a question the table
held every number for and could not answer.

**TIGHT COLUMNS, AND A SHARE BAR THAT TAKES THE REST.** The layout has been three other things and
each failed the same way — the width was spent on padding rather than on content:

- **Fixed columns plus an empty trailing spacer.** A third of the page blank.
- **Two half-width blocks side by side.** Filled the width by cutting the comparison in half, and a
  comparison you read in two places is not one.
- **Percentage columns stretched to full width.** Exactly what the original note warned of: it did
  not remove the gap, it moved it inside the cells, leaving a two-digit number adrift in a 326px
  column. Measured, **6.8% of the table's area had any text on it**.

So the counts get only the width they need, and the bar column is declared with **no width at all** —
under `table-fixed` an unsized column absorbs the remainder, so the bar grows with the window, the
table meets both edges at any size, and the extra pixels carry information instead of air. Ink plus
bars now covers 18.5% of the table against 6.8% before, and rows dropped 47px to 38px by putting
each count and its "from N" on ONE line ("68 from 13k", exact figure in the tooltip).

**THERE IS NO CHART COLUMN, and the reason is the most useful thing recorded about this page.** That
column was, in turn: an empty spacer, a share-of-kills bar, a unique-table-rolls bar, a clan-kills
bar, and a weekly activity sparkline. Every one of them was chasing the same problem, and the same
fact rules them all out:

> **Superior counts and base-monster counts are the same number.** r² between them is **0.9997**
> across 134 filled cells, and the scatter is *half* the Poisson noise real sampling would produce.
> Nobody's loot tracker logs ten thousand Gargoyles — for the five commonest bases the tracked count
> is literally **0** against **92,678** from baselines — so those base figures are admin estimates
> back-calculated from the superior counts at about **190:1**. Every magnitude on this page is one
> quantity wearing different clothes.

Measured against the live data: share of kills gave 26 distinct shapes across 38 rows; superiors per
1,000 base kills gave a 1.1× spread, because it *is* the constant; active timespan covered a median
97% of its axis. Clan kills varied 10×, but that is the Clan column drawn twice. Unique-table rolls
varied 20× and was the most interesting of them — and is **not assertable at all**, because a Slayer
master's bonus moves the true chance and no loot record says which master a kill was on.

**So the receipts segment took the column's place.** `SuperiorUniquesPanel` sits FLUSH against the
table — no page padding, no gap, no card, just the divider — and occupies exactly the width the
chart column used to. That matters: the table is sized to the sum of its own columns
(`TableWidth`, not `w-full`) so it claims what it needs and nothing more, and the segment takes the
remainder. When the table was left to stretch, the last column swallowed the space the chart had
held and Clan became a quarter of the page.

It lists every unique-table receipt, newest first, with the character, the source, the kill it
landed on and the date. It is the only content on the page not determined by that constant: a receipt
is a rare event with real variance. Each entry names its source, which is exactly what a per-row
column could not do — the feed reads as the clan's history rather than one monster's footnote.

**It is drawn as a COMMIT HISTORY**, after PropelVulnerabilityTracker's `ScanHistoryTimeline`: a
vertical rail with one node per receipt, grouped under month dividers that carry their own count, so
a quiet month reads as quiet rather than merely short. **The node is the item's own icon**, which is
what makes the column skimmable for "what fell" without reading a line of it — a ring of coloured
dots would need a key. The two rare ones (Imbued heart, Eternal gem) get an amber ring with a halo
and an amber card; the battlestaves stay plain, because giving them equal weight would make an Imbued
heart look like a Tuesday.

**THE BAND'S HORIZONTAL RULES ARE DRAWN ONCE, BY THE CONTAINER.** This is a `<table>` beside a
`<section>`, and every attempt to make their header rules meet by giving each half its own `border-y`
failed by a pixel — a `<th>` whose borders are halved and shared under `border-collapse`, against a
plain header whose borders sit inside its own box. The rules landed a pixel apart and the timeline's
edge stepped over the table's. Two rounds of pixel corrections each fixed it for one layout and broke
it for the next, because the correction depended on what sat above the band.

So neither half draws them. `.superior-band` carries two absolutely-positioned pseudo-elements
spanning the full width — one at the top, one at exactly `--superior-head-h` — and the headers keep
only their background. **One element per rule, so there is nothing for the two halves to disagree
about.** Measured after: both header boxes start and end on the same sub-pixel, delta 0.000.

Both headers are still pinned to `--superior-head-h`, because the rule is drawn at that height and
the backgrounds have to reach it. The table's is a `height` on a `<tr>`, which CSS treats as a
minimum, so a header that outgrows the figure pushes the row rather than clipping — the halves then
visibly disagree, which is the right way for this to fail. Below `xl` the two stack, and the
header-height rule is switched off: side by side it is one line across two headers, stacked it would
cut through the middle of the timeline.

The rail has to sit on the node centres or it reads as a misprint, and that offset is now **derived
rather than measured**: `.superior-rail` is `gutter + half a node`, and both the item nodes and the
month dividers sit in the same `.superior-node-slot`, so the line lands on their shared centre by
construction. It is also the **last** child of the timeline, deliberately: as the first child it took
`:first-child` away from the opening month divider, so that divider kept the `mt-4` meant only for the
ones after it and its dot sat 16px below the top of the rail, leaving the line poking up into the
padding. Absolute positioning ignores DOM order and the nodes carry `z-10`, so moving it costs
nothing. The month dots used to place themselves with their own `ml`, measured from the content
box while the rail is measured from the border box — one page gutter apart, so they sat 16px to the
right of the line they were supposed to be on, every time.

A receipt row is a **grid** (`.superior-receipt`), not a flex row. As flex — three fixed widths and a
`flex-1` — the source cell was 506px holding about 120px of text, so every line had a hole in it and
the dates floated alone at the far edge; fractional tracks spread the surplus across all four columns
instead, which is what makes columns read as columns. The tracks floor at **0, not at their content
width**: a `minmax(9rem, …)` floor reads better on a wide screen and pushes the page into a horizontal
scroll on a narrow one (measured, a 514px row inside a 379px box at a 465px viewport), and the page
body must never scroll sideways. Below 40rem the row folds to two columns rather than four slivers.

**The history shows RECEIPTS, never kills.** The table beside it already says how many superiors
everyone has killed; a log of kills here would be the third spelling of one number. Two versions that
did exactly that were built and reverted — a daily contribution heatmap (`6bbe931`) and a
(day, character) commit log of superior kills (`0db9275`). Both were the right shape for the wrong
quantity. What belongs in this column is the payoff and the gaps between the payoffs.

Characters are named in the live ticker's colours (`RollChipHues`, a process-lifetime map, so a name
is the same hue on both surfaces). Those classes set a **custom property** (`--roll-name`) rather than
a colour, so that `.roll-chip-name` can keep its slate default through the var() fallback — which
means a second consumer needs its own one-line rule to spend it. That rule is `.roll-name-text`;
without it every character renders in the inherited colour and the assignment silently does nothing.

The **kill ordinal** (`#60`) is the character's Nth kill of that superior when it dropped, a
correlated count plus any admin baseline — the same definition the rest of the site uses for a roll
number. It is a fact, not a rate: "their 60th Nechryarch" says nothing about what the odds were.

**THERE IS NO SUMMARY BAND, and there should not be one.** The page opened with five figures —
superiors met, clan kills, unique drops, characters, latest unique — first as a 76px gradient banner,
then as a 37px inline stat bar. Both were removed, and the reason the second was no better than the
first is that shrinking it never addressed the objection: **every figure in it is already on the
page.** Superiors met is the number of table rows. Clan kills is the Clan column's sum. Unique drops
is the timeline's own "N received". Characters is the number of character columns. The latest unique
is the timeline's first entry. A band that restates the page above the page is padding however
elegantly it is set, so the page now opens on the header row. Do not add it back.

**Each column header also carries that character's cumulative base-monster total** — every ordinary
monster they have killed that can spawn a superior, in the same "from N" wording the cells use, so
the two read as one figure at two scales. It is summed from the per-(character, base monster) rows,
NOT by adding up the table's rows: a superior can have two bases and the row figure already sums
them, so adding rows would double-count any base shared between two superiors.

**The table header is three lines, and each character carries their own colour** — the same
`RollChipHues` assignment the receipts timeline and the live roll ticker use, so a name is one colour
everywhere rather than three. It was three centred lines (name, kills, uniques) with a "no uniques
yet" placeholder holding the third line open for people who had none; kills and uniques now share a
line and the placeholder is gone; the base-monster total then took a third line back. That is what
sets `--superior-head-h`, so every change to it means re-measuring the token both halves of the seam
read from — and the failure is loud, which is the point: adding the base-kills line pushed the header
to 66.5px against a token pinned at 49px and the seam visibly stepped by 17.55px until the token was
re-measured to 4.1875rem.

**The hover card survives, moved onto the monster name.** Per character: kills, uniques, first and
last, and *never on task* shown distinctly from a zero — which the grid's dash cannot distinguish.
It is pre-rendered and hidden in the row, because every figure is already on the page; `site.js`
lifts it into a **fixed-position** panel, which it must, since the table's `overflow-x-auto` wrapper
is a scroll container and would clip an absolutely positioned one — the same trap that stops the
header being sticky.

There is no spacer column and no `tfoot`: the footer repeated the per-character totals the header
already carried, costing a row of height to say the same thing twice.

**Full bleed means cancelling the app gutter, not just declining a max-width.** `#hx-page-container`
carries `p-4`, so "no container" still left the table 16px off both edges, which on a page that is
one wide table reads as a mistake. `SuperiorsContent` has `-mx-4` to negate it for this page alone;
the table's own cell padding keeps text off the glass. The `overflow-x`
wrapper is a backstop for a very large roster only, because the page body must never scroll
horizontally.

The header is deliberately **not** sticky: the `overflow-x` wrapper is a scroll container, so a
sticky header inside it resolves against the wrapper rather than the viewport — `top-16` offset it
64px *down* from the table's own top instead of pinning it, leaving a blank band at scroll zero.
Making it stick to the page would mean dropping the wrapper.

**Every header sorts, and the sort lives in the query string** (`?characterId=42&asc=true`), so a
sorted view is linkable, survives a refresh and steps back through Back. It is applied **in memory,
after the cache** — every ordering shares one cached read, and because the sort key is a character id
rather than a column name there is no query to interpolate it into, which sidesteps the sort-column
whitelist problem the SQL-backed tables have. An unknown character id **falls back** to the default
ordering rather than throwing or emptying the table: the id comes off a query string, so a stale
bookmark or a since-hidden character is an ordinary thing to receive.

**`SuperiorComparison` carries the sort that was actually APPLIED** (`AppliedSort`/`Ordering`), and
the view reads it from there. The endpoint and the routable page used to build a `SuperiorSort` from
the query and hand it to the component alongside the rows, which let the two disagree: on a stale
bookmark the fallback ordered by level while no header said so, because the view was still holding
the character id that had been discarded. One object now carries both.

Each column header also carries **when that character last killed a superior**, because a large total
says nothing about whether it was earned last week or three years ago. Only the recent state is
coloured — tinting a stale one red would read as a fault rather than as someone who moved on.

Every count renders the same. There is no per-row leader highlight — it turned a set of facts into a
scoreboard, and the numbers are already side by side. Monster names are deliberately **not** links:
the global source page is behind the `User` policy while this page is anonymous, so a link would
401-redirect the visitors the page exists for.

### The Admin Area Is One Section Per URL

`AdminSections.All` (in `AdminSection.cs`) is the registry: slug, nav label, title, group, description. It drives the nav, the routable page and the shell endpoint together, so there is one list to add to.

- The page is `AdminSettingsTemplate.razor`, routed at both `/admin/settings` and `/admin/settings/{Section}`. The HTMX shell fragment is `GET /api/admin/settings/{section}`.
- `AdminSections.Resolve` falls back to the first section on an unknown or absent slug rather than 404ing — the nav is the only way in, so a bad slug is a stale bookmark.
- **Every panel-body endpoint must sit at least two segments deep** (`/admin/settings/item-values/panel`, not `/admin/settings/item-values`). A single-segment literal wins the match over the `{section}` parameter and would silently shadow the page. Seven routes were moved a level deeper for exactly this.
- Nav links set `hx-push-url` explicitly, because the fetch URL and the page URL differ by the `/api` prefix and `HtmxNavigationFilter`'s blanket strip can't derive one from the other. They also carry a real `href` so middle-click and JS-less loads work.
- Section bodies are components, dispatched by an explicit `switch` in `AdminSettingsHub.razor`. The common "body is one HTMX panel" case uses `AdminPanelLoader`; five sections with inline search boxes have their own `AdminSection*.razor`.
- Panels load on `load`, not on a `<details>` toggle — there are no `<details>` any more. A section with two independent loads staggers the second by 500ms (`AdminPanelLoader`'s `DelayMs`, or `load delay:500ms`), per the staggering rule above.

This replaced a single page holding all thirteen sections as collapsible `<details>` with an anchor nav: nothing was linkable, every section's markup shipped on every visit, and finding one meant scrolling.

### An Admin Edit That Changes A Luck Input Must Request A Rebuild

The luck leaderboard is precomputed hourly, but nearly every admin panel edits an *input* to it: a baseline kill count, a delve depth, a rate modifier, a source or item exclusion, the collection-log blacklist, an intrinsic item value, a source rename, an injected special drop. Before `RecomputeTrigger` existed, all of those left the board quoting the old numbers for up to an hour with nothing on screen saying so.

`RecomputeTrigger.LuckInputsChanged()` (Application/Features/Maintenance) is the single place that mapping lives. It flags a manual run on the existing poll-and-claim `IJobScheduleRepository` rather than recomputing inline — a rebuild walks every character and source, which has no business happening in an admin's request. The services poll once a minute, so it lands within ~60s, and the flag is idempotent, so ten edits cost one rebuild.

**A new admin panel that writes anything the luck maths reads must call it.** It is not auto-registered (it isn't a `*Handler`), so it has an explicit `TryAddScoped` line in `ApplicationDependencyConfiguration`.

### Progression Completion Is Manual Only

Template-node completion happens **only** when a user clicks a node in the viewer. There is deliberately no drop-driven auto-completion and no generated completion notes — that feature was removed, along with `Features/Progression/` and the `GetAutoCompletableNodes`/`AddCompletions` repository methods. Loot ingest must never write to `UserNodeCompletions`.

**A completion belongs to the TEMPLATE, not to whoever clicked it.** Despite the table being called `UserNodeCompletions`, every read and every write resolves to `template.CreatedById` — the owner's rows *are* the template's progress, which is why `ViewerDataHandler` loads the owner's rows for every viewer rather than the current user's. An **admin ticking a node or writing a note is doing it on the owner's behalf**, and that is intended: admins are the only other actor `ToggleCompletionHandler` lets through.

Keep the three sites in step — `ToggleCompletionHandler` (write), `ViewerDataHandler` (page read) and `CompletionEndpoint` (the read that renders the swapped-in fragment). They drifted once: the write targeted `currentUser` while the page read targeted the owner. For the owner those two ids are identical, so the bug was invisible to the person most likely to hit it; for an admin it was silent and total. The toggle *succeeded*, wrote a row under the **admin's** account, and the viewer then rendered the owner's rows, which had not changed — so the tick survived the htmx swap and vanished on the next load. It was reported as "the admin cannot check nodes", when in fact it was ticking a node nothing displays.

`KlavLor.IntegrationTests/AdminCompletionOnBehalfTests.cs` pins both halves against real SQL — the tick lands on the owner **and** nothing is written under the admin — because either half alone still looks right in the swap and wrong on reload. Note the write carries no record of *which* admin made it: `UserNodeCompletion` is a composite-key join row and does not extend `Entity`, so it has no `SavedById` audit trail. Adding attribution means a new column and a migration.

### Rate Limiting Policies

New endpoints must use one of these existing policies (applied via `.RequireRateLimiting("name")`):

- **login** — Per-IP: 5 attempts/min (anonymous auth endpoints)
- **mutation** — Per-user: 60 requests/min (node/edge/group/template CRUD, completion)
- **position** — Per-user: 300 requests/min (high-frequency drag updates)
- **loot-ingest** — Per-user: 120 requests/min (RuneLite plugin ingestion)
- **read** — Tiered by caller: authenticated 600/min counted **per user**, anonymous 240/min counted **per IP** (all read-only endpoints)
- **assets** — Tiered: authenticated 3000/min per user, anonymous 1200/min per IP (item/source icons, cached images)
- **upstream** — Per-caller: 30/min (routes that make a live third-party call — currently only the OSRS Wiki search)
- **sse** — Per-IP: 20 *concurrent* connections, no queue (SSE feed streams only)

`read` is one policy with two partitions rather than two policies, because the public read surface serves both kinds of caller: the same route is hit by a signed-out visitor and by a logged-in user, so a call site cannot choose in advance — only the request can. A signed-in user is identified, attributable and revocable, so they get a generous budget counted against their own account; anonymous traffic can only be identified by a possibly-shared address, so it gets the tighter one counted per address. The flat per-IP limit it replaced punished the wrong people: several signed-in users behind one NAT shared a single 120/min budget while an abusive anonymous client on its own address was unaffected.

Partition keys are prefixed (`u:` / `ip:`) so a user id can never collide with an address. The anonymous fallback on the per-user policies is **per-IP, not a single shared bucket** — the old `?? "anonymous"` fallback put every unauthenticated caller in one partition, so one of them could exhaust the budget for all the others.

`assets` is separate from `read` purely because of volume: those routes serve one request per `<img>`, and a single collection-log or search view paints hundreds, so a shared budget would be exhausted by one page. `upstream` is the opposite case — trivial work, but each request makes us call someone else's server, and being blocked there breaks item images site-wide, so it is far tighter than the cost suggests.

**Every mapped route carries a policy.** The sole exception is `HealthCheck`, deliberately and with the reason recorded on the endpoint: Swarm's probe polls it from one address, and a 429 would mark the container unhealthy and restart it — the limiter would manufacture the outage it exists to detect.

All policies live in `ConfigureRateLimiting.cs`, not Program.cs.

`sse` is a concurrency limiter, not a fixed window: feed streams stay open for the life of the page, so the limit that matters is simultaneous sockets per IP, not requests per minute. One feed page opens five streams (one per tier), so 20 permits ≈ 4 tabs. `QueueLimit` is 0 so excess connections get an immediate 429 instead of a hung `EventSource`. Any new long-lived/streaming endpoint must use this policy.

### Authentication & Authorization

- **Cookie auth** (`KlavLor.Web.Auth`) — 30-day sliding expiration, HttpOnly, Strict SameSite
- **API key auth** — Alternative scheme for programmatic access (e.g., RuneLite plugin). Both schemes are accepted on User/Admin policies.
- **ICurrentUser** — Injected into handlers for auth checks (`UserId`, `IsAdmin`). Authorization is checked inline in handlers, not via middleware attributes (beyond `[Authorize]`).
- **Policies:** `User` (any authenticated user), `Admin` (requires Admin role), `Auditor` (sync-log access). Default policy requires authentication.

**Public read surface.** Anonymous by design: loot feed (+ Leagues feed and their SSE streams), character loot logs / profiles / source detail / collection tabs, item and source icons, template search, and the Luck Leaderboard. These are linked in the sidebar for signed-out visitors, so an endpoint behind them must be `.AllowAnonymous()` or the nav link 401-redirects to login.

Authenticated (`RoleName.User`) despite also being read-only: the **global** source and drop detail pages (`Features/Source`, `Features/Drop`) and global search. Their routable pages carry `@attribute [Authorize]` to match. Everything that writes or reads one user's own data (templates CRUD, builder, completion, characters, admin, sync logs, ingest) requires authorization too.

**Routable Razor pages authorize separately from endpoints.** `MapRazorComponents<App>()` has no fallback policy, so a `@page` component is anonymous unless it carries `@attribute [Authorize]`. A page and the `/api` endpoint that serves its HTMX-navigated content must agree — otherwise direct URL loads and in-app navigation disagree about who may see it.

### Feature Folder Structure

Code is organized by feature, not by technical concern. Feature folders live under `KlavLor.Application/Features/` and `KlavLor.Web/Application/Features/`. The two layers overlap but don't mirror exactly — Application has top-level `ApiKeys/`, `Builder/`, `CollectionLog/`, `DropRates/` and `Maintenance/` folders whose Web-side counterparts are nested under `Users/`, `Templates/` and `Settings/`.

Shared in both layers:

- `Characters/` — Character profile pages
- `Drop/` — Global drop detail (one item across every source; `GlobalDropCache` memoises the aggregate)
- `Login/` — Authentication (Web also has `Logout/` and `Home/`, which just redirects to the loot feed)
- `Loot/` — the largest area, see breakdown below
- `Search/` — Global search across characters, sources and drops
- `Settings/` — Admin area. **One section per URL** (`/admin/settings/{slug}`) — see "The Admin Area Is One Section Per URL" above
- `Source/` — Global source (boss/monster) detail across all characters, with `GlobalSourceCache`
- `Templates/` — Template CRUD (`Commands/`, `Queries/`) and the visual canvas builder (`Builder/` — nodes, edges, groups, annotations, regions, layouts). There is deliberately no export, import or duplicate feature: the endpoints existed but were never registered or linked from the UI, and were removed rather than finished.
- `Users/` — Admin user management, API key generation/revocation, character assignment
- `Viewer/` — Read-only template viewing, completion tracking

`Loot/` subfolders:

- `Ingest/` — RuneLite batch ingest (+ `Ingest/Audit/` sync logs for the Auditor role)
- `Feed/` — Live SSE feed streams and cards (main + Leagues scopes)
- `Log/` — Per-character loot log, source detail, kill sessions, collection progress
- `Leaderboard/` — Luck leaderboard (spoons / dry streaks) and its source + item exclusion admin
- `Superiors/` — Superior slayer monster comparison (see "Superior Slayer Monsters" below)
- `SourceModels/` (Application only) — Pluggable per-source drop maths behind `ISourceLootStrategy`: `DefaultSourceLootStrategy`, `DoomLootStrategy` (per-run delve depth), `RaidUniqueShareStrategy`, dispatched by `SourceLootService`, plus admin rate modifiers. **Strategies are matched by interface dispatch — a new strategy must be registered with `SourceLootService` or it silently never engages** (see commit `abf0996`). Enforced by `KlavLor.UnitTests/SourceLootStrategyRegistrationTests.cs`, which scans the Application assembly and fails if any `ISourceLootStrategy` implementation is unregistered or unreachable through the facade.
- `Baseline/` (Application only) — Admin-entered pre-tracking kill counts, added to derived KC
- `Special/` (Application only) — Special/one-off loot item configuration
- `ItemValues/` (Application only) — Admin intrinsic GP values for untradeable drops (see "Item Values" above)

Application-only:

- `CollectionLog/` — Collection-log item blacklist admin
- `DropRates/` — Drop-rate admin + resync, missing-rate reporting
- `Maintenance/` — Icon audit, job health, sync status, source rename/admin

Web-only:

- `HealthCheck/` — Health check endpoint

### The App Is Dark-Only. There Is No Theme To Switch.

There is no light theme, no theme toggle, no `dark:` variant and no `.dark` class. Do not add a
`dark:` utility to anything — it will not compile to a variant, because `@variant dark` is gone from
`app.css`; it would be emitted as a literal class name that matches nothing and silently do nothing.
Write the colour you want.

It was removed rather than fixed. There never was a light theme — there was the dark theme with its
neutral ramp mirrored, which is why it read as "eye burningly bright and borderline unusable":
mirroring cannot survive the trip, since above 96.8% lightness there is no room left, so light got
1.05:1 between card and ground where dark gets 1.13:1, and the unpaired `*-400` tier borders ended up
carrying the whole page's structure. `docs/light-theme-audit.md` has the measurements and the
retuning that was tried first; it is kept because the same trap waits for anyone adding a second
theme later.

What the removal actually did, in case it has to be redone or reasoned about:

- **Every `x dark:y` pair collapsed to `y`.** This is exactly appearance-preserving, and the reason
  is worth knowing: a `dark:` utility and its light counterpart have EQUAL specificity in Tailwind 4
  (the variant is `&:where(.dark, .dark *)`, and `:where()` contributes none), so the dark one won
  purely on source order. Deleting the light utility and unprefixing the dark one therefore lands on
  precisely what dark mode painted.
- **Which light utility a `dark:` one overrode was decided from the compiled CSS**, never from the
  class name. `text-` is three different properties (`color`, `font-size`, `text-align`), so
  `dark:text-white` must delete `text-slate-500` and must not touch `text-xs` or `text-center`. Only
  the emitted stylesheet knows that.
- **`:where(.dark, .dark *) X { … }` rules in `app.css` had the prefix stripped in place**, keeping
  their position. They sat after a plain rule for the same selector and overrode only the properties
  they declared, so leaving the order alone preserves the cascade — deleting the plain rule would
  have dropped the properties the dark rule never set (`.sc-item` sets `font-weight` and `color`;
  only the colour was themed). The now-shadowed light declarations were then deleted individually.
- **Verified, not eyeballed.** Every class list the change touched (995 of them, including all
  `app.css` custom classes) was rendered against the OLD stylesheet with `.dark` set and against the
  new dark-only one, and all 66 computed visual properties compared: zero differences, base state and
  `:hover` alike.

A user who had previously chosen light gets dark; the stored `theme` key is simply ignored and never
read. `StackPalette` needed no change at all and the reason is recorded on it — its fills were
deliberately theme-independent.

### Frontend

- **Tailwind CSS 4** — Config lives in `KlavLor.Web/wwwroot/app.css` using `@theme` blocks (no tailwind.config.js). Output: `wwwroot/styles.css`.
- **HTMX** — Server-driven interactivity, bundled as `wwwroot/htmx.min.js`.
- **builder.js** — Canvas drag/drop, node/edge creation, Bezier paths, zoom/pan. This is the most complex client-side file.
- **sse.js** — Server-Sent Events client for live loot feed streams (per-tier subscriptions). **site.js** holds shared misc client helpers.
- **`#mobile-sidebar` IS THE ONLY SIDEBAR, at every width.** The id is a misnomer and it misleads: there is no separate desktop sidebar, no `lg:` override on the transform and no media query on it in `app.css`. It is `position: fixed`, off-canvas, and toggled by the same hamburger on a phone and at 1900px. Anything said about "the mobile sidebar" applies to desktop too.
- **A site-wide `htmx:afterSettle` handler must check WHAT was swapped.** `afterSettle` on `document.body` fires for *every* swap on the page — each feed lane, each SSE frame, each deferred panel, the sidebar's own account fetch — not just navigations. site.js closed the sidebar on every one of them, so opening it while anything was in flight slammed it shut the moment that request landed; the character page's six panels and the superiors page's two halves each did it, at every viewport width. A navigation is identifiable: every sidebar link carries `hx-target="#hx-page-container"`, so the handler gates on `evt.detail.target.id === 'hx-page-container'` — the same check `roll-ticker.js` uses to re-init after an in-app navigation.
- **roll-ticker.js** — The loot feed's live roll banner: the queue that paces arrivals, the reconnect dedupe, and the slide. Self-initialising, loaded before site.js, and the only front-end file with tests (see "JS Tests").
- **CSP note:** `img-src` allows `https://oldschool.runescape.wiki` for OSRS item images. Update the CSP in Program.cs if adding new external image sources.

### Domain Model

`Template` is the aggregate root. It owns `TemplateNodes`, `TemplateEdges`, `TemplateNodeGroups`, `CanvasAnnotations`, `CanvasRegions`, and `LayoutSnapshots` (DAG structure with visual canvas elements). `UserNodeCompletion` tracks per-user progress through nodes. `GearItem`, `ItemIcon`, and `CachedImage` support OSRS Wiki integration. `LootRecord` and `ApiKey` support the loot tracking feature.

All entities extend `Entity` base class (Id, RowVersion, SavedAt, SavedById audit trail).

### EF Core Patterns

- **Optimistic concurrency** via `uint RowVersion` on all entities (EF xmin token on Postgres).
- **Audit interceptor** (`UserIdAuditInterceptor`) automatically sets `SavedById` on every Add/Modify — never set it manually.
- **Private collections** on aggregates (e.g., `Template._nodes`) use `PropertyAccessMode.Field` in EF config.
- **Cascade delete** for owned entities; **restrict** for edges (prevents orphaning nodes).
- **Auto-include** on `User.UserRoles` — roles are always loaded with user queries.

### Background Services

All implementations live in `KlavLor.Infrastructure/Services/`, and **all of them are registered in one place** — `AddBackgroundServices()` inside `InfrastructureDependencyConfiguration`, called at the end of `AddInfrastructure()`. Registration used to be split between there and Program.cs, which hid the startup order; don't reintroduce `AddHostedService` calls in Program.cs. Hosted services start in registration order, and `LootFeedSeederService` must stay first.

- `LootFeedSeederService` — Seeds the feed with historical data on startup (must run first)
- `ImageCacheBackfillService` — Backfills OSRS Wiki image cache
- `ItemIconBackfillService` — Backfills item icon data
- `SourceIconBackfillService` — Backfills source (monster/boss) icon data
- `CachedImageReprocessService` — Reprocesses previously cached images
- `CollectionLogSyncService` — Syncs collection-log item definitions from the Wiki
- `DropRateSyncService` — Syncs per-source drop rates from the Wiki
- `LuckLeaderboardRefreshService` — Rebuilds the luck leaderboard hourly
- `LootDerivationBackfillService` — Backfills derived loot columns (effective kills, drop projection)

Recurring services poll `IJobScheduler` for an elapsed interval or a manual admin trigger, and record each cycle via `IJobRunRecorder` for the admin job-health panel (`BackgroundJobNames` holds the job keys).

These are the only places where manual DI scopes are acceptable (via `IServiceScopeFactory`). Program.cs startup also primes the singleton caches (`ICollectionLogCache`, `ISystemSettingsCache`, `ISourceRateModifierCache`) *before* the host starts, because the seeder classifies drops against them immediately.

## Integration Tests

`KlavLor.IntegrationTests` (xUnit) runs against a real PostgreSQL started by Testcontainers (`postgres:16-alpine`) with the full EF migration set applied, so tests exercise real SQL — including the raw-ADO repositories and the `LootDrop` projection — rather than an in-memory fake. **Docker must be running.** The container is shared via `PostgresFixture` / the `"postgres"` collection, so tests in that collection must not assume an empty database; seed and scope your own rows.

Coverage is targeted at the loot-derivation maths and query surface, not the web layer: character sessions, drop-rate bucket client and sync, feed ordinals and one-off drops, loot-drop projection, item-value override rebuild and restore, record-level luck exclusion, source rename, source tables, and golden-file assertions for drop search.

Three files exist because the bug they pin was invisible until production and looked like something else entirely:

- `ProjectionRebuildTests` — the projection rebuild must keep item-value overrides and `IsSpecial`, including through `RecomputeFirstTimeFlags`, which is what actually triggered it.
- `FeedBufferOverrideTests` — an override write must refresh the live feed's in-memory buffer, driven through the real `ItemValueOverrideAdminHandler`, plus the reported symptom: a later live drop merging onto the receipts the override revealed rather than replacing the card.
- `SourceCollectionClogMatchTests` — a name-matched collection-log item keeps its drop events and its place in the unlocked count.

```bash
dotnet test KlavLor.IntegrationTests/KlavLor.IntegrationTests.csproj
```

The top-level `tests/` directory holds manual testing-plan docs (Markdown) plus `tests/js/`, which
is runnable — see "JS Tests" below.

## Unit Tests

`KlavLor.UnitTests` (xUnit) has **no database dependency and needs no Docker**. It references Application (the pure loot maths) and Web (so the architecture tests can reflect over its components). Run it on any machine:

```bash
dotnet test KlavLor.UnitTests/KlavLor.UnitTests.csproj
```

What it covers, and why each file exists:

- `DoomLootStrategyTests` — `ProbabilityOverRun` / `ExpectedCompletionsForRuns` / `EstimateDepth`, including the two properties the strategy's own comments only *claimed*: that the per-run sum reduces to the flat per-run expectation at a uniform depth, and that mixed-depth runs do **not** score as if every run reached the deepest one (the bug that reported everyone as dry). Also pins the level-9 rate clamp for deep delves.
- `SourceLootServiceTests` — that raid unique-table scaling **and** admin rate modifiers are both applied *inside* the facade, so a hand-rolled call site is provably wrong (see "Luck Maths: One Path Only").
- `SourceLootStrategyRegistrationTests` — every `ISourceLootStrategy` in the Application assembly is registered and reachable through `SourceLootService` (commit `abf0996`).
- `RaidAndDefaultStrategyTests`, `LootFeedGroupingTests` — raid share scaling vs. tertiary pass-through; `MaxGap` / `SessionBreakGap` / `PlayDayStart` session boundaries.
- `LootFeedTierClassificationTests` — tiers are per drop, never per running total (500 cheap drops summing to millions must not read as legendary).
- `RepositoryRegistrationTests` — the reflection-based repository registration; see "Repository Auto-Registration".
- `RazorComponentDataAccessTests` — the SSR data-access rules; see "Razor Component Data-Access Rules".
- `ItemValueOverrideTests` — the intrinsic item-value cache and the tier consequence; see "Item Values".
- `FeedLuckShouldRateTests` — which feed drops get a lucky/dry line at all: collection-log items only, first receipt only, not admin-excluded, rare enough to judge. Each condition is pinned separately, plus a check that no two of them cancel out.
- `RollChipHueTests` — the ticker's per-character colour: distinctness across a palette-sized clan, stability, case-insensitivity, and that every class the assigner can emit has a rule in `app.css` (the names are computed, so nothing else would catch the two drifting apart).

There is still no coverage of Web endpoints.

## JS Tests

`tests/js/` runs under Node's built-in test runner with jsdom. **No browser, no Docker, no database.**

```bash
npm run test:js
```

- `roll-ticker.test.js` — the loot feed's roll banner: that a batch is released one at a time and
  not slid in as a block, that a roll landing a millisecond after another still waits its turn, that
  a reconnect replaying the server ring adds no duplicates (including against a roll still queued),
  the trim, the queue's overflow policy, reduced motion, and that `slideMs` still matches the CSS
  transition it paces against. Plus the hidden-tab pause: nothing released while hidden, an armed
  timer cancelled on the way out, the backlog resuming one at a time rather than as a block, the cap
  keeping the newest rolls across a long absence, a brief alt-tab costing nothing, and `destroy`
  unhooking the document listener it added.

Everything it covers fails **visibly but silently** — a batching regression still shows every chip,
just all at once, and a duplicate is just a chip — which is why it is asserted rather than eyeballed.
Both of those bugs shipped before this file existed.

## Deployment

CI/CD via GitHub Actions (`.github/workflows/pipeline.yml`). Push to `main` builds a Docker image, pushes to GHCR, and deploys via Docker Swarm with Traefik reverse proxy. Production config is in `docker-stack.yml`.

System admin credentials are injected via `SystemConfiguration__SystemUsername` and `SystemConfiguration__SystemPassword` environment variables.

## klavlor-sync (Loot Sync Tool)

A Go binary (`tools/klavlor-sync/`) that monitors RuneLite's Loot Tracker plugin and syncs kill records to the KlavLor server.

### How It Works

1. Polls `~/.runelite/loots/*.log` files every 5 seconds for new JSON lines written by RuneLite
2. Parses each line, computes a SHA-256 content hash (`relPath:lineNumber:rawJSON`) for deduplication
3. Batches up to 250 records and sends them to `POST /api/loot/ingest/batch` with `Authorization: Bearer {api_key}`
4. Server deduplicates by content hash, stores records, and publishes non-imported kills to SSE feed streams
5. Persists file offsets and recent hashes to `~/.klavlor-sync/state.json` for resumable syncing

### Fresh Install

```bash
# Build (from repo root) — Windows
cd tools/klavlor-sync && go build -o klavlor-sync.exe .
./klavlor-sync.exe --install

# Build — macOS (extension-less binary)
cd tools/klavlor-sync && go build -o klavlor-sync .
./klavlor-sync --install
```

`build.sh` cross-compiles release artifacts (Windows `.exe` + macOS universal binary via `lipo` when run on a Mac).

The installer walks through 4 steps:
1. **Find RuneLite** — Auto-detects `~/.runelite/loots/` or prompts for manual path
2. **API Key** — Paste a `klav_*` key generated from the KlavLor admin panel (`/admin/users/{id}/api-key/generate`)
3. **Server URL** — Defaults to `https://localhost:7081`, override for production
4. **Historical sync** — Choose to sync all existing loot history or start fresh (tail mode)

After install:
- Config saved to `~/.klavlor-sync/config.toml`
- Binary copied to `~/.klavlor-sync/klavlor-sync.exe` (Windows) or `~/.klavlor-sync/klavlor-sync` (macOS)
- Auto-start registered (launches hidden on login via `--background`):
  - **Windows** — Startup-folder VBS at `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\klavlor-sync.vbs`
  - **macOS** — launchd LaunchAgent at `~/Library/LaunchAgents/dev.joshuawoodward.klavlor-sync.plist` (loaded via `launchctl bootstrap`)

Platform-specific install backends live in `internal/install/install_windows.go` and `install_darwin.go` (Linux/other falls through to the unsupported stub in `install_other.go`). The shared interactive flow and the `atomicCopy` helper are in `install.go` / `install_common.go`.

### Key Commands

```bash
./klavlor-sync.exe --install      # Interactive setup
./klavlor-sync.exe --uninstall    # Remove startup entry, optionally delete config/state
./klavlor-sync.exe --background   # Run headless with log output to ~/.klavlor-sync/klavlor-sync.log
```

### Server-Side Data Flow

Sync tool → `ApiKeyAuthenticationHandler` (Bearer token → SHA256 lookup → user claims) → `LootIngestHandler` (validate, parse dates, deduplicate by content hash, insert) → `LootFeedService` (publish live kills to SSE subscribers at `/api/loot/feed/stream/{standard|uncommon|rare|epic|legendary}`).

Feed tiers are classified **per drop** (not per kill) by GP value, defined as `LootFeedTier` in `ILootFeedService`:
- **Standard** — 10K–100K
- **Uncommon** — 100K–1M
- **Rare** — 1M–10M
- **Epic** — 10M–100M
- **Legendary** — 100M+

Drops below 10K are not published. A single kill can produce entries on multiple tiers.

### Go Source Structure

```
tools/klavlor-sync/
├── main.go                       # Entry point, loop coordination
├── internal/
│   ├── config/config.go          # TOML config loading + CLI flags
│   ├── install/                  # Installer logic (install_windows.go for VBS startup)
│   ├── detect/runelite.go        # Auto-detect RuneLite loots directory
│   ├── watcher/watcher.go        # File polling & discovery
│   ├── tailer/tailer.go          # Line-by-line JSON parsing, content hashing
│   ├── sender/sender.go          # HTTP batching, rate limiting (1 req/s), retries (3x exponential)
│   ├── state/state.go            # Offset/hash persistence to state.json
│   └── model/loot.go             # LootRecord & LootDrop DTOs
└── RUNBOOK.md                    # User documentation
```

## Tests

Two test projects plus a JS suite. See "Integration Tests", "Unit Tests" and "JS Tests" above.

- `KlavLor.IntegrationTests` — the raw-ADO query surface, against a real Postgres via Testcontainers. **Needs Docker.**
- `KlavLor.UnitTests` — the pure loot maths plus the architecture rules (repository registration, SSR data-access). **No database, no Docker.**
- `tests/js/` — the roll ticker's client behaviour, under jsdom via `npm run test:js`. **No browser.**
