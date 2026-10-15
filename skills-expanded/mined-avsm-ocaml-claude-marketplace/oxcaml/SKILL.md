---
name: oxcaml
description: Working with the OxCaml extensions to OCaml. Use when the oxcaml compiler is available and you need high-performance, unboxing, stack allocation, data-race-free parallelism
---

You are writing code for the OxCaml compiler, a performance-focused fork of
OCaml with Jane Street extensions. This guide covers OxCaml-specific features.
You should already know standard OCaml.

**Current target**: OxCaml `5.2.0minus-39` — the **latest released
version**, shipping as `ocaml-variants.5.2.0+ox` on the OCaml 5.2
base. Later tags (`5.2.0minus-40`, `5.4.0-ox1`/`-ox2`) and main are
**unreleased** development, covered by
[CHANGES-unreleased.md](CHANGES-unreleased.md). Throughout these
guides, **any feature gated "minus-40+", "5.4.0-ox*", "5.4 base", or
"post-ox2" is unreleased** — don't use it unless targeting a compiler
built from main.

Change history, newest first — the upgrade guide at the bottom of each
file is the right starting point when bumping a project:

- [CHANGES-unreleased.md](CHANGES-unreleased.md) — everything after
  `5.2.0minus-39` (minus-40, the upstream-OCaml-5.4 merge, ox2, main)
- [CHANGES-38-39.md](CHANGES-38-39.md) — `5.2.0minus-38` → `5.2.0minus-39`
- [CHANGES-31-38.md](CHANGES-31-38.md) — `5.2.0minus-31` → `5.2.0minus-38`
- [CHANGES-25-31.md](CHANGES-25-31.md), [CHANGES-23-25.md](CHANGES-23-25.md)
  — earlier windows

### Quick Upgrade Flags (38 → 39)

When diagnosing build failures after a bump to minus-39, check these
first:

- **`unique_` / `once_` prefix syntax removed** — use
  `(x @ unique)` in patterns, `(e : @ unique)` on expressions.
  `local_` is kept.
- **`-extension labeled_tuples` no longer exists** —
  labeled tuples are always-on; repeated labels in one tuple are gone.
- **Mixed `float`+`float#` records now require `[@@flatten_floats]`**
  (hard error without it; such records get no unboxed `t#` version);
  all-`float64` records are mixed blocks
  (`[@@represent_as_float_array]` opts out). C layout asserts: v5 → v6.
- **`Stdlib_stable.Iarray` local API removed** — `( .:() )`
  and `*_local` functions gone (both survive only in
  `Stdlib_stable.IarrayLabels`).
- **`-ikinds` flag removed** — the ikinds checker is now the default;
  `-no-ikinds` opts out.
- **Scannable kind axes now meet instead of override** — an annotation
  can only lower an axis.
- **Magic number** 577 → 578 — rebuild everything including ppx
  rewriters.

See the *Breaking changes and upgrade guide* section of
CHANGES-38-39.md for an ordered checklist.

### Unreleased (after minus-39) — highlights

On unreleased tags / main only (details in CHANGES-unreleased.md):

- **OCaml 5.4 base** (`5.4.0-ox1`): `effect` becomes a keyword
  (escape: `-keywords 5.2` / `--enable-keyword-edition=5.2`), effect
  handler syntax (`| effect E, k ->`), `Stdlib.Iarray`,
  `Pqueue`/`Pair`/`Repr`, `[| |]` literal disambiguation, atomic
  record fields.
- **Runtime 4 retired**; SIMD primitives on `float array` removed;
  all-void variant constructors need
  `[@immediate_all_void_constructor]`; effect-handler cases force the
  function nonportable/stateful (all ox2).
- Mixed `float`+`float#` records no longer *require*
  `[@@flatten_floats]` (minus-40; default becomes non-flat);
  `[@atomic]` field restrictions; kind-`any` fields under
  `layouts_beta`; usable preemption (`Effect.Deep.Preemptible`,
  `Domain.Tick.with_`).
- `'a box` types, `int64_u`/`int32_u`/`nativeint_u` aliases,
  `val poly_`/`let poly_`, implicit kinds in structures (ox2);
  `array#`/`iarray#`, warnings 183/184 on by default, warning 220
  `redundant-modality` (post-ox2 main).
