---
name: scala-typelevel
description: >
  Advanced Scala 3 type system for library authors. TRIGGER when: designing
  library APIs with variance, implementing GADTs or typed expression trees,
  using type lambdas ([X] =>> F[X, E]), writing match types, deriving
  typeclasses with Mirror or Magnolia, using compiletime ops or inline
  definitions, phantom types for type-state tracking, path-dependent types,
  Shapeless 3 generic programming, or any question about making the compiler
  do verification work — shifting invariants from runtime to compile time.
  Use alongside /fp-patterns and /fp-advanced.
---

# Advanced Scala 3 Type System — Library Authors

## Variance — Producer vs Consumer

Variance controls how `F[A]` relates to `F[B]` when `A <: B`.

```scala
// Covariant F[+A]: Cat <: Animal ⟹ List[Cat] <: List[Animal]
// Use for: producers, read-only containers, return types
sealed trait Stream[+A]:
  def head: Option[A]          // A in output position — legal
  // def prepend(a: A): Stream[A]  // A in input position — compile error

// Contravariant F[-A]: Cat <: Animal ⟹ Encoder[Animal] <: Encoder[Cat]
// Use for: consumers, comparators, serializers, function inputs
trait Encoder[-A]:
  def encode(a: A): Json        // A only in input position — correct
  def contramap[B](f: B => A): Encoder[B] = b => encode(f(b))

given Encoder[Animal] = a => Json.obj("type" -> Json.str(a.species))
val catEncoder: Encoder[Cat] = summon[Encoder[Animal]]  // legal — contra

// Invariant F[A]: no subtyping in either direction
// Use for: mutable cells, codecs (A appears in both positions), typeclasses
trait Codec[A]:
  def encode(a: A): Bytes     // A contravariant here
  def decode(b: Bytes): A     // A covariant here → invariant overall

// Phantom type variance — variance without a value
sealed trait Read
sealed trait Write
class Handle[+P](private val fd: Int)  // covariant — Handle[Read&Write] <: Handle[Read]

def readHandle: Handle[Read]       = ???
def rwHandle:   Handle[Read&Write] = ???
val r: Handle[Read] = rwHandle     // compiles — covariance
```

**Rules for positions:**
- Return / output / upper bound → covariant (`+`)
- Parameter / input / lower bound → contravariant (`-`)
- Both input and output → invariant (no annotation)
- Mutable containers: always invariant, even if they "feel" like collections

---

## GADTs — Typed Expression Trees

GADTs encode type information per constructor, enabling type-safe interpreters.

```scala
// Each case refines the type parameter — the compiler tracks this
enum Expr[A]:
  case Lit(n: Int)                           extends Expr[Int]
  case BoolLit(b: Boolean)                   extends Expr[Boolean]
  case Add(l: Expr[Int], r: Expr[Int])       extends Expr[Int]
  case Eq[T](l: Expr[T], r: Expr[T])        extends Expr[Boolean]
  case If[T](cond: Expr[Boolean], t: Expr[T], f: Expr[T]) extends Expr[T]

// Evaluator: type-safe, no casting, exhaustive
def eval[A](e: Expr[A]): A = e match
  case Expr.Lit(n)       => n               // A =:= Int here
  case Expr.BoolLit(b)   => b               // A =:= Boolean here
  case Expr.Add(l, r)    => eval(l) + eval(r)
  case Expr.Eq(l, r)     => eval(l) == eval(r)
  case Expr.If(c, t, f)  => if eval(c) then eval(t) else eval(f)

// Type witnesses — prove type equality without a runtime value
sealed trait ===[A, B]
case class Refl[A]() extends (A === A)

def coerce[A, B](a: A, eq: A === B): B = eq match
  case Refl() => a  // compiler now knows A =:= B
```

Use GADTs for: type-safe DSLs, protocol state machines, heterogeneous typed collections, zero-cost proof terms.

---

## Type Lambdas and Higher-Kinded Types

