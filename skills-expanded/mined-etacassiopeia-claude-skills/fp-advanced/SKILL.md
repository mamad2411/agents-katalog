---
name: fp-advanced
description: >
  Advanced functional programming patterns grounded in category theory, for
  Scala 3 / ZIO projects. TRIGGER when: working with ZIO Prelude typeclasses
  (Covariant, Contravariant, ForEach, Validation, Associative), composing
  effectful pipelines with Kleisli, writing natural transformations (F ~> G),
  building interpreters with Free monad or ZPure, modeling recursive data
  (Fix/cata/ana), implementing bidirectional codecs (Profunctor/dimap),
  using optics (Lens, Prism, Traversal via Monocle), or when any category
  theory concept needs a concrete Scala 3 implementation. Use alongside
  /fp-patterns and /zio-best-practices.
---

# Advanced FP — Category Theory Applied to Scala 3 / ZIO

## ZIO Prelude Typeclasses

ZIO-native alternative to Cats. Prefer these over Cats in ZIO projects.

```scala
import zio.prelude.*

// Covariant = Functor: map over F[+_]
// Contravariant: contramap over F[-_]
// ForEach = Traverse: sequence effects, preserving structure

// Derive structural instances at definition site
case class UserId(value: UUID)    derives Equal, Hash, Ord
enum Status derives Equal:
  case Active, Inactive

// Validation: pure error accumulation — no ZIO needed
// E must be Associative so errors can be combined
val validated: Validation[String, User] =
  Validation.validate(
    Validation.fromPredicateWith("name empty")(name)(_.nonEmpty),
    Validation.fromPredicateWith("age negative")(age)(_ >= 0)
  )(User.apply)

// Collect all errors, not just the first
val result: Either[NonEmptyChunk[String], User] = validated.toEither
```

Value-level algebra — use when combining domain values:
```scala
// Associative = Semigroup (associative combine)
// Identity    = Monoid    (combine + zero element)
// Commutative = combine(a,b) == combine(b,a)

given Associative[Stats] with
  def combine(l: => Stats, r: => Stats): Stats = Stats(l.count + r.count)

given Identity[Stats] = Identity.make(Stats(0))

// ForEach to traverse a structure with effects
val effects: List[IO[E, A]] = ???
val results: IO[E, List[A]] = ZIO.foreach(effects)(identity)
// Or with ZIO Prelude's ForEach:
// ForEach[List].forEach(effects)(identity)
```

---

## Kleisli — Composing Effectful Functions

`A => ZIO[R, E, B]` is a Kleisli arrow. Compose with flatMap — no wrapper type needed.

```scala
// Three pipeline stages with different typed errors
val parse:    String => IO[ParseError, Json]       = ???
val validate: Json   => IO[ValidationError, Input] = ???
val process:  Input  => IO[ProcessError, Output]   = ???

// Compose into a single pipeline — translate errors to a common type
def pipeline(raw: String): IO[AppError, Output] =
  for
    json   <- parse(raw)   .mapError(AppError.Parse(_))
    input  <- validate(json).mapError(AppError.Validation(_))
    output <- process(input).mapError(AppError.Processing(_))
  yield output

// For middleware chains, lift to a function explicitly:
val fullPipeline: String => IO[AppError, Output] =
  parse(_).mapError(AppError.Parse(_))
    .flatMap(validate(_).mapError(AppError.Validation(_)))
    .flatMap(process(_) .mapError(AppError.Processing(_)))
```

Use Kleisli when: building data pipelines, middleware chains, multi-stage validation where each step has its own typed error.

---

## Natural Transformations — F ~> G

Converts `F[A]` to `G[A]` for any `A` without knowing what `A` is.

```scala
// Encode as a trait (Scala 3 — no kind-projector needed)
trait ~>[F[_], G[_]]:
  def apply[A](fa: F[A]): G[A]

val optionToList: Option ~> List = new (Option ~> List):
  def apply[A](fa: Option[A]): List[A] = fa.toList

// Main use case: effect interpreters for tagless-final algebras
trait Storage[F[_]]:
  def load(key: String): F[Array[Byte]]

// Swap in a test interpreter without changing algebra
val inMemory: Storage[IO[StorageError, _]]  = ???
val toTask:   IO[StorageError, _] ~> Task   = new:
  def apply[A](fa: IO[StorageError, A]): Task[A] = fa.orDie

// Also useful for: swapping effect systems in legacy interop,
// compiling Free monads into ZIO
```

---

## Bifunctor, Contravariant, Profunctor

### Bifunctor — map both type parameters independently

