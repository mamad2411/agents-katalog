---
name: doc-style
description: "OCaml comment and ocamldoc writing style, in the voice of a POSIX manual page. Use whenever writing, rewording, reviewing or deleting any OCaml comment or documentation. Triggers on ocamldoc, odoc, doc comments, (** ... *), .mli documentation, .mld pages, documenting a function, type or module, and on any request to add, tidy, rewrite or strip OCaml comments."
---

# OCaml Comment and Documentation Style

Write ocamldoc the way a POSIX manual page is written. State what a thing is
and what it does, in full sentences, and stop.

Implementations carry no comments at all unless the code cannot speak for
itself.

This skill covers *what to write*. For odoc reference syntax, cross-package
links and build warnings, see the `ocaml-docs` skill.

## The Six Rules

1. **Full sentences.** Every doc comment is one or more complete sentences,
   each ending in a full stop. No fragments, no bullet-point shorthand, no
   trailing "...".
2. **Manpage voice.** Terse, declarative, present tense, third person. No "we",
   no "you", no "this function", no enthusiasm.
3. **No extraneous detail.** Document what a caller must know to call it.
   History, rationale, benchmarks, future plans and implementation trivia do
   not appear.
4. **No connectives.** No colons and no em dashes joining clauses. Split into
   separate sentences instead. Semicolons only inside a genuine list.
5. **User-facing, not internal.** Describe observable behaviour. Mention an
   internal only when the caller can observe it, such as time complexity,
   allocation behaviour, evaluation order or thread safety.
6. **`[f x y] is ...`.** A function's documentation opens with the function
   applied to its arguments in brackets, followed by `is`.

## Function Documentation

The doc comment follows the `val` declaration. Name the arguments in the
bracketed application and refer to them with `[x]` thereafter.

```ocaml
val length : t -> int
(** [length t] is the number of elements in [t]. *)

val find : string -> t -> element option
(** [find name t] is the element of [t] called [name], or [None] if [t] has
    no such element. *)

val is_bot : t -> bool
(** [is_bot u] is [true] if [u] is a bot user. *)
```

Use `is` whenever the function has a meaningful result. Reserve an active verb
for functions that exist for their effect.

```ocaml
val flush : out_channel -> unit
(** [flush oc] writes the buffered bytes of [oc] to its underlying file. *)

val set : t -> key:string -> value:string -> unit
(** [set t ~key ~value] binds [key] to [value] in [t]. Any previous binding of
    [key] is dropped. *)
```

Effectful constructors are still `is`.

```ocaml
val create : unit -> t
(** [create ()] is a new empty table. *)

val of_file : Fpath.t -> (t, Error.t) result
(** [of_file file] is the configuration parsed from [file]. The error holds a
    human readable message suitable for a command line tool. *)
```

Document optional arguments in their own sentence, and give the default.

```ocaml
val sub : ?start:int -> ?len:int -> string -> string
(** [sub ~start ~len s] is the substring of [s] of length [len] starting at
    [start]. [start] defaults to [0]. [len] defaults to the remainder of [s]
    after [start]. *)
```

Failure conditions go last, as tags.

```ocaml
val get : t -> string -> element
(** [get t name] is the element of [t] called [name].

    @raise Not_found if [t] has no element called [name]. *)
```

Prefer naming arguments in the bracketed application over `@param` tags.
`@param` restates the signature and reads nothing like a manual page.

## Type and Value Documentation

A type is documented by what its values represent, not by its representation.

```ocaml
type t
(** The type for users. *)

type id = string
(** The type for user identifiers. An identifier is unique within a workspace
    and stable across renames. *)

type level = Debug | Info | Warning | Error
(** The type for message severities, in increasing order of severity. *)
```

Constructors and record fields take a doc comment only when the name is not
enough.

```ocaml
type t = {
  name : string;  (** The display name. It is not unique. *)
  id : id;
  created : Ptime.t;  (** The creation time, in UTC. *)
}
```

## Module Documentation