```scala
// Type lambda: partially apply a multi-param type constructor
// Scala 3 native — no kind-projector plugin needed
type EitherStr[A]  = Either[String, A]       // simple alias
type EitherStrK    = [A] =>> Either[String, A]  // first-class type lambda

// Use in typeclass constraint
def validate[F[_]: Applicative, A](fas: List[F[A]]): F[List[A]] =
  fas.sequence

// Bifunctor — two type params
trait Bifunctor[F[_, _]]:
  def bimap[A, B, C, D](fab: F[A, B])(f: A => C)(g: B => D): F[C, D]

given Bifunctor[Either] with
  def bimap[A, B, C, D](e: Either[A, B])(f: A => C)(g: B => D): Either[C, D] =
    e.fold(a => Left(f(a)), b => Right(g(b)))

// Type lambda in constraint
def mapRight[F[_, _]: Bifunctor, E, A, B](fab: F[E, A])(f: A => B): F[E, B] =
  summon[Bifunctor[F]].bimap(fab)(identity)(f)

// Partially applied type constructor as argument
def process[M[_]: Monad](ma: M[Int]): M[String] = ma.map(_.toString)
process[[A] =>> Either[String, A]](Right(42))  // use type lambda as M
```

---

## Match Types — Compile-Time Type Dispatch

```scala
// Type-level pattern matching — result type depends on input type
type Elem[C] = C match
  case String        => Char
  case Array[t]      => t
  case Iterable[t]   => t

val c: Elem[String]       = 'x'   // Char
val i: Elem[Array[Int]]   = 42    // Int
val s: Elem[List[String]] = "hi"  // String

// Recursive match type for type-level computation
type TupleToUnion[T <: Tuple] = T match
  case EmptyTuple  => Nothing
  case h *: t      => h | TupleToUnion[t]

type Colors = TupleToUnion[(Red, Green, Blue)]  // Red | Green | Blue

// Dependent return type using match type
def head[T <: NonEmptyTuple](t: T): Head[T] = t.head.asInstanceOf[Head[T]]

// Keep match types shallow — deep recursion produces unreadable errors
// Break into named intermediates rather than one long chain
```

---

## Mirror — Typeclass Derivation Without Libraries

Scala 3's built-in reflection for generic programming.

```scala
import scala.deriving.Mirror
import scala.compiletime.*

trait Show[A]:
  def show(a: A): String

object Show:
  given Show[Int]    = _.toString
  given Show[String] = s => s""""$s""""
  given Show[Boolean]= _.toString

  // Derive for case classes (products)
  inline given derivedProduct[A](using m: Mirror.ProductOf[A]): Show[A] =
    val instances = summonAll[Tuple.Map[m.MirroredElemTypes, Show]]
    val labels    = constValueTuple[m.MirroredElemLabels].toList.map(_.toString)
    a =>
      val values = a.asInstanceOf[Product].productIterator.toList
      val fields = labels.zip(values).zip(instances.toList).map {
        case ((label, value), inst) =>
          s"$label=${inst.asInstanceOf[Show[Any]].show(value)}"
      }
      s"${m.toString}(${fields.mkString(", ")})"

  // Derive for enums/sealed traits (coproducts)
  inline given derivedSum[A](using m: Mirror.SumOf[A]): Show[A] =
    val instances = summonAll[Tuple.Map[m.MirroredElemTypes, Show]]
    a =>
      val ord = m.ordinal(a)
      instances.toList(ord).asInstanceOf[Show[A]].show(a)

  inline given derived[A](using Mirror.Of[A]): Show[A] = summonFrom {
    case m: Mirror.ProductOf[A] => derivedProduct(using m)
    case m: Mirror.SumOf[A]     => derivedSum(using m)
  }

case class User(name: String, age: Int) derives Show
enum Color derives Show:
  case Red, Green, Blue
```

For complex derivation, prefer **Magnolia** over raw `Mirror` — same power, far less code.

---

## Magnolia — Automatic Typeclass Derivation