ZIO `[R, E, A]` is a bifunctor over `E` and `A`:
```scala
// map = rightward, mapError = leftward, bimap = both at once
userService.findUser(id)
  .bimap(
    e => ApiError.fromDomain(e),  // translate error at bounded-context boundary
    u => UserDto.from(u)          // transform success into response type
  )
```

### Contravariant — reverse the arrow

`F[A]` is contravariant when `A => B` gives `F[B] => F[A]`:
```scala
// Encoder[-A] is contravariant — if you can encode B, you can encode A => B
trait Encoder[-A]:
  def encode(a: A): Json
  def contramap[B](f: B => A): Encoder[B] = b => encode(f(b))

given Encoder[String] = Json.Str(_)

val uuidEncoder: Encoder[UUID]   = summon[Encoder[String]].contramap(_.toString)
val emailEncoder: Encoder[Email] = summon[Encoder[String]].contramap(_.value)

// Ordering is also contravariant
val byName: Ordering[User] = Ordering.String.on(_.name)
```

### Profunctor — contravariant in input, covariant in output

`F[-A, +B]`: use `dimap` to transform both ends simultaneously:
```scala
// Codec[-A, +B]: encode A, decode to B
trait Codec[-A, +B]:
  def encode(a: A): Bytes
  def decode(b: Bytes): Option[B]
  def dimap[C, D](f: C => A)(g: B => D): Codec[C, D]

val intCodec: Codec[Int, Int] = ???
val stringIntCodec: Codec[String, Int] = intCodec.dimap(_.toInt)(identity)
```

Use profunctors for: bidirectional serialization, optics (Lens is a Profunctor), protocol adapters. **Don't force profunctor abstractions onto simple covariant/contravariant types.**

---

## Optics (Monocle 3.x)

Compose getters and setters over nested immutable data structures.

```scala
import monocle.*
import monocle.syntax.all.*

case class Address(street: String, city: String)
case class User(name: String, address: Address)

// Lens: total get + set for a field
val streetLens: Lens[User, String] = Focus[User](_.address.street)

streetLens.get(user)                     // "Main St"
streetLens.replace("Oak Ave")(user)      // updated User
streetLens.modify(_.toUpperCase)(user)   // transformed User

// Prism: partial get for a sum type case
val circlePrism: Prism[Shape, Double] = Prism.partial[Shape, Double] {
  case Shape.Circle(r) => r
}(Shape.Circle.apply)

circlePrism.getOption(shape)    // Some(r) or None
circlePrism.reverseGet(3.14)    // Shape.Circle(3.14)

// Optional: partial get + total set (Lens ∘ Prism)
val headOptional: Optional[List[Int], Int] =
  Optional[List[Int], Int](_.headOption)(x => { case _ :: t => x :: t; case Nil => Nil })

// Traversal: focus on MULTIPLE values at once
val allCities: Traversal[List[User], String] =
  Traversal.fromTraverse[List, User].andThen(Focus[User](_.address.city))

allCities.getAll(users)                 // List[String]
allCities.modify(_.toLowerCase)(users)  // all cities lowercased
```

| Optic | `F[-,+]` | Get | Set | When |
|---|---|---|---|---|
| `Lens[S,A]` | total–total | `A` | always | Required field |
| `Prism[S,A]` | partial–total | `Option[A]` | always | Enum variant |
| `Optional[S,A]` | partial–total | `Option[A]` | always | Optional field |
| `Traversal[S,A]` | many–total | `List[A]` | always | Collection / multi-focus |

Compose optics with `andThen`. **Only use optics for genuinely nested or multi-focus operations; direct field access is clearer for flat data.**

---

## Recursive Schemes — Separating Recursion from Computation

Encode recursive data as non-recursive functors, apply algebras with `cata` / `ana`.

```scala
// Non-recursive functor — the "shape" of one level
enum ExprF[+A]:
  case Num(n: Int)
  case Add(l: A, r: A)
  case Mul(l: A, r: A)

given Functor[ExprF] = ...  // or use droste's Functor derivation

// Fix[F] ties the recursive knot: Fix[F] = F[Fix[F]]
case class Fix[F[_]](unfix: F[Fix[F]])
type Expr = Fix[ExprF]

// Smart constructors
def num(n: Int): Expr        = Fix(ExprF.Num(n))
def add(l: Expr, r: Expr): Expr = Fix(ExprF.Add(l, r))

// Catamorphism (fold): collapse a Fix[F] into a value bottom-up
def cata[F[_]: Functor, A](alg: F[A] => A)(fix: Fix[F]): A =
  alg(fix.unfix.map(cata(alg)))

// An algebra is just F[A] => A
val eval: ExprF[Int] => Int =
  case ExprF.Num(n)    => n
  case ExprF.Add(l, r) => l + r
  case ExprF.Mul(l, r) => l * r

cata(eval)(add(num(3), mul(num(2), num(4))))  // 11

// Anamorphism (unfold): build a Fix[F] from a seed
def ana[F[_]: Functor, A](coalg: A => F[A])(seed: A): Fix[F] =
  Fix(coalg(seed).map(ana(coalg)))

// Use droste (github.com/higherkindness/droste) in production
// It provides Basis[T, F], scheme, cata, ana, hylo, and law tests
```

