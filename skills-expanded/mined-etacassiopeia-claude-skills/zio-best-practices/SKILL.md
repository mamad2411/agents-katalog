---
name: zio-best-practices
description: >
  Comprehensive ZIO 2 coding standards, service patterns, error handling,
  concurrency, resource management, and testing guidance. TRIGGER when: code
  imports ZIO or zio.*, working with ZLayer composition, defining services,
  fiber management, resource acquisition, writing zio-test specs, using ZIO
  Prelude (Validation, Equal, ZPure), handling Cause/Exit, composing
  ZSchedule retry policies, or using advanced fiber patterns (interruption
  masks, Semaphore, Supervisor). Always consult before generating ZIO effects,
  service definitions, or layer wiring — it encodes Service Pattern 2.0,
  Cause/Exit semantics, and error model distinctions that are easy to get
  wrong and hard to refactor later.
---

# ZIO 2 Best Practices

## Effect Type Algebra — Use the Least Powerful Type

| Type | Meaning | Use when |
|---|---|---|
| `UIO[A]` | No env, no failure | Pure ZIO computations |
| `URIO[R, A]` | Needs env, no failure | Infallible env-dependent work |
| `Task[A]` | No env, fails with `Throwable` | Interop with Java/Scala exceptions |
| `IO[E, A]` | No env, typed error | Domain operations with typed errors |
| `ZIO[R, E, A]` | Full generality | Only when you need all three |

```scala
// Prefer specific aliases
def greet(name: String): UIO[String] = ZIO.succeed(s"Hello, $name")
def findUser(id: UserId): IO[UserNotFound, User] = ???

// Avoid — unnecessarily general
def greet(name: String): ZIO[Any, Nothing, String] = ZIO.succeed(s"Hello, $name")
```

---

## Service Pattern 2.0

Three-part structure. No `Has[]`, no accessor methods, no `ZLayer` in trait companion.

```scala
// 1. Trait — the service interface
trait UserRepo:
  def findById(id: UserId): IO[UserNotFound, User]
  def save(user: User): UIO[Unit]
  def delete(id: UserId): IO[UserNotFound, Unit]

// 2. Live implementation — dependencies injected via constructor
case class UserRepoLive(db: Database, cache: Cache) extends UserRepo:
  def findById(id: UserId): IO[UserNotFound, User] =
    cache.get(id).someOrElseZIO(db.query(id))
  def save(user: User): UIO[Unit] =
    db.insert(user) *> cache.put(user.id, user)
  def delete(id: UserId): IO[UserNotFound, User] =
    db.delete(id) <* cache.remove(id)

// 3. ZLayer in the implementation's companion — NOT in UserRepo companion
object UserRepoLive:
  val layer: URLayer[Database & Cache, UserRepo] =
    ZLayer.derive[UserRepoLive]

// 4. Access services — ZIO.serviceWithZIO, never accessor methods
val program: ZIO[UserRepo, UserNotFound, User] =
  ZIO.serviceWithZIO[UserRepo](_.findById(UserId.of("123")))
```

**Rules:**
- Layer goes in `ImplLive` companion, not the `Service` companion
- `ZLayer.derive[Impl]` handles constructor injection automatically
- For services requiring resources, extend `ZLayer.Derive.Scoped`

```scala
case class HttpClientLive(client: HttpClient) extends HttpService:
  // ...

object HttpClientLive:
  val layer: TaskLayer[HttpService] = ZLayer.scoped {
    ZIO.acquireRelease(
      ZIO.attempt(HttpClient.newBuilder().build())
    )(client => ZIO.succeed(client.close()))
  }.map(client => HttpClientLive(client))
```

---

## Error Handling

### Three Categories — Keep Them Distinct

| Category | How | When |
|---|---|---|
| **Failure** | Typed `E` in `ZIO[R, E, A]` | Expected domain errors you can recover from |
| **Defect** | `ZIO.die` / `dieMessage` | Programmer errors, contract violations |
| **Fatal** | `FiberFailure` / platform fatal | Shutdown-level errors |

