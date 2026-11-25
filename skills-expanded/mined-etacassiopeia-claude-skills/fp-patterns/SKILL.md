---
name: fp-patterns
description: >
  Functional programming patterns and anti-patterns for Scala 3. Use this skill
  when designing domain models, implementing typeclasses, composing effects,
  making architecture decisions about ADT structure, or choosing between tagless
  final and concrete effect types. TRIGGER on: ADT design questions, typeclass
  implementation, monad composition, effect system architecture, domain modeling
  with FP, or any question about when to use monads/applicatives/functors. Covers
  algebraic design, typeclass derivation, effect composition, and anti-patterns
  like monad transformers that ZIO makes obsolete.
---

# Functional Programming Patterns

## Algebraic Design — Make Illegal States Unrepresentable

Model with sum types (OR) and product types (AND). The type system should reject invalid states at compile time.

```scala
// Sum type: a payment is EITHER card OR bank transfer (not both)
enum Payment:
  case Card(number: CardNumber, cvv: CVV, expiry: YearMonth)
  case BankTransfer(iban: IBAN, bic: BIC)

// Product type: a user HAS a name AND an email AND a role (all required)
case class User(name: NonEmptyString, email: Email, role: Role)

// Nested — a cart is either empty or has items
enum Cart:
  case Empty
  case Active(items: NonEmptyList[CartItem], appliedCoupon: Option[Coupon])
```

### Smart Constructors

Never expose raw constructors for domain types. Enforce invariants at the boundary.

```scala
object Email:
  opaque type Email = String
  def parse(raw: String): Either[ValidationError, Email] =
    raw.trim match
      case s if s.contains('@') && s.contains('.') => Right(s)
      case s => Left(ValidationError.InvalidEmail(s))
  extension (e: Email) def value: String = e

// Usage — can't construct invalid Email without going through parse
val email: Either[ValidationError, Email] = Email.parse("user@example.com")
```

Use `Either[E, A]` for pure validation, `IO[E, A]` when validation needs effects.

### Refined Primitives via `opaque type`

```scala
object refined:
  opaque type NonEmptyString = String
  object NonEmptyString:
    def apply(s: String): Option[NonEmptyString] = Option(s).filter(_.nonEmpty)
    def unsafeFrom(s: String): NonEmptyString =
      require(s.nonEmpty, "NonEmptyString cannot be empty"); s
  extension (s: NonEmptyString) def value: String = s

  opaque type PosInt = Int
  object PosInt:
    def apply(n: Int): Option[PosInt] = Option(n).filter(_ > 0)
  extension (n: PosInt) def value: Int = n
```

### Phantom Types for State Machines

```scala
sealed trait Unvalidated
sealed trait Validated
sealed trait Submitted

case class Form[S](data: Map[String, String]):
  // Can only call submit on Validated forms — compile-time guarantee
  def submit(using ev: S =:= Validated): Form[Submitted] = ???

def validate(form: Form[Unvalidated]): Either[FormErrors, Form[Validated]] = ???
```

---

## Typeclasses

### Definition — Single Type Parameter Trait

```scala
trait Show[A]:
  def show(a: A): String

trait Eq[A]:
  def eqv(a: A, b: A): Boolean

// Contravariant example
trait Codec[-A]:
  def encode(a: A): Json
```

### Instances — `given` in Companion Objects

```scala
case class UserId(value: UUID)

object UserId:
  given Show[UserId] = id => s"UserId(${id.value})"
  given Eq[UserId] = (a, b) => a.value == b.value
  given Ordering[UserId] = Ordering.by(_.value)
```

### Derivation — Prefer `derives` Clause

```scala
import io.circe.{Encoder, Decoder}

// Automatic derivation at definition site
case class UserEvent(id: UserId, action: String) derives Encoder, Decoder

// Enum derivation
enum Color derives CanEqual:
  case Red, Green, Blue
```

### Access — `summon[TC]`, not `implicitly`

```scala
def printAll[A: Show](items: List[A]): Unit =
  items.foreach(a => println(summon[Show[A]].show(a)))

// Or use context bounds with extension
def display[A](a: A)(using Show[A]): String = summon[Show[A]].show(a)
```

### Least Powerful Constraint

```scala
// Prefer: use Functor when you only need map
def transform[F[_]: Functor, A, B](fa: F[A])(f: A => B): F[B] = fa.map(f)

// Over-constrained — why require Monad if you only call map?
def transform[F[_]: Monad, A, B](fa: F[A])(f: A => B): F[B] = fa.map(f)
```

Hierarchy: `Functor` (map) < `Applicative` (map + zip) < `Monad` (flatMap).

---

## Effect Composition

### Sequential — `flatMap` / for-comprehension

Use for dependent sequential effects where each step needs the previous result.

```scala
val program: IO[AppError, Report] =
  for
    user    <- userRepo.findById(userId)
    orders  <- orderRepo.findByUser(user.id)
    report  <- reportService.generate(user, orders)
  yield report
```

### Parallel — `zipPar` / `collectAllPar` / `foreachPar`

Use when effects are independent — don't sequence what doesn't need to be sequential.

```scala
// Two independent fetches — run in parallel
val (user, config) = ZIO.zipPar(
  userRepo.findById(userId),
  configService.load()
)

// Parallel map over a collection
val users: IO[UserError, List[User]] = ZIO.foreachPar(userIds)(userRepo.findById)

// Bounded parallelism
val results = ZIO.foreachParN(8)(items)(processItem)
```