Use recursive schemes when: your domain model is a tree/AST, you need multiple independent passes (eval + pretty-print + type-check), or you want to defer recursion strategy to the caller.

---

## Free Monad — Programs as Data

Represent a program as a pure data structure; interpret separately.

```scala
// Algebra: the set of operations (not implementations)
enum StoreOp[+A]:
  case Get(key: String)              extends StoreOp[Option[String]]
  case Put(key: String, value: String) extends StoreOp[Unit]
  case Delete(key: String)           extends StoreOp[Unit]

// In ZIO ecosystem, use ZPure for pure programs or ZIO with test layers
// ZPure[W, S1, S2, R, E, A] — stateful, traceable pure computation
import zio.prelude.fx.ZPure

type Store[+A] = ZPure[Nothing, Map[String, String], Map[String, String], Any, Nothing, A]

object Store:
  def get(key: String): Store[Option[String]]       = ZPure.get.map(_.get(key))
  def put(key: String, v: String): Store[Unit]      = ZPure.update(_.updated(key, v))
  def delete(key: String): Store[Unit]              = ZPure.update(_ - key)

// Programs compose naturally via flatMap
val program: Store[Option[String]] = for
  _     <- Store.put("x", "hello")
  value <- Store.get("x")
yield value

// Run against different backends — pure for tests, effectful for prod
val (finalState, result) = program.run(Map.empty)
```

**Use Free / ZPure when:**
- The program structure must be inspectable or optimizable before running
- Multiple interpreters: production, test, dry-run, serialized log
- Building embedded DSLs or query compilers

**Don't use when:** you just need a service layer — tagless final or concrete ZIO is simpler.

---

## Typeclass Laws as Property Tests

Laws make typeclasses trustworthy. Always test custom instances.

```scala
import zio.test.*
import zio.prelude.*

// Functor identity law: map(identity) == identity
def covariantIdentityLaw[F[+_]: Covariant, A](gen: Gen[Any, F[A]]) =
  test("identity") {
    check(gen)(fa => assertTrue(fa.map(identity) == fa))
  }

// Functor composition law: map(f andThen g) == map(f).map(g)
def covariantCompositionLaw[F[+_]: Covariant, A](gen: Gen[Any, F[A]]) =
  test("composition") {
    check(gen, Gen.function[Any, A, A](gen.map(_.asInstanceOf[A]))) { (fa, f) =>
      assertTrue(fa.map(f andThen f) == fa.map(f).map(f))
    }
  }

// Associative law: combine(combine(a,b),c) == combine(a,combine(b,c))
def associativeLaw[A: Associative](gen: Gen[Any, A]) =
  test("associativity") {
    check(gen, gen, gen) { (a, b, c) =>
      assertTrue((a <> b) <> c == a <> (b <> c))
    }
  }
```

**Minimum law coverage per typeclass:**
- `Covariant`: identity, composition
- `Contravariant`: identity, composition (reversed)
- `Associative`: associativity
- `Identity`: left/right identity
- `Equal`: reflexivity, symmetry, transitivity
- `Ord`: totality, antisymmetry, transitivity

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Skipping law tests for custom instances | Silent correctness bugs | Property-test every custom typeclass instance |
| `Monad` constraint when `Applicative` suffices | Forces sequential execution | Use `ForEach`/`zipWithPar` to retain parallelism |
| Manual recursion on `Fix[F]` | Error-prone, no reuse | Use `cata`/`ana` or droste |
| Free monad for simple service layers | Over-engineering | Concrete ZIO or tagless final |
| Optics for flat single-level data | Unnecessary indirection | Direct field access |
| `bimap` for error translation at every layer | Leaking internal error types | Define a single `AppError` sum at each bounded context |
| Contravariant confused with covariant | Wrong variance, compile errors | Check: does `A => B` give `F[A] => F[B]` (co) or `F[B] => F[A]` (contra)? |
| `ZPure` for effects with real side effects | ZPure is pure-only | Use ZIO for real effects; ZPure for stateful computation |
