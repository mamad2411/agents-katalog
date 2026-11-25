---
name: cats-ecosystem
description: >
  Cats Core typeclasses, Cats Effect 3, FS2, Doobie, Http4s, and Kyo for
  pure functional Scala without ZIO. TRIGGER when: code imports cats.*,
  cats.effect.*, fs2.*, doobie.*, http4s.*, org.http4s.*, when building
  tagless-final services with F[_] constraints, composing IO effects, managing
  resources with Resource[F, A], streaming with FS2 Stream, querying
  databases with Doobie, or comparing effect systems (Cats Effect vs ZIO vs
  Kyo). Also use for: Validated/ValidatedNel accumulation, Kleisli composition,
  MonoidK, NonEmptyList/NonEmptyChain, or any Cats data type question.
---

# Cats Ecosystem — Pure Functional Scala

## Effect System Choice

| System | Type | Style | Best for |
|---|---|---|---|
| **Cats Effect 3** | `IO[A]` | monadic | Typelevel ecosystem (FS2, Doobie, Http4s, Skunk) |
| **ZIO 2** | `ZIO[R, E, A]` | monadic | Service pattern, typed deps, ZIO-native ecosystem |
| **Kyo** | `A < Effects` | direct | Minimal overhead, direct style, emerging ecosystem |

When **not** on ZIO: use Cats Effect 3 as the default effect type for application code. Use tagless final (`F[_]` constraints) only for shared library code.

---

## Cats Core Typeclasses

### Hierarchy

```
Functor   → Applicative → Monad
                        → ApplicativeError → MonadError
          → Apply (independent zip)
Foldable  ↘
            Traverse (= Functor + Foldable with effects)
Functor   → Contravariant (contramap)
          → Invariant (imap — both map and contramap)
Semigroup → Monoid         (value-level combine)
SemigroupK → MonoidK       (F[_]-level combine / alternative)
```

### Key Typeclasses in Practice

```scala
import cats.*
import cats.syntax.all.*

// Functor: map over the value
List(1, 2, 3).map(_ * 2)

// Applicative: combine independent effects, lift pure values
val opt: Option[(Int, String)] = (Some(42), Some("hi")).tupled
val validated = (validateAge(n), validateName(s)).mapN(User.apply)

// Monad: sequential dependent effects
def findOrder(userId: String): IO[Option[Order]] =
  for
    user  <- userRepo.find(userId)
    order <- user.traverse(u => orderRepo.findLatest(u.id))
  yield order.flatten

// Traverse: map with effects, preserving structure
val results: IO[List[User]] = ids.traverse(id => fetchUser(id))
val parallel: IO[List[User]] = ids.parTraverse(id => fetchUser(id))

// Foldable: reduce a structure
List(1, 2, 3).foldMap(n => List(n.toString))   // List("1","2","3")
NonEmptyList.of(1, 2, 3).reduceLeft(_ + _)       // 6

// SemigroupK / MonoidK: combine F[A] structures
val routes: HttpRoutes[IO] = routesA <+> routesB   // MonoidK combine
val orElse: Option[Int]    = None <+> Some(42)     // Some(42)
```

### Validated — Pure Error Accumulation

```scala
import cats.data.*

type ValidationResult[A] = ValidatedNel[String, A]

def validateName(s: String): ValidationResult[String] =
  if s.nonEmpty then s.validNel else "name is empty".invalidNel

def validateAge(n: Int): ValidationResult[Int] =
  if n >= 0 then n.validNel else "age must be non-negative".invalidNel

def validateEmail(s: String): ValidationResult[String] =
  if s.contains('@') then s.validNel else "invalid email".invalidNel

// Applicative combination — accumulates ALL errors
val user: ValidationResult[User] =
  (validateName(name), validateAge(age), validateEmail(email)).mapN(User.apply)

// vs Either — fails on first error
val userEither: Either[String, User] =
  for
    n <- validateName(name).toEither.left.map(_.head)
    a <- validateAge(age).toEither.left.map(_.head)
    e <- validateEmail(email).toEither.left.map(_.head)
  yield User(n, a, e)
```

Use `Validated` at the validation layer; convert to `Either`/`IO` for the rest of the program.

