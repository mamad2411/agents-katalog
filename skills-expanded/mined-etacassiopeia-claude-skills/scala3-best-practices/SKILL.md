---
name: scala3-best-practices
description: >
  Comprehensive Scala 3 coding standards, idioms, and anti-pattern prevention.
  Use this skill whenever writing, reviewing, or refactoring Scala 3 code —
  including new files, type design, syntax choices, metaprogramming, and
  visibility decisions. TRIGGER on any .scala file work, build.sbt changes,
  or questions about how to structure Scala 3 code correctly. Always consult
  before generating non-trivial Scala 3 — it encodes decisions that are easy
  to get wrong (AnyVal vs opaque type, implicit vs given, sealed vs enum).
---

# Scala 3 Best Practices

## Syntax Essentials

### Sum Types — always `enum`, never sealed hierarchies for new code

```scala
// Prefer
enum Color:
  case Red, Green, Blue

enum Shape:
  case Circle(radius: Double)
  case Rectangle(width: Double, height: Double)

// Avoid — verbose, no added value in Scala 3
sealed trait Shape
case class Circle(radius: Double) extends Shape
case class Rectangle(w: Double, h: Double) extends Shape
```

`enum` supports methods, companion objects, `derives`, and exhaustiveness checks just like sealed hierarchies.

### Newtypes — always `opaque type`, never `AnyVal`

```scala
// Prefer — zero-cost, no boxing, proper encapsulation
object Domain:
  opaque type UserId = UUID
  object UserId:
    def apply(raw: UUID): UserId = raw
    def fromString(s: String): Either[String, UserId] =
      Try(UUID.fromString(s)).toEither.left.map(_.getMessage)
  extension (id: UserId) def value: UUID = id

// Avoid — deprecated pattern, has boxing edge cases
class UserId(val value: UUID) extends AnyVal
```

### Implicits — always `given`/`using`, never `implicit`

```scala
// Prefer
given Ordering[UserId] = Ordering.by(_.value)
def sorted[A](xs: List[A])(using ord: Ordering[A]): List[A] = xs.sorted

// Avoid — Scala 2 style, will be deprecated
implicit val userIdOrdering: Ordering[UserId] = Ordering.by(_.value)
def sorted[A](xs: List[A])(implicit ord: Ordering[A]): List[A] = xs.sorted
```

### Extension Methods — always `extension`, never implicit classes

```scala
// Prefer
extension (s: String)
  def trimmedNonEmpty: Option[String] = Option(s.trim).filter(_.nonEmpty)

// Avoid
implicit class StringOps(val s: String):
  def trimmedNonEmpty: Option[String] = Option(s.trim).filter(_.nonEmpty)
```

### Typeclass Derivation — use `derives` clause

```scala
import io.circe.{Encoder, Decoder}

case class UserEvent(userId: UserId, action: String) derives Encoder, Decoder

enum Status derives CanEqual:
  case Active, Inactive, Pending
```

### Context Functions — for capability/reader patterns

```scala
// Context function type: the `?=>` arrow
type Contextual[A] = Config ?=> A

def withTimeout[A](op: Contextual[A])(using config: Config): A =
  op // Config is passed implicitly into op
```

### Braceless Syntax — pick one style and be consistent

```scala
// Preferred: significant indentation throughout
def compute(n: Int): Int =
  if n < 0 then -n
  else n * 2

// Acceptable: braces throughout — just don't mix
def compute(n: Int): Int = {
  if (n < 0) { -n }
  else { n * 2 }
}
```

---

## Type Design

### Enforce Invariants at Construction

```scala
object Email:
  opaque type Email = String
  def parse(raw: String): Either[String, Email] =
    if raw.contains('@') then Right(raw) else Left(s"Invalid email: $raw")
  extension (e: Email) def value: String = e
```

Smart constructors return `Either[E, A]` or `IO[E, A]` — never expose raw constructors for domain types.

### State Machines with Enums

```scala
enum Connection[+S]:
  case Open(socket: Socket) extends Connection[Open.type]
  case Closed extends Connection[Closed.type]

// Phantom types: illegal transitions become compile errors
def send(conn: Connection[Open.type], data: Array[Byte]): IO[Error, Unit] = ???
def close(conn: Connection[Open.type]): IO[Error, Connection[Closed.type]] = ???
```

### Visibility — default to restrictive

```scala
private[domain] class UserRepoLive(db: Database) extends UserRepo  // visible within domain package
private[this] val cache: Map[UserId, User] = Map.empty             // visible only in this instance
```

Only `public` (`pub`) what is genuinely part of the API surface. Default to `private[package]`.

### Phantom Types for Compile-Time Guarantees

```scala
sealed trait Unvalidated
sealed trait Validated

case class Input[+S](value: String)

def validate(raw: Input[Unvalidated]): Either[String, Input[Validated]] = ???
def process(input: Input[Validated]): Result = ???  // Can't pass unvalidated accidentally
```

---

## Metaprogramming — Prefer Simpler Tools First

**Decision order**: `derives` clause → `inline` → macros (quotes/splices) → low-level reflection (almost never)

```scala
// Step 1: try derives first
case class Foo(x: Int, y: String) derives Show, Codec

// Step 2: inline for compile-time computation
inline def fieldCount[A]: Int = compiletime.constValue[compiletime.Erased[A]]

// Step 3: macros with quotes/splices when inline is insufficient
import scala.quoted.*
def myMacroImpl[A: Type](using Quotes): Expr[String] =
  '{ ${ Expr(Type.show[A]) } }  // Use quotes/splices — never manual AST
```

**Never**: use `scala.reflect` (Scala 2 API), raw `Tree` manipulation, or `mirrors.derived` when `derives` works.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `class UserId(val v: UUID) extends AnyVal` | Boxing edge cases, deprecated | `opaque type UserId = UUID` |
| `implicit val x: TC = ...` | Scala 2 syntax | `given x: TC = ...` |
| `sealed trait + case class/object` for simple sums | Boilerplate | `enum` |
| `String`/`Int`/`UUID` in public APIs | No domain safety | Wrap in `opaque type` |
| Mixing braceless and braced syntax | Inconsistency | Pick one, use everywhere |
| `implicitly[TC]` | Scala 2 style | `summon[TC]` |
| Macros for anything `derives` handles | Over-engineering | Use `derives` clause |
| Deep sealed hierarchy when flat enum suffices | Complexity | Flatten to `enum` |

---

## Style & Formatting

- 2-space indentation
- Configure `scalafmt` with `runner.dialect = scala3`
- Compile with `-Xfatal-warnings` — zero warnings in CI
- Max line length: 100 chars
- Prefer `NonEmptyList`/`NonEmptyChain` over bare collections when emptiness is invalid
- Use `@main` annotation for entry points, not `extends App`

```scala
@main def run(args: String*): Unit =
  // entry point — no extends App
```

## Build Verification

```sh
sbt compile
sbt scalafmtCheckAll
sbt test
```