```scala
// Domain error as typed enum
enum UserError:
  case NotFound(id: UserId)
  case InvalidEmail(raw: String)
  case Unauthorized(userId: UserId)

// Failure: typed, recoverable
def loadUser(id: UserId): IO[UserError.NotFound, User] = ???

// Defect: unexpected, unrecoverable — don't type it
def mustExist(id: UserId): UIO[User] =
  loadUser(id).orDie  // becomes defect if not found
```

### Error Operators

```scala
// Narrow: convert unexpected errors to defects
effect.refineOrDie { case e: DomainError => e }

// Transform error type between bounded contexts
effect.mapError(dbError => UserError.StorageFailure(dbError))

// Observe without handling
effect.tapError(e => ZIO.logError(s"Unexpected: $e"))
effect.tapDefect(cause => ZIO.logError(s"Defect: $cause"))

// Handle separately
effect.foldZIO(
  failure = e => ZIO.fail(translateError(e)),
  success = a => ZIO.succeed(process(a))
)

// Accumulate errors (don't fail-fast)
ZIO.validatePar(userIds)(id => loadUser(id))

// Convert Either result back to typed ZIO
ZIO.fromEither(validate(input))
ZIO.absolve(effect.map(eitherResult))
```

### Don't Log at Every Layer

```scala
// Anti-pattern — log noise, swallowed context
def findUser(id: UserId): IO[UserError, User] =
  db.query(id).tapError(e => ZIO.logError(s"Error: $e"))  // DON'T reflexively log here

// Correct — log once at the boundary
val program = findUser(id).catchAll { e =>
  ZIO.logError(s"Request failed: $e") *> ZIO.fail(e)
}
```

---

## Resource Management

Always use `Scope` for anything requiring cleanup.

```scala
// Scoped resource — guaranteed finalization
val managedConnection: ZIO[Scope, Throwable, Connection] =
  ZIO.acquireRelease(
    acquire = ZIO.attempt(openConnection()),
    release = conn => ZIO.succeed(conn.close())
  )

// Use in a bounded scope
ZIO.scoped {
  managedConnection.flatMap { conn =>
    useConnection(conn)
  }
}

// Layer with resource — scoped automatically
val connectionLayer: TaskLayer[Connection] = ZLayer.scoped {
  ZIO.acquireRelease(
    ZIO.attempt(openConnection()),
    conn => ZIO.succeed(conn.close())
  )
}
```

**Rules:**
- Never leak clients/connections on early failure
- `ZLayer.scoped` for service layers that own resources
- `ZIO.scoped` to bound a resource's lifetime within a single operation
- Implement `ZLayer.Derive.Scoped[-R, +E]` for automatic handling in `ZLayer.derive`

---

## Concurrency

### Fibers — Structured Concurrency

```scala
// Fork returns a Fiber — always join or interrupt
val fiber: UIO[Fiber[Nothing, Int]] = computation.fork
val result: UIO[Int] = fiber.flatMap(_.join)

// Independent parallel work — prefer combinators over manual fork
val (a, b) = ZIO.zipPar(fetchUser(id), fetchOrders(id))
val results = ZIO.collectAllPar(ids.map(fetchUser))
val parallelN = ZIO.foreachPar(ids)(fetchUser)  // unbounded concurrency
val parallelN = ZIO.foreachParN(8)(ids)(fetchUser)  // bounded

// Race: first to complete wins, other is interrupted
ZIO.race(fetchFromPrimary(key), fetchFromCache(key))
```

### Concurrent State — Never `var`

```scala
// Ref — single value, atomic update
val counter: UIO[Ref[Int]] = Ref.make(0)
counter.flatMap(_.update(_ + 1))
counter.flatMap(_.modify(n => (n, n + 1)))  // read + update atomically

// Queue — producer/consumer
val queue: UIO[Queue[Task]] = Queue.bounded[Task](capacity = 128)

// Hub — broadcast to multiple subscribers
val hub: UIO[Hub[Event]] = Hub.bounded[Event](capacity = 256)

// STM — composable atomic transactions
val transfer: STM[Nothing, Unit] =
  for
    _ <- accountA.update(_ - amount)
    _ <- accountB.update(_ + amount)
  yield ()
ZSTM.atomically(transfer)
```