### Kleisli — Composing Effectful Functions

```scala
import cats.data.Kleisli

// Kleisli[F, A, B] wraps A => F[B]
type Middleware[F[_], A, B] = Kleisli[F, A, B]

val authenticate: Kleisli[IO, Request, User]   = Kleisli(req => verifyToken(req.token))
val authorize:    Kleisli[IO, User, Permission] = Kleisli(user => checkPermission(user))
val handle:       Kleisli[IO, Permission, Response] = Kleisli(perm => handleRequest(perm))

// Compose: output feeds next input
val pipeline = authenticate andThen authorize andThen handle

// Run
pipeline.run(request)  // IO[Response]

// Http4s middleware is literally Kleisli under the hood
```

### NonEmptyList and NonEmptyChain

```scala
import cats.data.*

// Use when empty is invalid — encodes invariant in the type
def firstUser(users: NonEmptyList[User]): User = users.head  // always safe
def combineErrors(errs: NonEmptyList[Error]): Error = errs.reduce

// Constructing
NonEmptyList.of(1, 2, 3)
NonEmptyList.fromList(list).getOrElse(???)  // handle empty explicitly
list.toNel  // Option[NonEmptyList[A]] — explicit about the possibility of empty

// NonEmptyChain: O(1) append (prefer for error accumulation)
NonEmptyChain.of("err1", "err2").append("err3")
```

---

## Cats Effect 3

### IO — Pure Lazy Effects

```scala
import cats.effect.*

// Constructors
IO.pure(42)                         // pure value — must be already evaluated
IO.delay(sideEffect())              // synchronous side effect — lazy
IO.blocking(blockingCall())         // blocking I/O — runs on blocking thread pool
IO.async_[A] { cb => ... }         // async callback
IO.fromFuture(IO(futureCall()))     // interop with Scala Future
IO.fromEither(either)              // lift Either — Left becomes IO.raiseError

// Combining
(io1, io2).tupled         // sequential
(io1, io2).parTupled      // parallel (starts both, waits for both)
(io1, io2).parMapN(f)     // parallel map
io.race(io2)              // first wins, other is cancelled

// Fibers
io.start.flatMap { fiber =>
  fiber.join.flatMap {
    case Outcome.Succeeded(fa) => fa
    case Outcome.Errored(e)    => IO.raiseError(e)
    case Outcome.Canceled()    => IO.canceled
  }
}

// IOApp — application entry point
object Main extends IOApp.Simple:
  def run: IO[Unit] = program
```

### Resource — Safe Resource Management

```scala
val connection: Resource[IO, Connection] = Resource.make(
  IO.blocking(openConnection(url))        // acquire
)(conn => IO.blocking(conn.close()).void) // release — always runs

// Compose resources
val app: Resource[IO, (Connection, Cache)] = for
  conn  <- connection
  cache <- Cache.resource(maxSize = 1000)
yield (conn, cache)

// Use
app.use { (conn, cache) =>
  serve(conn, cache)
}  // connection and cache closed when done or on error

// In a layer-like pattern
val serverResource: Resource[IO, Server] = for
  db     <- Database.resource(config.db)
  cache  <- Cache.resource(config.cache)
  routes  = buildRoutes(db, cache)
  server <- BlazeServerBuilder[IO].bindHttp(8080).withHttpApp(routes).resource
yield server
```

### Concurrent Primitives

```scala
// Ref: atomic mutable cell (never use var)
val counter: IO[Ref[IO, Int]] = Ref.of[IO](0)
counter.flatMap { ref =>
  ref.update(_ + 1) *>      // atomic update
  ref.modify(n => (n + 1, n)) // read + update atomically, return old value
}

// Deferred: single-use async handoff (Promise equivalent)
Deferred[IO, Result].flatMap { deferred =>
  producer.flatMap(deferred.complete).start *>
  deferred.get  // suspends until completed
}

// Queue: bounded FIFO channel
Queue.bounded[IO, Task](capacity = 128).flatMap { queue =>
  producer.flatMap(queue.offer).start *>
  queue.take.flatMap(process)
}

// Semaphore: bound concurrency
Semaphore[IO](n = 4).flatMap { sem =>
  items.parTraverse(item => sem.permit.use(_ => process(item)))
}
```