### Error Accumulation — `validate` / `validatePar`

```scala
// Fail-fast (flatMap): stops at first error
val result1: IO[Error, (A, B, C)] =
  for { a <- opA; b <- opB; c <- opC } yield (a, b, c)

// Accumulate: collects ALL errors
val result2: IO[::[Error], (A, B, C)] =
  ZIO.validate((opA, opB, opC))(identity)
```

### Streaming — `ZStream` / `ZPipeline` / `ZSink`

Use ZStream for data that doesn't fit in memory or arrives continuously.

```scala
val pipeline: ZStream[Any, Error, Report] =
  ZStream.fromIterable(eventIds)         // source
    .mapZIO(id => eventStore.load(id))  // fetch
    .via(deduplicationPipeline)          // transform
    .grouped(100)                        // batch
    .mapZIO(batch => reportSvc.generate(batch))  // aggregate

// Run to completion
pipeline.run(ZSink.collectAll)       // accumulate
pipeline.run(ZSink.foreach(persist)) // side-effect per element
```

---

## Tagless Final vs Concrete ZIO

**Default: use concrete ZIO types** in application code.

```scala
// Concrete (preferred for application services)
trait UserRepo:
  def find(id: UserId): IO[UserNotFound, User]

// Tagless final — only for genuinely polymorphic library code
trait UserRepo[F[_]]:
  def find(id: UserId): F[User]
```

Use tagless final only when:
- Building a library that must work with multiple effect systems
- You have a proven need for polymorphism across `F[_]`

The ZIO ecosystem (ZLayer, ZStream, zio-test) is rich enough that `F[_]` abstraction rarely pays off in application code.

If you do use tagless final:
- Constrain `F[_]` to the least powerful typeclass needed
- Avoid `Monad` when `Applicative` suffices
- Document why polymorphism is needed

---

## Anti-Patterns

### Monad Transformers — Don't Use Them

```scala
// Anti-pattern — EitherT / OptionT stacking
def findUser(id: UserId): EitherT[Task, UserError, User] = ???
def findOrder(user: User): OptionT[Task, Order] = ???

// Result: callers must unwrap at every boundary, types infect your API

// Correct in ZIO — use the native error channel and Option combinators
def findUser(id: UserId): IO[UserError, User] = ???
def findOrder(user: User): UIO[Option[Order]] = ???

// ZIO.getOrFail, .some, .someOrFail handle Option lifting
val order: IO[OrderNotFound, Order] =
  findOrder(user).someOrFail(OrderNotFound(user.id))
```

### Reflexive IO Wrapping

```scala
// Anti-pattern — pure computation wrapped in IO for no reason
def add(a: Int, b: Int): UIO[Int] = ZIO.succeed(a + b)

// Correct — pure functions stay pure
def add(a: Int, b: Int): Int = a + b

// Only wrap at boundaries with actual side effects
def currentTime(): UIO[Instant] = ZIO.succeed(Instant.now())  // OK: real side effect
```

### Mutable State for Concurrency

```scala
// Anti-pattern — var in a ZIO service
class CounterLive extends Counter:
  private var count = 0  // NOT SAFE under fibers
  def increment: UIO[Unit] = ZIO.succeed { count += 1 }

// Correct — Ref for atomic shared state
case class CounterLive(ref: Ref[Int]) extends Counter:
  def increment: UIO[Unit] = ref.update(_ + 1)
  def get: UIO[Int] = ref.get

object CounterLive:
  val layer: ULayer[Counter] = ZLayer.fromZIO(Ref.make(0).map(CounterLive(_)))
```

### Non-Tail-Recursive Loops

```scala
// Anti-pattern — stack overflow for large n
def sum(n: Int): Int =
  if n <= 0 then 0
  else n + sum(n - 1)  // not tail-recursive

// Correct — tail-recursive
@scala.annotation.tailrec
def sum(n: Int, acc: Int = 0): Int =
  if n <= 0 then acc
  else sum(n - 1, acc + n)

// Or ZIO's built-in recursion
def sumZIO(n: Int): UIO[Int] = ZIO.loop(n)(_ > 0, _ - 1)(i => ZIO.succeed(i)).map(_.sum)
```

### Summary Anti-Pattern Table

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `EitherT[Task, E, A]` / `OptionT[Task, A]` | API infection, unwrapping burden | Use ZIO error channel + `.some`/`.someOrFail` |
| `ZIO.succeed(pureFn(a, b))` | Unnecessary lifting | Keep pure functions pure |
| `var` for concurrent state | Data races under fibers | `Ref`, `Queue`, `Hub`, `STM` |
| Non-tail-recursive loops | Stack overflow | `@tailrec` or `ZIO.loop` |
| `implicitly[TC]` | Scala 2 style | `summon[TC]` |
| Over-constraining with `Monad` | Forces unnecessary power | Use `Functor` or `Applicative` when sufficient |
| Tagless final in application code | Indirection without payoff | Concrete ZIO types |
| Anemic domain model | Logic scattered across services | Behavior belongs on domain types |
| Accumulate into `List` from stream | OOM risk | `ZStream` + `ZSink` |