### JoinSet for Grouped Fibers

```scala
// Prefer JoinSet over loose fork
ZIO.scoped {
  for
    set <- ZIO.acquireRelease(JoinSet.make[Error, Result])(_.shutdown)
    _   <- ZIO.foreachDiscard(tasks)(t => set.add(t.run))
    rs  <- set.joinAll
  yield rs
}
```

---

## ZIO Streams

Operate on **chunks**, not individual elements.

```scala
// Prefer — chunk-level transformation (no fragmentation)
stream.mapChunksZIO(chunk => ZIO.foreach(chunk)(transform))

// Avoid — fragments chunks, ~700ms overhead per element in benchmarks
stream.tap(element => process(element))

// Async islands for parallel processing
stream
  .aggregateAsync(ZSink.collectAllN[Event](100))
  .mapZIO(batch => processParallel(batch))

// Resource-safe stream construction
ZStream.scoped {
  ZIO.acquireRelease(openFile(path))(_.close).map { file =>
    ZStream.fromInputStream(file)
  }
}.flatten
```

**Performance rules:**
- Buffer sizes: powers of 2 (`64`, `128`, `256`, `1024`)
- `mapChunksZIO` > `mapZIO` > `tap` for throughput
- Use `aggregateAsync` to create parallel async islands

---

## ZIO Prelude Integration

ZIO Prelude is the ZIO-native typeclass library. Prefer it over Cats in ZIO projects.

```scala
import zio.prelude.*

// Derive structural instances at definition site — no boilerplate
case class UserId(value: UUID)    derives Equal, Hash, Ord
case class Email(value: String)   derives Equal, Hash
enum Status derives Equal:
  case Active, Inactive

// Validation: pure error accumulation, no effects needed
// Unlike ZIO.validate, Validation[E, A] is entirely pure
val validated: Validation[String, User] = Validation.validate(
  Validation.fromPredicateWith("name is empty")(name)(_.nonEmpty),
  Validation.fromPredicateWith("age is negative")(age)(_ >= 0),
  Validation.fromPredicateWith("email is invalid")(email)(_.contains('@'))
)(User.apply)

val result: Either[NonEmptyChunk[String], User] = validated.toEither

// ZPure: stateful, deterministic, pure programs — no ZIO runtime needed
// Use for config evaluation, state machines, rule engines, compilers
import zio.prelude.fx.ZPure

type Config[+A] = ZPure[Nothing, AppConfig, AppConfig, Any, ConfigError, A]

val readTimeout: Config[Duration]      = ZPure.get.map(_.timeout)
val readMaxRetries: Config[Int]        = ZPure.get.map(_.maxRetries)
val combined: Config[(Duration, Int)]  = readTimeout.zip(readMaxRetries)

// Run pure — no runtime, deterministic, easily testable
val (finalState, value) = combined.run(AppConfig.default)
```

**When to reach for ZIO Prelude:**
- `Validation[E, A]` — pure accumulation without effects (form validation, config parsing)
- `Equal`/`Hash`/`Ord` — structural instances for domain types (replace custom `==` overrides)
- `ZPure` — stateful pure computation where ZIO's fiber overhead is unnecessary
- `Associative`/`Identity` — when domain values need to be combined monoïdally (stats aggregation, metrics)

---

## Cause & Exit — Fine-Grained Error Inspection

`Exit[E, A]` and `Cause[E]` expose the full outcome of a fiber.

```scala
// Exit[E, A] = Succeed(value) | Failure(Cause[E])
// Cause[E]   = Fail(E) | Die(Throwable) | Interrupt(FiberId)
//            | Both(Cause, Cause)        — parallel failures
//            | Then(Cause, Cause)        — sequential failures

// Run to Exit — never throws, captures everything
val exit: UIO[Exit[UserError, User]] = findUser(id).exit

// Fold over cause — handles all variants correctly
effect.foldCauseZIO(
  failure = cause =>
    if cause.isInterrupted then ZIO.interrupt
    else cause.failureOption match
      case Some(e: UserError.NotFound) => ZIO.succeed(User.anonymous)
      case Some(e)                     => ZIO.fail(e)
      case None                        => ZIO.refailCause(cause)  // re-raise defect
  ,
  success = ZIO.succeed
)

// Sandbox: promote defects into the typed error channel for uniform handling
effect
  .sandbox              // ZIO[R, Cause[E], A]
  .mapError { cause =>
    cause.failureOption.getOrElse(AppError.Unexpected(cause.prettyPrint))
  }
  .unsandbox            // ZIO[R, AppError, A]

// Bring a specific Throwable defect back to typed error
effect.unrefine { case e: TimeoutException => UserError.Timeout }
```