- Magic numbers 578 → 581 across the unreleased windows.

## Detailed Guides

For in-depth coverage of each feature, see:

| Feature | Guide |
|---------|-------|
| **Modes** (local, unique, once, portable, contended) | [SKILL-MODES.md](SKILL-MODES.md) |
| **Stack Allocation** (local_, stack_, exclave_) | [SKILL-STACK-ALLOCATION.md](SKILL-STACK-ALLOCATION.md) |
| **Unboxed Types** (float#, int32#, mixed blocks) | [SKILL-UNBOXED.md](SKILL-UNBOXED.md) |
| **Kinds** (value, float64, bits32, kind products) | [SKILL-KINDS.md](SKILL-KINDS.md) |
| **Uniqueness** (unique/aliased, once/many) | [SKILL-UNIQUENESS.md](SKILL-UNIQUENESS.md) |
| **Comprehensions** (list/array builders) | [SKILL-COMPREHENSIONS.md](SKILL-COMPREHENSIONS.md) |
| **SIMD** (vector types, SSE/AVX intrinsics) | [SKILL-SIMD.md](SKILL-SIMD.md) |
| **Templates** (ppx_template, mangling) | [SKILL-TEMPLATES.md](SKILL-TEMPLATES.md) |
| **Zero-Alloc** ([@zero_alloc] checking) | [SKILL-ZERO-ALLOC.md](SKILL-ZERO-ALLOC.md) |
| **Base Library** (OxCaml extensions) | [SKILL-BASE.md](SKILL-BASE.md) |
| **Core Library** (OxCaml extensions) | [SKILL-CORE.md](SKILL-CORE.md) |

---

## Quick Reference: Syntax Cheat Sheet

```ocaml
(* Stack allocation *)
let f () = exclave_ stack_ (1, 2)      (* allocate on stack, return local *)
let g (x @ local) = ...                 (* local parameter *)

(* Unboxed types *)
let x : float# = #3.14                  (* unboxed float *)
let y : int32# = #42l                   (* unboxed int32 *)
let b : bool# = #true                   (* unboxed bool (5.2.0minus-31+) *)
let u : unit# = #()                     (* unboxed unit (5.2.0minus-31+) *)
type t = { a : int; b : float# }        (* mixed block record *)

(* Modes on values *)
let f (x @ local unique once) = ...     (* multiple modes *)
val g : t @ global -> t @ local         (* in signatures *)

(* Kinds on types *)
type ('a : float64) t = ...             (* kind annotation *)
val f : ('a : value). 'a -> 'a          (* kind-polymorphic *)

(* Comprehensions *)
[ x * 2 for x = 1 to 10 when x mod 2 = 0 ]
[| y for y in arr when y > 0 |]

(* Labeled tuples *)
let pair = ~x:1, ~y:2                   (* labeled tuple *)
let ~x, ~y = pair                       (* destructuring *)

(* Immutable arrays — module is Stdlib_stable.Iarray on released
   compilers (Stdlib.Iarray only on the unreleased 5.4 base) *)
let arr : int iarray = [: 1; 2; 3 :]
let x = Stdlib_stable.Iarray.get arr 0
                            (* a.:(n) needs Stdlib_stable.IarrayLabels *)

(* Effect handlers — UNRELEASED (5.4 base; forces fn
   nonportable/stateful) *)
let run c = match c () with
  | v -> v
  | effect Poke, k -> Effect.Deep.continue k ()

(* Box types — UNRELEASED (5.4.0-ox2+): boxed version of an unboxed
   type: float# box = float;  r# box = r *)

(* Unboxed number aliases — UNRELEASED (5.4.0-ox2+) *)
let n : int64_u = #42L      (* int64_u = int64#, int32_u, nativeint_u *)

(* Unboxed tuple destructuring - use #(...) pattern *)
let #(a, b) = some_unboxed_pair
let #(x, y, z) = fork_join3 par f1 f2 f3

(* Zero-alloc annotation *)
let[@zero_alloc] fast_add x y = x + y

(* Borrowing (5.2.0minus-31+) - prefix form cooperating with uniqueness *)
let r = ref 0 in f (borrow_ r)          (* typical: function argument *)

(* Implicit kinds (5.2.0minus-31+; also in structures since ox2) *)
module type S = sig
  [@@@implicit_kind: ('elt : word)]
  type 'elt collection                  (* 'elt defaults to kind word *)
end
```

---

## 1. Modes

Modes track runtime properties of values. Each mode axis is independent.

### Mode Axes

| Axis | Values | Default | Purpose |
|------|--------|---------|---------|
| Locality | `local`, `global` | `global` | Where value lives (stack vs heap) |
| Uniqueness | `unique`, `aliased` | `aliased` | Number of references |
| Linearity | `once`, `many` | `many` | How often closures can be called |
| Portability | `portable`, `corruptible`, `shareable`, `nonportable` | `nonportable` | Cross-thread safety |
| Contention | `uncontended`, `shared`, `corrupted`, `contended` | `uncontended` | Thread access patterns |
| Visibility | `read_write`, `read`, `write`, `immutable` | `read_write` | Mutable-field access rights |
| Statefulness | `stateless`, `reading`, `writing`, `stateful` | `stateful` | Closed-over mutable state |

Portability/contention and visibility/statefulness are 4-element
**diamonds** (`shared`/`corrupted` and `read`/`write` are
incomparable). `observing` was renamed to `reading` in 5.2.0minus-36.
This table is the user-facing subset — the compiler also tracks
`yielding`, `forkable`, and `staticity` axes.
See [SKILL-MODES.md](SKILL-MODES.md).

### Syntax

```ocaml
(* On parameters *)
let f (x @ local) = ...
let f (x @ local unique) = ...       (* multiple modes *)

(* On return types in signatures *)
val f : t @ local -> t @ global
val g : t @ unique once -> t @ aliased many

(* On expressions *)
let x = (expr : t @ local)

(* On let bindings — local_ is the only legacy prefix (global is default) *)
let local_ x = ...

(* On record fields - modalities *)
type t = {
  global_ data : int;                 (* always global *)
  mutable x : int @@ aliased;         (* aliased modality *)
}
```

### Subtyping Rules

More restrictive modes can be used where less restrictive are expected:
- `global` ≤ `local` (can use global where local expected)
- `unique` ≤ `aliased` (can use unique where aliased expected)
- `many` ≤ `once` (can use many where once expected)
- `portable` ≤ `shareable`/`corruptible` ≤ `nonportable` (diamond:
  `shareable` and `corruptible` are incomparable)
- `uncontended` ≤ `shared`/`corrupted` ≤ `contended` (diamond)

---

## 2. Stack Allocation (Locality)

Stack-allocated values avoid GC overhead but cannot escape their scope.

### Key Constructs

```ocaml
(* Allocate on stack *)
let f () =
  let local_ x = (1, 2) in            (* stack-allocated tuple *)
  ...

(* Force stack allocation *)
let f () =
  stack_ (1, 2)                        (* explicitly stack-allocate *)

(* Return local value from function *)
let f () = exclave_
  stack_ (1, 2)                        (* return value allocated in caller's frame *)

(* Combined pattern for local returns *)
let f () = exclave_ stack_ (make_tuple ())
```

### Rules

1. Local values CANNOT escape their defining scope (no storing in globals, no returning without `exclave_`)
2. Local values CAN reference global values
3. Global values CANNOT reference local values
4. `exclave_` allocates in caller's stack frame and must be at tail position

### Common Patterns

```ocaml
(* Process local data without allocation *)
let sum_pairs (pairs @ local) =
  List.fold_left (fun acc (a, b) -> acc + a + b) 0 pairs

(* Return local from function *)
let make_pair x y = exclave_ stack_ (x, y)

(* Local references for accumulators *)
let count_positives lst =
  let local_ r = ref 0 in
  List.iter (fun x -> if x > 0 then r := !r + 1) lst;
  !r
```

---

## 3. Unboxed Types

Unboxed types store values directly without heap allocation.

### Built-in Unboxed Types

```ocaml
(* Numeric types - # suffix means unboxed *)
float#     (* 64-bit float, kind float64 *)
int32#     (* 32-bit int, kind bits32 *)
int64#     (* 64-bit int, kind bits64 *)
nativeint# (* native int, kind word *)
float32#   (* 32-bit float, kind float32 *)
int8#      (* 8-bit int - untagged, kind bits8 *)
int16#     (* 16-bit int - untagged, kind bits16 *)
int#       (* native int - untagged *)
char#      (* 8-bit char - untagged, same layout as int8# *)
bool#      (* 8-bit bool, kind bits8 (5.2.0minus-31+) *)
unit#      (* zero-size, kind void (5.2.0minus-31+) *)

(* Literals use # prefix *)
let x : float# = #3.14
let y : int32# = #42l
let z : int64# = #100L
let w : float32# = #1.0s
let a : int8# = #42s       (* int8# literal *)
let b : int16# = #42S      (* int16# literal *)
let c : char# = #'x'       (* char# literal *)
let d : bool# = #true      (* bool# literal - also #false *)
let e : unit# = #()        (* unit# literal *)

(* Boxed versions (heap-allocated) *)
let a : float = 3.14       (* boxed *)
let b : float# = #3.14     (* unboxed *)
```

### Untagged Int Arrays (New in 5.2.0minus-25)

Arrays of untagged types are packed for memory efficiency:

```ocaml
(* Untagged int arrays - tightly packed *)
let bytes : int8# array = [| #0s; #1s; #255s |]
let shorts : int16# array = [| #0S; #1S; #32767S |]
let ints : int# array = [| #0m; #1m; #42m |]   (* int# literal suffix is m *)
let chars : char# array = [| #'a'; #'b'; #'c' |]

(* int8# array: 1 byte per element *)
(* int16# array: 2 bytes per element *)
(* int# array: native word size per element *)
```

### Unboxed Records

```ocaml
(* Unboxed record - stored inline, not heap-allocated *)
type point = #{ x : float#; y : float# }

(* Create unboxed record *)
let p : point = #{ x = #1.0; y = #2.0 }

(* Access fields *)
let get_x (p : point) = p.#x
```

### Unboxed Tuples

```ocaml
(* Unboxed tuple syntax *)
type pair = #(float# * int32#)

let p : #(float# * int32#) = #(#1.0, #42l)
```

### Mixed Blocks

Records can mix boxed and unboxed fields:

```ocaml
type mixed = {
  name : string;          (* boxed *)
  value : float#;         (* unboxed, stored flat *)
  count : int32#;         (* unboxed *)
}
```

### or_null Type

Non-allocating option for **value** types (`Null` is encoded without a box).
The argument must be a non-null value type — `float# or_null` is rejected:

```ocaml
type 'a or_null = Null | This of 'a

(* Use instead of option to avoid the Some allocation *)
let find (arr : string array) idx : string or_null =
  if idx < Array.length arr then This arr.(idx)
  else Null

(* Custom or_null types: any two-constructor variant (one nullary,
   one unary) can opt into the same non-allocating encoding *)
type 'a maybe = Nope | Yep of 'a [@@or_null]
type no_param = A | B of int [@@or_null]   (* payload shape free (ox2+) *)
```

---

## 4. Kinds

Kinds classify types by their runtime representation.

### Kind Hierarchy

```
any                           (* any layout *)
├── value                     (* standard OCaml boxed values *)
├── float64                   (* 64-bit floats *)
├── float32                   (* 32-bit floats *)
├── bits8                     (* 8-bit integers: int8#, bool#, char# *)
├── bits16                    (* 16-bit integers: int16# *)
├── bits32                    (* 32-bit integers *)
├── bits64                    (* 64-bit integers *)
├── word                      (* native word size *)
├── vec128 / vec256           (* SIMD vectors *)
└── void                      (* zero-width; unit# lives here *)
```

### Kind Annotations

```ocaml
(* On type parameters *)
type ('a : float64) container = ...

(* On type variables in signatures *)
val f : ('a : value). 'a -> 'a
val g : ('a : bits64). 'a -> 'a

(* On abstract types *)
type t : float64

(* Kind products for unboxed tuples *)
type pair : float64 & bits32    (* unboxed pair of float# and int32# *)
```

### Kind Abbreviations

```ocaml
value           = value_or_null non_null separable
immediate       = value non_pointer     (* crosses all modal axes *)
immediate64     = value non_pointer64
mutable_data    = value mod non_float
immutable_data  = value mod non_float immutable
```

### Mode Bounds on Kinds

Kinds can specify which modes a type crosses:

```ocaml
(* Type that cannot be used at mode local *)
type t : value mod global

(* Type that is always portable *)
type t : value mod portable
```

---

## 5. Uniqueness

Track values with exactly one reference for safe mutation/deallocation.

### Modes

- `unique`: Single reference exists
- `aliased`: Multiple references may exist

### Syntax

```ocaml
(* Unique parameter - consumed by function *)
val free : t @ unique -> unit

(* Aliased return - may have multiple references *)
val duplicate : t -> t * t @ aliased

(* Once closures - can only be invoked once *)
val delay_free : t @ unique -> (unit -> unit) @ once
```

### Uniqueness Rules

```ocaml
(* OK: match then use uniquely *)
let ok t =
  match t with
  | Con { field } -> free t

(* ERROR: using parts twice *)
let bad t =
  match t with
  | Con { field } ->
    free_field field;   (* uses field *)
    free t              (* uses t which contains field *)

(* OK: different branches *)
let ok t =
  match t with
  | Con { field } ->
    if cond then free_field field
    else free t
```

### Aliased Modality

Store aliased values in unique containers:

```ocaml
type 'a aliased_box = { value : 'a @@ aliased } [@@unboxed]

(* Container is unique but contents are aliased *)
val push : 'a @ aliased -> 'a aliased_box list @ unique -> 'a aliased_box list @ unique
```

---

## 6. Comprehensions

Python/Haskell-style list and array builders.

### List Comprehensions

```ocaml
(* Basic *)
[ x * 2 for x = 1 to 10 ]

(* With filter *)
[ x for x = 1 to 100 when x mod 2 = 0 ]

(* Nested iteration *)
[ (x, y) for x = 1 to 3 for y = 1 to 3 ]

(* Iterate over list *)
[ String.uppercase s for s in strings ]

(* Multiple conditions *)
[ x + y for x = 1 to 10 for y = 1 to 10 when x < y when x + y < 15 ]

(* Simultaneous iterators (sources evaluated once; still a product) *)
[ x + y for x = 1 to 3 and y = 10 to 12 ]
```

### Array Comprehensions

```ocaml
(* Same syntax with [| |] *)
[| x * x for x = 1 to 10 |]

(* Iterate over array *)
[| f elem for elem in source_array |]
```

### Immutable Array Comprehensions

```ocaml
[: x for x = 1 to 10 when x mod 2 = 0 :]
```

### Key Differences: `for` vs `and`

Both produce the **Cartesian product** — comprehensions cannot zip.

- `for ... for ...`: Nested (inner source re-evaluated each outer iteration;
  inner iterators may reference outer variables)
- `for ... and ...`: Sources evaluated once upfront; iterators are
  independent (cannot reference each other); enables exact-size array
  pre-allocation

```ocaml
(* Both are 9 elements *)
[ (x, y) for x = 1 to 3 for y = 1 to 3 ]
[ (x, y) for x = 1 to 3 and y = 10 to 12 ]
(* = [(1,10); (1,11); (1,12); (2,10); ...] *)
```

---

## 7. SIMD Vector Types

128-bit and 256-bit SIMD vectors for parallel numeric operations.

### Types

```ocaml
(* 128-bit vectors *)
int8x16    int8x16#      (* 16 x 8-bit ints *)
int16x8    int16x8#      (* 8 x 16-bit ints *)
int32x4    int32x4#      (* 4 x 32-bit ints *)
int64x2    int64x2#      (* 2 x 64-bit ints *)
float32x4  float32x4#    (* 4 x 32-bit floats *)
float64x2  float64x2#    (* 2 x 64-bit floats *)

(* 256-bit vectors *)
int8x32    int8x32#
int32x8    int32x8#
float64x4  float64x4#
(* etc. *)
```

### Usage

```ocaml
open Ocaml_simd_sse

let v = Float32x4.set 1.0 2.0 3.0 4.0
let v = Float32x4.sqrt v
let x, y, z, w = Float32x4.to_tuple v

(* Load from arrays *)
let v = Int8x16.String.get text ~byte:0
```

### C Stubs

```ocaml
external vec_op : (int8x16[@unboxed]) -> (int8x16[@unboxed]) =
  "boxed_stub" "unboxed_stub"
```

---

## 8. Templates (ppx_template)

Generate multiple copies of code with different modes/kinds.

### Mode Templates

```ocaml
(* Define once, get local and global versions *)
let%template[@mode m = (global, local)] id
  : 'a. 'a @ m -> 'a @ m
  = fun x -> x

(* Generates: id (global) and id__local *)

(* Instantiate *)
let f x = (id [@mode local]) x
```

### Kind Templates

```ocaml
let%template[@kind k = (value, float64)] id
  : ('a : k). 'a -> 'a
  = fun x -> x

(* Generates: id (value) and id__float64 *)
```

### Exclave Conditional

```ocaml
let%template[@mode m = (global, local)] make_pair x y =
  (x, y) [@exclave_if_local m]

(* local version gets: exclave_ (x, y) *)
```

### Alloc Templates

```ocaml
let%template rec map
  : f:('a -> 'b @ m) -> 'a list -> 'b list @ m
  = fun ~f list ->
    match[@exclave_if_stack a] list with
    | [] -> []
    | hd :: tl -> f hd :: (map [@alloc a]) ~f tl
[@@alloc a @ m = (heap_global, stack_local)]
```

### Portable Functors

```ocaml
(* Short form for portable/nonportable functor variants *)
module%template.portable Make (M : S) : T
```

### Default Floating Attributes

```ocaml
[%%template:
[@@@mode.default m = (global, local)]

val min : t @ m -> t @ m -> t @ m
val max : t @ m -> t @ m -> t @ m]
```

---

## 9. Zero-Alloc Checking

Compile-time verification that functions don't allocate.

### Basic Usage

```ocaml
(* Check function doesn't allocate *)
let[@zero_alloc] fast_add x y = x + y

(* Allow local/stack allocations *)
let[@zero_alloc] with_local_pair x y =
  let p = stack_ (x, y) in
  fst p + snd p

(* Only check in optimized builds *)
let[@zero_alloc opt] complex_func x = ...

(* Strict: no allocation even on error paths *)
let[@zero_alloc strict] very_strict x = ...
```

### Assume Annotations

```ocaml
(* Trust this function is zero-alloc *)
let[@zero_alloc assume] external_wrapper x = external_func x

(* Assume for error paths *)
let[@cold][@zero_alloc assume error] handle_error e =
  log_error e;
  default_value
```

### In Signatures

```ocaml
val[@zero_alloc] f : int -> int
val[@zero_alloc strict] g : t -> t
val[@zero_alloc arity 2] h : int -> int -> int
```

### File-Level

```ocaml
[@@@zero_alloc all]  (* All functions must be zero-alloc *)

let[@zero_alloc ignore] allowed_to_alloc x = [x]  (* Opt out *)
```

---

## 10. Parallelism & Capsules

Safe parallel programming with thread isolation.

### Contention Modes

- `contended`: May be accessed from multiple threads concurrently
- `shared` / `corrupted`: intermediate diamond points (see section 1 table)
- `uncontended`: Single-thread access

### Portability Modes

- `portable`: Safe to move across thread boundaries, captures all values at contended
- `shareable` / `corruptible`: intermediate diamond points
- `nonportable`: Thread-local only, captures uncontended mutable state

### Capsules (Experimental)

Capsules isolate mutable state for safe parallelism:

```ocaml
(* Capsule contains thread-local mutable state *)
type 'a capsule

(* Access requires entering capsule context *)
val with_capsule : 'a capsule -> ('a @ local -> 'b) -> 'b
```

### Preemption (Experimental, UNRELEASED — minus-40+)

On the released `minus-39`, only groundwork exists: the
`Effect.Preemption` effect constructor and
`Domain.Tick.acquire ~interval_usec`/`release` (tick frequency). The
usable API is unreleased: run code under
`Effect.Deep.Preemptible.match_with`/`try_with` (whose handler has a
signal-safe `tickc : unit -> tick_outcome` field returning `Preempt` or
`Continue`), with ticks from `Domain.Tick.acquire` or the scoped
`Domain.Tick.with_`. A preempted fiber performs the `Effect.Preemption`
effect. Default-off; effectively requires a compiler built with
`--enable-poll-insertion`.

### Effect Handlers and Modes (UNRELEASED — 5.4 base)

Upstream 5.4's `match ... with effect E, k -> ...` syntax arrives with
the unreleased 5.4 rebase, but a function containing effect cases is
forced **nonportable and stateful** (5.4.0-ox2) — you cannot
pattern-match on effects inside a `portable` or `stateless` function.

---

## 11. Borrowing (5.2.0minus-31+)

The `borrow_` keyword is a prefix expression form (`borrow_ e`) that
cooperates with the uniqueness analysis. It is valid in **exactly
three positions** — anywhere else is a hard "invalid borrowing
context" error:

```ocaml
let update_if_positive r =
  if !r > 0 then f (borrow_ r)     (* common: function argument *)

let y = borrow_ r in ...           (* let-binding RHS *)

match borrow_ r with _ -> ...      (* match scrutinee *)
```

Diagnostics:

- **Warning 216 `use-during-borrowing`** — "Use of a value during an
  active borrow." Raised when a value is used while being borrowed.
- **Error `Unique_use_during_borrowing`** — the uniqueness analysis
  detected a conflict between a borrow and a unique use.

Use `borrow_` where a callee only reads/writes through a unique value
transiently and you want to keep the unique reference after the call.

---

## 12. Implicit Kinds in Signatures and Structures (5.2.0minus-31+)

A floating `[@@@implicit_kind: ...]` attribute declares that specific
type-variable names default to a chosen kind. It saves repetitive
per-declaration annotations. Signatures-only on released compilers
(allowed in structures since the unreleased 5.4.0-ox2):

```ocaml
module type Word_collection = sig
  [@@@implicit_kind: ('elt : word)]

  type 'elt collection
  val singleton : 'elt -> 'elt collection
  val length : 'elt collection -> int
end
```

Multiple names at once:

```ocaml
[@@@implicit_kind: ('a : immediate) * ('b : immediate)]
val swap : 'a * 'b -> 'b * 'a
```

Rules: implicit kinds can't be overridden in nested signatures, don't
propagate through `include`, apply inside `constraint` clauses, and are
not legal in structures (until the unreleased ox2). See
[SKILL-KINDS.md](SKILL-KINDS.md) for details.

---

## 13. Miscellaneous Extensions

### Labeled Tuples

```ocaml
(* Create *)
let point = ~x:10, ~y:20

(* Type *)
type point = x:int * y:int

(* Destructure *)
let ~x, ~y = point

(* Partial match (needs type annotation) *)
let get_x (p : x:int * y:int) =
  let ~x, .. = p in x

(* Function returning labeled tuple *)
val dimensions : image -> width:int * height:int
```

### Immutable Arrays

```ocaml
(* Syntax uses : instead of | *)
let arr : string iarray = [: "a"; "b"; "c" :]

(* Access — module is Stdlib_stable.Iarray on released compilers *)
let first = Stdlib_stable.Iarray.get arr 0

(* a.:(0) works only with Stdlib_stable.IarrayLabels open —
   the ( .:() ) operator was removed from Stdlib_stable.Iarray
   in minus-39 *)

(* Covariant - allows safe subtyping *)
let arr2 : obj iarray = (arr : sub_obj iarray :> obj iarray)
```

UNRELEASED (5.4 base): `Iarray` moves to `Stdlib`, and plain
`[| e1; e2 |]` literals disambiguate to `iarray` (or `floatarray`)
from the expected type.

### Include Functor

```ocaml
(* Instead of *)
module M = struct
  module T = struct
    type t = ...
    [@@deriving compare, sexp]
  end
  include T
  include Comparable.Make(T)
end

(* Write *)
module M = struct
  type t = ...
  [@@deriving compare, sexp]

  include functor Comparable.Make
end
```

### Let Mutable

```ocaml
(* Mutable local variable - no allocation *)
let triangle n =
  let mutable total = 0 in
  for i = 1 to n do
    total <- total + i
  done;
  total
```

Restrictions: Cannot escape scope, no closure capture, single variable only.

### Polymorphic Parameters

```ocaml
(* Function taking polymorphic argument *)
let create (f : 'a. 'a field -> 'a) =
  { a = f A; b = f B }

val create : ('a. 'a field -> 'a) -> t
```

### Small Numbers

```ocaml
(* Types *)
float32   float32#
int8      int8#
int16     int16#
char#

(* Literals *)
1.0s    (* float32 *)
#1.0s   (* float32# *)
42s     (* int8 *)
#42s    (* int8# *)
42S     (* int16 *)
#42S    (* int16# *)
#'a'    (* char# *)

(* Arrays - now supported and packed! *)
int8 array    int8# array     (* 1 byte per element *)
int16 array   int16# array    (* 2 bytes per element *)
char# array                   (* 1 byte per element *)

(* Pattern matching with char# ranges *)
match c with
| #'a'..#'z' -> `lowercase
| #'A'..#'Z' -> `uppercase
| _ -> `other
```

### Module Strengthening

```ocaml
(* Instead of *)
sig type t = M.t end

(* Write *)
S with M
```

---

## Common Patterns

### Zero-Alloc Hot Path

```ocaml
let[@zero_alloc] process_batch (data @ local) =
  let local_ acc = ref 0 in
  for i = 0 to Array.length data - 1 do
    acc := !acc + process_item data.(i)
  done;
  !acc
```

### Local Allocation in Loop

```ocaml
let process_all items =
  List.iter (fun item ->
    let local_ temp = compute item in
    use temp
  ) items
```

### Unique Resource Management

```ocaml
type handle

val open_handle : unit -> handle @ unique
val use_handle : handle @ unique -> result * handle @ unique
val close_handle : handle @ unique -> unit

let with_handle f =
  let h = open_handle () in
  let result, h = use_handle h in
  close_handle h;
  result
```

### Mode-Polymorphic Function

```ocaml
let%template[@mode m = (global, local)] map_pair f (a, b) =
  ((f a, f b) [@exclave_if_local m])
```

### Kind-Polymorphic Container

```ocaml
type%template ('a : k) box = { contents : 'a }
[@@kind k = (value, float64, bits64)]
```

---

## Debugging Tips

1. **Mode errors**: Check if you're trying to return local data globally
2. **Kind errors**: Ensure type parameters have correct layout annotations
3. **Zero-alloc failures**: Use `-zero-alloc-checker-details-cutoff -1` for full details
4. **Template issues**: Check mangled names with `__suffix` pattern
5. **Mangled symbols** (UNRELEASED, 5.4.0-ox2+): pipe through `ocamlfilt` (installed
   with the compiler) — handles flat and structured mangling schemes
6. **Native debugging**: use the OxCaml LLDB build (`21.1.0+oxcaml0`);
   `b Module.fn` breakpoints and OCaml-syntax value printing work

---

## Library Dependencies

### Core Libraries

- **`stdlib_stable`** (the released home for OxCaml types):
  `Iarray`/`IarrayLabels` (the `( .:() )` operator and `*_local`
  functions survive only in `IarrayLabels`), `Float32`, `Int8`,
  `Int16`, `Char_u`, `Or_null`, `Idx_imm`/`Idx_mut`
- **`Stdlib`** (UNRELEASED 5.4 base): `Iarray` moves upstream, plus
  new upstream modules `Pqueue`, `Pair`, `Repr`, `Dynarray`,
  `Atomic.Loc`
- **`base`**: Jane Street's standard library with comprehensive OxCaml mode support
  - **IMPORTANT**: Consult [SKILL-BASE.md](SKILL-BASE.md) for OxCaml-friendly functions!
  - Contains 116 modules with extensive local/exclave, mode, and unboxed type support
  - Key modules: `Modes` (modal wrappers), `Iarray` (immutable arrays with local ops),
    `Container_with_local`, and `__local` variants of most collection functions
- **`core`**: Extended library with I/O, async, and system features
  - See [SKILL-CORE.md](SKILL-CORE.md) for Iobuf, Time_ns, Bigstring extensions

### PPX Libraries

- **`ppx_template`**: Mode/kind polymorphism via code generation
  - See [SKILL-TEMPLATES.md](SKILL-TEMPLATES.md) for mangling details
- **`ppx_simd`**: SIMD shuffle/blend mask generation

### SIMD Libraries

- **`ocaml_simd`**: Base SIMD types
- **`ocaml_simd_sse`**: SSE intrinsics (128-bit)
- **`ocaml_simd_avx`**: AVX/AVX2 intrinsics (256-bit)
- See [SKILL-SIMD.md](SKILL-SIMD.md) for usage details