```scala
import magnolia1.*

trait Validator[A]:
  def validate(a: A): List[String]  // list of violations, empty = valid

object Validator extends AutoDerivation[Validator]:
  // Combine all field validators into one product validator
  def join[T](ctx: CaseClass[Validator, T]): Validator[T] = value =>
    ctx.params.toList.flatMap { param =>
      param.typeclass.validate(param.deref(value))
        .map(msg => s"${param.label}: $msg")
    }

  // Delegate to the matching subtype
  def split[T](ctx: SealedTrait[Validator, T]): Validator[T] = value =>
    ctx.choose(value) { sub => sub.typeclass.validate(sub.cast(value)) }

  // Primitives
  given Validator[String]  = s => if s.isEmpty then List("must not be empty") else Nil
  given Validator[Int]     = n => if n < 0 then List("must be non-negative") else Nil
  given Validator[Boolean] = _ => Nil
  given [A: Validator]: Validator[Option[A]] = {
    case None    => Nil
    case Some(a) => summon[Validator[A]].validate(a)
  }

// One-liner derivation
case class Address(street: String, city: String, zip: String) derives Validator
case class User(name: String, age: Int, address: Address) derives Validator

User("", -1, Address("", "London", "SW1")).validate
// List("name: must not be empty", "age: must be non-negative", "address.street: must not be empty")
```

**Magnolia vs Mirror:**
- **Magnolia**: richer API (`label`, `annotations`, `default`), fewer inline errors → default for typeclass derivation
- **Mirror**: no dependency, lower-level, good for simple cases or when you control the whole typeclass hierarchy
- **Shapeless 3**: HList-style generic programming, poly functions, type-level proofs → only when Magnolia can't express it

---

## `compiletime` — Shifting Verification to Compile Time

```scala
import scala.compiletime.*
import scala.compiletime.ops.int.*

// Compile-time constants via ValueOf / constValue
inline def greet[N <: Int & Singleton]: String =
  "hello " * constValue[N]

greet[3]  // "hello hello hello " — computed at compile time

// Compile-time assertions in library APIs
inline def requirePositive[N <: Int](using ValueOf[N]): Unit =
  inline if constValue[N] <= 0 then error("N must be a positive literal")

// Type-level arithmetic
type Half[N <: Int]   = N / 2
type Double[N <: Int] = N * 2
val x: Half[8] = 4  // type is 4

// summonAll: gather instances for a Tuple of types
inline def instances[Ts <: Tuple, F[_]]: List[F[?]] =
  inline erasedValue[Ts] match
    case _: EmptyTuple => Nil
    case _: (h *: t)   => summonInline[F[h]] :: instances[t, F]

// erasedValue: type-level dispatch without a runtime value
inline def zero[A]: A = inline erasedValue[A] match
  case _: Int     => 0.asInstanceOf[A]
  case _: Long    => 0L.asInstanceOf[A]
  case _: String  => "".asInstanceOf[A]
  case _          => error("No zero for this type")
```

---

## Singleton and Literal Types

```scala
// Literal singleton types — the exact value is the type
val x: 42      = 42
val s: "hello" = "hello"
val b: true    = true

// Refined construction — reject bad inputs at compile time
opaque type Port = Int
object Port:
  inline def apply(n: Int): Port =
    inline if n < 1 || n > 65535 then
      error("Port must be between 1 and 65535")
    else n

val http: Port = Port(80)       // compiles
// val bad: Port = Port(99999) // compile error

// Narrowing via asMatchable + singleton pattern
def describe(x: Int | String): String = (x: @unchecked) match
  case n: Int    => s"number $n"
  case s: String => s"string $s"
```

---

## Anti-Patterns for Library Authors

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Invariant where covariant suffices | Callers can't pass subtypes | Check: only output positions? → `+A` |
| Covariant mutable container | Unsound (`Array[+A]` is a Java mistake) | Invariant for anything mutable |
| `asInstanceOf` instead of GADT match | Runtime `ClassCastException` | Let the GADT refine the type for you |
| Raw `Mirror` for complex derivation | Hundreds of lines of inline code | Use Magnolia — same power, 10× less code |
| `implicit` keyword | Scala 2 — confuses resolution | `given`/`using` always |
| Kind-projector plugin | Scala 2 dependency | Native type lambdas `[X] =>> F[X, E]` |
| Long recursive match types | Unreadable compiler errors | Break into named intermediate type aliases |
| `compiletime.ops` for business logic | Errors are cryptic, macros are fragile | Only for genuine type-level proofs in library APIs |
| Exposing `Mirror` in public API | Couples users to derivation internals | Expose only `derives` and the typeclass interface |
| Over-annotating variance | Fights the compiler on positions | Trust the compiler's variance error; fix the design |