**Rules:**
- Prefer `foldCauseZIO` over pattern-matching on `Exit` — it handles `Both`/`Then` correctly
- `sandbox`/`unsandbox` for uniform error handling at service boundaries
- Never catch `Throwable` with `.catchAll` — use `unrefine` to target specific defects
- Inspect `Cause` only at the outermost layer (HTTP handler, `main`); propagate otherwise

---

## ZSchedule — Retry and Repeat

Never implement retry with manual recursion. Use `Schedule`.

```scala
// Common retry policies
val retryThrice      = Schedule.recurs(3)
val retryExponential = Schedule.exponential(100.millis) && Schedule.recurs(5)
val retryWithJitter  = retryExponential.jittered           // avoids thundering herd
val retrySpaced      = Schedule.spaced(500.millis) && Schedule.recurs(10)

// Retry an effect
effect.retry(retryWithJitter)

// Retry with fallback when retries are exhausted
effect.retryOrElse(
  retryWithJitter,
  (err, schedule) => ZIO.logError(s"Exhausted retries: $err") *> ZIO.fail(err)
)

// Compose schedules
val fast   = Schedule.spaced(100.millis) && Schedule.recurs(3)
val slow   = Schedule.spaced(2.seconds)  && Schedule.recurs(20)
val tiered = fast >>> slow          // run fast policy first, then slow

val orElse  = fast || slow          // whichever allows more retries

// Repeat — for periodic / background tasks
ZIO.repeat(heartbeat)(Schedule.spaced(5.seconds))
ZIO.repeat(cleanup)(Schedule.fixed(1.hour))

// Retry only specific error types
effect.retryWhile { case _: TransientError => true; case _ => false }
```

---

## Advanced ZLayer Composition

```scala
// Horizontal: combine independent layers side-by-side
val repos: TaskLayer[UserRepo & OrderRepo] =
  UserRepoLive.layer ++ OrderRepoLive.layer

// ZLayer.make: auto-wires the full dependency graph from a flat list
// Compiler error if any dependency is missing; no ordering required
val appLayer: TaskLayer[UserRepo & OrderRepo & EmailService] =
  ZLayer.make[UserRepo & OrderRepo & EmailService](
    UserRepoLive.layer,
    OrderRepoLive.layer,
    EmailServiceLive.layer,
    DatabaseLive.layer,     // transitively required
    CacheLive.layer
  )

// provideSome: wire partial deps, leave remaining for the outer scope
val partialProgram: ZIO[Config, AppError, Unit] =
  program.provideSome[Config](UserRepoLive.layer, DatabaseLive.layer)

// Scoped layers are finalized in reverse acquisition order — guaranteed
val managed: TaskLayer[ConnectionPool] = ZLayer.scoped {
  ZIO.acquireRelease(
    ConnectionPool.make(config),
    pool => pool.shutdown
  )
}

// Memoization: ZIO memoizes layers by default — each type provided once
// To force a fresh instance per use, call .fresh on the layer
val freshDb = DatabaseLive.layer.fresh
```

**Rules:**
- `ZLayer.make` at the application entry point; `provide` in tests for clarity
- Keep layers flat — avoid long `>>>` chains; wire at the top
- Use `.provideSomeShared` in test suites to share expensive resources across tests
- Never put `ZLayer.make` inside a per-test `provide` — it rebuilds the graph each time

---

## Advanced Fiber Patterns