---

## FS2 Streams

`Stream[F, A]` — lazy, pull-based, resource-safe, chunked.

```scala
import fs2.*
import fs2.io.*

// Sources
Stream.emit(1)                           // single element
Stream.emits(List(1, 2, 3))             // from collection
Stream.eval(IO(computeValue()))          // lift effect
Stream.repeatEval(IO(poll()))            // infinite effectful stream
Stream.resource(Resource.make(...)(...)  // resource-safe stream

// Transforms
stream
  .filter(_ > 0)
  .map(_ * 2)
  .evalMap(n => IO(processItem(n)))     // effectful map, sequential
  .parEvalMap(maxConcurrent = 8)(n => IO(processItem(n)))  // parallel
  .chunks                               // expose Chunk[A] level
  .chunkN(100)                          // batch into chunks of 100
  .groupWithin(100, 1.second)           // batch by count OR time

// Pipes (Stream[F,A] => Stream[F,B])
val dedup: Pipe[IO, Event, Event] = stream =>
  stream.zipWithPrevious.collect {
    case (prev, curr) if !prev.contains(curr) => curr
  }

stream.through(dedup).through(encode).through(fs2.io.writeOutputStream(out))

// Concurrency
stream1.merge(stream2)                  // interleave two streams concurrently
stream1.zip(stream2)                    // pair elements
Stream(stream1, stream2).parJoin(2)     // run N streams concurrently

// Sinks / running
stream.compile.toList                   // IO[List[A]] — collect
stream.compile.drain                    // IO[Unit] — run for effects
stream.compile.fold(zero)(f)            // IO[B] — fold to single value
```

---

## Doobie — Functional Database Access

```scala
import doobie.*
import doobie.implicits.*
import cats.effect.*

// Transactor: manages connection pool and transaction boundaries
val xa = Transactor.fromDriverManager[IO](
  driver = "org.postgresql.Driver",
  url    = "jdbc:postgresql://localhost/mydb",
  user   = "user",
  pass   = "password"
)

// Queries: sql interpolation → ConnectionIO (runs inside a transaction)
def findUser(id: UUID): ConnectionIO[Option[User]] =
  sql"SELECT id, name, email FROM users WHERE id = $id"
    .query[User]          // Query0[User] — map row to User
    .option               // ConnectionIO[Option[User]]

def listUsers: ConnectionIO[List[User]] =
  sql"SELECT id, name, email FROM users"
    .query[User]
    .to[List]

def insertUser(u: User): ConnectionIO[Int] =
  sql"INSERT INTO users (id, name, email) VALUES (${u.id}, ${u.name}, ${u.email})"
    .update
    .run              // ConnectionIO[Int] — rows affected

// Fragment composition for dynamic queries
def search(name: Option[String], minAge: Option[Int]): ConnectionIO[List[User]] =
  val base = fr"SELECT id, name, age FROM users"
  val conds = List(
    name.map(n => fr"name ILIKE ${"%" + n + "%"}"),
    minAge.map(a => fr"age >= $a")
  ).flatten
  val where = NonEmptyList.fromList(conds).map(Fragments.whereAnd(_: _*)).getOrElse(Fragment.empty)
  (base ++ where).query[User].to[List]

// Run: transact converts ConnectionIO → IO
val users: IO[List[User]] = listUsers.transact(xa)

// Sequence queries in one transaction
val result: IO[(Option[User], Int)] =
  (findUser(id), insertUser(newUser)).tupled.transact(xa)

// Custom type mapping
given Meta[UUID] = Meta[String].timap(UUID.fromString)(_.toString)
given Meta[Status] = Meta[String].timap(Status.valueOf)(_.name)
```

---

## Http4s — Typeful HTTP