The first line of an `.mli` is a synopsis in the shape of a manpage `NAME`
line. A blank line follows, then the description.

```ocaml
(** User accounts and profiles.

    Users are workspace members. A user is identified by an {!type:id} that is
    stable for the lifetime of the account. Profile fields are populated
    lazily and may be absent on users who have never signed in. *)
```

Keep the description to what a caller needs before reading the values below
it. Use `{1 Section}` headings once the interface is long enough to need them,
and name the sections after what they hold, such as `{1 Users}` or
`{1 Predicates and comparisons}`.

## Rewrites

| Instead of | Write |
|------------|-------|
| `(** Returns the length of the buffer *)` | `(** [length b] is the number of bytes in [b]. *)` |
| `(** [parse s] parses [s]: it splits on commas and builds a record. *)` | `(** [parse s] is the record encoded in [s]. *)` |
| `(** [send t msg] sends a message — note this blocks. *)` | `(** [send t msg] sends [msg] on [t]. It blocks until [msg] has been written. *)` |
| `(** This function is used internally by the scheduler to requeue fibers. *)` | Delete it, or make the value private. |
| `(** Fast lookup (uses a hashtable). *)` | `(** [find t k] is the value bound to [k] in [t]. Lookup is constant time. *)` |
| `(** TODO: document *)` | Write the sentence. |

## Banned Words and Shapes

Delete these on sight.

- `This function`, `This value`, `This module` as an opener. Name the thing.
- `Basically`, `simply`, `just`, `obviously`, `of course`.
- `Note that`, `Please note`, `Be aware`. State the fact as a sentence.
- `Internally`, `under the hood`, `behind the scenes`.
- `Helper for`, `Wrapper around`, `Convenience function`.
- A colon or em dash introducing an explanatory clause.
- A parenthetical that repeats the type signature.
- Author names, dates, ticket numbers and changelog entries.

## Comments in Implementations

**Default is no comment.** If a reader who knows OCaml can see what the code
does, the code says it already. Naming a value is better than commenting it.

Delete on sight:

- Comments that restate the code, such as `(* increment i *)`.
- Section banners and boxes, such as `(* ---- Helpers ---- *)`.
- Commented-out code. Version control keeps it.
- Narration of obvious control flow, such as `(* loop over the list *)`.
- Attribution, dates and changelog entries.
- Doc comments in an `.ml` that has an `.mli`. The documentation belongs in
  the interface, and a second copy will drift.

Write a comment only for something the code cannot state:

- A citation for behaviour mandated elsewhere, such as `(* RFC 8259 §7. *)`.
- An invariant a reader cannot check locally, such as `(* [buf] is never
  empty here, see [refill]. *)`.
- A deliberate deviation or workaround, with the reason it exists.
- A justification for an unsafe or unusual operation.
- Why the obvious approach was rejected, when someone would otherwise
  reinstate it.

Kept comments are full sentences in `(* ... *)`, placed on the line above the
code they explain.

```ocaml
(* Bad. *)
let decode s =
  (* get the length *)
  let n = String.length s in
  (* loop over the characters *)
  let b = Buffer.create n in
  ...

(* Good. *)
let decode s =
  let b = Buffer.create (String.length s) in
  ...

(* Good. The comment states what the code cannot. *)
let decode s =
  (* RFC 4648 §3.2 requires padding to be rejected in strict mode. *)
  if strict && String.length s mod 4 <> 0 then invalid_arg "decode";
  ...
```

## Checklist

Before committing documentation:

- [ ] Every exported value has a doc comment.
- [ ] Every function doc opens with `[f x y] is` or an active verb for an
      effect.
- [ ] Every argument named in the brackets is referred to in the prose.
- [ ] Every optional argument has its default stated.
- [ ] Every sentence is complete and ends in a full stop.
- [ ] No colons or em dashes join clauses.
- [ ] No sentence describes the implementation.
- [ ] No banned word from the list above survives.
- [ ] The `.ml` has no comment that the code already says.
- [ ] `dune build @doc` is clean.