```scala
// Uninterruptible: protect cleanup / critical section from cancellation
ZIO.uninterruptible(releaseResource(r))

// Interruptible mask: uninterruptible outer, re-enable for the main work
ZIO.uninterruptibleMask { restore =>
  acquireResource.flatMap { r =>
    restore(useResource(r)).ensuring(releaseResource(r))
    // restore() re-enables interruption for useResource only
  }
}

// Promise: single-use async handoff between fibers
Promise.make[Nothing, Result].flatMap { promise =>
  producer.flatMap(promise.succeed).fork *>
  promise.await  // blocks fiber until producer resolves
}

// Semaphore: limit concurrency without blocking threads
Semaphore.make(permits = 4).flatMap { sem =>
  ZIO.foreachPar(requests)(req => sem.withPermit(processRequest(req)))
}

// Supervisor: observe fiber lifecycle (debugging, metrics)
Supervisor.track(weak = true).flatMap { supervisor =>
  program.supervised(supervisor).flatMap { _ =>
    supervisor.value.map(_.size)  // number of live child fibers
  }
}
```

---

## Testing with zio-test

```scala
object UserRepoSpec extends ZIOSpecDefault:
  def spec = suite("UserRepo")(

    test("finds existing user") {
      for
        repo <- ZIO.service[UserRepo]
        user <- repo.findById(UserId.of("1"))
      yield assertTrue(user.name == "Alice")
    },

    test("returns NotFound for missing user") {
      for
        repo   <- ZIO.service[UserRepo]
        result <- repo.findById(UserId.of("missing")).exit
      yield assert(result)(fails(equalTo(UserError.NotFound(UserId.of("missing")))))
    },

    // Property-based test
    test("save then find roundtrip") {
      check(Gen.alphaNumericString, Gen.int) { (name, age) =>
        for
          repo <- ZIO.service[UserRepo]
          user  = User(UserId.fresh, name, age)
          _    <- repo.save(user)
          found <- repo.findById(user.id)
        yield assertTrue(found == user)
      }
    }

  ).provide(
    InMemoryUserRepo.layer  // in-memory impl, not mocks
  )
```

**Rules:**
- `ZIOSpecDefault` as base
- `ZLayer.succeed(impl)` with in-memory implementations — not mocks
- Test error paths: use `.exit` + `fails(equalTo(...))`
- `@mockable` annotation on service traits for auto-generated mocks when in-memory is insufficient
- `Gen` + `check` for property-based testing
- Always test: happy path AND error paths

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `ZIO.effect(future.get())` | Blocks thread | `ZIO.fromFuture(_ => future)` |
| Using `Task` everywhere | Loses typed errors | Use `IO[DomainError, A]` |
| `IO[Task[Unit]]` return type | Double-wrapped | Flatten: `UIO[Unit]` |
| Accessor methods on service trait | ZIO 1.x pattern | `ZIO.serviceWithZIO[S](_.method)` |
| `ZLayer` in trait companion | Convention violation | Put in `ImplLive` companion |
| `println` inside effects | Executes outside ZIO control | `ZIO.log*` / `Console.printLine` |
| No `Scope` for cleanup resources | Resource leaks | `ZIO.scoped` / `ZLayer.scoped` |
| `Has[UserRepo]` type | ZIO 1.x, removed | Just `UserRepo` in environment |
| `ZManaged` | Removed in ZIO 2 | `ZIO.scoped` + `acquireRelease` |
| Reflexive error logging | Noise, duplicate logs | Log once at the outermost boundary |
| Manual retry recursion | No backoff, off-by-one | Use `Schedule.exponential` / `retry` |
| Pattern-matching on `Exit` | Misses `Both`/`Then` causes | Use `foldCauseZIO` |
| `catchAll` on `Throwable` | Swallows defects and interrupts | Use `unrefine` to target specific types |
| `ZIO.uninterruptible` around whole effect | Starves interrupt on shutdown | Wrap only the release/cleanup |
| `ZLayer.make` inside per-test `provide` | Rebuilds graph each test | Use `provideSomeShared` for shared resources |
| Cats typeclasses in ZIO projects | Dual dependency, impedance mismatch | Use ZIO Prelude (`Covariant`, `ForEach`, `Validation`) |
| Cats `Validated` for accumulation | Extra dependency | `zio.prelude.Validation[E, A]` |