```scala
import org.http4s.*
import org.http4s.dsl.io.*
import org.http4s.circe.*
import io.circe.generic.auto.*

// Routes: partial function over Request → Response (wrapped in OptionT)
val routes: HttpRoutes[IO] = HttpRoutes.of[IO] {
  case GET  -> Root / "users" / id =>
    userService.find(id).flatMap {
      case Some(user) => Ok(user)
      case None       => NotFound()
    }
  case req @ POST -> Root / "users" =>
    for
      body <- req.as[CreateUserRequest]
      user <- userService.create(body)
      resp <- Created(user)
    yield resp
}

// JSON codecs via Circe (add http4s-circe dependency)
given [A: io.circe.Encoder]: EntityEncoder[IO, A] = jsonEncoderOf
given [A: io.circe.Decoder]: EntityDecoder[IO, A] = jsonOf

// Middleware: HttpRoutes[F] => HttpRoutes[F]
val loggedRoutes = Logger.httpRoutes[IO](logHeaders = true, logBody = false)(routes)
val authedRoutes = AuthMiddleware(authUser)(authedHandler)

// Combine routes
val app: HttpApp[IO] = (routes <+> otherRoutes).orNotFound
```

---

## Kyo — Intersection-Type Effects

Kyo represents effects as intersection types — no monadic wrapping, direct style.

```scala
import kyo.*

// Effects expressed as intersection types, not wrappers
def getUser(id: String): User < (Abort[NotFound] & IO) =
  IO(db.findUser(id)).map {
    case None    => Abort.fail(NotFound(id))
    case Some(u) => u
  }

// Compose without flatMap — direct style
def workflow(id: String): Report < (Abort[AppError] & IO) =
  val user   = getUser(id)
  val orders = IO(db.findOrders(user.id))
  Report(user, orders)

// Handle effects layer by layer
val result: Either[NotFound, User] < IO = Abort.run(getUser("123"))
val io: IO[Either[NotFound, User]]      = IO.run(result)
```

Kyo is emerging (2024+). Best for new greenfield services where minimal overhead and direct style matter. Ecosystem is still growing — Cats Effect is safer for production today.

---

## Tagless Final — When and How

```scala
// Use F[_] constraints ONLY for library code that must work across effect systems
// Application code: use IO directly

trait UserRepo[F[_]]:
  def find(id: String): F[Option[User]]
  def save(user: User): F[Unit]

// Constrain to the least powerful typeclass you need
class UserRepoImpl[F[_]: Sync](xa: Transactor[F]) extends UserRepo[F]:
  def find(id: String): F[Option[User]] = sql"...".query[User].option.transact(xa)
  def save(user: User): F[Unit]         = sql"...".update.run.transact(xa).void

// Application wiring: fix F = IO at the top
val repo: UserRepo[IO] = new UserRepoImpl[IO](xa)
```

Tagless final hierarchy for constraints:
- `Functor[F]` — `map` only
- `Applicative[F]` — `pure` + parallel composition
- `Monad[F]` — `flatMap` (sequential)
- `MonadError[F, E]` — `raiseError` + `handleErrorWith`
- `Sync[F]` — `delay`, synchronous effects
- `Async[F]` — `async`, callback-style interop
- `Concurrent[F]` — fibers, racing, cancellation
- `Temporal[F]` — `sleep`, time

Always constrain to the weakest typeclass sufficient. Avoid `Monad` when `Applicative` enables parallel execution.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `Future` for effects | Not referentially transparent, eager, thread-unsafe | `IO.fromFuture(IO(future))` at boundaries only |
| `EitherT[IO, E, A]` everywhere | Transformer stack, `.value` everywhere | `IO[Either[E, A]]` or `IO.raiseError` with typed errors |
| `OptionT[IO, A]` for missing values | Same transformer noise | `IO[Option[A]]` + `.flatMap(_.liftTo[IO](err))` |
| `Validated` for sequential validation | Errors don't accumulate (use `Either`) | `Validated` only when ALL errors should be reported |
| `for` comprehension for independent effects | Forces sequential execution | `(io1, io2).parTupled` or `parTraverse` |
| `var` for concurrent state | Data races | `Ref[IO, A]` |
| `Resource` without `use` | Acquire without release guarantee | Always `resource.use { ... }` |
| `Monad` constraint when `Applicative` suffices | Prevents parallel combinator | Use `Applicative` + `parTraverse` |
| `stream.toList` on infinite stream | OOM | `.take(n)` or `compile.drain` with side effects |
| Tagless final in application code | Indirection with no payoff | Concrete `IO` in applications; `F[_]` only in libraries |
